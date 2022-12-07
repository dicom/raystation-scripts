
from __future__ import division
import math
# encoding: utf8
#!/usr/bin/python

# Import system libraries:
from connect import *
import clr, sys
import xlsxwriter, datetime, string
from tkinter import *
from tkinter import messagebox

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\quality_control")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\ts_classes")
sys.path.append("C:\\temp\\raystation-scripts\\various_classes")

import structure_set_functions as SSF
import plan_functions as PF
import raystation_utilities as RSU
import property as P
import radio_button as RB
import statistics_frame as FRAME
import statistics_region_code_frame as REGION_FRAME
import region_codes as RC
#import check_button_frame as FRAME
# Create an Excel file and sheet
headline = 'DoseStatistikkBrystReg2019'
file = '.xlsx'
title = headline+file
try:
  workbook = xlsxwriter.Workbook(title)
  worksheet = workbook.add_worksheet()
except:
  headline + "1" + file
patient_db = get_current('PatientDB')
roi = ['ICTV','CTV','PTV','External']

beam_set_codes = ['224','225','226','228','245','246','247','248','249','250']
ctv_list = ['ICTV','CTV','ICTV1','ICTV2','CTV1','CTV2','CTV_50','CTVp','CTVsb','CTV3']
ctv_sb_list = ['CTVsb']
ctv_nodes_list = ['CTVn','CTV!_47']
ctv_primary_list = ['CTVp','CTV_50']
ptv_nodes_list = ['PTVnc','PTV!_47c','PTV!_47']
ptv_primary_list = ['PTVpc','PTV_50c','PTV_50']
ptv_n_p_list = ['PTV_47+50','PTVc']
ptv_list = ['PTVc','PTV','PTV1','PTV2','PTVsbc','PTVpc','PTV_50c','PTV3']
external_list = ['External']
lung_list = ['Lungs-IGTV','Lung-GTV','Lungs','Lung union','Lungs-GTV']
lung_l_list = ['Lung_L']
lung_r_list = ['Lung_R']
heart_list = ['Heart']
# Create data array to hold ROI data


def is_target_objective(plan, beam_set, roi_dict, target_list, roi_type):
  objective_target_volumes = {}
  target = None
  # Create a dictionary of all CTVs defined as an objective.
  prescription_roi = beam_set.Prescription.PrimaryPrescriptionDoseReference.OnStructure.Name
  if roi_dict.get(prescription_roi) and roi_type == 'Ctv':
    target = prescription_roi
  elif roi_dict.get(prescription_roi.replace("C", "P")):
    target = prescription_roi.replace("C", "P")
  elif roi_dict.get(prescription_roi.replace("G", "P")):
    target = prescription_roi.replace("G", "P")
  elif roi_dict.get(prescription_roi) and roi_type == 'Ptv':
    target = prescription_roi
  if not target:
    if plan.PlanOptimizations != None:
      for po in plan.PlanOptimizations:
        for objective in po.Objective.ConstituentFunctions:
          if objective.ForRegionOfInterest.Type == roi_type:
            objective_target_volumes[objective.ForRegionOfInterest.Name] = True    
    # Check in the list of potential SIB volumes if any exist in the structure set, define as target
    for i in range(len(target_list)):
      if roi_dict.get(target_list[i]):
        t = target_list[i]
        # Check if the target was used as objective
        if objective_target_volumes.get(t):
          target = t
          break
  if not target:
    target = list(objective_target_volumes.keys())[0]
  if target:
    return target

parameter_list = [
  'Pasient','Beamset-navn','Sist endret',
  'Roinavn, CTV','CTV, D98 [Gy]','CTV, D98 [%]','CTV, D50 [Gy]','CTV, D50 [%]',
  'Roinavn, PTV','PTV, D98 [Gy]','PTV, D98 [%]','PTV, D50 [Gy]','PTV, D50 [%]','PTV, Volum [cc]','PTV, Paddick ','PTV, Conformity Index (95% dose)','PTV, Conformity Index (100% dose)',
  'External, Volum [cc]','External, D2cm3 [Gy]','External, D2cm3 [%]','External, Average [Gy]'
]

