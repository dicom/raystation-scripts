# encoding: utf8

# Import system libraries:
from __future__ import division
import math
from connect import *
import clr, sys

# Import local files:
import gui_functions as GUIF
import margins as MARGINS
import patient_model_functions as PMF
import rois as ROIS
import roi as ROI
import roi_functions as ROIF
import objective_functions as OF
import region_codes as RC
import structure_set_functions as SSF
import tolerance_doses as TOL
import prescription as PRES

# OAR objectives:
# Brain
brain_oar_objectives = []
brain_whole_oar_objectives = [ROIS.lens_l, ROIS.lens_r, ROIS.nasal_cavity]
brain_stereotactic_oar_objectives = []
# Breast
breast_tang_oar_objectives = [ROIS.lung_r, ROIS.lung_l]
breast_reg_l_oar_objectives = [ROIS.lung_r]
breast_reg_r_oar_objectives = [ROIS.lung_l]
breast_reg_oar_objectives = [ROIS.lung_l, ROIS.lung_r]
# Lung
lung_objectives = []
# Palliative
palliative_head_oar_objectives = [ROIS.spinal_canal_head, ROIS.eye_l, ROIS.eye_r]
palliative_neck_oar_objectives = [ROIS.spinal_canal_head, ROIS.parotids]
palliative_thorax_oar_objectives =  [ROIS.esophagus, ROIS.spinal_canal, ROIS.heart, ROIS.liver, ROIS.lungs]
palliative_thorax_and_abdomen_oar_objectives =  [ROIS.esophagus, ROIS.spinal_canal, ROIS.heart, ROIS.liver, ROIS.lungs, ROIS.kidneys, ROIS.bowel_space]
palliative_abdomen_oar_objectives =  [ROIS.spinal_canal, ROIS.kidneys, ROIS.liver, ROIS.bowel_space]
palliative_abdomen_and_pelvis_objectives = [ROIS.spinal_canal, ROIS.kidneys, ROIS.bowel_space, ROIS.bladder, ROIS.rectum]
palliative_pelvis_oar_objectives =  [ROIS.bowel_space, ROIS.bladder, ROIS.rectum, ROIS.cauda_equina]
palliative_other_oar_objectives =  []
palliative_prostate_oar_objectives = [ROIS.bowel_space, ROIS.bladder, ROIS.rectum]
# Bladder
bladder_objectives = [ROIS.bowel_space, ROIS.rectum]
# Prostate
prostate_objectives = []
prostate_bed_objectives = []
# Rectum
rectum_objectives = []


# Functions that creates objectives in the RayStation Plan Optimization module for various cases:


# Common objectives
def create_common_objectives(ss, plan, total_dose):
  OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 30)
  OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100*0.95, 150)
  OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.05, 80)
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)


# Breast boost (2 Gy x 8)
def create_breast_boost_objectives(ss, plan, region_code, total_dose):
  # External:
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30, beam_set_index = 1)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30, beam_set_index = 1)
  # Targets:
  # CTVsb:
  OF.uniform_dose(ss, plan, ROIS.ctv_sb.name, total_dose*100, 30, beam_set_index = 1)
  OF.min_dose(ss, plan, ROIS.ctv_sb.name, total_dose*100*0.95, 150, beam_set_index = 1)
  # PTVsbc:
  OF.min_dose(ss, plan, ROIS.ptv_sbc.name, total_dose*100*0.95, 75, beam_set_index = 1)
  OF.max_dose(ss, plan, ROIS.ptv_sbc.name, total_dose*100*1.05, 80, beam_set_index = 1)
  # OARs:
  # Side-neutral objectives:
  OF.max_eud(ss, plan, ROIS.heart.name, 0.5*100, 1, 3, beam_set_index = 1)
  # Side-dependent objectives:
  if region_code in RC.breast_l_codes:
    OF.max_eud(ss, plan, ROIS.lung_l.name, 6*100, 1, 2, beam_set_index = 1)
    OF.max_eud(ss, plan, ROIS.lung_r.name, 0.5*100, 1, 1, beam_set_index = 1)
    OF.max_eud(ss, plan, ROIS.breast_r.name, 1*100, 1, 1, beam_set_index = 1)
  elif region_code in RC.breast_r_codes:
    OF.max_eud(ss, plan, ROIS.lung_r.name, 6*100, 1, 2, beam_set_index = 1)
    OF.max_eud(ss, plan, ROIS.lung_l.name, 0.5*100, 1, 1, beam_set_index = 1)
    OF.max_eud(ss, plan, ROIS.breast_l.name, 1*100, 1, 1, beam_set_index = 1)
    OF.max_eud(ss, plan, ROIS.liver.name, 0.5*100, 1, 1, beam_set_index = 1)
  

