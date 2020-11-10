# encoding: utf8

# Contains treatment plan tests for individual treatment plans.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST
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
    self.defined_roi = TEST.Parameter('Geometri', self.roi_geometry.OfRoi.Name, self.param)
    self.updated_roi = TEST.Parameter('Geometri', self.roi_geometry.OfRoi.Name, self.param)


  # Tests if all ROIs are defined.
  def defined_volume_test(self):
    t = TEST.Test("Regionen må ha definert volum", True, self.defined_roi)
    if self.roi_geometry.HasContours():
      return t.succeed()
    else:
      return t.fail()

  # Tests if a ROI is updated when it is derived.
  def derived_roi_geometry_is_updated_test(self):
    t = TEST.Test("Regionen må være oppdatert når den er avledet", True, self.updated_roi)
    # Does the RoiGeometry have a shape?
    if self.roi_geometry.PrimaryShape:
      # Is the referenced ROI derived?
      if self.roi_geometry.OfRoi.DerivedRoiExpression:
        # Is this ROI Geometry updated or not?
        if not self.roi_geometry.PrimaryShape.DerivedRoiStatus:
          return t.succeed()
        elif self.roi_geometry.PrimaryShape.DerivedRoiStatus.IsShapeDirty:
          return t.fail()
        else:
          return t.succeed()
