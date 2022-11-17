# Quality control of ROIs used in the prostate pelvic model Deep Learning project.

# RayStation 10B - Python 3.6

# System files:
from connect import *
import sys
import datetime

# Used for GUI dialogues:
from tkinter import *
from tkinter import messagebox

# Log start time:
time_start = datetime.datetime.now()

# Load the patient case, examination and structure set:
try:
  # Case:
  case = get_current('Case')
  # Patient model:
  pm = case.PatientModel
  # Examination:
  examination = case.Examinations['CT 1']
  # Structure set:
  ss = case.PatientModel.StructureSets['CT 1']
except SystemError:
  raise IOError("No case loaded. Load patient and case.")


# Store test results in this list:
failures = []

# Determine the slice thickness of our examination:
slice_thickness = round(abs(examination.Series[0].ImageStack.SlicePositions[1] - examination.Series[0].ImageStack.SlicePositions[0]), 1)

# Creates a ROI.
# If the ROI already exists, do not create a duplicate.
# If a ROI with name of known_variants exists, do not create a duplicate,
# but instead rename that variant according to the given name.
def create_roi(name, color, type, alternatives):
  try:
    roi = pm.RegionsOfInterest[name]
  except:
    roi = None
  if not roi:
    variant_roi = False
    for alternative in alternatives:
      try:
        variant_roi = pm.RegionsOfInterest[alternative]
      except:
        pass
    if not variant_roi:
      # Create the ROI:
      roi = pm.CreateRoi(Name = name, Color = color, Type = type)
    else:
      # Process the existing variant ROI:
      variant_roi.Name = name
      variant_roi.Color = color
      variant_roi.Type = type
      roi = variant_roi
  else:
    # The ROI exists with the given name. Make sure it is of correct color and type:
    roi.Color = color
    roi.Type = type
  return roi

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

# A function which gives the slices (if any) where both given ROIs have contours.
# If no overlap exists, an empty list is returned.
def overlapping_slices(ss, name1, name2):
  rg1 = ss.RoiGeometries[name1]
  rg2 = ss.RoiGeometries[name2]
  slices1 = []
  slices2 = []
  for contour in rg1.PrimaryShape.Contours:
    slices1.append(round(contour[0].z, 1))
  for contour in rg2.PrimaryShape.Contours:
    slices2.append(round(contour[0].z, 1))
  return list(set(slices1).intersection(slices2))
  

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
# remove_overlap([master_rois], yielding_roi)
# From bone, extract nerves:
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum"], "CaudaEquina")
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum"], "SacralNerveRoots_L")
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum"], "SacralNerveRoots_R")
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum"], "LumbarNerveRoots_L")
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum"], "LumbarNerveRoots_R")
# From bone, vessels extract muscles:
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum", "PelvicGirdle_L", "A_CommonIliac_L", "A_ExternalIliac_L", "V_ExternalIliac_L", "V_CommonIliac_L", "V_InternalIliac_L", "Ureter_L"], "IliopsoasMuscle_L")
remove_overlap(["L2", "L3", "L4", "L5", "Sacrum", "PelvicGirdle_R", "V_InferiorVenaCava", "V_CommonIliac_R", "A_ExternalIliac_R", "V_ExternalIliac_R", "V_InternalIliac_R", "Ureter_R"], "IliopsoasMuscle_R")
# From muscle, extract kidney:
remove_overlap(["IliopsoasMuscle_L"], "Kidney_L")
remove_overlap(["IliopsoasMuscle_R"], "Kidney_R")
# From kidney, vessels, extract liver:
remove_overlap(["V_InferiorVenaCava", "Kidney_R"], "Liver")
# From arteries, extract veins:
remove_overlap(["A_DescendingAorta", "A_CommonIliac_R", "A_CommonIliac_L"], "V_InferiorVenaCava")
remove_overlap(["A_CommonIliac_R"], "V_CommonIliac_R")
remove_overlap(["A_CommonIliac_L"], "V_CommonIliac_L")
remove_overlap(["A_InternalIliac_R"], "V_InternalIliac_R")
remove_overlap(["A_InternalIliac_L"], "V_InternalIliac_L")
remove_overlap(["A_ExternalIliac_R"], "V_ExternalIliac_R")
remove_overlap(["A_ExternalIliac_L"], "V_ExternalIliac_L")
# From vessels, extract ductus deferens:
remove_overlap(["A_ExternalIliac_L", "V_ExternalIliac_L"], "DuctusDeferens_L")
remove_overlap(["A_ExternalIliac_R", "V_ExternalIliac_R"], "DuctusDeferens_R")
# From penile bulb, extract anal canal:
remove_overlap(["PenileBulb"], "AnalCanal")
# From prostate and seminalves, extract rectum:
remove_overlap(["Prostate", "SeminalVes"], "Rectum")


# ROIs which are used to derive ROIs (they are accepted to be present, but not required to be):
temp_rois = [
  'Bladder_Draft',
  'BowelBag_Draft'
]

