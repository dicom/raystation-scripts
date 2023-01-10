# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import roi as ROI
import rois as ROIS

# Definitions script for rectum treatments (conventional 50 Gy SIB and hypofractionated 25 Gy).
class DefRectum(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Fractionation - normo or hypofractionated?
    frac = choices[1]
    if frac == 'normo':
      # Conventionally fractionated (2 Gy x 25):
      # Choice 2: Groin target volume - included or not?
      groin = choices[2]
      if groin == 'with':
        # Groin targets included:
        gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n1, ROIS.gtv_groin_l, ROIS.gtv_groin_r])
        site.add_targets([ROIS.gtv_p, ROIS.gtv_n1, ROIS.gtv_groin_l, ROIS.gtv_groin_r, gtv, ROIS.ctv_groin_l, ROIS.ctv_groin_r])
      else:
        # No groin targets:
        gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n1])
        site.add_targets([ROIS.gtv_p, ROIS.gtv_n1, gtv])
      # Common for groin included or not:
      ctv_50 = ROI.ROIAlgebra(ROIS.ctv_50.name, ROIS.ctv_50.type, COLORS.ctv_high, sourcesA=[gtv], sourcesB=[ROIS.ctv_e], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion)
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
      site.add_targets([ROIS.ctv_e, ctv_50, ctv_47, ctv_47_50, ptv_50, ptv_47, ptv_47_50])
      # OARs:
      bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv_47_50], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      bowel_ptv = ROI.ROIAlgebra(ROIS.z_spc_bowel.name, ROIS.z_spc_bowel.type, COLORS.bowel_space, sourcesA = [ROIS.bowel_space], sourcesB = [ptv_47_50], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      wall_ptv_50 = ROI.ROIWall(ROIS.z_ptv_50_wall.name, ROIS.z_ptv_50_wall.type, COLORS.wall, ptv_50, 0.5, 0)
      wall_ptv_47_50 = ROI.ROIWall(ROIS.z_ptv_47_50_wall.name, ROIS.z_ptv_47_50_wall.type, COLORS.wall, ptv_47_50, 0.5, 0)
      # DL OARs:
      examination.RunOarSegmentation(ModelName="RSL Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Bladder", "FemoralHead_L", "FemoralHead_R"])
      # Non-DL OARs:
      site.add_oars([ROIS.bowel_space, ROIS.cauda_equina] + [bladder_ptv, bowel_ptv, wall_ptv_50, wall_ptv_47_50])
    else:
      # Hypofractionated treatment (5 Gy x 5):
      # Targets:
      gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n1])
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv_high, sourcesA=[gtv], sourcesB=[ROIS.ctv_e], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion)
      ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_low, sourcesA=[ROIS.ctv_e], sourcesB=[ctv_p])
      ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_med, sourcesA=[ctv_p], sourcesB=[ROIS.ctv_e], marginsA = MARGINS.rectum_ptv_50_expansion, marginsB = MARGINS.rectum_ctv_primary_risk_expansion)
      site.add_targets([ROIS.gtv_p, ROIS.gtv_n1, gtv, ctv_p, ROIS.ctv_e, ctv, ptv])
      # OARs:
      bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      bowel_ptv = ROI.ROIAlgebra(ROIS.z_spc_bowel.name, ROIS.z_spc_bowel.type, COLORS.bowel_space, sourcesA = [ROIS.bowel_space], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      # DL OARs:
      examination.RunOarSegmentation(ModelName="RSL Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Bladder", "FemoralHead_L", "FemoralHead_R"])
      # Non-DL OARs:
      site.add_oars([ROIS.bowel_space, ROIS.cauda_equina] + [bladder_ptv, bowel_ptv])
    # Create all targets and OARs in RayStation:
    site.create_rois()
