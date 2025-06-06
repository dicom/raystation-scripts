# Script for peforming various tasks on each patient in this project.


from connect import get_current


# List of patient names :
patient_names = [
  "AL_HBryst_001",
  "AL_HBryst_002",
  "AL_HBryst_003",
  "AL_HBryst_004",
  "AL_HBryst_005",
  "AL_HBryst_006",
  "AL_HBryst_007",
  "AL_HBryst_008",
  "AL_HBryst_009",
  "AL_HBryst_010",
  "AL_HBryst_011",
  "AL_HBryst_012",
  "AL_HBryst_013",
  "AL_HBryst_014",
  "AL_HBryst_015",
  "AL_HBryst_016",
  "AL_HBryst_017",
  "AL_HBryst_018",
  "AL_HBryst_019",
  "AL_HBryst_020",
  "AL_HBryst_021",
  "AL_HBryst_022",
  "AL_HBryst_023",
  "AL_HBryst_024",
  "AL_HBryst_025",
  "AL_HBryst_026",
  "AL_HBryst_027",
  "AL_HBryst_028",
  "AL_HBryst_029",
  "AL_HBryst_030",
  "AL_COBRA_032",
  "AL_COBRA_033",
  "AL_COBRA_034",
  "AL_COBRA_035",
  "AL_COBRA_036",
  "AL_COBRA_037",
  "AL_COBRA_038",
  "AL_COBRA_039",
  "AL_COBRA_040",
  "AL_COBRA_041",
  "AL_COBRA_042",
  "AL_COBRA_044",
  "AL_COBRA_045",
  "AL_COBRA_046",
  "AL_COBRA_047",
  "AL_COBRA_048",
  "AL_COBRA_049",
  "AL_COBRA_050",
  "AL_COBRA_051",
  "AL_COBRA_052",
  "AL_COBRA_054",
  "AL_COBRA_055",
  "AL_COBRA_056",
  "AL_COBRA_057",
  "AL_COBRA_058",
  "AL_COBRA_059",
  "AL_COBRA_060",
  "AL_COBRA_061",
  "AL_COBRA_062",
  "AL_COBRA_063",
  "AL_COBRA_064",
  "AL_COBRA_065",
  "AL_COBRA_066",
  "AL_COBRA_067",
  "AL_COBRA_068",
  "AL_COBRA_069",
  "AL_COBRA_070",
  "AL_COBRA_071",
  "AL_COBRA_072",
  "AL_COBRA_073",
  "AL_COBRA_075",
  "AL_COBRA_077",
  "AL_COBRA_078",
  "AL_COBRA_079",
  "AL_COBRA_080",
  "AL_COBRA_081",
  "AL_COBRA_082",
  "AL_COBRA_084",
  "AL_COBRA_085",
  "AL_COBRA_086",
  "AL_COBRA_087",
  "AL_COBRA_088",
  "AL_COBRA_089",
  "AL_COBRA_090",
  "AL_COBRA_091",
  "AL_COBRA_092",
  "AL_COBRA_093",
  "AL_COBRA_094",
  "AL_COBRA_095",
  "AL_COBRA_096",
  "AL_COBRA_097",
  "AL_COBRA_098",
  "AL_COBRA_100",
  "AL_COBRA_101",
  "AL_COBRA_102",
  "AL_COBRA_103",
  "AL_COBRA_105",
  "AL_COBRA_106",
  "AL_COBRA_108",
  "AL_COBRA_110"
]


# Patient database:
patient_db = get_current("PatientDB")


# Iterate patient ids and export RSBAK files:
for name in patient_names:
  # Load patient from database:
  patient_infos = patient_db.QueryPatientInfo(Filter={"LastName": name})
  # Open patient:
  patient = patient_db.LoadPatient(PatientInfo=patient_infos[0])
  # Update all derived ROIs:
  for case in patient.Cases:
    for struct in case.PatientModel.StructureSets:
      examination = struct.OnExamination
      # Search for ROIs which are derived but not updated:
      for roi in struct.RoiGeometries:
        if roi.PrimaryShape:
          # Check for dirty shape:
          if roi.PrimaryShape.DerivedRoiStatus:
            if roi.PrimaryShape.DerivedRoiStatus.IsShapeDirty == True:
              # For any dirty ROI, update it:
              roi.OfRoi.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
        else:
          # Check for empty, derived ROI:
          if roi.OfRoi.DerivedRoiExpression:
            # Construct the ROI by using the update feature:
            roi.OfRoi.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
  # Change some ROI names:
  name_pairs = [
    ['InterCostalMuscles_R_Draft', 'InterCostalSpace_R_Draft'],
    ['InterCostalMuscles_L_Draft', 'InterCostalSpace_L_Draft'],
    ['InterCostalMuscles_R', 'InterCostalSpace_R'],
    ['InterCostalMuscles_L', 'InterCostalSpace_L']
  ]
  for np in name_pairs:
    for case in patient.Cases:
      for roi in case.PatientModel.RegionsOfInterest:
        if roi.Name == np[0]:
          # Change old name to the new version:
          roi.Name = np[1]
  # Save changes:
  patient.Save()
