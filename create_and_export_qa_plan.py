# encoding: utf8
# Creates a QA plan with standard settings and exports it to specified folder.
#
# Authors:
# Christoffer Lervåg & Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 10B
# Python 3.6

# Import system libraries:
from connect import *
import clr, sys, os
import math
from tkinter import *
from tkinter import messagebox

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")

# Import local files:
import radio_button_frame as FRAME
import gui_functions as GUIF
import property as P
import radio_button as RB

# Load patient and case data:
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No plan loaded.")
try:
    plan = get_current("Plan")
except SystemError:
    raise IOError("No plan loaded.")
try:
    beam_set = get_current("BeamSet")
except SystemError:
    raise IOError("No beam set loaded.")

# Determine (unique) name of QA plan:
name = 'QA'
prefix = 'QA'
name_conflict = False
if len(list(plan.VerificationPlans)) > 0:
  for p in plan.VerificationPlans:
    if p.BeamSet.DicomPlanLabel == name:
      name_conflict = True
  if name_conflict:
    i = 0
    while True:
      i += 1
      name = prefix + " " + str(i)
      available = True
      for p in plan.VerificationPlans:
        if p.BeamSet.DicomPlanLabel == name:
          available = False
      if available:
        break

# Radiobutton choices for dose grid:
c2mm = P.Property('Konvensjonell VMAT (2 mm)', '0.2', default = True)
c1mm = P.Property('Stereotaksi (1 mm)','0.1')
choices = [c2mm, c1mm]

# Create radio button object
options = RB.RadioButton('VMAT QA','Velg dosematrise:', choices)

# Setup and run GUI:
my_window = Tk()
frame = FRAME.RadioButtonFrame(my_window, options)
frame.grid(row = 0,column = 0)
my_window.mainloop()

# Extract information from the users's selections in the GUI:
if frame.ok:
    (selection,value) = frame.get_results()
elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)

# Convert the selected value to a float:
resolution = float(value)

# Create QA plan:
beam_set.CreateQAPlan(
	PhantomName = 'ArcCheck (Heterogen bordtopp)',
	PhantomId = 'AC_plug_test',
	QAPlanName = name, 
	IsoCenter = { 'x': -0.0, 'y': 0.0, 'z': 0 }, 
	DoseGrid = { 'x': resolution, 'y': resolution, 'z': resolution }, 
	ComputeDoseWhenPlanIsCreated = True
)

# Save:
patient.Save()
last_plan = len(list(plan.VerificationPlans))-1

# DICOM export:
plan.VerificationPlans[last_plan].ScriptableQADicomExport(
	ExportFolderPath = "I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Stråleterapi_avd\\Stråleterapi\\Mosaiq\\dokument-import\\VMAT_QA",
	QaPlanIdentity = 'Patient',
	ExportExamination = False,
	ExportExaminationStructureSet = False,
	ExportBeamSet = False,
	ExportBeamSetDose = True,
	ExportBeamSetBeamDose = True,
	IgnorePreConditionWarnings = False
)
