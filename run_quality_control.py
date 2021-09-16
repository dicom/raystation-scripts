
# Executes the QualityControl class which runs a suite of tests on the current patient,
# case and treatment plan (including ROIs, beam sets, beams, objectives, etc).
#
# Authors:
# Christoffer Lervåg & Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 10B
# Python 3.6

# System configuration:
from connect import *
import sys
from tkinter import *
from tkinter import messagebox

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\quality_control")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\ts_classes")
sys.path.append("C:\\temp\\raystation-scripts\\various_classes")


# Local script imports:
import quality_control as QC

# "Global" variables:
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No patient loaded.")
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")
try:
    plan = get_current("Plan")
except SystemError:
    raise IOError("No plan loaded.")


# Set up and execute the quality control:
qc = QC.QualityControl(patient, case, plan)

# Display the results of the quality control:
title = "Plan Quality Control"
summary = qc.result.failure_summary()
text = str(qc.result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary
messagebox.showinfo(title,text)

