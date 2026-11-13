# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import test_p as TEST


class TSSegment(object):
  '''This class contains tests for the RayStation Segment object.'''

  def __init__(self, segment, ts_beam=None):
    '''Initializes the Segment test suite with the relevant RayStation instance.

    Args:
      segment (PyScriptObject): The RayStation Segment instance.
      ts_beam (TSBeam): The parent beam test suite instance.
    '''
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
