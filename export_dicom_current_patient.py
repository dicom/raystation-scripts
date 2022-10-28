# Export DICOM files for the current patient.

# RayStation 10B - Python 3.6

# System files:
from connect import get_current
from os import mkdir, path, chdir, getcwd
import time

# Export folder:
export_folder = r'C:\temp\DICOM'

# Load patient and case data:
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No patient loaded.")
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")


# Prepare folder:
if path.isdir(export_folder):
  chdir(export_folder)
else:
  mkdir(export_folder)
  chdir(export_folder)
  

# Function for exporting a patient case (specified by study nr):
def export(patient, case):
  # Create a folder for this patient:
  mkdir(patient.Name)
  case.ScriptableDicomExport(
    ExportFolderPath = path.join(getcwd(), patient.Name),
    Examinations = [e.Name for e in case.Examinations],
    RtStructureSetsForExaminations = [e.Name for e in case.Examinations],
    IgnorePreConditionWarnings = True
  )


# Export the current patient/case:
export(patient, case)

