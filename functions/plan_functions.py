# encoding: utf8

# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys
from System.Windows import *

# Import local files:
import clinical_goals
import objectives
import beams as BEAMS
import beam_set_functions as BSF
import case_functions as CF
import gui_functions as GUIF
import prescription as PRES
import structure_set_functions as SSF

# Contains a collection of plan functions.


# Creates additional palliative beamsets (if multiple targets exists).
def create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams=1, isocenter=False):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  common_isocenter = False
  if isocenter:
    common_isocenter = True
  i = 1
  beam_sets = []
  prescriptions = []
  if nr_targets > 1:
    for r in region_codes:
      region_code = int(r)
      # Create a prescription for this region code (using the same dose/fractions as in the original prescription):
      p = PRES.create_prescription(prescription.total_dose, prescription.nr_fractions, region_code, ss)
      p.target = 'CTV' + str(i+1)
      # Determine the point which will be our isocenter:
      if not isocenter:
        if SSF.has_named_roi_with_contours(ss, 'PTV' + str(i+1)):
          isocenter = SSF.determine_isocenter(examination, ss, region_code, 'PTV' + str(i+1), external)
          energy_name = SSF.determine_energy_single_target(ss, 'PTV'+str(i+1))
        else:
          GUIF.handle_missing_ptv()
      # Set up beam set and prescription:
      beam_set = plan.AddNewBeamSet(
        Name=BSF.label(p, 'VMAT'),
        ExaminationName=examination.Name,
        MachineName= "ALVersa",
        Modality='Photons',
        TreatmentTechnique='VMAT',
        PatientPosition=CF.determine_patient_position(examination),
        NumberOfFractions=p.nr_fractions
      )
      beam_sets.append(beam_set)
      prescriptions.append(p)
      BSF.add_prescription(beam_set, p)
      # Setup beams or arcs
      nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, p, 'VMAT', energy_name, iso_index=str(i+1), beam_index=nr_existing_beams+1)
      nr_existing_beams = nr_existing_beams + nr_beams
      if not common_isocenter:
        isocenter=False
      i += 1
  return beam_sets, prescriptions


# Creates additional stereotactic beamsets (if multiple targets exists).
def create_additional_stereotactic_beamsets_prescriptions_and_beams(plan, examination, ss, additional_region_codes, prescription, external, energy_name, nr_existing_beams=1):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  i = 1
  beam_sets = []
  prescriptions = []
  if nr_targets > 1:
    for r in additional_region_codes:
      region_code = int(r)
      # Create the prescription object:
      p = PRES.create_prescription(prescription.total_dose, prescription.nr_fractions, region_code, ss)
      p.target = 'PTV' + str(i+1)
      # Create beam set:
      beam_set = plan.AddNewBeamSet(
        Name=BSF.label_s(region_code, p.fraction_dose, p.nr_fractions),
        ExaminationName=examination.Name,
        MachineName= "ALVersa",
        Modality='Photons',
        TreatmentTechnique='VMAT',
        PatientPosition='HeadFirstSupine',
        NumberOfFractions=p.nr_fractions
      )
      beam_sets.append(beam_set)
      prescriptions.append(p)
      BSF.add_prescription(beam_set, p)
      # Determine the point which will be our isocenter:
      isocenter = SSF.determine_isocenter(examination, ss, region_code, p.target, external)
      # Setup beams or arcs
      nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, p, 'VMAT', energy_name, iso_index=str(i+1), beam_index=nr_existing_beams+1)
      nr_existing_beams += nr_beams
      i += 1
  return beam_sets, prescriptions


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


# Determines the first available beam number for this plan (which is the highest existing beam number + 1).
def first_available_beam_number(plan):
  highest_number = 0
  for bs in plan.BeamSets:
    for b in bs.Beams:
      if b.Number > highest_number:
        highest_number = b.Number
  return highest_number + 1
