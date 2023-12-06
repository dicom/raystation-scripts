# encoding: utf8

# Gives a list of OARs in a GUI, and creates those that are selected.
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
from tkinter import *
from tkinter import messagebox
import math

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\quality_control")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
# Import local files:
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS
import property as P
import radio_button as RB
import check_button_frame as FRAME
import structure_set_functions as SSF

# Load case data:
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")
try:
  patient_db = get_current('PatientDB')
except SystemError:
  raise IOError("No case loaded.")

# Load patient model, examination and structure set:
pm = case.PatientModel
examination = get_current("Examination")
ss = PMF.get_structure_set(pm, examination)

def get_my_key(obj):
  return obj.name
# OAR choices:
oar_list = [
  ROIS.eye_l, ROIS.eye_r, ROIS.lens_l, ROIS.lens_r,
  ROIS.retina_l, ROIS.retina_r, ROIS.cornea_l, ROIS.cornea_r,
  ROIS.optic_nrv_l, ROIS.optic_nrv_r, ROIS.optic_chiasm,
  ROIS.lacrimal_l, ROIS.lacrimal_r, ROIS.cochlea_l, ROIS.cochlea_r,
  ROIS.hippocampus_l, ROIS.hippocampus_r, ROIS.nasal_cavity, ROIS.oral_cavity,
  ROIS.brain, ROIS.brainstem, ROIS.spinal_canal, ROIS.spinal_cord,
  ROIS.parotids, ROIS.submands,
  ROIS.esophagus, ROIS.breast_l, ROIS.breast_r,
  ROIS.heart, ROIS.a_lad, ROIS.humeral_l, ROIS.humeral_r, ROIS.chestwall,
  ROIS.lungs,
  ROIS.greatves, ROIS.trachea,
  ROIS.ribs_r, ROIS.ribs_l,
  ROIS.main_bronchus_l, ROIS.main_bronchus_r, ROIS.cauda_equina,
  ROIS.kidneys,
  ROIS.stomach, ROIS.liver,  ROIS.small_bowel,
  ROIS.colon, ROIS.brachial, ROIS.bowel_space, ROIS.rectum, ROIS.z_rectum_p, ROIS.anal_canal, ROIS.bladder,
  ROIS.femoral_l, ROIS.femoral_r,
  ROIS.external, ROIS.body,
  ROIS.markers, ROIS.prosthesis_l, ROIS.prosthesis_r, ROIS.couch,
]
oar_list.sort(key=get_my_key)

# Setup GUI choices:
oar_property = []
for i in range(len(oar_list)):
  oar_property.append(P.Property(oar_list[i].name, oar_list[i].name))

# Create radio button object
options = RB.RadioButton('ROI','Velg:', oar_property)

# Setup and run GUI:
my_window = Tk()
frame = FRAME.CheckButtonFrame(my_window, options)
frame.grid(row = 0,column = 0)
my_window.mainloop()

# Extract information from the users's selections in the GUI:
if frame.ok:
    checkBoxes = frame.checkbuttons
    variables = frame.variables
elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)

# Determine which OARs have been selected:
selected_oar_list = {}
for i in range(len(checkBoxes)):
  for j in range(len(oar_list)):
    if variables[i].get() == 1:
      if oar_list[j].name == checkBoxes[i].cget("text"):
        selected_oar_list[oar_list[j]] = True
        break

# Add left/right organs in cases where a union organ has been selected from the list and create OARs that require special functions:
if selected_oar_list.get(ROIS.kidneys):
  selected_oar_list[ROIS.kidney_l] = True
  selected_oar_list[ROIS.kidney_r] = True
if selected_oar_list.get(ROIS.parotids):
  selected_oar_list[ROIS.parotid_l] = True
  selected_oar_list[ROIS.parotid_r] = True
if selected_oar_list.get(ROIS.submands):
  selected_oar_list[ROIS.submand_l] = True
  selected_oar_list[ROIS.submand_r] = True
if selected_oar_list.get(ROIS.ribs_l):
  selected_oar_list[ROIS.rib_y_l] = True
  selected_oar_list[ROIS.rib_x_l] = True  
