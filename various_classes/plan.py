# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys, os
from tkinter import *
from tkinter import messagebox
import math

# Import local files:
import beams as BEAMS
import beam_set_functions as BSF
import case_functions as CF
import clinical_goal as CG
import fractionation_frame as FORM
import gui_functions as GUIF
import margin as MARGIN
import objective_functions as OBJF
import optimization as OPT
import patient_model_functions as PMF
import plan_functions as PF
import prescription as PRES
import region_codes as RC
import region_list as REGIONS
import roi as ROI
import roi_functions as ROIF
import rois as ROIS
import site_functions as SF
import structure_set_functions as SSF
import ts_case as TS_C


class Plan(object):
  def __init__(self, patient, case, mq_patient):
    self.patient = patient
    self.case = case
    self.mq_patient = mq_patient


    # Load patient model, examination and structure set:
    pm = case.PatientModel
    examination = get_current("Examination")
    ss = PMF.get_structure_set(pm, examination)


    # Determine if a target volume is present (raises error if not):
    if not PMF.has_defined_ctv_or_ptv(pm, examination):
      GUIF.handle_missing_ctv_or_ptv()


    # Check if the last CT has been set as primary, and display a warning if not:
    most_recent_CT_examination_used = TS_C.TSCase(case).last_examination_used_test()
    if not most_recent_CT_examination_used:
      GUIF.handle_primary_is_not_most_recent_ct()


    # Setup and run GUI:
    my_window = Tk()
    (region_code, fraction_dose, nr_fractions, initials, total_dose) = GUIF.collect_fractionation_choices(my_window)


    # Load list of region codes and corresponding region names, and get the region name for our particular region code (raise error if a name is not retrieved):
    regions = REGIONS.RegionList("C:\\temp\\raystation-scripts\\settings\\regions.tsv")
    region_text = regions.get_text(region_code)
    assert region_text != None
    
    # Establish the number of target volumes:
    nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
    
    # Create the prescription object:
    prescription = PRES.create_prescription(total_dose, nr_fractions, region_code, ss)
    # Validate the prescription:
    valid = PRES.validate_prescription(prescription)
    if not valid:
      GUIF.handle_invalid_prescription(prescription, region_text)


    # For SBRT or palliative, if there are multiple targets, display an extra form
    # where the user can specify the region code(s) of the other target(s).
    target, palliative_choices, region_codes = GUIF.collect_target_strategy_and_region_codes(ss, nr_targets, prescription)

    
    # Set up plan, making sure the plan name does not already exist. If the plan name exists, (1), (2), (3) etc is added behind the name:
    plan = CF.create_plan(case, examination, region_text, initials)


    my_window = Toplevel()


    # For extremeties there a choice will be given between VMAT or 3D-CRT (for all other sites, VMAT is default):
    # Parameter values: technique ('VMAT' or 'Conformal'), technique name ('VMAT' or '3D-CRT') 
    technique, technique_name = GUIF.determine_choices(prescription, my_window)
    

    # Determine the prescription target volume:
    if not target:
      roi_dict = SSF.create_roi_dict(ss)
      target = SSF.determine_target(ss, roi_dict, prescription)


    # Create 'Mask_PTV' for partial brain and stereotactic brain:
    if region_code in RC.brain_codes and region_code not in RC.brain_whole_codes:
      PMF.create_mask_ptv_brain(patient, pm, examination, ss, nr_targets)


    # Create 'Mask_PTV' for stereotactic lung:
    if region_code in RC.lung_codes and prescription.is_stereotactic():
      PMF.create_mask_ptv_lung(patient, pm, examination, ss, nr_targets)


    # Determine name of the body contour ('External' or 'Body'):
    external = SSF.body_roi_name(ss)
    if not external:
      GUIF.handle_missing_external()


    # Determine the energy quality from the size of the target volume (note that only one target is taken into consideration here).
    # For those situations where you have two targets and you want to have separate isocenters, then you want to evaluate the targets separately.
    if prescription.is_stereotactic():
      energy_name = '6 FFF'
    elif target in [ROIS.ctv1.name, ROIS.ctv2.name, ROIS.ctv3.name, ROIS.ctv4.name] and palliative_choices[0] in ['sep_beamset_sep_iso', 'sep_plan']:
      energy_name = SSF.determine_energy_single_target(ss, target)
    elif region_code in RC.breast_codes:
      if region_code in RC.breast_partial_codes:
        energy_name = '6 FFF'
      else:
        energy_name = '6'
    else:
      # Determine the energy quality from the size of the target volume:
      energy_name = SSF.determine_energy(ss, target)

    # Create beamset name:
    beam_set_name = BSF.label(prescription, technique)


    # Create primary beam set:
    beam_set = PF.create_beam_set(plan, beam_set_name, examination, technique, prescription.nr_fractions)
    
    # Add prescription:
    # For breast SIB, set the surgical bed as prescription target (for others leave it as is):
    if prescription.nr_fractions == 15 and prescription.total_dose == 48 and region_code in RC.breast_codes:
      prescription.target = ROIS.ctv_sb.name
    else:
      prescription.target = target
    BSF.add_prescription(beam_set, prescription)

    # Set beam set dose grid:
    BSF.set_dose_grid(beam_set, prescription)

    # Determine the point which will be our isocenter:
    if nr_targets > 1:
      if palliative_choices and palliative_choices[0] in ['sep_beamset_iso', 'beamset']:
        # Consider all targets when determining isocenter:
        isocenter = SSF.determine_isocenter(examination, ss, region_code, target, external, multiple_targets = True)
      else:
        # Set isocenter for PTV1:
        isocenter = SSF.determine_isocenter(examination, ss, region_code, target, external)
    else:
      # Consider all targets when determining isocenter:
      isocenter = SSF.determine_isocenter(examination, ss, region_code, target, external, multiple_targets = True)
    
    
    # Determine if this patient has any previous beams in Mosaiq (which impacts which beam number is to be used with this plan):
    beam_nr = 1
    if self.mq_patient:
      beam_nr = self.mq_patient.next_available_field_number()
    # Setup beams:
    nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, prescription, technique_name, energy_name, beam_index=beam_nr)
    last_beam_index = beam_nr + nr_beams - 1

    
    # Determines and sets up isodoses based on region code and fractionation:
    CF.determine_isodoses(case, ss, prescription)
    
    # Loads the plan (done after beam set is created, as this is the only way the CT-images appears in Plan Design and Plan Optimization when the plan is loaded):
    CF.load_plan(case, plan)


    # Determine site:
    site = SF.site(pm, examination, ss, plan, prescription, target)


    # Set up Clinical Goals:
    es = plan.TreatmentCourse.EvaluationSetup
    CG.setup_clinical_goals(ss, es, site, prescription, target)
    
    
    # For SBRT brain or lung, if there are multiple targets, create beam sets for all targets:
    if nr_targets > 1:
      if region_code in RC.brain_codes + RC.lung_codes and region_code not in RC.brain_whole_codes:
        if prescription.is_stereotactic():
          PF.create_additional_stereotactic_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams = last_beam_index)
      elif region_code in RC.palliative_codes:
        # Palliative cases with multiple targets:
        if palliative_choices[0] == 'sep_beamset_iso':
          # Separate beam sets, but with the same isocenter:
          PF.create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams = last_beam_index, isocenter = isocenter)
        elif palliative_choices[0] == 'sep_beamset_sep_iso':
          # Separate beams sets and separate isocenter:
          PF.create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams = last_beam_index)


    # Use robust optimization for breast:
    if region_code in RC.breast_codes:
      OBJF.set_robustness_breast(plan, region_code)


    # Perform optimization:
    if site.optimizer:
      site.optimizer.optimize()


    # Load plan:
    CF.load_plan(case, plan)


    # Save:
    patient.Save()
