# encoding: utf8

# Contains tests for the case object.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
#sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\RayStation\\lib".decode('utf8'))

# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *

# Local script imports:
import test as TEST
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
    self.param = TEST.Parameter('Case', self.case.CaseName.decode('utf8', 'replace'), self.parent_param)
    self.localization_point = TEST.Parameter('REF', '', self.param)
    self.examination = TEST.Parameter('Examination', '', self.param)
    self.defined_roi = TEST.Parameter('Geometri','', self.param)
    # Attributes:
    self.has_target_volume = self.target_volume()




  # Determines if a target volume is defined in the case.
  def target_volume(self):
    match = False
    for roi in self.case.PatientModel.RegionsOfInterest:
      if roi.Type in ('Gtv', 'Ctv', 'Ptv'):
       match = True
    return match

  #Tests if all ROI's are defined, except 'LAD' for right sided breast, and contralateral breast for conventional treatment (ie. not VMAT)
  def breast_oar_defined_test(self):
    failed_geometries = []
    t = TEST.Test("Regionen må ha definert volum:", True, self.defined_roi)
    t.expected = None

    for rg in self.ts_structure_sets[0].structure_set.RoiGeometries:
      if rg.HasContours() == False:
        if self.ts_plan.ts_beam_sets[0].beam_set.DeliveryTechnique != 'Arc':
          if rg.OfRoi.Name == ROIS.lad.name and (int(self.ts_plan.ts_beam_sets[0].ts_label.label.region) in RC.breast_l_codes):
            failed_geometries.append(str(rg.OfRoi.Name.decode('utf8', 'replace')))
          elif not rg.OfRoi.Name in (ROIS.breast_r.name, ROIS.breast_r_draft.name) and (int(self.ts_plan.ts_beam_sets[0].ts_label.label.region) in RC.breast_l_codes):
            failed_geometries.append(str(rg.OfRoi.Name.decode('utf8', 'replace')))
          elif not rg.OfRoi.Name in (ROIS.lad.name, ROIS.breast_r.name, ROIS.breast_r_draft.name):
            failed_geometries.append(str(rg.OfRoi.Name.decode('utf8', 'replace')))
        elif self.ts_plan.ts_beam_sets[0].beam_set.DeliveryTechnique == 'Arc':
          if rg.OfRoi.Name == ROIS.lad.name and (int(self.ts_plan.ts_beam_sets[0].ts_label.label.region) in RC.breast_l_codes):
            failed_geometries.append(str(rg.OfRoi.Name.decode('utf8', 'replace')))
          elif rg.OfRoi.Name != ROIS.lad.name:
            failed_geometries.append(str(rg.OfRoi.Name.decode('utf8', 'replace')))

    new_failed_geometries = []
    if len(failed_geometries) >= 1:
      for structure_set in self.case.PatientModel.StructureSets:
        structure_sets = []
        if structure_set != self.ts_plan.ts_beam_sets[0].ts_structure_set().structure_set:
          structure_sets.append(structure_set)
          for struct_set in structure_sets:
            for rg in struct_set.RoiGeometries:
              for roi in list(set(failed_geometries)):
                if rg.OfRoi.Name == roi:
                  if rg.HasContours() == True:
                    failed_geometries.remove(roi)


    if len(failed_geometries) >= 1:
      return t.fail(list(set(failed_geometries)))
    else:
      return t.succeed()

 #Tests if the same localization point is set in the free breathing CT and DIBH CT.
  def localization_points_for_gating_test(self):
    t = TEST.Test("Skal være samme referansepunkt i både fripust CT og dyp innpust CT for planer som har gating-regionkode", True, self.localization_point)
    points = []
    if self.ts_plan.ts_beam_sets[0].ts_label.label.region and self.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.breast_l_codes:
      for ts_structure_set in self.ts_structure_sets:
        points.append(ts_structure_set.structure_set.LocalizationPoiGeometry.Point)
      if len(points) >= 2:
        if points[0].x - points[1].x > 0.05 or points[0].y - points[1].y > 0.05 or points[0].z - points[1].z > 0.05:
          return t.fail()
        else:
          return t.succeed()

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


