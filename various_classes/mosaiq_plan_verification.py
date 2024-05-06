# encoding: utf8

# Peforms a verification of the current treatment plan (including its beam sets) in Mosaiq,
# testing whether the parameters of the plan has been successfully exported to the Mosaiq database.

# System configuration:
from connect import *
import sys
# GUI framework (debugging only):
#from tkinter import *
#from tkinter import messagebox

# Local script imports:
import beam_set_label as BSL
import region_list as REGIONS
import test_p as TEST
#import raystation_utilities as RSU
import mqv_plan as MQV_P
import mqv_beam_set as MQV_BS
import mqv_beam as MQV_B
import mqv_segment as MQV_S


class MosaiqPlanVerification(object):
  def __init__(self, patient, case, plan, mq_patient):
    self.patient = patient
    self.case = case
    self.plan = plan
    self.mq_patient = mq_patient
    # Load list of region codes and corresponding region names, and get the region name for our particular region code (raise error if a name is not retrieved):
    self.regions = REGIONS.RegionList("C:\\temp\\raystation-scripts\\settings\\regions.tsv")
    
    # Initialize test suites:
    mqv_plan = MQV_P.MQVPlan(patient, case, plan, mq_patient)
    for beam_set in plan.BeamSets:
      mqv_beam_set = MQV_BS.MQVBeamSet(beam_set, mqv_plan=mqv_plan)
      for beam in beam_set.Beams:
        mqv_beam = MQV_B.MQVBeam(beam, mqv_beam_set=mqv_beam_set)
        for segment in beam.Segments:
          mqv_segment = MQV_S.MQVSegment(segment, mqv_beam=mqv_beam)
    
    if self.mq_patient:
      # Collect & assign the equivalent Mosaiq objects to the RayStation objects (beam sets, beams & segments):    
      # Beam sets:
      beam_sets = {}
      # Collect beam sets:
      for bs in self.mq_patient.prescriptions():
        beam_sets[bs.site_name] = bs
      # Iterate beam sets:
      for mqv_beam_set in mqv_plan.mqv_beam_sets:
        # Assign beam set (if we have a matching label):
        if mqv_beam_set.expected_mosaiq_label in beam_sets:
          mqv_beam_set.mq_beam_set = beam_sets[mqv_beam_set.expected_mosaiq_label]
          # Beams:
          beams = {}
          # Collect beams:
          for b in mqv_beam_set.mq_beam_set.fields():
            beams[str(b.label)] = b
          # Iterate beams:
          for mqv_beam in mqv_beam_set.mqv_beams:
            # Assign beam (if we have a matching beam number):
            if str(mqv_beam.nr.value) in beams:
              mqv_beam.mq_beam = beams[str(mqv_beam.nr.value)]
              # Segments:
              segments = {}
              # Collect segments:
              for s in mqv_beam.mq_beam.control_points():
                segments[s.number] = s
              # Iterate segments:
              for mqv_segment in mqv_beam.mqv_segments:
                # Assign segments:
                mqv_segment.mq_segment = segments[mqv_segment.segment.SegmentNumber]
    
    # Store the plan test results:
    self.result = mqv_plan.param

    # Run tests:
    mqv_plan.test_matching_patient()
    # Beam set tests:
    for mqv_beam_set in mqv_plan.mqv_beam_sets:
      mqv_beam_set.test_matching_beam_set_name()
      mqv_beam_set.test_technique()
      mqv_beam_set.test_modality()
      mqv_beam_set.test_patient_orientation()
      mqv_beam_set.test_setup_offsets()
      # Beam tests:
      for mqv_beam in mqv_beam_set.mqv_beams:
        mqv_beam.test_matching_beam_number()
        mqv_beam.test_mu()
        mqv_beam.test_name()
        # Segment tests:
        for mqv_segment in mqv_beam.mqv_segments:
          mqv_segment.test_matching_segment_number()
          mqv_segment.test_collimator_angle()
          mqv_segment.test_jaw_positions()
          mqv_segment.test_gantry_angle()
          mqv_segment.test_relative_weight()
          mqv_segment.test_positions_leaf_bank1()
          mqv_segment.test_positions_leaf_bank2()