def create_parameter_dict(patient, plan, plan_dose, beam_set, patient_nr, roi_dict, region_codes):
  parameter_dict = {}
  parameter_dict['Pasient'] = patient_nr +1
  parameter_dict['Beamset-navn'] = beam_set.DicomPlanLabel
  parameter_dict['Sist endret'] = str(patient.ModificationInfo.ModificationTime)
  nr_fractions = beam_set.FractionationPattern.NumberOfFractions
  try:
    region_code = int(beam_set.DicomPlanLabel[0:3])
  except:
    print ("Hei")  
  try:
    match = True
    for i in range(len(region_codes)):
      if region_codes[i] in RC.breast_codes and nr_fractions == 8:
        ctv = 'CTVsb'
        match = False
    if match:
      ctv = is_target_objective(plan, beam_set, roi_dict, ctv_list, 'Ctv')
    parameter_dict['Roinavn, CTV'] = ctv
  except:
    print ("Hei")
  try:
    match = True
    for i in range(len(region_codes)):
      if region_codes[i] in RC.breast_codes and nr_fractions == 8:
        ptv = 'PTVsbc'
        match = False
    if match:
      ptv = is_target_objective(plan, beam_set, roi_dict, ptv_list, 'Ptv')
  except:
    print ("Hei")
  
  if beam_set.Prescription.PrimaryPrescriptionDoseReference:
    dose_value = (beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue/nr_fractions)*0.95 #fraction dose
  else:
    dose_value = 0
  tot_dose = (beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue)/100 #total dose
  
  try:
    ctv_d98 = nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ctv, RelativeVolumes=[.98])[0]/100
    parameter_dict['CTV, D98 [Gy]'] = ctv_d98
    parameter_dict['CTV, D98 [%]'] = (ctv_d98*100)/tot_dose
    #messagebox.showinfo("Error.",ctv_d98)
    ctv_d50 = (plan_dose.GetDoseAtRelativeVolumes(RoiName=ctv, RelativeVolumes=[.5])[0]*nr_fractions)/100
    parameter_dict['CTV, D50 [Gy]'] = ctv_d50
    parameter_dict['CTV, D50 [%]'] = (ctv_d50*100)/tot_dose
  except:
    print ("Hei")
  try:
    parameter_dict['Roinavn, PTV'] = ptv
  except:
    print ("Hei")
  try:
    ptv_d98 =(nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ptv, RelativeVolumes=[.98])[0])/100
    ptv_d50 =(nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ptv, RelativeVolumes=[.5])[0])/100
    parameter_dict['PTV, D98 [Gy]'] = ptv_d98
    parameter_dict['PTV, D98 [%]'] = (ptv_d98*100)/tot_dose
    parameter_dict['PTV, D50 [Gy]'] = ptv_d50
    parameter_dict['PTV, D50 [%]'] = (ptv_d50*100)/tot_dose
    ptv_volume = plan.BeamSets[0].GetStructureSet().RoiGeometries[ptv].GetRoiVolume()
    parameter_dict['PTV, Volum [cc]'] = ptv_volume
    ptv_v95 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=ptv, DoseValues=[dose_value])[0]
    ptv_v100 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=ptv, DoseValues=[tot_dose*100/nr_fractions])[0]
    ptv_v95_volume = ptv_v95*ptv_volume
    ptv_v100_volume = ptv_v100*ptv_volume
  except:
    print ("Hei")

  try:
    dose_value_4465 = (beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue/nr_fractions)*0.893
    external_volume = plan.BeamSets[0].GetStructureSet().RoiGeometries[has_roi(roi_dict, external_list)].GetRoiVolume()
    parameter_dict['External, Volum [cc]'] = external_volume
    ext_d2cc = (nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=has_roi(roi_dict, external_list), RelativeVolumes=[2/external_volume])[0])/100
    parameter_dict['External, D2cm3 [Gy]'] = ext_d2cc
    
    parameter_dict['External, D2cm3 [%]'] = (ext_d2cc*100)/tot_dose
    external_v95 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, external_list), DoseValues=[dose_value])[0]
    external_v100 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, external_list), DoseValues=[tot_dose*100/nr_fractions])[0]
    external_v95_volume = external_v95*external_volume
    external_v100_volume = external_v100*external_volume
    external_v89 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, external_list), DoseValues=[dose_value_4465])[0]
    external_v89_volume = external_v89*external_volume
    parameter_dict['External, Average [Gy]'] = nr_fractions*plan_dose.GetDoseStatistic(RoiName=has_roi(roi_dict, external_list), DoseType='Average')/100
  except:
    print ("Hei")



  try:
    parameter_dict['PTV, Conformity Index (95% dose)'] = (ptv_v95_volume)/(external_v95_volume)
    parameter_dict['PTV, Paddick '] = (ptv_v95_volume*ptv_v95_volume)/(external_v95_volume*ptv_volume)
  except:
    print ("Hei")

  if region_code in RC.breast_codes or region_code in RC.lung_and_mediastinum_codes:
    try:
      parameter_dict['Lungs, Average [Gy]'] =  nr_fractions*plan_dose.GetDoseStatistic(RoiName=has_roi(roi_dict, lung_list), DoseType='Average')/100
      if nr_fractions == 15:
        if region_code in RC.breast_l_codes:
          parameter_dict['Lungs, V18Gy [%]'] = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, lung_l_list), DoseValues=[1800/nr_fractions])[0]*100
        if region_code in RC.breast_r_codes:
          parameter_dict['Lungs, V18Gy [%]'] = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, lung_r_list), DoseValues=[1800/nr_fractions])[0]*100
      elif nr_fractions == 25:
        if region_code in RC.breast_reg_l_codes:
          parameter_dict['Lungs, V20Gy [%]'] = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, lung_l_list), DoseValues=[2000/nr_fractions])[0]*100
        if region_code in RC.breast_reg_r_codes:
          parameter_dict['Lungs, V20Gy [%]'] = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=has_roi(roi_dict, lung_r_list), DoseValues=[2000/nr_fractions])[0]*100
    except:
      print ("Hei")
    try:
      parameter_dict['Heart, Average [Gy]'] = nr_fractions*plan_dose.GetDoseStatistic(RoiName=has_roi(roi_dict, heart_list), DoseType='Average')/100
    except:
      print ("Hei")
  if region_code in RC.breast_reg_codes or region_code in RC.rectum_codes:
    try:
      ctv_p = has_roi(roi_dict, ctv_primary_list)
      ctv_p_d98 =(nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ctv_p, RelativeVolumes=[.98])[0])/100
      ctv_p_d50 =(nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ctv_p, RelativeVolumes=[.5])[0])/100
      if ctv_p == 'CTVp':
        parameter_dict['CTVp, D98 [Gy]'] = ctv_p_d98
        parameter_dict['CTVp, D98 [%]'] = (ctv_p_d98*100)/tot_dose
        parameter_dict['CTVp, D50 [Gy]'] = ctv_p_d50
        parameter_dict['CTVp, D50 [%]'] = (ctv_p_d50*100)/tot_dose
        #messagebox.showinfo("Error.","Unexpected error.")
      else:
        parameter_dict['CTV_50, D98 [Gy]'] = ctv_p_d98
        parameter_dict['CTV_50, D98 [%]'] = (ctv_p_d98*100)/tot_dose
        parameter_dict['CTV_50, D50 [Gy]'] = ctv_p_d50
        parameter_dict['CTV_50, D50 [%]'] = (ctv_p_d50*100)/tot_dose
    except:
      print ("Hei")
    try:
      ctv_n =has_roi(roi_dict, ctv_nodes_list)
      ctv_n_d98 =(nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ctv_n, RelativeVolumes=[.98])[0])/100
      ctv_n_d50 =(nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ctv_n, RelativeVolumes=[.5])[0])/100
      if ctv_n == 'CTV!_47':
        tot_dose_47 = 47
        parameter_dict['CTV_47, D98 [Gy]'] = ctv_n_d98
        parameter_dict['CTV_47, D98 [%]'] = (ctv_n_d98*100)/tot_dose_47
        parameter_dict['CTV_47, D50 [Gy]'] = ctv_n_d50
        parameter_dict['CTV_47, D50 [%]'] = (ctv_n_d50*100)/tot_dose_47
        
      else:
        tot_dose_47 = tot_dose
        parameter_dict['CTVn, D98 [Gy]'] = ctv_n_d98
        parameter_dict['CTVn, D98 [%]'] = (ctv_n_d98*100)/tot_dose_47
        parameter_dict['CTVn, D50 [Gy]'] = ctv_n_d50
        parameter_dict['CTVn, D50 [%]'] = (ctv_n_d50*100)/tot_dose_47
    except:
      print ("Hei")
    try:
      ptv_p = has_roi(roi_dict, ptv_primary_list)
      ptv_p_d98 =nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ptv_p, RelativeVolumes=[.98])[0]/100
      ptv_p_d50 =nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ptv_p, RelativeVolumes=[.5])[0]/100
      if ptv_p == 'PTVp':
        parameter_dict['PTVp, D98 [Gy]'] = ptv_p_d98
        parameter_dict['PTVp, D98 [%]'] = (ptv_p_d98*100)/tot_dose
        parameter_dict['PTVp, D50 [Gy]'] = ptv_p_d50
        parameter_dict['PTVp, D50 [%]'] = (ptv_p_d50*100)/tot_dose
      else:
        parameter_dict['PTV_50, D98 [Gy]'] = ptv_p_d98
        parameter_dict['PTV_50, D98 [%]'] = (ptv_p_d98*100)/tot_dose
        parameter_dict['PTV_50, D50 [Gy]'] = ptv_p_d50
        parameter_dict['PTV_50, D50 [%]'] = (ptv_p_d50*100)/tot_dose
    except:
      print ("Hei")
    try:
      ptv_n = has_roi(roi_dict, ptv_nodes_list)
      ptv_n_d98 =nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ptv_n, RelativeVolumes=[.98])[0]/100
      ptv_n_d50 =nr_fractions*plan_dose.GetDoseAtRelativeVolumes(RoiName=ptv_n, RelativeVolumes=[.5])[0]/100
      if ptv_n in ['PTV!_47c','PTV!_47']:
        tot_dose_47 = 47
        parameter_dict['PTV_47, D98 [Gy]'] = ptv_n_d98
        parameter_dict['PTV_47, D98 [%]'] = (ptv_n_d98*100)/tot_dose_47
        parameter_dict['PTV_47, D50 [Gy]'] = ptv_n_d50
        parameter_dict['PTV_47, D50 [%]'] = (ptv_n_d50*100)/tot_dose_47
      else:
        tot_dose_47 = tot_dose
        parameter_dict['PTVn, D98 [Gy]'] = ptv_n_d98
        parameter_dict['PTVn, D98 [%]'] = (ptv_n_d98*100)/tot_dose_47
        parameter_dict['PTVn, D50 [Gy]'] = ptv_n_d50
        parameter_dict['PTVn, D50 [%]'] = (ptv_n_d50*100)/tot_dose_47
    except:
      print ("Hei")
    try:
      dose_value_4465 = (beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue/nr_fractions)*0.893
      ptv_n_p = has_roi(roi_dict, ptv_n_p_list)
      ptv_n_p_volume = plan.BeamSets[0].GetStructureSet().RoiGeometries[ptv_n_p].GetRoiVolume()
      
      ptv_n_p_v95 = plan_dose.GetRelativeVolumeAtDoseValues(RoiName=ptv_n_p, DoseValues=[dose_value_4465])[0]
      ptv_n_p_v95_volume = ptv_n_p_v95*ptv_n_p_volume
      if ptv_n_p == 'PTV_47+50':
        parameter_dict['PTV_47+50, Volum [cc]'] = ptv_n_p_volume
        parameter_dict['PTV_47+50, Conformity Index (44.65 Gy)'] = (ptv_n_p_v95_volume)/(external_v89_volume)
        #messagebox.showinfo("Error.",parameter_dict['PTV_47+50, Conformity Index (44.65 Gy)'])
      else:
        parameter_dict['PTVc, Volum [cc]'] = ptv_n_p_volume
        parameter_dict['PTVc, Conformity Index (44.65 Gy)'] = (ptv_n_p_v95_volume)/(external_v89_volume)
    except:
      print ("Hei")
      
  if stereotactic == True:
    try:
      parameter_dict['PTV, Conformity Index (100% dose)'] = (ptv_v100_volume)/(external_v100_volume)
    except:
      print ("Hei")

  return parameter_dict