# Whole breast objectives
def create_breast_objectives(ss, plan, region_code, total_dose, target):
  # External dose fall off:
  if region_code in RC.breast_partial_codes:
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
  else:
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 5.0, 30)
  # External max dose:
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)
  # Targets:
  if total_dose == 48:
    # SIB (48 & 40.05 Gy in 15 fx):
    whole_breast_dose = 40.05
    # Tumor bed:
    # CTVsb:
    OF.uniform_dose(ss, plan, ROIS.ctv_sb.name, total_dose*100, 30)
    OF.min_dose(ss, plan, ROIS.ctv_sb.name, total_dose*100*0.95, 150)
    # PTVsbc:
    OF.min_dose(ss, plan, ROIS.ptv_sbc.name, total_dose*100*0.95, 75)
    OF.max_dose(ss, plan, ROIS.ptv_sbc.name, total_dose*100*1.05, 80)
    # Whole breast:
    # CTV:
    OF.uniform_dose(ss, plan, ROIS.ctv_ptv_sbc.name, whole_breast_dose*100, 30)
    OF.min_dose(ss, plan, target, whole_breast_dose*100*0.95, 150)
    # PTVc:
    OF.min_dose(ss, plan, target.replace("C", "P")+"c", whole_breast_dose*100*0.95, 100)
    OF.max_dose(ss, plan, ROIS.ptv_c_ptv_sbc.name, whole_breast_dose*100*1.05, 80)
  else:
    # Ordinary WBRT:
    # CTV:
    OF.uniform_dose(ss, plan, target, total_dose*100, 30)
    OF.min_dose(ss, plan, target, total_dose*100*0.95, 150)
    # PTVc:
    OF.min_dose(ss, plan, target.replace("C", "P")+"c", total_dose*100*0.95, 100)
    OF.max_dose(ss, plan, target.replace("C", "P")+"c", total_dose*100*1.05, 80)
  # OARs:
  # Side-neutral objectives:
  OF.max_dvh(ss, plan, ROIS.a_lad.name, total_dose*0.5*100, 2, 2)
  OF.max_eud(ss, plan, ROIS.heart.name, 2*100, 1, 3)
  # Side-dependent objectives:
  if region_code in RC.breast_l_codes:
    OF.max_eud(ss, plan, ROIS.lung_l.name, 16*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.lung_l.name, total_dose*0.4*100, 15, 2)
    OF.max_eud(ss, plan, ROIS.lung_r.name, 1*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.breast_r.name, 3*100, 1, 1)
  elif region_code in RC.breast_r_codes:
    OF.max_eud(ss, plan, ROIS.lung_r.name, 16*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.lung_r.name, total_dose*0.4*100, 15, 2)
    OF.max_eud(ss, plan, ROIS.lung_l.name, 1*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.breast_l.name, 3*100, 1, 1)
    if not region_code in RC.breast_partial_codes:
      OF.max_eud(ss, plan, ROIS.liver.name, 2*100, 1, 1)


