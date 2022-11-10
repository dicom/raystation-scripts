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
    # OARs:
    site.add_oars(DEF.bladder_oars)
    # Create all targets and OARs in RayStation:
    site.create_rois()
