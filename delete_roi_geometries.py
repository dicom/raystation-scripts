# Deletes all ROI geometries for the current patient, except for External and Couch.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#

from connect import *

case = get_current("Case")

# Iterate structure sets and ROI geometries:
for struct in case.PatientModel.StructureSets:
  for rg in struct.RoiGeometries:
    # Is the ROI neither External or Support?
    if not rg.OfRoi.Type in ['External', 'Support']:
      # Delete the geometry:
      rg.DeleteGeometry()