# Breast with regional lymph nodes
def create_breast_reg_objectives(ss, plan, region_code, total_dose):
  # External:
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 5.0, 30)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)
  # Targets:
  if total_dose == 48:
    # SIB (48 & 40.05 Gy in 15 fx):
    regional_dose = 40.05
    # Tumor bed:
    # CTVsb:
    OF.uniform_dose(ss, plan, ROIS.ctv_sb.name, total_dose*100, 30)
    OF.min_dose(ss, plan, ROIS.ctv_sb.name, total_dose*100*0.95, 150)
    # PTVsbc:
    OF.min_dose(ss, plan, ROIS.ptv_sbc.name, total_dose*100*0.95, 75)
    OF.max_dose(ss, plan, ROIS.ptv_sbc.name, total_dose*100*1.05, 80)
    # Regional breast:
    # CTV:
    OF.uniform_dose(ss, plan, ROIS.ctv_ptv_sbc.name, regional_dose*100, 30)
    # PTVc:
    OF.min_dose(ss, plan, ROIS.ptv_c.name, regional_dose*100*0.95, 100)
    OF.max_dose(ss, plan, ROIS.ptv_c_ptv_sbc.name, regional_dose*100*1.05, 80)
    # PTVpc:
    OF.min_dose(ss, plan, ROIS.ptv_pc.name, regional_dose*100*0.95, 100)
    OF.max_dose(ss, plan, ROIS.ptv_pc_ptv_sbc.name, regional_dose*100*1.05, 80)
  else:
    # Ordinary regional RT:
    # CTV:
    OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 30)
    OF.min_dose(ss, plan, ROIS.ctv.name, total_dose*100*0.95, 150)
    # PTVc:
    OF.min_dose(ss, plan, ROIS.ptv_c.name, total_dose*100*0.95, 100)
    OF.max_dose(ss, plan, ROIS.ptv_c.name, total_dose*100*1.05, 80)
    # PTVpc:
    OF.min_dose(ss, plan, ROIS.ptv_pc.name, total_dose*100*0.95, 100)
    OF.max_dose(ss, plan, ROIS.ptv_pc.name, total_dose*100*1.05, 80)
  # OARs:
  # Side-neutral objectives:
  OF.max_dvh(ss, plan, ROIS.a_lad.name, total_dose*0.5*100, 2, 2)
  OF.max_eud(ss, plan, ROIS.heart.name, 2*100, 1, 3)
  OF.max_eud(ss, plan, ROIS.thyroid.name, 8.7*100, 1, 1)
  OF.max_eud(ss, plan, ROIS.esophagus.name, 8.2*100, 1, 1)
  # Side-dependent objectives:
  if region_code in RC.breast_l_codes:
    OF.max_eud(ss, plan, ROIS.lung_l.name, 16*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.lung_l.name, total_dose*0.4*100, 35, 2)
    OF.max_eud(ss, plan, ROIS.lung_r.name, 1*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.breast_r.name, 3*100, 1, 1)
  elif region_code in RC.breast_r_codes:
    OF.max_eud(ss, plan, ROIS.lung_r.name, 16*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.lung_r.name, total_dose*0.4*100, 35, 2)
    OF.max_eud(ss, plan, ROIS.lung_l.name, 1*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.breast_l.name, 3*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.liver.name, 2*100, 1, 1)


# Palliative objectives
def create_palliative_objectives(ss, plan, total_dose, target):
  OF.uniform_dose(ss, plan, target, total_dose*100, 30)
  OF.min_dose(ss, plan, target.replace("C", "P"), total_dose*100*0.95, 150)
  OF.max_dose(ss, plan, target.replace("C", "P"), total_dose*100*1.05, 80)
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)
  OF.fall_off(ss, plan, ROIS.wall_ptv.name, total_dose*100, total_dose*0.75*100, 1.0, 2)


# Palliative beam sets in cases of multiple (additional) beam sets
def create_palliative_objectives_for_additional_beamsets(ss, plan, total_dose, beam_set_index):
  OF.uniform_dose(ss, plan, ROIS.ctv.name+str(beam_set_index+1), total_dose*100, 30, beam_set_index = beam_set_index)
  OF.min_dose(ss, plan, ROIS.ptv.name+str(beam_set_index+1), total_dose*100*0.95, 150, beam_set_index = beam_set_index)
  OF.max_dose(ss, plan, ROIS.ptv.name+str(beam_set_index+1), total_dose*100*1.05, 80, beam_set_index = beam_set_index)
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30, beam_set_index = beam_set_index)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30, beam_set_index = beam_set_index)
  OF.fall_off(ss, plan, ROIS.wall_ptv.name+str(beam_set_index+1), total_dose*100, total_dose*0.75*100, 1.0, 2, beam_set_index = beam_set_index)



# Whole brain
def create_whole_brain_objectives(ss, plan, total_dose):
  # Note that objectives for eye_l/r, lens_l/r and nasal_cavity are not specified here,
  # they are instead setup with adaptive optimization.
  OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 30)
  OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100*0.97, 150)
  OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.03, 80)
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)


