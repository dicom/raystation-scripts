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
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, examination, site)
    # Choice 1: Scope (whole brain, part or stereotactic).
    region = choices[1]
    # Region:
    if region== 'whole':
      # Choice 2: Involvement of menignes.
      meninges = choices[2]
      self.add_whole_brain(pm, examination, site, meninges)
    elif region == 'part':
      # Partial Brain:
      self.add_partial_brain(pm, examination, site)
    elif region == 'stereotactic':
      # Stereotactic brain:
      # Choice 2: Nr of targets.
      nr_targets = int(choices[2])
      self.add_stereotactic_brain(pm, examination, site, nr_targets)
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Change ROI type to "Other" for selected ROIs:
    for name in [ROIS.brain_gtv.name, ROIS.brain_ptv.name, 'Brain-Brainstem']:
      try:
        pm.RegionsOfInterest[name].OrganData.OrganType = "Other"
      except:
        pass
  
  
  # Adds rois that are common across all cases.
  def add_common_rois(self, pm, examination, site):
    # DL ROIs:
    examination.RunOarSegmentation(ModelName="RSL Head and Neck CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Brain", "Brainstem", "Cochlea_L", "Cochlea_R", "Eye_L", "Eye_R", "LacrimalGland_L", "LacrimalGland_R", "Lens_L", "Lens_R", "OpticChiasm", "OpticNerve_L", "OpticNerve_R", "OralCavity", "Parotid_L", "Parotid_R", "Pituitary", "SpinalCanal", "SubmandGland_L", "SubmandGland_R"])


  # Adds partial brain ROIs to the site object.
  def add_partial_brain(self, pm, examination, site):
    # Brain-Brainstem (used to aid in CTV definition):
    brain_brainstem = ROI.ROIAlgebra('Brain-Brainstem', ROIS.brain.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [ROIS.brainstem], operator = 'Subtraction')
    # Targets:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, sourcesA = [ROIS.gtv], sourcesB = [brain_brainstem], operator = 'Intersection', marginsA = MARGINS.uniform_20mm_expansion, marginsB = MARGINS.zero)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, sourcesA = [ctv], sourcesB = [ROIS.body], operator = 'Intersection', marginsA = MARGINS.uniform_3mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.gtv, ctv, ptv])
    # Derived OARs:
    brain_gtv = ROI.ROIAlgebra(ROIS.brain_gtv.name, ROIS.brain_gtv.type, ROIS.brain.color, sourcesA = [ROIS.brain], sourcesB = [ROIS.gtv], operator = 'Subtraction')
    brain_ptv = ROI.ROIAlgebra(ROIS.brain_ptv.name, ROIS.brain_ptv.type, ROIS.other_ptv.color, sourcesA = [ROIS.brain], sourcesB = [ptv], operator = 'Subtraction')
    # Non-DL OARs:
    site.add_oars([ROIS.brainstem_core, ROIS.brainstem_surface, ROIS.hippocampus_l, ROIS.hippocampus_r, ROIS.skin_brain_5, brain_brainstem, brain_gtv, brain_ptv])
  
  
  # Adds stereotactic brain ROIs to the site object.
  def add_stereotactic_brain(self, pm, examination, site, nr_targets):
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
        walls.append(ROI.ROIWall("zPTV"+str(i+1)+"_Wall", ROIS.z_ptv_wall.type, COLORS.wall, ptvs[-1], 1, 0))
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
    # Non-DL OARs:
    site.add_oars([ROIS.hippocampus_l, ROIS.hippocampus_r, ROIS.skin_srt, brain_gtv, brain_ptv] + walls)
  
  
  # Adds whole brain ROIs to the site object.
  def add_whole_brain(self, pm, examination, site, meninges):
    # Brain margin:
    if meninges == 'yes':
      brain_margin = MARGINS.uniform_1mm_expansion
    else:
      brain_margin = MARGINS.zero   
    # Targets:
    ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv, ROIS.brain, margins = brain_margin)
    ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv, ctv, margins = MARGINS.uniform_3mm_expansion)
    site.add_targets([ctv, ptv])
    # Non-DL OARs:
    site.add_oars([ROIS.skin_brain, ROIS.nasal_cavity])
    