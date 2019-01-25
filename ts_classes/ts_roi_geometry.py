# encoding: utf8

# Contains treatment plan tests for individual treatment plans.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
#sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\RayStation\\lib".decode('utf8'))

# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *

# Local script imports:
import test as TEST
import raystation_utilities as RSU
import ts_structure_set as SS

# This class contains tests for the RayStation Roi Geometry object:
class TSROIGeometry(object):
  def __init__(self, roi_geometry, ts_structure_set=None):
    # RayStation object:
    self.roi_geometry = roi_geometry
    # Related test suite objects:
    self.ts_structure_set = ts_structure_set
    if ts_structure_set:
      ts_structure_set.ts_roi_geometries.append(self)
      self.parent_param = ts_structure_set.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('ROI', '', self.parent_param)
    self.defined_roi = TEST.Parameter('Geometri', self.roi_geometry.OfRoi.Name.decode('utf8', 'replace'), self.param)
    self.updated_roi = TEST.Parameter('Geometri', self.roi_geometry.OfRoi.Name.decode('utf8', 'replace'), self.param)



#Tests if all ROI's are defined
  def defined_volume_test(self):
    t = TEST.Test("Regionen må ha definert volum", True, self.defined_roi)
    if self.ts_structure_set.structure_set == self.ts_structure_set.ts_case.ts_plan.plan.GetStructureSet():
      if self.roi_geometry.HasContours():
        return t.succeed()
      else:
        return t.fail()



#Tests if a ROI is updated when it is derived
  def derived_roi_geometry_is_updated_test(self):
    t = TEST.Test("Regionen må være oppdatert når den er avledet", True, self.updated_roi)
    if self.ts_structure_set.structure_set == self.ts_structure_set.ts_case.ts_plan.plan.GetStructureSet():
      if self.roi_geometry.PrimaryShape:
        # Is the referenced ROI derived?
        if self.roi_geometry.OfRoi.DerivedRoiExpression:
          # Is this ROI Geometry not updated?
          if not self.roi_geometry.PrimaryShape.DerivedRoiStatus:
            return t.fail()
          elif self.roi_geometry.PrimaryShape.DerivedRoiStatus.IsShapeDirty:
            return t.fail()
          else:
            return t.succeed()