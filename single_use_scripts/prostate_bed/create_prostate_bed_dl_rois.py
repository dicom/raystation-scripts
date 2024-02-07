# Processes ROIs to be used in the Prostate Bed Deep Learning project.
# This script is designed to be run after a patient has been imported in the research environment.
# It does the following:
# -Creates new ROIs which are not originally present
# -Renames ROIs which are present, but have a different name than the one decided for the project
# -Deletes ROIs which are not supposed to be included in the project

# RayStation 12A - Python 3.6

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


# Delete ROIs which we rather want to have DL segmented:
delete_originals = [
  'Bowel space', 'BowelBag', 'Spc_Bowel', 'BowelBag_draft', 'BowelBag_Draft',
  'Rectum',
  'AnalCanal',
  'CaudaEquina', 'SpinalCord', 'Spinalkanal', 'SpinalCanal', 'Spinal Cord', 'Cauda Equina',
  'FemurHeadNeck_L', 'Femur_Head_L', 'FemoralHead_L', 'Femoral head left',
  'FemurHeadNeck_R', 'Femur_Head_R', 'FemoralHead_R', 'Femoral head right',
  'LN_Iliac', 'Pelvic nodes',
]
for name in delete_originals:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass


# Create ROIs:
# External:
external = create_roi(name = 'External', color = '255, 173, 91', type = 'External', alternatives=['Body'])

# Target volumes:
# Prostate bed  and nodes:
create_roi(name = 'ProstateBed', color = 'Salmon', type = 'Ctv', alternatives=['SurgicalBed', 'Prostate bed', 'CTVsb', 'CTV'])
create_roi(name = 'LN_Iliac', color = 'Magenta', type = 'Ctv', alternatives=['Pelvic nodes'])