patient_nr = -1
patient_info = patient_db.QueryPatientInfo(Filter = {})

# Set up header row
# Edit this if other dose statistics are desired

my_window = Tk()
frame_r = REGION_FRAME.RegionCodeFrame(my_window)
frame_r.grid(row = 0, column = 0)
my_window.mainloop()

# Extract information from the users's selections in the GUI
if frame_r.ok:
  region_codes = frame_r.get_results()
elif not frame_r.ok:
  print ("Script execution cancelled by user...")
  sys.exit(0)
else:
  messagebox.showinfo("Error.","Unexpected error.")
  sys.exit(0)
breast = False
lung = False
breast_reg = False
rectum = False
for i in range(len(region_codes)):
  if region_codes[i] in RC.breast_codes:
    breast = True

  if region_codes[i] in RC.breast_reg_codes:
    breast_reg = True

  if region_codes[i] in RC.lung_and_mediastinum_codes:
    lung = True
    
  if region_codes[i] in RC.rectum_codes:
    rectum = True
    
if breast or lung:
  parameter_list.append('Lungs, Average [Gy]')
  parameter_list.append('Heart, Average [Gy]')
  parameter_list.append('Lungs, V18Gy [%]')
  parameter_list.append('Lungs, V20Gy [%]')
if breast:
  parameter_list.append('CTVsb, D98 [Gy]')
  parameter_list.append('CTVsb, D98 [%]')

