# Adds chestwall ROIs to be used in a Thorax Bone Deep learning segmentation project.
# This script is designed to be run after a patient has been imported in the research environment.
# It does the following:
# -Creates new ROIs for manual segmentation: InterCostalMuscles_R_Draft, InterCostalMuscles_L_Draft
# -Creates derived ROI variants of the above ROIs: InterCostalMuscles_R, InterCostalMuscles_L
# -Creatse derived ROIs (union of all chestwall substructures): Chestwall_R, Chestwall_R


from connect import *

# Used for GUI debugging:
from tkinter import *
from tkinter import messagebox

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# The patient model:  
pm = case.PatientModel

# Store test results in this list:
failures = []

# Types of ROIs: External, Ptv, Ctv, Bolus, Organ, Marker, Cavity, Support, Fixation, Undefined

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

# Create empty ROIs:
create_roi(name = 'InterCostalMuscles_R_Draft', color = 'Teal', type = 'Undefined', alternatives=[])
create_roi(name = 'InterCostalMuscles_L_Draft', color = 'Teal', type = 'Undefined', alternatives=[])

# Create derived ROIs (with ROI Algebra):
costal_r = create_roi(name = 'InterCostalMuscles_R', color = 'Teal', type = 'Organ', alternatives=[])
costal_r.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['InterCostalMuscles_R_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Lung_R', 'Sternum', 'Scapula_R', 'Clavicle_R', 'Ribs_R', 'CostalCartilage_R', 'Th1', 'Th2', 'Th3', 'Th4', 'Th5', 'Th6', 'Th7', 'Th8', 'Th9', 'Th10', 'Th11', 'Th12'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
costal_r.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
costal_l = create_roi(name = 'InterCostalMuscles_L', color = 'Teal', type = 'Organ', alternatives=[])
costal_l.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['InterCostalMuscles_L_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Lung_L', 'Sternum', 'Scapula_L', 'Clavicle_L', 'Ribs_L', 'CostalCartilage_L', 'Th1', 'Th2', 'Th3', 'Th4', 'Th5', 'Th6', 'Th7', 'Th8', 'Th9', 'Th10', 'Th11', 'Th12'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
costal_l.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
chestwall_r = create_roi(name = 'Chestwall_R', color = 'Purple', type = 'Organ', alternatives=[])
chestwall_r.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['InterCostalMuscles_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Ribs_R', 'CostalCartilage_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
chestwall_r.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
chestwall_l = create_roi(name = 'Chestwall_L', color = 'Purple', type = 'Organ', alternatives=[])
chestwall_l.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['InterCostalMuscles_L'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Ribs_L', 'CostalCartilage_L'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
chestwall_l.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

# Update ROI types:
pm.RegionsOfInterest['InterCostalMuscles_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['InterCostalMuscles_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Chestwall_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Chestwall_L'].OrganData.OrganType = "Other"

