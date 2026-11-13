# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import raystation_utilities as RSU
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF
import test_p as TEST


class TSPlan(object):
  '''This class contains tests for the RayStation TreatmentPlan object.'''

  def __init__(self, plan, ts_case=None):
    '''Initializes the plan test suite with the relevant RayStation instance.

    Args:
      plan (PyScriptObject): The RayStation TreatmentPlan instance.
      ts_case (TSCase): The parent case test suite instance.
    '''
    # RayStation objects:
    self.plan = plan
    # Related test suite objects:
    self.ts_case = ts_case
    self.ts_beam_sets = []
    if ts_case:
      ts_case.ts_plan = self
      self.parent_param = ts_case.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Plan', self.plan.Name, self.parent_param)
    self.planned_by = TEST.Parameter('Planlagt av', self.plan.PlannedBy, self.param)
    self.isocenter = TEST.Parameter('Isocenter', '', self.param)
    self.numbers = TEST.Parameter('Beam numbers', '', self.param)
    self.defined_roi = TEST.Parameter('Geometri','', self.param)
    self.localization_point = TEST.Parameter('REF', '', self.param)

  def localization_point_not_in_first_or_last_slice_test(self):
    '''Tests if the localization point is not placed in the first or last CT slice of the examination.'''
    t = TEST.Test("Referansepunkt skal (normalt) ikke være plassert i første eller siste snitt (dette er gjerne en indikasjon på at det kan være satt feil)", True, self.localization_point)
    points = []
    bs = self.plan.BeamSets[0]
    if bs:
      ss = bs.GetStructureSet()
      # Examination bounding box:
      bbox = ss.OnExamination.Series[0].ImageStack.GetBoundingBox()
      # Determine localization point geometry:
      for pg in ss.PoiGeometries:
        if pg.OfPoi.Type == 'LocalizationPoint':
          if pg.Point:
            slice_pos = pg.Point.z
            # Check if it is at the image stack boundary:
            if slice_pos == bbox[0].z or slice_pos == bbox[1].z:
              return t.fail()
            else:
              return t.succeed()

  def planned_by_test(self):
    '''Tests the presence of a "planned by" label.'''
    t = TEST.Test('Doseplanleggerens initialer bør være fylt inn her (Planned by)', True, self.planned_by)
    if self.plan.PlannedBy:
      return t.succeed()
    else:
      return t.fail()

  def unique_beam_numbers_test(self):
    '''Tests that beam numbers are not repeated among beam sets in the treatment plan.'''
    t = TEST.Test("Skal være unik for alle felt i planen", True, self.numbers)
    beam_numbers = set([])
    has_duplicate_beam_nr = False
    for beam_set in self.plan.BeamSets:
      for beam in beam_set.Beams:
        if beam.Number in beam_numbers:
          has_duplicate_beam_nr = beam
        else:
          beam_numbers.add(beam.Number)
    if has_duplicate_beam_nr:
      return t.fail(has_duplicate_beam_nr.Number)
    else:
      return t.succeed()
