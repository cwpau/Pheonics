# # create a new 'Probe Location'
# probeLocation1 = ProbeLocation(Input=eLNOfieldToSurface1,
#     ProbeType='Fixed Radius Point Source')

# N=5 #Specify number of points on which to find values
# Stress2 = []
# for i in range(N):
#     x=i    #Select x-coordinate
#     y=i+1  #Select y-coordinate
#     # Properties modified on probeLocation1.ProbeType
#     probeLocation1.ProbeType.Center = [x, y, 0.0]  #interpolates all data to a specific point
#     polyData = servermanager.Fetch(probeLocation1) #Get data from the server side to the client side
#     pointData = polyData.GetPointData()
#     StressArray = pointData.GetArray('resnonl_SIGM_ELNO') #Select which data you want to extract
#     Stress = StressArray.GetTuple(0)
#     Coordinates = [x, y, 0]
#     Stress1 = np.r_[Coordinates, Stress]#Combines the coordinates and stress values in one variable
#     Stress2.append(Stress1)#Adds the next point to the array
#     #print(Stress2)
# #print(pointData) ##Print this (into the python shell) to see which data can be extracted into "StressArray"
# np.savetxt(r"C:\Users\Matthijs\Documents\StressExtract2.txt" ,Stress2)#Save array to the desired file


# from paraview import numpy_support as ns
# from paraview.simple import *

# probeResults = []
# variable = 'U' # name of the array
# files = [r"C:\Users\wilsoncwpau\Desktop\Phoenics\phi.vtk"]

# #Pipeline
# reader = OpenDataFile(files[0])
# probe = ProbeLocation(reader, ProbeType = "Fixed Radius Point Source")
# probe.ProbeType.Center = [0,0,0]  # probe location [x,y,z]

# # Loop through the files
# # for file in files:
# reader.FileNames = files[0]
# probe.UpdatePipeline()
# data = servermanager.Fetch(probe)
# probeResults.append(ns.vtk_to_numpy(data.GetPointData().GetArray(variable)))
# print(probeResults)



# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# set active source
SetActiveSource(None)

# find source
phivtk = FindSource('phi.vtk')

# set active source
SetActiveSource(phivtk)

# create a new 'Probe Location'
probeLocation4 = ProbeLocation(registrationName='ProbeLocation1', Input=phivtk,
    ProbeType='Fixed Radius Point Source')
probeLocation4.PassFieldArrays = 1
probeLocation4.ComputeTolerance = 1
probeLocation4.Tolerance = 2.220446049250313e-16

# init the 'Fixed Radius Point Source' selected for 'ProbeType'
probeLocation4.ProbeType.Center = [1434.52392578125, 1466.7115478515625, 556.011474609375]
probeLocation4.ProbeType.NumberOfPoints = 1
probeLocation4.ProbeType.Radius = 0.0

# # find source
# probeLocation1 = FindSource('ProbeLocation1')

# # find source
# probeLocation3 = FindSource('ProbeLocation3')

# # find source
# legacyVTKReader1 = FindSource('LegacyVTKReader1')

# # find source
# legacyVTKReader2 = FindSource('LegacyVTKReader2')

# # find source
# probeLocation2 = FindSource('ProbeLocation2')

# # find source
# contour1 = FindSource('Contour1')

# # find source
# extractSubset1 = FindSource('ExtractSubset1')

# # find source
# wavelet1 = FindSource('Wavelet1')

# get active view
spreadSheetView1 = GetActiveViewOrCreate('SpreadSheetView')

# show data in view
probeLocation4Display = Show(probeLocation4, spreadSheetView1, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
probeLocation4Display.Assembly = 'Hierarchy'
probeLocation4Display.BlockVisibilities = []

# update the view to ensure updated data information
spreadSheetView1.Update()

# find view
pythonView1 = FindViewOrCreate('PythonView1', viewtype='PythonView')

# update the view to ensure updated data information
pythonView1.Update()

# Properties modified on probeLocation4Display
probeLocation4Display.Assembly = ''

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

# clear all selections
ClearSelection()

# set active source
SetActiveSource(probeLocation4)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

# get display properties
probeLocation1Display = GetDisplayProperties(probeLocation4, view=spreadSheetView1)

# export view
ExportView('C:/Users/wilsoncwpau/Desktop/Phoenics/123.csv', view=spreadSheetView1, RealNumberNotation='Mixed',
    RealNumberPrecision=10)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=probeLocation4.ProbeType)