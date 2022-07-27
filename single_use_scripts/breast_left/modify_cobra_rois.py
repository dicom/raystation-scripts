# Processes ROIs to be used in the COBRA Deep Learning project.
# This script is designed to be run after a COBRA patient has been imported in the research environment.
# It does the following:
# -Renames the A_Subclavian_L ROI to A_Subclavian_L+A_Axillary_L
# -Deletes the A_Axillary_L ROI
# -Renames the V_Subclavian_L ROI to V_Subclavian_L+V_Axillary_L
# -Deletes the V_Axillary_L ROI

# RayStation 9A - Python 3.6

from connect import *

# Used for GUI debugging:
#from tkinter import *
#from tkinter import messagebox

#root = Tk()
#root.withdraw()
#title = "COBRA Deep Learning project"
#text = ""
#messagebox.showinfo(title, text)
#root.destroy()

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# The patient model:  
pm = case.PatientModel


# Change ROI names:
pm.RegionsOfInterest['A_Subclavian_L'].Name = "A_Subclavian_L+A_Axillary_L"
pm.RegionsOfInterest['V_Subclavian_L'].Name = "V_Subclavian_L+V_Axillary_L"

# Delete ROIs:
try:
  pm.RegionsOfInterest['A_Axillary_L'].DeleteRoi()
except:
  pass
try:
  pm.RegionsOfInterest['V_Axillary_L'].DeleteRoi()
except:
  pass


