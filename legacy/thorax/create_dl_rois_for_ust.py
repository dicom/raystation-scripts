# Creates DL ROIs for the "Chestwall & Detailed Heart" UST.

from connect import *

# Load the patient case and examination:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# The patient model:  
pm = case.PatientModel

# Run deep learning segmentation:
examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
  'RSL DLS CT (v3.0.0.37)': {
    # Chestwall and bones:
    "UST_CW_2cm_L": "Chestwall_L",
    "UST_CW_2cm_R": "Chestwall_R",
    "UST_CW_Anatomical_L": "Chestwall_anatomical_L",
    "UST_CW_Anatomical_R": "Chestwall_anatomical_R",
    "UST_Cartlg_Costal_L": "CostalCartilage_L",
    "UST_Cartlg_Costal_R": "CostalCartilage_R",
    "UST_Clavicle_L": "Clavicle_L",
    "UST_Clavicle_R": "Clavicle_R",
    "UST_HumeralHead_L": "HumeralHead_L",
    "UST_HumeralHead_R": "HumeralHead_R",
    "UST_Humerus_L": "HumeralHeadNeck_L",
    "UST_Humerus_R": "HumeralHeadNeck_R",
    "UST_Scapula_L": "Scapula_L",
    "UST_Scapula_R": "Scapula_R",
    "UST_C1": "C1",
    "UST_C2": "C2",
    "UST_C3": "C3",
    "UST_C4": "C4",
    "UST_C5": "C5",
    "UST_C6": "C6",
    "UST_C7": "C7",
    "UST_T1": "T1",
    "UST_T2": "T2",
    "UST_T3": "T3",
    "UST_T4": "T4",
    "UST_T5": "T5",
    "UST_T6": "T6",
    "UST_T7": "T7",
    "UST_T8": "T8",
    "UST_T9": "T9",
    "UST_T10": "T10",
    "UST_T11": "T11",
    "UST_T12": "T12",
    "UST_L1": "L1",
    "UST_L2": "L2",
    "UST_L3": "L3",
    "UST_L4": "L4",
    "UST_L5": "L5",
    "UST_Rib1_L": "Rib1_L",
    "UST_Rib2_L": "Rib2_L",
    "UST_Rib3_L": "Rib3_L",
    "UST_Rib4_L": "Rib4_L",
    "UST_Rib5_L": "Rib5_L",
    "UST_Rib6_L": "Rib6_L",
    "UST_Rib7_L": "Rib7_L",
    "UST_Rib8_L": "Rib8_L",
    "UST_Rib9_L": "Rib9_L",
    "UST_Rib10_L": "Rib10_L",
    "UST_Rib11_L": "Rib11_L",
    "UST_Rib12_L": "Rib12_L",
    "UST_Rib1_R": "Rib1_R",
    "UST_Rib2_R": "Rib2_R",
    "UST_Rib3_R": "Rib3_R",
    "UST_Rib4_R": "Rib4_R",
    "UST_Rib5_R": "Rib5_R",
    "UST_Rib6_R": "Rib6_R",
    "UST_Rib7_R": "Rib7_R",
    "UST_Rib8_R": "Rib8_R",
    "UST_Rib9_R": "Rib9_R",
    "UST_Rib10_R": "Rib10_R",
    "UST_Rib11_R": "Rib11_R",
    "UST_Rib12_R": "Rib12_R",
    "UST_Ribs_L": "Ribs_L",
    "UST_Ribs_R": "Ribs_R",
    # Detailed Heart:
    "UST_A_Aorta_Root": "Aortic root",
    "UST_A_Aorta_Asc_Prox": "Ascending aorta",
    "UST_A_Pulmonary": "Pulmonary artery",
    "UST_Atrium_L": "Left atrium",
    "UST_Atrium_R": "Right atrium",
    "UST_V_Pulmonary": "Pulmonary veins",
    "UST_V_Venacava_S_Prox": "Superior vena cava",
    "UST_Ventricle_L": "Left ventricle",
    "UST_Ventricle_R": "Right ventricle",
  }
})

