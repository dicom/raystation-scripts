# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS

# Definitions script for bladder treatments.
class DefBladder(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, patient, pm, examination, ss, choices, site):
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, examination, site)
    # Add ROIs based on gender:
    self.add_gender_based_rois(patient, pm, examination, site)
    # Choice 1: Intent
    intent = choices[1]
    if intent == 'palliative':
      self.add_palliative(pm, examination, site)
    else:
      self.add_curative(pm, examination, site)
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Change type to "Other":
    pm.RegionsOfInterest['Bone'].OrganData.OrganType = "Other"
    pm.RegionsOfInterest['BowelBag_Draft'].OrganData.OrganType = "Other"
    # Exclude some ROIs from export:
    exclude = ["L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "Femur_L", "Femur_R"]
    for roi_name in exclude:
      PMF.exclude_roi_from_export(pm, roi_name)


  # Adds rois that are common across all cases.
  def add_common_rois(self, pm, examination, site):
    # Create "Bone" ROI Algebra:
    pelvic_bone_rois = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_l, ROIS.femur_r]
    vertebrae_rois = [ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = pelvic_bone_rois, sourcesB = vertebrae_rois)
    site.add_oars([ROIS.anal_canal, ROIS.bladder, bone, ROIS.bowel_bag_draft, ROIS.bowel_bag, ROIS.cauda_equina, ROIS.coccyx, ROIS.l5, ROIS.femoral_head_l, ROIS.femoral_head_r, ROIS.femur_l, ROIS.femur_r, ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.rectum, ROIS.sacrum])
  
  
  # Adds rois that are based on gender.
  def add_gender_based_rois(self, patient, pm, examination, site):
    if patient.Gender == 'Female':
      site.add_oars([ROIS.uterus])
    elif patient.Gender == 'Male':
      site.add_oars([ROIS.penile_bulb])
  
  
  # Adds curative ROIs to the site object.
  def add_curative(self, pm, examination, site):
    # Targets:
    ctv_p = ROI.ROIExpanded(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv, source = ROIS.gtv_p, margins = MARGINS.uniform_5mm_expansion)
    ctv_e = ROI.ROIExpanded(ROIS.ctv_e.name, ROIS.ctv_e.type, COLORS.ctv, source = ROIS.bladder, margins = MARGINS.zero)
    ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, sourcesA=[ctv_p], sourcesB=[ctv_e], marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.gtv_p, ctv_p, ctv_e, ctv, ptv])
  
  
  # Adds palliative ROIs to the site object.
  def add_palliative(self, pm, examination, site):
    # Targets:
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ROIS.ctv_underived], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.ctv_underived, ptv])
