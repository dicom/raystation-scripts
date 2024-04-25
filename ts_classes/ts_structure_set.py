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
import rois as ROIS
import region_codes as RC
import structure_set_functions as SSF


# This class contains tests for the RayStation Structure Set object:
class TSStructureSet(object):
  def __init__(self, structure_set, ts_case=None):
    # RayStation object:
    self.structure_set = structure_set
    # Related test suite objects:
    self.ts_case = ts_case
    self.ts_poi_geometries = []
    self.ts_roi_geometries = []
    if ts_case:
      ts_case.ts_structure_sets.append(self)
      self.parent_param = ts_case.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('Struktursett', self.structure_set.OnExamination.Name, self.parent_param)
    self.localization_point = TEST.Parameter('REF', '', self.param)
    self.couch = TEST.Parameter('Bordtopp', '', self.param)
    self.external = TEST.Parameter('External', '', self.param)
    self.external_bounding = TEST.Parameter('External', '', self.param)
    self.geometry = TEST.Parameter('Geometri', '', self.param)
    self.name = TEST.Parameter('Navn', '', self.param)
    #self.dose_region = TEST.Parameter('Geometri', '', self.param)
    #self.target_volume_test = TEST.Parameter('Geometri', '', self.param)
    #self.ptv_derived = TEST.Parameter('Geometri', '', self.param)
    #self.prosthesis = TEST.Parameter('Geometri', '', self.param)
    #self.dsc = TEST.Parameter('Geometri', '', self.param)
    #self.breast = TEST.Parameter('Geometri', '', self.param)
    # Determine the slice thickness for the examination associated with this structure set:
    self.slice_thickness = round(abs(self.structure_set.OnExamination.Series[0].ImageStack.SlicePositions[1] - self.structure_set.OnExamination.Series[0].ImageStack.SlicePositions[0]), 2)


  # Tests if breast patients having a boost of 2 Gy x 8 has Clips/Markers defined.
  def breast_seeds_test(self):
    t = TEST.Test("Bryst-pasienter som skal ha ungdomsboost skal ha Clips_L eller Clips_R definert.", True, self.geometry)
    if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region:
      if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.breast_codes:
        for beam_set in self.ts_case.ts_plan.ts_beam_sets:
          if beam_set.ts_label.label.nr_fractions == '8':
            match = False
            for rg in self.structure_set.RoiGeometries:
              if rg.HasContours():
                if rg.OfRoi.Name == 'Clips_L' or rg.OfRoi.Name == 'Clips_R':
                  match = True
            if match:
              return t.succeed()
            else:
              return t.fail()

  # Test for presence of couch for photon plans.
  # Skips the test for stereotactic brain plans, where external is used to define the couch instead.
  def couch_test(self):
    t = TEST.Test("Struktursettet må ha definert en bordtopp-ROI (Couch) med tetthet 0.121 g/cm^3", True, self.couch)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    match = False
    if self.ts_case.ts_plan.ts_beam_sets[0].beam_set.Modality == 'Photons':
      if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.technique and self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.technique.upper() == 'S' and self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.brain_codes:
        match = True
      else:
        for rg in self.structure_set.RoiGeometries:
          if rg.OfRoi.Name == ROIS.couch.name and rg.OfRoi.RoiMaterial and rg.OfRoi.RoiMaterial.OfMaterial.MassDensity == 0.121 and rg.HasContours():
            match = True
        if match:
          return t.succeed()
        else:
          return t.fail()

  # Tests if the couch top is placed close to the patient.
  def couch_close_to_patient_test(self):
    t = TEST.Test("Bordtopp-ROI (Couch) skal ligge inntil external", True, self.couch)
    if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.technique:
      if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.technique.upper() != 'S' and self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region not in RC.brain_codes:
        for roi in self.structure_set.RoiGeometries:
          if roi.OfRoi.Name == ROIS.couch.name and roi.HasContours():
            for r in self.structure_set.RoiGeometries:
              if r.OfRoi.Name == ROIS.external.name and r.HasContours():
                couch = self.structure_set.RoiGeometries[ROIS.couch.name].GetBoundingBox()
                external = self.structure_set.RoiGeometries[ROIS.external.name].GetBoundingBox()
                if abs(couch[1].y - external[1].y) > 15 or abs(couch[1].y - external[1].y) < 5.41:
                  return t.fail()
                else:
                  return t.succeed()

  # Tests for presence of an external.
  def external_test(self):
    t = TEST.Test("Struktursettet må ha definert en ytterkontur (navn og type skal være: External)", True, self.external)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    match = False
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.Name == ROIS.external.name and rg.OfRoi.Type == ROIS.external.type :
        match = True
    if match:
      return t.succeed()
    else:
      return t.fail()

  # Tests if the CT-images are cropped close to external.
  def external_bounding_test(self):
    t = TEST.Test("External ligger helt på yttergrensen av bildeopptaket. Dette kan tyde på at CT-bildene er beskjært uheldig, og at deler av pasienten mangler. Dersom denne beskjæringen forekommer i nærheten av målvolumet, vil det resultere i feil doseberegning.", True, self.external_bounding)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    has_external_at_bounding_box = False
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.Type == ROIS.external.type:
        # Check if the external bounding box equals that of its image series
        # (which indicates that the patient was cropped with the chosen FOV,
        # and that dose computation will not be accurate).
        ext_box = rg.GetBoundingBox()
        for series in self.structure_set.OnExamination.Series:
          img_box = series.ImageStack.GetBoundingBox()
          # We check in lateral (x) and vertical (y) directions:
          if abs(ext_box[0].x - img_box[0].x) < 0.1:
            has_external_at_bounding_box = True
          if abs(ext_box[1].x - img_box[1].x) < 0.1:
            has_external_at_bounding_box = True
          if abs(ext_box[0].y - img_box[0].y) < 0.1:
            has_external_at_bounding_box = True
          if abs(ext_box[1].y - img_box[1].y) < 0.1:
            has_external_at_bounding_box = True
        if has_external_at_bounding_box:
          return t.fail()
        else:
          return t.succeed()

  # Tests if the CT-images are cropped close to external, in the same area as there is a target volume.
  def external_ptv_bounding_test(self):
    t = TEST.Test("External ligger helt på yttergrensen av bildeopptaket. Dette kan tyde på at CT-bildene er beskjært uheldig, og at deler av pasienten mangler. Dersom denne beskjæringen forekommer i nærheten av målvolumet, vil det resultere i feil doseberegning.", True, self.external_bounding)
    match = False
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    if SSF.has_named_roi_with_contours(self.structure_set, ROIS.external.name):
      ext_box = self.structure_set.RoiGeometries[ROIS.external.name].GetBoundingBox()
      img_box = self.structure_set.OnExamination.Series[0].ImageStack.GetBoundingBox()
      # Iterate all ROI geometries:
      for rg in self.structure_set.RoiGeometries:
        # We have quite a few criterias on which ROI geometries to test with. It should be a GTV or CTV, it should have contours
        # (unfotunately a cornercase has been discovered with an underived but unedited ROI which means we also have to check for the attribute 'Contours'),
        # and finally we dont check on derived ROIs:
        if rg.OfRoi.Type in ['Gtv','Ctv'] and rg.HasContours() and hasattr(rg.PrimaryShape, 'Contours') and not rg.PrimaryShape.DerivedRoiStatus:
          roi_box = rg.GetBoundingBox()
          if abs(roi_box[0].z - img_box[0].z) < 1.5 or abs(roi_box[1].z -img_box[1].z) < 1.5:
            match = True
          elif abs(ext_box[0].x - img_box[0].x) < 0.2 or abs(ext_box[1].x - img_box[1].x) < 0.2:
            for [contour_index, contour] in enumerate(rg.PrimaryShape.Contours):
              for coordinate in contour:
                if round(ext_box[0].x, 1) == round(coordinate.x, 1):
                  z = round(coordinate.z, 1)
                  if (ptv_box[0].z - 5 < z) or (ptv_box[1].z + 5 > z):
                    match = True
    if match:
      return t.fail()
    else:
      return t.succeed()

  # Tests for presence of localization point POI geometry.
  def localization_point_test(self):
    t = TEST.Test("Skal inneholde et referansepunkt (Localization Point)", True, self.localization_point)
    match = False
    for pg in self.structure_set.PoiGeometries:
      if pg.OfPoi.Type == 'LocalizationPoint':
        match = True
    if match:
      return t.succeed()
    else:
      return t.fail()

  # Tests if there is a ROI called 'Prosthesis' and if the material is Titanium.
  def prosthesis_titanium_test(self):
    t = TEST.Test("Hvis proteser er til stede, skal disse hete " + ROIS.prosthesis.name + ", " + ROIS.prosthesis_r.name + " eller " + ROIS.prosthesis_l.name + " og material skal være satt til 'Titanium'", None, self.param)
    invalid = []
    # Test for properly named ROI with invalid material:
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.Name in [ROIS.prosthesis.name, ROIS.prosthesis_r.name, ROIS.prosthesis_l.name]:
        if not rg.OfRoi.RoiMaterial or rg.OfRoi.RoiMaterial.OfMaterial.Name != 'Titanium':
          invalid.append(rg.OfRoi.Name)
    # Test for ROI with prosthethic material but invalid name:
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.RoiMaterial and rg.OfRoi.RoiMaterial.OfMaterial.Name == 'Titanium':
        if rg.OfRoi.Name not in [ROIS.prosthesis.name, ROIS.prosthesis_r.name, ROIS.prosthesis_l.name]:
          invalid.append(rg.OfRoi.Name)
    if len(invalid) == 0:
      return t.succeed()
    else:
      return t.fail(str(invalid))

  # Tests if the structure set has a dose region or a target volume
  def dose_region_test(self):
    t = TEST.Test("Struktursett som mangler målvolum skal ha en 'Dose region' ROI, som brukes til volum-normering, eller hvis punkt-normert, som veiledningsvolum til XVI (90% isodose).", True, self.geometry)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    match = False
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.Type in ('Gtv', 'Ctv', 'Ptv','DoseRegion'):
        match = True
    if match:
      return t.succeed()
    else:
      return t.fail()

  # Tests if PTV's are derived
  def ptv_derived_test(self):
    t = TEST.Test("Alle PTV skal i utgangspunktet være 'derived'", True, self.geometry)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.Type == 'Ptv' and rg.PrimaryShape:
        if rg.OfRoi.DerivedRoiExpression:
          return t.succeed()
        else:
          return t.fail()

  # Tests that there is no empty slice between the rectum and the anal canal ROI geometries.
  # (which is a known bug/weakness in the current DL segmentation model)
  def no_empty_slice_between_rectum_and_analcanal_test(self):
    t = TEST.Test("Pasienter som har Rectum og AnalCanal definert, skal ikke ha et tomt snitt mellom disse ROI geometriene.", None, self.geometry)
    rectum = None
    anal_canal = None
    bb_rectum = None
    bb_anal_canal = None
    for rg in self.structure_set.RoiGeometries:
      if rg.OfRoi.Name == 'Rectum':
        rectum = rg
      elif rg.OfRoi.Name == 'AnalCanal':
        anal_canal = rg
    try:
      bb_rectum = rectum.GetBoundingBox()
      bb_anal_canal = anal_canal.GetBoundingBox()
    except:
      pass
    if bb_rectum and bb_anal_canal:
      rectum_caudal_limit = bb_rectum[0].z
      anal_canal_cranial_limit = bb_anal_canal[1].z
      # Distance between the two ROI geometries in the longitudinal axis:
      distance = rectum_caudal_limit - anal_canal_cranial_limit
      if distance > 0.5 * self.slice_thickness:
        return t.fail(round(distance, 2))
      else:
        return t.succeed()

  # Tests if any ROI geometry seems to be outside the External contour.
  # (Test is performed left-right and anterior-posterior, not in longitudinal direction)
  def no_geometries_outside_external_test(self):
    t = TEST.Test("Geometri forventes å ikke være definert utenfor 'External' for noen ROI", None, self.geometry)
    external = None
    geometries = []
    failed_geometries = []
    # Iterate ROI geometries:
    for ts_rg in self.ts_roi_geometries:
      if ts_rg.roi().Type == 'External':
        external = ts_rg
      elif ts_rg.roi().Type != 'Support' and ts_rg.primary_shape():
        # The ROI geometry actually has a shape, and is not a couch ROI, so it is relevant for the test:
        geometries.append(ts_rg)
    if external and len(geometries) > 0:
      ext_bb = external.bounding_box()
      # Iterate the selected geometries and check their bounding boxes against external:
      for ts_rg in geometries:
        bb = ts_rg.bounding_box()
        if bb[0].x < ext_bb[0].x or bb[1].x > ext_bb[1].x or bb[0].y < ext_bb[0].y or bb[1].y > ext_bb[1].y:
          failed_geometries.append(ts_rg.roi().Name)
    if len(failed_geometries) == 0:
      return t.succeed()
    else:
      return t.fail(str(failed_geometries))
