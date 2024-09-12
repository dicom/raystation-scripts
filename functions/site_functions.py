# encoding: utf8

# Import local files:
import objectives
import beam_functions as BF
import def_oars as OAR
import region_codes as RC
import clinical_goals as CGS
import rt_site as SITE
import rois as ROIS
import patient_model_functions as PMF
import structure_set_functions as SSF

import breast_optimization as OPT

# Example:
# SITE.Site(codes, oar_objectives, opt_objectives, oar_clinical_goals, target_clinical_goals)

# Set up regions:
# Brain:
def brain(pm, examination, ss, plan, prescription):
  obj = objectives.Brain(ss, plan, prescription, pm, examination)
  if prescription.region_code in RC.brain_whole_codes:
    site = SITE.Site(RC.brain_codes, obj.oars, obj.targets, CGS.brain_oars(prescription), CGS.brain_targets(ss, prescription))
  else:
    site = SITE.Site(RC.brain_codes, obj.oars, obj.targets, CGS.brain_oars(prescription), CGS.brain_targets(ss, prescription))
  return site


# Lung:
def lung(ss, plan, prescription, target):
  obj = objectives.Lung(ss, plan, prescription)
  if prescription.is_stereotactic() and prescription.nr_fractions == 3:
    site = SITE.Site(RC.lung_codes, obj.oars, obj.targets, CGS.lung_stereotactic_3fx_oars(prescription), CGS.lung_stereotactic_targets(ss))
  elif prescription.is_stereotactic() and prescription.nr_fractions == 5:
    site = SITE.Site(RC.lung_codes, obj.oars, obj.targets, CGS.lung_stereotactic_5fx_oars(prescription), CGS.lung_stereotactic_targets(ss))
  elif prescription.is_stereotactic() and prescription.nr_fractions == 8:
    site = SITE.Site(RC.lung_codes, obj.oars, obj.targets, CGS.lung_stereotactic_8fx_oars(prescription), CGS.lung_stereotactic_targets(ss))
  else:
    site = SITE.Site(RC.lung_codes, obj.oars, obj.targets, CGS.lung_oars(ss, prescription), CGS.lung_targets(ss))
  return site


# Breast:
def breast(ss, plan, prescription, target):
  obj = objectives.Breast(ss, plan, prescription)
  if prescription.region_code in RC.breast_reg_codes:
    site = SITE.Site(RC.breast_reg_codes, obj.oars, obj.targets, CGS.breast_oars(ss, prescription), CGS.breast_targets(ss, target, prescription))
    # Set up treat ROIs for bilateral cases:
    if prescription.region_code in RC.breast_bilateral_codes:
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[0], ROIS.ptv_c.name + '_R', 0.5)
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[1], ROIS.ptv_c.name + '_L', 0.5)
    site.optimizer = OPT.BreastOptimization(ss, plan, site, prescription)
  else:
    site = SITE.Site(RC.breast_whole_codes, obj.oars, obj.targets, CGS.breast_oars(ss, prescription), CGS.breast_targets(ss, target, prescription))
    # Set up treat ROIs for bilateral cases:
    if prescription.region_code in RC.breast_bilateral_codes:
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[0], ROIS.ptv_c.name + '_R', 0.5)
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[1], ROIS.ptv_c.name + '_L', 0.5)
    site.optimizer = OPT.BreastOptimization(ss, plan, site, prescription)
  return site