if breast_reg:
  parameter_list.append('CTVp, D98 [Gy]')
  parameter_list.append('CTVp, D98 [%]')
  parameter_list.append('CTVp, D50 [Gy]')
  parameter_list.append('CTVp, D50 [%]')
  parameter_list.append('CTVn, D98 [Gy]')
  parameter_list.append('CTVn, D98 [%]')
  parameter_list.append('CTVn, D50 [Gy]')
  parameter_list.append('CTVn, D50 [%]')
  parameter_list.append('PTVp, D98 [Gy]')
  parameter_list.append('PTVp, D98 [%]')
  parameter_list.append('PTVp, D50 [Gy]')
  parameter_list.append('PTVp, D50 [%]')
  parameter_list.append('PTVn, D98 [Gy]')
  parameter_list.append('PTVn, D98 [%]')
  parameter_list.append('PTVn, D50 [Gy]')
  parameter_list.append('PTVn, D50 [%]')
  parameter_list.append('PTVc, Conformity Index (44.65 Gy)')

if rectum:
  parameter_list.append('CTV_50, D98 [Gy]')
  parameter_list.append('CTV_50, D98 [%]')
  parameter_list.append('CTV_50, D50 [Gy]')
  parameter_list.append('CTV_50, D50 [%]')
  parameter_list.append('CTV_47, D98 [Gy]')
  parameter_list.append('CTV_47, D98 [%]')
  parameter_list.append('CTV_47, D50 [Gy]')
  parameter_list.append('CTV_47, D50 [%]')
  parameter_list.append('PTV_50, D98 [Gy]')
  parameter_list.append('PTV_50, D98 [%]')
  parameter_list.append('PTV_50, D50 [Gy]')
  parameter_list.append('PTV_50, D50 [%]')
  parameter_list.append('PTV_47, D98 [Gy]')
  parameter_list.append('PTV_47, D98 [%]')
  parameter_list.append('PTV_47, D50 [Gy]')
  parameter_list.append('PTV_47, D50 [%]')
  parameter_list.append('PTV_47+50, Conformity Index (44.65 Gy)')

