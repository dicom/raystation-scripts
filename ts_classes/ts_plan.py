# encoding: utf8

# Contains treatment plan tests for individual treatment plans.
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
import structure_set_functions as SSF
import rois as ROIS
import region_codes as RC

# This class contains tests for the RayStation TreatmentPlan object:
class TSPlan(object):
  def __init__(self, plan, ts_case=None):
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


  # Tests if all expected breast OARs are defined, except 'A_LAD' for right sided breast, and contralateral breast for conventional treatment (ie. not VMAT).
  # FIXME: Have a look at this function sometime...
  def breast_oar_defined_test(self):
    failed_geometries = []
    t = TEST.Test("Regionen må ha definert volum:", True, self.defined_roi)
    t.expected = None
    ss = self.ts_beam_sets[0].ts_structure_set().structure_set
    roi_not_contours_dict = SSF.create_roi_dict_not_contours(ss)
    roi_and_region_dict = {ROIS.a_lad.name: RC.breast_r_codes, ROIS.breast_r_draft.name: RC.breast_l_codes, ROIS.breast_r.name: RC.breast_l_codes, ROIS.breast_l.name :RC.breast_r_codes}
    if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region:
      for key, value in roi_and_region_dict.items():
        if roi_not_contours_dict.get(key) and self.ts_beam_sets[0].ts_label.label.region in value:
          del roi_not_contours_dict[key]
    structure_sets = self.ts_case.case.PatientModel.StructureSets
    for i in range(len(structure_sets)):
      if structure_sets[i].OnExamination.Name != self.ts_beam_sets[0].ts_structure_set().structure_set.OnExamination.Name:
        roi = structure_sets[i].RoiGeometries
        for j in range(len(roi)):
          if roi[j].HasContours() and roi_not_contours_dict.get(roi[j].OfRoi.Name):
            del roi_not_contours_dict[roi[j].OfRoi.Name]
    if len(roi_not_contours_dict.keys()) >= 1:
      return t.fail(list(roi_not_contours_dict.keys()))
    else:
      return t.succeed()


  # Tests if the same localization point is not placed in the first or last CT slice of the examination.
  def localization_point_not_in_first_or_last_slice_test(self):
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


  # Tests the presence of a planned by label.
  def planned_by_test(self):
    t = TEST.Test('Doseplanleggerens initialer bør være fylt inn her (Planned by)', True, self.planned_by)
    if self.plan.PlannedBy:
      return t.succeed()
    else:
      return t.fail()


  # Tests that beam numbers are not repeated among beam sets in the treatment plan.
  def unique_beam_numbers_test(self):
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
