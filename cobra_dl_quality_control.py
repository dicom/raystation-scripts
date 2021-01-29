# Quality control of ROIs used in the COBRA Deep Learning project.

# RayStation 9A - Python 3.6

# System files:
from connect import *
import sys

# Used for GUI dialogues:
from tkinter import *
from tkinter import messagebox

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# Load the patient model:
pm = case.PatientModel

# Store test results in this list:
failures = []

# A function for extracting an item from a script collection by its name parameter.
# Returns the item if there is a match, if not returns None.
def get_item(collection, item_name):
  # Verify input:
  assert isinstance(item_name, str), "item_name is not a string: %r" % item_name
  match = None
  for item in collection:
    if item.Name == item_name:
      match = item
  return match

# A function for removing the overlap between two volumes.
def remove_overlap(master_rois, yielding_roi):
  # Verify input:
  assert isinstance(master_rois, list), "master_rois is not a list: %r" % master_rois
  assert isinstance(yielding_roi, str), "yielding_roi is not a string: %r" % yielding_roi
  temp = "TempROI"
  # Make sure our temp ROI doesnt exist:
  if get_item(pm.RegionsOfInterest, temp):
    pm.RegionsOfInterest[temp].DeleteRoi()
  # Create a copy of the yielding_roi:
  pm.CreateRoi(Name=temp, Color="#FFFF0000", Type="Organ")
  pm.RegionsOfInterest[temp].CreateMarginGeometry(Examination=examination, SourceRoiName=yielding_roi, MarginSettings = { 'Type': "Contract", 'Superior' : 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0})
  # Use ROI Algebra to create a ROI where the yielding ROI is pulled out of the master ROI:
  pm.RegionsOfInterest[yielding_roi].CreateAlgebraGeometry(
    Examination = examination,
    ExpressionA =  { 'Operation': "Union", 'SourceRoiNames': [temp], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } },
    ExpressionB = { 'Operation': "Union", 'SourceRoiNames': master_rois, 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } },
    ResultOperation ='Subtraction',
    ResultMarginSettings =  { 'Type': "Contract", 'Superior' : 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 }
  )
  pm.RegionsOfInterest[yielding_roi].SetAlgebraExpression(
    ExpressionA =  { 'Operation': "Union", 'SourceRoiNames': [temp], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } },
    ExpressionB = { 'Operation': "Union", 'SourceRoiNames': master_rois, 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } },
    ResultOperation ='Subtraction',
    ResultMarginSettings =  { 'Type': "Contract", 'Superior' : 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 }
  )
  pm.RegionsOfInterest[yielding_roi].UpdateDerivedGeometry(Examination = examination)
  # At the end, underive it, as it isnt supposed to be a derived ROI:
  pm.RegionsOfInterest[yielding_roi].DeleteExpression()
  # Finally, delete the temp ROI:
  pm.RegionsOfInterest[temp].DeleteRoi()

# Some cleanup for Ålesund:
# Rename/switch spinal canal ROIs for Ålesund:
r1 = get_item(pm.RegionsOfInterest, "SpinalCanal")
r2 = get_item(pm.RegionsOfInterest, "SpinalCanal (1)")
if r1 and r2:
  r1.Name = 'SpinalCanalFull'
  r2.Name = 'SpinalCanal'
# Delete 'BreastString_Step1' and 'BreastString_Step2':
d1 = get_item(pm.RegionsOfInterest, "BreastString_Step1")
if d1:
  d1.DeleteRoi()
d2 = get_item(pm.RegionsOfInterest, "BreastString_Step2")
if d2:
  d2.DeleteRoi()
# Rename ScaleneMusc_Ant to ScaleneMusc_Ant_L:
r3 = get_item(pm.RegionsOfInterest, "ScaleneMusc_Ant")
if r3:
  r3.Name = 'ScaleneMusc_Ant_L'
