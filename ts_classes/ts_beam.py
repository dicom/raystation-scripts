# encoding: utf8

# Contains treatment plan tests for individual beams.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
from tkinter import messagebox

# Local script imports:
import test_p as TEST
import patient_model_functions as PMF
import raystation_utilities as RSU

# This class contains tests for the RayStation Beam object:
class TSBeam(object):
  def __init__(self, beam, ts_beam_set=None):
    # RayStation object:
    self.beam = beam
    # Related test suite objects:
    self.ts_beam_set = ts_beam_set
    self.ts_segments = []
    if ts_beam_set:
      ts_beam_set.ts_beams.append(self)
      self.parent_param = ts_beam_set.param
    else:
      self.parent_param = None
    # Cache attributes:
    self._leaf_min_max = None
    # Parameters:
    self.param = TEST.Parameter('Felt', str(beam.Number), self.parent_param)
    self.name = TEST.Parameter('Navn', '', self.param)
    self.mu = TEST.Parameter('MU', '', self.param)
    self.gantry = TEST.Parameter('Gantryvinkel', str(round(self.beam.GantryAngle, 1)), self.param)
    self.energy = TEST.Parameter('Energi', str( self.beam.MachineReference.Energy), self.param)
    self.collimator = TEST.Parameter('Kollimatorvinkel', str(round(beam.InitialCollimatorAngle, 1)), self.param)
    self.segments = TEST.Parameter('Segmenter', '', self.param)
    self.gantry_spacing = TEST.Parameter('Gantry spacing', '', self.param)
    self.isocenter = TEST.Parameter('Isosenter', '', self.param)
    self.opening = TEST.Parameter('Åpning', '', self.param)
    self.mlc = TEST.Parameter('MLC', '', self.param)
    self.couch_rotation_angle = TEST.Parameter('Bordvinkel', str(beam.CouchRotationAngle), self.param)
    # Other attributes:
    self.segment_length = None

  # Gives the cached leaf min and leaf max positions of the segments of this beam.
  def leaf_min_max(self):
    if not self._leaf_min_max:
      # Start values (will be overwritten when extracting real leaf positions):
      minMLCX1 = 20
      maxMLCX2 = -20
      # Iterate all segments:
      for s in self.beam.Segments:
        # Get min and max leaf positions for this segment:
        val = min(s.LeafPositions[0])
        if val < minMLCX1:
          minMLCX1 = val
        val = max(s.LeafPositions[1])
        if val > maxMLCX2:
          maxMLCX2 = val
      self._leaf_min_max = [minMLCX1, maxMLCX2]
    return self._leaf_min_max
  
  # Gives true/false if the beam has segments or not.
  def has_segment(self):
    if not self.segment_length:
      self.segment_length = len(list(self.beam.Segments))
    if self.segment_length > 0:
      return True
    else:
      return False

  # Gives true/false if the beam is an VMAT arc
  def is_vmat(self):
    if self.beam.ArcRotationDirection != 'None':
      return True
    else:
      return False

  # Tests that for arcs that a gantry spacing of either 2 or 4 is used.
  def arc_gantry_spacing_test(self):
    t = TEST.Test("Skal normalt være 2 eller 4", "[2,4]", self.gantry_spacing)
    if self.is_vmat():
      # VMAT optimization settings:
      beam_s = RSU.beam_settings(self.ts_beam_set.ts_plan.plan, self.ts_beam_set.beam_set, self.beam)
      if beam_s:
        if not beam_s.ArcConversionPropertiesPerBeam.FinalArcGantrySpacing in [2, 4]:
          return t.fail(beam_s.ArcConversionPropertiesPerBeam.FinalArcGantrySpacing)
        else:
          return t.succeed()

  # Tests if the field is asymmetric, i.e. ifthe maximum jaw opening is more than 12.5 cm for Y1 and Y2 jaws for an VMAT arc, for filter free energies.
  def asymmetric_jaw_opening_for_filter_free_energies(self):
    t = TEST.Test("Maksimal avstand fra isosenter til feltgrense ved bruk av filter fri energi bør være < 12.5 cm  ", '<12.5 cm', self.collimator)
    # Perform the test only for VMAT beams:
    if self.is_vmat():
      if self.beam.BeamQualityId == '6 FFF':
        if self.has_segment():
          maxJawY1 = self.beam.Segments[0].JawPositions[2]
          maxJawY2 = self.beam.Segments[0].JawPositions[3]
          for segment in self.beam.Segments:
            if segment.JawPositions[2] < maxJawY1:
              maxJawY1 = segment.JawPositions[2]
            if segment.JawPositions[3] > maxJawY1:
              maxJawY2 = segment.JawPositions[3]
          if maxJawY1 < -12.5:
            return t.fail(maxJawY1)
          elif maxJawY2 > 12.5:
            return t.fail(maxJawY2)
          else:
            return t.succeed()

  # Tests if the maximum jaw opening is more than 10.5 cm for both Y1 and Y2 jaws for an VMAT arc, to be able to measure it with the ArcCHECK-phantom.
  def asymmetric_jaw_opening_for_vmat_qa_detector_test(self):
    t = TEST.Test("Isosenter ser ut til å være asymmetrisk, det bør vurderes å flytte isosenter. Dette for å få målt hele målvolumet med ArcCheck-fantomet", '<10.5 cm', self.isocenter)
    # Perform the test only for VMAT beams:
    if self.is_vmat():
      if self.has_segment():
        maxJawY1 = self.beam.Segments[0].JawPositions[2]
        maxJawY2 = self.beam.Segments[0].JawPositions[3]
        
        for segment in self.beam.Segments:
          if segment.JawPositions[2] < maxJawY1:
            maxJawY1 = segment.JawPositions[2]
          if segment.JawPositions[3] > maxJawY1:
            maxJawY2 = segment.JawPositions[3]
        messagebox.showinfo("", "2")
        if maxJawY1 < -10.5 and maxJawY2 > 10.5:
          return t.succeed()
        elif maxJawY1 < -10.5:
          return t.fail(abs(maxJawY1))
        elif maxJawY2 > 10.5:
          return t.fail(maxJawY2)
        else:
          return t.succeed()

  # Tests if a bolus is activated for the beam (in cases where a bolus exists among the ROIs).
  def bolus_set_test(self):
    t = TEST.Test("Bolus forventes å være aktivert for feltet når en bolus ROI eksisterer i struktursettet", None, self.param)
    if PMF.bolus(self.ts_beam_set.ts_plan.ts_case.case.PatientModel):
      t.expected = str(PMF.bolus_names(self.ts_beam_set.ts_plan.ts_case.case.PatientModel))
      if len(self.beam.Boli) > 0:
        return t.succeed()
      else:
        return t.fail(None)
  
  # Tests for cardinal collimator angles for VMAT arcs.
  def collimator_angle_of_arc_test(self):
    t = TEST.Test("Skal normalt unngå rette vinkler for VMAT buer", 'Ulik [0, 90, 180, 270]', self.collimator)
    if self.beam.ArcRotationDirection != 'None':
      if self.beam.InitialCollimatorAngle in [0, 90, 180, 270]:
        return t.fail(self.beam.InitialCollimatorAngle)
      else:
        return t.succeed()

  # Tests for a valid couch rotation angle (Max couch rotation angle on our linacs is 100 and 260 degrees).
  def couch_rotation_angle_test(self):
    t = TEST.Test("Skal ikke være større enn 100 grader eller mindre enn 260 grader", 'Ikke <100-260>', self.couch_rotation_angle)
    if 100 < self.beam.CouchRotationAngle < 260:
      return t.fail(self.beam.CouchRotationAngle)
    else:
      return t.succeed()
  
  # Tests for energy used for VMAT arcs.
  def energy_of_arc_test(self):
    t = TEST.Test("Skal normalt ikke bruke 15 MV ved VMAT", '6 eller 10', self.energy)
    if self.is_vmat():
      if self.beam.BeamQualityId == '15':
        return t.fail(self.beam.BeamQualityId)
      else:
        return t.succeed()

  # Tests for gantry angle (we want to avoid using the exact 180.0 angle).
  def gantry_angle_test(self):
    t = TEST.Test("Gantryvinkel lik 180 grader bør unngås, da denne vinkelen er tvetydig. Bruk < eller > enn 180.0, og velg den siden som best passer overens med øvrige feltvinkler samt planlagt XVI-protokoll.", '!= 180.0', self.gantry)
    if self.beam.GantryAngle == 180:
      return t.fail(self.beam.GantryAngle)
    else:
      return t.succeed()

  # Tests for SBRT with multiple targets (indexed targets) that the beam index matches the target index.
  def indexed_prescription_target_matches_beam_index_for_sbrt_test(self):
    t = TEST.Test("Ved stereotaksi og indekserte målvolum skal normeringsvolumets indeks være likt felt-nummer", self.beam.Number, self.param)
    # Only run test for SBRT:
    if self.ts_beam_set.ts_prescription.is_stereotactic():
      # Extract the numbers from the prescription name:
      target = self.ts_beam_set.ts_prescription.roi.value
      target_index = ''.join(n for n in target if n.isdigit())
      # Only run test for indexed targets:
      if target_index != '':
        if int(target_index) != self.beam.Number:
          return t.fail(target_index)
        else:
          return t.succeed()

  # Tests for gantry angle on a breast treatment (where we should not have an entry in the opposite posterior quadrant).
  def logical_gantry_angle_breast_test(self):
    t = TEST.Test("Gantryvinkel skrått bakfra fra motsatt side bør ikke forekomme ved brystbestråling", None, self.gantry)
    left_side_codes = [239, 241, 243, 273]
    right_side_codes = [240, 242, 244, 274]
    if self.ts_beam_set.ts_label:
      if self.ts_beam_set.ts_label.label.region in left_side_codes+right_side_codes:
        if self.ts_beam_set.ts_label.label.region in left_side_codes:
          t.expected = '!<180-270>'
          if 180 <= self.beam.GantryAngle <= 270:
            return t.fail(round(self.beam.GantryAngle, 1))
          else:
            return t.succeed()
        if self.ts_beam_set.ts_label.label.region in right_side_codes:
          t.expected = '!<90-180>'
          if 90 <= self.beam.GantryAngle <= 180:
            return t.fail(round(self.beam.GantryAngle, 1))
          else:
            return t.succeed()
  
  
  # Tests for monitor units being in the range 1000-1001 (which seems to create problems on the Elekta linac sometimes).
  def mu_1000_test(self):
    t = TEST.Test("Skal ikke være i intervallet 1000-1001", '<1000 eller >1001', self.mu)    
    if self.beam.BeamMU >= 1000 and self.beam.BeamMU <= 1001:
      return t.fail(round(self.beam.BeamMU, 2))
    else:
      return t.succeed()
  
  
  # Tests for low number of monitor units, for VMAT beams.
  def mu_beam_vmat_test(self):
    t = TEST.Test("Skal være høyere enn nedre praktiserte grense", '>2', self.mu)
    if self.is_vmat():
      if self.beam.BeamMU < 2:
        return t.fail(round(self.beam.BeamMU, 2))
      else:
        return t.succeed()

  # Tests for low number of monitor units for 3D-CRT beams.
  def mu_segment_3dcrt_test(self):
    t = TEST.Test("Skal være høyere enn nedre praktiserte grense", '>2', self.mu)
    if self.beam.ArcRotationDirection == 'None':
      for segment in self.beam.Segments:
        if self.beam.BeamMU*segment.RelativeWeight < 2:
          return t.fail(round(self.beam.BeamMU*segment.RelativeWeight, 2))
        else:
          return t.succeed()

  # Tests name capitalization (test passes also if first character is a non-letter (e.g. number)).
  def name_capitalization_test(self):
    t = TEST.Test("Skal være navngitt med stor forbokstav", None, self.name)
    if self.beam.Name[0].isupper() or not self.beam.Name[0].isalpha():
      return t.succeed()
    else:
      t.expected = self.beam.Name[0].upper()
      return t.fail(self.beam.Name[0])

  # Tests that name format is 'Arc X', with X being the beam number, for VMAT arcs.
  def name_of_arc_test(self):
    t = TEST.Test("Felt-navn for VMAT buer skal følge formatet 'Arc ' + feltnr", None, self.name)
    if self.is_vmat():
      expected = 'Arc ' + str(self.beam.Number)
      if expected != self.beam.Name:
        t.expected = expected
        return t.fail(self.beam.Name)
      else:
        return t.succeed()

  # Tests presence of name.
  def name_test(self):
    t = TEST.Test("Skal ha angitt et feltnavn", True, self.name)
    if self.beam.Name and len(self.beam.Name) > 0:
      return t.succeed()
    else:
      return t.fail()

  # Tests the number of segments used on a static beam.
  def number_of_segments_of_static_beam_test(self):
    t = TEST.Test("Skal i utgangspunktet være tilbakeholden med å bruke mange segmenter (ved IMRT)", '<8', self.segments)
    if self.beam.ArcRotationDirection == 'None':
      nr_segments = RSU.soc_length(self.beam.Segments)
      if nr_segments >= 8:
        return t.fail(nr_segments)
      else:
        return t.succeed()

  # Tests if the beam has segments.
  def segment_test(self):
    t = TEST.Test("Segment skal være definert.", True, self.segments)
    if self.has_segment():
      return t.succeed()
    else:
      return t.fail()

  # Tests if the jaw opening on a vmat plan is big enough to risk exposing the electronics of the QA detector.
  # The "limit" towards the electronics is 15 cm away from the gantry from the isocenter.
  # FIXME: This test is flawed in that it only really works in the default case of collimator angle near zero,
  # because it only reads the value of the Y1 jaw. Ideally this test (and perhaps many other of the field size related tests),
  # could be replaced with a target volume bounding box based test related to the isocenter position.
  def wide_jaw_opening_which_can_hit_vmat_qa_detector_electronics_test(self):
    t = TEST.Test("Høy kollimator-åpning detektert. Avhengig av kollimatorvinkel og kollimatoråpning, kan man i slike situasjoner risikere å bestråle elektronikken på ArcCheck-detektoren, som bør unngås. Ved asymmetrisk isosenter, bør isosenter vurderes flyttet for å unngå dette.", '<15 cm', self.opening)
    # Perform the test only for VMAT beams:
    if self.is_vmat():
      if self.has_segment():
        # Extract the jaw[2] value from 3 segments, and use the minimum value for the test (the maximally negative number):
        jaw_first = self.beam.Segments[0].JawPositions[2]
        jaw_middle = self.beam.Segments[round(len(self.beam.Segments)/2)].JawPositions[2]
        jaw_last = self.beam.Segments[len(self.beam.Segments)-1].JawPositions[2]
        jaw_position = min(jaw_first, jaw_middle, jaw_last)
        if jaw_position <= -15:
          return t.fail(round(abs(jaw_position), 1))
        else:
          return t.succeed()

  # Tests if the maximal jaw opening is large and a filter free energy has been used.
  def wide_jaw_opening_for_filter_free_energies(self):
    t = TEST.Test("Høy kollimatoråpning detektert, det bør vurderes om filter-energi bør brukes.", '<25 cm', self.opening)
    # Perform the test only for VMAT beams:
    if self.is_vmat():
      if self.beam.BeamQualityId == '6 FFF':
        if self.has_segment():
          # Extract field size from 3 segments (avoid pulling data from all segments to save execution time).
          segment_first = self.beam.Segments[0]
          segment_middle = self.beam.Segments[round(len(self.beam.Segments)/2)]
          segment_last = self.beam.Segments[len(self.beam.Segments)-1]
          # For Y1 more negative number means larger field size:
          maxJawY1 = min([segment_first.JawPositions[2], segment_middle.JawPositions[2], segment_last.JawPositions[2]])
          # For Y2 more positive number means larger field size:
          maxJawY2 = max([segment_first.JawPositions[3], segment_middle.JawPositions[3], segment_last.JawPositions[3]])
          leaf_min_max = self.leaf_min_max()
          if leaf_min_max[1] - leaf_min_max[0] > 25:
            return t.fail(leaf_min_max[1] - leaf_min_max[0])
          elif maxJawY2 - maxJawY1 > 25:
            return t.fail(maxJawY2 - maxJawY1)
          else:
            return t.succeed()
            
  # Tests if the maximal jaw opening is small and a filter free beam quality has not been used.
  def narrow_jaw_opening_for_filter_energies(self):
    t = TEST.Test("Liten kollimatoråpning detektert. Det bør vurderes om filterfri-energi kan brukes for å spare tid.", '<20 cm', self.opening)
    # Perform the test only for VMAT beams:
    if self.is_vmat():
      if not 'FFF' in self.beam.BeamQualityId:
        if self.has_segment():
          maxJawY1 = self.beam.Segments[0].JawPositions[2]
          maxJawY2 = self.beam.Segments[0].JawPositions[3]
          for segment in self.beam.Segments:
            if segment.JawPositions[2] < maxJawY1:
              maxJawY1 = segment.JawPositions[2]
            if segment.JawPositions[3] > maxJawY1:
              maxJawY2 = segment.JawPositions[3]
          if abs(maxJawY1)+abs(maxJawY2) < 20:
            return t.fail(abs(maxJawY1)+abs(maxJawY2))
          else:
            return t.succeed()