if selected_oar_list.get(ROIS.ribs_r):
  selected_oar_list[ROIS.rib_y_r] = True
  selected_oar_list[ROIS.rib_x_r] = True  
if selected_oar_list.get(ROIS.lungs):
  selected_oar_list[ROIS.lung_l] = True
  selected_oar_list[ROIS.lung_r] = True    
if selected_oar_list.get(ROIS.breast_l):
  selected_oar_list[ROIS.breast_l_draft] =True
if selected_oar_list.get(ROIS.breast_r):
  selected_oar_list[ROIS.breast_r_draft] =True
if selected_oar_list.get(ROIS.markers)and SSF.has_roi(ss, ROIS.rectum.name):
  del selected_oar_list[ROIS.markers]
  selected_oar_list[ROIS.marker1] = True
  selected_oar_list[ROIS.marker2] = True
  selected_oar_list[ROIS.marker3] = True
  selected_oar_list[ROIS.marker4] = True
if selected_oar_list.get(ROIS.couch):
  PMF.create_couch(patient_db, pm, ss, examination)
if selected_oar_list.get(ROIS.body):
  PMF.create_stereotactic_body_geometry(pm, examination, ss)
  PMF.create_stereotactic_external_geometry(pm, examination, ss)
if selected_oar_list.get(ROIS.external):
  PMF.create_external_geometry(pm, examination, ss)
if selected_oar_list.get(ROIS.anal_canal):
  PMF.create_bottom_part_x_cm(pm, examination, ss, ROIS.rectum, ROIS.anal_canal, 4)
if selected_oar_list.get(ROIS.dorso_rectum):
  PMF.create_posterior_half(pm, examination, ss, ROIS.rectum, ROIS.dorso_rectum)
if selected_oar_list.get(ROIS.cornea_l) and selected_oar_list.get(ROIS.retina_l):
  PMF.create_retina_and_cornea(pm, examination, ss, ROIS.lens_l, ROIS.box_l, ROIS.eye_l, ROIS.retina_l, ROIS.cornea_l)
elif selected_oar_list.get(ROIS.retina_l) and not selected_oar_list.get(ROIS.cornea_l):
  PMF.create_retina(pm, examination, ss, ROIS.lens_l, ROIS.box_l, ROIS.eye_l, ROIS.retina_l)
elif selected_oar_list.get(ROIS.cornea_l) and not selected_oar_list.get(ROIS.retina_l):
  PMF.create_cornea(pm, examination, ss, ROIS.lens_l, ROIS.box_l, ROIS.eye_l, ROIS.cornea_l)
if selected_oar_list.get(ROIS.cornea_r) and selected_oar_list.get(ROIS.retina_r):
  PMF.create_retina_and_cornea(pm, examination, ss, ROIS.lens_r, ROIS.box_r, ROIS.eye_r, ROIS.retina_r, ROIS.cornea_r)
elif selected_oar_list.get(ROIS.retina_r) and not selected_oar_list.get(ROIS.cornea_r):
  PMF.create_retina(pm, examination, ss, ROIS.lens_r, ROIS.box_r, ROIS.eye_r, ROIS.retina_r)
elif selected_oar_list.get(ROIS.cornea_r) and not selected_oar_list.get(ROIS.retina_r):
  PMF.create_cornea(pm, examination, ss, ROIS.lens_r, ROIS.box_r, ROIS.eye_r, ROIS.cornea_r)


# Create ROIs:
for roi in reversed(list(selected_oar_list)):
  # Only create ROI if it doesn't already exist:
  if not PMF.has_roi(pm, roi.name):
    if roi.__class__.__name__ == 'ROI':
      if roi.dlsm:
        examination.RunOarSegmentation(ModelName=roi.dlsm, ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=[roi.name])
      elif roi.model:
        PMF.create_model_roi(pm, examination, roi)
      else:
        PMF.create_empty_roi(pm, roi)
    elif roi.__class__.__name__ == 'ROIExpanded':
      PMF.create_expanded_roi(pm, examination, ss, roi)
    elif roi.__class__.__name__ == 'ROIAlgebra':
      PMF.create_algebra_roi(pm, examination, ss, roi)
    elif roi.__class__.__name__ == 'ROIWall':
      PMF.create_wall_roi(pm, examination, ss, roi)
