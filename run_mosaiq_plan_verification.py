
# Verifies that the current plan in RayStation has been exported successfully to Mosaiq.
# This is achieved by attempting to locate the corresponding plan (Rad Rx) in the Mosiaq
# database and verify all plan parameters (e.q. monitor units, gantry angle, collimator angle,
# couch angle, jaw positions, mlc positions, etc).
#
# Author:
# Christoffer Lervåg
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
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\ts_classes")
sys.path.append("C:\\temp\\raystation-scripts\\various_classes")
sys.path.append(r'C:\temp\raystation-scripts')

# Import local packages:
import mosaiq

# Local script imports:
import mosaiq_plan_verification as MPV

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

# Load mosaiq patient:
mq_patient = mosaiq.Patient.find_by_ida(patient.PatientID)

# Set up and execute the quality control:
mpv = MPV.MosaiqPlanVerification(patient, case, plan, mq_patient)

# Display the results of the quality control:
title = "Mosaiq Plan Verification"
summary = mpv.result.failure_summary()
if mpv.result.nr_failures() == 0:
  # Zero failures:
  text = "Ingen problemer ble funnet! :)\n\n"
else:
  # 1 or more failures:
  text = str(mpv.result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary
messagebox.showinfo(title,text)
