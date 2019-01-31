# encoding: utf8

# Peforms quality control of the current patient, case and treatment plan (including its beam sets).
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
clr.AddReference("PresentationFramework")
from System.Windows import *

# Local script imports:
import test as TEST
import raystation_utilities as RSU
import ts_patient as TS_P
import ts_case as TS_C
import ts_poi as TS_POI
import ts_roi as TS_ROI
import ts_structure_set as TS_SS
import ts_poi_geometry as TS_PG
import ts_roi_geometry as TS_RG
import ts_plan as TS_PLAN
import ts_beam_set as TS_BS
import ts_prescription as TS_PR
import ts_label as TS_L
import ts_beam as TS_B
import ts_segment as TS_S
import ts_optimization as TS_O


class QualityControl(object):
  def __init__(self, patient, case, plan):
    self.patient = patient
    self.case = case
    self.plan = plan

    # Initialize test suites:
    ts_patient = TS_P.TSPatient(patient)
    ts_case = TS_C.TSCase(case, ts_patient=ts_patient)
    for poi in case.PatientModel.PointsOfInterest:
      ts_poi = TS_POI.TSPOI(poi, ts_case=ts_case)
    for roi in case.PatientModel.RegionsOfInterest:
      ts_roi = TS_ROI.TSROI(roi, ts_case=ts_case)
    for structure_set in case.PatientModel.StructureSets:
      ts_structure_set = TS_SS.TSStructureSet(structure_set, ts_case=ts_case)
      for poi_geometry in structure_set.PoiGeometries:
        ts_poi_geometry = TS_PG.TSPOIGeometry(poi_geometry, ts_structure_set=ts_structure_set)
      for roi_geometry in structure_set.RoiGeometries:
        ts_roi_geometry = TS_RG.TSROIGeometry(roi_geometry, ts_structure_set=ts_structure_set)
    ts_plan = TS_PLAN.TSPlan(plan, ts_case=ts_case)
    for beam_set in plan.BeamSets:
      ts_beam_set = TS_BS.TSBeamSet(beam_set, ts_plan=ts_plan)
      ts_label = TS_L.TSLabel(beam_set.DicomPlanLabel, ts_beam_set=ts_beam_set)
      if beam_set.Prescription.PrimaryDosePrescription:
        ts_prescription = TS_PR.TSPrescription(beam_set.Prescription, ts_beam_set=ts_beam_set)
      po = RSU.plan_optimization(plan, beam_set)
      if po:
        ts_optimization = TS_O.TSOptimization(po, ts_beam_set=ts_beam_set)
      for beam in beam_set.Beams:
        ts_beam = TS_B.TSBeam(beam, ts_beam_set=ts_beam_set)
        for segment in beam.Segments:
          ts_segment = TS_S.TSSegment(segment, ts_beam=ts_beam)

    # Store the patient test results:
    self.result = ts_patient.param

    # Run tests:
    # Patient tests:
    ts_patient.id_length_test()
    ts_patient.id_space_test()
    # Case tests:
    ts_case.last_examination_used_test()
    ts_case.localization_points_for_gating_test()

    # Structure set tests:
    for ts_structure_set in ts_case.ts_structure_sets:
      ts_structure_set.localization_point_test()
      ts_structure_set.external_test()
      ts_structure_set.dose_region_test()
      ts_structure_set.ptv_derived_test()
      ts_structure_set.prosthesis_titanium_test()
      ts_structure_set.external_ptv_bounding_test()
      ts_structure_set.couch_test()
      ts_structure_set.couch_close_to_patient_test()
      ts_structure_set.breast_seeds_test()
      # POI geometry tests:
      for ts_poi_geometry in ts_structure_set.ts_poi_geometries:
        ts_poi_geometry.is_defined_test()
        ts_poi_geometry.is_not_zero_test()
      # ROI geometry tests:
      for ts_roi_geometry in ts_structure_set.ts_roi_geometries:
        ts_roi_geometry.derived_roi_geometry_is_updated_test()
    # Plan tests:
    ts_plan.planned_by_test()
    ts_plan.unique_beam_numbers_test()
    ts_plan.breast_oar_defined_test()

    # Beam set tests:
    for ts_beam_set in ts_plan.ts_beam_sets:
      ts_beam_set.unmerged_beams_test()
      ts_beam_set.technique_test()
      ts_beam_set.machine_test()
      ts_beam_set.setup_beams_test()
      ts_beam_set.dose_test()
      ts_beam_set.dose_is_clinical_test()
      ts_beam_set.dose_algorithm_test()
      ts_beam_set.number_of_histories_test()
      ts_beam_set.beam_energy_equality_test()
      ts_beam_set.photon_energy_for_curative_fractionations_test()
      ts_beam_set.vmat_full_arc_rotation_of_last_beam_test()
      ts_beam_set.vmat_arc_sequence_test()
      ts_beam_set.reasonable_collimator_angles_test()
      ts_beam_set.defined_prescription_test()
      ts_beam_set.specific_energy_for_region_test()
      ts_beam_set.nr_fractions_test()
      ts_beam_set.label_vmat_test()
      ts_beam_set.label_target_volume_test()
      ts_beam_set.guard_leaf_test()
      ts_beam_set.name_of_beam_iso_test()
      ts_beam_set.prostate_normalisation_test()
      ts_beam_set.recti_normalisation_test()
      ts_beam_set.isocenter_centered_long_test()
      ts_beam_set.prescription_mu_breast_regional_caudal_test()
      ts_beam_set.prescription_mu_breast_regional_cranial_test()
      ts_beam_set.prescription_mu_test()
      ts_beam_set.asymmetric_jaw_opening_long_test()
      ts_beam_set.isocenter_centered_test()
      ts_beam_set.stereotactic_mu_test()
      ts_beam_set.vmat_mu_test()
      # Label tests:
      ts_label = ts_beam_set.ts_label
      ts_label.nr_parts_test()
      ts_label.nr_fractions_test()
      ts_label.technique_test()
      ts_label.region_test()
      ts_label.middle_part_separator_test()
      ts_label.middle_part_doses_test()
      # Prescription tests:
      ts_prescription = ts_beam_set.ts_prescription
      if ts_prescription:
        ts_prescription.ctv_prescription_test()
        ts_prescription.prescription_type_test()
        ts_prescription.prescription_poi_technique_test()
        ts_prescription.prescription_poi_target_volume_test()
        ts_prescription.prescription_dose_test()
        ts_prescription.prescription_real_dose_test()
        ts_prescription.clinical_max_test()
        ts_prescription.stereotactic_prescription_technique_test()
      # Objectives/constraints tests:
      ts_optimization = ts_beam_set.ts_optimization
      if ts_optimization:
        ts_optimization.constraints_test()
        ts_optimization.objectives_background_dose_test()
        ts_optimization.constrain_leaf_motion_test()
        ts_optimization.dose_grid_test()
      # Beam tests:
      for ts_beam in ts_beam_set.ts_beams:
        ts_beam.name_test()
        ts_beam.name_capitalization_test()
        ts_beam.name_of_arc_test()
        ts_beam.mu_beam_vmat_test()
        ts_beam.gantry_angle_test()
        ts_beam.energy_of_arc_test()
        ts_beam.collimator_angle_of_arc_test()
        ts_beam.number_of_segments_of_static_beam_test()
        ts_beam.wide_jaw_opening_which_can_hit_vmat_qa_detector_electronics_test()
        ts_beam.arc_gantry_spacing_test()
        ts_beam.wide_jaw_opening_for_filter_free_energies()
        ts_beam.mu_segment_3dcrt_test()
        ts_beam.stereotactic_beam_distribution_mu_test()
        ts_beam.stereotactic_mu_constraints_for_multiple_beams()
        ts_beam.stereotactic_mu_constraints_for_single_beam()
        ts_beam.segment_test()
        # Segment tests:
        for ts_segment in ts_beam.ts_segments:
          ts_segment.mlc_corner_validity_test()

