# Export DICOM files for patient cases in the COBRA Deep Learning project.

# RayStation 10A - Python 3.6

# System files:
from connect import get_current
from os import mkdir, path, chdir, getcwd
import time

# Export folder:
export_folder = r'C:\temp\COBRA'

# All numbers in range (from 1 to 110):
numbers = list(range(110+1))
numbers.remove(0)

# Selected export:
selected_cases = [
  66
]

# Control cases (which are not to be exported):
control_cases = [
  5,
  24,
  26,
  33,
  38,
  44,
  55,
  61,
  66,
  73,
  82,
  87,
  94,
  98,
  108
]

# Excluded from the study (doesnt exist in database at all):
excluded = [
  31,
  43,
  53,
  74,
  76,
  83,
  99,
  104,
  107,
  109
]
avoid = control_cases + excluded

# Actual numbers to be exported:
export_numbers = [x for x in numbers if x not in avoid]

# Function for converting number to patient case string:
def name(number):
  prefix = 'AL_COBRA_'
  result = ''
  if number < 10:
    result = prefix + '00' + str(number)
  elif number < 100:
    result = prefix + '0' + str(number)
  else:
    result = prefix + str(number)
  return result

# Function for exporting a patient case (specified by study nr):
def export(number):
  # Database:
  db = get_current('PatientDB')
  # Query patients:
  patients = db.QueryPatientInfo(Filter = {'LastName': name(number)})
  if len(patients) != 1:
    LogFile.write('Unexpected result! Got ' + str(len(patients)) + ' patient(s) for query ' + name(number) + ' \n')
    sys.exit()
  else:
    # Load patient and case:
    patient = db.LoadPatient(PatientInfo = patients[0])
    case = patient.Cases[0]
    # Create a folder for this patient:
    mkdir(patient.Name)
    case.ScriptableDicomExport(
      ExportFolderPath = path.join(getcwd(), patient.Name),
      Examinations = [e.Name for e in case.Examinations],
      RtStructureSetsForExaminations = [e.Name for e in case.Examinations],
      IgnorePreConditionWarnings = True
    )
    print('Export complete for patient {}'.format(name(number)))
    LogFile.write('Export complete for patient ' + patient.Name + ' \n')

# Prepare folder:
if path.isdir(export_folder):
  chdir(export_folder)
else:
  mkdir(export_folder)
  chdir(export_folder)

# Log entry:
LogFile = open(path.join(export_folder, 'export_log.txt'), 'a')
LogFile.write('Script started on ' + time.ctime() + '\n') 

# Iterate case numbers:
#for nr in export_numbers:
  # Export the given case:
  #export(nr)

# Export control cases instead:
# Iterate case numbers:
#for nr in control_cases:
  # Export the given case:
  #export(nr)

for nr in selected_cases:
  # Export the given case:
  export(nr)

# Log script completion:
LogFile.write('Export complete! ' + time.ctime() + '\n')
print('Export complete')
LogFile.close()
