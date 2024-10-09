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
import clinical_goal as CG
import gui_functions as GUIF
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
      BSF.add_prescription(beam_set, p)
      # Setup beams or arcs
      nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, p, 'VMAT', energy_name, iso_index=str(i+1), beam_index=nr_existing_beams+1)
      nr_existing_beams = nr_existing_beams + nr_beams
      i += 1
      if not common_isocenter:
        isocenter=False
      # Add objectives for the new beam set:
      obj = objectives.Other(ss, plan, p, beam_set_index=beam_set.Number-1)
      # Add OAR clinical goals to the existing plan for the new beam set:
      cg = clinical_goals.Other(ss, plan, p)
      es = plan.TreatmentCourse.EvaluationSetup
      CG.setup_oar_clinical_goals(cg.oars, es, p)


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
        isocenter = SSF.determine_isocenter(examination, ss, region_code, 'PTV' + str(i+1), external)
        # Setup beams or arcs
        nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, prescription, 'VMAT', energy_name, iso_index=str(i+1), beam_index=nr_existing_beams+1)
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


# Determines the first available beam number for this plan (which is the highest existing beam number + 1).
def first_available_beam_number(plan):
  highest_number = 0
  for bs in plan.BeamSets:
    for b in bs.Beams:
      if b.Number > highest_number:
        highest_number = b.Number
  return highest_number + 1

