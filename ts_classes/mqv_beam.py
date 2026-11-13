# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import test_p as TEST


class MQVBeam(object):
  '''This class contains tests for the RayStation Beam object.'''

  def __init__(self, beam, mqv_beam_set=None):
    '''Initializes the beam verification with the relevant RayStation instance.

    Args:
      beam (PyScriptObject): The RayStation Beam instance.
      mqv_beam_set (MQVBeamSet): The parent instance in the verification hierarchy. Defaults to None.
    '''
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
    self.energy = TEST.Parameter('Energi', self.beam.BeamQualityId, self.param)

  def test_matching_beam_number(self):
    '''Checks that there is a beam in Mosaiq with a number corresponding to this RayStation beam's number.'''
    t = TEST.Test("Skal finnes en beam i dette beam-settet med forventet nr.", self.beam.Number, self.nr)
    if self.mq_beam:
      return t.succeed()
    else:
      return t.fail()

  def test_mu(self):
    '''Comparison of meterset (MU).'''
    t = TEST.Test("Meterset", round(self.beam.BeamMU, 1), self.mu)
    # Proceed only on matching beam:
    if self.mq_beam:
      if round(self.beam.BeamMU, 1) == self.mq_beam.meterset:
        return t.succeed()
      else:
        return t.fail(self.mq_beam.meterset)

  def test_name(self):
    '''Comparison of name.'''
    t = TEST.Test("Name", self.beam.Name, self.name)
    # Proceed only on matching beam:
    if self.mq_beam:
      if self.beam.Name == self.mq_beam.name:
        return t.succeed()
      else:
        return t.fail(self.mq_beam.name)

  def test_energy(self):
    '''Comparison of energy (e.g. 6 or 10 MV).'''
    t = TEST.Test("Energy", self.beam.BeamQualityId, self.energy)
    # Proceed only on matching beam:
    if self.mq_beam:
      energy = self.beam.BeamQualityId
      energy = energy.replace(' FFF', '')
      if int(energy) == self.mq_beam.control_points()[0].energy:
        return t.succeed()
      else:
        return t.fail(self.mq_beam.control_points()[0].energy)

  def test_fff(self):
    '''Comparison of FFF (flattening filter free).'''
    t = TEST.Test("FFF", self.beam.BeamQualityId, self.energy)
    # Proceed only on matching beam:
    if self.mq_beam:
      fff = False
      if 'FFF' in self.beam.BeamQualityId:
        fff = True
      if fff == self.mq_beam.is_fff:
        return t.succeed()
      else:
        return t.fail(self.mq_beam.is_fff)
