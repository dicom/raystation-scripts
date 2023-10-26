# encoding: utf8

# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys

from System.Windows import *
# Import local files:
import beams as BEAMS
import beam_set_functions as BSF
import case_functions as CF
import gui_functions as GUIF
import objectives as OBJ
import prescription as PRES
import region_codes as RC
import roi_functions as ROIF
import structure_set_functions as SSF

# Contains a collection of plan functions.


# Creates additional palliative beamsets (if multiple targets exists).
def create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams=1, isocenter=False):
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
          energy_name = SSF.determine_energy_single_target(ss, 'PTV'+str(i+1))
        else:
          GUIF.handle_missing_ptv()
      # Set up beam set and prescription:
      beam_set = plan.AddNewBeamSet(
        Name=BSF.label(region_code, prescription, 'VMAT'),
        ExaminationName=examination.Name,
        MachineName= "ALVersa",
        Modality='Photons',
        TreatmentTechnique='VMAT',
        PatientPosition=CF.determine_patient_position(examination),
        NumberOfFractions=prescription.nr_fractions
      )
      BSF.add_prescription(beam_set, prescription, 'CTV' + str(i+1))
      # Setup beams or arcs
      nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, region_code, prescription.fraction_dose, 'VMAT', energy_name, iso_index=str(i+1), beam_index=nr_existing_beams+1)
      nr_existing_beams = nr_existing_beams + nr_beams
      OBJ.create_palliative_objectives_for_additional_beamsets(ss, plan, prescription.fraction_dose*prescription.nr_fractions, i)
      i += 1
      if not common_isocenter:
        isocenter=False


# Creates additional stereotactic beamsets (if multiple targets exists).
# (Used for brain or lung)
def create_additional_stereotactic_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams=1):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  i = 1
  if nr_targets > 1:
    if int(region_codes[0]) in RC.brain_codes + RC.lung_codes:
      for r in region_codes:
        # Set up beam set and prescription:
        region_code = int(r)
        beam_set = plan.AddNewBeamSet(
          Name=BSF.label_s(region_code, prescription.fraction_dose, prescription.nr_fractions),
          ExaminationName=examination.Name,
          MachineName= "ALVersa",
          Modality='Photons',
          TreatmentTechnique='VMAT',
          PatientPosition='HeadFirstSupine',
          NumberOfFractions=prescription.nr_fractions
        )
        BSF.add_prescription(beam_set, prescription, 'PTV' + str(i+1))
        # Determine the point which will be our isocenter:
        isocenter = SSF.determine_isocenter(examination, ss, region_code, 'VMAT', 'PTV' + str(i+1), external)
        # Setup beams or arcs
        nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, region_code, prescription.fraction_dose, 'VMAT', energy_name, iso_index=str(i+1), beam_index=nr_existing_beams+1)
        nr_existing_beams += nr_beams
        i += 1


# Creates a beam set (the first beam set, if multiple beam sets are to me made).
def create_beam_set(plan, name, examination, treatment_technique, nr_fractions, modality='Photons', patient_position="HeadFirstSupine"):
    beam_set = plan.AddNewBeamSet(
      Name=name,
      ExaminationName=examination.Name,
      MachineName="ALVersa",
      Modality=modality,
      TreatmentTechnique=treatment_technique,
      PatientPosition=CF.determine_patient_position(examination),
      NumberOfFractions=nr_fractions
    )
    return beam_set


# Creates an additional beam set for breast patients with a 2 Gy x 8 boost.
# (Prescription is set, three conventional beams are set up and common objectives are set)
def create_breast_boost_beamset(ss, plan, examination, isocenter, region_code, roi_name, background_dose=0):
  # Create prescription:
  prescription = PRES.create_prescription(16, 8, region_code, ss)
  # Determine first available beam number:
  next_beam_number = first_available_beam_number(plan)
  # Set up beam set and prescription:
  beam_set = plan.AddNewBeamSet(
    Name=BSF.label(region_code, prescription, 'VMAT', background_dose=background_dose),
    ExaminationName=examination.Name,
    MachineName= "ALVersa",
    Modality='Photons',
    TreatmentTechnique='VMAT',
    PatientPosition='HeadFirstSupine',
    NumberOfFractions=prescription.nr_fractions
  )
  BSF.add_prescription(beam_set, prescription, roi_name)
  # Create arcs:
  if region_code in RC.breast_l_codes:
    BSF.create_single_arc(beam_set, isocenter, energy = '6', gantry_stop_angle = '300', gantry_start_angle = '179', collimator_angle = '5', iso_index=2, beam_index=next_beam_number)
  elif region_code in RC.breast_r_codes:
    BSF.create_single_arc(beam_set, isocenter, energy = '6', gantry_stop_angle = '60', gantry_start_angle = '181', collimator_angle = '5', iso_index=2, beam_index=next_beam_number)
  OBJ.create_breast_boost_objectives(ss, plan, region_code, prescription.total_dose)


# Determines the first available beam number for this plan (which is the highest existing beam number + 1).
def first_available_beam_number(plan):
  highest_number = 0
  for bs in plan.BeamSets:
    for b in bs.Beams:
      if b.Number > highest_number:
        highest_number = b.Number
  return highest_number + 1

