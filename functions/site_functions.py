# encoding: utf8

# Import local files:
import clinical_goals
import objectives
import optimizers
import beam_functions as BF
import def_oars as OAR
import region_codes as RC
import rt_site as SITE
import rois as ROIS
import patient_model_functions as PMF
import structure_set_functions as SSF


# Example:
# SITE.Site(codes, oar_objectives, opt_objectives, oar_clinical_goals, target_clinical_goals)

# Set up regions:
# Brain:
def brain(pm, examination, ss, plan, prescription):
  obj = objectives.Brain(ss, plan, prescription, pm, examination)
  cg = clinical_goals.Brain(ss, plan, prescription)
  site = SITE.Site(RC.brain_codes, obj.oars, obj.targets, cg.oars, cg.targets)
  if prescription.region_code in RC.brain_whole_codes:
    site.optimizer = optimizers.General(ss, plan, site, prescription, adaptive_optimization=True)
  else:
    site.optimizer = optimizers.General(ss, plan, site, prescription)
  return site


# Lung:
def lung(ss, plan, prescription, target):
  obj = objectives.Lung(ss, plan, prescription)
  cg = clinical_goals.Lung(ss, plan, prescription)
  site = SITE.Site(RC.lung_codes, obj.oars, obj.targets, cg.oars, cg.targets)
  site.optimizer = optimizers.General(ss, plan, site, prescription)
  return site


# Breast:
def breast(ss, plan, prescription, target):
  obj = objectives.Breast(ss, plan, prescription)
  cg = clinical_goals.Breast(ss, plan, prescription)
  site = SITE.Site(RC.breast_codes, obj.oars, obj.targets, cg.oars, cg.targets)
  # Set up treat ROIs for bilateral cases:
  if prescription.region_code in RC.breast_bilateral_codes:
    BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[0], ROIS.ptv_c.name + '_R', 0.5)
    BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[1], ROIS.ptv_c.name + '_L', 0.5)
  site.optimizer = optimizers.Breast(ss, plan, site, prescription)
  return site


# Prostate:
def prostate(ss, plan, prescription, target):
  obj = objectives.Prostate(ss, plan, prescription)
  cg = clinical_goals.Prostate(ss, plan, prescription)
  site = SITE.Site(RC.prostate_codes, obj.oars, obj.targets, cg.oars, cg.targets)
  site.optimizer = optimizers.General(ss, plan, site, prescription)
  return site


# Rectum:
def rectum(ss, plan, prescription):
  obj = objectives.Rectum(ss, plan, prescription)
  cg = clinical_goals.Rectum(ss, plan, prescription)
  return SITE.Site(RC.rectum_codes, obj.oars, obj.targets, cg.oars, cg.targets)


# Palliative:
# Gives a treatment site (e.g. Pelvis) based on a specific region code (e.g. 314).
def palliative(ss, plan, prescription, target):
  obj = objectives.Other(ss, plan, prescription)
  cg = clinical_goals.Other(ss, plan, prescription)
  site = SITE.Site(RC.bone_codes, obj.oars, obj.targets, cg.oars, cg.targets)
  site.optimizer = optimizers.General(ss, plan, site, prescription, adaptive_optimization=True)
  return site


# Stereotactic bone/spine:
def bone_stereotactic(ss, plan, prescription):
  obj = objectives.OtherSBRT(ss, plan, prescription)
  cg = clinical_goals.OtherSBRT(ss, plan, prescription)
  site = SITE.Site(RC.bone_codes, obj.oars, obj.targets, cg.oars, cg.targets)
  site.optimizer = optimizers.General(ss, plan, site, prescription, adaptive_optimization=True)
  return site


# Bladder:
def bladder(ss, plan, prescription):
  obj = objectives.Bladder(ss, plan, prescription)
  cg = clinical_goals.Bladder(ss, plan, prescription)
  site.optimizer = optimizers.General(ss, plan, site, prescription, adaptive_optimization=True)
  return SITE.Site(RC.bladder_codes, obj.oars, obj.targets, cg.oars, cg.targets)


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
