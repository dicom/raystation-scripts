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
    site.add_oars(DEF.bladder_oars)
    ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_low, sourcesA=[ROIS.gtv], sourcesB=[ROIS.bladder])
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.gtv, ctv, ptv])
    # Create all targets and OARs in RayStation:
    site.create_rois()
