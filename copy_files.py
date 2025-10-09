# Copies python script files from a network folder to a local harddrive folder.

from shutil import copytree, rmtree, copy2
import os

# Source and destination paths:
source = "I:/HMR - Begrenset/Klinikk for kreftbehandling og rehabilitering - Stråleterapi-kontor - Doseplanlegging/Skript/raystation-scripts/"
destination = "C:/temp/raystation-scripts/"

# Copies files and folders from source to destination.
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

# Deletes files and folders in the given path.
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
          print("FEIL: Klarte ikke å slette fil: " + p)
    try:
      os.rmdir(destination)
    except:
      print ("FEIL: Klarte ikke å slette mappe: " + destination)

try:
  delete_files_and_folders(destination)
except: 
  print("FEIL: Klarte ikke å slette den eksisterende skript-mappen!")

copytree(source, destination, symlinks=False, ignore=None)
