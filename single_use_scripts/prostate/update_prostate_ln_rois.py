# Processes ROIs to be used in the Prostate+LN Deep Learning project.
# This script is designed to be run after a patient has been imported in the research environment,
# and an initial ROI script has been executed.
# This script does the following updates:
# -Creates "Vessels_with_margin" ROI, with 7mm margin to vessels.
# -Sets subtraction margin of 0 mm for Bladder and BowelBag ROIs
# -Creates LevatorAniMuscle ROI

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

  
# Create ROIs:

# LevatorAniMuscle:
create_roi(name = 'LevatorAniMuscle', color = 'Darkcyan', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['LevatorAniMuscle'].OrganData.OrganType = "OrganAtRisk"

# Bladder Algebra: Subtract Prostate:
bladder = create_roi(name = 'Bladder', color = 'Yellow', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Bladder'].OrganData.OrganType = "OrganAtRisk"
bladder.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['Bladder_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Prostate'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
bladder.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

# BowelBag Algebra (subtract Bladder, veins, etc)
bowel_bag = create_roi(name = 'BowelBag', color = 'SandyBrown', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['BowelBag'].OrganData.OrganType = "OrganAtRisk"
bowel_bag.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['BowelBag_Draft'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['Bladder_Draft', 'Prostate', 'SeminalVes', 'LN_Iliac', 'Rectum', 'PelvicGirdle_L', 'PelvicGirdle_R', 'Coccyx', 'Sacrum', 'L2', 'L3', 'L4', 'L5', 'IliopsoasMuscle_L', 'IliopsoasMuscle_R', 'A_DescendingAorta', 'A_CommonIliac_L', 'A_CommonIliac_R', 'A_ExternalIliac_L', 'A_ExternalIliac_R', 'A_InternalIliac_L', 'A_InternalIliac_R', 'V_InferiorVenaCava', 'V_CommonIliac_L', 'V_CommonIliac_R', 'V_ExternalIliac_L', 'V_ExternalIliac_R', 'V_InternalIliac_L', 'V_InternalIliac_R', 'Ureter_L', 'Ureter_R', 'Ureter_L', 'DuctusDeferens_L', 'DuctusDeferens_R', 'Kidney_L', 'Kidney_R', 'Liver'], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.0, 'Inferior': 0.0, 'Anterior': 0.0, 'Posterior': 0.0, 'Right': 0.0, 'Left': 0.0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
bowel_bag.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

# Vessel Algebra LN help structure (add 7 mm margin, subtract bone, muscles)
vessels_help = create_roi(name = 'Vessels_with_margin', color = 'Yellow', type = 'Organ', alternatives=[])
pm.RegionsOfInterest['Vessels_with_margin'].OrganData.OrganType = "Target"
vessels_help.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ["A_Pelvic", "V_Pelvic"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0.7, 'Inferior': 0.7, 'Anterior': 0.7, 'Posterior': 0.7, 'Right': 0.7, 'Left': 0.7 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ["FemurHeadNeck_L", "FemurHeadNeck_R", "Rectum", "L2", "L3", "L4", "L5", "PelvicGirdle_L", "PelvicGirdle_R", "Sacrum", "Coccyx", "IliopsoasMuscle_L", "IliopsoasMuscle_R"], 'MarginSettings': { 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })
vessels_help.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
