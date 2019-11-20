
from __future__ import division
import math
# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("PresentationFramework")
from System.Windows import *
import Microsoft.Office.Interop.Excel as interop_excel


# Add necessary folders to the system path:
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\def_regions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\functions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\gui_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\rt_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\settings".decode('utf8'))

#import region_codes as RC

# Utility function to create 2-dimensional array
def create_array(m, n):
    dims = System.Array.CreateInstance(System.Int32, 2)
    dims[0] = m
    dims[1] = n
    return System.Array.CreateInstance(System.Object, dims)

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

nr_f = beam_set.FractionationPattern.NumberOfFractions
structure_set = plan.GetStructureSet()
text = ''
title = "EDRIC"
match_l = False
for r in structure_set.RoiGeometries:
  if r.OfRoi.Name == 'Lungs-IGTV'and r.HasContours():
    l = 'Lungs-IGTV'
    match_l = True
    
if not match_l:
  for r in structure_set.RoiGeometries:
    if r.OfRoi.Name == 'Lungs-GTV'and r.HasContours():
      l = 'Lungs-GTV'
    match_l = True

if not match_l:
  for r in structure_set.RoiGeometries:
    if r.OfRoi.Name == 'Lungs'and r.HasContours():
      l = 'Lungs'
    match_l = True

if not match_l:
  for r in structure_set.RoiGeometries:
    if r.OfRoi.Name == 'Lung union'and r.HasContours():
      l = 'Lung union'
    match_l = True
 
if not match_l:
  text += "Finner ingen Lungs-IGTV. Dette skriptet kan bare brukes på lungeplaner."
  MessageBox.Show(text, title, MessageBoxButton.OK)
  sys.exit(0)

mld = round(plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName=l, DoseType='Average')/100,2)
mbd = round(plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName='External', DoseType='Average')/100,2)
mhd = round(plan.TreatmentCourse.TotalDose.GetDoseStatistic(RoiName='Heart', DoseType='Average')/100,2)
edric = round((0.12*mld)+(0.08*mhd)+(0.45+(0.35*0.85*math.sqrt(nr_f/45)))*mbd ,2)


text += "EDRIC: " + str(edric) + " Gy" + "\n" 

MessageBox.Show(text, title, MessageBoxButton.OK, MessageBoxImage.Information)

