# encoding: utf8

# Contains treatment plan tests for the optimization settings.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST
import raystation_utilities as RSU
import region_codes as RC

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
    self.parameter = TEST.Parameter('Parameter', '', self.param)
    self.grid = TEST.Parameter('Beregningsmatrise', '', self.param)


  # Tests if Constrain leaf motion of 0.3 cm/deg is used for stereotactic plans.
  def constrain_leaf_motion_test(self):
    t = TEST.Test("Skal i utgangspunktet bruke Constrain leaf motion <= 0.3 cm/deg", True, self.parameter)
    match = True
    arc_properties = self.optimization.OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties
    if self.ts_beam_set.ts_label.label.technique:
      if self.ts_beam_set.ts_label.label.technique.upper() == 'S':
        if arc_properties.UseMaxLeafTravelDistancePerDegree:
          if arc_properties.MaxLeafTravelDistancePerDegree > 0.3:
            match = False
        else:
          match = False
    if match:
      return t.succeed()
    else:
      return t.fail()

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

  def dose_grid_test(self):
    correct_grid = 0.3
    match = True
    grid = self.optimization.OptimizationParameters.TreatmentSetupSettings[0].ForTreatmentSetup.FractionDose.InDoseGrid.VoxelSize
    if self.ts_beam_set.ts_label.label.technique:
      if self.ts_beam_set.ts_label.label.technique.upper() == 'S' and self.ts_beam_set.ts_label.label.region in RC.brain_partial_codes:
        if grid.x != 0.1 or grid.y != 0.1 or grid.z != 0.1:
          correct_grid = 0.1
          match = False
      elif self.ts_beam_set.ts_label.label.region in RC.brain_partial_codes or self.ts_beam_set.ts_label.label.region in RC.prostate_codes or self.ts_beam_set.ts_label.label.technique.upper() == 'S' and self.ts_beam_set.ts_label.label.region in RC.lung_codes:
        if grid.x != 0.2 or grid.y != 0.2 or grid.z != 0.2:
          correct_grid = 0.2
          match = False
      elif grid.x != 0.3 or grid.y != 0.3 or grid.z != 0.3:
        correct_grid = 0.3
        match = False
        
    t = TEST.Test("Skal i utgangspunktet bruke dosegrid: " + str(correct_grid)+"x"+str(correct_grid)+"x"+str(correct_grid)+" cm^3", True, self.grid)
    if match:
      return t.succeed()
    else:
      return t.fail(grid.x)

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
          return et.fail(str(external_fails))
        else:
          return et.succeed()
        if len(oar_fails) > 0:
          return ot.fail(str(len(oar_fails)) + ": " + str(oar_fails))
        else:
          return ot.succeed()
        if len(target_fails) > 0:
          return tt.fail(str(len(target_fails)) + ": " + str(target_fails))
        else:
          return tt.succeed()




