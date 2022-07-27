# Displays D98 for ICTV and D2cm3 for External in a GUI for perturbed doses
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 10B
# Python 3.6

# Import system libraries:
from connect import *
import clr, sys
from tkinter import *
from tkinter import messagebox

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

i=1
text = ''
title = "Dosestatistikk perturberte planer"
rows, cols = (20, 20)
data_array =[[0 for i in range(cols)] for j in range(rows)] 
for doe in case.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations:
  for de in doe.DoseEvaluations:
    if beam_set.DicomPlanLabel == de.ForBeamSet.DicomPlanLabel:
      data_array[i][0] = plan.Name
      if de.PerturbedDoseProperties.IsoCenterShift.x > 0:
        data_array[i][1] = 'x' 
        data_array[i][2] = de.PerturbedDoseProperties.IsoCenterShift.x  
      elif de.PerturbedDoseProperties.IsoCenterShift.x < 0:
        data_array[i][1] = 'x' 
        data_array[i][2] = de.PerturbedDoseProperties.IsoCenterShift.x  
      elif de.PerturbedDoseProperties.IsoCenterShift.y > 0 or de.PerturbedDoseProperties.IsoCenterShift.y < 0:
        data_array[i][1] = 'z' 
        data_array[i][2] = -de.PerturbedDoseProperties.IsoCenterShift.y  
      elif de.PerturbedDoseProperties.IsoCenterShift.z > 0 or de.PerturbedDoseProperties.IsoCenterShift.z < 0:
        data_array[i][1] = 'y' 
        data_array[i][2] = de.PerturbedDoseProperties.IsoCenterShift.z 

      nr_f = plan.BeamSets[0].FractionationPattern.NumberOfFractions
      structure_set = plan.BeamSets[0].GetStructureSet()
      match_c = False
      for r in structure_set.RoiGeometries:
        if r.OfRoi.Name == 'ICTV' and r.HasContours():
          c = 'ICTV'
          match_c = True
      if not match_c:
        for r in structure_set.RoiGeometries:
          if r.OfRoi.Name == 'CTV'and r.HasContours():
            c = 'CTV'
            match_c = True
      if not match_c:
        for r in structure_set.RoiGeometries:
          if r.OfRoi.Name == 'ICTV1'and r.HasContours():
            c = 'ICTV1'
            match_c = True
      if not match_c:
        for r in structure_set.RoiGeometries:
          if r.OfRoi.Name == 'ICTV2'and r.HasContours():
            c = 'ICTV2'
      if not match_c:
        text += "Finner ingen ICTV/CTV. Dette skriptet kan bare brukes på lungeplaner."
        messagebox.showinfo(title,text)
        sys.exit(0)
        
      vol_external = de.GetDoseGridRoi(RoiName = 'External').RoiVolumeDistribution.TotalVolume
      data_array[i][3] = round(de.GetDoseAtRelativeVolumes(RoiName=c,RelativeVolumes=[0.98])[0]*nr_f/100,2)
      data_array[i][4] = round(de.GetDoseAtRelativeVolumes(RoiName='External', RelativeVolumes=[2/vol_external])[0]*nr_f/100,2)
      
      if i % 6 == 0:

        text += "Plan: " + str(data_array[i][0]) + "\n\n" 
        text += "ICTV D98: " + "\n"
        
        if data_array[i-5][2] < 0:
          p5 = "+"
        else:
          p5 = "- "
        if data_array[i-4][2] < 0:
          p4 = "+"
        else:
          p4 = "- "
        if data_array[i-3][2] < 0:
          p3 = "+"
        else:
          p3 = "- "
        if data_array[i-2][2] < 0:
          p2 = "+"
        else:
          p2 = "- "
        if data_array[i-1][2] < 0:
          p1 = "+"
        else:
          p1 = "- "
        if data_array[i][2] < 0:
          p = "+"
        else:
          p = "- "
        text += "                              " + p5 + str(abs(data_array[i-5][2])) + " " + str(data_array[i-5][1]) + " : " + str(data_array[i-5][3]) + "\n" 
        text += "                              " + p4 + str(abs(data_array[i-4][2])) + " " + str(data_array[i-4][1]) + " : " + str(data_array[i-4][3]) + "\n" 
        text += "                              " + p3 + str(abs(data_array[i-3][2])) + " " + str(data_array[i-3][1]) + " : " + str(data_array[i-3][3]) + "\n" 
        text += "                              " + p2 + str(abs(data_array[i-2][2])) + " " + str(data_array[i-2][1]) + " : " + str(data_array[i-2][3]) + "\n" 
        text += "                              " + p1 + str(abs(data_array[i-1][2])) + " " + str(data_array[i-1][1]) + " : " + str(data_array[i-1][3]) + "\n" 
        text += "                              " + p + str(abs(data_array[i][2])) + " " + str(data_array[i][1]) + " : " + str(data_array[i][3]) + "\n" 
        text += "External D2cm2: " + "\n"
        text += "                              " + p5 + str(abs(data_array[i-5][2])) + " " + str(data_array[i-5][1]) + " : " +str(data_array[i-5][4]) + "\n" 
        text += "                              " + p4 + str(abs(data_array[i-4][2])) + " " + str(data_array[i-4][1]) + " : " + str(data_array[i-4][4]) + "\n" 
        text += "                              " + p3 + str(abs(data_array[i-3][2])) + " " + str(data_array[i-3][1]) + " : " + str(data_array[i-3][4]) + "\n" 
        text += "                              " + p2 + str(abs(data_array[i-2][2])) + " " + str(data_array[i-2][1]) + " : " + str(data_array[i-2][4]) + "\n" 
        text += "                              " + p1 + str(abs(data_array[i-1][2])) + " " + str(data_array[i-1][1]) + " : " + str(data_array[i-1][4]) + "\n" 
        text += "                              " + p + str(abs(data_array[i][2])) + " " + str(data_array[i][1]) + " : " + str(data_array[i][4]) + "\n" 
        
        text += "\n\n"
        root = Tk()
        root.withdraw()
        messagebox.showinfo(title, text)

      i += 1
      


