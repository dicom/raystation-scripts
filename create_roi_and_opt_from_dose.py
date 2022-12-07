from connect import *

plan = get_current('Plan')
case = get_current('Case')
beamset = get_current('BeamSet')

# Access the plan dose
plan_dose = plan.TreatmentCourse.TotalDose

# Define the threshold level
threshold_level = beamset.Prescription.PrimaryPrescriptionDoseReference.DoseValue * 0.95

# Create a new ROI and create its geometry from the plan dose
# and the threshold level
# Define the name of the ROI
roi_name = '95'
roi = case.PatientModel.CreateRoi(Name = roi_name, Color = 'Blue', Type = 'Control')
roi.CreateRoiGeometryFromDose(DoseDistribution = plan_dose, ThresholdLevel = threshold_level)

from connect import *

case = get_current("Case")
examination = get_current("Examination")


with CompositeAction('ROI Algebra (opt)'):

  retval_0 = case.PatientModel.CreateRoi(Name=r"opt", Color="Gray", Type="Ptv", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)

  retval_0.SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': [r"PTV"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ExpressionB={ 'Operation': "Union", 'SourceRoiNames': [r"95"], 'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, ResultOperation="Subtraction", ResultMarginSettings={ 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 })

  retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

  # CompositeAction ends 


with CompositeAction('Apply ROI changes (opt)'):

  case.PatientModel.ToggleExcludeFromExport(ExcludeFromExport=True, RegionOfInterests=[r"opt"], PointsOfInterests=[])

  case.PatientModel.RegionsOfInterest['opt'].OrganData.OrganType = "Other"

  # CompositeAction ends 



