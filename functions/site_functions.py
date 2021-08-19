# encoding: utf8

# Import local files:
import region_codes as RC
import clinical_goals as CGS
import objectives as OBJ
import rt_site as SITE
import rois as ROIS
import patient_model_functions as PMF
import structure_set_functions as SSF

# Example:
# SITE.Site(codes, oar_objectives, opt_objectives, oar_clinical_goals, target_clinical_goals)

# Set up regions:
# Brain
def brain(pm, examination, ss, plan, prescription, region_code):
  if region_code in RC.brain_whole_codes:
    return SITE.Site(RC.brain_codes, OBJ.brain_whole_oar_objectives, OBJ.create_whole_brain_objectives(ss, plan, prescription.total_dose), CGS.brain_oars(prescription.nr_fractions, region_code), CGS.brain_targets(ss, prescription.nr_fractions))
  else:
    return SITE.Site(RC.brain_codes, OBJ.brain_oar_objectives, OBJ.create_brain_objectives(pm, examination, ss, plan, prescription.total_dose, prescription.nr_fractions), CGS.brain_oars(prescription.nr_fractions, region_code), CGS.brain_targets(ss, prescription.nr_fractions))


# Lung
def lung(ss, plan, prescription, region_code, target):
  if prescription.total_dose == 45 and prescription.nr_fractions == 3:
    return SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_stereotactic_objectives(ss, plan, region_code, prescription.total_dose), CGS.lung_stereotactic_3fx_oars(region_code), CGS.lung_stereotactic_targets(ss))
  elif prescription.total_dose == 55 and prescription.nr_fractions == 5:
    return SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_stereotactic_objectives(ss, plan, region_code, prescription.total_dose), CGS.lung_stereotactic_5fx_oars(region_code), CGS.lung_stereotactic_targets(ss))
  elif prescription.total_dose == 56 and prescription.nr_fractions == 8:
    return SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_stereotactic_objectives(ss, plan, region_code, prescription.total_dose), CGS.lung_stereotactic_8fx_oars(region_code), CGS.lung_stereotactic_targets(ss))
  else:
    return SITE.Site(RC.lung_codes, OBJ.lung_objectives, OBJ.create_lung_objectives(ss, plan, target, prescription.total_dose), CGS.lung_oars(ss), CGS.lung_targets(ss))


# Breast
def breast(ss, plan, prescription, region_code, technique_name, target):
  if region_code in RC.breast_reg_codes:
    return SITE.Site(RC.breast_reg_codes, OBJ.breast_reg_oar_objectives, OBJ.create_breast_reg_objectives(ss, plan, region_code, prescription.total_dose, technique_name), CGS.breast_oars(ss, region_code, prescription.nr_fractions, target), CGS.breast_targets(ss, region_code, target))
  else:
    return SITE.Site(RC.breast_tang_codes, OBJ.breast_tang_oar_objectives, OBJ.create_breast_tang_objectives(ss, plan, prescription.total_dose, target), CGS.breast_oars(ss, region_code, prescription.nr_fractions, target), CGS.breast_targets(ss, region_code, target))


# Prostate
def prostate(ss, plan, prescription, region_code, target):
  if prescription.total_dose < 40:
    return SITE.Site(RC.prostate_codes, OBJ.palliative_prostate_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.prostate_oars(ss, prescription.total_dose), CGS.palliative_targets(ss, plan, target))
  if region_code in RC.prostate_bed_codes:
    return SITE.Site(RC.prostate_bed_codes, OBJ.prostate_objectives, OBJ.create_prostate_bed_objectives(ss, plan, prescription.total_dose), CGS.prostate_oars(ss, prescription.total_dose), CGS.prostate_bed_targets(ss))
  else:
    return SITE.Site(RC.prostate_codes, OBJ.prostate_objectives, OBJ.create_prostate_objectives(ss, plan, prescription.total_dose), CGS.prostate_oars(ss, prescription.total_dose), CGS.prostate_targets(ss, prescription.total_dose))


# Rectum
def rectum(ss, plan, prescription):
  return SITE.Site(RC.rectum_codes, OBJ.rectum_objectives, OBJ.create_rectum_objectives(ss, plan, prescription.total_dose), CGS.rectum_oars, CGS.rectum_targets(prescription.total_dose))


