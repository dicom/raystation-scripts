'''Executes the Definition script, which sets up all ROIs and POIs needed for treatment planning in RayStation.

Authors:
Christoffer Lervåg & Marit Funderud
Helse Møre og Romsdal HF
'''

# Import system libraries:
import clr, sys, os
from tkinter import *
from tkinter import messagebox

# Import RayStation packages:
sys.path.append("C:/Program Files/RaySearch Laboratories/RayStation 2024B/ScriptClient/")
from connect import *

# Add local folders to the system path:
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
import def_choices as DC
import patient_model_setup as PMS
import gui_functions as GUIF
import patient_model_functions as PMF
import radio_button as RB


def main():
  '''Loads patient and case data and performs configuration of the patient model for a given treatment
  site from user selections in a GUI.
  '''
  # Load patient, case and db:
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
  
  # Get patient model, examination and structure set:
  pm = case.PatientModel
  examination = get_current("Examination")
  ss = PMF.get_structure_set(pm, examination)

  # Handle existing ROIs (if there are any):
  my_window = GUIF.handle_existing_rois(pm, ss)

  # Create initial radiobutton object, then recursively iterate it to collect all user choices:
  regions = RB.RadioButton('Behandlingsregion', 'Velg behandlingsregion:', DC.regions)
  choices = GUIF.collect_choices(regions, my_window, [])

  # Create patient model setup (site):
  site = PMS.PatientModelSetup(patient_db, pm, examination, ss, choices, targets = [], oars = [])

  # Choice 1: Which region is going to be setup?
  region = choices[0]

  # Execute the site specific def script which corresponds to the user choice:
  if region == 'brain':
    import def_brain as DEF_BRAIN
    DEF_BRAIN.DefBrain(pm, examination, ss, choices, site)
  elif region == 'lung':
    import def_lung as DEF_LUNG
    DEF_LUNG.DefLung(pm, examination, ss, choices, site)
  elif region == 'breast':
    import def_breast as DEF_BREAST
    DEF_BREAST.DefBreast(pm, ss, choices, site)
  elif region == 'bladder':
    import def_bladder as DEF_BLADDER
    DEF_BLADDER.DefBladder(patient, pm, ss, choices, site)
  elif region == 'prostate':
    import def_prostate as DEF_PROSTATE
    DEF_PROSTATE.DefProstate(pm, ss, choices, site)
  elif region == 'rectum':
    import def_rectum as DEF_RECTUM
    DEF_RECTUM.DefRectum(patient, pm, ss, choices, site)
  elif region == 'other':
    import def_palliative as DEF_PALLIATIVE
    DEF_PALLIATIVE.DefPalliative(pm, ss, choices, site)

  # Exclude ROIs from export:
  PMF.exclude_rois_from_export(pm)
  # Changes OrganType to "Other" for all ROIs in the given patient model which are of type "Undefined" or "Marker".
  PMF.set_all_undefined_to_organ_type_other(pm)

# Execution:
if __name__ == "__main__":
  main()