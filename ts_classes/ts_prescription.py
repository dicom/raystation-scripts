# encoding: utf8

# Contains treatment plan tests for individual beams.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import raystation_utilities as RSU
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF
import test_p as TEST

# This class contains tests for the RayStation Prescription object:
class TSPrescription(object):
  def __init__(self, prescription, ts_beam_set=None):
    # RayStation object:
    self.prescription = prescription
    # Related test suite objects:
    self.ts_beam_set = ts_beam_set
    if ts_beam_set:
      ts_beam_set.ts_prescription = self
      self.parent_param = ts_beam_set.param
    else:
      self.parent_param = None
    # ROI (Name) parameter:
    # In case SITE prescription is used:
    try:
      name = self.prescription.PrimaryPrescriptionDoseReference.OnStructure.Name
    except:
      name = self.prescription.PrimaryPrescriptionDoseReference.Description
    # Parameters:
    self.param = TEST.Parameter('Prescription', str(prescription.PrimaryPrescriptionDoseReference.DoseValue/100.0), self.parent_param)
    self.roi = TEST.Parameter('ROI', name, self.param)
    self.type = TEST.Parameter('Type', self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType, self.param)
    self.dose = TEST.Parameter('Dose', '', self.param)
    self.mu = TEST.Parameter('MU', '', self.param)
    self.max = TEST.Parameter('Klinisk maksdose', '', self.param)


  # Gives true/false if the prescription is stereotactic or not.
  def is_stereotactic(self):
    match = False
    if self.ts_beam_set.ts_label:
      if self.ts_beam_set.ts_label.label.valid:
        if self.ts_beam_set.ts_label.label.technique.upper() == 'S':
          match = True
    return match
  
  # Tests if the clinical max dose is higher than the set limit.
  def clinical_max_test(self):
    ss = self.ts_beam_set.ts_structure_set().structure_set
    if SSF.has_named_roi_with_contours(ss, ROIS.external.name):
      # Get the external ROI and its volume:
      external = ss.OutlineRoiGeometry
      volume = external.GetRoiVolume()
      # Determine which max dose level and volume fraction is to be used:
      if self.is_stereotactic():
        # Use point dose (0 cc):
        fraction = 0
        # For stereotactic treatments, max allowed dose is dependent on site:
        if self.ts_beam_set.ts_label.label.region in RC.brain_codes:
          # Brain SRT:
          max_factor = 1.7
        else:
          # Other SBRT:
          max_factor = 1.5
      else:
        # Use the fraction which gives a 2 cc volume:
        fraction = 2 / volume
        # For conventional treatment max allowed dose is 105 %:
        max_factor = 1.05
      # The differential dose of this prescription:
      diff_pr_dose = RSU.differential_prescription_dose(self.ts_beam_set.ts_plan.plan, self.ts_beam_set.beam_set)
      # Create the test:
      expected = "<" + str(round(diff_pr_dose * max_factor, 2))
      t = TEST.Test("Skal i utgangspunktet være mindre enn {} % av normeringsdosen".format(round(max_factor*100)), expected, self.max)
      # Get the clinical max dose:
      clinical_max_dose = RSU.gy(self.ts_beam_set.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = external.OfRoi.Name, RelativeVolumes = [fraction])[0]) * self.ts_beam_set.beam_set.FractionationPattern.NumberOfFractions
      # Is it outside the set limit?
      if clinical_max_dose > diff_pr_dose * max_factor:
        return t.fail(round(clinical_max_dose, 2))
      else:
        return t.succeed()
        

  # Tests if the prescription volume type is as expected.
  def ctv_prescription_test(self):
    t = TEST.Test("Skal i utgangspunktet benytte CTV til normalisering.", True, self.roi)
    ts = TEST.Test("Skal i utgangspunktet benytte PTV til normalisering.", True, self.roi)
    if self.ts_beam_set.ts_label.label.technique:
      # In case SITE prescription is used:
      try:
        type = self.prescription.PrimaryPrescriptionDoseReference.OnStructure.Type
      except:
        type = self.prescription.PrimaryPrescriptionDoseReference.Description
      if self.ts_beam_set.ts_label.label.technique.upper() == 'S':
        # SBRT (PTV should be prescription volume):
        if type == 'Ptv':
          ts.succeed()
        else:
          ts.fail(type)
      else:
        # Conventional RT (CTV should be prescription volume)
        if type == 'Ctv':
          return t.succeed()
        else:
          return t.fail(type)

  # Tests that the prescription type (MedianDose/DoseAtVolume) is as expected.
  def prescription_type_test(self):
    t = TEST.Test("Skal være en av disse", ['MedianDose'], self.type)
    expected = 'MedianDose'
    if self.is_stereotactic():
      expected = 'DoseAtVolume'
      t.expected = [expected]
    found = self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType
    if expected == found:
      return t.succeed()
    else:
      return t.fail(found)

  # Tests if the prescription dose is equal to the dose given in the DICOM plan label.
  def prescription_dose_test(self):
    t = TEST.Test("Skal stemme overens med totaldose indikert av beam set label.", True, self.dose)
    cum_pr_dose = RSU.prescription_dose(self.ts_beam_set.beam_set)
    diff_pr_dose = RSU.differential_prescription_dose(self.ts_beam_set.ts_plan.plan, self.ts_beam_set.beam_set)
    if self.ts_beam_set.ts_label.label.valid:
      label_dose_acc = RSU.accumulated_label_dose(self.ts_beam_set.ts_plan.plan, self.ts_beam_set.beam_set, self.ts_beam_set.ts_label.label)
      t.expected = round(label_dose_acc, 2)
      if label_dose_acc != cum_pr_dose:
        return t.fail(cum_pr_dose)
      else:
        return t.succeed()

  # Tests if the dose in the prescription volume is within 0.5 % of the set prescription dose.
  def prescription_real_dose_test(self):
    t = TEST.Test("Skal stemme overens (innenfor 0.5%) med aktuell dose for nomeringsvolum (eller punkt)", True, self.dose)
    if self.ts_beam_set.beam_set.Modality == 'Photons':
      cum_pr_dose = RSU.prescription_dose(self.ts_beam_set.beam_set)
      diff_pr_dose = RSU.differential_prescription_dose(self.ts_beam_set.ts_plan.plan, self.ts_beam_set.beam_set)
      low_dose = round(diff_pr_dose * 0.995, 2)
      high_dose = round(diff_pr_dose * 1.005, 2)
      t.expected = "<" + str(low_dose) + " - " + str(high_dose) + ">"
      # If the prescription type is "SITE", we are not able to verify the prescription (at least currently):
      try:
        struct = self.prescription.PrimaryPrescriptionDoseReference.OnStructure
      except:
        struct = None
      if struct:
        # What type of prescription has been used?
        if self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType == 'DoseAtPoint':
          norm_poi = RSU.ss_poi_geometry(self.ts_beam_set.beam_set, struct)
          p = {'x': norm_poi.Point.x, 'y': norm_poi.Point.y, 'z': norm_poi.Point.z}
          real_poi_dose = RSU.gy(self.ts_beam_set.beam_set.FractionDose.InterpolateDoseInPoint(Point = p)) * self.ts_beam_set.beam_set.FractionationPattern.NumberOfFractions
          if real_poi_dose < low_dose or real_poi_dose > high_dose:
            return t.fail(round(real_poi_dose, 2))
          else:
            return t.succeed()
        if self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType == 'MedianDose':
          real_dose_d50 = RSU.gy(self.ts_beam_set.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = struct.Name, RelativeVolumes = [0.50])[0]) * self.ts_beam_set.beam_set.FractionationPattern.NumberOfFractions
          if real_dose_d50 < low_dose or real_dose_d50 > high_dose:
            return t.fail(round(real_dose_d50, 2))
          else:
            return t.succeed()
        elif self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType == 'DoseAtVolume':
          real_dose_d99 = RSU.gy(self.ts_beam_set.beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = struct.Name, RelativeVolumes = [0.99])[0]) * self.ts_beam_set.beam_set.FractionationPattern.NumberOfFractions
          if real_dose_d99 < low_dose or real_dose_d99 > high_dose:
            return t.fail(round(real_dose_d99, 2))
          else:
            return t.succeed()

  # Tests if beam set label code 'S' is used when a stereotactic prescription (DoseAtVolume 99 %) is given.
  def stereotactic_prescription_technique_test(self):
    t = TEST.Test("Ved stereotaksi skal prescription være: DoseAtVolume 99 %. Planteknikk skal være S.", True, self.type)
    if self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType == 'DoseAtVolume' and self.prescription.PrimaryPrescriptionDoseReference.DoseVolume == 99 and self.ts_beam_set.beam_set.DeliveryTechnique == 'Arc':
      if self.ts_beam_set.ts_label.label.technique:
        if self.ts_beam_set.ts_label.label.technique.upper() == 'S':
          return t.succeed()
        else:
          return t.fail()
      else:
        return t.fail(self.prescription.PrimaryPrescriptionDoseReference.PrescriptionType)