# Partial brain (conventional or stereotactic)
def create_brain_objectives(pm, examination, ss, plan, prescription):
  assert type(prescription) is PRES.Prescription, "prescription is not a Prescription: %r" % prescription
  total_dose = prescription.total_dose
  nr_fractions = prescription.nr_fractions
  if prescription.is_stereotactic():
    # Stereotactic brain:
    nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
    for i in range(0, nr_targets):
      OF.max_eud(ss, plan, ROIS.brain_ptv.name, 0.08*total_dose*100, 1.3, 1, beam_set_index = i)
      OF.max_eud(ss, plan, ROIS.brain_ptv.name, 0.06*total_dose*100, 1, 1, beam_set_index = i)
      OF.fall_off(ss, plan, ROIS.body.name, total_dose*100, total_dose*100/2, 0.8, 25, beam_set_index = i)
    if nr_targets == 1:
      # Single target:
      OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100, 200, beam_set_index = 0)
      OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, total_dose*100, 0.7*total_dose*100, 0.6, 25, beam_set_index = 0)
    else:
      # Multiple targets:
      for i in range(0, nr_targets):
        OF.min_dose(ss, plan, ROIS.ptv.name+str(i+1), total_dose*100, 200, beam_set_index = i)
        OF.fall_off(ss, plan, "zPTV"+str(i+1)+"_Wall", total_dose*100, 0.7*total_dose*100, 0.6, 25, beam_set_index = i)
  else:
    # Conventional partial brain:
    OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.05, 80)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)
    # Objectives for prioritized OARs:
    OF.max_dose(ss, plan, ROIS.brainstem_surface.name, (TOL.brainstem_surface_v003_adx.equivalent(nr_fractions)*100)-50, 60)
    OF.max_dose(ss, plan, ROIS.brainstem_core.name, (TOL.brainstem_core_v003_adx.equivalent(nr_fractions)*100)-50, 80)
    OF.max_dose(ss, plan, ROIS.optic_chiasm.name, (TOL.optic_chiasm_v003_adx.equivalent(nr_fractions)*100)-50, 40)
    OF.max_dose(ss, plan, ROIS.optic_nrv_l.name, (TOL.optic_nrv_v003_adx.equivalent(nr_fractions)*100)-50, 20)
    OF.max_dose(ss, plan, ROIS.optic_nrv_r.name, (TOL.optic_nrv_v003_adx.equivalent(nr_fractions)*100)-50, 20)
    prioritized_oars = [ROIS.brainstem_core, ROIS.brainstem_surface, ROIS.optic_chiasm, ROIS.optic_nrv_l, ROIS.optic_nrv_r]
    tolerances = [TOL.brainstem_core_v003_adx, TOL.brainstem_surface_v003_adx, TOL.optic_chiasm_v003_adx, TOL.optic_nrv_v003_adx, TOL.optic_nrv_v003_adx]
    conflict_oars = []
    for i in range(len(prioritized_oars)):
      if tolerances[i].equivalent(nr_fractions) < total_dose*0.95:
        conflict_oars.append(prioritized_oars[i])
    # Setup of min and uniform doses depends on presence of critical overlaps or not:
    if len(conflict_oars) > 0:
      # Create subtraction and intersect ROIs for planning of conflicting sites:
      ctv_oars = ROI.ROIAlgebra(ROIS.ctv_oars.name, ROIS.ctv_oars.type, ROIS.ctv.color, sourcesA = [ROIS.ctv], sourcesB = conflict_oars, operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_2mm_expansion)
      ptv_oars = ROI.ROIAlgebra(ROIS.ptv_oars.name, ROIS.ptv_oars.type, ROIS.ptv.color, sourcesA = [ROIS.ptv], sourcesB = conflict_oars, operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_2mm_expansion)
      ptv_and_oars = ROI.ROIAlgebra(ROIS.ptv_and_oars.name, ROIS.ptv_and_oars.type, ROIS.other_ptv.color, sourcesA = [ROIS.ptv], sourcesB = conflict_oars, operator='Intersection')
      rois = [ctv_oars, ptv_oars, ptv_and_oars]
      PMF.delete_matching_rois(pm, rois)
      for i in range(len(rois)):
        PMF.create_algebra_roi(pm, examination, ss, rois[i])
        PMF.exclude_roi_from_export(pm, rois[i].name)
      # Create objectives for the subtraction/intersect ROIs:
      OF.uniform_dose(ss, plan, ROIS.ptv_and_oars.name, (tolerances[0].equivalent(nr_fractions)*100-50), 5) # (Note that this assumes our OARs have the same tolerance dose...)
      OF.uniform_dose(ss, plan, ROIS.ctv_oars.name, total_dose*100, 30)
      OF.min_dose(ss, plan, ROIS.ptv_oars.name, total_dose*100*0.95, 150)
    else:
      OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 30)
      OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100*0.95, 150)
    # Setup of objectives for less prioritized OARs:
    other_oars = [ROIS.cochlea_l, ROIS.cochlea_r, ROIS.hippocampus_l, ROIS.hippocampus_r, ROIS.lens_l, ROIS.lens_r, ROIS.lacrimal_l, ROIS.lacrimal_r, ROIS.retina_l, ROIS.retina_r, ROIS.cornea_r, ROIS.cornea_l, ROIS.pituitary]
    tolerances = [TOL.cochlea_mean_tinnitus, TOL.cochlea_mean_tinnitus, TOL.hippocampus_v40, TOL.hippocampus_v40, TOL.lens_v003_adx, TOL.lens_v003_adx, TOL.lacrimal_mean, TOL.lacrimal_mean, TOL.retina_v003_adx, TOL.retina_v003_adx, TOL.cornea_v003_adx, TOL.cornea_v003_adx, TOL.pituitary_mean]
    for i in range(len(other_oars)):
      if SSF.has_named_roi_with_contours(ss, other_oars[i].name):
        weight = None
        # Conflict with dose?
        if tolerances[i].equivalent(nr_fractions) < total_dose*0.95:
          # Conflict with dose:
          if not SSF.roi_overlap(pm, examination, ss, ROIS.ptv, other_oars[i], 2):
            if ROIF.roi_vicinity_approximate(SSF.rg(ss, ROIS.ptv.name), SSF.rg(ss, other_oars[i].name), 2):
              # OAR is close, but not overlapping:
              weight = 2
            else:
              weight = 20
        else:
          # No conflict with dose:
          weight = 20
        # Create objective if indicated:
        if weight:
          if other_oars[i].name in  [ROIS.cochlea_r.name, ROIS.cochlea_l.name, ROIS.lacrimal_l.name, ROIS.lacrimal_r.name, ROIS.hippocampus_l.name, ROIS.hippocampus_r.name, ROIS.pituitary.name]:
            OF.max_eud(ss, plan, other_oars[i].name, tolerances[i].equivalent(nr_fractions)*100-50, 1, weight)
          else:
            OF.max_dose(ss, plan, other_oars[i].name, (tolerances[i].equivalent(nr_fractions)*100)-50, weight)
      else:
        GUIF.handle_missing_roi_for_objective(other_oars[i].name)