# ROIs which are required to always be present:
required_rois = [
  'Prostate',
  'SeminalVes',
  'LN_Iliac',
  'Vessels_with_margin',
  'External',
  'Markers',
  'L2',
  'L3',
  'L4',
  'L5',
  'Sacrum',
  'Coccyx',
  'PelvicGirdle_L',
  'PelvicGirdle_R',
  'FemurHeadNeck_L',
  'FemurHeadNeck_R',
  'A_DescendingAorta',
  'A_CommonIliac_L',
  'A_CommonIliac_R',
  'A_ExternalIliac_L',
  'A_InternalIliac_L',
  'A_ExternalIliac_R',
  'A_InternalIliac_R',
  'V_InferiorVenaCava',
  'V_CommonIliac_L',
  'V_CommonIliac_R',
  'V_InternalIliac_L',
  'V_InternalIliac_R',
  'V_ExternalIliac_L',
  'V_ExternalIliac_R',
  'IliopsoasMuscle_R',
  'IliopsoasMuscle_L',
  'CaudaEquina',
  'LumbarNerveRoots_L',
  'LumbarNerveRoots_R',
  'SacralNerveRoots_L',
  'SacralNerveRoots_R',
  'Liver',
  'BowelBag',
  'Rectum',
  'AnalCanal',
  'Kidney_L',
  'Kidney_R',
  'Ureter_L',
  'Ureter_R',
  'Bladder',
  'PenileBulb',
  'DuctusDeferens_L',
  'DuctusDeferens_R',
  'Testis_L',
  'Testis_R',
  'A_Pelvic',
  'V_Pelvic'
]

# ROIs which may be defined, depending on the patient case:
optional_rois = [
  'LevatorAniMuscle_R',
  'LevatorAniMuscle_L',
  'Couch',
  
]

# All possible allowed ROIs:
allowed_rois = temp_rois + required_rois + optional_rois

# Some cases contain LevatorAniMuscle ROI. For these cases, rename it to _L and create a _R version as well:
if get_item(pm.RegionsOfInterest, "LevatorAniMuscle"):
  pm.RegionsOfInterest["LevatorAniMuscle"].Name = "LevatorAniMuscle_L"
  create_roi(name = 'LevatorAniMuscle_R', color = 'Darkcyan', type = 'Organ', alternatives=[])
  pm.RegionsOfInterest['LevatorAniMuscle_R'].OrganData.OrganType = "OrganAtRisk"

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
  'SeminalVes',
  'Prostate',
  'LN_Iliac'
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
  'Markers'
]
for marker in markers:
  if get_item(pm.RegionsOfInterest, marker):
    if not pm.RegionsOfInterest[marker].Type == 'Marker':
      failures.append(marker + ' - forventet at denne var type marker ("Marker"), fant: ' + pm.RegionsOfInterest[marker].Type)

# Test that ROIs which are defined actually are delinated:
for roi in allowed_rois:
  if get_item(pm.RegionsOfInterest, roi):
    # Get the Roi Geometry for the chosen structure set:
    rg = ss.RoiGeometries[roi]
    if not rg.HasContours():
      if roi not in ["LevatorAniMuscle_L", "LevatorAniMuscle_R"]:
        failures.append(roi + " - denne ROIen har ikke blitt tegnet!")

# Test for gaps in ROIs:
rois = required_rois

for roi in rois:
  if roi not in ["Markers"]:
    if get_item(pm.RegionsOfInterest, roi):
      missing_slices = gaps(roi)
      if len(missing_slices) > 0:
        failures.append(roi + " mangler definisjon i tilknytning til følgende snitt: " + str(missing_slices))

# Run an update on all derived ROIs:
derived_rois = [
  'A_Pelvic',
  'V_Pelvic',
  'BowelBag',
  'Bladder',
  'Vessels_with_margin'
]
for roi_name in derived_rois:
  rg = ss.RoiGeometries[roi_name]
  if rg.PrimaryShape:
    # Check for dirty shape:
    if rg.PrimaryShape.DerivedRoiStatus:
      if rg.PrimaryShape.DerivedRoiStatus.IsShapeDirty == True:
        # For any dirty ROI, update it:
        rg.OfRoi.UpdateDerivedGeometry(Examination=ss.OnExamination, Algorithm="Auto")
    else:
      # Check for empty, derived ROI:
      if rg.OfRoi.DerivedRoiExpression:
        # Construct the ROI by using the update feature:
        rg.OfRoi.UpdateDerivedGeometry(Examination=ss.OnExamination, Algorithm="Auto")

# Test for overlapping slices:
# Rectum and BowelBag:
overlap_slices = overlapping_slices(ss, "BowelBag", "Rectum")
if len(overlap_slices) > 0:
  failures.append("BowelBag er definert i overlappende snitt med Rectum: " + str(overlap_slices))
# Rectum and AnalCanal:
overlap_slices = overlapping_slices(ss, "AnalCanal", "Rectum")
if len(overlap_slices) > 0:
  failures.append("AnalCanal er definert i overlappende snitt med Rectum: " + str(overlap_slices))

# Create a success message if there are zero failures:
if len(failures) == 0:
  failures.append("PERFEKT!!!  :)")


# Log finish time:
time_end = datetime.datetime.now()
elapsed_time = time_end - time_start
if elapsed_time.seconds > 3600:
  hours = elapsed_time.seconds // 3600 % 3600
  minutes = (elapsed_time.seconds - hours * 3600) // 60 % 60
  seconds = elapsed_time.seconds - hours * 3600 - minutes * 60
else:
  hours = 0
  minutes = elapsed_time.seconds // 60 % 60
  seconds = elapsed_time.seconds - minutes * 60
if hours > 0:
  time_str = "Tidsbruk: " +str(hours) + " time(r) " + str(minutes) + " min " + str(seconds) + " sek"
else:
  time_str = "Tidsbruk: " + str(minutes) + " min " + str(seconds) + " sek"


# Display the results:
root = Tk()
root.withdraw()
title = "Prostate pelvic Deep Learning project"
text = "\n".join(failures) + "\n\n" + time_str
messagebox.showinfo(title, text)
root.destroy()
