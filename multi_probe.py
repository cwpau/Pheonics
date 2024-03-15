#import modules
import csv
import pandas as pd
import os

#####Manual input#########################################################################
#####Coordinate transform coefficients Pheonics<--->Paraview/Real Coordinates
x0 = 8.415319e5
y0 = 8.134692e5
z0 = -9.557

# vtk_list = ['']
##########################################################################################
working_folder = __file__
working_folder = working_folder.rpartition('\\')[0]

vtk_list = []
run_folder = working_folder
for file in os.listdir(run_folder):
    if file.endswith(".vtk"):
        print(os.path.join(run_folder, file))
        vtk_list.append(os.path.join(file))

if not vtk_list:    #go find other files in run folder if no vtk found in main folder
    run_folder = working_folder + '\Run'
    for file in os.listdir(run_folder):
        if file.endswith(".vtk"):
            print(os.path.join(run_folder, file))
            vtk_list.append(os.path.join(file))
print(vtk_list)

# absolute path to import module (put the trace_function.py in same folder with this script)
import importlib.util
import sys
spec = importlib.util.spec_from_file_location("trace_function", working_folder+"\\trace_function.py")
foo = importlib.util.module_from_spec(spec)
sys.modules["trace_function"] = foo
spec.loader.exec_module(foo)
import trace_function as tf
destination_folder = working_folder

#AP csv file location
ap_z_file = working_folder+'\Assessment_Pt\AP_z.csv'
ap_file = working_folder+'\Assessment_Pt\AP.csv'
print('getcwd:      ', os.getcwd())
print('__file__:    ', working_folder)

#read AP coordinates
listofap = []
with open(ap_z_file, 'rt')as f:
  data = csv.reader(f)
#   next(data)    #skip first line
  for row in data:
    # print(row)
    # row=row[0].split(" ") ###uncomment only if all data is in 1 column and separated by spaces
    # print(row)
    row = [x for x in row]   #convert str to floats
    # print(row)
    # print(float(row[0])-x0, float(row[1])-y0, float(row[2])-z0) #check

    row = [float(row[0])-x0, float(row[1])-y0, float(row[2])-z0]    #transform geographical coordinates to model coorddinates
    # print(row)
    listofap.append(row)

#read AP IDs for insert at result
df_ap = pd.read_csv(ap_file)
print(df_ap)



print(listofap) #
# print("LIST LENGTH",len(listofap))
# print("2nd Y", listofap[1][1])
# print(type(listofap[1][1]))

def createprobe(xyz, count, phivtk_source):
    # create a new 'Probe Location'
    probeLocation1 = ProbeLocation(registrationName=f'ProbeLocation{count}', Input=phivtk_source,
        ProbeType='Fixed Radius Point Source')
    probeLocation1.PassFieldArrays = 1
    probeLocation1.ComputeTolerance = 1
    probeLocation1.Tolerance = 2.220446049250313e-16

    # init the 'Fixed Radius Point Source' selected for 'ProbeType'
    probeLocation1.ProbeType.Center = xyz

    probeLocation1.ProbeType.NumberOfPoints = 1
    probeLocation1.ProbeType.Radius = 0.0
    return probeLocation1

def read_vtk(vtk_name):
# create a new 'Legacy VTK Reader'
    phivtk = FindSource(vtk_name)

    if not phivtk:
    # create a new 'Legacy VTK Reader'
        phivtk = LegacyVTKReader(registrationName=vtk_name, FileNames=[run_folder+'\\'+vtk_name])
    print([run_folder+'\\'+vtk_name])

    # set active source
    SetActiveSource(phivtk)
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # show data in view
    vtkDisplay = Show(phivtk, renderView1, 'UnstructuredGridRepresentation')
    # trace defaults for the display properties.
    vtkDisplay.Representation = 'Surface'
    # show color bar/color legend
    vtkDisplay.SetScalarBarVisibility(renderView1, True)
    # get color transfer function/color map for 'P1'
    p1LUT = GetColorTransferFunction('P1')
    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(p1LUT, renderView1)
    # hide data in view
    Hide(phivtk, renderView1)
    return phivtk

# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

##### import the simple module from the paraview
from paraview.simple import *
##### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# TEMP for development OR force to start at specific run after Paraview accidentally closed
# vtk_list = ['run009.vtk', 'run010.vtk', 'run011.vtk'] #override vtk_list manually

#Loop throgh vtk files
for vtk in vtk_list:
    # create a new 'Legacy VTK Reader'  #FOR LOOP TO LOOP THROUGH vtks
    phivtk = read_vtk(vtk)

    # set active source
    SetActiveSource(phivtk)
    
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    count = 0

    #Loop through the APs
    for xyz in listofap:
        print(xyz)
        #create probe location procedure
        probeLocation1 = createprobe(xyz, count, phivtk)


        # get active view
        spreadSheetView1 = FindViewOrCreate('SpreadSheetView1', viewtype='SpreadSheetView')

        # show data in view
        probeLocation1Display = Show(probeLocation1, spreadSheetView1, 'SpreadSheetRepresentation')

        # trace defaults for the display properties.
        probeLocation1Display.Assembly = 'Hierarchy'
        probeLocation1Display.BlockVisibilities = []

        # update the view to ensure updated data information
        spreadSheetView1.Update()

        # Properties modified on probeLocation1Display
        probeLocation1Display.Assembly = ''

        SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

        # clear all selections
        ClearSelection()

        # set active source
        SetActiveSource(probeLocation1)

        SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

        # get display properties
        probeLocation1Display = GetDisplayProperties(probeLocation1, view=spreadSheetView1)

        # export view
        ExportView(destination_folder+f'/{vtk}_AP_{count}.csv', view=spreadSheetView1, RealNumberNotation='Mixed', RealNumberPrecision=10)

        # toggle 3D widget visibility (only when running from the GUI)
        Hide3DWidgets(proxy=probeLocation1.ProbeType)

        count+=1

    #do smth to append the excel tables of all APs on 1 vtk into 1; then merge with AP_z.csv/excel
    df = pd.read_csv(destination_folder+f'/{vtk}_AP_0.csv')

    # print(df)
    for i in range(1,count):
        # print(i)
        filename = destination_folder+f'/{vtk}_AP_{i}.csv'
        df_temp = pd.read_csv(filename)
        df = pd.concat([df, df_temp])
        if(os.path.exists(filename) and os.path.isfile(filename)):
            os.remove(filename)
        else:
            print("file not found")

    os.remove(destination_folder+f'/{vtk}_AP_0.csv')

    df.reset_index(drop=True, inplace=True)
    df_ap.reset_index(drop=True, inplace=True)
    # df_ap.columns = ['X', 'Y', 'Z']
    df = pd.concat([df_ap, df],axis=1)

    df.to_csv(destination_folder+f'/{vtk}_AP_results.csv')
    # print(df_ap)
    # print(df)
    print(f"Script Completed to Extract all values at Assessment Points of {vtk}")


####################################################Visuals########################################################

# find source (The model to display)
# phivtk = FindSource('phi.vtk')##########select here for which vtk file to show

# tf.displaythemodel(phivtk)
# tf.show_vel1(phivtk)

######################################################Slice########################################################
    # tf.make_slice(phivtk, 16)  #source (phivtk = FindSource('phi.vtk')), height
    # tf.screenshot_func(working_folder, "slice1")
  
print("End of Script")