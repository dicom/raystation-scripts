# encoding: utf8

# Gives a list of OARs in a GUI, and creates those that are selected.
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9A

# Import system libraries:
from connect import *
import clr, sys, os
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Microsoft.Office.Interop.Excel import *
from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton, TextBox)
import math

# Add necessary folders to the system path:
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\def_regions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\functions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\gui_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\quality_control".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\rt_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\settings".decode('utf8'))

# Import local files:
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS
import property as P
import radio_button as RB
import check_box_form as FORM
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
  ROIS.optic_nrv_l, ROIS.optic_nrv_r, ROIS.optic_chiasm,
  ROIS.lacrimal_l, ROIS.lacrimal_r, ROIS.cochlea_l, ROIS.cochlea_r,
  ROIS.hippocampus_l, ROIS.hippocampus_r, ROIS.nasal_cavity,
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

# Setup and run GUI:
options = RB.RadioButton('ROI','Velg:', oar_property)
form_r = FORM.CheckBoxForm(options)
form_r.DialogResult

# Extract information from the users's selections in the GUI:
if form_r.DialogResult == DialogResult.OK:
  checkBoxes = form_r.SelectedBoxes
elif form_r.DialogResult == DialogResult.Cancel:
  print "Script execution cancelled by user..."
  sys.exit(0)
else:
  raise IOError("Unexpected error (selection).")

# Determine which OARs have been selected:
selected_oar_list = []
for box in checkBoxes:
  for i in range(len(oar_list)):
    if box.Checked:
      if oar_list[i].name == box.Text:
        selected_oar_list.append(oar_list[i])
        break

# Add left/right organs in cases where a union organ has been selected from the list:
for i in range(len(selected_oar_list)):
  if selected_oar_list[i].name == ROIS.kidneys.name:
    selected_oar_list.extend([ROIS.kidney_l, ROIS.kidney_r])
  if selected_oar_list[i].name == ROIS.parotids.name:
    selected_oar_list.extend([ROIS.parotid_l, ROIS.parotid_r])
  if selected_oar_list[i].name == ROIS.submands.name:
    selected_oar_list.extend([ROIS.submand_l, ROIS.submand_r])
  if selected_oar_list[i].name == ROIS.ribs_l.name:
    selected_oar_list.extend([ROIS.rib_y_l, ROIS.rib_x_l])
  if selected_oar_list[i].name == ROIS.ribs_r.name:
    selected_oar_list.extend([ROIS.rib_y_r, ROIS.rib_x_r])
  if selected_oar_list[i].name == ROIS.lungs.name:
    selected_oar_list.extend([ROIS.lung_l, ROIS.lung_r])
  if selected_oar_list[i].name == ROIS.breast_l.name:
    selected_oar_list.extend([ROIS.breast_l_draft])
  if selected_oar_list[i].name == ROIS.breast_r.name:
    selected_oar_list.extend([ROIS.breast_r_draft])
  if selected_oar_list[i].name == ROIS.markers.name and SSF.has_roi(ss, ROIS.rectum.name):
    del selected_oar_list[i]
    selected_oar_list.extend([ROIS.marker1, ROIS.marker2, ROIS.marker3, ROIS.marker4])
  if selected_oar_list[i].name == ROIS.couch.name:
    PMF.create_couch(patient_db, pm, examination)
  if selected_oar_list[i].name == ROIS.body.name:
    PMF.create_stereotactic_body_geometry(pm, examination, ss)
    PMF.create_stereotactic_external_geometry(pm, examination, ss)
  if selected_oar_list[i].name == ROIS.external.name:
    PMF.create_external_geometry(pm, examination, ss)
  if selected_oar_list[i].name == ROIS.anal_canal.name:
    PMF.create_bottom_part_x_cm(pm, examination, ss, ROIS.rectum, ROIS.anal_canal, 4)
  if selected_oar_list[i].name == ROIS.dorso_rectum.name:
    PMF.create_posterior_half(pm, examination, ss, ROIS.rectum, ROIS.dorso_rectum)


# Create ROIs:
for roi in reversed(selected_oar_list):
  # Only create ROI if it doesn't already exist:
  if not PMF.has_roi(pm, roi.name):
    if roi.__class__.__name__ == 'ROI':
      if roi.model:
        PMF.create_model_roi(pm, examination, roi)
      else:
        PMF.create_empty_roi(pm, roi)
    elif roi.__class__.__name__ == 'ROIExpanded':
      PMF.create_expanded_roi(pm, examination, ss, roi)
    elif roi.__class__.__name__ == 'ROIAlgebra':
      PMF.create_algebra_roi(pm, examination, ss, roi)
    elif roi.__class__.__name__ == 'ROIWall':
      PMF.create_wall_roi(pm, examination, ss, roi)
