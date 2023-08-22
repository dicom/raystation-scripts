# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import roi as ROI
import rois as ROIS

# Definitions script for bladder treatments.
class DefBladder(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Intent
    intent = choices[1]
    if intent == 'palliative':
      # Targets:
      ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_low, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.bladder], marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
      ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      site.add_targets([ROIS.gtv_p, ctv, ptv])
    else:
      # Curative:
      # Targets:
      ctv_p = ROI.ROIExpanded(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv, source = ROIS.gtv_p, margins = MARGINS.uniform_5mm_expansion)
      ctv_e = ROI.ROIExpanded(ROIS.ctv_e.name, ROIS.ctv_e.type, COLORS.ctv, source = ROIS.bladder, margins = MARGINS.zero)
      ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, sourcesA=[ctv_p], sourcesB=[ctv_e], marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      site.add_targets([ROIS.gtv_p, ctv_p, ctv_e, ctv, ptv])
    # DL OARs:
    examination.RunOarSegmentation(ModelName="RSL DLS Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Bladder"])
    examination.RunOarSegmentation(ModelName="Alesund Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["CaudaEquina", "BowelBag", "Rectum", "AnalCanal", "L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "FemurHeadNeck_L", "FemurHeadNeck_R"])
    # Create "Bone" ROI Algebra:
    bone_rois = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r]
    vertebrae_rois = [ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = bone_rois, sourcesB = vertebrae_rois)
    site.add_oars([bone])
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Change type to "Other":
    pm.RegionsOfInterest[bone.name].OrganData.OrganType = "Other"
