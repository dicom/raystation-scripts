# encoding: utf8

# Contains tests for the case object.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
import math

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST
import region_codes as RC
import rois as ROIS
#import raystation_utilities as RSU

# This class contains tests for the RayStation Case object:
class TSCase(object):
  def __init__(self, case, ts_patient=None):
    # RayStation object:
    self.case = case
    # Related test suite objects:
    self.ts_patient = ts_patient
    self.ts_plan = None
    self.ts_pois = []
    self.ts_rois = []
    self.ts_structure_sets = []
    if ts_patient:
      ts_patient.ts_case = self
      self.parent_param = ts_patient.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Case', self.case.CaseName, self.parent_param)
    self.localization_point = TEST.Parameter('REF', '', self.param)
    self.examination = TEST.Parameter('Examination', '', self.param)

    # Attributes:
    self.has_target_volume = self.target_volume()




  # Determines if a target volume is defined in the case.
  def target_volume(self):
    match = False
    for roi in self.case.PatientModel.RegionsOfInterest:
      if roi.Type in ('Gtv', 'Ctv', 'Ptv'):
       match = True
    return match

  
  # Tests if a POI exists for specifying where the breath measurement point is.
  def breath_measurement_point_for_lung_sbrt_test(self):
    t = TEST.Test("For lunge stereotaksi (som behandles i DIBH) skal det finnes en 'Pust' POI for markering av målepunkt for pustebevegelse", True, self.param)
    # Only relevant to run this test for lung region and stereotactic treatment:
    if self.ts_plan.ts_beam_sets[0].ts_prescription.is_stereotactic() and self.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.lung_codes:
      match = False
      for poi in self.case.PatientModel.PointsOfInterest:
        if poi.Name == 'Pust' or poi.Name == 'PUST':
          match = True
      if match:
        return t.succeed()
      else:
        return t.fail()
  
  # Tests if the breath measurement point is not too far offset from the isocenter.
  # (such that it falls in the shadow of the gantry from the Catalyst camera's point of view)
  def breath_measurement_point_not_in_gantry_shadow_for_lung_sbrt_test(self):
    t = TEST.Test("For lunge stereotaksi (som behandles i DIBH) bør avstanden mellom isocenter og 'Pust' POIen ikke være såpass stor at pustepunktet kommer i skyggen av gantry (fra Catalyst kameraet sitt synspunkt)", True, self.param)
    # Only relevant to run this test for lung region and stereotactic treatment:
    if self.ts_plan.ts_beam_sets[0].ts_prescription.is_stereotactic() and self.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.lung_codes:
      match = False
      for poi in self.case.PatientModel.PointsOfInterest:
        if poi.Name == 'Pust' or poi.Name == 'PUST':
          match = True
      if match:
        # The POI exists. Proceed to test the geometry between the POI and the isocenter:
        # Isocenter:
        iso = self.ts_plan.ts_beam_sets[0].ts_beams[0].beam.Isocenter.Position
        ss = self.ts_plan.ts_beam_sets[0].beam_set.GetStructureSet()
        for poi in ss.PoiGeometries:
          if poi.OfPoi.Name == 'Pust' or poi.OfPoi.Name == 'PUST':
            # Set (max/expected) breathing amplitude (cm):
            amplitude = 2
            # Catalyst camera angle:
            angle = 60
            # Maximum (realistic) catalyst height:
            max = 22
            # Catalyst realistic field of view along iso:
            iso_real_fov = max * math.tan(math.radians(angle))
            # Calculate difference in the height and long directions:
            delta_height = abs(iso.y - poi.Point.y)
            delta_long = poi.Point.z - iso.z
            # Catalyst realistic field of view at breath measurement point: 
            breath_real_fov = (iso_real_fov - delta_long) / math.tan(math.radians(angle))
            delta_height_dibh = delta_height + amplitude
            if delta_height_dibh > breath_real_fov:
              t.expected = "<" + str(round(breath_real_fov, 1))
              return t.fail(round(delta_height_dibh, 1))
            else:
              return t.succeed()
  
  # For DIBH cases, tests that there are at least 2 DIBH control examinations present.
  def dibh_control_examinations_present_on_dibh_case_test(self):
    t = TEST.Test("DIBH-planer skal ha minst to 'DIBH Kontroll' serier til stede i casen", ">=2", self.param)
    # Only relevant to run this test if the planning CT name includes 'DIBH':
    ce = get_current("Examination")
    if 'DIBH' in ce.Name.upper():
      # The DIBH test is only relevant for non-breast cases:
      if self.ts_plan.ts_beam_sets[0].ts_label.label.region not in RC.breast_codes:
        dibh_controls = 0
        for e in self.case.Examinations:
          if e.Name != ce.Name:
            # Assume it is a DIBH control series if it includes the string 'DIBH':
            if 'DIBH' in e.Name.upper():
              dibh_controls += 1
        if dibh_controls >= 2:
          return t.succeed()
        else:
          return t.fail(dibh_controls)
  
  # Tests if the CT image series used for treatment planning is the most recent CT image series in this case.
  # While evaluating against other image series, non-CT modalities, CBCT series and CT image series
  # having the same frame of reference UID as the primary image series are filtered out.
  def last_examination_used_test(self):
    t = TEST.Test("Den siste CT-serien som er tatt skal i utgangspunktet brukes til planlegging ", True, self.examination)
    more_recent = None
    primary = get_current("Examination")
    primary_date = primary.GetExaminationDateTime()
    for examination in self.case.Examinations:
      current_date = examination.GetExaminationDateTime()
      if current_date:
        if current_date > primary_date:
          description = examination.GetAcquisitionDataFromDicom()['SeriesModule']['SeriesDescription']
          frame_uid = examination.EquipmentInfo.FrameOfReference
          modality = examination.EquipmentInfo.Modality
          if modality == 'CT' and 'CBCT' not in description and frame_uid != primary.EquipmentInfo.FrameOfReference:
            more_recent = examination.Name
    if more_recent:
      return t.fail(more_recent)
    else:
      return t.succeed()

  # Tests if the same localization point is set in the free breathing CT and DIBH CT.
  def localization_points_for_gating_test(self):
    t = TEST.Test("Skal være samme referansepunkt i både fripust CT og dyp innpust CT for planer som har gating-regionkode", True, self.localization_point)
    points = []
    if self.ts_plan.ts_beam_sets[0].ts_label.label.region and self.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.breast_codes:
      for ts_structure_set in self.ts_structure_sets:
        if ts_structure_set.structure_set.LocalizationPoiGeometry.Point:
          points.append(ts_structure_set.structure_set.LocalizationPoiGeometry.Point)
      if len(points) >= 2:
        if points[0].x - points[1].x > 0.05 or points[0].y - points[1].y > 0.05 or points[0].z - points[1].z > 0.05:
          return t.fail()
        else:
          return t.succeed()

  # Tests that the CTV is not contracted (e.q. 5 mm) beneath the external contour for breast cases with virtual bolus.
  # (In these cases, the CTV should go all they way out to the external contour)
  def ctv_not_contracted_from_external_for_breast_case_with_virtual_bolus_test(self):
    t = TEST.Test("CTV skal ha 0 mm contraction i forhold til External for bryst caser som har virtuell bolus (bolus definert i RayStation)", 0, self.param)
    # Is this a Breast case?
    if self.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.breast_codes:
      # Do we have a virtual bolus present?
      match = False
      for roi in self.case.PatientModel.RegionsOfInterest:
        if roi.Name == 'Bolus' or roi.Type == 'Bolus':
          match = True
      if match:
        ctv = self.case.PatientModel.RegionsOfInterest['CTV']
        external_anterior_contraction = ctv.DerivedRoiExpression.Children[0].Children[1].AnteriorDistance
        if external_anterior_contraction > 0:
          return t.fail(external_anterior_contraction)
        else:
          return t.succeed()

  # Tests if there exists a virtual Bolus ROI in the case without a density override.
  def virtual_bolus_without_density_override_test(self):
    t = TEST.Test("Når en case har virtuell bolus (bolus definert i RayStation), skal denne være definert med et Material (density override).", True, self.param)
    # Do we have a virtual bolus present?
    bolus = None
    for roi in self.case.PatientModel.RegionsOfInterest:
      if roi.Name == 'Bolus' or roi.Type == 'Bolus':
        bolus = roi
    if bolus:
      if bolus.RoiMaterial == None:
        return t.fail(None)
      else:
        return t.succeed()
