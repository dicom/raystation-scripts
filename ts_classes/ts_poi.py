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

# This class contains tests for the RayStation POI object:
class TSPOI(object):
  def __init__(self, poi, ts_case=None):
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

