
# Import system libraries:
from connect import *


plan = get_current('Plan')
case = get_current('Case')
beam_set = get_current('BeamSet')

# Access the plan dose
plan_dose = plan.TreatmentCourse.TotalDose

# Define the threshold level
threshold_level =beam_set.Prescription.PrimaryPrescriptionDoseReference.DoseValue * 0.95

# Create a new ROI and create its geometry from the plan dose
# and the threshold level
# Define the name of the ROI
roi_name = '95'
roi = case.PatientModel.CreateRoi(Name = roi_name, Color = 'Green', Type = 'Control')
roi.CreateRoiGeometryFromDose(DoseDistribution = plan_dose, ThresholdLevel = threshold_level)














