# Import system libraries:
from connect import *
import clr, sys, os
from tkinter import *
from tkinter import messagebox

# Import local files:
import def_choices as DC
import patient_model_setup as PMS
import gui_functions as GUIF
import patient_model_functions as PMF
import radio_button as RB


class Definition(object):
  """A class for configuration of a patient model for a given treatment site derived from user selections in a GUI.

  Attributes:
    patient_db (PyScriptObject): The RayStation PatientDB instance.
    patient (PyScriptObject): The RayStation Patient instance.
    case (PyScriptObject): The RayStation Case instance.
  """

  def __init__(self, patient_db, patient, case):
    """Initializes the patient model with the relevant RayStation instances.

    Args:
      patient_db (PyScriptObject): The RayStation PatientDB instance.
      patient (PyScriptObject): The RayStation Patient instance.
      case (PyScriptObject): The RayStation Case instance.
    """
    self.patient_db = patient_db
    self.patient = patient
    self.case = case

    # Load patient model, examination and structure set:
    pm = case.PatientModel
    examination = get_current("Examination")
    ss = PMF.get_structure_set(pm, examination)

    # Handle existing ROIs (if there are any):
    my_window = GUIF.handle_existing_rois(pm, ss)

    # Create initial radiobutton object, then recursively iterate it to collect all user choices:
    regions = RB.RadioButton('Behandlingsregion', 'Velg behandlingsregion:', DC.regions)
    choices = GUIF.collect_choices(regions, my_window, [])

    # Create site:
    site = PMS.PatientModelSetup(patient_db, pm, examination, ss, choices, targets = [], oars = [])

    # Choice 1: Which region is going to be treated?
    region = choices[0]

    # Execute the def script which corresponds to the user choice:
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

    # Changes OrganType to "Other" for all ROIs in the given patient model which are of type "Undefined" or "Marker".
    PMF.exclude_rois_from_export(pm)
    PMF.set_all_undefined_to_organ_type_other(pm)
