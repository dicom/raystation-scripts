# encoding: utf8

# Contains treatment plan tests for individual segments.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
import itertools as it
#sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\RayStation\\lib".decode('utf8'))

# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *
from tkinter import messagebox

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

  # Tests validity of mlc corners.
  def mlc_corner_validity_test(self):
    t = TEST.Test("Skal ha hjørne-posisjoner som er leverbare på Elekta", True, self.mlc)
    violated = False
    # Agility/Versa HD:
    limits = [20.0 for i in range(80)]
    limits[0] = limits[79] = 16.1
    limits[1] = limits[78] = 16.7
    limits[2] = limits[77] = 17.3
    limits[3] = limits[76] = 17.8
    limits[4] = limits[75] = 18.3
    limits[5] = limits[74] = 18.8
    limits[6] = limits[73] = 19.2
    limits[7] = limits[72] = 19.7
 
    # Iterate leaf positions and check against limits:
    #for i in range(len(limits)):
    for i in it.chain(range(0, 7), range(72, 79)):
      if self.segment.LeafPositions[0][i] < -limits[i]:
        violated = True
      if self.segment.LeafPositions[1][i] > limits[i]:
        violated = True

    if violated:
      return t.fail(False)
    else:
      return t.succeed()


