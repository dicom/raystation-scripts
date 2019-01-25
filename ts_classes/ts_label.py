# encoding: utf8

# Contains treatment plan tests for individual beam set labels.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
import re
#sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\RayStation\\lib".decode('utf8'))

# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *

# Local script imports:
import test as TEST
import beam_set_label as BSL
#import raystation_utilities as RSU

# This class contains tests for the RayStation Label object:
class TSLabel(object):
  def __init__(self, label, ts_beam_set=None):
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


  # Tests the number of semi colon separated parts in the label.
  def nr_parts_test(self):
    t = TEST.Test("Skal være 3 deler adskilt av kolon (eks '342V:70-78:4')", 3, self.param)
    if len(self.label.parts) == 3:
      return t.succeed()
    else:
      return t.fail(len(self.label.parts))

  # Tests that nr of fractions is specified in the last part of the label.
  def nr_fractions_test(self):
    t = TEST.Test("Siste del skal være heltall for antall fraksjoner (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if self.label.nr_fractions:
        return t.succeed()
      else:
        return t.fail(self.label.nr_fractions)

  # Tests that technique has been properly coded with a letter.
  def technique_test(self):
    t = TEST.Test("Siste tegn av første del skal være en bokstav for plan-teknikk (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if self.label.technique:
        return t.succeed()
      else:
        return t.fail(self.label.technique)

  # Tests that region has been properly coded with a 1-3 digit integer.
  def region_test(self):
    t = TEST.Test("Første del (av første del) skal være et heltall for regionkode (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if self.label.region:
        return t.succeed()
      else:
        return t.fail(self.label.region)

  # Tests that the middle part contains a separator '-'.
  def middle_part_separator_test(self):
    t = TEST.Test("Midterste del skal inneholde to deler adskilt av bindestrek (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if len(self.label.middle_parts) == 2:
        return t.succeed()
      else:
        return t.fail(len(self.label.middle_parts))

  # Tests that the middle part contains start and stop dose.
  def middle_part_doses_test(self):
    t = TEST.Test("Midterste del skal inneholde start- og slutt-doser (eks '342V:70-78:4')", True, self.param)
    if len(self.label.parts) == 3:
      if len(self.label.middle_parts) == 2:
        if re.match("^\d+\.\d+$", self.label.start_dose_str) is None and not self.label.start_dose_str.isdigit():
          return t.fail(self.label.start_dose_str)
        elif re.match("^\d+\.\d+$", self.label.end_dose_str) is None and not self.label.end_dose_str.isdigit():
          return t.fail(self.label.end_dose_str)
        else:
          return t.succeed()




