# encoding: utf8

# Contains treatment plan tests for individual beam sets.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
import math
#sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\RayStation\\lib".decode('utf8'))

# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *

# Local script imports:
import test as TEST
import raystation_utilities as RSU
import rois as ROIS
import region_codes as RC

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
    self.grid = TEST.Parameter('Beregningsmatrise', '', self.param)
    self.max_leaf_dist = TEST.Parameter('Parameter', '', self.param)
    self.couch = TEST.Parameter('Bordtopp', '', self.param)
    self.mlc = TEST.Parameter('MLC', '', self.param)
    self.name = TEST.Parameter('Navn', '', self.param)
    self.breast = TEST.Parameter('Geometri', '', self.param)
    self.norm_dose = TEST.Parameter('Dose', '', self.param)
    self.isocenter = TEST.Parameter('Isosenter','', self.param)
    self.mu = TEST.Parameter('MU', '', self.param)


  # Gives the fraction dose (in Gy):
  def fraction_dose(self):
    return (self.beam_set.Prescription.PrimaryDosePrescription.DoseValue / 100.0) / self.beam_set.FractionationPattern.NumberOfFractions

  # Gives the ts_structure_set which corresponds with this beam set:
  #def ts_structure_set(self):
  #  for ts_struct in self.ts_plan.ts_case.ts_structure_sets:
  #    if ts_struct.structure_set.OnExamination == self.beam_set.GetPlanningExamination():
   #     return ts_struct

    # Gives the ts_structure_set which corresponds with this beam set:
  def ts_structure_set(self):
    for ts_struct in self.ts_plan.ts_case.ts_structure_sets:
      if ts_struct.structure_set.OnExamination == self.beam_set.GetPlanningExamination():
        return ts_struct

  # Tests presence of unmerged beams.
  def unmerged_beams_test(self):
    t = TEST.Test('Når Beam-settet inneholder felt som har identisk gantry- og kollimator-vinkel, skal i utgangspunktet disse være sammeslått (merge).', True, self.param)
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

  # Tests that delivery technique is among the 3 white listed: VMAT (Arc), 3DCRT or IMRT (SMLC)
  def technique_test(self):
    t = TEST.Test("Plan-teknikk skal være en av disse", ['3D-CRT', 'SMLC', 'VMAT'], self.technique)
    if not self.beam_set.DeliveryTechnique in ('Arc', 'SMLC', '3DCRT'):
      return t.fail(self.beam_set.DeliveryTechnique)
    else:
      return t.succeed()

  # Tests that the machine is among the 2 white listed: ALVersa & ALVersa_FFF
  def machine_test(self):
    t = TEST.Test("Behandlingsapparat skal være en av disse", ['ALVersa', 'ALVersa_FFF'], self.machine)
    if not self.beam_set.MachineReference.MachineName in ('ALVersa', 'ALVersa_FFF'):
      return t.fail(self.beam_set.MachineReference.MachineName)
    else:
      return t.succeed()

  # Tests the presence of "Create setup beams" (it should be deactivated).
  def setup_beams_test(self):
    t = TEST.Test("'Create setup beams' skal ikke være aktivert", False, self.param)
    if self.beam_set.PatientSetup.UseSetupBeams:
      return t.fail(True)
    else:
      return t.succeed()

  # Tests the presence of a dose calculation.
  def dose_test(self):
    t = TEST.Test("Skal være definert", True, self.dose)
    if not self.beam_set.FractionDose.DoseValues:
      return t.fail()
    else:
      return t.succeed()

  # Tests that the dose status is 'clinical'.
  def dose_is_clinical_test(self):
    t = TEST.Test("Beregning skal være markert som 'klinisk'", True, self.dose)
    if self.beam_set.FractionDose.DoseValues:
      if self.beam_set.FractionDose.DoseValues.IsClinical:
        return t.succeed()
      else:
        return t.fail()

  # Tests that the dose algorithm is among the 2 white listed: CCDose & ElectronMonteCarlo
  def dose_algorithm_test(self):
    t = TEST.Test("Algoritme skal være en av disse", ['CCDose', 'ElectronMonteCarlo'], self.dose)
    if self.beam_set.FractionDose.DoseValues:
      if self.beam_set.FractionDose.DoseValues.AlgorithmProperties.DoseAlgorithm in ['CCDose', 'ElectronMonteCarlo']: # other plausible value: 'Mixed'
        return t.succeed()
      else:
        return t.fail(self.beam_set.FractionDose.DoseValues.AlgorithmProperties.DoseAlgorithm)

  # Tests that a sufficient number of histories has been used (in the case of Electron Monte Carlo calculations).
  def number_of_histories_test(self):
    t = TEST.Test("Antall historier skal være minst 200.000", '>=200000', self.dose)
    if self.beam_set.FractionDose.DoseValues:
      if self.beam_set.FractionDose.DoseValues.AlgorithmProperties.DoseAlgorithm == 'ElectronMonteCarlo':
        if self.beam_set.FractionDose.DoseValues.AlgorithmProperties.ElectronMCHistoriesPerAreaFluence < 200000:
          return t.fail(beam_set.FractionDose.DoseValues.AlgorithmProperties.ElectronMCHistoriesPerAreaFluence)
        else:
          return t.succeed()

  # Tests if the energies of the beams in the beam set are the same.
  def beam_energy_equality_test(self):
    wanted_energy = 6
    t = TEST.Test("Det skal i utgangspunktet benyttes samme energi for alle felt i et beam set. Kun ved særskilte kliniske begrunnelser skal dette avvikes.", wanted_energy, self.energies)
    energies = []
    for beam in self.beam_set.Beams:
      energies.append(beam.MachineReference.Energy)
    if len(set(energies)) > 1:
      return t.fail(energies)
    else:
      return t.succeed()

  # Tests if the energies of the beams in the beam set are the same as the expected energy.
  def specific_energy_for_region_test(self):
    wanted_energy = 6 # (default)
    if self.ts_label.label.region in RC.brain_whole_codes:
      if self.beam_set.DeliveryTechnique != 'Arc':
        wanted_energy = 10
    t = TEST.Test("Det skal i utgangspunktet benyttes gitt energi for denne behandlingsregionen.", wanted_energy, self.energies)
    energies = []
    for beam in self.beam_set.Beams:
      energies.append(beam.MachineReference.Energy)
    if set(energies) != set([wanted_energy]):
      return t.fail(energies)
    else:
      return t.succeed()


  # Tests if the label usage of V for VMAT seems to make sense.
  def label_vmat_test(self):
    t = TEST.Test("Plan-teknikk for 'VMAT' og bruk av VMAT-teknikk skal stemme overens", False, self.label)
    if not self.ts_label.label.technique in ('S', 's'):
      if self.beam_set.DeliveryTechnique == 'Arc' and not self.ts_label.label.technique in ('V', 'v'):
        t.expected = 'V'
        return t.fail(self.ts_label.label.technique)
      elif self.beam_set.DeliveryTechnique != 'Arc' and self.ts_label.label.technique in ('V', 'v'):
        t.expected = 'U/M/I'
        return t.fail(self.ts_label.label.technique)
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


  # Tests what photon energy is used for beam sets which are interpreted as being curative (would like to avoid 15 MV due to neutron production in these cases).
  def photon_energy_for_curative_fractionations_test(self):
    t = TEST.Test("Skal normalt ikke bruke 15MV ved 'kurativ' fraksjonering (av hensyn til nøytronproduksjon)", '6 eller 10', self.energies)
    # The test can only be performed if a prescription is defined, and if the modality is photons:
    if self.beam_set.Prescription.PrimaryDosePrescription and self.beam_set.Modality == 'Photons':
      energies = []
      for beam in self.beam_set.Beams:
        energies.append(beam.MachineReference.Energy)
      # Define treatment as curative if fraction dose is less than 2.5 Gy (FIXME: This is of course extremely naive!!):
      if self.fraction_dose < 2.5:
        if 15 in energies:
          return t.fail(15)
        else:
          return t.succeed()

  # Tests that in cases of full arcs, if the last arc of the beam set is clockwise, which gives a more efficient patient takedown.
  def vmat_full_arc_rotation_of_last_beam_test(self):
    t = TEST.Test("Siste bue i en VMAT plan skal som hovedregel være med klokken når det er en full bue", 'Clockwise', self.vmat)
    # Get the last beam:
    if len(list(self.beam_set.Beams)) > 0:
      beam = self.beam_set.Beams[self.beam_set.Beams.Count - 1]
      if beam.ArcRotationDirection != 'None' and abs(beam.ArcStopGantryAngle - beam.GantryAngle) < 10:
        if not beam.ArcRotationDirection == 'Clockwise':
          return t.fail(beam.ArcRotationDirection)
        else:
          return t.succeed()

  # Tests that sequential arcs have opposite rotation direction.
  def vmat_arc_sequence_test(self):
    t = TEST.Test("Ved flerbue-oppsett skal påfølgende buer ha motsatt rotasjonsretning", None, self.vmat)
    previous_arc_direction = None
    failed_beam = None
    if self.beam_set.DeliveryTechnique == 'Arc':
      for beam in self.beam_set.Beams:
        if previous_arc_direction:
          if beam.ArcRotationDirection == previous_arc_direction:
            failed_beam = beam.Number
        previous_arc_direction = beam.ArcRotationDirection
      if failed_beam:
        return t.fail(failed_beam)
      else:
        return t.succeed()

  # Tests correspondence of nr fractions in beam set with external value (from label).
  def nr_fractions_test(self):
    if self.ts_label.label.nr_fractions:
      expected = self.ts_label.label.nr_fractions
      t = TEST.Test("Antall fraksjoner i beam set skal stemme med antall fraksjoner i beam set label", expected, self.fractions)
      if self.beam_set.FractionationPattern.NumberOfFractions != int(expected):
        return t.fail(self.beam_set.FractionationPattern.NumberOfFractions)
      else:
        return t.succeed()

  # Tests if the sequence of beam collimator angles are reasonable.
  # FIXME: I suspect there are cases where this test doesnt give the correct result...
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

  #Tests if prescription in defined
  def defined_prescription_test(self):
    t = TEST.Test("Skal være definert.", True, self.defined_prescription)
    if self.beam_set.Prescription.PrimaryDosePrescription:
      return t.succeed()
    else:
      return t.fail()


  # Tests if the default grid size of 0.3x0.3x0.3 cm^3 is used, unless the plan is stereotactic, then the grid size should be 0.1x0.1x0.1 cm^3 for brain and 0.2x0.2x0.2 cm^3 for lung.
  def dose_grid_test(self):
    t = TEST.Test("Skal i utgangspunktet bruke dosegrid: 0.3x0.3x0.3 cm^3.", True, self.grid)
    t2 = TEST.Test("Skal i utgangspunktet bruke dosegrid: 0.2x0.2x0.2 cm^3.", True, self.grid)
    ts = TEST.Test("Skal i utgangspunktet bruke dosegrid: 0.1x0.1x0.1 cm^3 ved siste final dose.", True, self.grid)
    tsl = TEST.Test("Skal i utgangspunktet bruke dosegrid: 0.2x0.2x0.2 cm^3 ved siste final dose.", True, self.grid)
    grid = self.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].ForTreatmentSetup.FractionDose.InDoseGrid.VoxelSize
    if self.ts_label.label.technique:
      if self.ts_label.label.technique.upper() == 'S':
        if self.ts_label.label.region in RC.brain_partial_codes:
          if grid.x != 0.1 or grid.y != 0.1 or grid.z != 0.1:
            ts.fail(grid.x)
          else:
            ts.succeed()
        else:
          if grid.x != 0.2 or grid.y != 0.2 or grid.z != 0.2:
            tsl.fail(grid.x)
          else:
            tsl.succeed()
      else:
        if self.ts_label.label.region in RC.prostate_codes:
          if grid.x != 0.2 or grid.y != 0.2 or grid.z != 0.2:
            t2.fail(grid.x)
          else:
            t2.succeed()
        elif grid.x != 0.3 or grid.y != 0.3 or grid.z != 0.3:
            return t.fail(grid.x)
        else:
          return t.succeed()

 # Tests if Constrain leaf motion of 0.3 cm/deg is used for stereotactic plans.
  def max_leaf_distance_test(self):
    t = TEST.Test("Skal i utgangspunktet bruke Constrain leaf motion = 0.3 cm/deg", True, self.max_leaf_dist)
    t.expected = 0.3
    if self.ts_label.label.technique:
      if self.ts_label.label.technique.upper() == 'S':
        if self.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties.UseMaxLeafTravelDistancePerDegree:
          if self.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree <= 0.3:
            return t.succeed()
          else:
            return t.fail(self.ts_plan.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree)
        else:
          return t.fail()


  #Tests if the couch top is placed close to the patient
  def couch_close_to_patient_test(self):
    t = TEST.Test("Bordtopp-ROI (Couch) skal ligge inntil external", True, self.couch)
    for structure_set in self.ts_plan.ts_case.case.PatientModel.StructureSets:
      if self.ts_label.label.technique:
        if self.ts_label.label.technique.upper() != 'S':
          if self.ts_label.label.region not in RC.brain_codes:
            for roi in self.ts_structure_set().structure_set.RoiGeometries:
              if roi.OfRoi.Name == ROIS.couch.name and roi.HasContours():
                for r in self.ts_structure_set().structure_set.RoiGeometries:
                  if r.OfRoi.Name == ROIS.external.name and r.HasContours():
                    couch = self.ts_structure_set().structure_set.RoiGeometries[ROIS.couch.name].GetBoundingBox()
                    external = self.ts_structure_set().structure_set.RoiGeometries[ROIS.external.name].GetBoundingBox()
                    if abs(couch[1].y - external[1].y) > 15 or abs(couch[1].y - external[1].y) < 5.41:
                      return t.fail()




 # Tests that, for conventional plans, the first MLC leaf behind the collimator is at the same posiition as the first MLC leaf inside the field.
  def guard_leaf_test(self):
    failed_beams = []
    t = TEST.Test("Første MLC blad utenfor blender skal være på samme posisjon som første MLC blad innenfor blender", None, self.mlc)
    if self.beam_set.DeliveryTechnique != 'Arc':
      for beam in self.beam_set.Beams:
        for [segment_index, segment] in enumerate(beam.Segments):
          assert (segment.LeafPositions.Length == 2)
          leaf_positions = segment.LeafPositions
          jaw = segment.JawPositions
          # array (x1,x2,y1,y2)  we are looking at Y1 and Y2.
          y1 = jaw[2]
          y2 = jaw[3]
          if -1 < y1 < 1:
            # get the last corresponding MLC that is in the field
            mlcY1 = math.floor((y1 + 20) * 2) + 1.0
            # don't forget that mlc 50 is in spot leafPositions[0][49]
            if (mlcY1 - 2) > 0:
              if round(abs(leaf_positions[0][mlcY1 - 2]), 3) - round(abs(leaf_positions[0][mlcY1 - 1]), 3) > 0.2 or round(abs(leaf_positions[1][mlcY1 - 2]), 3) - round(abs(leaf_positions[1][mlcY1 - 1]), 3) > 0.2:
                if round(beam.BeamMU*segment.RelativeWeight, 2) > 20:
                  failed_beams.append(str(beam.Name.decode('utf8', 'replace')))
          elif -1< y2 < 1:
            mlcY2 = math.ceil ((y2 + 20) * 2)
            if mlcY2 < 80:
              if round(abs(leaf_positions[0][mlcY2]), 3) - round(abs(leaf_positions[0][mlcY2 - 1]), 3) > 0.2 or round(abs(leaf_positions[1][mlcY2]), 3)  - round(abs(leaf_positions[1][mlcY2 - 1]), 3) > 0.2:
                if round(beam.BeamMU*segment.RelativeWeight, 2) > 20:
                  failed_beams.append(str(beam.Name.decode('utf8', 'replace')))

        if len(failed_beams) >= 1:
          return t.fail(list(set(failed_beams)))
        else:
          return t.succeed()


  # Tests that number of monitor units corresponds to fraction dose (within 20%) for the caudal part of conventional, locoregional breast plans.
  def prescription_mu_breast_regional_caudal_test(self):
    t = TEST.Test("Skal stå i forhold til fraksjonsdosen for beam-settet, det ser ut som MU kaudalt for isosenter avviker med mer enn 20% av fraksjonsdosen (cGy).", True, self.mu)
    mu_total_under = 0
    t.expected = RSU.fraction_dose(self.beam_set) * 100
    if self.beam_set.DeliveryTechnique != 'Arc':
      if self.ts_label.label.region in RC.breast_reg_codes:
        for beam in self.beam_set.Beams:
          for segment in beam.Segments:
            jaw = segment.JawPositions
            y1 = jaw[2]
            y2 = jaw[3]
            if y1 < 0 or y2 < 0:
              mu_total_under += beam.BeamMU*segment.RelativeWeight
        if abs((mu_total_under - RSU.fraction_dose(self.beam_set) * 100) / (RSU.fraction_dose(self.beam_set) * 100) * 100) > 20:
          return t.fail(round(mu_total_under, 1))
        else:
          return t.succeed()


  # Tests that number of monitor units corresponds to fraction dose (within 20%) for the cranial part of conventional, locoregional breast plans.
  def prescription_mu_breast_regional_cranial_test(self):
    t = TEST.Test("Skal stå i forhold til fraksjonsdosen for beam-settet, det ser ut som MU kranielt for isosenter avviker med mer enn 20% av fraksjonsdosen (cGy).", True, self.mu)
    mu_total_over = 0
    t.expected = RSU.fraction_dose(self.beam_set) * 100
    if self.beam_set.DeliveryTechnique != 'Arc':
      if self.ts_label.label.region in RC.breast_reg_codes:
        for beam in self.beam_set.Beams:
          for segment in beam.Segments:
            jaw = segment.JawPositions
            y1 = jaw[2]
            y2 = jaw[3]
            if y1 >= 0 or y2 > 0:
              mu_total_over += beam.BeamMU*segment.RelativeWeight
        if abs((mu_total_over - RSU.fraction_dose(self.beam_set) * 100) / (RSU.fraction_dose(self.beam_set) * 100) * 100) > 20:
          return t.fail(round(mu_total_over, 1))
        else:
          return t.succeed()


  # Tests that number of monitor units corresponds to fraction dose (within 15 %) for conventional plans (non-VMAT) that is not locoregional breast.
  def prescription_mu_test(self):
    t = TEST.Test("Skal stå i forhold til fraksjonsdosen for beam-settet, bør som hovedregel være innenfor +/- 15% av fraksjonsdosen (cGy)", True, self.mu)
    mu_total = 0
    for beam in self.beam_set.Beams:
      mu_total += beam.BeamMU
    if self.beam_set.DeliveryTechnique != 'Arc':
      if not self.ts_label.label.region in RC.breast_reg_codes:
        # Naive approximation only relevant for conventional plans (not VMAT):
        # Sum of monitor units compared to fraction dose (+/- 15% of 100Mu/Gy):
        percent_dev = (mu_total - RSU.fraction_dose(self.beam_set) * 100) / (RSU.fraction_dose(self.beam_set) * 100) * 100
        t.expected = RSU.fraction_dose(self.beam_set) * 100
        if abs(percent_dev) > 15:
          return t.fail(round(mu_total, 1))
        else:
          return t.succeed()


  def stereotactic_mu_test(self):
    t = TEST.Test("Bør som hovedregel være innenfor 1.4*fraksjonsdose (cGy)", True, self.mu)
    mu_total = 0
    if self.defined_prescription_test():
      t.expected = "<" + str(RSU.fraction_dose(self.beam_set) * 140)
      if self.ts_label.label.technique:
        if self.ts_label.label.technique.upper() == 'S':
          for beam in self.beam_set.Beams:
            mu_total += beam.BeamMU
          if mu_total > RSU.fraction_dose(self.beam_set) * 140:
            return t.fail(round(mu_total, 1))
          else:
            return t.succeed()

  def vmat_mu_test(self):
    t = TEST.Test("Bør som hovedregel være innenfor 2.5*fraksjonsdose (cGy)", True, self.mu)
    mu_total = 0
    if self.defined_prescription_test():
      t.expected = "<" + str(RSU.fraction_dose(self.beam_set) * 250)
      if self.beam_set.DeliveryTechnique == 'Arc':
        for beam in self.beam_set.Beams:
          mu_total += beam.BeamMU
        if mu_total > RSU.fraction_dose(self.beam_set) * 250:
          return t.fail(round(mu_total, 1))
        else:
          return t.succeed()

  #Tests if the isocentet name of the beams are 'Iso','ISO' or 'Iso1', 'ISO1' etc. The plan label, for example '401V:0-70:35 1' is also allowed.
  def name_of_beam_iso_test(self):
    t = TEST.Test("Isosenter-navn på felt/buer skal være 'Iso' eller 'Iso1', 'Iso2' osv", True, self.name)
    match = False
    expected1 = 'Iso'
    expected2 = 'ISO'
    for beam in self.beam_set.Beams:
      if beam.Isocenter.Annotation.Name in ('Iso','ISO'):
        match = True
      elif not beam.Isocenter.Annotation.Name in ('Iso','ISO'):
        if beam.Isocenter.Annotation.Name in ('Iso1','ISO1','Iso2','ISO2','Iso3','ISO3'):
          match = True
      elif self.ts_label.label.nr_fractions and len(self.ts_label.label.parts) == 3 and self.ts_label.label.nr_fractions.isdigit() and self.ts_label.label.technique.isalpha() and self.ts_label.label.region and self.ts_label.label.region.isdigit() and len(self.ts_label.label.middle_parts) == 2:
        if beam.Isocenter.Annotation.Name == (str(self.beam_set.DicomPlanLabel) + ' 1'):
          match = True
      if match:
        return t.succeed()
      else:
        return t.fail(beam.Isocenter.Annotation.Name.decode('utf8', 'replace'))

  #Tests if breast patients having a boost of 2 Gy x 8 has 'Clips' defined
  def breast_seeds_test(self):
    t = TEST.Test("Mammae-pasienter som skal ha ungdomsboost skal ha " + ROIS.clips.name + " definert.", True, self.breast)
    for structure_set in self.ts_plan.ts_case.case.PatientModel.StructureSets:
      if self.ts_label.label.region:
        if self.ts_label.label.region in RC.breast_codes:
          if self.ts_label.label.nr_fractions== '8':
            match = False
            for rg in structure_set.RoiGeometries:
              if rg.OfRoi.Name == ROIS.clips.name and rg.HasContours():
                match = True
            if match:
              return t.succeed()
            else:
              return t.fail()

 #Tests for prostate SIB plans, if the 'CTV 0-70' and 'CTV 0-56' volumes are normalised to the correct value, within 0.5%.
  def prostate_normalisation_test(self):
    t_70 = TEST.Test("Skal stemme overens (innenfor 0.5%) med aktuell dose for nomeringsvolum " + ROIS.ctv_70_sib.name + ".", True, self.norm_dose)
    t_56 = TEST.Test("Skal stemme overens (innenfor 0.5%) med aktuell dose for nomeringsvolum " + ROIS.ctv_56.name + ".", True, self.norm_dose)
    t_56.expected = 56
    t_70.expected = 70
    for structure_set in self.ts_plan.ts_case.case.PatientModel.StructureSets:
      if self.ts_label.label.region in RC.prostate_codes:
        if self.ts_label.label.nr_fractions == '35':
          match = False
          cum_pr_dose = RSU.prescription_dose(self.beam_set)
          diff_pr_dose = RSU.differential_prescription_dose(self.ts_plan.plan, self.beam_set)
          low_dose_70 = 70 * 0.995
          high_dose_70 = 70 * 1.005
          low_dose_56 = 56 * 0.995
          high_dose_56 = 56 * 1.005
          for rg in structure_set.RoiGeometries:
            if rg.OfRoi.Name == ROIS.ctv_70_sib.name:
              real_dose_d50_70 = RSU.gy(self.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = ROIS.ctv_70_sib.name, RelativeVolumes = [0.50])[0]) * self.beam_set.FractionationPattern.NumberOfFractions
              if real_dose_d50_70 < low_dose_70 or real_dose_d50_70 > high_dose_70:
                t_70.fail(round(real_dose_d50_70, 2))
              else:
                t_70.succeed()
            elif rg.OfRoi.Name == ROIS.ctv_56.name:
              real_dose_d50_56 = RSU.gy(self.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = ROIS.ctv_56.name, RelativeVolumes = [0.50])[0]) * self.beam_set.FractionationPattern.NumberOfFractions
              #t_56.fail(round(real_dose_d50_56, 2))
              if real_dose_d50_56 < low_dose_56 or real_dose_d50_56 > high_dose_56:
                t_56.fail(round(real_dose_d50_56, 2))
              else:
                t_56.succeed()


 #Tests for recti SIB plans, if the 'CTV 0-47' volume is normalised to the correct value, within 0.5%.
  def recti_normalisation_test(self):
    t_47 = TEST.Test("Skal stemme overens (innenfor 0.5%) med aktuell dose for nomeringsvolumet " + ROIS.ctv_47.name +".", True, self.norm_dose)
    for structure_set in self.ts_plan.ts_case.case.PatientModel.StructureSets:
      if self.ts_label.label.region not in RC.rectum_codes:
        if self.ts_label.label.nr_fractions == '25':
          match = False
          cum_pr_dose = RSU.prescription_dose(self.beam_set)
          diff_pr_dose = RSU.differential_prescription_dose(self.ts_plan.plan, self.beam_set)
          low_dose_47 = round(47 * 0.995, 2)
          high_dose_47 = round(47 * 1.005, 2)
          for rg in structure_set.RoiGeometries:
            if rg.OfRoi.Name == ROIS.ctv_47.name and rg.OfRoi.Type == 'Ctv':
              real_dose_d50_47 = RSU.gy(self.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = ROIS.ctv_47.name, RelativeVolumes = [0.50])[0]) * self.beam_set.FractionationPattern.NumberOfFractions
              t_47.expected = "<" + str(low_dose_47) + " - " + str(high_dose_47) + ">"
              if real_dose_d50_47 < low_dose_47 or real_dose_d50_47 > high_dose_47:
                t_47.fail(round(real_dose_d50_47, 2))
              else:
                t_47.succeed()

 #Tests for breast SIB plans, if the 'CTV 0-47' volume is normalised to the correct value, within 0.5%.
  def breast_normalisation_test(self):
    t_47 = TEST.Test("Skal stemme overens (innenfor 0.5%) med aktuell dose for nomeringsvolumet " + ROIS.ctv_47.name +".", True, self.norm_dose)
    for structure_set in self.ts_plan.ts_case.case.PatientModel.StructureSets:
      if self.ts_label.label.region in RC.breast_reg_codes:
        if self.ts_label.label.nr_fractions== '25':
          match = False
          cum_pr_dose = RSU.prescription_dose(self.beam_set)
          diff_pr_dose = RSU.differential_prescription_dose(self.ts_plan.plan, self.beam_set)
          low_dose_47 = round(47 * 0.995, 2)
          high_dose_47 = round(47 * 1.005, 2)
          for rg in structure_set.RoiGeometries:
            if rg.OfRoi.Name == ROIS.ctv_47.name and rg.OfRoi.Type == 'Ctv':
              real_dose_d50_47 = RSU.gy(self.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = ROIS.ctv_47.name, RelativeVolumes = [0.50])[0]) * self.beam_set.FractionationPattern.NumberOfFractions
              t_47.expected = "<" + str(low_dose_47) + " - " + str(high_dose_47) + ">"
              if real_dose_d50_47 < low_dose_47 or real_dose_d50_47 > high_dose_47:
                t_47.fail(round(real_dose_d50_47, 2))
              else:
                t_47.succeed()

  # Tests that the isocenter coordinate is reasonably centered in the normalisation volume (in the longitudinal direction).
  #An exception is for prostate plans with pelvic lymph nodes, here you want to use this volume. Another exception is for non-VMAT breast plans, where the isocenter is often placed more cranially.
  def isocenter_centered_long_test(self):
    t = TEST.Test("Isosenter skal i utgangspunktet være mest mulig sentrert i long-retning, avstand mellom isosenter og senter av normeringsvolumet bør være mindre enn 1 cm", '<1 cm', self.isocenter)
    if self.beam_set.Modality == 'Photons':
      diff = 0
      ss = self.ts_structure_set().structure_set
      target0 = None
      target1 = None
      for roi in ss.RoiGeometries:
        if roi.OfRoi.Type == 'Ptv' and roi.PrimaryShape:
          # Determine if this target volume is relevant for this beam set (by checking if it is used as an objective):
          po = RSU.plan_optimization(self.ts_plan.plan, self.beam_set)
          if po:
            for objective in po.Objective.ConstituentFunctions:
              if objective.ForRegionOfInterest.Name == roi.OfRoi.Name:
                current_target = roi.GetBoundingBox()
                if target0 == None or current_target[0].z < target0:
                  target0 = current_target[0].z
                if target1 == None or current_target[1].z > target1:
                  target1 = current_target[1].z
      if self.beam_set.DeliveryTechnique == 'Arc':
        if target0 and target1:
          target_center_z = target0 + 0.5*abs(target0 - target1)
          for beam in self.beam_set.Beams:
            photon_iso = beam.Isocenter.Position
            diff = abs(photon_iso.z - target_center_z)
      elif self.beam_set.DeliveryTechnique != 'Arc':
        if not self.ts_label.label.region in RC.conventional_and_vmat_site_codes:
          if self.beam_set.Modality == 'Photons':
            for beam in self.beam_set.Beams:
              photon_iso = beam.Isocenter.Position
              for rg in self.ts_structure_set().structure_set.RoiGeometries:
                if rg.OfRoi.Name == self.beam_set.Prescription.PrimaryDosePrescription.OnStructure.Name:
                  target = rg.GetBoundingBox()
                  target_center_z = target[0].z + 0.5*abs(target[0].z - target[1].z)
                  diff = abs(photon_iso.z - target_center_z)
      if diff:
        if diff > 1:
          return t.fail(round(diff, 2))
        else:
          return t.succeed()

  def asymmetric_jaw_opening_long_test(self):
    t = TEST.Test("Isosenter ser ut til å være asymmetrisk, det bør vurderes å flytte isosenter. Dette for å få målt hele målvolumet med ArcCheck-fantomet", '<10.5 cm', self.isocenter)
    ss = self.ts_structure_set().structure_set
    isocenter = None
    ctv_upper = None
    ctv_lower = None
    if self.beam_set.DeliveryTechnique == 'Arc':
      if self.beam_set.Modality == 'Photons':
        for beam in self.beam_set.Beams:
          photon_iso = beam.Isocenter.Position
          for roi in ss.RoiGeometries:
            if roi.OfRoi.Type == 'Ptv' and roi.PrimaryShape:
              isocenter = ss.RoiGeometries[roi.OfRoi.Name].GetCenterOfRoi()
          if isocenter:
            ctv_upper = isocenter.z
            ctv_lower = isocenter.z
          for roi in ss.RoiGeometries:
            if roi.OfRoi.Type == 'Ptv' and roi.PrimaryShape:
              ctv_box = roi.GetBoundingBox()
              ctv_box_upper = ctv_box[1].z
              ctv_box_lower = ctv_box[0].z
              if abs(ctv_box_upper) < abs(ctv_upper):
                ctv_upper = ctv_box_upper
              if abs(ctv_box_lower) > abs(ctv_lower):
                ctv_lower = ctv_box_lower
            if ctv_upper and ctv_lower:
              if abs(ctv_upper - ctv_lower) <= 21:
                if abs(photon_iso.z - ctv_lower) > 10.5:
                  return t.fail()
                elif abs(photon_iso.z - ctv_upper) > 10.5:
                 return t.fail()
                else:
                  return t.succeed()
              else:
                return t.succeed()
'''
  def stereotactic_beam_distribution_mu_test(self):
    t = TEST.Test("Antall MU bør være jevnt fordelt per bue (buelengde tatt i betraktning). MU på denne buen er > 1.15 * forventningsverdien.", True, self.mu)
    beam_start = 0
    beam_stop = 0
    beam_length = 0
    total_beam_length = 0
    if self.beam_set.Prescription.PrimaryDosePrescription:
      if self.ts_label.label.technique:
        if self.ts_label.label.technique.upper() == 'S':
          for beam in self.beam_set.Beams:
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

          for beam in self.beam_set.Beams:
            if beam_start > 180:
              beam_length += 360 - beam_start
            else:
              beam_length += beam_start
            if beam_stop > 180:
              beam_length += 360 - beam_stop
            else:
              beam_length += beam_stop
            t.expected = "<" + str((beam_length/total_beam_length)*RSU.fraction_dose(self.beam_set) * 140)
            if beam.BeamMU > (beam_length/total_beam_length)*RSU.fraction_dose(self.beam_set) * 140 * 1.15:
              return t.fail(round(beam.BeamMU, 1))
'''