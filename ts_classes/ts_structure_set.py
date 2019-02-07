# encoding: utf8

# Contains treatment plan tests for individual treatment plans.
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
    self.param = TEST.Parameter('Struktursett', self.structure_set.OnExamination.Name.decode('utf8', 'replace'), self.parent_param)
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


  # Tests if breast patients having a boost of 2 Gy x 8 has Clips/Markers defined
  def breast_seeds_test(self):
    t = TEST.Test("Mammae-pasienter som skal ha ungdomsboost skal ha " + ROIS.clips.name + " definert.", True, self.geometry)
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
      if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region:
        if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.breast_codes:
          for beam_set in self.ts_case.ts_plan.ts_beam_sets:
            if beam_set.ts_label.label.nr_fractions == '8':
              match = False
              for rg in self.structure_set.RoiGeometries:
                if rg.OfRoi.Name == ROIS.clips.name and rg.HasContours():
                  match = True
              if match:
                return t.succeed()
              else:
                return t.fail()

  # Test for presence of couch for photon plans.
  # Skips the test for stereotactic brain plans, where external is used to define the couch instead.
  def couch_test(self):
    t = TEST.Test("Struktursettet må ha definert en bordtopp-ROI (Couch)", True, self.couch)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
      match = False
      if self.ts_case.ts_plan.ts_beam_sets[0].beam_set.Modality == 'Photons':
        if self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.technique and self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.technique.upper() == 'S' and self.ts_case.ts_plan.ts_beam_sets[0].ts_label.label.region in RC.brain_codes:
          match = True
        else:
          for rg in self.structure_set.RoiGeometries:
            if rg.OfRoi.Name == ROIS.couch.name and rg.OfRoi.RoiMaterial.OfMaterial.MassDensity == 0.121 and rg.HasContours():
              match = True
        if match:
          return t.succeed()
        else:
          return t.fail()

  # Tests if the couch top is placed close to the patient
  def couch_close_to_patient_test(self):
    t = TEST.Test("Bordtopp-ROI (Couch) skal ligge inntil external", True, self.couch)
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
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

  # Tests for presence of an external
  def external_test(self):
    t = TEST.Test("Struktursettet må ha definert en ytterkontur (navn og type skal være: External)", True, self.external)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
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
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
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
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    #t.expected = 0
    match = False
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
    #or structure_set in self.ts_plan.ts_case.case.PatientModel.StructureSets:
      for rg in self.structure_set.RoiGeometries:
        if SSF.has_named_roi_with_contours(self.structure_set, ROIS.external.name):
          ext_box = self.structure_set.RoiGeometries[ROIS.external.name].GetBoundingBox()
          img_box = self.structure_set.OnExamination.Series[0].ImageStack.GetBoundingBox()
          if rg.OfRoi.Type in ['Gtv','Ctv'] and rg.HasContours() and not rg.PrimaryShape.DerivedRoiStatus:
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

  # Tests for presence of localization point.
  def localization_point_test(self):
    t = TEST.Test("Skal inneholde et referansepunkt (Localization Point)", True, self.localization_point)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    # (FIXME: This may not be correct for mamma gating)
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
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
    t = TEST.Test("Hvis proteser er til stedet, skal disse hete " + ROIS.prosthesis.name + ", " + ROIS.prosthesis_r.name + " eller " + ROIS.prosthesis_l.name + " og skal være satt til 'Titanium'", True, self.geometry)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
      match = False
      for rg in self.structure_set.RoiGeometries:
        if rg.OfRoi.Name in [ROIS.prosthesis.name, ROIS.prosthesis_r.name, ROIS.prosthesis_l.name]:
          if rg.OfRoi.Name in [ROIS.prosthesis.name, ROIS.prosthesis_r.name, ROIS.prosthesis_l.name] and rg.OfRoi.RoiMaterial.OfMaterial.Name == 'Titanium' and rg.OfRoi.RoiMaterial.OfMaterial.MassDensity == 4.54:
            match = True
          else:
            match = False
        else:
          match = True
      for rg in self.structure_set.RoiGeometries:
        if rg.OfRoi.RoiMaterial:
          if rg.OfRoi.RoiMaterial.OfMaterial.Name == 'Titanium' and rg.OfRoi.Name not in [ROIS.prosthesis.name, ROIS.prosthesis_r.name, ROIS.prosthesis_l.name]:
            match = False
        else:
          match = True
      if match:
        return t.succeed()
      else:
        return t.fail()

  # Tests if the structure set has a dose region or a target volume
  def dose_region_test(self):
    t = TEST.Test("Struktursett som mangler målvolum skal ha en 'Dose region' ROI, som brukes til volum-normering, eller hvis punkt-normert, som veiledningsvolum til XVI (90% isodose).", True, self.geometry)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
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
    if self.structure_set == self.ts_case.ts_plan.plan.GetStructureSet():
      for rg in self.structure_set.RoiGeometries:
        if rg.OfRoi.Type == 'Ptv' and rg.PrimaryShape:
          if rg.OfRoi.DerivedRoiExpression:
            return t.succeed()
          else:
            return t.fail()







