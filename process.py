#import modules
import csv
import pandas as pd
import os

#####Manual input#######################################################################
#####Coordinate transform coefficients Pheonics<--->Paraview/Real Coordinates
x0 = 8.415319e5
y0 = 8.134692e5
z0 = -9.557

# vtk_list = ['']
########################################################################################
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

# TEMP for development
# vtk_list = ['run001.vtk', 'run002.vtk', 'run003.vtk']

#absolute path to import module (put the trace_function.py in same folder with this script)
import importlib.util
import sys
spec = importlib.util.spec_from_file_location("trace_function", working_folder+"\\trace_function.py")
foo = importlib.util.module_from_spec(spec)
sys.modules["trace_function"] = foo
spec.loader.exec_module(foo)
import trace_function as tf
#######################################################################################
destination_folder = working_folder

def read_vtk(vtk_name):
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

def import_STL():

    out_allstl = FindSource('out_all.stl') #only 1 file

    if not out_allstl:
    # create a new 'STL Reader'
        out_allstl = STLReader(registrationName='out_all.stl', FileNames=[working_folder+'\\Test3\\out_all.stl'])

    return out_allstl




##### import the simple module from the paraview
from paraview.simple import *
##### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

max_scale_vtk = 0

for vtk in vtk_list:
    print(vtk)
    # create a new 'Legacy VTK Reader'  #FOR LOOP TO LOOP THROUGH vtks
    phivtk = read_vtk(vtk)
    
    max_scale_vtk_temp = phivtk.PointData['Vel1'].GetRange(-1)[1]
    print("TEMP:",max_scale_vtk_temp)
    max_scale_vtk = max(max_scale_vtk,max_scale_vtk_temp)

print(max_scale_vtk)


#Loop through vtk files
for vtk in vtk_list:
    # create a new 'Legacy VTK Reader'  #FOR LOOP TO LOOP THROUGH vtks
    phivtk = read_vtk(vtk)

    # set active source
    SetActiveSource(phivtk)

    count = 0

    tf.displaythemodel(phivtk)
    tf.show_vel1(phivtk)    

    vtk = vtk.rpartition(".")[0]
    #Hide all except glyph and slice
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')
    HideAll(renderView1)
    slice_view = tf.make_slice(phivtk, height=16.0, vtk=vtk, max_scale=max_scale_vtk)
    tf.make_glyph(slice_view, vtk=vtk, scale_factor=32.0)

    # add buildings
    out_allstl = import_STL()
    tf.make_clip(out_allstl, height=100, radius=500, vtk=vtk)
    tf.screenshot_func(working_folder, vtk+"_pic1")

print("End of Script")