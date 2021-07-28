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

# This class contains tests for the RayStation ROI object:
class TSROI(object):
  def __init__(self, roi, ts_case=None):
    # RayStation objects:
    self.roi = roi
    # Related test suite objects:
    self.ts_case = ts_case
    if ts_case:
      ts_case.ts_rois.append(self)
      self.parent_param = ts_case.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('ROI', self.roi.Name, self.parent_param) # (roi parameter)
    self.exclude_from_export = TEST.Parameter('Exclude from export', str(roi.ExcludeFromExport), self.param)


  # Tests if ROIs of type "Unknown" are excluded from export.
  def exclude_from_export_test(self):
    t = TEST.Test("Hjepestrukturer (ROIer med Organ type 'Unknown') skal være ekskludert fra eksport", True, self.exclude_from_export)
    # Perform test for ROIs of type Unknown:
    if self.roi.OrganData.OrganType == 'Unknown':
      if self.roi.ExcludeFromExport == True:
        return t.succeed()
      else:
        return t.fail(self.roi.ExcludeFromExport)
