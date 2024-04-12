
# Executes the QualityControl class which runs a suite of tests on the current patient,
# case and treatment plan (including ROIs, beam sets, beams, objectives, etc).
#
# Authors:
# Christoffer Lervåg & Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 12A
# Python 3.8

# System configuration:
from connect import *
import datetime
import sys
from tkinter import *
from tkinter import messagebox

# Log start time:
time_start = datetime.datetime.now()

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
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

# Set up and execute the quality control class:
qc = QC.QualityControl(patient, case, plan)

# Create title and body strings:
title = "Plan Quality Control"
summary = qc.result.failure_summary()
if qc.result.nr_failures() == 0:
  # Zero failures:
  text = "Ingen problemer ble funnet! :)\n\n"
else:
  # One or more failures:
  text = str(qc.result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary

# Log finish time and format a time string:
time_end = datetime.datetime.now()
elapsed_time = time_end - time_start
if elapsed_time.seconds > 3600:
  hours = elapsed_time.seconds // 3600 % 3600
  minutes = (elapsed_time.seconds - hours * 3600) // 60 % 60
  seconds = elapsed_time.seconds - hours * 3600 - minutes * 60
else:
  hours = 0
  minutes = elapsed_time.seconds // 60 % 60
  seconds = elapsed_time.seconds - minutes * 60
# Append time string to result:
if hours > 0:
  text += "\n\n" + "Tidsbruk: " +str(hours) + " time(r) " + str(minutes) + " min " + str(seconds) + " sek"
else:
  if minutes > 0:
    text += "\n\n" + "Tidsbruk: " + str(minutes) + " min " + str(seconds) + " sek"
  else:
    text += "\n\n" + "Tidsbruk: " + str(seconds) + " sek"

# Display the messagebox GUI:
messagebox.showinfo(title,text)
