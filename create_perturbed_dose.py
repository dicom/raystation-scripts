# Compute perturbed doses based on user input
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6

# Import system libraries:
from connect import *
import clr, sys, os
from tkinter import *
from tkinter import messagebox

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")

# Import local files:
import text_box_perturbed_frame as FRAME

# Load beam set and examination 
beam_set = get_current("BeamSet")
examination = get_current("Examination")
name = examination.Name

# Setup and run GUI:
my_window = Tk()
frame = FRAME.TextBoxFrame(my_window)
frame.grid(row=0,column=0)
my_window.mainloop()

# Extract information from the users's selections in the GUI:
if frame.ok:
    (x,y,z) = frame.get_results()
elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)

# Compute perturbed doses
beam_set.ComputePerturbedDose(DensityPerturbation = 0, PatientShift = { 'x': x, 'y': 0, 'z': 0 }, OnlyOneDosePerImageSet = False, AllowGridExpansion = False, ExaminationNames = [name], FractionNumbers = [0], ComputeBeamDoses = True)

beam_set.ComputePerturbedDose(DensityPerturbation = 0, PatientShift = { 'x': -x, 'y': 0, 'z': 0 }, OnlyOneDosePerImageSet = False, AllowGridExpansion = False, ExaminationNames = [name], FractionNumbers = [0], ComputeBeamDoses = True)

beam_set.ComputePerturbedDose(DensityPerturbation = 0, PatientShift = { 'x': 0, 'y': 0, 'z': y }, OnlyOneDosePerImageSet = False, AllowGridExpansion = False, ExaminationNames = [name], FractionNumbers = [0], ComputeBeamDoses = True)

beam_set.ComputePerturbedDose(DensityPerturbation = 0, PatientShift = { 'x': 0, 'y': 0, 'z': -y }, OnlyOneDosePerImageSet = False, AllowGridExpansion = False, ExaminationNames = [name], FractionNumbers = [0], ComputeBeamDoses = True)

beam_set.ComputePerturbedDose(DensityPerturbation = 0, PatientShift = { 'x': 0, 'y': -z, 'z': 0 }, OnlyOneDosePerImageSet = False, AllowGridExpansion = False, ExaminationNames = [name], FractionNumbers = [0], ComputeBeamDoses = True)

beam_set.ComputePerturbedDose(DensityPerturbation = 0, PatientShift = { 'x': 0, 'y': z, 'z': 0 }, OnlyOneDosePerImageSet = False, AllowGridExpansion = False, ExaminationNames = [name], FractionNumbers = [0], ComputeBeamDoses = True)