# Lung (conventional)
def create_lung_objectives(ss, plan, target, total_dose):
  if total_dose > 40:
    # Curative fractionation:
    OF.uniform_dose(ss, plan, target, total_dose*100, 25)
    OF.max_dose(ss, plan, target, total_dose*100*1.05, 5)
    OF.min_dvh(ss, plan, target, total_dose*0.95*100, 98, 100)
    OF.min_dvh(ss, plan, ROIS.ptv.name, total_dose*0.95*100, 95, 80)
    OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.05, 50)
    OF.max_eud(ss, plan, ROIS.esophagus.name, 0.51*total_dose*100, 1, 1) # (~34 Gy for 66 Gy total dose)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 80)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 3, 2)
    OF.max_eud(ss, plan, ROIS.heart.name, 0.53*total_dose*100, 1, 10) # (~35 Gy for 66 Gy total dose)
    OF.max_eud(ss, plan, ROIS.spinal_canal.name, 0.6818*total_dose*100, 1, 10) # (~45 Gy for 66 Gy total dose)
    match = False
    if SSF.has_roi_with_shape(ss, ROIS.lungs_gtv.name):
      l = ROIS.lungs_gtv.name
    elif SSF.has_roi_with_shape(ss, ROIS.lungs_igtv.name):
      l = ROIS.lungs_igtv.name
    else:
      l = ROIS.lungs.name
    OF.max_eud(ss, plan, l, 0.29*total_dose*100, 1, 15) # (~19 Gy for 66 Gy total dose)
    OF.max_dvh(ss, plan, l, total_dose*0.07575*100, 55, 70) # (~5 Gy for 66 Gy total dose)
    OF.max_dvh(ss, plan, l, total_dose*0.3030*100, 30, 80) # (~5 Gy for 66 Gy total dose)
  elif total_dose < 40:
    # Palliative fractionation:
    OF.uniform_dose(ss, plan, target, total_dose*100, 35)
    OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.05, 120)
    OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100*0.95, 150)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 80)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 3, 2)
    OF.max_eud(ss, plan, ROIS.heart.name, 0.29*total_dose*100, 1, 10)
    OF.max_eud(ss, plan, ROIS.lungs.name, 0.23*total_dose*100, 1, 15)
    OF.max_eud(ss, plan, ROIS.spinal_canal.name, 0.9*total_dose*100, 1, 5)