# Organs:
# Intestinal:
create_roi(name = 'Liver', color = 'Khaki', type = 'Organ', alternatives=[])
create_roi(name = 'BowelBag_Draft', color = 'SandyBrown', type = 'Organ', alternatives=['Bowel space', 'BowelBag', 'Spc_Bowel', 'BowelBag_draft'])
create_roi(name = 'Rectum', color = 'SaddleBrown', type = 'Organ', alternatives=[])
create_roi(name = 'AnalCanal', color = 'Maroon', type = 'Organ', alternatives=[])
# Urological:
create_roi(name = 'Kidney_L', color = 'LightSalmon', type = 'Organ', alternatives=[])
create_roi(name = 'Kidney_R', color = 'LightSalmon', type = 'Organ', alternatives=[])
create_roi(name = 'Ureter_L', color = 'Orange', type = 'Organ', alternatives=[])
create_roi(name = 'Ureter_R', color = 'Orange', type = 'Organ', alternatives=[])
bladder = create_roi(name = 'Bladder', color = 'Yellow', type = 'Organ', alternatives=[])
# Genital:
create_roi(name = 'PenileBulb', color = 'PaleVioletRed', type = 'Organ', alternatives=['Penile bulbi'])
create_roi(name = 'Testis_L', color = 'Mediumvioletred', type = 'Organ', alternatives=[])
create_roi(name = 'Testis_R', color = 'Mediumvioletred', type = 'Organ', alternatives=[])
create_roi(name = 'DuctusDeferens_L', color = 'Lightpink', type = 'Organ', alternatives=[])
create_roi(name = 'DuctusDeferens_R', color = 'Lightpink', type = 'Organ', alternatives=[])
# Nerves:
create_roi(name = 'CaudaEquina', color = 'Blue', type = 'Organ', alternatives=['SpinalCanal', 'SpinalCord', 'Spinalkanal', 'Spinal Cord', 'Cauda Equina'])
create_roi(name = 'LumbarNerveRoots_L', color = 'RoyalBlue', type = 'Organ', alternatives=[])
create_roi(name = 'LumbarNerveRoots_R', color = 'RoyalBlue', type = 'Organ', alternatives=[])
create_roi(name = 'SacralNerveRoots_L', color = 'RoyalBlue', type = 'Organ', alternatives=[])
create_roi(name = 'SacralNerveRoots_R', color = 'RoyalBlue', type = 'Organ', alternatives=[])
# Vessels:
# Arteries:
create_roi(name = 'A_DescendingAorta', color = 'Maroon', type = 'Organ', alternatives=[])
create_roi(name = 'A_CommonIliac_L', color = 'Red', type = 'Organ', alternatives=[])
create_roi(name = 'A_CommonIliac_R', color = 'Red', type = 'Organ', alternatives=[])
create_roi(name = 'A_InternalIliac_L', color = 'Tomato', type = 'Organ', alternatives=[])
create_roi(name = 'A_InternalIliac_R', color = 'Tomato', type = 'Organ', alternatives=[])
create_roi(name = 'A_ExternalIliac_L', color = 'OrangeRed', type = 'Organ', alternatives=[])
create_roi(name = 'A_ExternalIliac_R', color = 'OrangeRed', type = 'Organ', alternatives=[])
# Artery Algebra (union):
a_pelvic = create_roi(name = 'A_Pelvic', color = 'Red', type = 'Organ', alternatives=[])
a_pelvic.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['A_DescendingAorta'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['A_CommonIliac_L', 'A_CommonIliac_R', 'A_ExternalIliac_L', 'A_ExternalIliac_R', 'A_InternalIliac_L', 'A_InternalIliac_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
a_pelvic.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Veins:
create_roi(name = 'V_InferiorVenaCava', color = 'Navy', type = 'Organ', alternatives=[])
create_roi(name = 'V_CommonIliac_L', color = 'Blue', type = 'Organ', alternatives=[])
create_roi(name = 'V_CommonIliac_R', color = 'Blue', type = 'Organ', alternatives=[])
create_roi(name = 'V_InternalIliac_L', color = 'SlateBlue', type = 'Organ', alternatives=[])
create_roi(name = 'V_InternalIliac_R', color = 'SlateBlue', type = 'Organ', alternatives=[])
create_roi(name = 'V_ExternalIliac_L', color = 'MediumSlateBlue', type = 'Organ', alternatives=[])
create_roi(name = 'V_ExternalIliac_R', color = 'MediumSlateBlue', type = 'Organ', alternatives=[])
# Vein Algebra (union):
v_pelvic = create_roi(name = 'V_Pelvic', color = 'Blue', type = 'Organ', alternatives=[])
v_pelvic.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['V_InferiorVenaCava'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['V_CommonIliac_L', 'V_CommonIliac_R', 'V_ExternalIliac_L', 'V_ExternalIliac_R', 'V_InternalIliac_L', 'V_InternalIliac_R'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Union", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
v_pelvic.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Muscles:
create_roi(name = 'IliopsoasMuscle_L', color = 'Darkcyan', type = 'Organ', alternatives=[])
create_roi(name = 'IliopsoasMuscle_R', color = 'Darkcyan', type = 'Organ', alternatives=[])
# Bone:
create_roi(name = 'L2', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'L3', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'L4', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'L5', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'PelvicGirdle_L', color = bone_color3, type = 'Organ', alternatives=[])
create_roi(name = 'PelvicGirdle_R', color = bone_color3, type = 'Organ', alternatives=[])
create_roi(name = 'Sacrum', color = bone_color1, type = 'Organ', alternatives=[])
create_roi(name = 'Coccyx', color = bone_color2, type = 'Organ', alternatives=[])
create_roi(name = 'FemurHeadNeck_L', color = bone_color1, type = 'Organ', alternatives=['Femur_Head_L', 'FemoralHead_L', 'Femoral head left'])
create_roi(name = 'FemurHeadNeck_R', color = bone_color1, type = 'Organ', alternatives=['Femur_Head_R', 'FemoralHead_R', 'Femoral head right'])

# Apply DL segmentation:
examination.RunOarSegmentation(ModelName="Alesund MalePelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=['PenileBulb', "CaudaEquina", "BowelBag_Draft", "Rectum", "AnalCanal", "Testis_L", "Testis_R", "L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "FemurHeadNeck_L", "FemurHeadNeck_R", "LN_Iliac", "Kidney_L", "Kidney_R", "Liver", "IliopsoasMuscle_L", "IliopsoasMuscle_R", "L2", "L3", "L4", "A_DescendingAorta", "A_CommonIliac_L", "A_CommonIliac_R", "A_ExternalIliac_L", "A_ExternalIliac_R", "A_InternalIliac_L", "A_InternalIliac_R", "V_InferiorVenaCava", "V_CommonIliac_L", "V_CommonIliac_R", "V_ExternalIliac_L", "V_ExternalIliac_R", "V_InternalIliac_L", "V_InternalIliac_R", 'LumbarNerveRoots_L', 'LumbarNerveRoots_R', 'SacralNerveRoots_L', 'SacralNerveRoots_R', 'DuctusDeferens_L', 'DuctusDeferens_R', 'Ureter_L', 'Ureter_R'])

# ROI Algebra:
# BowelBag Algebra (subtract Bladder, veins, etc)
bowel_bag = create_roi(name = 'BowelBag', color = 'SandyBrown', type = 'Organ', alternatives=[])
bowel_bag.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['BowelBag_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Bladder', 'LN_Iliac', 'PelvicGirdle_L', 'PelvicGirdle_R', 'Sacrum', 'L2', 'L3', 'L4', 'L5', 'IliopsoasMuscle_L', 'IliopsoasMuscle_R', 'A_DescendingAorta', 'A_CommonIliac_L', 'A_CommonIliac_R', 'A_ExternalIliac_L', 'A_ExternalIliac_R', 'A_InternalIliac_L', 'A_InternalIliac_R', 'V_InferiorVenaCava', 'V_CommonIliac_L', 'V_CommonIliac_R', 'V_ExternalIliac_L', 'V_ExternalIliac_R', 'V_InternalIliac_L', 'V_InternalIliac_R', 'Ureter_L', 'Ureter_R', 'Ureter_L', 'DuctusDeferens_L', 'DuctusDeferens_R', 'Kidney_L', 'Kidney_R', 'Liver'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
bowel_bag.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
# Vessel Algebra LN help structure (add 7 mm margin, subtract bone, muscles)
vessels_help = create_roi(name = 'Vessels_with_margin', color = 'Yellow', type = 'Organ', alternatives=[])
vessels_help.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["A_Pelvic", "V_Pelvic"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.7, 'Inferior': 0.7, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["FemurHeadNeck_L", "FemurHeadNeck_R", "Rectum", "L2", "L3", "L4", "L5", "PelvicGirdle_L", "PelvicGirdle_R", "Sacrum", "IliopsoasMuscle_L", "IliopsoasMuscle_R"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
vessels_help.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")


# For cases having multiple CT examinations, run the DL segmentation ROIs on the other CT examinations as well:
for e in case.Examinations:
  # No need to do segmentation again for the default examination:
  if e.Name != examination.Name:
    # Only do segmentation for CT series, not MR or CBCT series:
    if e.Name[0:2] == 'CT':
      e.RunOarSegmentation(ModelName="Alesund MalePelvic CT", ExaminationsAndRegistrations={ e.Name: None }, RoisToInclude=['PenileBulb', "CaudaEquina", "BowelBag_Draft", "Rectum", "AnalCanal", "Testis_L", "Testis_R", "L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "FemurHeadNeck_L", "FemurHeadNeck_R", "LN_Iliac", "Kidney_L", "Kidney_R", "Liver", "IliopsoasMuscle_L", "IliopsoasMuscle_R", "L2", "L3", "L4", "A_DescendingAorta", "A_CommonIliac_L", "A_CommonIliac_R", "A_ExternalIliac_L", "A_ExternalIliac_R", "A_InternalIliac_L", "A_InternalIliac_R", "V_InferiorVenaCava", "V_CommonIliac_L", "V_CommonIliac_R", "V_ExternalIliac_L", "V_ExternalIliac_R", "V_InternalIliac_L", "V_InternalIliac_R", 'LumbarNerveRoots_L', 'LumbarNerveRoots_R', 'SacralNerveRoots_L', 'SacralNerveRoots_R', 'DuctusDeferens_L', 'DuctusDeferens_R', 'Ureter_L', 'Ureter_R'])


# If we delete the prescription volume, RayStation will crash. To avoid this, set the prescription
# of any existing plans to ProstateBed, before proceeding with deleting ROIs:
for plan in case.TreatmentPlans:
  for bs in plan.BeamSets:
    if bs.Prescription.PrimaryPrescriptionDoseReference.OnStructure.Name != 'ProstateBed':
      bs.AddRoiPrescriptionDoseReference(RoiName="ProstateBed", DoseVolume=0, PrescriptionType="MedianDose", DoseValue=7000, RelativePrescriptionLevel=1)


# Set organ types:
pm.RegionsOfInterest['ProstateBed'].OrganData.OrganType = "Target"
pm.RegionsOfInterest['LN_Iliac'].OrganData.OrganType = "Target"
pm.RegionsOfInterest['Liver'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['BowelBag_Draft'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Rectum'].OrganData.OrganType = "OrganAtRisk"
pm.RegionsOfInterest['AnalCanal'].OrganData.OrganType = "OrganAtRisk"
pm.RegionsOfInterest['Kidney_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Kidney_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Ureter_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Ureter_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['PenileBulb'].OrganData.OrganType = "OrganAtRisk"
pm.RegionsOfInterest['Testis_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Testis_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['DuctusDeferens_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['DuctusDeferens_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['CaudaEquina'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['LumbarNerveRoots_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['LumbarNerveRoots_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['SacralNerveRoots_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['SacralNerveRoots_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_DescendingAorta'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_CommonIliac_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_CommonIliac_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_InternalIliac_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_InternalIliac_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_ExternalIliac_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_ExternalIliac_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['A_Pelvic'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_InferiorVenaCava'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_CommonIliac_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_CommonIliac_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_InternalIliac_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_InternalIliac_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_ExternalIliac_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_ExternalIliac_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['V_Pelvic'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['IliopsoasMuscle_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['IliopsoasMuscle_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['L2'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['L3'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['L4'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['L5'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['PelvicGirdle_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['PelvicGirdle_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Sacrum'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Coccyx'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['FemurHeadNeck_L'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['FemurHeadNeck_R'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['BowelBag'].OrganData.OrganType = "Other"
pm.RegionsOfInterest['Vessels_with_margin'].OrganData.OrganType = "Target"


# Delete ROIs:
# Delete known ROIs which we know we do not want:
delete = [
  'CTV',
  'CTVsb (1)',
  'CTV 0-70',
  'CTV 0-56',
  'CTV_56',
  'CTV!_56',
  'CTV!56opt',
  'CTV!_66',
  'CTV_66',
  'CTV_74',
  'CTV!_70',
  'CTV_70',
  'CTVn + CTV_70',
  'CTVn',
  'CTVn_66',
  'CTV nodes',
  'CTV nodes-PTV70',
  'CTVm',
  'CTV56marg',
  'PTV',
  'PTV 0-70',
  'PTV0-70-Dorsorectum',
  'PTV_70',
  'PTVn + PTV_70',
  'ptv56',
  'PTV 0-56',
  'PTV_56+70',
  'PTV_56+66+70',
  'PTVsb',
  'PTVn',
  'PTVm',
  'PTV nodes',
  'PTVn_66',
  'PTVnOpt',
  'PTV nodes -PTV70',
  'PTV!_70',
  'PTV!_56',
  'PTV!_66',
  'PTV_66',
  'PTVc!_56',
  'ptv56opt',
  'PTVopt',
  'PTV 56 opt',
  'PTV 56 - Ptv 70',
  'ptv70opt',
  'PTV56opt',
  'PTV70opt',
  'PTV_70 opt',
  'PTV!_70_opt',
  'ptv70-95',
  'ptv70-95 (1)',
  'PTV70-rectum',
  'PTV-Rectum',
  'PTV-rectum',
  'ptv-95-70',
  'ptv-95-70 (1)',
  'ptv-95-56',
  'PTV56-69%dose',
  'PTV_Prostate_SV',
  'PTV - opt rectum',
  'PTV70-dorsrect',
  'PTV 70-dorsrect',
  'ptv-dors rectum',
  'PTV-zRectum_P',
  'PTV_SeminalVes',
  'ptv-95',
  'PTV 95',
  'Ptv_95plan4',
  'PTV56marg',
  'PTV_Wall',
  'PTV wall',
  'ptv wall',
  'PTV wall 56-70',
  'PTV wall 70',
  'Pelvic nodes & PTV70-intersect',
  'SeminalVes10',
  'SeminalVes20',
  'zptv56opt',
  'zPTV_56',
  'zOpt_56',
  'zWall56',
  'zPTV_wall',
  'z_PTV_Wall',
  'zPTV56_Wall',
  'zPTV_56_Wall',
  'zPTV_56_wall',
  'zPTV!_56_Wall',
  'zPTV_56_Temp',
  'zPTV56_wall',
  'zPTV_66_wall',
  'zPTV_66_Wall',
  'zWall_PTV_56',
  'zWall_PTV56',
  'zPTVsb_Wall',
  'zPTV_70_Wall',
  'zPTV_70_wall',
  'zPTV_70',
  'zPTV_70 opt!',
  'zPTV70-Rectum',
  'zWall_PTV_70',
  'zWall_temp',
  'wall',
  'Walltemp',
  'Wall_temp',
  'Wall_PTVp',
  'Wall 56-70',
  'Wall56',
  'Wall70',
  'Wall_PTV_56',
  'Wall_PTV_70',
  'Wall_PTV70',
  'Xvi bowel',
  'zPTV_Wall',
  'zWall',
  'zBladder',
  'zBladderXVI',
  'zBladder_XVI',
  'zBowel',
  'zAnalCanal',
  'zRectum',
  'zRectum (1)',
  'zRectum_Posterior',
  'zRectum_P',
  'zBowelBag',
  'zSpc_Bowel',
  'zAnal',
  'zopt',
  'z95',
  'z105',
  'AnalCanal1',
  'Bolus',
  'Bolus (1)',
  'Bowel space - PTV',
  'Bowel - PTV',
  'BowelBag_XVI',
  'Bowelbag XVi',
  'Rectum - PTV',
  'Bladder_minVol',
  'Bladder minvol.',
  'Bladder_minvolum',
  'Bladder_overlap',
  'Bladder_XVI',
  'Bladder-XVI',
  'Bladder_min',
  'Bladder_minimum',
  'Bladder - PTV',
  'Bladder MBS',
  'Bladder-PTV',
  'Bladder XVI',
  'Box',
  'Contrast',
  'Kontrast',
  'Dorso_Rektum',
  'Dorso_Rectum',
  'Dorsorectum',
  'External XVI',
  'External_xvi',
  'maks105',
  'maks105_2',
  'max',
  'max 105',
  'matchbox',
  'Min_bladderVol',
  'min_blære',
  'NV',
  'ny opt',
  'ny105',
  'Wall PTV',
  'wall_temp',
  'wall temp',
  'DorsRectum',
  'Dorsorect',
  'rectPTV',
  'Rectum dors',
  'Rectum part',
  'Rectum copy',
  'Rectum XVI',
  'Rectum_XVI',
  'Rectum_MaxVol',
  'RectumPTV',
  'red',
  'Residiv',
  'TestBB',
  'test',
  'Spinalcanal',
  'opt',
  'opt1',
  'opt2',
  'opt 56',
  'opt 56.2',
  'opt_56',
  'opt56',
  'opt56.',
  'opt561',
  'opt70',
  'opt_70',
  'opt 70',
  'opt-70',
  'opt53',
  'opt53,2',
  'optctv',
  'optn',
  'optmax',
  'opt PTV',
  'optPTV',
  'optPTV56',
  'opt_ptv56',
  'Opt_ptv70',
  'opt_ptv70',
  'opt_PTV70',
  'Opt PTV',
  'optptv',
  'Opt PTV 70',
  'Optimering ptv',
  'Opt rectum',
  'Opt rectum 2',
  'opt2 105',
  'opt2 PTV 70',
  '53',
  '53,2',
  '56',
  '56 - 95',
  '66',
  '66,5',
  '69',
  '69.2',
  '70',
  '70opt',
  '70 opt1',
  '73',
  '73,5',
  '76',
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
  '95-70',
  '105',
  '105_1',
  '105,2',
  '1052',
  '105_2',
  '105 3',
  '105-56',
  '105-70',
  '1055',
  '105_maks',
  '106',
]

for name in delete:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass
  

