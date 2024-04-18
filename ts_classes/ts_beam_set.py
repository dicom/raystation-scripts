# encoding: utf8

# Contains treatment plan tests for individual beam sets.
#
# Verified for RayStation 9.A
# Python 3.6

# System configuration:
from connect import *
import sys
import math

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST
import raystation_utilities as RSU
import rois as ROIS
import region_codes as RC
import structure_set_functions as SSF

# This class contains tests for the RayStation BeamSet object:
class TSBeamSet(object):
  def __init__(self, beam_set, ts_plan=None):
    # RayStation object:
    self.beam_set = beam_set
    # Related test suite objects:
    self.ts_plan = ts_plan
    self.ts_prescription = None
    self.ts_optimization = None
    self.ts_label = None
    self.ts_beams = []
    if ts_plan:
      ts_plan.ts_beam_sets.append(self)
      self.parent_param = ts_plan.param
    # Cache attributes:
    self._prescription_roi_name = None
    # Parameters:
    self.param = TEST.Parameter('Beam Set', self.beam_set.DicomPlanLabel, self.parent_param)
    self.technique = TEST.Parameter('Teknikk', self.beam_set.DeliveryTechnique, self.param)
    self.machine = TEST.Parameter('Maskin', self.beam_set.MachineReference.MachineName, self.param)
    self.dose = TEST.Parameter('Doseberegning', '', self.param)
    self.energies = TEST.Parameter('Energier', '', self.param)
    self.label = TEST.Parameter('Label', beam_set.DicomPlanLabel, self.param)
    self.vmat = TEST.Parameter('VMAT', '', self.param)
    self.fractions = TEST.Parameter('Fraksjoner', beam_set.FractionationPattern.NumberOfFractions, self.param)
    self.collimator_angles = TEST.Parameter('Kollimator vinkler', '', self.param)
    self.defined_prescription = TEST.Parameter('Prescription', '', self.param)
    self.couch = TEST.Parameter('Bordtopp', '', self.param)
    self.mlc = TEST.Parameter('MLC', '', self.param)
    self.norm_dose = TEST.Parameter('Dose', '', self.param)
    self.isocenter = TEST.Parameter('Isosenter','', self.param)
    self.mu = TEST.Parameter('MU', '', self.param)
    self.name = TEST.Parameter('Navn', '', self.param)
    self.number = TEST.Parameter('Feltnummer','', self.param)


  # Gives true/false if the beam set has beams of not.
  def has_beam(self):
    if len(list(self.beam_set.Beams)) > 0:
      return True
    else:
      return False

  # Gives true/false if the beam set has dose or not.
  def has_dose(self):
    if self.beam_set.FractionDose.DoseValues:
      return True
    else:
      return False

  # Gives true/false if the beam set has a prescription defined.
  def has_prescription(self):
    if self.beam_set.Prescription.PrimaryPrescriptionDoseReference:
      return True
    else:
      return False

  # Gives true/false if the delivery technique is VMAT or not.
  def is_vmat(self):
    if self.beam_set.DeliveryTechnique in ['Arc','DynamicArc'] and self.beam_set.Modality == 'Photons':
      return True
    else:
      return False

  # Gives the fraction dose (in Gy).
  def fraction_dose(self):
    return (self.beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue / 100.0) / self.beam_set.FractionationPattern.NumberOfFractions

  # Gives the cached precription ROI name.
  def prescription_roi_name(self):
    if not self._prescription_roi_name:
     self._prescription_roi_name = self.beam_set.Prescription.PrimaryPrescriptionDoseReference.OnStructure.Name
    return self._prescription_roi_name
  
  # Gives the ts_structure_set which corresponds with this beam set:
  def ts_structure_set(self):
    for ts_struct in self.ts_plan.ts_case.ts_structure_sets:
      if ts_struct.structure_set.OnExamination.Name == self.beam_set.GetPlanningExamination().Name:
        return ts_struct

  # Tests if the isocenter is assymmetric in the longitudinal direction, in such a way that it could pose a problem for measuring the plan by VMAT QA.
  def asymmetric_jaw_opening_long_test(self):
    t = TEST.Test("Isosenter ser ut til å være asymmetrisk, det bør vurderes å flytte isosenter. Dette for å få målt hele målvolumet med ArcCheck-fantomet", '<10.5 cm', self.isocenter)
    ss = self.ts_structure_set().structure_set
    isocenter = None
    target0 = None
    target1 = None
    if self.is_vmat():
      roi = ss.RoiGeometries[self.prescription_roi_name()]
      box = roi.GetBoundingBox()
      target0 = box[0].z
      target1 = box[1].z
      # Iterate beams:
      for beam in self.beam_set.Beams:
        photon_iso = beam.Isocenter.Position
        if target0 and target1:
          if abs(target0 - target1) <= 21:
            if abs(photon_iso.z - target0) > 10.5:
              return t.fail(round(abs(photon_iso.z - target0),2))
            elif abs(photon_iso.z - target1) > 10.5:
              return t.fail(round(abs(photon_iso.z - target1),2))
            else:
              return t.succeed()
          else:
            return t.succeed()

  # Tests if the energies of the beams in the beam set are the same.
  def beam_energy_equality_test(self):
    wanted_energy = '6'
    t = TEST.Test("Det skal i utgangspunktet benyttes samme energi for alle felt i et beam set. Kun ved særskilte kliniske begrunnelser skal dette avvikes.", wanted_energy, self.energies)
    energies = []
    for beam in self.beam_set.Beams:
      energies.append(beam.BeamQualityId)
    if len(set(energies)) > 1:
      return t.fail(energies)
    else:
      return t.succeed()

  # Tests that the beam numbering in the beam set is correct (that subsequent beam numbers are used, i.e. no gaps).
  def beam_number_test(self):
    numbers = []
    order = True
    t = TEST.Test("Feltnummereringen ser ikke ut til å være riktig.", True, self.number)
    for beam in self.beam_set.Beams:
      numbers.append(beam.Number)
    numbers.sort()
    if len(numbers) > 1:
      for i in range(0, len(numbers)-1):
        if numbers[i+1] != numbers[i]+1:
          order = False
    if order:
      return t.succeed()
    else:
      return t.fail()

  # Tests if a prescription is defined.
  def defined_prescription_test(self):
    t = TEST.Test("Skal være definert.", True, self.defined_prescription)
    if self.has_prescription():
      return t.succeed()
    else:
      return t.fail()

  # Tests the presence of a dose calculation.
  def dose_test(self):
    t = TEST.Test("Skal være definert", True, self.dose)
    if not self.has_dose():
      return t.fail()
    else:
      return t.succeed()

  # Tests that the dose status is 'clinical'.
  def dose_is_clinical_test(self):
    t = TEST.Test("Beregning skal være markert som 'klinisk'", True, self.dose)
    if self.has_dose():
      if self.beam_set.FractionDose.DoseValues.IsClinical:
        return t.succeed()
      else:
        return t.fail()

  # Tests that the dose algorithm is among the 2 white listed: CCDose & ElectronMonteCarlo.
  def dose_algorithm_test(self):
    t = TEST.Test("Algoritme skal være en av disse", ['CCDose', 'ElectronMonteCarlo'], self.dose)
    if self.has_dose():
      if self.beam_set.FractionDose.DoseValues.AlgorithmProperties.DoseAlgorithm in ['CCDose', 'ElectronMonteCarlo']: # other plausible value: 'Mixed'
        return t.succeed()
      else:
        return t.fail(self.beam_set.FractionDose.DoseValues.AlgorithmProperties.DoseAlgorithm)

 # Tests that, for conventional plans, the first MLC leaf behind the collimator is at the same posiition as the first MLC leaf inside the field.
  def guard_leaf_test(self):
    failed_beams = []
    t = TEST.Test("Første MLC blad utenfor blender skal være på samme posisjon som første MLC blad innenfor blender", None, self.mlc)
    if not self.is_vmat():
      for beam in self.beam_set.Beams:
        for [segment_index, segment] in enumerate(beam.Segments):
          leaf_positions = segment.LeafPositions
          jaw = segment.JawPositions
          # array (x1,x2,y1,y2)  we are looking at Y1 and Y2.
          y1 = jaw[2]
          y2 = jaw[3]
          if -1 < y1 < 1:
            # get the last corresponding MLC that is in the field
            mlcY1 = int(math.floor((y1 + 20) * 2) + 1.0)
            # don't forget that mlc 50 is in spot leafPositions[0][49]
            if (mlcY1 - 2) > 0:
              if round(abs(leaf_positions[0][mlcY1 - 2]), 3) - round(abs(leaf_positions[0][mlcY1 - 1]), 3) > 0.2 or round(abs(leaf_positions[1][mlcY1 - 2]), 3) - round(abs(leaf_positions[1][mlcY1 - 1]), 3) > 0.2:
                if round(beam.BeamMU*segment.RelativeWeight, 2) > 20:
                  failed_beams.append(str(beam.Name))
          elif -1< y2 < 1:
            mlcY2 = int(math.ceil ((y2 + 20) * 2))
            if mlcY2 < 80:
              if round(abs(leaf_positions[0][mlcY2]), 3) - round(abs(leaf_positions[0][mlcY2 - 1]), 3) > 0.2 or round(abs(leaf_positions[1][mlcY2]), 3)  - round(abs(leaf_positions[1][mlcY2 - 1]), 3) > 0.2:
                if round(beam.BeamMU*segment.RelativeWeight, 2) > 20:
                  failed_beams.append(str(beam.Name))

        if len(failed_beams) >= 1:
          return t.fail(list(set(failed_beams)))
        else:
          return t.succeed()

  # Tests that the isocenter coordinate is reasonably centered in the patient (in the axial slice).
  def isocenter_centered_test(self):
    t = TEST.Test("Skal i utgangspunktet være mest mulig sentrert i pasientens aksial-snitt", '<= 12 cm', self.isocenter)
    photon_iso = None
    if self.beam_set.Modality == 'Photons':
      ss = self.ts_structure_set().structure_set
      for beam in self.beam_set.Beams:
        if not photon_iso:
          photon_iso = beam.Isocenter.Position
          # For photon plans, isosenter should be somewhat centered in the patient to avoid gantry collisions.
          # Compare isocenter x and y coordinates to the center coordinates of the external ROI:
          if SSF.has_named_roi_with_contours(ss, ROIS.external.name):
            # Determine x and y coordinate:
            patient_center_x = SSF.roi_center_x(ss, ROIS.external.name)
            patient_center_y = SSF.roi_center_y(ss, ROIS.external.name)
            # Reset large patient center x values (Why do we do this?!)
            if abs(patient_center_x) > 3:
              patient_center_x = 0
            # Determine the distance between patient center and isocenter:
            diff = round(((photon_iso.x - patient_center_x ) ** 2 + (photon_iso.y - patient_center_y) ** 2) ** 0.5, 1)
            if diff > 12:
              return t.fail(diff)
            else:
              return t.succeed()

  # Tests that the isocenter coordinate is reasonably centered in the normalisation volume (in the longitudinal direction).
  def isocenter_centered_long_test(self):
    t = TEST.Test("Isosenter skal i utgangspunktet være mest mulig sentrert i long-retning (avstand mellom isosenter og senter av normeringsvolumet bør være mindre enn 1 cm)", '<1 cm', self.isocenter)
    if self.beam_set.Modality == 'Photons':
      diff = 0
      ss = self.ts_structure_set().structure_set
      # Get the target geometry:
      roi = ss.RoiGeometries[self.prescription_roi_name()]
      target = roi.GetBoundingBox()
      target0 = target[0].z
      target1 = target[1].z
      if target0 and target1:
        target_center_z = target0 + 0.5*abs(target0 - target1)
        for beam in self.beam_set.Beams:
          photon_iso = beam.Isocenter.Position
          diff = abs(photon_iso.z - target_center_z)
      if diff:
        if diff > 1:
          return t.fail(round(diff, 2))
        else:
          return t.succeed()

  # Tests if the plan has a target volume if the beam set label is U for 'Uten MV' and if the plan does not have a target volume and beam set label is M for 'Med MV'
  def label_target_volume_test(self):
    t = TEST.Test("Plan-teknikk og tilstedeværelse av målvolum bør stemme overens", True, self.label)
    if self.ts_plan.ts_case.has_target_volume and self.ts_label.label.technique in ('U', 'u'):
      return t.fail()
    elif not self.ts_plan.ts_case.has_target_volume and self.ts_label.label.technique in ('M', 'm'):
      return t.fail()
    else:
      return t.succeed()

  # Tests if the label usage of V for VMAT seems to make sense.
  def label_vmat_test(self):
    t = TEST.Test("Plan-teknikk for 'VMAT' og bruk av VMAT-teknikk skal stemme overens", False, self.label)
    if not self.ts_label.label.technique in ('S', 's'):
      if self.is_vmat() and not self.ts_label.label.technique in ('V', 'v'):
        t.expected = 'V'
        return t.fail(self.ts_label.label.technique)
      elif self.beam_set.DeliveryTechnique not in ['Arc','DynamicArc'] and self.ts_label.label.technique in ('V', 'v'):
        t.expected = 'U/M/I'
        return t.fail(self.ts_label.label.technique)
      else:
        return t.succeed()

  # Tests that the machine name is the one that is clinically validated (ALVersa).
  def machine_test(self):
    t = TEST.Test("Behandlingsapparat skal være:", 'ALVersa', self.machine)
    if not self.beam_set.MachineReference.MachineName == 'ALVersa':
      return t.fail(self.beam_set.MachineReference.MachineName)
    else:
      return t.succeed()

  # Tests if the isocentet name of the beams are 'Iso','ISO' or 'Iso1', 'ISO2' etc.
  def name_of_beam_iso_test(self):
    t = TEST.Test("Isosenter-navn på felt/buer skal være 'Iso' eller 'Iso1', 'Iso2' osv", True, self.name)
    match = False
    expected1 = 'Iso'
    expected2 = 'ISO'
    for beam in self.beam_set.Beams:
      if beam.Isocenter.Annotation.Name.lower() in ['iso','iso1','iso2','iso3','iso4','iso5','iso6','iso7','iso8','iso9']:
        return t.succeed()
      else:
        return t.fail(beam.Isocenter.Annotation.Name)

  # Tests correspondence of nr fractions in beam set with external value (from label).
  def nr_fractions_test(self):
    if self.ts_label.label.nr_fractions:
      expected = self.ts_label.label.nr_fractions
      t = TEST.Test("Antall fraksjoner i beam set skal stemme med antall fraksjoner i beam set label", expected, self.fractions)
      if self.beam_set.FractionationPattern.NumberOfFractions != int(expected):
        return t.fail(self.beam_set.FractionationPattern.NumberOfFractions)
      else:
        return t.succeed()

  # Tests that a sufficient low statistical uncertainty has been set (in the case of Electron Monte Carlo dose calculations).
  def electron_mc_uncertainty_test(self):
    t = TEST.Test("Statistisk usikkerhet for Monte Carlo doseberegning for elektroner skal være <= 0.1 %", '<=0.001', self.dose)
    if self.has_dose():
      if self.beam_set.FractionDose.DoseValues.AlgorithmProperties.DoseAlgorithm == 'ElectronMonteCarlo':
        if self.beam_set.FractionDose.DoseValues.AlgorithmProperties.MCStatisticalUncertaintyForFinalDose > 0.001:
          return t.fail(self.beam_set.FractionDose.DoseValues.AlgorithmProperties.MCStatisticalUncertaintyForFinalDose)
        else:
          return t.succeed()

  # Tests what photon energy is used for beam sets which are interpreted as being curative (would like to avoid 15 MV due to neutron production in these cases).
  def photon_energy_for_curative_fractionations_test(self):
    t = TEST.Test("Skal normalt ikke bruke 15MV.", '6 eller 10', self.energies)
    # The test can only be performed if a prescription is defined, and if the modality is photons:
    if self.has_prescription() and self.beam_set.Modality == 'Photons':
      energies = []
      for beam in self.beam_set.Beams:
        energies.append(beam.BeamQualityId)

      if '15' in energies:
        return t.fail('15')
      else:
        return t.succeed()

  # Tests that number of monitor units corresponds to fraction dose (within 20%) for the caudal part of conventional, locoregional breast plans.
  def prescription_mu_breast_regional_caudal_test(self):
    t = TEST.Test("Skal stå i forhold til fraksjonsdosen for beam-settet, det ser ut som MU kaudalt for isosenter avviker med mer enn 20% av fraksjonsdosen (cGy).", True, self.mu)
    mu_total_over = 0
    text = ""
    t.expected = RSU.fraction_dose(self.beam_set) * 100
    if not self.is_vmat():
      if self.ts_label.label.region in RC.breast_reg_codes:
        for beam in self.beam_set.Beams:
          segment_partial_area = []
          for index, segment in enumerate(beam.Segments):
            jaw = segment.JawPositions
            y1 = jaw[2]
            y2 = jaw[3]
            if y2 > 0:
              y2 = 0
            if y2 <= 0 and y1 < 0 or y1 < 0:
              leaf_positions = segment.LeafPositions
              mlc_y1 = int(math.floor((y1 + 20) * 2))
              mlc_y2 = int(math.ceil ((y2 + 20) * 2))-1
              segment_partial_area.extend([0])
              segment_partial_area[index] += (leaf_positions[1][mlc_y1] - leaf_positions[0][mlc_y1])*(((mlc_y1+1)-(y1+20)*2)/2)
              for mlc in range(mlc_y1+1, mlc_y2):
                segment_partial_area[index] += (leaf_positions[1][mlc] - leaf_positions[0][mlc])*0.5
              segment_partial_area[index] += (leaf_positions[1][mlc_y2] - leaf_positions[0][mlc_y2])*(((y2+20)*2-(mlc_y2))/2)
            else:
              segment_partial_area.extend([0])
          max_area = max(segment_partial_area)
          for index, segment in enumerate(beam.Segments):
            jaw = segment.JawPositions
            if segment_partial_area[index] > 1.5 and segment_partial_area[index]/max_area > 0.2 or round(jaw[3],1) <=0:
              mu_total_over += beam.BeamMU*segment.RelativeWeight
        if abs((mu_total_over - RSU.fraction_dose(self.beam_set) * 100) / (RSU.fraction_dose(self.beam_set) * 100) * 100) > 20:
          return t.fail(round(mu_total_over,1))
        else:
          return t.succeed()

  # Tests that number of monitor units corresponds to fraction dose (within 20%) for the cranial part of conventional, locoregional breast plans.
  def prescription_mu_breast_regional_cranial_test(self):
    t = TEST.Test("Skal stå i forhold til fraksjonsdosen for beam-settet, det ser ut som MU kranielt for isosenter avviker med mer enn 20% av fraksjonsdosen (cGy).", True, self.mu)
    mu_total_over = 0
    text = ""
    t.expected = RSU.fraction_dose(self.beam_set) * 100
    if not self.is_vmat():
      if self.ts_label.label.region in RC.breast_reg_codes:
        for beam in self.beam_set.Beams:
          segment_partial_area = []
          for index, segment in enumerate(beam.Segments):
            jaw = segment.JawPositions
            y1 = jaw[2]
            if y1 < 0:
              y1 = 0
            y2 = jaw[3]
            if y1 >= 0 and y2 > 0 or y2 > 0:
              leaf_positions = segment.LeafPositions
              mlc_y1 = int(math.floor((y1 + 20) * 2))
              mlc_y2 = int(math.ceil ((y2 + 20) * 2))-1
              segment_partial_area.extend([0])
              segment_partial_area[index] += (leaf_positions[1][mlc_y1] - leaf_positions[0][mlc_y1])*(((mlc_y1+1)-(y1+20)*2)/2)
              for mlc in range(mlc_y1+1, mlc_y2):
                segment_partial_area[index] += (leaf_positions[1][mlc] - leaf_positions[0][mlc])*0.5
              segment_partial_area[index] += (leaf_positions[1][mlc_y2] - leaf_positions[0][mlc_y2])*(((y2+20)*2-(mlc_y2))/2)
            else:
              segment_partial_area.extend([0])
          max_area = max(segment_partial_area)
          for index, segment in enumerate(beam.Segments):
            jaw = segment.JawPositions
            if segment_partial_area[index] > 1.5 and segment_partial_area[index]/max_area > 0.4 or round(jaw[2],1) >=0:
              mu_total_over += beam.BeamMU*segment.RelativeWeight
        if abs((mu_total_over - RSU.fraction_dose(self.beam_set) * 100) / (RSU.fraction_dose(self.beam_set) * 100) * 100) > 20:
          return t.fail(round(mu_total_over,1))
        else:
          return t.succeed()

  # Tests that number of monitor units corresponds to fraction dose (within 15 %) for conventional plans (non-VMAT) that is not locoregional breast.
  def prescription_mu_test(self):
    t = TEST.Test("Skal stå i forhold til fraksjonsdosen for beam-settet, bør som hovedregel være innenfor +/- 15% av fraksjonsdosen (cGy)", True, self.mu)
    mu_total = 0
    for beam in self.beam_set.Beams:
      mu_total += beam.BeamMU
    if not self.is_vmat():
      if not self.ts_label.label.region in RC.breast_reg_codes:
        # Naive approximation only relevant for conventional plans (not VMAT):
        # Sum of monitor units compared to fraction dose (+/- 15% of 100Mu/Gy):
        percent_dev = (mu_total - RSU.fraction_dose(self.beam_set) * 100) / (RSU.fraction_dose(self.beam_set) * 100) * 100
        t.expected = RSU.fraction_dose(self.beam_set) * 100
        if abs(percent_dev) > 15:
          return t.fail(round(mu_total, 1))
        else:
          return t.succeed()

  # Tests if the sequence of beam collimator angles are reasonable.
  # Note that this test only returns one beam in case of several beams with unreasonable values.
  def reasonable_collimator_angles_test(self):
    t = TEST.Test("Tilsynelatende upraktisk stort hopp i kollimatorvinkel brukt på dette feltet i forhold til det forrige. Samme feltform kan oppnås i et mer optimalt oppsett med kollimatorvinkel rotert 180 grader i forhold til gjeldende vinkel.", '', self.collimator_angles)
    previous_beam_collimator_angle = 0
    unreasonable_beam = None
    expected_angle = None
    for beam in self.beam_set.Beams:
      coll_delta = RSU.practical_angle_delta(previous_beam_collimator_angle, beam.InitialCollimatorAngle)
      if coll_delta > 90:
        # In case of a suboptimal collimator angle being used, the 'correct' angle will be
        unreasonable_beam = beam
        expected_angle = RSU.proper_angle(round(beam.InitialCollimatorAngle - 180, 1))
      previous_beam_collimator_angle = beam.InitialCollimatorAngle
    if unreasonable_beam:
      t.expected = expected_angle
      return t.fail(round(beam.InitialCollimatorAngle, 1))
    else:
      return t.succeed()

  # Tests the presence of "Create setup beams" (it should be deactivated).
  def setup_beams_test(self):
    t = TEST.Test("'Create setup beams' skal ikke være aktivert", False, self.param)
    if self.beam_set.PatientSetup.UseSetupBeams:
      return t.fail(True)
    else:
      return t.succeed()

  # Tests that delivery technique is among the 3 white listed: VMAT (Arc), 3DCRT or IMRT (SMLC).
  def technique_test(self):
    t = TEST.Test("Plan-teknikk skal være en av disse", ['3D-CRT', 'SMLC', 'VMAT'], self.technique)
    if not self.beam_set.DeliveryTechnique in ('Arc', 'SMLC', '3DCRT','DynamicArc'):
      return t.fail(self.beam_set.DeliveryTechnique)
    else:
      return t.succeed()

  # Tests presence of unmerged (static) beams.
  def unmerged_beams_test(self):
    t = TEST.Test('Når Beam-settet inneholder felt som har identisk gantry- og kollimator-vinkel, skal i utgangspunktet disse være sammeslått (merge).', True, self.param)
    # It doesn't make sense to run this test on VMAT plans (since we don't merge arcs):
    if self.beam_set.DeliveryTechnique != 'DynamicArc':
      gantry_and_coll_angles = set([])
      has_unmerged_beams = None
      for beam in self.beam_set.Beams:
        beam_angles = str(beam.GantryAngle) + '-' + str(beam.InitialCollimatorAngle)
        if beam_angles in gantry_and_coll_angles:
          has_unmerged_beams = True
        else:
          gantry_and_coll_angles.add(beam_angles)
      if has_unmerged_beams:
        return t.fail(True)
      else:
        return t.succeed()

  # Tests that in cases of full arcs, if the last arc of the beam set is clockwise, which gives a more efficient patient takedown.
  def vmat_full_arc_rotation_of_last_beam_test(self):
    t = TEST.Test("Siste bue i en VMAT plan skal som hovedregel være med klokken når det er en full bue", 'Clockwise', self.vmat)
    # Get the last beam:
    if self.has_beam():
      beam = self.beam_set.Beams[self.beam_set.Beams.Count - 1]
      if self.is_vmat() and abs(beam.ArcStopGantryAngle - beam.GantryAngle) < 10:
        if not beam.ArcRotationDirection == 'Clockwise':
          return t.fail(beam.ArcRotationDirection)
        else:
          return t.succeed()

  # Tests for optimal arc sequencing
  # (that the start angle of following arcs are equal to the stop angle of the previous arc).
  def vmat_arc_sequence_test(self):
    t = TEST.Test("Ved flerbue-oppsett bør påfølgende buer ha startvinkel lik stoppvinkel til forrige bue", None, self.vmat)
    if self.is_vmat():
      previous_gantry_stop_angle = None
      failed_beam = None
      for beam in self.beam_set.Beams:
        if previous_gantry_stop_angle:
          if beam.GantryAngle != previous_gantry_stop_angle:
            failed_beam = beam.Number
        previous_gantry_stop_angle = beam.ArcStopGantryAngle
      if failed_beam:
        return t.fail(failed_beam)
      else:
        return t.succeed()

  # Tests if the total number of MUs is below 2.5*fraction dose (cGy).
  # (plus a margin of 5 MU to avoid getting a lot of marginally positive outcomes on this test)
  def vmat_mu_test(self):
    t = TEST.Test("Bør som hovedregel være innenfor 2.5*fraksjonsdose (cGy) (+/- 5 MU)", True, self.mu)
    mu_total = 0
    if self.has_prescription():
      # Do not run MU test on SBRT plans:
      if self.ts_label.label.valid and self.ts_label.label.technique.upper() != 'S':
        t.expected = "<" + str(round(RSU.fraction_dose(self.beam_set) * 250 + 5, 1))
        if self.is_vmat():
          for beam in self.beam_set.Beams:
            mu_total += beam.BeamMU
          if mu_total > RSU.fraction_dose(self.beam_set) * 250 + 5:
            return t.fail(round(mu_total, 1))
          else:
            return t.succeed()

  # Tests for SIB plans, if the lower dose volumes is normalised to the correct value (within 0.5 %).
  def target_volume_normalisation_for_sib_test(self):
    if self.ts_label.label.region in RC.prostate_codes + RC.breast_codes + RC.rectum_codes:
      ss = self.ts_structure_set().structure_set
      roi_dict = SSF.create_roi_dict(ss)
      potential_target_volumes = [ROIS.ctv_47.name, ROIS.ctv_56.name, ROIS.ctv_70_sib.name, ROIS.ctv_57.name]
      # Create a dictionary of all CTVs defined as an objective:
      objective_target_volumes = {}
      po = RSU.plan_optimization(self.ts_plan.plan, self.beam_set)
      if po and po.Objective:
        for objective in po.Objective.ConstituentFunctions:
          if objective.ForRegionOfInterest.Type == 'Ctv':
            objective_target_volumes[objective.ForRegionOfInterest.Name] = True
      # Check in the list of potential SIB volumes if any exist in the structure set, define as target
      for i in range(len(potential_target_volumes)):
        if roi_dict.get(potential_target_volumes[i]):
          target = potential_target_volumes[i]
          t = TEST.Test("Skal stemme overens (innenfor 0.5%) med aktuell dose for normeringsvolumet " + target + ".", True, self.norm_dose)
          # Check if the target was used as objective
          if objective_target_volumes.get(target):
            # Use the two last characters in the target-string to find the wanted median dose of that target volume
            prescription_dose = int(target[-2:])
            if prescription_dose > 30:
              low_dose = round(prescription_dose * 0.995, 2)
              high_dose = round(prescription_dose * 1.005, 2)
              real_dose_d50 = RSU.gy(self.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = target, RelativeVolumes = [0.50])[0]) * self.beam_set.FractionationPattern.NumberOfFractions
              t.expected = ">" + str(low_dose) + " og " + "<" +str(high_dose)
              if real_dose_d50 < low_dose or real_dose_d50 > high_dose:
                t.fail(round(real_dose_d50, 2))
              else:
                t.succeed()
