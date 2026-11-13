# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import test_p as TEST


class TSPOI(object):
  '''This class contains tests for the RayStation POI object.'''

  def __init__(self, poi, ts_case=None):
    '''Initializes the POI test suite with the relevant RayStation instance.

    Args:
      poi (PyScriptObject): The RayStation POI instance.
      ts_case (TSCase): The parent case test suite instance.
    '''
    # RayStation object:
    self.poi = poi
    # Related test suite objects:
    self.ts_case = ts_case
    if ts_case:
      ts_case.ts_pois.append(self)
      self.parent_param = ts_case.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('POI', self.poi.Name, self.parent_param) # (poi parameter)