# Prostate:
def prostate(ss, plan, prescription, target):
  obj = objectives.Prostate(ss, plan, prescription)
  if prescription.total_dose < 40:
    site = SITE.Site(RC.prostate_codes, obj.oars, obj.targets, CGS.prostate_oars(ss, prescription), CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.prostate_bed_codes:
    site = SITE.Site(RC.prostate_bed_codes, obj.oars, obj.targets, CGS.prostate_oars(ss, prescription), CGS.prostate_bed_targets(ss))
  else:
    site = SITE.Site(RC.prostate_codes, obj.oars, obj.targets, CGS.prostate_oars(ss, prescription), CGS.prostate_targets(ss, prescription))
  return site


# Rectum:
def rectum(ss, plan, prescription):
  obj = objectives.Rectum(ss, plan, prescription)
  return SITE.Site(RC.rectum_codes, obj.oars, obj.targets, CGS.rectum_oars, CGS.rectum_targets(prescription))


# Palliative:
# Gives a treatment site (e.g. Pelvis) based on a specific region code (e.g. 314).
def palliative(ss, plan, prescription, target):
  obj = objectives.Other(ss, plan, prescription)
  if prescription.region_code in RC.palliative_head_codes:
    site = SITE.Site(RC.palliative_head_codes, obj.oars, obj.targets, CGS.head, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_neck_codes:
    site = SITE.Site(RC.palliative_neck_codes, obj.oars, obj.targets, CGS.neck, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_thorax_codes:
    site = SITE.Site(RC.palliative_thorax_codes, obj.oars, obj.targets, CGS.thorax, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_thorax_and_abdomen_codes:
    site = SITE.Site(RC.palliative_thorax_and_abdomen_codes, obj.oars, obj.targets, CGS.thorax_and_abdomen, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_abdomen_codes:
    site = SITE.Site(RC.palliative_abdomen_codes, obj.oars, obj.targets, CGS.abdomen, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_abdomen_and_pelvis_codes:
    site = SITE.Site(RC.palliative_abdomen_and_pelvis_codes, obj.oars, obj.targets, CGS.abdomen_and_pelvis, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_pelvis_codes:
    site = SITE.Site(RC.palliative_pelvis_codes, obj.oars, obj.targets, CGS.pelvis, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_other_codes:
    site = SITE.Site(RC.palliative_other_codes, obj.oars, obj.targets, CGS.other, CGS.palliative_targets(ss, plan, target))
  return site


# Stereotactic bone/spine:
def bone_stereotactic(ss, plan, prescription):
  obj = objectives.OtherSBRT(ss, plan, prescription)
  if prescription.nr_fractions == 1:
    site = SITE.Site(RC.bone_codes, obj.oars, obj.targets, CGS.bone_stereotactic_1fx_oars(prescription), CGS.bone_stereotactic_targets)
  else:
    site = SITE.Site(RC.bone_codes, obj.oars, obj.targets, CGS.bone_stereotactic_3fx_oars(prescription), CGS.bone_stereotactic_targets)
  return site


# Bladder:
def bladder(ss, plan, prescription):
  obj = objectives.Bladder(ss, plan, prescription)
  return SITE.Site(RC.bladder_codes, obj.oars, obj.targets, CGS.bladder_oars, CGS.targets)


# Determines the site from the region code.
def site(pm, examination, ss, plan, prescription, target, technique_name):
  if prescription.region_code in RC.brain_codes:
    # Brain:
    if prescription.region_code not in RC.brain_whole_codes:
      if prescription.nr_fractions > 5:
        PMF.create_retina_and_cornea(pm, examination, ss, ROIS.lens_l, ROIS.box_l, ROIS.eye_l, ROIS.retina_l, ROIS.cornea_l)
        PMF.create_retina_and_cornea(pm, examination, ss, ROIS.lens_r, ROIS.box_r, ROIS.eye_r, ROIS.retina_r, ROIS.cornea_r)
    site = brain(pm, examination, ss, plan, prescription)
  elif prescription.region_code in RC.breast_codes:
    # Breast:
    site = breast(ss, plan, prescription, target)
  elif prescription.region_code in RC.lung_and_mediastinum_codes:
    # Lung:
    site = lung(ss, plan, prescription, target)
  elif prescription.region_code in RC.prostate_codes:
    # Prostate:
    site = prostate(ss, plan, prescription, target)
  elif prescription.region_code in RC.rectum_codes:
    # Rectum:
    site = rectum(ss, plan, prescription)
  elif prescription.region_code in RC.bladder_codes:
    # Bladder:
    site = bladder(ss, plan, prescription)
  elif prescription.region_code in RC.palliative_codes:
    # Palliative:
    if prescription.is_stereotactic():
      site = bone_stereotactic(ss, plan, prescription)
    else:
      site = palliative(ss, plan, prescription, target)
  return site
