# Creates ROIs to be used in a Thorax Bone Deep learning segmentation project.
# This script is designed to be run after a patient has been imported in the research environment.
# It does the following:
# -Creates new ROIs which are not originally present
# -Renames ROIs which are present, but have a different name than the one decided for the project
# -Changes colors for some ROIs.
# -Deletes ROIs which are not supposed to be included in the project


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


# Bone colors:
bone_color1 = 'ForestGreen'
bone_color2 = 'Lime'
bone_color3 = 'YellowGreen'
cartilage_color = 'PaleGreen'

# Create ROIs:
# Humeral Head Neck:
create_roi(name = 'HumeralHeadNeck_R', color = bone_color1, type = 'Organ', alternatives=['HumeralHead_R'])
create_roi(name = 'HumeralHeadNeck_L', color = bone_color1, type = 'Organ', alternatives=['HumeralHead_L'])
# Scapula:
create_roi(name = 'Scapula_R', color = bone_color3, type = 'Organ', alternatives=[])
create_roi(name = 'Scapula_L', color = bone_color3, type = 'Organ', alternatives=[])
# Clavicle:
create_roi(name = 'Clavicle_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Clavicle_L', color = bone_color2, type = 'Organ', alternatives=[])
# Sternum:
create_roi(name = 'Sternum', color = bone_color3, type = 'Organ', alternatives=[])
# Ribs:
# Right:
create_roi(name = 'Rib1_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib2_R', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib3_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib4_R', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib5_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib6_R', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib7_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib8_R', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib9_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib10_R', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib11_R', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib12_R', color = bone_color1, type = 'Organ', alternatives=[])
# Left:
create_roi(name = 'Rib1_L', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib2_L', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib3_L', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib4_L', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib5_L', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib6_L', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib7_L', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib8_L', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib9_L', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib10_L', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Rib11_L', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Rib12_L', color = bone_color1, type = 'Organ', alternatives=[])
# Ribs Algebra (union):
ribs_r = create_roi(name = 'Ribs_R', color = bone_color3, type = 'Organ', alternatives=[])
ribs_r.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['Rib1_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Rib2_R', 'Rib3_R', 'Rib4_R', 'Rib5_R', 'Rib6_R', 'Rib7_R', 'Rib8_R', 'Rib9_R', 'Rib10_R', 'Rib11_R', 'Rib12_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
ribs_r.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
ribs_l = create_roi(name = 'Ribs_L', color = bone_color3, type = 'Organ', alternatives=[])
ribs_l.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['Rib1_L'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Rib2_L', 'Rib3_L', 'Rib4_L', 'Rib5_L', 'Rib6_L', 'Rib7_L', 'Rib8_L', 'Rib9_L', 'Rib10_L', 'Rib11_L', 'Rib12_L'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
ribs_l.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Vertebra:
create_roi(name = 'C7', color = bone_color3, type = 'Organ', alternatives=[])
create_roi(name = 'Th1', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Th2', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Th3', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Th4', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Th5', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Th6', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Th7', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Th8', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Th9', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Th10', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Th11', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'Th12', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'L1', color = bone_color3, type = 'Organ', alternatives=[])
# Costal Cartilage:
create_roi(name = 'CostalCartilage_R', color = cartilage_color, type = 'Organ', alternatives=[])
create_roi(name = 'CostalCartilage_L', color = cartilage_color, type = 'Organ', alternatives=[])

# Create DL ROIs:
ss = case.TreatmentPlans[0].BeamSets[0].GetStructureSet()
dl_rois = ["Liver", "Pancreas", "Spleen", "Stomach"]
for roi in dl_rois:
  create = True
  if get_item(pm.RegionsOfInterest, roi):
    # Check for existing contour:
    rg = ss.RoiGeometries[roi]
    if rg.HasContours():
      create = False
  if create:
    examination.RunOarSegmentation(ModelName="RSL Thorax-Abdomen CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=[roi])

# Update ROI types:
# This code is moved a bit after the creation of these ROIs, because of a scaling issue discovered in RayStation.
# When many ROIs are created, there is a delay which makes RayStation crash if we attempt to edit a ROI immediately after creation.
pm.RegionsOfInterest['HumeralHeadNeck_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['HumeralHeadNeck_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Scapula_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Scapula_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Clavicle_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib1_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Clavicle_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Sternum'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib2_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib3_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib4_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib5_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib6_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib7_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib8_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib9_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib10_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib11_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib12_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib1_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib2_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib3_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib4_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib5_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib6_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib7_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib8_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib9_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib10_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib11_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rib12_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Ribs_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Ribs_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['C7'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th1'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th2'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th3'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th4'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th5'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th6'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th7'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th8'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th9'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th10'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th11'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Th12'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['L1'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['CostalCartilage_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['CostalCartilage_L'].OrganData.OrganType = "Other"

# Adjust colors:
for roi in ['Clips_L', 'Clips_R', 'BreastString_L', 'BreastString_R']:
  if get_item(pm.RegionsOfInterest, roi):
    pm.RegionsOfInterest[roi].Color = 'Magenta'
if get_item(pm.RegionsOfInterest, 'Heart'):
    pm.RegionsOfInterest['Heart'].Color = 'Maroon'
if get_item(pm.RegionsOfInterest, 'A_LAD'):
    pm.RegionsOfInterest['A_LAD'].Color = 'Red'

# Delete ROIs:
# Delete known ROIs which we know we do not want:
delete = [
  'SpinalCanal',
  '(DL) A_LAD',
  '(DL) BreastString_R',
  '(DL) Breast_L',
  '(DL) Breast_R',
  '(DL) Clips_R',
  '(DL) Esophagus',
  '(DL) Heart',
  '(DL) HumeralHead_R',
  '(DL) LN_Ax_L1_R',
  '(DL) LN_Ax_L2_R',
  '(DL) LN_Ax_L3_R',
  '(DL) LN_Ax_L4_R',
  '(DL) LN_Ax_Pectoral_R',
  '(DL) LN_IMN_R',
  '(DL) Lung_L',
  '(DL) Lung_R',
  '(DL) SpinalCanal',
  '(DL) SpinalCanalFull',
  '(DL) Sternum',
  '(DL) SurgicalBed_R',
  '(DL) ThyroidGland',
  '(DL) Trachea',
  '(DL) A_LAD (1)',
  '(DL) BreastString_R (1)',
  '(DL) Breast_L (1)',
  '(DL) Breast_R (1)',
  '(DL) Clips_R (1)',
  '(DL) Esophagus (1)',
  '(DL) Heart (1)',
  '(DL) HumeralHead_R (1)',
  '(DL) LN_Ax_L1_R (1)',
  '(DL) LN_Ax_L2_R (1)',
  '(DL) LN_Ax_L3_R (1)',
  '(DL) LN_Ax_L4_R (1)',
  '(DL) LN_Ax_Pectoral_R (1)',
  '(DL) LN_IMN_R (1)',
  '(DL) Lung_L (1)',
  '(DL) Lung_R (1)',
  '(DL) SpinalCanal (1)',
  '(DL) SpinalCanalFull (1)',
  '(DL) Sternum (1)',
  '(DL) SurgicalBed_R (1)',
  '(DL) ThyroidGland (1)',
  '(DL) Trachea (1)'
]

for name in delete:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass
  

# ROIs which are required to always be present:
required_rois = [
  'External',
  'Breast_R_Draft',
  'Breast_L_Draft',
  'Breast_R',
  'Breast_L',
  'Sternum',
  'Lung_R',
  'Lung_L',
  'Heart',
  'A_LAD',
  'SpinalCanalFull',
  'ThyroidGland',
  'Trachea',
  'Esophagus',
  'Liver',
  'Pancreas',
  'Spleen',
  'Stomach',
  'HumeralHeadNeck_R',
  'HumeralHeadNeck_L',
  'Scapula_R',
  'Scapula_L',
  'Clavicle_R',
  'Clavicle_L',
  'Rib1_R',
  'Rib2_R',
  'Rib3_R',
  'Rib4_R',
  'Rib5_R',
  'Rib6_R',
  'Rib7_R',
  'Rib8_R',
  'Rib9_R',
  'Rib10_R',
  'Rib11_R',
  'Rib12_R',
  'Rib1_L',
  'Rib2_L',
  'Rib3_L',
  'Rib4_L',
  'Rib5_L',
  'Rib6_L',
  'Rib7_L',
  'Rib8_L',
  'Rib9_L',
  'Rib10_L',
  'Rib11_L',
  'Rib12_L',
  'Ribs_R',
  'Ribs_L',
  'C7',
  'Th1',
  'Th2',
  'Th3',
  'Th4',
  'Th5',
  'Th6',
  'Th7',
  'Th8',
  'Th9',
  'Th10',
  'Th11',
  'Th12',
  'L1',
  'CostalCartilage_R',
  'CostalCartilage_L',
]

# ROIs which may be defined, depending on the patient case:
optional_rois = [
  'Couch',
  'SurgicalBed_R',
  'Clips_R',
  'BreastString_R',
  'ScaleneMusc_Ant_R',
  'A_Brachioceph',
  'A_Subclavian_R+A_Axillary_R',
  'A_Carotid_R',
  'V_Brachioceph_R',
  'V_Subclavian_R+V_Axillary_R',
  'V_Jugular_R',
  'LN_Ax_L1_R',
  'LN_Ax_L2_R',
  'LN_Ax_L3_R',
  'LN_Ax_L4_R',
  'LN_Ax_Pectoral_R',
  'LN_IMN_R',
  'SurgicalBed_L',
  'Clips_L',
  'BreastString_L',
  'ScaleneMusc_Ant_L',
  'A_Subclavian_L+A_Axillary_L',
  'A_Carotid_L',
  'V_Brachioceph_L',
  'V_Subclavian_L+V_Axillary_L',
  'V_Jugular_L',
  'LN_Ax_L1_L',
  'LN_Ax_L2_L',
  'LN_Ax_L3_L',
  'LN_Ax_L4_L',
  'LN_Ax_Pectoral_L',
  'LN_IMN_L',
]

# All possible allowed ROIs:
allowed_rois = required_rois + optional_rois

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
  'LN_Ax_L1_R',
  'LN_Ax_L2_R',
  'LN_Ax_L3_R',
  'LN_Ax_L4_R',
  'LN_Ax_Pectoral_R',
  'LN_IMN_R',
  'SurgicalBed_R',
  'LN_Ax_L1_L',
  'LN_Ax_L2_L',
  'LN_Ax_L3_L',
  'LN_Ax_L4_L',
  'LN_Ax_Pectoral_L',
  'LN_IMN_L',
  'SurgicalBed_L',
]
for target in targets:
  if get_item(pm.RegionsOfInterest, target):
    if not pm.RegionsOfInterest[target].Type == 'Ctv':
      failures.append(target + ' - forventet at denne var type target ("Ctv"), fant: ' + pm.RegionsOfInterest[target].Type)

# Test for type organ/organ at risk:
risk_organs = [
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
  'Pancreas',
  'Spleen',
  'Stomach',
]
for organ in risk_organs:
  if get_item(pm.RegionsOfInterest, organ):
    if not pm.RegionsOfInterest[organ].Type == 'Organ':
      failures.append(organ + ' - forventet at denne var type "Organ", fant: ' + pm.RegionsOfInterest[organ].Type)
    else:
      if not pm.RegionsOfInterest[organ].OrganData.OrganType == 'OrganAtRisk':
        failures.append(organ + ' - forventet at denne har OrganType "OrganAtRisk", fant: ' + pm.RegionsOfInterest[organ].OrganData.OrganType)

# Test for type target/OAR:
targets_or_oars = [
  'Breast_R',
  'Breast_L',
]
for too in targets_or_oars:
  if get_item(pm.RegionsOfInterest, too):
    if not pm.RegionsOfInterest[too].Type in ['Ctv', 'Organ']:
      failures.append(too + ' - forventet at denne var type target ("Ctv") eller "OrganAtRisk", fant: ' + pm.RegionsOfInterest[too].Type)

# Test for type marker:
markers = [
  'Clips_R',
  'BreastString_R'
]
for marker in markers:
  if get_item(pm.RegionsOfInterest, marker):
    if not pm.RegionsOfInterest[marker].Type == 'Marker':
      failures.append(marker + ' - forventet at denne var type marker ("Marker"), fant: ' + pm.RegionsOfInterest[marker].Type)

# Other/Target definition support structures:
support_organs = [
  'ScaleneMusc_Ant_R',
  'A_Brachioceph',
  'A_Subclavian_R+A_Axillary_R',
  'A_Carotid_R',
  'V_Brachioceph_R',
  'V_Subclavian_R+V_Axillary_R',
  'V_Jugular_R',
  'HumeralHeadNeck_R',
  'HumeralHeadNeck_L',
  'Scapula_R',
  'Scapula_L',
  'Clavicle_R',
  'Clavicle_L',
  'Rib1_R',
  'Rib2_R',
  'Rib3_R',
  'Rib4_R',
  'Rib5_R',
  'Rib6_R',
  'Rib7_R',
  'Rib8_R',
  'Rib9_R',
  'Rib10_R',
  'Rib11_R',
  'Rib12_R',
  'Rib1_L',
  'Rib2_L',
  'Rib3_L',
  'Rib4_L',
  'Rib5_L',
  'Rib6_L',
  'Rib7_L',
  'Rib8_L',
  'Rib9_L',
  'Rib10_L',
  'Rib11_L',
  'Rib12_L',
  'C7',
  'Th1',
  'Th2',
  'Th3',
  'Th4',
  'Th5',
  'Th6',
  'Th7',
  'Th8',
  'Th9',
  'Th10',
  'Th11',
  'Th12',
  'L1',
  'CostalCartilage_R',
  'CostalCartilage_L',
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