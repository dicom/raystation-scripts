# encoding: utf8
# Creates a QA plan with standard settings and exports it to specified folder.
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9A
# Python 3.6

# Import system libraries:
from connect import *
import clr, sys, os

import math


# Load patient and case data:
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No plan loaded.")
try:
    plan = get_current("Plan")
except SystemError:
    raise IOError("No plan loaded.")
try:
    beam_set = get_current("BeamSet")
except SystemError:
    raise IOError("No beam set loaded.")

name = 'QA'
org_name = 'QA'
name_conflict = False
if len(list(plan.VerificationPlans)) > 0:
  for p in plan.VerificationPlans:
    if p.BeamSet.DicomPlanLabel == org_name:
      name_conflict = True
  if name_conflict:
    i = 0
    while True:
      i += 1
      name = org_name + " " + str(i) + ""
      name_conflict = False
      for p in plan.VerificationPlans:
        if p.BeamSet.DicomPlanLabel == name:
          name_conflict = True
      if name_conflict == False:
        break

beam_set.CreateQAPlan(
	PhantomName = 'ArcCheck (Heterogen bordtopp)',
	PhantomId = 'AC_plug_test',
	QAPlanName = name, 
	IsoCenter = { 'x': -0.0, 'y': 0.0, 'z': 0 }, 
	DoseGrid = { 'x': 0.2, 'y': 0.2, 'z': 0.2 }, 
	ComputeDoseWhenPlanIsCreated = True
)

# Save
patient.Save()
last_plan = len(list(plan.VerificationPlans))-1
plan.VerificationPlans[last_plan].ScriptableQADicomExport(
	ExportFolderPath = "I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Stråleterapi_avd\\Stråleterapi\\Mosaiq\\dokument-import\\VMAT_QA",
	QaPlanIdentity = 'Patient',
	ExportExamination = False,
	ExportExaminationStructureSet = False,
	ExportBeamSet = False,
	ExportBeamSetDose = True,
	ExportBeamSetBeamDose = True,
	IgnorePreConditionWarnings = False
)


