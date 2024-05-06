# encoding: utf8

# Contains treatment plan tests for individual segments.
#

# System configuration:
from connect import *
import sys
from struct import *

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST


# This class contains tests for the RayStation Segment object:
class MQVSegment(object):
  def __init__(self, segment, mqv_beam=None):
    # RayStation objects:
    self.segment = segment
    # Mosaiq object:
    self.mq_segment = None
    # Related test suite objects:
    self.mqv_beam = mqv_beam
    if mqv_beam:
      mqv_beam.mqv_segments.append(self)
      self.parent_param = mqv_beam.param
    else:
      self.parent_param = None
    # Process gantry angle:
    gantry_angle = self.mqv_beam.beam.GantryAngle
    if hasattr(segment, 'DeltaGantryAngle'):
      gantry_angle += segment.DeltaGantryAngle
    # Parameters:
    self.param = TEST.Parameter('Segment', str(segment.SegmentNumber), self.parent_param)
    self.nr = TEST.Parameter('Number', int(segment.SegmentNumber), self.param)
    self.collimator_angle = TEST.Parameter('Collimator Angle', segment.CollimatorAngle, self.param)
    self.jaw_positions = TEST.Parameter('Jaw Positions', "", self.param)
    self.gantry_angle = TEST.Parameter('Gantry Angle', self.format_angle(gantry_angle), self.param)
    self.relative_weight = TEST.Parameter('Relative Weight', round(segment.RelativeWeight, 4), self.param)
    self.leaf_bank1 = TEST.Parameter('Leaf Bank 1', "", self.param)
    self.leaf_bank2 = TEST.Parameter('Leaf Bank 1', "", self.param)

  # Formats the angle value between 0 and 360:
  def format_angle(self, angle):
    if angle > 360:
      return round(angle - 360, 1)
    elif angle < 0:
      return round(360 + angle, 1)
    elif round(angle, 1) == 360:
      return 0
    else:
      return round(angle, 1)
  
  # Checks that there is a segment in Mosaiq with a number corresponding to this RayStation segment's number.
  def test_matching_segment_number(self):
    t = TEST.Test("Skal finnes et segment i dette feltet med forventet nr.", self.segment.SegmentNumber, self.nr)
    if self.mq_segment:
      return t.succeed()
    else:
      return t.fail()

  # Comparison of collimator angle.
  def test_collimator_angle(self):
    t = TEST.Test("Collimator angle", round(self.segment.CollimatorAngle, 1), self.collimator_angle)
    # Proceed only on matching segment:
    if self.mq_segment:
      if round(self.segment.CollimatorAngle, 1) == round(self.mq_segment.collimator_angle, 1):
        return t.succeed()
      else:
        return t.fail(self.mq_segment.collimator_angle)
  
  # Comparison of jaw positions.
  def test_jaw_positions(self):
    t = TEST.Test("Jaw positions", None, self.jaw_positions)
    # Proceed only on matching segment:
    if self.mq_segment:
      jp = [float('%.2f' % element) for element in [self.segment.JawPositions[0], self.segment.JawPositions[1], self.segment.JawPositions[2], self.segment.JawPositions[3]]]
      mq_jp = [float('%.2f' % element) for element in [self.mq_segment.collimator_x1, self.mq_segment.collimator_x2, self.mq_segment.collimator_y1, self.mq_segment.collimator_y2]]
      t.expected = jp
      if jp == mq_jp:
        return t.succeed()
      else:
        return t.fail(mq_jp)
  
  # Comparison of gantry angle.
  def test_gantry_angle(self):
    t = TEST.Test("Gantry angle", self.gantry_angle.value, self.gantry_angle)
    # Proceed only on matching segment:
    if self.mq_segment:
      mq_gantry_angle = round(float(self.mq_segment.gantry_angle), 1)
      # Tolerate a discrepancy of 0.2 degrees (to account for rounding issues, etc):
      if abs(self.gantry_angle.value - mq_gantry_angle) < 0.2:
        return t.succeed()
      else:
        return t.fail(mq_gantry_angle)
  
  # Comparison of relative weight (MU).
  def test_relative_weight(self):
    t = TEST.Test("Relative weight", self.relative_weight.value, self.relative_weight)
    # Proceed only on matching segment:
    if self.mq_segment:
      # Proceed only if this is not the last segment (subtract 2 because index is one less than length):
      nr = int(self.segment.SegmentNumber)
      if nr < len(self.mqv_beam.mqv_segments) - 2:
        # Proceed only if also the next raystation segment instance has a matching mosaiq segment:
        next_segment = self.mqv_beam.mqv_segments[nr+1].mq_segment
        if next_segment:
          # In RayStation segments, relative weights are stored on each segments, with the last segment having a zero value.
          # In Mosaiq segments, a cumulative percentage value is stored, with the first segment having zero and the last segment 100.
          mq_relative_weight = round(float(next_segment.index - self.mq_segment.index) * 0.01, 4)
          # Tolerate a discrepancy of 0.0002 (to account for rounding issues, etc):
          if abs(self.relative_weight.value - mq_relative_weight) < 0.0002:
            return t.succeed()
          else:
            return t.fail(mq_relative_weight)
  
  # Comparison of leaf positions in leaf bank 1.
  def test_positions_leaf_bank1(self):
    t = TEST.Test("Leaf bank 1", None, self.leaf_bank1)
    # Proceed only on matching segment:
    if self.mq_segment:
      # RayStation leaf bank positions:
      rs_lp1 = [round(element, 2) for element in self.segment.LeafPositions[0]] 
      # Mosaiq leaf bank position binary strings:
      mq_lp1_str = self.mq_segment.leaf_bank1 # (A binary string consisting of 100 signed short integers, where the first 80 are actual leaf values.)
      # Mosaiq leaf bank positions (integers multiplied by 100):
      mq_lp1_int = unpack('h'*100, mq_lp1_str)[0:79]
      # Mosaiq leaf bank positions (proper floats):
      mq_lp1 = [round(element / 100.0, 2) for element in mq_lp1_int]
      # Absolute difference between the two lists:
      diff1 = [abs(round(rs_lp1[i]-mq_lp1[i], 2)) for i in range(min(len(rs_lp1), len(mq_lp1)))]
      # Store the expected value (reformatted to values with two decimals):
      t.expected = str([float('%.2f' % element) for element in rs_lp1])
      # Iterate results to see if there is a discrepancy:
      succeed = True
      for d in diff1:
        # Tolerate a discrepancy of 0.02 mm (to account for some apparent observed rounding issues between RayStation and Mosaiq):
        if d > 0.02:
          succeed = False
      # Register the result:
      if succeed:
        return t.succeed()
      else:
        return t.fail(str(mq_lp1))
  
