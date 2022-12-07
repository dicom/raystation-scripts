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
bone_color1 = 'ForestGreen'
bone_color2 = 'Lime'
bone_color3 = 'YellowGreen'
  
# Create ROIs:
# External:
external = create_roi(name = 'External', color = '255, 173, 91', type = 'External', alternatives=['Body'])

# Target volumes:
# Prostate, vesicles and nodes:
create_roi(name = 'Prostate', color = 'DeepPink', type = 'Ctv', alternatives=[])
pm.RegionsOfInterest['Prostate'].OrganData.OrganType = "Target"
create_roi(name = 'SeminalVes', color = 'Violet', type = 'Ctv', alternatives=['Seminal vesicles'])
pm.RegionsOfInterest['SeminalVes'].OrganData.OrganType = "Target"
create_roi(name = 'LN_Iliac', color = 'Magenta', type = 'Ctv', alternatives=['Pelvic nodes'])
pm.RegionsOfInterest['LN_Iliac'].OrganData.OrganType = "Target"

# Organs:
# Intestinal:
create_roi(name = 'Liver', color = 'Khaki', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Liver'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'BowelBag_Draft', color = 'SandyBrown', type = 'Organ', alternatives=['Bowel space', 'BowelBag', 'Spc_Bowel', 'BowelBag_draft'])
pm.RegionsOfInterest['BowelBag_Draft'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Rectum', color = 'SaddleBrown', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Rectum'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'AnalCanal', color = 'Maroon', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['AnalCanal'].OrganData.OrganType = "OrganAtRisk"
# Urological:
create_roi(name = 'Kidney_L', color = 'LightSalmon', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Kidney_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Kidney_R', color = 'LightSalmon', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Kidney_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Ureter_L', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Ureter_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Ureter_R', color = 'Orange', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Ureter_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Bladder_Draft', color = 'Yellow', type = 'Organ', alternatives=['Bladder'])
pm.RegionsOfInterest['Bladder_Draft'].OrganData.OrganType = "OrganAtRisk"
# Bladder Algebra: Subtract Prostate:
bladder = create_roi(name = 'Bladder', color = 'Yellow', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Bladder'].OrganData.OrganType = "OrganAtRisk"
bladder.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['Bladder_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Prostate'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
bladder.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# (decided to exclude Urethra from this project)
#create_roi(name = 'Urethra', color = 'Orange', type = 'Organ', alternatives=[])
#pm.RegionsOfInterest['Urethra'].OrganData.OrganType = "OrganAtRisk"
# Genital:
create_roi(name = 'PenileBulb', color = 'PaleVioletRed', type = 'Organ', alternatives=['Penile bulbi'])
pm.RegionsOfInterest['PenileBulb'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Testis_L', color = 'Mediumvioletred', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Testis_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Testis_R', color = 'Mediumvioletred', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Testis_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'DuctusDeferens_L', color = 'Lightpink', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['DuctusDeferens_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'DuctusDeferens_R', color = 'Lightpink', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['DuctusDeferens_R'].OrganData.OrganType = "OrganAtRisk"
# Nerves:
create_roi(name = 'CaudaEquina', color = 'Blue', type = 'Organ', alternatives=['SpinalCanal', 'SpinalCord', 'Spinalkanal', 'Spinal Cord', 'Cauda Equina'])
pm.RegionsOfInterest['CaudaEquina'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'LumbarNerveRoots_L', color = 'RoyalBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['LumbarNerveRoots_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'LumbarNerveRoots_R', color = 'RoyalBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['LumbarNerveRoots_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'SacralNerveRoots_L', color = 'RoyalBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['SacralNerveRoots_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'SacralNerveRoots_R', color = 'RoyalBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['SacralNerveRoots_R'].OrganData.OrganType = "OrganAtRisk"
# Vessels:
# Arteries:
create_roi(name = 'A_DescendingAorta', color = 'Maroon', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_DescendingAorta'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'A_CommonIliac_L', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_CommonIliac_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'A_CommonIliac_R', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_CommonIliac_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'A_InternalIliac_L', color = 'Tomato', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_InternalIliac_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'A_InternalIliac_R', color = 'Tomato', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_InternalIliac_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'A_ExternalIliac_L', color = 'OrangeRed', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_ExternalIliac_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'A_ExternalIliac_R', color = 'OrangeRed', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_ExternalIliac_R'].OrganData.OrganType = "OrganAtRisk"
# Artery Algebra (union):
a_pelvic = create_roi(name = 'A_Pelvic', color = 'Red', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['A_Pelvic'].OrganData.OrganType = "OrganAtRisk"
a_pelvic.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['A_DescendingAorta'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['A_CommonIliac_L', 'A_CommonIliac_R', 'A_ExternalIliac_L', 'A_ExternalIliac_R', 'A_InternalIliac_L', 'A_InternalIliac_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
a_pelvic.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Veins:
create_roi(name = 'V_InferiorVenaCava', color = 'Navy', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_InferiorVenaCava'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'V_CommonIliac_L', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_CommonIliac_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'V_CommonIliac_R', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_CommonIliac_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'V_InternalIliac_L', color = 'SlateBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_InternalIliac_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'V_InternalIliac_R', color = 'SlateBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_InternalIliac_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'V_ExternalIliac_L', color = 'MediumSlateBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_ExternalIliac_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'V_ExternalIliac_R', color = 'MediumSlateBlue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_ExternalIliac_R'].OrganData.OrganType = "OrganAtRisk"
# Vein Algebra (union):
v_pelvic = create_roi(name = 'V_Pelvic', color = 'Blue', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['V_Pelvic'].OrganData.OrganType = "OrganAtRisk"
v_pelvic.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['V_InferiorVenaCava'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['V_CommonIliac_L', 'V_CommonIliac_R', 'V_ExternalIliac_L', 'V_ExternalIliac_R', 'V_InternalIliac_L', 'V_InternalIliac_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
v_pelvic.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Muscles:
create_roi(name = 'IliopsoasMuscle_L', color = 'Darkcyan', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['IliopsoasMuscle_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'IliopsoasMuscle_R', color = 'Darkcyan', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['IliopsoasMuscle_R'].OrganData.OrganType = "OrganAtRisk"
# Bone:
create_roi(name = 'L2', color = bone_color1, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L2'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L3', color = bone_color2, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L3'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L4', color = bone_color1, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L4'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'L5', color = bone_color2, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['L5'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'PelvicGirdle_L', color = bone_color3, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['PelvicGirdle_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'PelvicGirdle_R', color = bone_color3, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['PelvicGirdle_R'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Sacrum', color = bone_color1, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Sacrum'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'Coccyx', color = bone_color2, type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Coccyx'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'FemurHeadNeck_L', color = bone_color1, type = 'Organ', alternatives=['FemoralHead_L', 'Femoral head left'])
pm.RegionsOfInterest['FemurHeadNeck_L'].OrganData.OrganType = "OrganAtRisk"
create_roi(name = 'FemurHeadNeck_R', color = bone_color1, type = 'Organ', alternatives=['FemoralHead_R', 'Femoral head right'])
pm.RegionsOfInterest['FemurHeadNeck_R'].OrganData.OrganType = "OrganAtRisk"

# ROI Algebra:
# BowelBag Algebra (subtract Bladder, veins, etc)
bowel_bag = create_roi(name = 'BowelBag', color = 'SandyBrown', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['BowelBag'].OrganData.OrganType = "OrganAtRisk"
bowel_bag.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['BowelBag_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Bladder_Draft', 'Prostate', 'SeminalVes', 'LN_Iliac', 'PelvicGirdle_L', 'PelvicGirdle_R', 'Sacrum', 'L2', 'L3', 'L4', 'L5', 'IliopsoasMuscle_L', 'IliopsoasMuscle_R', 'A_DescendingAorta', 'A_CommonIliac_L', 'A_CommonIliac_R', 'A_ExternalIliac_L', 'A_ExternalIliac_R', 'A_InternalIliac_L', 'A_InternalIliac_R', 'V_InferiorVenaCava', 'V_CommonIliac_L', 'V_CommonIliac_R', 'V_ExternalIliac_L', 'V_ExternalIliac_R', 'V_InternalIliac_L', 'V_InternalIliac_R', 'Ureter_L', 'Ureter_R', 'Ureter_L', 'DuctusDeferens_L', 'DuctusDeferens_R', 'Kidney_L', 'Kidney_R', 'Liver'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
bowel_bag.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Vessel Algebra LN help structure (add 7 mm margin, subtract bone, muscles)
vessels_help = create_roi(name = 'Vessels_with_margin', color = 'Yellow', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Vessels_with_margin'].OrganData.OrganType = "Target"
vessels_help.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["A_Pelvic", "V_Pelvic"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.7, 'Inferior': 0.7, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["FemurHeadNeck_L", "FemurHeadNeck_R", "Rectum", "L2", "L3", "L4", "L5", "PelvicGirdle_L", "PelvicGirdle_R", "Sacrum", "IliopsoasMuscle_L", "IliopsoasMuscle_R"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
vessels_help.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")


# Non-organs:
# Prostate seed markers:
# Does markers exist already? (If so, we'll set up our marker ROI as a union of those)
marker_candidates = ['Markers', 'Seed iso', 'Seed 1', 'Seed 2', 'Seed 3', 'Seed 4', 'Marker1', 'Marker2', 'Marker3', 'Marker4']
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
    if bs.Prescription.PrimaryPrescriptionDoseReference.OnStructure.Name != 'Prostate':
      bs.AddDosePrescriptionToRoi(RoiName="Prostate", DoseVolume=0, PrescriptionType="MedianDose", DoseValue=7700, RelativePrescriptionLevel=1, AutoScaleDose=True)

# Delete ROIs:
# Delete known ROIs which we know we do not want:
delete = [
  'CTV',
  'CTV 0-77',
  'CTV 0-70',
  'CTV 0-56',
  'CTV 0-77 union',
  'CTV_56',
  'CTV!_56',
  'CTV!_66',
  'CTV_74',
  'CTV_77',
  'CTV!_70',
  'CTV_Prostate_SV',
  'CTV 0-63 bekken glandel sin met',
  'CTVn',
  'CTVn_66',
  'PTV',
  'PTV 0-77',
  'PTV 0-70',
  'PTV 0-56',
  'PTV 0-63',
  'PTV 0-77 union',
  'PTV_66+74',
  'PTV_74',
  'PTV_77',
  'PTVn',
  'PTVn_66',
  'PTVnOpt',
  'PTV77-95%dose',
  'PTV!_70',
  'PTV!_56',
  'PTV!_66',
  'PTVc!_56',
  'PTV_56+66+74',
  'ptv56opt',
  'PTV 56 opt',
  'ptv70opt',
  'ptv77opt',
  'PTV56opt',
  'PTV70opt',
  'PTV77opt',
  'PTV_70+77',
  'PTV_56+70+77',
  'PTV56-69%dose',
  'PTV_Prostate_SV',
  'PTV70-dorsrect',
  'PTV ves sim 0-77',
  'PTV_SeminalVes',
  'SeminalVes10',
  'SeminalVes20',
  'zptv56opt',
  'zPTV_56',
  'zPTV_0-77',
  'zOpt_56',
  'zWall56',
  'zPTV56_Wall',
  'zPTV_56_Wall',
  'zPTV_56_wall',
  'zPTV!_56_Wall',
  'zPTV_77_Wall',
  'zPTV_70+77_Wall',
  'zPTV70+77_Wall',
  'zWall_PTV56',
  'zWall_temp',
  'Walltemp',
  'Wall_temp',
  'Wall_PTVp',
  'Wall_PTV77',
  'zBladder',
  'zAnalCanal',
  'zRectum',
  'zRectum (1)',
  'zRectum_Posterior',
  'zBowelBag',
  'zSpc_Bowel',
  'AnalCanal1',
  'Bolus',
  'Bolus (1)',
  'Bowel space - PTV',
  'BowelBag_XVI',
  'Rectum - PTV',
  'Bladder_XVI',
  'Bladder-XVI',
  'Bladder - PTV',
  'Bladder MBS',
  'Dorso_Rektum',
  'Dorso_Rectum',
  'External XVI',
  'Wall PTV',
  'Wall PTV_77',
  'wall_temp',
  'wall temp',
  'hjelp',
  'hjelprektum',
  'hjelp56',
  'hjelp77',
  'DorsRectum',
  'Dorsorect',
  'rectPTV',
  'red',
  'Seed iso',
  'Seed 1',
  'Seed 2',
  'Seed 3',
  'Seed 4',
  'Marker1',
  'Marker2',
  'Marker3',
  'Marker4',
  'opt',
  'opt2',
  'opt 26-35',
  'opt 56',
  'opt 56.2',
  'opt_56',
  'opt56',
  'opt56.',
  'opt561',
  'Opt56nyplan',
  'opt 60 Gy',
  'opt70',
  'opt_70',
  'opt 70',
  'opt-70',
  'Opt70nyplan',
  'opt73',
  'opt77',
  'opt_77',
  'opt 77',
  'opt77_2',
  'opt 77-2',
  'opt 77-3',
  'opt53',
  'opt53,2',
  'optctv',
  'optn',
  'optmax',
  'optPTV56',
  'opt_ptv56',
  'optPTV77',
  'Opt_ptv70',
  'opt_ptv70',
  'opt_PTV77',
  '53',
  '53,2',
  '56',
  '56 - 95',
  '66',
  '66,5',
  '69',
  '69.2',
  '70',
  '73',
  '77',
  '78',
  '79',
  '86',
  '87',
  '95',
  '95_1',
  '95.2',
  '95_2',
  '95_56',
  '95-56',
  '95_70',
  '95/70',
  '95_77',
  '95/77',
  '105',
  '1052',
  '105-70',
  'Ves sem sin innvekst 77GY',
]

for name in delete:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass
  