# Set colors:
pm.RegionsOfInterest["UST_Cartlg_Costal_L"].Color = "Salmon"
pm.RegionsOfInterest["UST_Cartlg_Costal_R"].Color = "Salmon"
pm.RegionsOfInterest["UST_CW_2cm_L"].Color = "LightGreen"
pm.RegionsOfInterest["UST_CW_2cm_R"].Color = "LightGreen"
pm.RegionsOfInterest["UST_CW_Anatomical_L"].Color = "LightGreen"
pm.RegionsOfInterest["UST_CW_Anatomical_R"].Color = "LightGreen"
pm.RegionsOfInterest["UST_Clavicle_L"].Color = "Magenta"
pm.RegionsOfInterest["UST_Clavicle_R"].Color = "Magenta"
pm.RegionsOfInterest["UST_HumeralHead_L"].Color = "Olive"
pm.RegionsOfInterest["UST_HumeralHead_R"].Color = "Olive"
pm.RegionsOfInterest["UST_Humerus_L"].Color = "Teal"
pm.RegionsOfInterest["UST_Humerus_R"].Color = "Teal"
pm.RegionsOfInterest["UST_Scapula_L"].Color = "Goldenrod"
pm.RegionsOfInterest["UST_Scapula_R"].Color = "Goldenrod"
pm.RegionsOfInterest["UST_C1"].Color = "Blue"
pm.RegionsOfInterest["UST_C2"].Color = "Purple"
pm.RegionsOfInterest["UST_C3"].Color = "Blue"
pm.RegionsOfInterest["UST_C4"].Color = "Purple"
pm.RegionsOfInterest["UST_C5"].Color = "Blue"
pm.RegionsOfInterest["UST_C6"].Color = "Purple"
pm.RegionsOfInterest["UST_C7"].Color = "Blue"
pm.RegionsOfInterest["UST_T1"].Color = "Maroon"
pm.RegionsOfInterest["UST_T2"].Color = "OrangeRed"
pm.RegionsOfInterest["UST_T3"].Color = "Maroon"
pm.RegionsOfInterest["UST_T4"].Color = "OrangeRed"
pm.RegionsOfInterest["UST_T5"].Color = "Maroon"
pm.RegionsOfInterest["UST_T6"].Color = "OrangeRed"
pm.RegionsOfInterest["UST_T7"].Color = "Maroon"
pm.RegionsOfInterest["UST_T8"].Color = "OrangeRed"
pm.RegionsOfInterest["UST_T9"].Color = "Maroon"
pm.RegionsOfInterest["UST_T10"].Color = "OrangeRed"
pm.RegionsOfInterest["UST_T11"].Color = "Maroon"
pm.RegionsOfInterest["UST_T12"].Color = "OrangeRed"
pm.RegionsOfInterest["UST_L1"].Color = "Blue"
pm.RegionsOfInterest["UST_L2"].Color = "Purple"
pm.RegionsOfInterest["UST_L3"].Color = "Blue"
pm.RegionsOfInterest["UST_L4"].Color = "Purple"
pm.RegionsOfInterest["UST_L5"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib1_L"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib2_L"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib3_L"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib4_L"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib5_L"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib6_L"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib7_L"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib8_L"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib9_L"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib10_L"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib11_L"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib12_L"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib1_R"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib2_R"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib3_R"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib4_R"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib5_R"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib6_R"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib7_R"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib8_R"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib9_R"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib10_R"].Color = "Purple"
pm.RegionsOfInterest["UST_Rib11_R"].Color = "Blue"
pm.RegionsOfInterest["UST_Rib12_R"].Color = "Purple"
pm.RegionsOfInterest["UST_Ribs_L"].Color = "PaleVioletRed"
pm.RegionsOfInterest["UST_Ribs_R"].Color = "PaleVioletRed"