# Comparison of leaf positions in leaf bank 2.
  def test_positions_leaf_bank2(self):
    t = TEST.Test("Leaf bank 2", None, self.leaf_bank2)
    # Proceed only on matching segment:
    if self.mq_segment:
      # RayStation leaf bank positions:
      rs_lp2 = [round(element, 2) for element in self.segment.LeafPositions[1]] 
      # Mosaiq leaf bank position binary strings:
      mq_lp2_str = self.mq_segment.leaf_bank2 # (A binary string consisting of 100 signed short integers, where the first 80 are actual leaf values.)
      # Mosaiq leaf bank positions (integers multiplied by 100):
      mq_lp2_int = unpack('h'*100, mq_lp2_str)[0:79]
      # Mosaiq leaf bank positions (proper floats):
      mq_lp2 = [round(element / 100.0, 2) for element in mq_lp2_int]
      # Absolute difference between the two lists:
      diff2 = [abs(round(rs_lp2[i]-mq_lp2[i], 2)) for i in range(min(len(rs_lp2), len(mq_lp2)))]
      # Store the expected value (reformatted to values with two decimals):
      t.expected = str([float('%.2f' % element) for element in rs_lp2])
      # Iterate results to see if there is a discrepancy:
      succeed = True
      for d in diff2:
        # Tolerate a discrepancy of 0.02 mm (to account for some apparent observed rounding issues between RayStation and Mosaiq):
        if d > 0.02:
          succeed = False
      # Register the result:
      if succeed:
        return t.succeed()
      else:
        return t.fail(str(mq_lp2))  
  