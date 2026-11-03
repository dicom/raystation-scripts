# Quality control of ROIs used in the Breast_R Deep Learning project.

# RayStation 10B - Python 3.6

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

# Determine the slice thickness for this examination:
slice_thickness = round(abs(examination.Series[0].ImageStack.SlicePositions[1] - examination.Series[0].ImageStack.SlicePositions[0]), 1)

# A function which determines if there are any gaps (i.e. definition missing in one or more slices) in the given ROI geometry.
def gaps(roi_name):
  missing_slices = []
  # Verify input:
  assert isinstance(roi_name, str), "roi_name is not a string: %r" % roi_name
  # Get the ROI geometry:
  rg = pm.StructureSets[examination.Name].RoiGeometries[roi_name]
  # Extract all slices (z coordinates) where the ROI is defined:
  slices = []
  # We are only able to test this if there actually are contours:
  try:
    contours = rg.PrimaryShape.Contours
  except Exception:
    contours = None
  if contours:
    for slice in rg.PrimaryShape.Contours:
      slices.append(slice[0].z)
    # Determine unique slice positions and sort them:
    unique_slices = list(set(slices))
    unique_slices.sort()
    # Iterate the recorded slices to see if there are any gaps (i.e. a difference bigger than the slice thickness):
    for i in range(len(unique_slices)):
      if i > 0:
        gap = round(abs(unique_slices[i] - unique_slices[i-1]), 1)
        # If this gap is larger than slice thickness, then we have a missing slice:
        if gap > slice_thickness:
          missing_slices.append(round(unique_slices[i], 1))
  return missing_slices

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


# Remove some common overlaps between neighbouring ROIs:
# From Lungs and Esophagus, extract Heart:
remove_overlap(["Lung_R", "Lung_L", "Esophagus"], "Heart")
# From Lungs and Trachea, extract Esophagus:
remove_overlap(["Lung_R", "Lung_L", "Trachea"], "Esophagus")
# From Lung_R, extract V_Brachioceph_R:
remove_overlap(["Lung_R"], "V_Brachioceph_R")
# From Lungs, extract A_Brachioceph:
remove_overlap(["Lung_R", "Lung_L"], "A_Brachioceph")
# From Sternum and Lung_R, extract LN_IMN_R:
remove_overlap(["Sternum", "Lung_R"], "LN_IMN_R")
# From Breast_R, extract LN_Ax_L1_R:
remove_overlap(["Breast_R"], "LN_Ax_L1_R")
# From LN_Ax_L1_R, extract LN_Ax_L2_R:
remove_overlap(["LN_Ax_L1_R"], "LN_Ax_L2_R")
# From LN_Ax_L3_R, extract LN_Ax_L2_R:
remove_overlap(["LN_Ax_L3_R"], "LN_Ax_L2_R")
# From LN_Ax_L3_R, extract LN_Ax_L4_R:
remove_overlap(["LN_Ax_L3_R"], "LN_Ax_L4_R")
# From LN_Ax_L1_R and LN_Ax_L2_R and LN_Ax_L3_R, extract LN_Ax_Pectoral_R:
remove_overlap(["LN_Ax_L1_R", "LN_Ax_L2_R", "LN_Ax_L3_R"], "LN_Ax_Pectoral_R")
# From A_Subclavian_R+A_Axillary_R, extract ScaleneMusc_Ant_R:
remove_overlap(["A_Subclavian_R+A_Axillary_R"], "ScaleneMusc_Ant_R")
# From Trachea and A_Carotid_R and V_Jugular_R, extract ThyroidGland:
remove_overlap(["Trachea", "A_Carotid_R", "V_Jugular_R"], "ThyroidGland")
# From A_Carotid_R, extract V_Subclavian_R+V_Axillary_R:
remove_overlap(["A_Carotid_R"], "V_Subclavian_R+V_Axillary_R")


# Remove bony density areas from the SpinalCanal (and SpinalCanalFull):
# Create a bony ROI by density:
bone = get_item(pm.RegionsOfInterest, "Bone")
if bone:
  bone.DeleteRoi()
