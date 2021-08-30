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
    region = choices[1]
    # Region:
    if region== 'whole':
      # Whole brain:
      # Targets:
      ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, ROIS.brain)
      ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, ctv, margins = MARGINS.uniform_3mm_expansion)
      site.add_targets([ctv, ptv])
      # OARs:
      site.add_oars(DEF.brain_whole_oars)
    elif region == 'part':
      # Partial Brain:
      # Targets:
      ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, sourcesA = [ROIS.gtv], sourcesB = [ROIS.brain], operator = 'Intersection', marginsA = MARGINS.uniform_20mm_expansion, marginsB = MARGINS.uniform_1mm_expansion)
      ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, sourcesA = [ctv], sourcesB = [ROIS.body], operator = 'Intersection', marginsA = MARGINS.uniform_3mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
      site.add_targets([ROIS.gtv, ctv, ptv])
      # OARs:
      brain_gtv = ROI.ROIAlgebra(ROIS.brain_gtv.name, ROIS.brain_gtv.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [ROIS.gtv], operator = 'Subtraction')
      brain_ptv = ROI.ROIAlgebra(ROIS.brain_ptv.name, ROIS.brain_ptv.type, ROIS.other_ptv.color, sourcesA = [ROIS.brain], sourcesB = [ptv], operator = 'Subtraction')
      site.add_oars(DEF.brain_partial_oars +  [brain_gtv, brain_ptv])
    elif region == 'stereotactic':
      # Stereotactic brain:
      # Choice 2: Nr of targets.
      nr_targets = int(choices[2])
      gtvs = []
      ptvs = []
      walls = []
      # How many targets?
      if nr_targets == 1:
        # Single target:
        gtv = ROI.ROI('GTV', 'Gtv', ROIS.gtv.color)
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, gtv, margins = MARGINS.uniform_2mm_expansion)
        gtvs.append(gtv)
        ptvs.append(ptv)
        walls.append(ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptvs[-1], 1, 0))
      else:
        # Multiple targets (2, 3 or 4):
        for i in range(0, nr_targets):
          # Targets:
          gtvs.append(ROI.ROI('GTV'+str(i+1), 'Gtv', ROIS.gtv.color))
          ptvs.append(ROI.ROIExpanded(ROIS.ptv.name+str(i+1), ROIS.ptv.type, COLORS.ptv, gtvs[-1], margins = MARGINS.uniform_2mm_expansion))
          # OARs:
          walls.append(ROI.ROIWall(ROIS.z_ptv_wall.name+str(i+1), ROIS.z_ptv_wall.type, COLORS.wall, ptvs[-1], 1, 0))
        # Union target volumes:
        gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[gtvs[0]], sourcesB=gtvs[1:])
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptvs[0]], sourcesB=ptvs[1:])
        gtvs.append(gtv)
        ptvs.append(ptv)
      # Common for single or multiple SRT targets:
      # Brain with targets excluded:
      brain_gtv = ROI.ROIAlgebra(ROIS.brain_gtv.name, ROIS.brain_gtv.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [gtv], operator = 'Subtraction')
      brain_ptv = ROI.ROIAlgebra(ROIS.brain_ptv.name, ROIS.brain_ptv.type, ROIS.other_ptv.color, sourcesA = [ROIS.brain], sourcesB = [ptv], operator = 'Subtraction')
      # Add to site:
      site.add_targets(gtvs + ptvs)
      site.add_oars(DEF.brain_stereotactic_oars + [brain_gtv, brain_ptv] + walls)
    # Create all targets and OARs in RayStation:
    site.create_rois()
