# encoding: utf8

# Import system libraries:

import math
# Import local files:

# Contains a collection of ROI functions.

# Determines if two roi geometries are closer to each other than the given threshold (in cm).
# This is calculated by determining the center and radius of the geometries by approximating them as perfect spheres.
def roi_vicinity_approximate(roi_geometry1, roi_geometry2, threshold):
  result = False
  if roi_geometry1.HasContours() and roi_geometry2.HasContours():
    center1 = roi_geometry1.GetCenterOfRoi()
    volume1 = roi_geometry1.GetRoiVolume()
    center2 = roi_geometry2.GetCenterOfRoi()
    volume2 = roi_geometry2.GetRoiVolume()
    radius1 = math.pow((volume1 * 3)/ (4*math.pi), 1.0/3.0)
    radius2 = math.pow((volume2 * 3)/ (4*math.pi), 1.0/3.0)
    length = math.sqrt((center1.x - center2.x)**2 +(center1.y - center2.y)**2 +(center1.z - center2.z)**2 )
    max_length = radius1 + radius2 + threshold
    if length < max_length:
      result = True
  return result
