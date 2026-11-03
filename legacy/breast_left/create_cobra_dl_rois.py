# Creates ROIs to be used in the COBRA Deep Learning project.

# RayStation 9A - Python 3.6

from connect import *

# Used for GUI debugging:
#from tkinter import *
#from tkinter import messagebox

#root = Tk()
#root.withdraw()
#title = "COBRA Deep Learning project"
#text = ""
#messagebox.showinfo(title, text)
#root.destroy()

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

  
pm = case.PatientModel

# Types: External, Ptv, Ctv, Bolus, Organ, Marker, Cavity, Support, Fixation, Undefined

# pm.CreateStructureFromAtlas()
# pm.MBSAutoInitializer()

# Create ROIs:
# Target volumes:
breast_l_draft = pm.CreateRoi(Name = 'Breast_L_Draft', Color = '255, 128, 128', Type = 'Ctv')
surgical_bed_l = pm.CreateRoi(Name = 'SurgicalBed_L', Color = '255, 128, 128', Type = 'Ctv')
ln_ax_l1_l = pm.CreateRoi(Name = 'LN_Ax_L1_L', Color = '255, 255, 128', Type = 'Ctv')
ln_ax_l2_l = pm.CreateRoi(Name = 'LN_Ax_L2_L', Color = '128, 0, 0', Type = 'Ctv')
ln_ax_l3_l = pm.CreateRoi(Name = 'LN_Ax_L3_L', Color = '0, 0, 160', Type = 'Ctv')
ln_ax_l4_l = pm.CreateRoi(Name = 'LN_Ax_L4_L', Color = '255, 128, 64', Type = 'Ctv')
ln_ax_pectoral_l = pm.CreateRoi(Name = 'LN_Ax_Pectoral_L', Color = '128, 255, 255', Type = 'Ctv')
ln_imn_l = pm.CreateRoi(Name = 'LN_IMN_L', Color = '128, 0, 0', Type = 'Ctv')

# Organs:
# External:
external = pm.CreateRoi(Name = 'External', Color = '255, 173, 91', Type = 'External')
# OARs:
# Already used (AL)
lung_r = pm.CreateRoi(Name = 'Lung_R', Color = '0, 255, 0', Type = 'Organ')
lung_l = pm.CreateRoi(Name = 'Lung_L', Color = '0, 255, 0', Type = 'Organ')
heart = pm.CreateRoi(Name = 'Heart', Color = 'Red', Type = 'Organ')
spinal_canal = pm.CreateRoi(Name = 'SpinalCanal', Color = 'Blue', Type = 'Organ')
a_lad = pm.CreateRoi(Name = 'A_LAD', Color = 'Yellow', Type = 'Organ')
humeral_head = pm.CreateRoi(Name = 'HumeralHead_L', Color = '64, 128, 128', Type = 'Organ')
breast_r_draft = pm.CreateRoi(Name = 'Breast_R_Draft', Color = '255, 192, 203', Type = 'Organ')
# New for this DL project:
thyroid_gland = pm.CreateRoi(Name = 'ThyroidGland', Color = '64, 128, 128', Type = 'Organ')
trachea = pm.CreateRoi(Name = 'Trachea', Color = '64, 128, 128', Type = 'Organ')
esophagus = pm.CreateRoi(Name = 'Esophagus', Color = '255, 192, 0', Type = 'Organ')
ventricle_l = pm.CreateRoi(Name = 'Ventricle_L', Color = '255, 128, 64', Type = 'Organ')
sternum = pm.CreateRoi(Name = 'Sternum', Color = '64, 128, 128', Type = 'Organ')
# Other organs:
# Organs that are support for lymph node definition:
scalene_musc_ant = pm.CreateRoi(Name = 'ScaleneMusc_Ant', Color = '64, 0, 0', Type = 'Organ')
a_subclavian_l = pm.CreateRoi(Name = 'A_Subclavian_L', Color = 'Red', Type = 'Organ')
a_carotid_l = pm.CreateRoi(Name = 'A_Carotid_L', Color = 'Red', Type = 'Organ')
v_brachioceph = pm.CreateRoi(Name = 'V_Brachioceph_L', Color = 'Blue', Type = 'Organ')
v_subclavian_l = pm.CreateRoi(Name = 'V_Subclavian_L', Color = 'Blue', Type = 'Organ')
v_jugular_l = pm.CreateRoi(Name = 'V_Jugular_L', Color = 'Blue', Type = 'Organ')

# Non-organs:
clips_l = pm.CreateRoi(Name = 'Clips_L', Color = 'Yellow', Type = 'Marker')
breast_string_l = pm.CreateRoi(Name = 'BreastString_L', Color = 'Yellow', Type = 'Marker')

# Create MBS (model based) ROIs:
# Lung_L:
#pm.MBSAutoInitializer(
#  MbsRois=[{'CaseType': case, 'ModelName': 'Lung (Left)', 'RoiName': 'Lung_L', 'RoiColor': '0, 255, 0'}],
#  CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True
#)
#pm.AdaptMbsMeshes(Examination=examination, RoiNames=['Lung_L'])

#pm.MBSAutoInitializer(MbsRois=[{'CaseType': case, 'ModelName': 'Lung (Left)', 'RoiName': 'Lung_L', 'RoiColor': '0, 255, 0'}], CreateNewRois=True, Examination=case.Examinations[0], UseAtlasBasedInitialization=False)