def has_roi(roi_dict, oar_list):
  roi = None
  for k in range(len(oar_list)):
    if roi_dict.get(oar_list[k]):
      roi = oar_list[k]
      break
  return roi

# Setup GUI choices:
parameter_property = []

for i in range(len(parameter_list)):
  parameter_property.append(P.Property(parameter_list[i], parameter_list[i]))

# Create radio button object
options = RB.RadioButton('Statistikk','Velg:', parameter_property)

# Setup and run GUI:
my_window = Toplevel()
frame = FRAME.StatisticsFrame(my_window, options)
frame.grid(row = 0,column = 0)
my_window.mainloop()

# Extract information from the users's selections in the GUI:
if frame.ok:
    checkBoxes = frame.checkbuttons
    variables = frame.variables
    (start_date, stop_date, stereotactic, conv) = frame.get_results()
elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)

# Determine which OARs have been selected:
def determine_selected_parameters(checkBoxes, variables, all_parameters_dict):
  selected_parameter_dict = {}
  for i in range(len(checkBoxes)):
    for (text, value) in all_parameters_dict.items():
      if variables[i].get() == 1:
        if text == checkBoxes[i].cget("text"):
          selected_parameter_dict[text] = value
          break
  
  return selected_parameter_dict
cols = len(parameter_list)
#rows, cols = (60, len(parameter_list))
#header_row =[[0 for i in range(cols)] for j in range(rows)]
header_row =[[0 for i in range(cols)]]
data_array =[[0 for i in range(cols)]]

