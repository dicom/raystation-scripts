'''Copies python script files from a network folder to a local harddrive folder.

The motive behind this script is that we noticed that execution of the RayStation scripts
from our network folder was slow, whereas executing the files from the local harddisk
was considerably faster.

Authors:
Christoffer Lervåg
Helse Møre og Romsdal HF
'''

# Import system libraries:
from shutil import copytree, rmtree, copy2
import os

# Source and destination paths:
source = open(r'C:\temp\raystation-scripts\config\script_source.txt', "r", encoding='utf-8').read()
destination = "C:\\temp\\raystation-scripts"


def copytree(src, dst, symlinks=False, ignore=None):
  """Copies files and folders from source to destination.

    Args:
      src (str): The source path (where files will be copied from).
      dst (str): The destination path (where files will be copied to).
      symlinks (bool): See documentation of shutil.copytree().
      ignore (bool): See documentation of shutil.copytree().
    """
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
  """Deletes files and folders in the given path.

    Args:
      dst (str): The destination path (where files and folders will be deleted).
    """
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


# Clean up the destination folder:
try:
  delete_files_and_folders(destination)
except:
  print("FEIL: Klarte ikke å slette den eksisterende skript-mappen!")

# Copy files from source to destination:
copytree(source, destination, symlinks=False, ignore=None)
