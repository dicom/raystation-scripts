# encoding: utf8

# Contains treatment plan tests for individual segments.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
import itertools as it

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST
import raystation_utilities as RSU

# This class contains tests for the RayStation Segment object:
class TSSegment(object):
  def __init__(self, segment, ts_beam=None):
    # RayStation objects:
    self.segment = segment
    # Related test suite objects:
    self.ts_beam = ts_beam
    if ts_beam:
      ts_beam.ts_segments.append(self)
      self.parent_param = ts_beam.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Segment', str(segment.SegmentNumber), self.parent_param)
    self.mlc = TEST.Parameter('MLC', '', self.param)