# Lung (SBRT)
def create_lung_stereotactic_objectives(ss, plan, region_code, total_dose):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  for i in range(0, nr_targets):
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 3, 5, beam_set_index = i)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*130, 15, beam_set_index = i)
    OF.max_dose(ss, plan, ROIS.skin.name, 30*100, 10, beam_set_index = i)
    OF.max_dose(ss, plan, ROIS.spinal_canal.name, 13*100, 5, beam_set_index = i)
    OF.max_dvh(ss, plan, ROIS.chestwall.name, 30*100, 2, 100, beam_set_index = i)
    OF.max_eud(ss, plan, ROIS.lungs.name, 4.5*100, 1, 1, beam_set_index = i)
    if region_code in RC.lung_r_codes:
      OF.max_eud(ss, plan, ROIS.lung_r.name, 6.5*100, 1, 3, beam_set_index = i)
      OF.max_dose(ss, plan, ROIS.ribs_r.name, total_dose*120, 10, beam_set_index = i)
    else:
      OF.max_eud(ss, plan, ROIS.lung_l.name, 6.5*100, 1, 3, beam_set_index = i)
      OF.max_dose(ss, plan, ROIS.ribs_l.name, total_dose*120, 10, beam_set_index = i)
  if nr_targets == 1:
    OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100, 250)
    OF.fall_off(ss, plan, ROIS.wall_ptv.name, total_dose*100, 0.7*total_dose*100, 0.8, 5)
  else:
    for i in range(0, nr_targets):
      OF.min_dose(ss, plan, ROIS.ptv.name+str(i+1), total_dose*100, 250, beam_set_index = i)
      OF.fall_off(ss, plan, "zPTV"+str(i+1)+"_Wall", total_dose*100, 0.7*total_dose*100, 0.8, 5, beam_set_index = i)


