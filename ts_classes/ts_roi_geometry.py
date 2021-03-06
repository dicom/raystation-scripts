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

  # Tests if there are any gaps (i.e. definition missing in one or more slices) in the geometry of a given ROI.
  def gaps_in_definition_test(self):
    t = TEST.Test("ROI-geometrien forventes å være sammenhengende definert (at den ikke inneholder tomme snitt innimellom definerte snitt)", None, self.defined_roi)    
    # We are only able to test this if there actually are contours (e.q. it is not a derived ROI geometry):
    try:
      contours = self.roi_geometry.PrimaryShape.Contours
    except Exception:
      contours = None
    if contours:
      missing_slices = []
      # Extract all slices (z coordinates) where the ROI is defined:
      slices = []
      for slice in self.roi_geometry.PrimaryShape.Contours:
        slices.append(slice[0].z)
      # Determine unique slice positions and sort them:
      unique_slices = list(set(slices))
      unique_slices.sort()
      # Iterate the recorded slices to see if there are any gaps (i.e. a difference bigger than the slice thickness):
      for i in range(len(unique_slices)):
        if i > 0:
          gap = round(abs(unique_slices[i] - unique_slices[i-1]), 1)
          # If this gap is larger than slice thickness, then we have a missing slice:
          if gap > self.ts_structure_set.slice_thickness:
            missing_slices.append(round(unique_slices[i], 1))
      if len(missing_slices) > 0:
        return t.fail(str(missing_slices))
      else:
        return t.succeed()
