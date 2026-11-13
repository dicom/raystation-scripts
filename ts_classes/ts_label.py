# Import system libraries:
import sys
import re

# Import RayStation packages:
from connect import *

# Import local files:
import beam_set_label as BSL
import test_p as TEST


class TSLabel(object):
  '''This class contains tests for the RayStation Label object.'''

  def __init__(self, label, ts_beam_set=None):
    '''Initializes the beam set label test suite with the relevant RayStation instance.

    Args:
      label (str): The RayStation Label instance.
      ts_beam_set (TSBeamSet): The parent beam set test suite instance.
    '''
    # Label object (from beam set dicom plan label):
    self.label = BSL.BeamSetLabel(label)
    # Related test suite objects:
    self.ts_beam_set = ts_beam_set
    if ts_beam_set:
      ts_beam_set.ts_label = self
      self.parent_param = ts_beam_set.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Label', label, self.parent_param)

  def nr_parts_test(self):
    '''Tests the number of semi colon separated parts in the label.'''
    t = TEST.Test("Skal være 3 deler adskilt av kolon (eks '342V:70-78:4')", 3, self.param)
    if len(self.label.parts) == 3:
      return t.succeed()
    else:
      return t.fail(len(self.label.parts))

  def nr_fractions_test(self):
    '''Tests that nr of fractions is specified in the last part of the label.'''
    t = TEST.Test("Siste del skal være heltall for antall fraksjoner (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if self.label.nr_fractions:
        return t.succeed()
      else:
        return t.fail(self.label.nr_fractions)

  def technique_test(self):
    '''Tests that technique has been properly coded with a letter.'''
    t = TEST.Test("Siste tegn av første del skal være en bokstav for plan-teknikk (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if self.label.technique:
        return t.succeed()
      else:
        return t.fail(self.label.technique)

  def region_test(self):
    '''Tests that region has been properly coded with a 1-3 digit integer.'''
    t = TEST.Test("Første del (av første del) skal være et heltall for regionkode (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if self.label.region:
        return t.succeed()
      else:
        return t.fail(self.label.region)

  def middle_part_separator_test(self):
    '''Tests that the middle part contains a separator "-".'''
    t = TEST.Test("Midterste del skal inneholde to deler adskilt av bindestrek (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if len(self.label.middle_parts) == 2:
        return t.succeed()
      else:
        return t.fail(len(self.label.middle_parts))

  def middle_part_doses_test(self):
    '''Tests that the middle part contains start and stop dose.'''
    t = TEST.Test("Midterste del skal inneholde start- og slutt-doser (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if len(self.label.middle_parts) == 2:
        if re.match("^\d+\.\d+$", self.label.start_dose_str) is None and not self.label.start_dose_str.isdigit():
          return t.fail(self.label.start_dose_str)
        elif re.match("^\d+\.\d+$", self.label.end_dose_str) is None and not self.label.end_dose_str.isdigit():
          return t.fail(self.label.end_dose_str)
        else:
          return t.succeed()
