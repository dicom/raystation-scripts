# encoding: utf8

# Contains treatment plan tests for individual treatment plans.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys
#sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\RayStation\\lib".decode('utf8'))

# GUI framework (debugging only):
#clr.AddReference("PresentationFramework")
#from System.Windows import *

# Local script imports:
import test as TEST
import raystation_utilities as RSU

# This class contains tests for the RayStation Poi Geometry object:
class TSPOIGeometry(object):
  def __init__(self, poi_geometry, ts_structure_set=None):
    # RayStation object:
    self.poi_geometry = poi_geometry
    # Related test suite objects:
    self.ts_structure_set = ts_structure_set
    if ts_structure_set:
      ts_structure_set.ts_poi_geometries.append(self)
      self.parent_param = ts_structure_set.param
    else:
      self.parent_param = None
    # Parameters:
    self.param = TEST.Parameter('POI Geometri', self.poi_geometry.OfPoi.Name.decode('utf8', 'replace'), self.parent_param)
    self.coordinates = TEST.Parameter('Koordinater', '', self.param)

  # Tests for coordinate definition.
  def is_defined_test(self):
    t = TEST.Test("Skal ha definerte koordinater", True, self.coordinates)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    # (FIXME: This may not be correct for mamma gating)
    if self.ts_structure_set.structure_set == self.ts_structure_set.ts_case.ts_plan.plan.GetStructureSet():
      # When the poi geometry is undefined, RayStation seems to represent this with the min float value:
      if self.poi_geometry.Point.x != sys.float_info.min:
        return t.succeed()
      else:
        return t.fail()

  # Tests for coordinate definition.
  def is_not_zero_test(self):
    t = TEST.Test("Skal ikke ha koordinater i punktet: 0,0,0", True, self.coordinates)
    # Run test if this structure set corresponds to the examination used for the treatment plan:
    # (FIXME: This may not be correct for mamma gating)
    if self.ts_structure_set.structure_set == self.ts_structure_set.ts_case.ts_plan.plan.GetStructureSet():
      # When the poi geometry is undefined, RayStation seems to represent this with the min float value:
      if self.poi_geometry.Point.x == 0 and self.poi_geometry.Point.y == 0 and self.poi_geometry.Point.z == 0:
        return t.fail()
      else:
        return t.succeed()