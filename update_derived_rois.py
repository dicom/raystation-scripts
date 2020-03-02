# encoding: utf8

# Updates all ROIs which are derived and not up to date.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 6.0
# Python 3.6

from connect import *

case = get_current("Case")
examination = get_current("Examination")

# Search for ROIs which are derived but not updated:
for struct in case.PatientModel.StructureSets:
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



