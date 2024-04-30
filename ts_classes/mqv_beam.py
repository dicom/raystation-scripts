# encoding: utf8

# Contains tests for individual beams.
#

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST


# This class contains tests for the RayStation Beam object:
class MQVBeam(object):
  def __init__(self, beam, mqv_beam_set=None):
    # RayStation object:
    self.beam = beam
    # Mosaiq object:
    self.mq_beam = None
    # Related test suite objects:
    self.mqv_beam_set = mqv_beam_set
    self.mqv_segments = []
    if mqv_beam_set:
      mqv_beam_set.mqv_beams.append(self)
      self.parent_param = mqv_beam_set.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Felt', str(beam.Number), self.parent_param)
    self.nr = TEST.Parameter('Number', self.beam.Number, self.param)
    self.name = TEST.Parameter('Navn', '', self.param)
    self.mu = TEST.Parameter('MU', round(self.beam.BeamMU, 1), self.param)

  # Checks that there is a beam in Mosaiq with a number corresponding to this RayStation beam's number.
  def test_matching_beam_number(self):
    t = TEST.Test("Skal finnes en beam i dette beam-settet med forventet nr.", self.beam.Number, self.nr)
    if self.mq_beam:
      return t.succeed()
    else:
      return t.fail()
  
  # Comparison of meterset (MU).
  def test_mu(self):
    t = TEST.Test("Meterset", round(self.beam.BeamMU, 1), self.mu)
    # Proceed only on matching beam:
    if self.mq_beam:
      if round(self.beam.BeamMU, 1) == self.mq_beam.meterset:
        return t.succeed()
      else:
        return t.fail(self.mq_beam.meterset)
  
  # Comparison of name.
  def test_name(self):
    t = TEST.Test("Name", self.beam.Name, self.name)
    # Proceed only on matching beam:
    if self.mq_beam:
      if self.beam.Name == self.mq_beam.name:
        return t.succeed()
      else:
        return t.fail(self.mq_beam.name)
