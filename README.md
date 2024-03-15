# Pheonics

#### CFD post-processing script in Paraview. Streamlined process to manually export datapoints and create screenshots at certain angles after operations.


multi_probe.py: run in paraview. reads the vtk files, reads the Assessment Pt csv and extract data points accordingly and produces csv outputs

single_probe.py: run in paraview. trial devlopment to extract single point from vtk

pda_to_vtk.py: utilizing 'pho2vtk.exe' from Phoenics to convert pdas to vtks

summarize.py: run after multi_probe.py outside paraview. combines all output csvs to create 1 summarized excel for report

process.py: run in paraview. imports Buildings.stl(model without data) and perform actions such as clipping. produces screenshots.

trace_function.py: functions created based on 'trace' function in paraview. required to be in same folder with running script.

GUI.py: a trial for using a GUI out of paraview. NOT working.

### Folder structure:

![alt text](https://github.com/cwpau/Pheonics/blob/main/folder%20structure.png)


### Procedure:
1. Convert .pda to .vtk if necessary by pda_to_vtk.py
2. Actual script should be multi_probe.py (run script in paraview)
3. Followed by summarize.py to combine excels outputs
4. Run process.py if screenshot is needed (run script in paraview)

*adjustment of code is necessary from task to task. Take a look into trace_function.py.

### Results:
datapoints:</ br>
![datapoints](https://github.com/cwpau/Pheonics/blob/main/result/datapoints.png)

screenshot:</ br>
![pic](/result/run001_pic1.png)
