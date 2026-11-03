# Script for exporting patients to rsbak files.
# Exports the 50 patients used in a brain project.


from connect import get_current


# List of patient ids of patients to export:
names = [
  "AL_BrainSRT_001",
  "AL_BrainSRT_002",
  "AL_BrainSRT_003",
  "AL_BrainSRT_004",
  "AL_BrainSRT_005",
  "AL_BrainSRT_006",
  "AL_BrainSRT_007",
  "AL_BrainSRT_008",
  "AL_BrainSRT_009",
  "AL_BrainSRT_010",
  "AL_BrainSRT_011",
  "AL_BrainSRT_012",
  "AL_BrainSRT_013",
  "AL_BrainSRT_014",
  "AL_BrainSRT_015",
  "AL_BrainSRT_016",
  "AL_BrainSRT_017",
  "AL_BrainSRT_018",
  "AL_BrainSRT_019",
  "AL_BrainSRT_020",
  "AL_BrainSRT_021",
  "AL_BrainSRT_022",
  "AL_BrainSRT_023",
  "AL_BrainSRT_024",
  "AL_BrainSRT_025",
  "AL_BrainSRT_026",
  "AL_BrainSRT_027",
  "AL_BrainSRT_028",
  "AL_BrainSRT_029",
  "AL_BrainSRT_030",
  "AL_BrainSRT_031",
  "AL_BrainSRT_032",
  "AL_BrainSRT_033",
  "AL_BrainSRT_034",
  "AL_BrainSRT_035",
  "AL_BrainSRT_036",
  "AL_BrainSRT_037",
  "AL_BrainSRT_038",
  "AL_BrainSRT_039",
  "AL_BrainSRT_040",
  "AL_BrainSRT_041",
  "AL_BrainSRT_042",
  "AL_BrainSRT_043",
  "AL_BrainSRT_044",
  "AL_BrainSRT_045",
  "AL_BrainSRT_046",
  "AL_BrainSRT_047",
  "AL_BrainSRT_048",
  "AL_BrainSRT_049",
  "AL_BrainSRT_050"
]


# Export folder:
target_path = "C:\\Temp\\RayStation Deep Learning\\AL_BrainSRT"

# Patient database:
patient_db = get_current("PatientDB")


# Iterate patient ids and export RSBAK files:
for name in names:
  # Load patient from database:
  patient_infos = patient_db.QueryPatientInfo(Filter={"LastName": name})
  # Export patient:
  patient_db.BackupPatient(
    PatientInfo=patient_infos[0],
    TargetPath=target_path + "\\",
    AnonymizationSettings={"Anonymize": False},
  )