# Remove some common overlaps between neighbouring ROIs:
# From Lungs and Esophagus, extract Heart:
remove_overlap(["Lung_R", "Lung_L", "Esophagus"], "Heart")
# From Lungs and Trachea, extract Esophagus:
remove_overlap(["Lung_R", "Lung_L", "Trachea"], "Esophagus")
# From Lung_L, extract A_Subclavian_L+A_Axillary_L:
remove_overlap(["Lung_L"], "A_Subclavian_L+A_Axillary_L")
# From Lungs, extract V_Brachioceph_L:
remove_overlap(["Lung_R", "Lung_L"], "V_Brachioceph_L")
# From Sternum and Lung_L, extract LN_IMN_L:
remove_overlap(["Sternum", "Lung_L"], "LN_IMN_L")
# From Breast_L, extract LN_Ax_L1_L:
remove_overlap(["Breast_L"], "LN_Ax_L1_L")
# From LN_Ax_L1_L, extract LN_Ax_L2_L:
remove_overlap(["LN_Ax_L1_L"], "LN_Ax_L2_L")
# From LN_Ax_L3_L, extract LN_Ax_L2_L:
remove_overlap(["LN_Ax_L3_L"], "LN_Ax_L2_L")
# From LN_Ax_L3_L, extract LN_Ax_L4_L:
remove_overlap(["LN_Ax_L3_L"], "LN_Ax_L4_L")
# From LN_Ax_L1_L and LN_Ax_L2_L and LN_Ax_L3_L, extract LN_Ax_Pectoral_L:
remove_overlap(["LN_Ax_L1_L", "LN_Ax_L2_L", "LN_Ax_L3_L"], "LN_Ax_Pectoral_L")
# From A_Subclavian_L+A_Axillary_L, extract ScaleneMusc_Ant_L:
remove_overlap(["A_Subclavian_L+A_Axillary_L"], "ScaleneMusc_Ant_L")
# From Trachea and A_Carotid_L and V_Jugular_L, extract ThyroidGland:
remove_overlap(["Trachea", "A_Carotid_L", "V_Jugular_L"], "ThyroidGland")
# From A_Carotid_L, extract V_Subclavian_L+V_Axillary_L:
remove_overlap(["A_Carotid_L"], "V_Subclavian_L+V_Axillary_L")
# Remove bony density areas from the SpinalCanal (and SpinalCanalFull):
# Create a bony ROI by density:
bone = get_item(pm.RegionsOfInterest, "Bone")
if bone:
  bone.DeleteRoi()
bone = pm.CreateRoi(Name = 'Bone', Color = 'Yellow', Type = 'Undefined')
bone.GrayLevelThreshold(Examination=examination, LowThreshold=250, HighThreshold=3071, PetUnit=r"", CbctUnit=None, BoundingBox=None)
# From the bony density ROI, extract SpinalCanal and SpinalCanalFull:
remove_overlap(["Bone"], "SpinalCanal")
remove_overlap(["Bone"], "SpinalCanalFull")
bone.DeleteRoi()

# ROIs which are used to derive ROIs (they are accepted to be present, but not required to be):
temp_rois = [
  'Breast_L_Draft',
  'Breast_R_Draft'
]

# ROIs which are required to always be present:
required_rois = [
  'Breast_L',
  'LN_Ax_L1_L',
  'LN_Ax_L2_L',
  'LN_Ax_L3_L',
  'LN_Ax_L4_L',
  'LN_Ax_Pectoral_L',
  'LN_IMN_L',
  'Sternum',
  'ScaleneMusc_Ant_L',
  'A_Subclavian_L+A_Axillary_L',
  'A_Carotid_L',
  'V_Brachioceph_L',
  'V_Subclavian_L+V_Axillary_L',
  'V_Jugular_L',
  'External', # Body også tillatt (i Ålesund kun brukt External).
  'Lung_R',
  'Lung_L',
  'Heart',
  'A_LAD',
  'SpinalCanal',
  'HumeralHead_L',
  'ThyroidGland',
  'Trachea',
  'Esophagus',
  'Breast_R'
]

# ROIs which may be defined, depending on the patient case:
optional_rois = [
  'SurgicalBed_L',
  'Clips_L',
  'BreastString_L',
  'SpinalCanalFull'
]

# All possible allowed ROIs:
allowed_rois = temp_rois + required_rois + optional_rois

# Test for presence of required ROIs:
for roi in required_rois:
  if not get_item(pm.RegionsOfInterest, roi):
    failures.append(roi + " - fant ikke denne obligatoriske ROIen\n")

