# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import test_p as TEST


class TSROI(object):
  '''This class contains tests for the RayStation ROI object.'''

  def __init__(self, roi, ts_case=None):
    '''Initializes the ROI test suite with the relevant RayStation instance.

    Args:
      roi (PyScriptObject): The RayStation ROI instance.
      ts_case (TSCase): The parent case test suite instance.
    '''
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

  def exclude_from_export_test(self):
    '''Tests if ROIs of type "Unknown" are excluded from export.'''
    t = TEST.Test("Hjepestrukturer (ROIer med Organ type 'Unknown') skal være ekskludert fra eksport", True, self.exclude_from_export)
    # Perform test for ROIs of type Unknown:
    if self.roi.OrganData.OrganType == 'Unknown':
      if self.roi.ExcludeFromExport == True:
        return t.succeed()
      else:
        return t.fail(self.roi.ExcludeFromExport)
