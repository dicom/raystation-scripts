# encoding: utf8

# Import local files:

# Contains a collection of beam functions.


# Gives rotation direction based on gantry start and stop angles.
# Returns a string, i.e. either 'CounterClockwise' or 'Clockwise'.
def rotation_direction(start, stop):
  rotation = 'Clockwise'
  # We need to have to separate tests for gantry stop angles above or below 180 degrees:
  if float(stop) >= 180:
    if not 180 < float(start) < float(stop):
      rotation = 'CounterClockwise'
  else: # stop < 180
    if float(stop) < float(start) < 180:
      rotation = 'CounterClockwise'
  return rotation


 # Sets up treat or protect for a given beam.
 # Required parameters are the RayStation beam instance, ROI name and the margin to be used (cm).
def set_up_treat_or_protect(beam, roi_name, margin):
  assert isinstance(roi_name, str), "roi_name is not a string: %r" % roi_name
  assert isinstance(margin, (float, int)), "margin is not a float or integer: %r" % margin
  beam.SetTreatOrProtectRoi(RoiName = roi_name, TopMargin = margin, BottomMargin = margin, LeftMargin = margin, RightMargin = margin)
