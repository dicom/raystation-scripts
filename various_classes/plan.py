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
    success = TS_C.TSCase(case).last_examination_used_test()
    if not success:
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
    valid = PRES.validate_prescription(prescription, region_code)
    if not valid:
      GUIF.handle_invalid_prescription(prescription, region_code, region_text)


    # For SBRT brain or lung, if there are multiple targets, display an extra form
    # where the user can specify the region code(s) of the other target(s).
    target, palliative_choices, region_codes = GUIF.collect_target_strategy_and_region_codes(ss, nr_targets, region_code, prescription)

    
    # Set up plan, making sure the plan name does not already exist. If the plan name exists, (1), (2), (3) etc is added behind the name:
    plan = CF.create_plan(case, examination, region_text)


    # Set planners initials:
    plan.PlannedBy = initials

    my_window = Toplevel()

    # Determine which technique and optimization choices which will appear in the form:
    results = GUIF.determine_choices(region_code, prescription, my_window, [])
    # Chosen technique value ('VMAT' or 'Conformal'):
    technique = results[0]
    # Chosen technique name ('VMAT' or '3D-CRT'):
    technique_name = results[1]
    # Chosen optimization value:
    opt = results[2]
    

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
    beam_set_name = BSF.label(region_code, prescription, technique)


    # Create primary beam set:
    beam_set = PF.create_beam_set(plan, beam_set_name, examination, technique, prescription.nr_fractions)
    
    # Add prescription:
    # For breast SIB, set the surgical bed as prescription target (for others leave it as is):
    if prescription.nr_fractions == 15 and prescription.total_dose == 48 and region_code in RC.breast_codes:
      prescription_target = ROIS.ctv_sb.name
    else:
      prescription_target = target
    BSF.add_prescription(beam_set, prescription, prescription_target)

    # Set beam set dose grid:
    BSF.set_dose_grid(beam_set, region_code, prescription)

    # Determine the point which will be our isocenter:
    if nr_targets > 1:
      if palliative_choices and palliative_choices[0] in ['sep_beamset_iso', 'beamset']:
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
    # Setup beams (or arcs):
    nr_beams = BEAMS.setup_beams(ss, examination, beam_set, isocenter, region_code, prescription.fraction_dose, technique_name, energy_name, beam_index=beam_nr)
    last_beam_index = beam_nr + nr_beams - 1


    # For SBRT brain or lung, if there are multiple targets, create beam sets for all targets:
    if nr_targets > 1:
      if region_code in RC.brain_codes + RC.lung_codes and region_code not in RC.brain_whole_codes:
        if prescription.is_stereotactic():
          PF.create_additional_stereotactic_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams = last_beam_index)
      elif region_code in RC.palliative_codes:
        # Palliative cases with multiple targets:
        if palliative_choices[0] in ['sep_beamset_iso', 'sep_beamset_sep_iso']:
          if palliative_choices[0] == 'sep_beamset_iso':
            PF.create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams = last_beam_index, isocenter = isocenter)
          else:
            PF.create_additional_palliative_beamsets_prescriptions_and_beams(plan, examination, ss, region_codes, prescription, external, energy_name, nr_existing_beams = last_beam_index)


    # Creates a 2 Gy x 8 boost beam set for breast patients, if indicated:
    if SSF.breast_sequentual_boost_is_indicated(ss, region_code, prescription):
      PF.create_breast_boost_beamset(ss, plan, examination, isocenter, region_code, ROIS.ctv_sb.name, background_dose=int(round(prescription.total_dose)))
      # Make sure that the original beam set (not this boost beam set) is loaded in the GUI:
      infos = plan.QueryBeamSetInfo(Filter={'Name':'^'+beam_set_name+'$'})
      plan.LoadBeamSet( beamSetInfo=infos[0])


    # Determines and sets up isodoses based on region code and fractionation:
    CF.determine_isodoses(case, ss, region_code, prescription)


    # Determine site:
    site = SF.site(pm, examination, ss, plan, prescription, region_code, target, technique_name)


    # Set up Clinical Goals:
    es = plan.TreatmentCourse.EvaluationSetup
    CG.setup_clinical_goals(ss, es, site, prescription, target)
    # Loads the plan (done after beam set is created, as this is the only way the CT-images appears in Plan Design and Plan Optimization when the plan is loaded):
    CF.load_plan(case, plan)


    # Set up beams and optimization for breast patients:
    if technique_name == 'VMAT' and region_code in RC.breast_codes:
      # Use robust optimization for VMAT breast:
      OBJF.set_robustness_breast(plan, region_code)
    elif technique_name == '3D-CRT' and region_code in RC.breast_codes:
      if region_code in RC.breast_reg_codes:
        BSF.set_up_beams_and_optimization_for_regional_breast(plan, beam_set, ROIS.ptv_c.name, region_code)
      else:
        BSF.set_up_beams_and_optimization_for_tangential_breast(plan, beam_set, plan.PlanOptimizations[0], target.replace("C", "P")+"c")
        # Configures the 2 Gy x 8 boost for breast patients, if indicated:
        if SSF.breast_boost_is_indicated(ss, region_code):
          BSF.set_up_beams_and_optimization_for_tangential_breast(plan, plan.BeamSets[1], plan.PlanOptimizations[1], ROIS.ptv_sbc.name)


    # Use the site optimizer for sites where it has been implemented:
    if site.optimizer:
      site.optimizer.optimize()
    else:
      # For legacy sites, use the old optimization procedure:
      # Run first optimization on each beam set:
      for plan_optimization in plan.PlanOptimizations:
        # Optimization parameters to be used on all cases (3D-CRT and VMAT):
        plan_optimization.OptimizationParameters.DoseCalculation.ComputeFinalDose = True
        # Configure optimization parameters for VMAT only:
        if "Arc" in plan_optimization.OptimizedBeamSets[0].DeliveryTechnique:
          optimization_parameters = OPT.optimization_parameters(region_code, prescription)
          optimization_parameters.apply_to(plan_optimization)
        # Run the optimization (may crash if GPU for computation is not available):
        # (Optimization may crash if e.g. GPU for computation is not available, or if max arc delivery time is too low for this target volume)
        # Assume we may have a beam delivery time error:
        possible_beam_delivery_time_error = True
        while possible_beam_delivery_time_error:
          try:
            plan_optimization.RunOptimization()
            # Optimization succeeded, thus there is no time error:
            possible_beam_delivery_time_error = False
          except Exception as e:
            if "is shorter than the minimum feasible time" in e.args[0]:
              # We need to increase the beam delivery time (and try the optimization again). Increase by 10 seconds:
              plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[0].ArcConversionPropertiesPerBeam.MaxArcDeliveryTime += 10
            else:
              # Although it did crash, it wasnt because of the time error:
              possible_beam_delivery_time_error = False
              GUIF.handle_optimization_error(plan_optimization, e)
      # Start adaptive optimization if indicated:
      if opt == 'oar':
        try:
          OBJF.adapt_optimization_oar(ss, plan, site.oar_objectives, region_code)
        except Exception as e:
          GUIF.handle_optimization_error(plan_optimization, e)
        if region_code in RC.breast_codes and technique_name != 'VMAT':
          # Modify leaves for the open fields in non-VMAT breast:
          if region_code in RC.breast_reg_codes:
            # Close leaves behind jaw for breast regional patients:
            BSF.close_leaves_behind_jaw_for_regional_breast(beam_set)
          # Create 2.5 cm margin to air for breast patient planned with a 3D-CRT technique (for robustness purpuses):
          BSF.create_margin_air_for_3dcrt_breast(ss, beam_set, region_code)
          # Compute dose:
          try:
            beam_set.ComputeDose(DoseAlgorithm = 'CCDose')
          except Exception as e:
            GUIF.handle_optimization_error(plan_optimization, e)
        # Auto scale to prescription:
        # In 12A it seems we cannot set the auto scale to prescription parameter:
        #for plan_optimization in plan.PlanOptimizations:
          #plan_optimization.AutoScaleToPrescription = True
    # Load plan:
    CF.load_plan(case, plan)


    # Save:
    patient.Save()
