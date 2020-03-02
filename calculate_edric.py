# Calculate the EDRIC from "Impact of Radiation Dose to the Host Immune System on Tumor Control and Survival for
# Stage III Non-Small Cell Lung Cancer Treated with Definitive Radiation Therapy" by Ladbury et al (2019).
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6
from __future__ import division
import math
# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys
from tkinter import *
from tkinter import messagebox

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\quality_control")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")

# Import local files:
import patient_model_functions as PMF
import structure_set_functions as SSF
import gui_functions as GUIF

patient_db = get_current('PatientDB')

# Load patient and case data:
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No patient loaded.")
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")
try:
    plan = get_current("Plan")
except SystemError:
    raise IOError("No plan loaded.")
try:
    beam_set = get_current("BeamSet")
except SystemError:
    raise IOError("No beam set loaded.")

# Load patient model, examination and structure set:
pm = case.PatientModel
examination = get_current("Examination")
ss = PMF.get_structure_set(pm, examination)

nr_f = beam_set.FractionationPattern.NumberOfFractions
text = ''
title = "EDRIC"
match_l = False
target_list = ['Lungs-IGTV','Lungs-GTV','Lungs','Lung union']
roi_dict = SSF.create_roi_dict(ss)
for i in range(len(target_list)):
  if roi_dict.get(target_list[i]):
    l = target_list[i]
    match_l = True
    break
      
if not match_l:
  text += "Finner ingen Lungs-IGTV. Dette skriptet kan bare brukes på lungeplaner."
  messagebox.showinfo(title, text)
  sys.exit(0)

mld = round(plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName=l, DoseType='Average')/100,2)
mbd = round(plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName='External', DoseType='Average')/100,2)
mhd = round(plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName='Heart', DoseType='Average')/100,2)
edric = round((0.12*mld)+(0.08*mhd)+(0.45+(0.35*0.85*math.sqrt(nr_f/45)))*mbd ,2)


text += "EDRIC: " + str(edric) + " Gy" + "\n" 

GUIF.message_box(title, text)