bone = pm.CreateRoi(Name = 'Bone', Color = 'Yellow', Type = 'Undefined')
bone.GrayLevelThreshold(Examination=examination, LowThreshold=250, HighThreshold=3071, PetUnit=r"", CbctUnit=None, BoundingBox=None)
# From the bony density ROI, extract SpinalCanalFull:
remove_overlap(["Bone"], "SpinalCanalFull")
bone.DeleteRoi()


# ROIs which are used to derive ROIs (they are accepted to be present, but not required to be):
temp_rois = [
  'Breast_L_Draft',
  'Breast_R_Draft'
]

# ROIs which are required to always be present:
required_rois = [
  'Breast_R',
  'LN_Ax_L1_R',
  'LN_Ax_L2_R',
  'LN_Ax_L3_R',
  'LN_Ax_L4_R',
  'LN_Ax_Pectoral_R',
  'LN_IMN_R',
  'Sternum',
  'ScaleneMusc_Ant_R',
  'A_Brachioceph',
  'A_Subclavian_R+A_Axillary_R',
  'A_Carotid_R',
  'V_Brachioceph_R',
  'V_Subclavian_R+V_Axillary_R',
  'V_Jugular_R',
  'External',
  'Lung_R',
  'Lung_L',
  'Heart',
  'A_LAD',
  'SpinalCanalFull',
  'HumeralHead_R',
  'ThyroidGland',
  'Trachea',
  'Esophagus',
  'Liver',
  'Breast_L'
]

# ROIs which may be defined, depending on the patient case:
optional_rois = [
  'SurgicalBed_R',
  'Clips_R',
  'BreastString_R',
  'Couch'
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
  'Breast_R',
  'LN_Ax_L1_R',
  'LN_Ax_L2_R',
  'LN_Ax_L3_R',
  'LN_Ax_L4_R',
  'LN_Ax_Pectoral_R',
  'LN_IMN_R',
  'SurgicalBed_R'
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
  'SpinalCanalFull',
  'HumeralHead_R',
  'ThyroidGland',
  'Trachea',
  'Esophagus',
  'Liver',
  'Breast_L'
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
  'Clips_R',
  'BreastString_R'
]
for marker in markers:
  if get_item(pm.RegionsOfInterest, marker):
    if not pm.RegionsOfInterest[marker].Type == 'Marker':
      failures.append(marker + ' - forventet at denne var type marker ("Marker"), fant: ' + pm.RegionsOfInterest[marker].Type)

# Target definition support structures:
support_organs = [
  'ScaleneMusc_Ant_R',
  'A_Brachioceph',
  'A_Subclavian_R+A_Axillary_R',
  'A_Carotid_R',
  'V_Brachioceph_R',
  'V_Subclavian_R+V_Axillary_R',
  'V_Jugular_R'
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
if get_item(pm.RegionsOfInterest, 'Clips_R'):
  if not get_item(pm.RegionsOfInterest, 'SurgicalBed_R'):
    failures.append("Når strukstursettet inneholder 'Clips_R', så skal 'SurgicalBed_R' være definert også!")

# Get the structure set in which we expect to have the ROI geometries defined:
ss = case.TreatmentPlans[0].BeamSets[0].GetStructureSet()
# Test that ROIs which are defined actually are delinated:
for roi in allowed_rois:
  if get_item(pm.RegionsOfInterest, roi):
    # Get the Roi Geometry for the chosen structure set:
    rg = ss.RoiGeometries[roi]
    if not rg.HasContours():
      failures.append(roi + " - denne ROIen har ikke blitt tegnet!")

# Test for gaps in ROIs:
rois = required_rois
rois.append('BreastString_R')
rois.append('SurgicalBed_R')

for roi in rois:
  if get_item(pm.RegionsOfInterest, roi):
    missing_slices = gaps(roi)
    if len(missing_slices) > 0:
      failures.append(roi + " mangler definisjon i tilknytning til følgende snitt: " + str(missing_slices))

# Create a success message if there are zero failures:
if len(failures) == 0:
  failures.append("PERFEKT!!!  :)")

# Display the results:
root = Tk()
root.withdraw()
title = "BREAST_R Deep Learning project"
text = "\n".join(failures)
messagebox.showinfo(title, text)
root.destroy()
