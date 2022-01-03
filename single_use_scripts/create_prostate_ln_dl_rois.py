# Processes ROIs to be used in the Prostate+LN Deep Learning project.
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
#title = "COBRA Deep Learning project"
#text = ""
#messagebox.showinfo(title, text)
#root.destroy()

# Load local files:
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
import patient_model_functions as PMF
import structure_set_functions as SSF

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# The patient model:  
pm = case.PatientModel

# Load structure set:
ss = PMF.get_structure_set(pm, examination)

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

# ROI colors:
bone_color = '23, 107, 43'
  
# Create ROIs:
# External:
external = create_roi(name = 'External', color = '255, 173, 91', type = 'External', alternatives=['Body'])

# Target volumes:
# Prostate, vesicles and nodes:
create_roi(name = 'Prostate', color = 'Magenta', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Prostate'].OrganData.OrganType = "Target"
create_roi(name = 'SeminalVes', color = '255, 128, 255', type = 'Organ', alternatives=['Seminal vesicles'])
pm.RegionsOfInterest['SeminalVes'].OrganData.OrganType = "Target"
create_roi(name = 'LN_Iliac', color = 'Magenta', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['LN_Iliac'].OrganData.OrganType = "Target"

# Organs:
# Intestinal:
create_roi(name = 'BowelBag', color = '64, 0, 0', type = 'Organ', alternatives=['Bowel space'])
pm.RegionsOfInterest['BowelBag'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Rectum', color = 'SaddleBrown', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Rectum'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'AnalCanal', color = '64, 0, 0', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['AnalCanal'].OrganData.OrganType = "OrganAtRisk"
# Urological:
create_roi(name = 'Kidney_L', color = '255, 160, 122', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Kidney_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Kidney_R', color = '255, 160, 122', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Kidney_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Ureter_L', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Ureter_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Ureter_R', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Ureter_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Bladder', color = 'Yellow', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Bladder'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Urethra', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Urethra'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'PenileBulb', color = '255, 160, 122', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['PenileBulb'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Testis_L', color = '255, 160, 122', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Testis_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Testis_R', color = '255, 160, 122', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Testis_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'DuctusDeferens_L', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['DuctusDeferens_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'DuctusDeferens_R', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['DuctusDeferens_R'].OrganData.OrganType = "OrganAtRisk"
# Nerves:
create_roi(name = 'SpinalCanal', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['SpinalCanal'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'CaudaEquina', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['CaudaEquina'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'SacralNerveRoots', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['SacralNerveRoots'].OrganData.OrganType = "OrganAtRisk"
# Other organs:
# Vessels:
create_roi(name = 'A_DescendingAorta', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_DescendingAorta'].OrganData.OrganType = "Other"
create_roi(name = 'A_InternalIliac', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_InternalIliac'].OrganData.OrganType = "Other"
create_roi(name = 'A_ExternalIliac', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_ExternalIliac'].OrganData.OrganType = "Other"
create_roi(name = 'V_InferiorVenaCava', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_InferiorVenaCava'].OrganData.OrganType = "Other"
create_roi(name = 'V_InternalIliac', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_InternalIliac'].OrganData.OrganType = "Other"
create_roi(name = 'V_ExternalIliac', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_ExternalIliac'].OrganData.OrganType = "Other"
# Bone:
create_roi(name = 'FemurHeadNeck_L', color = bone_color, type = 'Organ', alternatives=['FemoralHead_L', 'Femoral head left'])
pm.RegionsOfInterest['FemurHeadNeck_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'FemurHeadNeck_R', color = bone_color, type = 'Organ', alternatives=['FemoralHead_R', 'Femoral head right'])
pm.RegionsOfInterest['FemurHeadNeck_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'PelvicGirdle_L', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['PelvicGirdle_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'PelvicGirdle_R', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['PelvicGirdle_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Sacrum', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Sacrum'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L2', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L2'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L3', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L3'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L4', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L4'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L5', color = bone_color, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L5'].OrganData.OrganType = "OrganAtRisk"

# Non-organs:
# Prostate seed markers:
# Does markers exist already? (If so, we'll set up our marker ROI as a union of those)
marker_candidates = ['Seed 1', 'Seed 2', 'Seed 3', 'Seed 4', 'Marker1', 'Marker2', 'Marker3']
marker_rois = []
# Add ones that exist to our list:
for candidate in marker_candidates:
  if SSF.has_named_roi_with_contours(ss, candidate):
    marker_rois.append(candidate)
# If we have a list of verified marker ROIs, create a ROI algebra based on it (if not, create empty ROI):
markers = create_roi(name = 'Markers', color = 'Blue', type = 'Marker', alternatives=[])
pm.RegionsOfInterest['Markers'].OrganData.OrganType = "Other"
if len(marker_rois) > 1:
  markers.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': marker_rois, 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"External"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } }, ResultOperation="Intersection", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
  markers.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

# If we delete the prescription volume, RayStation will crash. To avoid this, set the prescription
# of any existing plans to Prostate, before proceeding with deleting ROIs:
for plan in case.TreatmentPlans:
  for bs in plan.BeamSets:
    bs.AddDosePrescriptionToRoi(RoiName="Prostate", DoseVolume=0, PrescriptionType="MedianDose", DoseValue=7700, RelativePrescriptionLevel=1, AutoScaleDose=True)

# Delete ROIs:
# Delete known ROIs which we know we do not want:
delete = [
  'CTV 0-77',
  'CTV 0-70',
  'CTV_56',
  'CTV!_56',
  'CTV_77',
  'CTV!_70',
  'CTV_Prostate_SV',
  'PTV 0-77',
  'PTV 0-70',
  'PTV_77',
  'PTV!_70',
  'PTV!_56',
  'PTV_70+77',
  'PTV_56+70+77',
  'PTV_Prostate_SV',
  'zPTV_77_Wall',
  'zPTV_70+77_Wall',
  'zBladder',
  'zRectum',
  'zBowelBag',
  'Bowel space - PTV',
  'Rectum - PTV',
  'Bladder - PTV',
  'Dorso_Rektum',
  'Wall PTV_77',
  'hjelprektum',
  'Seed 1',
  'Seed 2',
  'Seed 3',
  'Seed 4',
  'Marker1',
  'Marker2',
  'Marker3',
  '79',
]

for name in delete:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass
  

