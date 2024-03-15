import os
import subprocess
import tkinter as tk
import tkinter.filedialog as fd

working_folder = __file__
working_folder = working_folder.rpartition('\\')[0]

root = tk.Tk()
root.withdraw()
filesopened = fd.askopenfilenames(parent=root, title='Choose the files')
root.destroy()

print(str(len(filesopened)), "FILES SELECTED")
count=0
for filename in filesopened:
    count+=1
    cmd = working_folder+"\Run\pho2vtk.exe -phi:" + filename
    subprocess.run(cmd)
    print("COMPLETED:", filename.rpartition("/")[2], "PROGRESS:", str(count),"/",str(len(filesopened)))
