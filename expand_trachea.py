# Expand the trachea ROI by 1.5mm laterally and AP.
# The reason for having this script, is that it is easier to delineate manually the internal wall
# of the trachea, then expand it, then to manually delieate the outer walls of the trachea.

# RayStation 10B - Python 3.6

# System files:
from connect import *
import sys

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# Load the patient model:
pm = case.PatientModel

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

# A function expanding a ROI laterally and AP by 0.15 mm.
def expand(new_roi_name, original_roi):
  # Verify input:
  assert isinstance(new_roi_name, str), "master_rois is not a string: %r" % new_roi_name
  # Make sure our new ROI doesnt exist:
  if get_item(pm.RegionsOfInterest, new_roi_name):
    raise Exception("The new ROI already exists for this patient. Please check your code...")
  else:
    # Create it:
    new_roi = pm.CreateRoi(Name = 'Trachea', Color = '64, 128, 128', Type = 'Organ')
  # Use ROI Algebra to create an expanded ROI:
  pm.RegionsOfInterest[new_roi.Name].CreateAlgebraGeometry(
    Examination = examination,
    ExpressionA =  { 'Operation': "Union", 'SourceRoiNames': [original_roi.Name], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.15, 'Posterior': 0.15, 'Right': 0.15, 'Left': 0.15 } },
    ResultMarginSettings =  { 'Type': "Contract", 'Superior' : 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 }
  )
  pm.RegionsOfInterest[new_roi.Name].SetAlgebraExpression(
    ExpressionA =  { 'Operation': "Union", 'SourceRoiNames': [original_roi.Name], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.15, 'Posterior': 0.15, 'Right': 0.15, 'Left': 0.15 } },
    ResultMarginSettings =  { 'Type': "Contract", 'Superior' : 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 }
  )
  pm.RegionsOfInterest[new_roi.Name].UpdateDerivedGeometry(Examination = examination)
  # At the end, underive it, as it isnt supposed to be a derived ROI:
  pm.RegionsOfInterest[new_roi.Name].DeleteExpression()
  # Finally, delete the original ROI:
  pm.RegionsOfInterest[original_roi.Name].DeleteRoi()
  # Return the created ROI:
  return new_roi

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

# Rename original Trachea:
trachea_old = get_item(pm.RegionsOfInterest, "Trachea")
trachea_old.Name = 'Trachea_old'

# Create expanded Trachea ROI:
trachea = expand('Trachea', trachea_old)

# With the expanded Trachea we may need to crop some neighbouring ROIs to remove overlap:
# From Trachea, extract Esophagus:
if get_item(pm.RegionsOfInterest, "Esophagus"):
  remove_overlap(["Trachea"], "Esophagus")
# From Trachea, extract ThyroidGland:
if get_item(pm.RegionsOfInterest, "ThyroidGland"):
  remove_overlap(["Trachea"], "ThyroidGland")
# From Trachea, extract Lung_R:
if get_item(pm.RegionsOfInterest, "Lung_R"):
  remove_overlap(["Trachea"], "Lung_R")