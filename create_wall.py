# Script recorded 06 Dec 2019, 13:45:06

#   RayStation version: 9.0.0.113
#   Selected patient: ...

from connect import *

case = get_current("Case")
examination = get_current("Examination")


with CompositeAction('Create wall (zPTV_Wall)'):

  retval_0 = case.PatientModel.CreateRoi(Name=r"zPTV_Wall", Color="Gray", Type="Organ", TissueName=None, RbeCellTypeName=None, RoiMaterial=None)

  retval_0.SetWallExpression(SourceRoiName=r"PTV", OutwardDistance=1, InwardDistance=0)

  retval_0.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

  # CompositeAction ends 


with CompositeAction('Apply ROI changes (zPTV_Wall)'):

  case.PatientModel.ToggleExcludeFromExport(ExcludeFromExport=True, RegionOfInterests=[r"zPTV_Wall"], PointsOfInterests=[])

  case.PatientModel.RegionsOfInterest['zPTV_Wall'].OrganData.OrganType = "Other"

  # CompositeAction ends 



