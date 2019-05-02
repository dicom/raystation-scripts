# encoding: utf8

# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Microsoft.Office.Interop.Excel import *
from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton, TextBox)
clr.AddReference("PresentationFramework")
from System.Windows import *
# Import local files:
import beams as BEAMS
import beam_set_functions as BSF
import case_functions as CF
import gui_functions as GUIF
import objectives as OBJ
import region_codes as RC
import roi_functions as ROIF
import structure_set_functions as SSF

# Contains a collection of plan functions.


# Creates additional palliative beamsets (if multiple targets exists).
def create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, fraction_dose, nr_fractions, external, machine_name, nr_existing_beams=1, isocenter=False):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  common_isocenter = False
  if isocenter:
    common_isocenter = True
  i = 1
  if nr_targets > 1:
    for r in region_codes:
      region_code = int(r)
      # Determine the point which will be our isocenter:
      if not isocenter:
        if SSF.has_named_roi_with_contours(ss, 'PTV' + str(i+1)):
          isocenter = SSF.determine_isocenter(examination, ss, region_code, 'VMAT', 'PTV' + str(i+1), external)
          machine_name = SSF.determine_machine_single_target(ss, 'PTV'+str(i+1))
        else:
          GUIF.handle_missing_ptv()
      # Set up beam set and prescription:
      beam_set = plan.AddNewBeamSet(
        Name=BSF.label(region_code, fraction_dose, nr_fractions, 'VMAT'),
        ExaminationName=examination.Name,
        MachineName= machine_name,
        Modality='Photons',
        TreatmentTechnique='VMAT',
        PatientPosition=CF.determine_patient_position(examination),
        NumberOfFractions=nr_fractions
      )
      BSF.add_prescription(beam_set, nr_fractions, fraction_dose, 'CTV' + str(i+1))

      # Setup beams or arcs
      nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, region_code, fraction_dose, 'VMAT', iso_index=str(i+1), beam_index=nr_existing_beams+1)
      nr_existing_beams += nr_beams
      OBJ.create_palliative_objectives_for_additional_beamsets(ss, plan, fraction_dose*nr_fractions, i)
      i += 1
      if not common_isocenter:
        isocenter=False

# Creates additional stereotactic beamsets (if multiple targets exists).
# (Used for brain or lung)
def create_additional_stereotactic_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, fraction_dose, nr_fractions, external, nr_existing_beams=1):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  i = 1
  if nr_targets > 1:
    if int(region_codes[0]) in RC.brain_codes + RC.lung_codes:
      for r in region_codes:
        # Set up beam set and prescription:
        region_code = int(r)
        beam_set = plan.AddNewBeamSet(
          Name=BSF.label_s(region_code, fraction_dose, nr_fractions),
          ExaminationName=examination.Name,
          MachineName= "ALVersa_FFF",
          Modality='Photons',
          TreatmentTechnique='VMAT',
          PatientPosition='HeadFirstSupine',
          NumberOfFractions=nr_fractions
        )
        BSF.add_prescription(beam_set, nr_fractions, fraction_dose, 'PTV' + str(i+1))
        # Determine the point which will be our isocenter:
        isocenter = SSF.determine_isocenter(examination, ss, region_code, 'VMAT', 'PTV' + str(i+1), external)
        # Setup beams or arcs
        nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, region_code, fraction_dose, 'VMAT', iso_index=str(i+1), beam_index=nr_existing_beams+1)
        nr_existing_beams += nr_beams
        i += 1


# Creates a beam set (the first beam set, if multiple beam sets are to me made):
def create_beam_set(plan, name, examination, machine, treatment_technique, nr_fractions, modality='Photons', patient_position="HeadFirstSupine"):
    beam_set = plan.AddNewBeamSet(
      Name=name,
      ExaminationName=examination.Name,
      MachineName=machine,
      Modality=modality,
      TreatmentTechnique=treatment_technique,
      PatientPosition=CF.determine_patient_position(examination),
      NumberOfFractions=nr_fractions
    )
    return beam_set

# Creates an additional beam set for breast patients with a 2 Gy x 8 boost, prescription is set, two beams are set up and common objectives are set:
def create_breast_boost_beamset(ss, plan, examination, isocenter, region_code, roi_name, background_dose=0):
  # Set up beam set and prescription:
  beam_set = plan.AddNewBeamSet(
    Name=BSF.label(region_code, 2, 8, 'Conformal', background_dose=background_dose),
    ExaminationName=examination.Name,
    MachineName= "ALVersa",
    Modality='Photons',
    TreatmentTechnique='Conformal',
    PatientPosition='HeadFirstSupine',
    NumberOfFractions=8
  )
  BSF.add_prescription(beam_set, 8, 2, roi_name)
  if region_code in RC.breast_l_codes:
    BSF.create_two_beams(beam_set, isocenter, name1='LPO', name2='RAO', gantry_angle1='130', gantry_angle2='310', collimator_angle1='343', collimator_angle2='17', iso_index=2)
  elif region_code in RC.breast_r_codes:
    BSF.create_two_beams(beam_set, isocenter, name1='RPO', name2='LAO', gantry_angle1='230', gantry_angle2='50', collimator_angle1='8.9', collimator_angle2='351.5', iso_index=2)
  total_dose = 16
  OBJ.create_breast_boost_objectives(ss, plan, total_dose)



# Returns true if stereotactic fractionation is used
def is_stereotactic(nr_fractions, fraction_dose):
  if nr_fractions in [3, 5, 8] and fraction_dose in [15, 11, 7, 8, 9] or nr_fractions == 1 and fraction_dose > 14:
    return True
  else:
    return False


# Set dose grid, 0.2x0.2x0.2 cm3 for stereotactic treatments and 0.3x03x0.3 cm3 otherwise
def set_dose_grid(plan, region_code, nr_fractions, fraction_dose):
  # Default grid size:
  size = 0.3
  if is_stereotactic(nr_fractions, fraction_dose) or region_code in RC.prostate_codes:
    size = 0.2
  plan.SetDefaultDoseGrid(VoxelSize={'x':size, 'y':size, 'z':size})
