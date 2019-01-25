# encoding: utf8

# Import system libraries:

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import structure_set_functions as SSF
import roi as ROI
import rois as ROIS

# Definitions script for brain treatments (whole brain, part of brain, stereotactic brain).
class DefBrain(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Scope (whole brain, part or stereotactic).
    region = choices[1].value
    # Region:
    # Whole brain:
    if region== 'whole':
      site.add_oars(DEF.brain_whole_oars)
      ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, ROIS.brain)
      ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, ctv, margins = MARGINS.uniform_3mm_expansion)
      site.add_targets([ctv, ptv])
    # Partial Brain:
    elif region == 'part':
      # Choice 2: Diagnosis:
      diagnosis = choices[2].value
      # Glioblastom:
      if diagnosis == 'glio':
        gtv =  ROI.ROIExpanded(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, ROIS.gtv_sb)
        ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, gtv, margins = MARGINS.uniform_20mm_expansion)
        brain_gtv = ROI.ROIAlgebra(ROIS.brain_gtv.name, ROIS.brain_gtv.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [gtv], operator = 'Subtraction')
        site.add_oars([brain_gtv])
        site.add_targets([ROIS.gtv_p, ROIS.gtv_sb, gtv, ctv])
      # All other diagnoses:
      else:
        ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, ROIS.gtv, margins = MARGINS.uniform_20mm_expansion)
        brain_gtv = ROI.ROIAlgebra(ROIS.brain_gtv.name, ROIS.brain_gtv.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [ROIS.gtv], operator = 'Subtraction')
        site.add_oars([brain_gtv])
        site.add_targets([ROIS.gtv, ctv])
      # Common for all diagnoses of partial brain:
      site.add_oars(DEF.brain_partial_oars)
      ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, ctv, margins = MARGINS.uniform_3mm_expansion)
      brain_ptv = ROI.ROIAlgebra(ROIS.brain_ptv.name, ROIS.brain_ptv.type, ROIS.other_ptv.color, sourcesA = [ROIS.brain], sourcesB = [ptv], operator = 'Subtraction')
      site.add_oars([brain_ptv])
      site.add_targets([ptv])
      
    # Stereotactic brain:
    elif region == 'stereotactic':
      site.add_oars(DEF.brain_stereotactic_oars)
      # Choice 2: Nr of targets.
      nr_targets= choices[2].value
      # One target:
      if nr_targets == 'one':
        gtv = ROI.ROI('GTV', 'Gtv', ROIS.gtv.color)
        ptv =  ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, gtv, margins = MARGINS.uniform_2mm_expansion)
        wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv, 1, 0)
        site.add_targets([wall_ptv])
      # Multiple targets (2, 3 or 4):
      elif nr_targets in ['two','three','four']:
        gtv =  ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv1], sourcesB=[ROIS.gtv2])
        ptv1 =  ROI.ROIExpanded(ROIS.ptv1.name, ROIS.ptv1.type, COLORS.ptv, ROIS.gtv1, margins = MARGINS.uniform_2mm_expansion)
        ptv2 =  ROI.ROIExpanded(ROIS.ptv2.name, ROIS.ptv2.type, COLORS.ptv, ROIS.gtv2, margins = MARGINS.uniform_2mm_expansion)
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptv1], sourcesB=[ptv2])
        wall_ptv1 = ROI.ROIWall(ROIS.z_ptv1_wall.name, ROIS.z_ptv1_wall.type, COLORS.wall, ptv1, 1, 0)
        wall_ptv2 = ROI.ROIWall(ROIS.z_ptv2_wall.name, ROIS.z_ptv2_wall.type, COLORS.wall, ptv2, 1, 0)
        site.add_targets([wall_ptv1, wall_ptv2])
        site.add_targets([ROIS.gtv1, ROIS.gtv2, ptv1, ptv2])
        # 3 or 4 targets:
        if nr_targets in ['three','four']:
          ptv3 =  ROI.ROIExpanded(ROIS.ptv3.name, ROIS.ptv3.type, COLORS.ptv, ROIS.gtv3, margins = MARGINS.uniform_2mm_expansion)
          wall_ptv3 = ROI.ROIWall(ROIS.z_ptv3_wall.name, ROIS.z_ptv3_wall.type, COLORS.wall, ptv3, 1, 0)
          ptv.sourcesB.extend([ptv3])
          gtv.sourcesB.extend([ROIS.gtv3])
          site.add_targets([ROIS.gtv3, ptv3])
          site.add_targets([wall_ptv3])
          # 4 targets:
          if nr_targets in ['four']:
            ptv4 =  ROI.ROIExpanded(ROIS.ptv4.name, ROIS.ptv4.type, COLORS.ptv, ROIS.gtv4, margins = MARGINS.uniform_2mm_expansion)
            wall_ptv4 = ROI.ROIWall(ROIS.z_ptv4_wall.name, ROIS.z_ptv4_wall.type, COLORS.wall, ptv4, 1, 0)
            ptv.sourcesB.extend([ptv4])
            gtv.sourcesB.extend([ROIS.gtv4])
            site.add_targets([ROIS.gtv4, ptv4])
            site.add_targets([wall_ptv4])
      # Common for stereotactic:
      brain_ptv = ROI.ROIAlgebra(ROIS.brain_ptv.name, ROIS.brain_ptv.type, ROIS.other_ptv.color, sourcesA = [ROIS.brain], sourcesB = [ptv], operator = 'Subtraction')
      brain_gtv = ROI.ROIAlgebra(ROIS.brain_gtv.name, ROIS.brain_gtv.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [gtv], operator = 'Subtraction')
      site.add_targets([gtv, ptv])
      site.add_oars([brain_ptv, brain_gtv])

    # Create all targets and OARs in RayStation:
    site.create_rois()