# Test for presence of unknown ROIs:
for roi in pm.RegionsOfInterest:
  if not roi.Name in allowed_rois:
    failures.append(roi.Name + " - inneholdt denne ROIen som ikke var forventet å være med")
  
# Test for type target:
targets = [
  'Breast_L',
  'LN_Ax_L1_L',
  'LN_Ax_L2_L',
  'LN_Ax_L3_L',
  'LN_Ax_L4_L',
  'LN_Ax_Pectoral_L',
  'LN_IMN_L',
  'SurgicalBed_L'
]
for target in targets:
  if get_item(pm.RegionsOfInterest, target):
    if not pm.RegionsOfInterest[target].Type == 'Ctv':
      failures.append(target + ' - forventet at denne var type target ("Ctv"), fant: ' + pm.RegionsOfInterest[target].Type)

# Test for type organ/organ at risk:
risk_organs = [
  'Sternum',
  'Lung_R',
  'Lung_L',
  'Heart',
  'A_LAD',
  'SpinalCanal',
  'HumeralHead_L',
  'ThyroidGland',
  'Trachea',
  'Esophagus',
  'Breast_R'
]
for organ in risk_organs:
  if get_item(pm.RegionsOfInterest, organ):
    if not pm.RegionsOfInterest[organ].Type == 'Organ':
      failures.append(organ + ' - forventet at denne var type "Organ", fant: ' + pm.RegionsOfInterest[organ].Type)
    else:
      if not pm.RegionsOfInterest[organ].OrganData.OrganType == 'OrganAtRisk':
        failures.append(organ + ' - forventet at denne har OrganType "OrganAtRisk", fant: ' + pm.RegionsOfInterest[organ].OrganData.OrganType)

# Test for type marker:
markers = [
  'Clips_L',
  'BreastString_L'
]
for marker in markers:
  if get_item(pm.RegionsOfInterest, marker):
    if not pm.RegionsOfInterest[marker].Type == 'Marker':
      failures.append(marker + ' - forventet at denne var type marker ("Marker"), fant: ' + pm.RegionsOfInterest[marker].Type)

# Target definition support structures:
support_organs = [
  'ScaleneMusc_Ant',
  'A_Subclavian_L+A_Axillary_L',
  'A_Carotid_L',
  'V_Brachioceph_L',
  'V_Subclavian_L+V_Axillary_L',
  'V_Jugular_L'
]
# Test for organ type other:
for organ in support_organs:
  if get_item(pm.RegionsOfInterest, organ):
    if not pm.RegionsOfInterest[organ].Type == 'Organ':
      failures.append(organ + ' - forventet at denne var type "Organ", fant: ' + pm.RegionsOfInterest[organ].Type)
    else:
      if not pm.RegionsOfInterest[organ].OrganData.OrganType == 'Other':
        failures.append(organ + ' - forventet at denne har OrganType "Other", fant: ' + pm.RegionsOfInterest[organ].OrganData.OrganType)

# If the optional ROI 'Clips_L' exists, then the optional 'SurgicalBed_L' ROI should be defined:
if get_item(pm.RegionsOfInterest, 'Clips_L'):
  if not get_item(pm.RegionsOfInterest, 'SurgicalBed_L'):
    failures.append("Når strukstursettet inneholder 'Clips_L', så skal 'SurgicalBed_L' være definert også!")

# Get the structure set in which we expect to have the ROI geometries defined:
ss = case.TreatmentPlans[0].GetStructureSet()
# Test that ROIs which are defined actually are delinated:
for roi in allowed_rois:
  if get_item(pm.RegionsOfInterest, roi):
    # Get the Roi Geometry for the chosen structure set:
    rg = ss.RoiGeometries[roi]
    if not rg.HasContours():
      failures.append(roi + " - denne ROIen har ikke blitt tegnet!")

# Create a success message if there are zero failures:
if len(failures) == 0:
  failures.append("PERFEKT!!!  :)")

# Display the results:
root = Tk()
root.withdraw()
title = "COBRA Deep Learning project"
text = "\n".join(failures)
messagebox.showinfo(title, text)
root.destroy()
