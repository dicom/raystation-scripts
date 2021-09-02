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
    region = choices[1]
    # Choice 2: Side - Left or right?
    side = choices[2]
    # Region:
    if region == 'partial':
      # Partial breast only:
      if side == 'right':
        # Right:
        breast_draft = ROIS.breast_r_draft
        breast = ROI.ROIAlgebra(ROIS.breast_r.name, ROIS.breast_r.type, ROIS.breast_r.color, sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      else:
        # Left:
        breast_draft = ROIS.breast_l_draft
        breast = ROI.ROIAlgebra(ROIS.breast_l.name, ROIS.breast_l.type, ROIS.breast_l.color, sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      # Targets:
      ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.surgical_bed], sourcesB = [breast], operator = 'Intersection', marginsA = MARGINS.uniform_15mm_expansion, marginsB = MARGINS.zero)
      ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      site.add_targets([ctv_sb, ptv_sbc])
      # OARs:
      site.add_oars(DEF.breast_part_oars + [breast_draft, breast])
    else:
      # Whole breast (with or without regional nodes):
      # Choice 3: With our without boost?
      boost = choices[3]
      if region == 'whole':
        # Whole breast:
        if side == 'right':
          breast_draft = ROIS.breast_r_draft
        else:
          breast_draft = ROIS.breast_l_draft
        # Targets:
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_targets([ctv, ptv])
        # OARs:
        site.add_oars(DEF.breast_whole_oars + [breast_draft])
      elif region in ['regional','regional_imn']:
        # Regional breast (with or without IMN):
        # Side dependent OARs and support structures for regional treatment:
        if side == 'right':
          # Targets:
          ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
          if region == 'regional_imn':
            imn = ROIS.imn_r
          # Others:
          site.add_oars([ROIS.breast_r_draft, ROIS.breast_l, ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r])
          # OARs:
          site.add_oars(DEF.breast_reg_oars + [ROIS.humeral_r, ROIS.scalene_muscle_r, ROIS.artery1_r, ROIS.artery2_r, ROIS.artery3_r, ROIS.vein1_r, ROIS.vein2_r, ROIS.vein3_r, ROIS.liver])
        else:
          # Targets:
          ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
          if region == 'regional_imn':
            imn = ROIS.imn_l
          # Others:
          site.add_oars([ROIS.breast_l_draft, ROIS.breast_r, ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l])
          # OARs:
          site.add_oars(DEF.breast_reg_oars + [ROIS.humeral_l, ROIS.scalene_muscle_l, ROIS.artery1_l, ROIS.artery2_l, ROIS.vein1_l, ROIS.vein2_l, ROIS.vein3_l])
        # Common targets for left and right:
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ctv_n], sourcesB = [ctv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        ptv_p = ROI.ROIAlgebra(ROIS.ptv_pc.name, ROIS.ptv_pc.type, ROIS.ptv.color, sourcesA = [ctv_p], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv_n = ROI.ROIAlgebra(ROIS.ptv_nc.name, ROIS.ptv_nc.type, ROIS.ptv.color, sourcesA = [ctv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ptv_n], sourcesB = [ptv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        # IMN:
        if region == 'regional_imn':
          site.add_oars([imn])
          ctv_n.sourcesA.extend([imn])
        # Common targets for all regional:
        site.add_targets([ctv_p, ctv_n, ctv, ptv_p, ptv_n, ptv])
      # Add targets for boost (2 Gy x 8) if selected:
      if boost == 'with':
        ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.surgical_bed], sourcesB = [ctv], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
        ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv_sb.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_targets([ROIS.surgical_bed, ctv_sb, ptv_sbc])
    # Create all targets and OARs in RayStation:
    site.create_rois()
