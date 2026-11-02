'''Updates all ROIs which are derived and not up to date.

Authors:
Christoffer Lervåg
Helse Møre og Romsdal HF
'''

# Import system libraries:
import sys

# Import RayStation packages:
sys.path.append("C:/Program Files/RaySearch Laboratories/RayStation 2024B/ScriptClient/")
from connect import *

# Load case and examination:
case = get_current("Case")
examination = get_current("Examination")

# Search for ROIs which are derived but not updated:
for struct in case.PatientModel.StructureSets:
  for roi in struct.RoiGeometries:
    # Is the ROI empty or defined?
    if roi.PrimaryShape:
      # Is this a derived ROI?
      if roi.PrimaryShape.DerivedRoiStatus:
        # Check for dirty shape:
        if roi.PrimaryShape.DerivedRoiStatus.IsShapeDirty == True:
          # Update dirty ROI:
          roi.OfRoi.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
    else:
      # Is the empty ROI derived?
      if roi.OfRoi.DerivedRoiExpression:
        # Initialize the ROI geometry by using the update feature:
        roi.OfRoi.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
