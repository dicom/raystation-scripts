# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import roi as ROI
import rois as ROIS

# Definitions script for breast treatments (local/locoregional, with/without IMN, with/without boost).
class DefBreast(object):


  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Local/Regional/Regional with IMN
    region = choices[1].value
    # Choice 2: Side - Left or right?
    side = choices[2].value

    if region == 'part':
      site.add_oars(DEF.breast_part_oars)
      if side == 'right':
        site.add_oars([ROIS.breast_r_draft])
        breast_r = ROI.ROIAlgebra(ROIS.breast_r.name, ROIS.breast_r.type, ROIS.breast_r.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.surgical_bed], sourcesB = [breast_r], operator = 'Intersection', marginsA = MARGINS.uniform_15mm_expansion, marginsB = MARGINS.zero)
        ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_oars([breast_r, ctv_sb, ptv_sbc])
      else:
        site.add_oars([ROIS.breast_l_draft])
        breast_l = ROI.ROIAlgebra(ROIS.breast_l.name, ROIS.breast_l.type, ROIS.breast_l.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.surgical_bed], sourcesB = [breast_l], operator = 'Intersection', marginsA = MARGINS.uniform_15mm_expansion, marginsB = MARGINS.zero)
        ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_oars([breast_l, ctv_sb, ptv_sbc])
    elif region == 'tang':
      # Breast with tangential fields
      site.add_oars(DEF.breast_tang_oars)
      if side == 'right':
        site.add_oars([ROIS.breast_r_draft])
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      else:
        site.add_oars([ROIS.breast_l_draft])
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      site.add_targets([ctv, ptv])
      # Choice 2: With our without boost?
      boost = choices[3].value
    elif region in ['reg','imn']:
      # Breast where regional lymph nodes or IMN is included
      # Choice 3: Hypofractionation or not
      frac = choices[3].value
      # Choice 4: With our without boost?
      boost = choices[4].value
      site.add_oars(DEF.breast_reg_oars)
      # Hypofractionated
      if frac == 'hypo':
        if side == 'right':
          ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_expansion)
          site.add_oars([ROIS.breast_r_draft, ROIS.humeral_r, ROIS.breast_l, ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r, ROIS.artery1_r, ROIS.artery2_r, ROIS.vein1_r, ROIS.vein2_r])
        else: # (left)
          ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_expansion)
          site.add_oars([ROIS.breast_l_draft, ROIS.humeral_l, ROIS.breast_r, ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l, ROIS.artery1_l, ROIS.artery2_l, ROIS.vein1_l, ROIS.vein2_l])
        # Common for left and right:
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ctv_n], sourcesB = [ctv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        ptv_p = ROI.ROIAlgebra(ROIS.ptv_pc.name, ROIS.ptv_pc.type, ROIS.ptv.color, sourcesA = [ctv_p], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv_n = ROI.ROIAlgebra(ROIS.ptv_nc.name, ROIS.ptv_nc.type, ROIS.ptv.color, sourcesA = [ctv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ptv_n], sourcesB = [ptv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      else:
        if side == 'right':
          ctv_50 = ROI.ROIAlgebra(ROIS.ctv_50.name, ROIS.ctv_50.type, ROIS.ctv.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          ctv_47 = ROI.ROIAlgebra(ROIS.ctv_47.name, ROIS.ctv_50.type, ROIS.ctv.color, sourcesA = [ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r], sourcesB = [ctv_50], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_expansion)
          site.add_oars([ROIS.breast_r_draft, ROIS.humeral_r, ROIS.breast_l, ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r, ROIS.artery1_r, ROIS.artery2_r, ROIS.vein1_r, ROIS.vein2_r])
        else: # (left)
          ctv_50 = ROI.ROIAlgebra(ROIS.ctv_50.name, ROIS.ctv_50.type, ROIS.ctv.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          ctv_47 = ROI.ROIAlgebra(ROIS.ctv_47.name, ROIS.ctv_47.type, ROIS.ctv.color, sourcesA = [ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l], sourcesB = [ctv_50], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_expansion)
          site.add_oars([ROIS.breast_l_draft, ROIS.humeral_l, ROIS.breast_r, ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l, ROIS.artery1_l, ROIS.artery2_l, ROIS.vein1_l, ROIS.vein2_l])
        # Common for left and right:
        ctv_47_50 = ROI.ROIAlgebra(ROIS.ctv_47_50.name, ROIS.ctv_47_50.type, ROIS.ctv.color, sourcesA = [ctv_47], sourcesB = [ctv_50], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        ptv_50c = ROI.ROIAlgebra(ROIS.ptv_50c.name, ROIS.ptv_50.type, ROIS.ptv.color, sourcesA = [ctv_50], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv_47 = ROI.ROIAlgebra(ROIS.ptv_47.name, ROIS.ptv_47.type, ROIS.ptv.color, sourcesA = [ctv_47], sourcesB = [ptv_50c], operator = 'Subtraction', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
        ptv_47c = ROI.ROIAlgebra(ROIS.ptv_47c.name, ROIS.ptv_47.type, ROIS.ptv.color, sourcesA = [ptv_47], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ptv_47c], sourcesB = [ptv_50c], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        # Only if IMN is included in target volume:
      if region == 'imn':
        site.add_oars([ROIS.imn])
        if frac == 'hypo':
          ctv_n.sourcesA.extend([ROIS.imn])
        else:
          ctv_47.sourcesA.extend([ROIS.imn])
      # Common for all regional:
      if frac == 'hypo':
        site.add_targets([ctv_p, ctv_n, ctv, ptv_p, ptv_n, ptv])
      else:
        site.add_targets([ctv_50, ctv_47, ctv_47_50, ptv_50c, ptv_47, ptv_47c, ptv])
    # Add volumes for boost (2Gy x 8) if selected:
    if not region == 'part':
      if boost:
        if side == 'right':
          ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.surgical_bed], sourcesB = [ROIS.breast_r_draft], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
        else:
          ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.surgical_bed], sourcesB = [ROIS.breast_l_draft], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
        ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv_sb.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_targets([ROIS.surgical_bed, ctv_sb, ptv_sbc])
    # Create all targets and OARs in RayStation:
    site.create_rois()