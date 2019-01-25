# encoding: utf8

# Contains treatment plan tests for individual segments.
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

  # Tests validity of mlc corners.
  def mlc_corner_validity_test(self):
    t = TEST.Test("Skal ha hjørne-posisjoner som er leverbare på Elekta", True, self.mlc)
    mlc_violation = RSU.check_mlc_corners(self.segment)
    if mlc_violation:
      return t.fail(False)
    else:
      return t.succeed()


