# Processes ROIs to be used in the Breast_R Deep Learning validation project.
# This script is designed to be run after a patient has been imported in the research environment.
# It does the following:
# -Creates new ROIs which are not originally present
# -Renames ROIs which are present, but have a different name than the one decided for the project
# -Deletes ROIs which are not supposed to be included in the project

# RayStation 10B - Python 3.6

from connect import *

# Used for GUI debugging:
#from tkinter import *
#from tkinter import messagebox

#root = Tk()
#root.withdraw()
#title = "Deep Learning validation project"
#text = ""
#messagebox.showinfo(title, text)
#root.destroy()

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# The patient model:  
pm = case.PatientModel

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


# Create ROIs:
# External:
external = create_roi(name = 'External', color = '255, 173, 91', type = 'External', alternatives=['Body'])

# Target volumes:
# Breast left (draft and final):
create_roi(name = 'Breast_R_Draft', color = '255, 128, 128', type = 'Undefined', alternatives=['Breast draft'])
pm.RegionsOfInterest['Breast_R_Draft'].OrganData.OrganType = "Target"
breast_r = create_roi(name = 'Breast_R', color = '255, 128, 128', type = 'Ctv', alternatives=['CTV', 'CTV 0-40', 'CTV 46-50', 'ctv breast', 'CTV_50', 'CTVp'])
# To avoid issues with the prescription with the original plan, assume this is correct and dont need to be set:
breast_r.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [r"Breast_R_Draft"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"External"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } }, ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
breast_r.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Other targets:
create_roi(name = 'LN_Ax_L1_R', color = '255, 255, 128', type = 'Ctv', alternatives=['Level 1', 'LN_Ax_L1'])
pm.RegionsOfInterest['LN_Ax_L1_R'].OrganData.OrganType = "Target"
create_roi(name = 'LN_Ax_L2_R', color = '128, 0, 0', type = 'Ctv', alternatives=['Level 2', 'LN_Ax_L2'])
pm.RegionsOfInterest['LN_Ax_L2_R'].OrganData.OrganType = "Target"
create_roi(name = 'LN_Ax_L3_R', color = '0, 0, 160', type = 'Ctv', alternatives=['Level 3', 'LN_Ax_L3'])
pm.RegionsOfInterest['LN_Ax_L3_R'].OrganData.OrganType = "Target"
create_roi(name = 'LN_Ax_L4_R', color = '255, 128, 64', type = 'Ctv', alternatives=['Level 4', 'LN_Ax_L4'])
pm.RegionsOfInterest['LN_Ax_L4_R'].OrganData.OrganType = "Target"
create_roi(name = 'LN_Ax_Pectoral_R', color = '128, 255, 255', type = 'Ctv', alternatives=['Level interpectoral nodes', 'LN_Ax_Pectoral'])
pm.RegionsOfInterest['LN_Ax_Pectoral_R'].OrganData.OrganType = "Target"
create_roi(name = 'LN_IMN_R', color = '255, 128, 128', type = 'Ctv', alternatives=['LN_IMN'])
pm.RegionsOfInterest['LN_IMN_R'].OrganData.OrganType = "Target"
create_roi(name = 'SurgicalBed_R', color = '255, 128, 128', type = 'Ctv', alternatives=['CTV 40.05-56.05', 'CTV 50-66', 'CTV 40-56', 'CTVsb', 'SurgicalBed'])
pm.RegionsOfInterest['SurgicalBed_R'].OrganData.OrganType = "Target"
# Organs:
# OARs:
# Already used sometimes (AL)
create_roi(name = 'Lung_R', color = '0, 255, 0', type = 'Organ', alternatives=['Lung right'])
create_roi(name = 'Lung_L', color = '0, 255, 0', type = 'Organ', alternatives=['Lung left'])
create_roi(name = 'Heart', color = 'Red', type = 'Organ', alternatives=[])
create_roi(name = 'SpinalCanalFull', color = 'Blue', type = 'Organ', alternatives=['SpinalCord', 'Spinalcord', 'SpinalCanal'])
create_roi(name = 'A_LAD', color = 'Yellow', type = 'Organ', alternatives=['LAD'])
create_roi(name = 'HumeralHead_R', color = '64, 128, 128', type = 'Organ', alternatives=['Caput Humeri', 'Caput humeri', 'Humeral_Head_L/R', 'Humeral_Head_R'])
create_roi(name = 'Liver', color = '255, 255, 128', type = 'Organ', alternatives=[])
# Breast left (draft and final):
create_roi(name = 'Breast_L_Draft', color = '255, 192, 203', type = 'Organ', alternatives=['Breast left', 'Contra lateral breast', 'Contralat breast draft'])
pm.RegionsOfInterest['Breast_L_Draft'].OrganData.OrganType = "OrganAtRisk"
breast_r = create_roi(name = 'Breast_L', color = '255, 192, 203', type = 'Organ', alternatives=['Contralat breast'])
pm.RegionsOfInterest['Breast_L'].OrganData.OrganType = "OrganAtRisk"
breast_r.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [r"Breast_L_Draft"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"External"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.5, 'Inferior': 0.5, 'Anterior': 0.5, 'Posterior': 0.5, 'Right': 0.5, 'Left': 0.5 } }, ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
breast_r.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# New OARs for this DL project:
create_roi(name = 'ThyroidGland', color = '64, 128, 128', type = 'Organ', alternatives=[])
create_roi(name = 'Trachea', color = '64, 128, 128', type = 'Organ', alternatives=[])
create_roi(name = 'Esophagus', color = '255, 192, 0', type = 'Organ', alternatives=['esofagus'])
create_roi(name = 'Sternum', color = '64, 128, 128', type = 'Organ', alternatives=[])
# Other organs:
# Organs that are support for lymph node definition:
# Muscles:
create_roi(name = 'ScaleneMusc_Ant_R', color = '64, 0, 0', type = 'Organ', alternatives=['Scalene muscle ant', 'Musc_Scalene', 'ScaleneMusc', 'ScaleneMusc_Ant'])
pm.RegionsOfInterest['ScaleneMusc_Ant_R'].OrganData.OrganType = "Other"
# Arteries:
create_roi(name = 'A_Subclavian_R+A_Axillary_R', color = 'Red', type = 'Organ', alternatives=['Subclavian and axillary artery', 'A_Subclavian'])
pm.RegionsOfInterest['A_Subclavian_R+A_Axillary_R'].OrganData.OrganType = "Other"
create_roi(name = 'A_Carotid_R', color = 'Red', type = 'Organ', alternatives=['Common carotid artery', 'A_Carotid'])
pm.RegionsOfInterest['A_Carotid_R'].OrganData.OrganType = "Other"
create_roi(name = 'A_Brachioceph', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_Brachioceph'].OrganData.OrganType = "Other"
# Veins:
create_roi(name = 'V_Brachioceph_R', color = 'Blue', type = 'Organ', alternatives=['Brachiocephalic / subclavian / axillary vein', 'V_Brachiocephls / V_subclavian', 'V_Brachiocephls/ V_Subclavian', 'V_Brachioceph+V_Subclavian_R'])
pm.RegionsOfInterest['V_Brachioceph_R'].OrganData.OrganType = "Other"
create_roi(name = 'V_Subclavian_R+V_Axillary_R', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_Subclavian_R+V_Axillary_R'].OrganData.OrganType = "Other"
create_roi(name = 'V_Jugular_R', color = 'Blue', type = 'Organ', alternatives=['Internal jugular vein', 'V_Jugular_Int', 'V_Jugular_Internal'])
pm.RegionsOfInterest['V_Jugular_R'].OrganData.OrganType = "Other"

# Non-organs:
# Clips:
clips_r = create_roi(name = 'Clips_R', color = 'Magenta', type = 'Marker', alternatives=[])
pm.RegionsOfInterest['Clips_R'].OrganData.OrganType = "Other"
# Breast string (temporary ROIs and final):
string_step1 = create_roi(name = 'BreastString_Step1', color = 'Magenta', type = 'Undefined', alternatives=[])
string_step1.GrayLevelThreshold(Examination=examination, LowThreshold=150, HighThreshold=3071, PetUnit=r"", CbctUnit=None, BoundingBox=None)
string_step2 = create_roi(name = 'BreastString_Step2', color = 'Magenta', type = 'Undefined', alternatives=[])
string_step2.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [r"BreastString_Step1"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"External"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.2, 'Inferior': 0.2, 'Anterior': 0.2, 'Posterior': 0.2, 'Right': 0.2, 'Left': 0.2 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
string_step2.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
string = create_roi(name = 'BreastString_R', color = 'Magenta', type = 'Marker', alternatives=[])
pm.RegionsOfInterest['BreastString_R'].OrganData.OrganType = "Other"
string.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [r"BreastString_Step2"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"Breast_R"], 'MarginSettings': { 'Type': "Expand", 'Superior': 3, 'Inferior': 3, 'Anterior': 3, 'Posterior': 3, 'Right': 3, 'Left': 3 } }, ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
string.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Set clips definition:
clips_r.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [r"BreastString_Step1"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"Breast_R"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.2, 'Inferior': 0.2, 'Anterior': 0.2, 'Posterior': 0.2, 'Right': 0.2, 'Left': 0.2 } }, ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
clips_r.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

# Delete ROIs:
# Delete known ROIs which we know we do not want:
delete = [
  'PTV 0-40',
  'PTV 40.05-56.05',
  'PTV 0-46',
  'PTV 46-50',
  'PTV 50-66',
  'PTV boost',
  'PTV40-56',
  'PTV_50',
  'PTV!_47',
  'PTV!_47c',
  'PTVn',
  'PTVp',
  'PTVpn',
  'PTV',
  'PTVc',
  'PTVpc',
  'PTVnc',
  'PTVsbc',
  'PTVsbc (robust)',
  'PTVsbc_Wall',
  'PTV_50c',
  'PTV_47c',
  'PTVopt',
  'Ptv opt',
  'PTV_IMN',
  'PTV_Robustness',
  'PTV_robustness',
  'CTV',
  'CTV 0-46',
  'CTV!_47',
  'CTV_47+50',
  'CTVn',
  'CTVpn',
  'ctv -95%',
  'CTV-95',
  'CTVsb',
  'wall ptv',
  '105',
  '105.',
  '105..',
  '1052',
  '105,2',
  '105 2',
  '105_2',
  '105_3',
  '105_4',
  '105-a',
  '105-c',
  '105-c1',
  '105o',
  '105ny',
  '105_Vmat',
  'max',
  'CTV low',
  'PTV',
  'test',
  'Lung Union',
  'Lungs',
  'Bolus .5',
  'Seed 1',
  'Seed 2',
  'Seed 3',
  'Seed 4',
  'opt',
  'opt47',
  'opt50',
  'Opt CTV',
  'opt CTV',
  '42',
  '42.2',
  '48.3',
  '89',
  '95%',
  '95',
  'CTV-95',
  'dose',
  'DV',
  'Gatingpute',
  'Heart (XVI)',
  'Markers',
  'Skråpute',
  'hevelse',
  'hevelse brys 29-10',
  'Z_ThyroidGland',
  'Lung left XVI'
]

for name in delete:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass
  

