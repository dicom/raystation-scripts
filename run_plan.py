# encoding: utf8

# Executes the Plan class, which sets up all parameters needed for treatment planning in RayStation.
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

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\ts_classes")
sys.path.append("C:\\temp\\raystation-scripts\\various_classes")
sys.path.append(r'C:\temp\raystation-scripts')
# Relative paths would be better, but unfortunately doesnt seem to work when imported into the RayStation database, e.g.:
#sys.path.append(os.path.join(sys.path[0],'def_regions'))

# Import local packages:
import mosaiq

# Local script imports:
import plan as PLAN

# Load patient and case data:
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No patient loaded.")
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")

# Load mosaiq patient:
mq_patient = mosaiq.Patient.find_by_ida(patient.PatientID)
    
# Set up and execute the plan script:
p = PLAN.Plan(patient, case, mq_patient)
