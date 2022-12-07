# encoding: utf8

# Calculates the Paddick conformity index for the prescription ROI and displays the result in a GUI.
# For prescriptions using median dose, the Paddick index is calculated on the 95% dose value.
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6

from __future__ import division
import math

# Import system libraries:
from connect import *
import clr, sys
from tkinter import *
from tkinter import messagebox


# Load case data:
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")

# Load patient model, examination and structure set:
pm = case.PatientModel
examination = get_current("Examination")
plan = get_current("Plan")
text = ""
roi_existence = False
ext_existence = False

for beam_set in plan.BeamSets:
  plan_dose = beam_set.FractionDose
  structure_set = plan.BeamSets[0].GetStructureSet()
  text = ""
  if beam_set.Prescription:
    if beam_set.Prescription.PrimaryPrescriptionDoseReference:
      # Number of fractions
      nr_fractions  = beam_set.FractionationPattern.NumberOfFractions
      # Name of the roi which is used for prescription
      prescription_roi = beam_set.Prescription.PrimaryPrescriptionDoseReference.OnStructure.Name
      # For all plans where "MedianDose" is the prescription type
      if beam_set.Prescription.PrimaryPrescriptionDoseReference.PrescriptionType == 'MedianDose':
        # The dose value used is 95 % of the total dose
        dose_value = beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue/nr_fractions*0.95
        # The roi we want to find the conformity index for is the PTV corresponding to the prescription roi
        if prescription_roi[:1] == "C":
          roi = prescription_roi.replace("C", "P")
        elif prescription_roi[:1] == "G":
          roi = prescription_roi.replace("G", "P")
        else:
          roi = 'PTV'
      else: # Other prescription types, used for stereotactic treatments
        # The dose value used is 100 % of the total dose
        dose_value = beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue/nr_fractions
        # For stereotactic treatments, the prescription roi is the roi we want we to find the conformity index for
        roi = prescription_roi
    else:
      dose_value = 0
      prescription_roi = 'Hei'
    for r in structure_set.RoiGeometries:
      if r.OfRoi.Name == roi:
        roi_existence = True
        # Volume [cc] of the roi we want to find the conformity index for
        volume = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName = roi).RoiVolumeDistribution.TotalVolume
        # The relative volume of the roi we want to find the conformity index for at a given dose value
        v100 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=roi, DoseValues=[dose_value])
        # Multiplying the relative volume with volume of 'PTV' to get the volume of 'PTV' which gets the 95% of the total dose
        vv = v100[0]*volume
      elif r.OfRoi.Name in ['External','Body']:
        ext_existence = True
        # Volume [cc] of the 'External' or 'Body' roi
        volume_e = plan.TreatmentCourse.TotalDose.GetDoseGridRoi(RoiName = r.OfRoi.Name).RoiVolumeDistribution.TotalVolume
        # The relative volume of the 'External' or 'Body' for at a given dose value
        v100_e = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=r.OfRoi.Name, DoseValues=[dose_value])
        # Multiplying the relative volume with volume of 'External' or 'Body' to get the volume of 'External' or 'Body'  which gets the 95% of the total dose
        vve = v100_e[0]*volume_e

  # The paddick conformity index
  paddick = None
  if roi_existence and ext_existence:
    if vve != 0:
      paddick = round((vv*vv)/(vve*volume),2)
      text += "Paddick konformitetsindeks:" + "\n"
      text += str(roi) + ": " + str(paddick) + "\n"
  elif ext_existence:
    text += "Fant ikke forventet ROI: " + str(roi) + "\n" + "Kan derfor ikke beregne Paddick konformitetsindeks" + "\n"
  elif roi_existence and not ext_existence:
    text += "Fant ikke forventet ROI: " + "'External' eller 'Body'" + "\n" + "Kan derfor ikke beregne Paddick konformitetsindeks" + "\n"
  else:
    text += "Fant ikke forventet ROI: " + str(roi) + " eller " + "'External' eller 'Body'" + "\n" + "Kan derfor ikke beregne Paddick konformitetsindeks" + "\n"
  title = "Paddick konformitetsindeks"
  root = Tk()
  root.withdraw()
  messagebox.showinfo(title, text)