# Prostate
def create_prostate_objectives(ss, plan, total_dose):
  if total_dose == 60:
    # Hypofractionated prosate only:
    OF.uniform_dose(ss, plan, ROIS.ctv_60.name, total_dose*100, 40)
    OF.uniform_dose(ss, plan, ROIS.ctv_57.name, total_dose*0.95*100, 40)
    OF.min_dose(ss, plan, ROIS.ptv_60.name, 57.1*100, 150)
    OF.min_dose(ss, plan, ROIS.ptv_57.name, total_dose*100*0.91, 170)
    OF.min_dose(ss, plan, ROIS.ctv_57.name, total_dose*100*0.93, 35)
    OF.max_dose(ss, plan, ROIS.ptv_60.name, total_dose*100*1.02, 60)
    OF.max_dvh(ss, plan, ROIS.ptv_57.name, total_dose*0.978*100, 1, 50)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.038, 25)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 20*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 20*100, 2, 1)
    OF.max_eud(ss, plan, ROIS.rectum.name, 22.6*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.rectum.name, total_dose*0.975*100, 3, 4)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 24*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 18*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 28*100, 3, 1)
    OF.max_dvh(ss, plan, ROIS.z_rectum.name, 51*100, 1, 10)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 12.4*100, 1, 1)
    OF.fall_off(ss, plan, ROIS.z_ptv_60_wall.name, total_dose*100, 57*100, 0.3, 1)
    OF.fall_off(ss, plan, ROIS.z_ptv_57_60_wall.name, total_dose*100, 42*100, 0.8, 12)
  elif total_dose == 55:
    # Hypofractionated local control (STAMPEDE):
    OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 40)
    OF.min_dose(ss, plan, ROIS.ptv.name, 52.3*100, 150)
    OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.02, 60)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.038, 25)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 20*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 20*100, 2, 1)
    OF.max_eud(ss, plan, ROIS.rectum.name, 22.6*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.rectum.name, total_dose*0.975*100, 3, 4)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 22*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 18*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 28*100, 3, 1)
    OF.max_dvh(ss, plan, ROIS.z_rectum.name, 51*100, 1, 10)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 12.4*100, 1, 1)
    OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, total_dose*100, 42*100, 1, 1)
  elif total_dose == 77 and SSF.has_roi_with_shape(ss, ROIS.ptv_56.name):
    # Normo-fractionated with elective nodes:
    OF.uniform_dose(ss, plan, ROIS.ctv_56.name, 56*100, 15)
    OF.uniform_dose(ss, plan, ROIS.ctv_70_sib.name, 70*100, 25)
    OF.uniform_dose(ss, plan, ROIS.ctv_77.name, 77*100, 20)
    OF.min_dose(ss, plan, ROIS.ptv_56.name, 54*100, 100)
    OF.max_dvh(ss, plan, ROIS.ptv_56.name, 58.5*100, 5, 5)
    OF.min_dose(ss, plan, ROIS.ptv_70_sib.name, total_dose*100*0.88, 100)
    OF.max_dvh(ss, plan, ROIS.ptv_70_sib.name, total_dose*0.95*100, 5, 50)
    OF.min_dose(ss, plan, ROIS.ptv_77.name, total_dose*100*0.98, 100)
    OF.max_dose(ss, plan, ROIS.ptv_77.name, total_dose*100*1.02, 70)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 20)
    OF.fall_off(ss, plan, ROIS.external.name, 56*100, 28*100, 2, 15)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.rectum.name, 72.5*100, 5, 10)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 31*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 34*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_spc_bowel.name, 14.2*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 45*100, 2, 2)
    OF.fall_off(ss, plan, ROIS.z_ptv_77_wall.name, total_dose*100, 71*100, 0.3, 10)
    OF.fall_off(ss, plan, ROIS.z_ptv_70_77_wall.name, total_dose*100, 56*100, 0.5, 5)
  elif total_dose == 77:
    # Normo-fractionated prostate only:
    OF.uniform_dose(ss, plan, ROIS.ctv_77.name, total_dose*100, 40)
    OF.uniform_dose(ss, plan, ROIS.ctv_70_sib.name, 70*100, 40)
    OF.min_dose(ss, plan, ROIS.ctv_70_sib.name, total_dose*100*0.89, 25)
    OF.min_dose(ss, plan, ROIS.ptv_77.name, total_dose*100*0.98, 150)
    OF.min_dvh(ss, plan, ROIS.ptv_70_sib.name, total_dose*100*0.89, 98, 150)
    OF.max_dose(ss, plan, ROIS.ptv_77.name, total_dose*100*1.02, 70)
    OF.max_dose(ss, plan, ROIS.ptv_70_sib.name, total_dose*0.95*100, 50)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.038, 25)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 35*100, 2, 1)
    OF.max_eud(ss, plan, ROIS.rectum.name, 40*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.rectum.name, 72.4*100, 5, 15)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 36.5*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.z_rectum.name, 60*100, 3, 10)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 29.5*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 30*100, 5, 1)
    OF.max_dvh(ss, plan, ROIS.z_rectum.name, 51*100, 1, 10)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 25*100, 1, 3)
    OF.fall_off(ss, plan, ROIS.z_ptv_77_wall.name, total_dose*100, 68*100, 0.3, 15)
  elif total_dose == 67.5 and SSF.has_roi_with_shape(ss, ROIS.ptv__50.name):
    # Hypo-fractionated prostate prostate with elective nodes:
    OF.uniform_dose(ss, plan, 'CTV!_50', 50*100, 15)
    OF.uniform_dose(ss, plan, 'CTV!_62.5', 62.5*100, 25)
    OF.uniform_dose(ss, plan, 'CTV_67.5', 67.5*100, 20)
    OF.min_dose(ss, plan, 'PTV!_50', 48*100, 100)
    OF.max_dvh(ss, plan, 'PTV!_50', 52*100, 5, 5)
    OF.min_dose(ss, plan, 'PTV!_62.5', total_dose*100*0.88, 100)
    OF.max_dvh(ss, plan, 'PTV!_62.5', total_dose*0.95*100, 5, 50)
    OF.min_dose(ss, plan, 'PTV_67.5', total_dose*100*0.98, 100)
    OF.max_dose(ss, plan, 'PTV_67.5', total_dose*100*1.02, 70)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 20)
    OF.fall_off(ss, plan, ROIS.external.name, 50*100, 25*100, 2, 15)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 30*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 30*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.rectum.name, 65*100, 5, 10)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 32*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 28*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 30*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_spc_bowel.name, 12*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 40*100, 2, 2)
    OF.fall_off(ss, plan, 'zPTV_67.5_Wall', total_dose*100, 62*100, 0.3, 10)
    OF.fall_off(ss, plan, 'zPTV_62.5+67.5_Wall', total_dose*100, 50*100, 0.5, 5)
  elif total_dose == 67.5:
    # Hypo-fractionated prostate prostate only:
    OF.uniform_dose(ss, plan, 'CTV!_62.5', 62.5*100, 25)
    OF.uniform_dose(ss, plan, 'CTV_67.5', 67.5*100, 20)
    OF.min_dose(ss, plan, 'PTV!_62.5', total_dose*100*0.88, 100)
    OF.max_dvh(ss, plan, 'PTV!_62.5', total_dose*0.95*100, 5, 50)
    OF.min_dose(ss, plan, 'PTV_67.5', total_dose*100*0.98, 100)
    OF.max_dose(ss, plan, 'PTV_67.5', total_dose*100*1.02, 70)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 20)
    OF.fall_off(ss, plan, ROIS.external.name, 50*100, 25*100, 2, 15)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 30*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 30*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.rectum.name, 65*100, 5, 10)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 32*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 28*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 30*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 40*100, 2, 2)
    OF.fall_off(ss, plan, 'zPTV_67.5_Wall', total_dose*100, 62*100, 0.3, 10)


