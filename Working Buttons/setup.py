import cx_Freeze, os


makebuttons=['F','F\'','B','B\'','L','L\'','R','R\'','U','U\'','D','D\'','Scramble','Solve','Step 1','Step 2','Step 3','Step 4','Step 5','Step 6','Step 7']
files=[i+".png" for i in makebuttons]
files.append('logo.png')
files.append('Arial Bold.ttf')
executables = [cx_Freeze.Executable("rubikscubealgoworkingbuttons.py")]

cx_Freeze.setup(name="Rubik'sCubeSolver",options={"build_exe": {"packages":["pygame","OpenGL"],"include_files":files}},executables = executables)