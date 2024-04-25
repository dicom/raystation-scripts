# encoding: utf8

# Contains treatment plan tests for individual treatment plans.
#
# Verified for RayStation 10B.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import *
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
    # Cache attributes:
    self._bounding_box = None
    self._contours = None
    self._primary_shape = None
    self._roi = None
    # Parameters:
    self.param = TEST.Parameter('ROI', '', self.parent_param)
    self.defined_roi = TEST.Parameter('Geometri', self.roi().Name, self.param)
    self.updated_roi = TEST.Parameter('Geometri', self.roi().Name, self.param)


  # Gives the cached bounding box of the ROI geometry.
  def bounding_box(self):
    if not self._bounding_box:
     self._bounding_box = self.roi_geometry.GetBoundingBox()
    return self._bounding_box
  
  # Gives the cached primary shape of the ROI geometry.
  def contours(self):
    if not self._contours:
      try:
        self._contours = self.primary_shape().Contours
      except Exception:
        pass
    return self._contours
  
  # Gives the cached primary shape of the ROI geometry.
  def primary_shape(self):
    if not self._primary_shape:
     self._primary_shape = self.roi_geometry.PrimaryShape
    return self._primary_shape
  
  # Gives the cached ROI of the ROI geometry.
  def roi(self):
    if not self._roi:
     self._roi = self.roi_geometry.OfRoi
    return self._roi
  
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
    if self.primary_shape():
      # Is the referenced ROI derived?
      if self.roi().DerivedRoiExpression:
        # Is this ROI Geometry updated or not?
        if not self.primary_shape().DerivedRoiStatus:
          return t.succeed()
        elif self.primary_shape().DerivedRoiStatus.IsShapeDirty:
          return t.fail()
        else:
          return t.succeed()

  # Tests if there are any gaps (i.e. definition missing in one or more slices) in the geometry of a given ROI.
  def gaps_in_definition_test(self):
    t = TEST.Test("ROI-geometrien forventes å være sammenhengende definert (at den ikke inneholder tomme snitt innimellom definerte snitt)", None, self.defined_roi)    
    # For performance reasons, we choose to skip this test for External and Couch ROIs:
    if self.roi().Name not in ["External", "Couch"]:
      # Perform the test if indicated (ROI has contours and is not a derived ROI):
      if self.contours() and not self.primary_shape().DerivedRoiStatus:
        missing_slices = []
        # Extract all slices (z coordinates) where the ROI is defined:
        slices = []
        for slice in self.contours():
          slices.append(slice[0].z)
        # Determine unique slice positions and sort them:
        unique_slices = list(set(slices))
        unique_slices.sort()
        # Iterate the recorded slices to see if there are any gaps (i.e. a difference bigger than the slice thickness):
        for i in range(len(unique_slices)):
          if i > 0:
            gap = round(abs(unique_slices[i] - unique_slices[i-1]), 2)
            # If this gap is larger than slice thickness, then we have a missing slice:
            if gap > self.ts_structure_set.slice_thickness:
              missing_slices.append(round(unique_slices[i], 2))
        if len(missing_slices) > 0:
          return t.fail(str(missing_slices))
        else:
          return t.succeed()

  # Tests if a ROI geometry contains more than an expected nr of "islands" in any given axial slice of its contour.
  def max_nr_of_islands_in_slice_test(self):
    # ROIs which are to be tested, and their respective limit of nr of islands:
    limits = {
      "LN_Iliac": 2,
      "SeminalVes": 2
    }
    t = TEST.Test("ROIGeometri skal maks inneholde dette antall separate konturer i ethvert aksial-snitt", None, self.defined_roi)
    # Iterate the defines ROIs:
    for key in limits:
      # Only run test if the ROI Name matches:
      if self.roi().Name == key:
        # Set the expected value for this ROI:
        t.expected = "<="+str(limits[key])
        # Does the RoiGeometry actually have a shape?
        if self.primary_shape():
          # Store contour information in a dict:
          slices = {}
          if self.contours():
            # Iterate contours:
            for c in self.contours():
              z = str(round(c[0].z, 2))
              if slices.get(z):
                slices[z] += 1
              else:
                slices[z] = 1
          # Find deviating slices:
          deviations = {}
          for pair in slices.items():
            if pair[1] > limits[key]:
              deviations[pair[0]] = pair[1]
          # Determine result:
          if len(deviations) > 0:
            return t.fail(str(deviations))
          else:
            return t.succeed()
