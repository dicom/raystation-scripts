# encoding: utf8

# Creates clinical goals which are specific for patients included in the COBRA-study.
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6

# Import system libraries:
from connect import *
import clr, sys, os

import math


# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\quality_control")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")


import patient_model_functions as PMF
import roi as ROI
import rois as ROIS
import clinical_goal as CG
import region_codes as RC
import tolerance_doses as TOL
import gui_functions as GUIF
import structure_set_functions as SSF

# Load case data:
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")

# Load patient model, examination and structure set:
pm = case.PatientModel
examination = get_current("Examination")
#ss = PMF.get_structure_set(pm, examination)
plan = get_current("Plan")
beam_set = get_current("BeamSet")
nr_fractions = beam_set.FractionationPattern.NumberOfFractions

def get_structure_set(pm, examination):
  ss = pm.StructureSets[examination.Name]
  if ss:
    return ss
ss = get_structure_set(pm, examination)
# Sets up clinical goals.
# Creates clinical goals in RayStation from clinical goal objects
# using the given fractionation to determine target clinical goals as well as doing EQD2 conversion on OAR clinical goals.
def setup_clinical_goals(ss, es, clinical_goals, nr_fractions):
  # Make sure corresponding ROI exists before trying to create clinical goal:
  for cg in clinical_goals:
    if SSF.has_roi(ss, cg.name):
      if cg.tolerance == 10000:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance, ParameterValue = cg.value, Priority = cg.priority)
      else:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance, ParameterValue = cg.value.equivalent(nr_fractions)*100, Priority = cg.priority)


# Creates clinical goal objects which are specific for patients included in the COBRA-study,
def create_cobra_clinical_goals(nr_fractions):
  # Criterias:
  at_most = 'AtMost'
  # Types:
  volume_at_dose = 'VolumeAtDose'
  abs_volume_at_dose = 'AbsoluteVolumeAtDose'
  priority8 = 8

  clinical_goals = [
    CG.ClinicalGoal(ROIS.external.name, at_most, abs_volume_at_dose, 10000, 5*100, priority8)
  ]
  if nr_fractions == 25:
    clinical_goals.extend([
      CG.ClinicalGoal(ROIS.external.name, at_most, abs_volume_at_dose, 10000, 40*100, priority8),
      CG.ClinicalGoal(ROIS.lad.name, at_most, volume_at_dose, 1, TOL.lad_v100_adx, priority8)
    ])
  else:
    clinical_goals.extend([
      CG.ClinicalGoal(ROIS.external.name, at_most, abs_volume_at_dose, 10000, 32*100, priority8),
      CG.ClinicalGoal(ROIS.lad.name, at_most, volume_at_dose, 1, TOL.lad_v100_adx_15, priority8)
    ])
  return clinical_goals


es = plan.TreatmentCourse.EvaluationSetup
# Creates the clinical goals
setup_clinical_goals(ss, es, create_cobra_clinical_goals(nr_fractions), nr_fractions)
