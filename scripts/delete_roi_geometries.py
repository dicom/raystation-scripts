'''Deletes ROI geometries for all ROIs (except for External and Couch) for the current patient.

This script is typically used on training cases where ROIs have been segmented previously,
and the current user wants a fresh start with empty ROI geometries.

Authors:
Christoffer Lervåg
Helse Møre og Romsdal HF
'''

# Import system libraries:
import sys

# Import RayStation packages:
sys.path.append("C:/Program Files/RaySearch Laboratories/RayStation 2024B/ScriptClient/")
from connect import *

# Load case data:
try:
  case = get_current("Case")
except SystemError:
  raise IOError("No case loaded.")

# Iterate structure sets and ROI geometries:
for struct in case.PatientModel.StructureSets:
  for rg in struct.RoiGeometries:
    # Is the ROI neither External or Support?
    if not rg.OfRoi.Type in ['External', 'Support']:
      # Delete the geometry:
      rg.DeleteRoiGeometry()
