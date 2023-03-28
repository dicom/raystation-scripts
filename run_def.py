# encoding: utf8

# Executes the Definition class, which sets up all ROIs and POIs needed for treatment planning in RayStation.
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
# Relative paths would be better, but unfortunately doesnt seem to work when imported into the RayStation database, e.q.:
#sys.path.append(os.path.join(sys.path[0],'def_regions'))


# Import local files:
import definition as DEF


# Load patient and case data:
try:
  patient = get_current("Patient")
except SystemError:
  raise IOError("No patient loaded.")
try:
  case = get_current("Case")
except SystemError:
  raise IOError("No case loaded.")
try:
  patient_db = get_current('PatientDB')
except SystemError:
  raise IOError("No case loaded.")

# Set up and execute the def script:
d = DEF.Definition(patient_db, patient, case)
