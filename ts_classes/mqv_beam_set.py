# encoding: utf8

# Contains tests for individual beam sets.
#

# System configuration:
from connect import *
import sys
import math

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import beam_set_label as BSL
import region_list as REGIONS
import test_p as TEST


# This class contains tests for the RayStation BeamSet object:
class MQVBeamSet(object):
  def __init__(self, beam_set, mqv_plan=None):
    # RayStation object:
    self.beam_set = beam_set
    # Mosaiq object:
    self.mq_beam_set = None
    # Related test suite objects:
    self.mqv_plan = mqv_plan
    self.mqv_beams = []
    if mqv_plan:
      mqv_plan.mqv_beam_sets.append(self)
      self.parent_param = mqv_plan.param
    # Load list of region codes and corresponding region names:
    self.regions = REGIONS.RegionList("C:\\temp\\raystation-scripts\\settings\\regions.tsv")
    # Beam set label:
    beam_set_label = beam_set.DicomPlanLabel
    label = BSL.BeamSetLabel(beam_set_label)
    self.expected_mosaiq_label = self.translate(label)
    # Parameters:
    self.param = TEST.Parameter('Beam Set', self.beam_set.DicomPlanLabel, self.parent_param)
    self.label = TEST.Parameter('Label', beam_set.DicomPlanLabel, self.param)
    self.technique = TEST.Parameter('Teknikk', self.beam_set.DeliveryTechnique, self.param)
    self.modality = TEST.Parameter('Modalitet', self.beam_set.Modality, self.param)
    self.orientation = TEST.Parameter('Pasientleie', self.beam_set.PatientPosition, self.param)
    self.setup_offsets = TEST.Parameter('Bord-forflytninger', '', self.param)

  # Translates a RayStation (code format) beam set label to the Mosaiq (readable) version.
  def translate(self, bs_label):
    assert type(bs_label) is BSL.BeamSetLabel, "bs_label is not a BeamSetLabel: %r" % bs_label
    # Get the region text part of the label:
    region_text = self.regions.get_text(bs_label.region)
    assert region_text != None
    # Add the dose part of the label to complete it:
    nr_decimals = 2
    # Format start and end dose:
    if round(bs_label.start_dose, nr_decimals) == round(bs_label.start_dose):
      start_dose = str(round(bs_label.start_dose))
    else:
      start_dose = str(round(bs_label.start_dose, nr_decimals))
    if round(bs_label.end_dose, nr_decimals) == round(bs_label.end_dose):
      end_dose = str(round(bs_label.end_dose))
    else:
      end_dose = str(round(bs_label.end_dose, nr_decimals))
    mq_label = region_text + " " + start_dose + "-" + end_dose
    return mq_label


  # Checks that there is a beam set in Mosaiq with a name corresponding to the decoded beam set label.
  def test_matching_beam_set_name(self):
    t = TEST.Test("Skal finnes et beam set (RadRx) i Mosaiq med forventet navn.", self.expected_mosaiq_label, self.label)
    if self.mq_beam_set:
      return t.succeed()
    else:
      return t.fail()
  
  # Comparison of technique.
  def test_technique(self):
    t = TEST.Test("DeliveryTechnique", self.technique.value, self.technique)
    # Proceed only on matching beam set:
    if self.mq_beam_set:
      if self.beam_set.DeliveryTechnique == "DynamicArc":
        if self.mq_beam_set.technique in ["VMAT", "Stereotaksi"]:
          return t.succeed()
        else:
          return t.fail(self.mq_beam_set.technique)
      elif self.beam_set.DeliveryTechnique == "SMLC":
        if self.mq_beam_set.technique in ["IMRT", "IMRT SIB", "DPL m/MV", "DPL m/MV PS"]:
          return t.succeed()
        else:
          return t.fail(self.mq_beam_set.technique)
      else:
        return t.fail("Ukjent technique! (oppdater skript)")
  
  # Comparison of modality.
  def test_modality(self):
    t = TEST.Test("Modality", self.beam_set.Modality, self.modality)
    # Proceed only on matching beam set:
    if self.mq_beam_set:
      if self.beam_set.Modality == "Photons":
        if self.mq_beam_set.modality == "Xrays":
          return t.succeed()
        else:
          return t.fail(self.mq_beam_set.modality)
      elif self.beam_set.Modality == "Electrons":
        if self.mq_beam_set.modality == "Elect":
          return t.succeed()
        else:
          return t.fail(self.mq_beam_set.modality)
      else:
        return t.fail("Ukjent modalitet! (oppdater skript)")

  # Comparison of patient orientation.
  def test_patient_orientation(self):
    t = TEST.Test("Patient Orientation", self.beam_set.PatientPosition, self.orientation)
    # Proceed only on matching beam set:
    if self.mq_beam_set:
      if self.beam_set.PatientPosition == "HeadFirstSupine":
        if self.mq_beam_set.site_setup().patient_orientation_id == 1:
          return t.succeed()
        else:
          return t.fail(self.mq_beam_set.site_setup().patient_orientation_id)
      elif self.beam_set.PatientPosition == "FeetFirstSupine":
        if self.mq_beam_set.site_setup().patient_orientation_id == 5:
          return t.succeed()
        else:
          return t.fail(self.mq_beam_set.site_setup().patient_orientation_id)
      else:
        return t.fail("Ukjent orientering! (oppdater skript) (ID: " + str(self.mq_beam_set.site_setup().patient_orientation_id) + ")")
  
  # Comparison of setup offsets (table top displacement from localization point to isocenter).
  def test_setup_offsets(self):
    # Get RayStation displacement values:
    displacement = self.beam_set.PatientSetup.TreatmentSetupPositions[0].TableTopDisplacement
    rs_displacements = []
    for disp in [displacement.LongitudinalDisplacement, displacement.LateralDisplacement, displacement.VerticalDisplacement]:
      rs_displacements.append(-round(disp, 1))
    t = TEST.Test("Setup offsets", rs_displacements, self.setup_offsets)
    # Get Mosaiq displacement values:
    mq_displacements = [
      float(self.mq_beam_set.site_setup().prescribed_offset().superior),
      float(self.mq_beam_set.site_setup().prescribed_offset().lateral),
      float(self.mq_beam_set.site_setup().prescribed_offset().anterior)
    ]
    # Compare:
    if rs_displacements == mq_displacements:
      return t.succeed()
    else:  
      return t.fail(mq_displacements)