# Prostate bed
def create_prostate_bed_objectives(ss, plan, total_dose):
  if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name):
    # Elective nodes:
    OF.uniform_dose(ss, plan, ROIS.ctv_70.name, total_dose*100, 20)
    OF.uniform_dose(ss, plan, ROIS.ctv_56.name, 56*100, 20)
    OF.min_dose(ss, plan, ROIS.ptv_70.name, 67*100, 150)
    OF.min_dose(ss, plan, ROIS.ptv_56.name, 54*100, 150)
    OF.max_dose(ss, plan, ROIS.ptv_70.name, total_dose*100*1.045, 70)
    OF.fall_off(ss, plan, ROIS.external.name, 70*100, 35*100, 3, 15)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 20)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.rectum.name, 72.5*100, 5, 10)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 40*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 35*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 44*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.z_spc_bowel.name, 28*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 45*100, 2, 2)
    OF.fall_off(ss, plan, ROIS.z_ptv_70_wall.name, total_dose*100, 56*100, 1, 1)
    OF.fall_off(ss, plan, ROIS.z_ptv_56_wall.name, 56*100, 42*100, 1, 1)
  else:
    # Prostate bed only:
    OF.uniform_dose(ss, plan, ROIS.ctv_70.name, total_dose*100, 25)
    OF.min_dose(ss, plan, ROIS.ptv_70.name, total_dose*100*0.96, 100)
    OF.max_dose(ss, plan, ROIS.ptv_70.name, total_dose*100*1.03, 50)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 2, 20)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 40)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 35*100, 2, 1)
    OF.max_eud(ss, plan, ROIS.rectum.name, 40*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.anal_canal.name, 40*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.z_rectum.name, 60*100, 3, 10)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 29.5*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_rectum.name, 30*100, 5, 1)
    OF.max_dvh(ss, plan, ROIS.z_rectum.name, 51*100, 1, 10)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 25*100, 1, 3)


# Bladder
def create_bladder_objectives(plan, ss, total_dose):
  OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 30)
  OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100*0.95, 150)
  OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.05, 80)
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.5, 30)
  OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 30)
  OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 45*100, 2, 1)
  OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 45*100, 2, 1)


# Rectum
def create_rectum_objectives(ss, plan, total_dose):
  if total_dose == 50:
    OF.uniform_dose(ss, plan, ROIS.ctv_50.name, total_dose*100, 20)
    OF.uniform_dose(ss, plan, ROIS.ctv_47.name, 47*100, 35)
    OF.min_dose(ss, plan, ROIS.ptv_47_50.name, 44.8*100, 200)
    OF.min_dose(ss, plan, ROIS.ptv_50.name, total_dose*0.95*100, 150)
    OF.max_dvh(ss, plan, ROIS.ptv_47.name, total_dose*0.95*100, 3, 20)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 2, 10)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 20)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 35*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 35*100, 2, 1)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 28*100, 1, 2)
    OF.max_eud(ss, plan, ROIS.bowel_space.name, 20*100, 1, 5)
    OF.max_dvh(ss, plan, ROIS.z_spc_bowel.name, 44*100, 2, 2)
    OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 45*100, 2, 2)
    OF.fall_off(ss, plan, ROIS.z_ptv_50_wall.name, 49*100, 45*100, 0.5, 5)
    OF.fall_off(ss, plan, ROIS.z_ptv_47_50_wall.name, 50*100, 35*100, 1.0, 1)
  else:
    OF.uniform_dose(ss, plan, ROIS.ctv.name, total_dose*100, 35)
    OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100*0.95, 150)
    OF.max_dose(ss, plan, ROIS.ptv.name, total_dose*100*1.05, 50)
    OF.fall_off(ss, plan, ROIS.external.name, total_dose*100, total_dose*100/2, 1.8, 15)
    OF.max_dose(ss, plan, ROIS.external.name, total_dose*100*1.05, 20)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 18*100, 2, 1)
    OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 18*100, 2, 1)
    OF.max_eud(ss, plan, ROIS.z_bladder.name, 16.2*100, 1, 1)
    OF.max_eud(ss, plan, ROIS.z_spc_bowel.name, 14*100, 1, 2)
    OF.max_dvh(ss, plan, ROIS.z_spc_bowel.name, 22*100, 2, 2)
    OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 23*100, 2, 2)


# Bone/Spine SBRT
def create_bone_stereotactic_objectives(ss, plan, total_dose):
  OF.min_dose(ss, plan, ROIS.ptv.name, total_dose*100, 200)
  OF.fall_off(ss, plan, ROIS.external.name, total_dose*106, 3*100, 3, 3)
  OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, total_dose*100, 0.65*total_dose*100, 0.5, 10)
