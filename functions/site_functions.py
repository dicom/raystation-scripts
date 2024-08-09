# encoding: utf8

# Import local files:
import beam_functions as BF
import def_oars as OAR
import region_codes as RC
import clinical_goals as CGS
import objectives as OBJ
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
  if prescription.region_code in RC.brain_whole_codes:
    site = SITE.Site(RC.brain_codes, OBJ.brain_whole_oar_objectives, OBJ.create_whole_brain_objectives(ss, plan, prescription), CGS.brain_oars(prescription), CGS.brain_targets(ss, prescription))
  else:
    site = SITE.Site(RC.brain_codes, OBJ.brain_oar_objectives, OBJ.create_brain_objectives(pm, examination, ss, plan, prescription), CGS.brain_oars(prescription), CGS.brain_targets(ss, prescription))
  return site


# Lung:
def lung(ss, plan, prescription, target):
  if prescription.is_stereotactic() and prescription.nr_fractions == 3:
    site = SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_stereotactic_objectives(ss, plan, prescription), CGS.lung_stereotactic_3fx_oars(prescription), CGS.lung_stereotactic_targets(ss))
  elif prescription.is_stereotactic() and prescription.nr_fractions == 5:
    site = SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_stereotactic_objectives(ss, plan, prescription), CGS.lung_stereotactic_5fx_oars(prescription), CGS.lung_stereotactic_targets(ss))
  elif prescription.is_stereotactic() and prescription.nr_fractions == 8:
    site = SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_stereotactic_objectives(ss, plan, prescription), CGS.lung_stereotactic_8fx_oars(prescription), CGS.lung_stereotactic_targets(ss))
  else:
    site = SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_objectives(ss, plan, target, prescription), CGS.lung_oars(ss, prescription), CGS.lung_targets(ss))
  return site


# Breast:
def breast(ss, plan, prescription, target):
  if prescription.region_code in RC.breast_reg_codes:
    site = SITE.Site(RC.breast_reg_codes, OBJ.breast_reg_oar_objectives, OBJ.create_breast_reg_objectives(ss, plan, prescription), CGS.breast_oars(ss, prescription), CGS.breast_targets(ss, target, prescription))
    # Set up treat ROIs for bilateral cases:
    if prescription.region_code in RC.breast_bilateral_codes:
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[0], ROIS.ptv_c.name + '_R', 0.5)
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[1], ROIS.ptv_c.name + '_L', 0.5)
    site.optimizer = OPT.BreastOptimization(ss, plan, site, prescription)
  else:
    site = SITE.Site(RC.breast_whole_codes, OBJ.breast_tang_oar_objectives, OBJ.create_breast_objectives(ss, plan, prescription, target), CGS.breast_oars(ss, prescription), CGS.breast_targets(ss, target, prescription))
    # Set up treat ROIs for bilateral cases:
    if prescription.region_code in RC.breast_bilateral_codes:
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[0], ROIS.ptv_c.name + '_R', 0.5)
      BF.set_up_treat_or_protect(plan.BeamSets[0].Beams[1], ROIS.ptv_c.name + '_L', 0.5)
    site.optimizer = OPT.BreastOptimization(ss, plan, site, prescription)
  return site


# Prostate:
def prostate(ss, plan, prescription, target):
  if prescription.total_dose < 40:
    site = SITE.Site(RC.prostate_codes, OBJ.palliative_prostate_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.prostate_oars(ss, prescription), CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.prostate_bed_codes:
    site = SITE.Site(RC.prostate_bed_codes, OBJ.prostate_objectives, OBJ.create_prostate_bed_objectives(ss, plan, prescription), CGS.prostate_oars(ss, prescription), CGS.prostate_bed_targets(ss))
  else:
    site = SITE.Site(RC.prostate_codes, OBJ.prostate_objectives, OBJ.create_prostate_objectives(ss, plan, prescription), CGS.prostate_oars(ss, prescription), CGS.prostate_targets(ss, prescription))
  return site


# Rectum:
def rectum(ss, plan, prescription):
  return SITE.Site(RC.rectum_codes, OBJ.rectum_objectives, OBJ.create_rectum_objectives(ss, plan, prescription), CGS.rectum_oars, CGS.rectum_targets(prescription))


# Palliative:
# Gives a treatment site (e.g. Pelvis) based on a specific region code (e.g. 314).
def palliative(ss, plan, prescription, target):
  if prescription.region_code in RC.palliative_head_codes:
    site = SITE.Site(RC.palliative_head_codes, OBJ.palliative_head_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.head, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_neck_codes:
    site = SITE.Site(RC.palliative_neck_codes, OBJ.palliative_neck_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.neck, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_thorax_codes:
    site = SITE.Site(RC.palliative_thorax_codes, OBJ.palliative_thorax_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.thorax, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_thorax_and_abdomen_codes:
    site = SITE.Site(RC.palliative_thorax_and_abdomen_codes, OBJ.palliative_thorax_and_abdomen_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.thorax_and_abdomen, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_abdomen_codes:
    site = SITE.Site(RC.palliative_abdomen_codes, OBJ.palliative_abdomen_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.abdomen, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_abdomen_and_pelvis_codes:
    site = SITE.Site(RC.palliative_abdomen_and_pelvis_codes, OBJ.palliative_abdomen_and_pelvis_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.abdomen_and_pelvis, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_pelvis_codes:
    site = SITE.Site(RC.palliative_pelvis_codes, OBJ.palliative_pelvis_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.pelvis, CGS.palliative_targets(ss, plan, target))
  elif prescription.region_code in RC.palliative_other_codes:
    site = SITE.Site(RC.palliative_other_codes, OBJ.palliative_other_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription, target=target), CGS.other, CGS.palliative_targets(ss, plan, target))
  return site


# Stereotactic bone/spine:
def bone_stereotactic(ss, plan, prescription):
  oar_objectives = OBJ.palliative_other_oar_objectives
  if prescription.region_code in RC.palliative_head_codes or prescription.region_code in RC.palliative_neck_codes:
    oar_objectives = OAR.palliative_stereotactic_cervical_oars
  elif prescription.region_code in RC.palliative_thorax_codes:
    oar_objectives = OAR.palliative_stereotactic_thorax_oars
  elif prescription.region_code in RC.palliative_abdomen_codes:
    oar_objectives = OAR.palliative_stereotactic_thorax_oars
  elif prescription.region_code in RC.palliative_pelvis_codes:
    oar_objectives = OAR.palliative_stereotactic_pelvis_oars
  if prescription.nr_fractions == 1:
    site = SITE.Site(RC.bone_codes, oar_objectives, OBJ.create_bone_stereotactic_objectives(ss, plan, prescription), CGS.bone_stereotactic_1fx_oars(prescription), CGS.bone_stereotactic_targets)
  else:
    site = SITE.Site(RC.bone_codes, oar_objectives, OBJ.create_bone_stereotactic_objectives(ss, plan, prescription), CGS.bone_stereotactic_3fx_oars(prescription), CGS.bone_stereotactic_targets)
  return site


# Bladder:
def bladder(ss, plan, prescription):
  return SITE.Site(RC.bladder_codes, OBJ.bladder_objectives, OBJ.create_bladder_objectives(plan, ss, prescription), CGS.bladder_oars, CGS.targets)


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