# Palliative
# Gives a treatment site (e.g. Pelvis) based on a specific region code (e.g. 314).
def palliative(ss, plan, prescription, region_code, target):
	if region_code in RC.palliative_head_codes:
		return SITE.Site(RC.palliative_head_codes, OBJ.palliative_head_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.head, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_neck_codes:
		return SITE.Site(RC.palliative_neck_codes, OBJ.palliative_neck_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.neck, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_thorax_codes:
		return SITE.Site(RC.palliative_thorax_codes, OBJ.palliative_thorax_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.thorax, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_thorax_and_abdomen_codes:
		return SITE.Site(RC.palliative_thorax_and_abdomen_codes, OBJ.palliative_thorax_and_abdomen_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.thorax_and_abdomen, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_abdomen_codes:
		return SITE.Site(RC.palliative_abdomen_codes, OBJ.palliative_abdomen_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.abdomen, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_abdomen_and_pelvis_codes:
		return SITE.Site(RC.palliative_abdomen_and_pelvis_codes, OBJ.palliative_abdomen_and_pelvis_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.abdomen_and_pelvis, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_pelvis_codes:
		return SITE.Site(RC.palliative_pelvis_codes, OBJ.palliative_pelvis_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.pelvis, CGS.palliative_targets(ss, plan, target))
	elif region_code in RC.palliative_other_codes:
		return SITE.Site(RC.palliative_other_codes, OBJ.palliative_other_oar_objectives, OBJ.create_palliative_objectives(ss, plan, prescription.total_dose, target=target), CGS.other, CGS.palliative_targets(ss, plan, target))


# Stereotactic bone/spine
def bone_stereotactic(ss, plan, prescription, region_code):
  if prescription.nr_fractions == 1:
    return SITE.Site(RC.bone_stereotactic_codes, OBJ.palliative_other_oar_objectives, OBJ.create_bone_stereotactic_objectives(ss, plan, prescription.total_dose), CGS.bone_stereotactic_1fx_oars(region_code), CGS.bone_stereotactic_targets)
  elif prescription.nr_fractions == 3:
    return SITE.Site(RC.bone_stereotactic_codes, OBJ.palliative_other_oar_objectives, OBJ.create_bone_stereotactic_objectives(ss, plan, prescription.total_dose), CGS.bone_stereotactic_3fx_oars(region_code), CGS.bone_stereotactic_targets)


# Bladder
def bladder(ss, plan, prescription):
  return SITE.Site(RC.bladder_codes, OBJ.bladder_objectives, OBJ.create_bladder_objectives(plan, ss, prescription.total_dose), CGS.bladder_oars, CGS.targets)


# Determines the site from the region code
def site(pm, examination, ss, plan, prescription, region_code, target, technique_name):
  if region_code in RC.brain_codes:
    if region_code not in RC.brain_whole_codes:
      if prescription.nr_fractions > 5:
        PMF.create_retina_and_cornea(pm, examination, ss, ROIS.lens_l, ROIS.box_l, ROIS.eye_l, ROIS.retina_l, ROIS.cornea_l)
        PMF.create_retina_and_cornea(pm, examination, ss, ROIS.lens_r, ROIS.box_r, ROIS.eye_r, ROIS.retina_r, ROIS.cornea_r)
    return brain(pm, examination, ss, plan, prescription, region_code)
  elif region_code in RC.breast_codes:
    if region_code in RC.breast_not_thorax_codes:
      # Create a "Markers" ROI:
      breast_target = SSF.determine_breast_primary_target(ss)
      PMF.create_grey_value_intersection_roi(pm, examination, ss, ROIS.temp_markers, breast_target, ROIS.markers, 250, 2500)
      pm.RegionsOfInterest[ROIS.markers.name].OrganData.OrganType = 'Other'
    return breast(ss, plan, prescription, region_code, technique_name, target)
  elif region_code in RC.lung_and_mediastinum_codes:
    return lung(ss, plan, prescription, region_code, target)
  elif region_code in RC.prostate_codes:
    if prescription.total_dose > 50:
      PMF.create_bottom_part_x_cm(pm, examination, ss, ROIS.rectum, ROIS.anal_canal, 4)
    return prostate(ss, plan, prescription, region_code, target)
  elif region_code in RC.rectum_codes:
    return rectum(ss, plan, prescription)
  elif region_code in RC.bladder_codes:
    return bladder(ss, plan, prescription)
  elif region_code in RC.palliative_codes or region_code in RC.prostate_codes:
    if prescription.nr_fractions == 1 and prescription.total_dose > 15 or prescription.nr_fractions == 3 and prescription.total_dose == 27:
      return bone_stereotactic(ss, plan, prescription, region_code)
    else:
      return palliative(ss, plan, prescription, region_code, target)
