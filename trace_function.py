#### import the simple module from the paraview
from paraview.simple import *
import numpy as np

def screenshot_func(working_folder, filename):
    
    paraview.simple._DisableFirstRenderCameraReset()

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # reset view to fit data bounds
    # renderView1.ResetCamera(1010.9299926757812, 1910.9300537109375, 1010.9299926757812, 1927.9300537109375, 0.0, 101.09300231933594, True)

    # get layout
    layout1 = GetLayout()

    # layout/tab size in pixels
    layout1.SetSize(893, 552)

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [1460.9300231933594, 1469.4300231933594, 2540.394538300714]
    renderView1.CameraFocalPoint = [1460.9300231933594, 1469.4300231933594, 50.54650115966797]
    renderView1.CameraParallelScale = 511.073905033722

    # save screenshot
    SaveScreenshot(working_folder + f'\{filename}.png', renderView1, ImageResolution=[1786, 1104])

def make_clip(out_allstl, height, radius, vtk):
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    out_allstlDisplay = Show(out_allstl, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    out_allstlDisplay.Representation = 'Surface'

    # # show color bar/color legend
    # out_allstlDisplay.SetScalarBarVisibility(renderView1, True)

    # create a new 'Clip'
    clip1 = Clip(registrationName=f'{vtk}_Clip', Input=out_allstl)

    # toggle 3D widget visibility (only when running from the GUI)
    Show3DWidgets(proxy=clip1.ClipType)

    # Properties modified on clip1
    clip1.ClipType = 'Cylinder'

    # Properties modified on clip1.ClipType
    clip1.ClipType.Center = [1434.5240478515625, 1466.7115478515625, height]
    clip1.ClipType.Axis = [0.0, 0.0, 1.0]
    clip1.ClipType.Radius = radius

    # show data in view
    clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

    # trace defaults for the display properties.
    clip1Display.Representation = 'Surface'

    # hide data in view
    Hide(out_allstl, renderView1)

    # # show color bar/color legend
    # clip1Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # turn off scalar coloring
    ColorBy(clip1Display, None)

    # get color transfer function/color map for 'STLSolidLabeling'
    sTLSolidLabelingLUT = GetColorTransferFunction('STLSolidLabeling')

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(sTLSolidLabelingLUT, renderView1)

    # toggle 3D widget visibility (only when running from the GUI)
    Hide3DWidgets(proxy=clip1.ClipType)

def make_slice(phivtk_source, height, vtk, max_scale):  
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # set active view
    SetActiveView(renderView1)


    # create a new 'Slice'
    slice1 = Slice(registrationName=f'{vtk}_Slice', Input=phivtk_source)
    slice1.SliceType = 'Plane'
    slice1.HyperTreeGridSlicer = 'Plane'
    slice1.UseDual = 0
    slice1.Crinkleslice = 0
    slice1.Triangulatetheslice = 1
    slice1.Mergeduplicatedpointsintheslice = 1
    slice1.SliceOffsetValues = [0.0]

    # init the 'Plane' selected for 'SliceType'
    slice1.SliceType.Origin = [1284.5489501953125, 1277.64404296875, height]
    slice1.SliceType.Normal = [0.0, 0.0, 1.0]
    slice1.SliceType.Offset = 0.0


    # find source
    slice1 = FindSource(f'{vtk}_Slice')
    # set active source
    SetActiveSource(slice1)

    # show data in view
    slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    slice1Display.Selection = None
    slice1Display.Representation = 'Surface'
    slice1Display.ColorArrayName = ['POINTS', 'P1']

    # set scalar coloring
    ColorBy(slice1Display, ('POINTS', 'Vel1', 'Magnitude'))

    # get color transfer function/color map for 'P1'
    p1LUT = GetColorTransferFunction('P1')

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(p1LUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    slice1Display.RescaleTransferFunctionToDataRange(True, False)

    # get color transfer function/color map for 'Vel1'
    vel1LUT = GetColorTransferFunction('Vel1')

    # get color legend/bar for vel1LUT in view renderView1
    vel1LUTColorBar = GetScalarBar(vel1LUT, renderView1)

    # Properties modified on vel1LUTColorBar
    vel1LUTColorBar.AutoOrient = 0
    vel1LUTColorBar.TitleJustification = 'Right'
    vel1LUTColorBar.HorizontalTitle = 0
    vel1LUTColorBar.ScalarBarThickness = 12
    vel1LUTColorBar.Orientation = 'Vertical'
    vel1LUTColorBar.Title = 'Velocity'
    vel1LUTColorBar.ScalarBarLength = 0.33
    # Properties modified on vel1LUTColorBar
    vel1LUTColorBar.TextPosition = 'Ticks left/bottom, annotations right/top'
    vel1LUTColorBar.LabelBold = 1
    vel1LUTColorBar.TitleBold = 1

    # get opacity transfer function/opacity map for 'Vel1'
    vel1PWF = GetOpacityTransferFunction('Vel1')

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

###################manual################################
    # Properties modified on vel1LUT
    vel1LUT.AutomaticRescaleRangeMode = 'Never'

    # Rescale transfer function
    vel1LUT.RescaleTransferFunction(0.0, max_scale)

    # Rescale transfer function
    vel1PWF.RescaleTransferFunction(0.0, max_scale)

################################################################
    # Update the pipeline, if it hasn't been updated already.
    slice1.UpdatePipeline()


    # #TRIAL read data
    # UpdatePipeline()
    # dataInfo = slice1.GetDataInformation()
    # get display properties
    # slice1Display = GetDisplayProperties(slice1, view=renderView1)
    # print(slice1Display)
    # print(slice1.PointData[:])
    # print(slice1.PointData.values())
    # print("No. of components:",slice1.PointData["Vel1"].GetNumberOfComponents())
    # print("MAX:", (slice1.PointData['Vel1'].GetRange(-1)))
    # print("MAX:", (slice1.PointData['Vel1'].GetRange(-1))[1])

    # print("RANGE:", (slice1.PointData['Vel1'].GetRange(0)))
    # print("RANGE:", (slice1.PointData['Vel1'].GetRange(0))[1])

    # show color bar/color legend
    slice1Display.SetScalarBarVisibility(renderView1, True)

    # # rescale color and/or opacity maps used to exactly fit the current data range
    # slice1Display.RescaleTransferFunctionToDataRange(False, True)

    # update the view to ensure updated data information
    renderView1.Update()

    return slice1

def make_glyph(slice1, vtk, scale_factor):
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # set active view
    SetActiveView(renderView1)

    # create a new 'Glyph'
    glyph1 = Glyph(registrationName=f'{vtk}_Glyph', Input=slice1,
        GlyphType='Arrow')
    glyph1.GlyphType = '2D Glyph'
    glyph1.ScaleArray = ['POINTS', 'No scale array']
    glyph1.OrientationArray = ['POINTS', 'Vel1']
    glyph1.ScaleFactor = scale_factor
    glyph1.GlyphTransform = 'Transform2'

    # # hide data in view
    # Hide(run002vtk, renderView1)

    # Properties modified on glyph1
    glyph1.GlyphMode = 'Uniform Spatial Distribution (Surface Sampling)'
    glyph1.MaximumNumberOfSamplePoints = 30000
    
    # find source
    glyph1 = FindSource(f'{vtk}_Glyph')
    # set active source
    SetActiveSource(glyph1)

    # show data in view
    glyph1Display = Show(glyph1, renderView1, 'GeometryRepresentation')

    # trace defaults for the display properties.
    glyph1Display.Representation = 'Surface'

    # get display properties
    glyph1Display = GetDisplayProperties(glyph1, view=renderView1)

    # Properties modified on glyph1Display
    glyph1Display.LineWidth = 2.0

    # Properties modified on glyph1Display
    glyph1Display.RenderLinesAsTubes = 1

    # show color bar/color legend
    glyph1Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # turn off scalar coloring
    ColorBy(glyph1Display, None)

    # get color transfer function/color map for 'P1'
    p1LUT = GetColorTransferFunction('P1')
    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(p1LUT, renderView1)

    # change solid color
    glyph1Display.AmbientColor = [0.0, 0.0, 0.0]
    glyph1Display.DiffuseColor = [0.0, 0.0, 0.0]

    # reset view to fit data
    renderView1.ResetCamera(False)



def show_vel1(phivtk):
    #################################################Choose to show model Velocity######################
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # set active view
    SetActiveView(renderView1)
    # set active source
    SetActiveSource(phivtk)

    # get display properties
    phivtkDisplay = GetDisplayProperties(phivtk, view=renderView1)

    # set scalar coloring
    ColorBy(phivtkDisplay, ('POINTS', 'Vel1', 'Magnitude'))

    p1LUT = GetColorTransferFunction('P1')
    # # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(p1LUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    phivtkDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    phivtkDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'Vel1'
    vel1LUT = GetColorTransferFunction('Vel1')
    vel1LUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 11.978924654944429, 0.865003, 0.865003, 0.865003, 23.957849309888857, 0.705882, 0.0156863, 0.14902]
    vel1LUT.ScalarRangeInitialized = 1.0

    # get opacity transfer function/opacity map for 'Vel1'
    vel1PWF = GetOpacityTransferFunction('Vel1')
    vel1PWF.Points = [0.0, 0.0, 0.5, 0.0, 23.957849309888857, 1.0, 0.5, 0.0]
    vel1PWF.ScalarRangeInitialized = 1


def displaythemodel(phivtk):
    # find view
    renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

    # set active view
    SetActiveView(renderView1)

    #Find Source already done

    # set active source
    SetActiveSource(phivtk)

    # show data in view
    phivtkDisplay = Show(phivtk, renderView1, 'UnstructuredGridRepresentation')

    # init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
    phivtkDisplay.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
    phivtkDisplay.OSPRayScaleFunction.UseLogScale = 0

    # init the 'Arrow' selected for 'GlyphType'
    phivtkDisplay.GlyphType.TipResolution = 6
    phivtkDisplay.GlyphType.TipRadius = 0.1
    phivtkDisplay.GlyphType.TipLength = 0.35
    phivtkDisplay.GlyphType.ShaftResolution = 6
    phivtkDisplay.GlyphType.ShaftRadius = 0.03
    phivtkDisplay.GlyphType.Invert = 0

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    phivtkDisplay.ScaleTransferFunction.Points = [-142.28237915039062, 0.0, 0.5, 0.0, 164.49954223632812, 1.0, 0.5, 0.0]
    phivtkDisplay.ScaleTransferFunction.UseLogScale = 0

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    phivtkDisplay.OpacityTransferFunction.Points = [-142.28237915039062, 0.0, 0.5, 0.0, 164.49954223632812, 1.0, 0.5, 0.0]
    phivtkDisplay.OpacityTransferFunction.UseLogScale = 0

    # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
    phivtkDisplay.DataAxesGrid.XTitle = 'X Axis'
    phivtkDisplay.DataAxesGrid.YTitle = 'Y Axis'
    phivtkDisplay.DataAxesGrid.ZTitle = 'Z Axis'
    phivtkDisplay.DataAxesGrid.XTitleFontFamily = 'Arial'
    phivtkDisplay.DataAxesGrid.XTitleFontFile = ''
    phivtkDisplay.DataAxesGrid.XTitleBold = 0
    phivtkDisplay.DataAxesGrid.XTitleItalic = 0
    phivtkDisplay.DataAxesGrid.XTitleFontSize = 12
    phivtkDisplay.DataAxesGrid.XTitleShadow = 0
    phivtkDisplay.DataAxesGrid.XTitleOpacity = 1.0
    phivtkDisplay.DataAxesGrid.YTitleFontFamily = 'Arial'
    phivtkDisplay.DataAxesGrid.YTitleFontFile = ''
    phivtkDisplay.DataAxesGrid.YTitleBold = 0
    phivtkDisplay.DataAxesGrid.YTitleItalic = 0
    phivtkDisplay.DataAxesGrid.YTitleFontSize = 12
    phivtkDisplay.DataAxesGrid.YTitleShadow = 0
    phivtkDisplay.DataAxesGrid.YTitleOpacity = 1.0
    phivtkDisplay.DataAxesGrid.ZTitleFontFamily = 'Arial'
    phivtkDisplay.DataAxesGrid.ZTitleFontFile = ''
    phivtkDisplay.DataAxesGrid.ZTitleBold = 0
    phivtkDisplay.DataAxesGrid.ZTitleItalic = 0
    phivtkDisplay.DataAxesGrid.ZTitleFontSize = 12
    phivtkDisplay.DataAxesGrid.ZTitleShadow = 0
    phivtkDisplay.DataAxesGrid.ZTitleOpacity = 1.0
    phivtkDisplay.DataAxesGrid.FacesToRender = 63
    phivtkDisplay.DataAxesGrid.CullBackface = 0
    phivtkDisplay.DataAxesGrid.CullFrontface = 1
    phivtkDisplay.DataAxesGrid.ShowGrid = 0
    phivtkDisplay.DataAxesGrid.ShowEdges = 1
    phivtkDisplay.DataAxesGrid.ShowTicks = 1
    phivtkDisplay.DataAxesGrid.LabelUniqueEdgesOnly = 1
    phivtkDisplay.DataAxesGrid.AxesToLabel = 63
    phivtkDisplay.DataAxesGrid.XLabelFontFamily = 'Arial'
    phivtkDisplay.DataAxesGrid.XLabelFontFile = ''
    phivtkDisplay.DataAxesGrid.XLabelBold = 0
    phivtkDisplay.DataAxesGrid.XLabelItalic = 0
    phivtkDisplay.DataAxesGrid.XLabelFontSize = 12
    phivtkDisplay.DataAxesGrid.XLabelShadow = 0
    phivtkDisplay.DataAxesGrid.XLabelOpacity = 1.0
    phivtkDisplay.DataAxesGrid.YLabelFontFamily = 'Arial'
    phivtkDisplay.DataAxesGrid.YLabelFontFile = ''
    phivtkDisplay.DataAxesGrid.YLabelBold = 0
    phivtkDisplay.DataAxesGrid.YLabelItalic = 0
    phivtkDisplay.DataAxesGrid.YLabelFontSize = 12
    phivtkDisplay.DataAxesGrid.YLabelShadow = 0
    phivtkDisplay.DataAxesGrid.YLabelOpacity = 1.0
    phivtkDisplay.DataAxesGrid.ZLabelFontFamily = 'Arial'
    phivtkDisplay.DataAxesGrid.ZLabelFontFile = ''
    phivtkDisplay.DataAxesGrid.ZLabelBold = 0
    phivtkDisplay.DataAxesGrid.ZLabelItalic = 0
    phivtkDisplay.DataAxesGrid.ZLabelFontSize = 12
    phivtkDisplay.DataAxesGrid.ZLabelShadow = 0
    phivtkDisplay.DataAxesGrid.ZLabelOpacity = 1.0
    phivtkDisplay.DataAxesGrid.XAxisNotation = 'Mixed'
    phivtkDisplay.DataAxesGrid.XAxisPrecision = 2
    phivtkDisplay.DataAxesGrid.XAxisUseCustomLabels = 0
    phivtkDisplay.DataAxesGrid.XAxisLabels = []
    phivtkDisplay.DataAxesGrid.YAxisNotation = 'Mixed'
    phivtkDisplay.DataAxesGrid.YAxisPrecision = 2
    phivtkDisplay.DataAxesGrid.YAxisUseCustomLabels = 0
    phivtkDisplay.DataAxesGrid.YAxisLabels = []
    phivtkDisplay.DataAxesGrid.ZAxisNotation = 'Mixed'
    phivtkDisplay.DataAxesGrid.ZAxisPrecision = 2
    phivtkDisplay.DataAxesGrid.ZAxisUseCustomLabels = 0
    phivtkDisplay.DataAxesGrid.ZAxisLabels = []
    phivtkDisplay.DataAxesGrid.UseCustomBounds = 0
    phivtkDisplay.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

    # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
    phivtkDisplay.PolarAxes.Visibility = 0
    phivtkDisplay.PolarAxes.Translation = [0.0, 0.0, 0.0]
    phivtkDisplay.PolarAxes.Scale = [1.0, 1.0, 1.0]
    phivtkDisplay.PolarAxes.Orientation = [0.0, 0.0, 0.0]
    phivtkDisplay.PolarAxes.EnableCustomBounds = [0, 0, 0]
    phivtkDisplay.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
    phivtkDisplay.PolarAxes.EnableCustomRange = 0
    phivtkDisplay.PolarAxes.CustomRange = [0.0, 1.0]
    phivtkDisplay.PolarAxes.PolarAxisVisibility = 1
    phivtkDisplay.PolarAxes.RadialAxesVisibility = 1
    phivtkDisplay.PolarAxes.DrawRadialGridlines = 1
    phivtkDisplay.PolarAxes.PolarArcsVisibility = 1
    phivtkDisplay.PolarAxes.DrawPolarArcsGridlines = 1
    phivtkDisplay.PolarAxes.NumberOfRadialAxes = 0
    phivtkDisplay.PolarAxes.AutoSubdividePolarAxis = 1
    phivtkDisplay.PolarAxes.NumberOfPolarAxis = 0
    phivtkDisplay.PolarAxes.MinimumRadius = 0.0
    phivtkDisplay.PolarAxes.MinimumAngle = 0.0
    phivtkDisplay.PolarAxes.MaximumAngle = 90.0
    phivtkDisplay.PolarAxes.RadialAxesOriginToPolarAxis = 1
    phivtkDisplay.PolarAxes.Ratio = 1.0
    phivtkDisplay.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
    phivtkDisplay.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
    phivtkDisplay.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
    phivtkDisplay.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
    phivtkDisplay.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
    phivtkDisplay.PolarAxes.PolarAxisTitleVisibility = 1
    phivtkDisplay.PolarAxes.PolarAxisTitle = 'Radial Distance'
    phivtkDisplay.PolarAxes.PolarAxisTitleLocation = 'Bottom'
    phivtkDisplay.PolarAxes.PolarLabelVisibility = 1
    phivtkDisplay.PolarAxes.PolarLabelFormat = '%-#6.3g'
    phivtkDisplay.PolarAxes.PolarLabelExponentLocation = 'Labels'
    phivtkDisplay.PolarAxes.RadialLabelVisibility = 1
    phivtkDisplay.PolarAxes.RadialLabelFormat = '%-#3.1f'
    phivtkDisplay.PolarAxes.RadialLabelLocation = 'Bottom'
    phivtkDisplay.PolarAxes.RadialUnitsVisibility = 1
    phivtkDisplay.PolarAxes.ScreenSize = 10.0
    phivtkDisplay.PolarAxes.PolarAxisTitleOpacity = 1.0
    phivtkDisplay.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
    phivtkDisplay.PolarAxes.PolarAxisTitleFontFile = ''
    phivtkDisplay.PolarAxes.PolarAxisTitleBold = 0
    phivtkDisplay.PolarAxes.PolarAxisTitleItalic = 0
    phivtkDisplay.PolarAxes.PolarAxisTitleShadow = 0
    phivtkDisplay.PolarAxes.PolarAxisTitleFontSize = 12
    phivtkDisplay.PolarAxes.PolarAxisLabelOpacity = 1.0
    phivtkDisplay.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
    phivtkDisplay.PolarAxes.PolarAxisLabelFontFile = ''
    phivtkDisplay.PolarAxes.PolarAxisLabelBold = 0
    phivtkDisplay.PolarAxes.PolarAxisLabelItalic = 0
    phivtkDisplay.PolarAxes.PolarAxisLabelShadow = 0
    phivtkDisplay.PolarAxes.PolarAxisLabelFontSize = 12
    phivtkDisplay.PolarAxes.LastRadialAxisTextOpacity = 1.0
    phivtkDisplay.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
    phivtkDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
    phivtkDisplay.PolarAxes.LastRadialAxisTextBold = 0
    phivtkDisplay.PolarAxes.LastRadialAxisTextItalic = 0
    phivtkDisplay.PolarAxes.LastRadialAxisTextShadow = 0
    phivtkDisplay.PolarAxes.LastRadialAxisTextFontSize = 12
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextBold = 0
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextItalic = 0
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextShadow = 0
    phivtkDisplay.PolarAxes.SecondaryRadialAxesTextFontSize = 12
    phivtkDisplay.PolarAxes.EnableDistanceLOD = 1
    phivtkDisplay.PolarAxes.DistanceLODThreshold = 0.7
    phivtkDisplay.PolarAxes.EnableViewAngleLOD = 1
    phivtkDisplay.PolarAxes.ViewAngleLODThreshold = 0.7
    phivtkDisplay.PolarAxes.SmallestVisiblePolarAngle = 0.5
    phivtkDisplay.PolarAxes.PolarTicksVisibility = 1
    phivtkDisplay.PolarAxes.ArcTicksOriginToPolarAxis = 1
    phivtkDisplay.PolarAxes.TickLocation = 'Both'
    phivtkDisplay.PolarAxes.AxisTickVisibility = 1
    phivtkDisplay.PolarAxes.AxisMinorTickVisibility = 0
    phivtkDisplay.PolarAxes.ArcTickVisibility = 1
    phivtkDisplay.PolarAxes.ArcMinorTickVisibility = 0
    phivtkDisplay.PolarAxes.DeltaAngleMajor = 10.0
    phivtkDisplay.PolarAxes.DeltaAngleMinor = 5.0
    phivtkDisplay.PolarAxes.PolarAxisMajorTickSize = 0.0
    phivtkDisplay.PolarAxes.PolarAxisTickRatioSize = 0.3
    phivtkDisplay.PolarAxes.PolarAxisMajorTickThickness = 1.0
    phivtkDisplay.PolarAxes.PolarAxisTickRatioThickness = 0.5
    phivtkDisplay.PolarAxes.LastRadialAxisMajorTickSize = 0.0
    phivtkDisplay.PolarAxes.LastRadialAxisTickRatioSize = 0.3
    phivtkDisplay.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
    phivtkDisplay.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
    phivtkDisplay.PolarAxes.ArcMajorTickSize = 0.0
    phivtkDisplay.PolarAxes.ArcTickRatioSize = 0.3
    phivtkDisplay.PolarAxes.ArcMajorTickThickness = 1.0
    phivtkDisplay.PolarAxes.ArcTickRatioThickness = 0.5
    phivtkDisplay.PolarAxes.Use2DMode = 0
    phivtkDisplay.PolarAxes.UseLogAxis = 0

    # show color bar/color legend
    phivtkDisplay.SetScalarBarVisibility(renderView1, True)

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # reset view to fit data
    renderView1.ResetCamera(False)