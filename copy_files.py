
from shutil import copytree, rmtree, copy2
import os
source = "I:/HSM - Kreftavdelingen - gammelt fellesområde/Program/Skript/raystation-scripts/"
destination = "C:/temp/raystation-scripts/"

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                copy2(s, d)
def delete_files_and_folders(destination):
  if os.path.isdir(destination):
    for file in os.listdir(destination):
      p = os.path.join(destination, file)
      if os.path.isdir(p):
        delete_files_and_folders(p)
      else:
        try:
          os.remove(p)
        except: 
          print("hei")
    try:
      os.rmdir(destination)
    except:
      print ("hei")

try:
    delete_files_and_folders(destination)  
except: 
    print("hei")
copytree(source, destination, symlinks=False, ignore=None)


