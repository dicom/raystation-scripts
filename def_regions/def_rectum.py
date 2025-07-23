# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS

# Definitions script for rectum treatments (conventional 50 Gy SIB and hypofractionated 25 Gy).
class DefRectum(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, examination, site)
    # Choice 1: Fractionation - normo or hypofractionated?
    frac = choices[1]
    if frac == 'normo':
      # Choice 2: Groin target volume - included or not?
      groin = choices[2]
      # Conventionally fractionated (2 Gy x 25):
      self.add_conventional_fx(pm, examination, site, groin)
    else:
      # Hypofractionated treatment (5 Gy x 5):
      self.add_hypo_fx(pm, examination, site)
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Change type to "Other":
    pm.RegionsOfInterest['Bone'].OrganData.OrganType = "Other"
    pm.RegionsOfInterest['BowelBag_Draft'].OrganData.OrganType = "Other"
    # Exclude some ROIs from export:
    exclude = ["L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "FemurHeadNeck_L", "FemurHeadNeck_R"]
    for roi_name in exclude:
      PMF.exclude_roi_from_export(pm, roi_name)


  # Adds rois that are common across all cases.
  def add_common_rois(self, pm, examination, site):
    # DL ROIs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "Bladder": "Bladder"
      },
      'Alesund Male Pelvic CT': {
        "CaudaEquina": "CaudaEquina",
        "BowelBag_Draft": "BowelBag",
        "L5": "L5",
        "Sacrum": "Sacrum",
        "Coccyx": "Coccyx",
        "PelvicGirdle_L": "PelvicGirdle_L",
        "PelvicGirdle_R": "PelvicGirdle_R",
        "FemurHeadNeck_L": "FemurHeadNeck_L",
        "FemurHeadNeck_R": "FemurHeadNeck_R"
      }
    })
    # Create "Bone" ROI Algebra:
    bone_rois = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r]
    vertebrae_rois = [ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = bone_rois, sourcesB = vertebrae_rois)
    site.add_oars([bone, ROIS.bowel_bag])
  
  
  # Adds hypo fx (5 Gy x 5) ROIs to the site object.
  def add_hypo_fx(self, pm, examination, site):
    # Targets:
    gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n1])
    # We will not use the CTVp in ROI algebra from now on, but we'll keep it present for visual aid:
    z_ctv_p_default = ROI.ROIAlgebra('zCTVp_default', 'Undefined', COLORS.ctv_high, sourcesA = [gtv], sourcesB=[ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r, ROIS.l5, ROIS.sacrum, ROIS.coccyx], operator = 'Subtraction', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.zero)
    ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_low, sourcesA=[ROIS.ctv_e], sourcesB=[ROIS.external], operator = 'Intersection', marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_med, sourcesA=[ROIS.ctv_e], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.rectum_ctv_primary_risk_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.gtv_p, ROIS.gtv_n1, gtv, z_ctv_p_default, ROIS.ctv_e, ctv, ptv])
    # OARs:
    wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv, 0.5, 0)
    # Non-DL OARs:
    site.add_oars([wall_ptv])
  
  
  # Adds conventional fractionated (2 Gy x 25) ROIs to the site object.
  def add_conventional_fx(self, pm, examination, site, groin):
    # With our without groin targets?
    if groin == 'with':
      # Groin targets included:
      gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n1, ROIS.gtv_groin_l, ROIS.gtv_groin_r])
      site.add_targets([ROIS.gtv_p, ROIS.gtv_n1, ROIS.gtv_groin_l, ROIS.gtv_groin_r, gtv, ROIS.ctv_groin_l, ROIS.ctv_groin_r])
    else:
      # No groin targets:
      gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n1])
      site.add_targets([ROIS.gtv_p, ROIS.gtv_n1, gtv])
    # Common for groin included or not:
    ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv_high, sourcesA = [ROIS.gtv_p], sourcesB=[ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r, ROIS.l5, ROIS.sacrum, ROIS.coccyx], operator = 'Subtraction', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.zero)
    ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.ctv_high, sourcesA = [ROIS.gtv_n1], sourcesB=[ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r, ROIS.l5, ROIS.sacrum, ROIS.coccyx], operator = 'Subtraction', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.zero)
    ctv_50 = ROI.ROIAlgebra(ROIS.ctv_50.name, ROIS.ctv_50.type, COLORS.ctv_high, sourcesA=[ctv_p], sourcesB=[ctv_n], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv_50 = ROI.ROIAlgebra(ROIS.ptv_50.name, ROIS.ptv_50.type, COLORS.ptv_high, sourcesA=[ctv_50], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.rectum_ptv_50_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    ctv_47 = ROI.ROIAlgebra(ROIS.ctv_47.name, ROIS.ctv_47.type, COLORS.ctv_low, sourcesA=[ROIS.ctv_e], sourcesB=[ptv_50], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    if groin == 'with':
      # Specific for groin targets included:
      ctv_47.sourcesA.extend([ROIS.ctv_groin_l, ROIS.ctv_groin_r])
      ptv_groin_l = ROI.ROIAlgebra(ROIS.ptv_groin_l.name, ROIS.ptv_groin_l.type, COLORS.ptv, sourcesA=[ROIS.ctv_groin_l], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      ptv_groin_r = ROI.ROIAlgebra(ROIS.ptv_groin_r.name, ROIS.ptv_groin_r.type, COLORS.ptv, sourcesA=[ROIS.ctv_groin_r], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      ptv_e = ROI.ROIAlgebra(ROIS.ptv_e.name, ROIS.ptv_e.type, COLORS.ptv, sourcesA=[ROIS.ctv_e], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.rectum_ctv_primary_risk_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      ptv_47_tot = ROI.ROIAlgebra(ROIS.ptv_47_tot.name, ROIS.ptv_47.type, COLORS.ptv_med, sourcesA=[ptv_e], sourcesB=[ptv_groin_l, ptv_groin_r], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv_47 = ROI.ROIAlgebra(ROIS.ptv_47.name, ROIS.ptv_47.type, COLORS.ptv_med, sourcesA=[ptv_47_tot], sourcesB=[ptv_50], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      site.add_targets([ptv_groin_l, ptv_groin_r, ptv_e, ptv_47_tot])
    else:
      # Specific for groin targets excluded:
      ptv_47 = ROI.ROIAlgebra(ROIS.ptv_47.name, ROIS.ptv_47.type, COLORS.ptv_med, sourcesA=[ctv_47], sourcesB=[ptv_50], operator = 'Subtraction', marginsA = MARGINS.rectum_ctv_primary_risk_expansion, marginsB = MARGINS.zero)
    # Targets:
    ctv_47_50 = ROI.ROIAlgebra(ROIS.ctv_47_50.name, ROIS.ctv_47_50.type, COLORS.ctv_alt, sourcesA = [ctv_47], sourcesB = [ctv_50], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv_47_50 = ROI.ROIAlgebra(ROIS.ptv_47_50.name, ROIS.ptv_47_50.type, COLORS.ptv_low, sourcesA = [ptv_47], sourcesB = [ptv_50], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    site.add_targets([ROIS.ctv_e, ctv_p, ctv_n, ctv_50, ctv_47, ctv_47_50, ptv_50, ptv_47, ptv_47_50])
    # OARs:
    wall_ptv_50 = ROI.ROIWall(ROIS.z_ptv_50_wall.name, ROIS.z_ptv_50_wall.type, COLORS.wall, ptv_50, 0.5, 0)
    wall_ptv_47_50 = ROI.ROIWall(ROIS.z_ptv_47_50_wall.name, ROIS.z_ptv_47_50_wall.type, COLORS.wall, ptv_47_50, 0.5, 0)
    # Non-DL OARs:
    site.add_oars([wall_ptv_50, wall_ptv_47_50])
  