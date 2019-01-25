# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import roi as ROI
import rois as ROIS

# Definitions script for palliative treatments (prostate/prostate bed, with or without lymph nodes, normo/hypofractionated).
class DefPalliative(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Stereotactic or not?
    stereotactic = choices[1].value
    # Choice 2: Region
    region = choices[2].value
    # Stereotactic:
    if stereotactic:
      if region in ['col thorax', 'col pelvis']:
        if region == 'col thorax':
          site.add_oars(DEF.palliative_stereotactic_thorax_oars)
        elif region == 'col pelvis':
          site.add_oars(DEF.palliative_stereotactic_spine_pelvis_oars)
        ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_med, ROIS.gtv, margins = MARGINS.uniform_3mm_expansion)
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB=[ROIS.vb])
        ptv_gtv = ROI.ROIAlgebra(ROIS.ptv_gtv.name, ROIS.ptv_gtv.type, COLORS.ptv_med, sourcesA = [ptv], sourcesB = [ROIS.gtv], operator='Subtraction')
        ptv_spinal = ROI.ROIAlgebra(ROIS.ptv_spinal.name, ROIS.ptv_spinal.type, COLORS.ptv_med, sourcesA = [ptv], sourcesB = [ROIS.spinal_cord_prv], operator='Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_1mm_expansion)
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        site.add_oars([ROIS.spinal_cord_prv, wall_ptv])
        site.add_targets([ROIS.gtv, ROIS.vb, ptv_gtv, ptv_spinal, ctv, ptv])
      else:
        site.add_oars(DEF.palliative_stereotactic_pelvis_oars)
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, ROIS.gtv, margins = MARGINS.uniform_3mm_expansion)
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        site.add_oars([wall_ptv])
        site.add_targets([ROIS.gtv, ptv])
    # Not stereotactic:
    else:
      # Region:
      if region == 'head':
        site.add_oars(DEF.palliative_head_oars)
      elif region == 'neck':
        site.add_oars(DEF.palliative_neck_oars)
      elif region == 'thorax':
        site.add_oars(DEF.palliative_thorax_oars)
      elif region == 'abdomen':
        site.add_oars(DEF.palliative_abdomen_oars)
      elif region == 'pelvis':
        site.add_oars(DEF.palliative_pelvis_oars)
      # Choice 3: Number of targets:
      nr_targets = choices[3].value
      # Choice 4: GTV included?
      with_gtv = choices[4].value
      # Nr of target volumes:
      if nr_targets == '1':
        if with_gtv:
          site.add_targets([ROIS.gtv, ROIS.ctv_ext])
        else:
          site.add_targets([ROIS.ctv_underived])
          ROIS.ptv_ext.source = ROIS.ctv_underived
        site.add_targets([ROIS.ptv_ext])
      # 2 targets:
      else:
        # With GTV:
        if with_gtv:
          ctv1 = ROI.ROIAlgebra(ROIS.ctv1.name, ROIS.ctv1.type, ROIS.ctv.color, sourcesA = [ROIS.gtv1], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
          ctv2 = ROI.ROIAlgebra(ROIS.ctv2.name, ROIS.ctv2.type, ROIS.ctv.color, sourcesA = [ROIS.gtv2], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
          ptv1 = ROI.ROIAlgebra(ROIS.ptv1.name, ROIS.ptv1.type, ROIS.ptv.color, sourcesA = [ROIS.ctv1], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
          ptv2 = ROI.ROIAlgebra(ROIS.ptv2.name, ROIS.ptv2.type, ROIS.ptv.color, sourcesA = [ROIS.ctv2], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
          gtv =  ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv1], sourcesB=[ROIS.gtv2])
          ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ctv1], sourcesB=[ctv2])
          site.add_targets([ROIS.gtv1, ROIS.gtv2, gtv, ctv1, ctv2, ctv, ptv1, ptv2])
        # Without GTV:
        else:
          ptv1 = ROI.ROIAlgebra(ROIS.ptv1.name, ROIS.ptv1.type, ROIS.ptv.color, sourcesA = [ROIS.ctv1], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
          ptv2 = ROI.ROIAlgebra(ROIS.ptv2.name, ROIS.ptv2.type, ROIS.ptv.color, sourcesA = [ROIS.ctv2], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
          ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ROIS.ctv1], sourcesB=[ROIS.ctv2])
          site.add_targets([ROIS.ctv1, ROIS.ctv2, ctv, ptv1, ptv2])

        ptv =  ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptv1], sourcesB=[ptv2])
        site.add_targets([ptv])
    # Create all targets and OARs in RayStation:
    site.create_rois()
