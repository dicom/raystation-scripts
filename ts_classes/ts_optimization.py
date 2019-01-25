# encoding: utf8

# Contains treatment plan tests for the optimization settings.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys


# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *

# Local script imports:
import test as TEST
import raystation_utilities as RSU

# This class contains tests for the RayStation Optimization object:
class TSOptimization(object):
  def __init__(self, optimization, ts_beam_set=None):
    # RayStation object:
    self.optimization = optimization
    # Related test suite objects:
    self.ts_beam_set = ts_beam_set
    if ts_beam_set:
      ts_beam_set.ts_optimization = self
      self.parent_param = ts_beam_set.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Optimalisering', '', self.parent_param)
    self.background_dose = TEST.Parameter('Bakgrunnsdose', '', self.param)
    self.mu = TEST.Parameter('MU', '', self.param)


  # Tests for presence of constraints.
  def constraints_test(self):
    t = TEST.Test("Det skal i utgangspunktet ikke brukes constraints (det er mer effektivt og presist å bruke objectives - eventuelt med høy vekt for å simulere en constraint)", None, self.param)
    # Check for presence of constraints:
    constraints = []
    for c in self.optimization.Constraints:
      constraints.append(c.ForRegionOfInterest.Name)
    if len(constraints) > 0:
      return t.fail(str(constraints))
    else:
      return t.succeed()

  # Tests for proper usage of background dose for three kinds of ROIs: Target volume, external and organ.
  # Our expectation is that background dose is used on OARs, but not on targets or external volumes.
  def objectives_background_dose_test(self):
    et = TEST.Test("Det skal normalt ikke brukes 'Beam Set + Background' på external-objectives for beam sets basert på background dose.", 0, self.background_dose)
    ot = TEST.Test("Det skal normalt brukes 'Beam Set + Background' på alle risikorgan-objectives for beam sets som basert på background dose.", 0, self.background_dose)
    tt = TEST.Test("Det skal normalt ikke brukes 'Beam Set + Background' på målvolum-objectives for beam sets basert på background dose.", 0, self.background_dose)
    # Array of failed objectives in the 3 categories:
    external_fails = 0
    oar_fails = []
    target_fails = []
    if self.optimization.BackgroundDose:
      if self.optimization.Objective:
        for obj in self.optimization.Objective.ConstituentFunctions:
          # An objective is based on background dose if there is no OfDoseDistribution.ForBeamSet defined!
          if obj.ForRegionOfInterest.Type == 'External':
            if not hasattr(obj.OfDoseDistribution, 'ForBeamSet'): #if obj.OfDoseDistribution.ForBeamSet: # (This more 'normal' code failed to work in this case)
              external_fails += 1
          elif obj.ForRegionOfInterest.Type == 'Organ':
            if hasattr(obj.OfDoseDistribution, 'ForBeamSet'):
              oar_fails.append(obj.ForRegionOfInterest.Name)
          elif obj.ForRegionOfInterest.Type in ('Gtv', 'Ctv', 'Ptv'):
            if not hasattr(obj.OfDoseDistribution, 'ForBeamSet'):
              target_fails.append(obj.ForRegionOfInterest.Name)
        if external_fails > 0:
          return t.fail(str(external_fails))
        else:
          return t.succeed()
        if len(oar_fails) > 0:
          return t.fail(str(len(oar_fails)) + ": " + str(oar_fails))
        else:
          return t.succeed()
        if len(target_fails) > 0:
          return t.fail(str(len(target_fails)) + ": " + str(target_fails))
        else:
          return t.succeed()
'''
# Tests if a constraint is set for the maximum number of MU per beam, and if it is lower than 1.4 times the fraction dose
  def stereotactic_mu_constraints(self):
    t = TEST.Test("Skal i utgangspunktet bruke begrensninger på antall MU per bue <= 1.4*fraksjonsdose (cGy).", True, self.mu)
    if self.ts_beam_set.beam_set.Prescription.PrimaryDosePrescription:
      if self.ts_beam_set.ts_label.label.technique:
        if self.ts_beam_set.ts_label.label.technique.upper() == 'S':
          if self.ts_beam_set.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[0].ArcConversionPropertiesPerBeam.MaxArcMU:
            for index, beam in enumerate(self.ts_beam_set.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings):
              beam_start = 0
              beam_stop = 0
              beam_length = 0
              total_beam_length = 0
              for beam in self.ts_beam_set.beam_set.Beams:
                beam_start = beam.GantryAngle
                beam_stop = beam.ArcStopGantryAngle
                if beam_start > 180:
                  total_beam_length += 360 - beam_start
                else:
                  total_beam_length += beam_start
                if beam_stop > 180:
                  total_beam_length += 360 - beam_stop
                else:
                  total_beam_length += beam_stop

              beam_start = self.beam.GantryAngle
              beam_stop = self.beam.ArcStopGantryAngle
              if beam_start > 180:
                beam_length += 360 - beam_start
              else:
                beam_length += beam_start
              if beam_stop > 180:
                beam_length += 360 - beam_stop
              else:
                beam_length += beam_stop
              t.expected = "<" + str(round((beam_length/total_beam_length)*RSU.fraction_dose(self.ts_beam_set.beam_set) * 140))
              if self.beam.BeamMU > (beam_length/total_beam_length)*RSU.fraction_dose(self.ts_beam_set.beam_set) * 140 *1.15:

              if self.ts_beam_set.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[index].ArcConversionPropertiesPerBeam.MaxArcMU <= ((beam_length/total_beam_length)*RSU.fraction_dose(self.ts_beam_set.beam_set) * 140):
                return t.succeed()
              else:
                return t.fail(self.ts_beam_set.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[index].ArcConversionPropertiesPerBeam.MaxArcMU)
'''






