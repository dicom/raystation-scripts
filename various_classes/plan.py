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
#import general_functions as GF
import gui_functions as GUIF
import margin as MARGIN
import objective_functions as OBJF
import patient_model_functions as PMF
import plan_functions as PF
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


    # Check if the last CT has been set as primary, and display a warning if not.
    success = TS_C.TSCase(case).last_examination_used_test()
    if not success:
      GUIF.handle_primary_is_not_most_recent_ct()


    # Setup and run GUI:
    my_window = Tk()
    (region_code, fraction_dose, nr_fractions, initials, total_dose) = GUIF.collect_fractionation_choices(my_window)


    # Load list of region codes and corresponding region names and get the region name for our particular region code (raise error if a name is not retrieved):
    regions = REGIONS.RegionList("C:\\temp\\raystation-scripts\\settings\\regions.tsv")
    region_text = regions.get_text(region_code)
    assert region_text != None


    # For SBRT brain or lung, if there are multiple targets, an extra form appear where
    # the user has to type region code of the other targets.
    # FIXME: Bruke funksjon for test fx?
    # FIXME: Vurder hvor denne koden bør ligge.
    target = None
    palliative_choices = None
    nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
    if nr_targets > 1:
      if region_code in RC.brain_codes + RC.lung_codes:
        if PF.is_stereotactic(nr_fractions, fraction_dose):
          region_codes = GUIF.multiple_beamset_form(ss, Toplevel())
          GUIF.check_region_codes(region_code, region_codes)
      elif region_code in RC.palliative_codes:
        # For palliative cases with multiple targets:
        palliative_choices = GUIF.palliative_beamset_form(ss, Toplevel())
        if palliative_choices[0] in ['sep_beamset_iso', 'sep_beamset_sep_iso']:
          region_codes = GUIF.multiple_beamset_form(ss, Toplevel())
          GUIF.check_region_codes(region_code, region_codes)
          if SSF.has_roi_with_shape(ss, ROIS.ctv1.name):
            target = ROIS.ctv1.name
          elif SSF.has_roi_with_shape(ss, ROIS.ctv2.name):
            target = ROIS.ctv2.name
          elif SSF.has_roi_with_shape(ss, ROIS.ctv3.name):
            target = ROIS.ctv3.name
          elif SSF.has_roi_with_shape(ss, ROIS.ctv4.name):
            target = ROIS.ctv4.name
        elif palliative_choices[0] == 'sep_plan':
          target = palliative_choices[1]


    # Set up plan, making sure the plan name does not already exist. If the plan name exists, (1), (2), (3) etc is added behind the name.
    plan = CF.create_plan(case, examination, region_text)


    # Check that the number of fractions and fraction dose is among those expected for the given region code
    GUIF.check_input(ss, region_code, nr_fractions, fraction_dose)


    # Set planners initials
    plan.PlannedBy = initials


    # Set dose grid, 0.2x0.2x0.2 cm3 for stereotactic treatments and for prostate and 0.3x03x0.3 cm3 otherwise
    PF.set_dose_grid(plan, region_code, nr_fractions, fraction_dose)

    my_window = Toplevel()
    # Determine which technique and optimization choices which will appear in the form
    results = GUIF.determine_choices(region_code, nr_fractions, fraction_dose, my_window, [])
    # Chosen technique value, 'VMAT' or 'Conformal'
    technique = results[0]
    # Chosen technique name, 'VMAT' or '3D-CRT'
    technique_name = results[1]
    # Chosen optimization value
    opt = results[2]
    

    # Determine prescription target:
    if not target:
      roi_dict = SSF.create_roi_dict(ss)
      target = SSF.determine_target(ss, roi_dict, nr_fractions, fraction_dose)


    # Translate the couch in the longitudinal direction according to the target position
    if SSF.has_roi_with_shape(ss, ROIS.couch.name):
      PMF.translate_couch_long(pm, ss, examination, target)


    # Create 'Mask_PTV' for partial brain and stereotactic brain
    if region_code in RC.brain_codes and region_code not in RC.brain_whole_codes:
      if nr_targets > 1:
        targets = [ROIS.ptv1, ROIS.ptv2, ROIS.ptv3, ROIS.ptv4]
        for i in range(nr_targets):
          SSF.create_expanded_and_intersected_volume(pm, examination, ss, targets[i], ROIS.external, ROIS.mask_ptv.name+str(i+1), 1600)
          patient.SetRoiVisibility(RoiName = ROIS.mask_ptv.name+str(i+1), IsVisible = False)
      else:
          SSF.create_expanded_and_intersected_volume(pm, examination, ss, ROIS.ptv, ROIS.external, ROIS.mask_ptv.name, 1600)
          patient.SetRoiVisibility(RoiName = ROIS.mask_ptv.name, IsVisible = False)
          


    # Create 'Mask_PTV' for stereotactic lung
    if region_code in RC.lung_codes and PF.is_stereotactic(nr_fractions, fraction_dose):
      if nr_targets > 1:
        targets = [ROIS.ptv1, ROIS.ptv2, ROIS.ptv3]
        for i in range(nr_targets):
          created = SSF.create_roi_subtraction(pm, examination, ss, targets[i], ROIS.chestwall, ROIS.mask_ptv.name+str(i+1), 0)
          if created:
            patient.SetRoiVisibility(RoiName = ROIS.mask_ptv.name+str(i+1), IsVisible = False)
      else:
        created = SSF.create_roi_subtraction(pm, examination, ss, ROIS.ptv, ROIS.chestwall, ROIS.mask_ptv.name, 0)
        if created:
          patient.SetRoiVisibility(RoiName = ROIS.mask_ptv.name, IsVisible = False)


    # Determine name of the body contour ('External' or 'Body'):
    external = SSF.body_roi_name(ss)
    if not external:
      GUIF.handle_missing_external()


    # Determine the machine name from the size of the target volume, only one target is taken into consideration here.
    # For those situations where you have two targets and you want to have separate isocenters, then you what to evaluate the targets separately.
    if target in [ROIS.ctv1.name, ROIS.ctv2.name, ROIS.ctv3.name, ROIS.ctv4.name] and palliative_choices[0] in ['sep_beamset_sep_iso', 'sep_plan']:
      energy_name = SSF.determine_energy_single_target(ss, target)
    elif region_code in RC.breast_codes:
      energy_name = '6'
    else:
      # Determine the machine name from the size of the target volume:
      energy_name = SSF.determine_energy(ss, target)

    # Create the name of the beamset
    beam_set_name = BSF.label(region_code, fraction_dose, nr_fractions, technique)


    # Create primary beam set:
    beam_set = PF.create_beam_set(plan, beam_set_name, examination, technique, nr_fractions)
    # Add prescription:
    BSF.add_prescription(beam_set, nr_fractions, fraction_dose, target)
    # Determine the point which will be our isocenter:
    if nr_targets > 1:
      if palliative_choices and palliative_choices[0] in ['sep_beamset_iso','beamset']:
        # Consider all targets when determining isocenter:
        isocenter = SSF.determine_isocenter(examination, ss, region_code, technique_name, target, external, multiple_targets = True)
      else:
        # Set isocenter for PTV1:
        isocenter = SSF.determine_isocenter(examination, ss, region_code, technique_name, target, external)
    else:
      # Consider all targets when determining isocenter:
      isocenter = SSF.determine_isocenter(examination, ss, region_code, technique_name, target, external, multiple_targets = True)
    # Determine if this patient has any previous beams in Mosaiq (which impacts which beam number is to be used with this plan):
    beam_nr = 1
    if self.mq_patient:
      beam_nr = self.mq_patient.next_available_field_number()
    # Setup beams or arcs
    nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, region_code, fraction_dose, technique_name, energy_name, beam_index=beam_nr)


    # For SBRT brain or lung, if there are multiple targets, create beam sets for all targets
    # FIXME: Bruke funksjon for test fx?
    if nr_targets > 1:
      if region_code in RC.brain_codes + RC.lung_codes and region_code not in RC.brain_whole_codes:
        if PF.is_stereotactic(nr_fractions, fraction_dose):
          PF.create_additional_stereotactic_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, fraction_dose, nr_fractions, external, energy_name, nr_existing_beams = nr_beams)
      elif region_code in RC.palliative_codes:
        # Palliative cases with multiple targets:
        if palliative_choices[0] in ['sep_beamset_iso', 'sep_beamset_sep_iso']:
          if palliative_choices[0] == 'sep_beamset_iso':
            PF.create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, fraction_dose, nr_fractions, external, energy_name, nr_existing_beams = nr_beams, isocenter = isocenter)
          else:
            PF.create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, fraction_dose, nr_fractions, external, energy_name, nr_existing_beams = nr_beams)


    # If there is a 2Gy x 8 boost for breast patients
    if SSF.has_roi_with_shape(ss, ROIS.ctv_sb.name) and SSF.has_roi_with_shape(ss, ROIS.ptv_c.name) and region_code in RC.breast_codes:
      PF.create_breast_boost_beamset(ss, plan, examination, isocenter, region_code, ROIS.ctv_sb.name, background_dose=int(round(fraction_dose*nr_fractions)))
      # Make sure that the original beam set (not this boost beam set) is loaded in the GUI:
      infos = plan.QueryBeamSetInfo(Filter={'Name':'^'+beam_set_name+'$'})
      plan.LoadBeamSet( BeamSetInfo=infos[0])


    # Determines and sets up isodoses based on region code and fractionation
    CF.determine_isodoses(case, ss, region_code, nr_fractions, fraction_dose)


    # Determine site
    site = SF.site(pm, examination, ss, plan, nr_fractions, total_dose, region_code, target, technique_name)


    # Set up Clinical Goals:
    es = plan.TreatmentCourse.EvaluationSetup
    CG.setup_clinical_goals(ss, es, site, total_dose, nr_fractions, target)
    # Loads the plan, done after beam set is created, as this is the only way the CT-images appears in Plan Design and Plan Optimization when the plan is loaded
    CF.load_plan(case, plan)


    # Set up beams and optimization for breast patients
    if technique_name == 'VMAT' and region_code in RC.breast_reg_codes:
      # Use robust optimization for VMAT breast:
      OBJF.set_robustness_breast(plan, region_code)
    elif technique_name == '3D-CRT' and region_code in RC.breast_codes:
      if region_code in RC.breast_reg_codes:
        BSF.set_up_beams_and_optimization_for_regional_breast(plan, beam_set, ROIS.ptv_c.name, region_code)
      else:
        BSF.set_up_beams_and_optimization_for_tangential_breast(plan, beam_set, plan.PlanOptimizations[0], target.replace("C", "P")+"c")
        # If there is a 2Gy x 8 boost for breast patients
        if SSF.has_roi_with_shape(ss, ROIS.ctv_sb.name) and SSF.has_roi_with_shape(ss, ROIS.ptv_c.name):
          BSF.set_up_beams_and_optimization_for_tangential_breast(plan, plan.BeamSets[1], plan.PlanOptimizations[1], ROIS.ptv_sbc.name)

    # Set up treat and protect for stereotactic lung
    #if region_code in RC.lung_codes and PF.is_stereotactic(nr_fractions, fraction_dose):
    #  BSF.set_up_treat_and_protect_for_stereotactic_lung(beam_set, target, 0.5)


    # Run first optimization on each beam set:
    for po in plan.PlanOptimizations:
      po.OptimizationParameters.DoseCalculation.ComputeFinalDose = True
      # Set 'Constrain leaf motion' to 0.3 for stereotactic patients
      if PF.is_stereotactic(nr_fractions, fraction_dose):
        acp = po.OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties
        acp.UseMaxLeafTravelDistancePerDegree = True
        acp.MaxLeafTravelDistancePerDegree = 0.3
      po.RunOptimization()


    # Start adaptive optimization if indicated 
    if opt == 'oar':
      OBJF.adapt_optimization_oar(ss, plan, site.oar_objectives, region_code)
      if region_code in RC.breast_codes:
        if region_code in RC.breast_reg_codes:
          # Need to close leafs behind jaw for breast regional patients 
          BSF.close_leaves_behind_jaw_for_regional_breast(beam_set)
        # Create 2.5 cm margin to air for breast patient planned with a 3D-CRT technique for robustness purpuses
        BSF.create_margin_air_for_3dcrt_breast(ss, beam_set, region_code)
        # Compute dose
        beam_set.ComputeDose(DoseAlgorithm = 'CCDose')
      # Auto scale to prescription
      for po in plan.PlanOptimizations:
        po.AutoScaleToPrescription = True
    # Load plan
    CF.load_plan(case, plan)



    # Save
    patient.Save()