start_date = datetime.datetime(int(start_date[6:10]),int(start_date[3:5]),int(start_date[0:2]))
stop_date = datetime.datetime(int(stop_date[6:10]),int(stop_date[3:5]),int(stop_date[0:2]))
for i in range(len(patient_info)):
  p = str(patient_info[i]['LastModified'])
  current_patient_date = datetime.datetime(int(p[6:10]),int(p[3:5]),int(p[0:2])) 
  if current_patient_date > start_date and current_patient_date < stop_date:
    try:
      patient = patient_db.LoadPatient(PatientInfo=patient_info[i])
    except:
      print ("hei")
    try:
      for case in patient.Cases:
        plan = case.TreatmentPlans
        plan_info = case.QueryPlanInfo(Filter = {})
        for i in range(len(plan)):   
          if plan[i].Review:
            if plan[i].Review.ApprovalStatus == 'Approved':
              if plan[i].Comments != 'Imported plan':
                c = str(plan_info[i]['LastModified'])
                current_date = datetime.datetime(int(c[6:10]),int(c[3:5]),int(c[0:2])) 
                if current_date > start_date and current_date < stop_date:
                  if len(plan[i].BeamSets)>0:
                    beam_set = plan[i].BeamSets
                    for j in range(len(beam_set)):
                      label = beam_set[j].DicomPlanLabel
                      #messagebox.showinfo("Error.",str(label[3]))
                      if stereotactic == False and conv == True:
                        if int(label[0:3]) in region_codes and str(label[3]) != 'S' or int(label[0:2]) in region_codes and str(label[2]) != 'S':
                          #plan_dose = plan[i].TreatmentCourse.TotalDose
                          plan_dose = beam_set[j].FractionDose
                          # Find all visible ROIs with defined geometry in the current plan
                          ss = plan[i].BeamSets[0].GetStructureSet()
                          roi_dict = SSF.create_roi_dict(ss)
                          patient_nr += 1
                          
                          parameter_dict = create_parameter_dict(patient, plan[i], plan_dose, beam_set[j], patient_nr, roi_dict, region_codes)
                          selected_parameters_dict = determine_selected_parameters(checkBoxes, variables, parameter_dict)
                          l = 0  
                          for name, value in selected_parameters_dict.items():
                            header_row[0][l] = name
                            
                            data_array.append([0 for i in range(cols)])
                            try:
                              #messagebox.showinfo("Error.",round(value,2))
                              data_array[patient_nr][l] = round(value,2)
                            except:
                              #messagebox.showinfo("Error.",value)
                              data_array[patient_nr][l] = value
                            l+=1
                      elif stereotactic == True and conv == False:
                        if int(label[0:3]) in region_codes and str(label[3]) == 'S' or int(label[0:2]) in region_codes and str(label[2]) == 'S':
                          plan_dose = beam_set[j].FractionDose
                          # Find all visible ROIs with defined geometry in the current plan
                          ss = plan[i].BeamSets[0].GetStructureSet()
                          roi_dict = SSF.create_roi_dict(ss)
                          patient_nr += 1
                          parameter_dict = create_parameter_dict(patient, plan[i], plan_dose, beam_set[j], patient_nr, roi_dict, region_codes)
                          selected_parameters_dict = determine_selected_parameters(checkBoxes, variables, parameter_dict)
                          l = 0  
                          for name, value in selected_parameters_dict.items():
                            header_row[0][l] = name
                            data_array.append([0 for i in range(cols)])
                            try: 
                              data_array[patient_nr][l] = round(value,2)
                            except:
                              data_array[patient_nr][l] = value
                            l+=1
                      elif stereotactic == True and conv == True:
                        if int(label[0:3]) in region_codes or int(label[0:2]) in region_codes:
                          plan_dose = beam_set[j].FractionDose
                          # Find all visible ROIs with defined geometry in the current plan
                          ss = plan[i].BeamSets[0].GetStructureSet()
                          roi_dict = SSF.create_roi_dict(ss)
                          patient_nr += 1
                          parameter_dict = create_parameter_dict(patient, plan[i], plan_dose, beam_set[j], patient_nr, roi_dict, region_codes)
                          selected_parameters_dict = determine_selected_parameters(checkBoxes, variables, parameter_dict)
                          l = 0  
                          for name, value in selected_parameters_dict.items():
                            header_row[0][l] = name
                            data_array.append([0 for i in range(cols)])
                            try: 
                              data_array[patient_nr][l] = round(value,2)
                            except:
                              data_array[patient_nr][l] = value
                            l+=1
    except:
      print ("hei")

#messagebox.showinfo("Error.",len(data_array[0]))

d = dict(enumerate(string.ascii_uppercase, 1))

# Write to excel-files 
for i in range(int(round(len(data_array)/len(data_array[0]),0))):
  #messagebox.showinfo("Error.",round(len(data_array)/len(data_array[0]),0))
  for j in range(len(data_array[0])):
    
    if header_row[0][j]:
      worksheet.write(0, j, header_row[0][j])
    if data_array[i][j]:
      worksheet.write(i+1, j, data_array[i][j])
i =-1
for j in list(range(len(parameter_dict))):
  if j > 25:
    i +=1
    worksheet.write(patient_nr+2, j, '=AVERAGE('+"A"+str(d[i+1])+'2:'+"A"+str(d[i+1])+str(patient_nr+2)+')')
  else:
    worksheet.write(patient_nr+2, j, '=AVERAGE('+str(d[j+1])+'2:'+str(d[j+1])+str(patient_nr+2)+')')

worksheet.write(patient_nr+2, 0, 'Gjennomsnitt')      
workbook.close()




