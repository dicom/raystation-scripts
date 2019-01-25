# encoding: utf8

# A collection of convenience methods for dealing with the RayStation scripting interface.
#
# Verified for RayStation 6.0.


# Gets the optimization BeamSettings that corresponds to the given beam, beam set and plan:
def beam_settings(plan, beam_set, beam):
  po = plan_optimization(plan, beam_set)
  if po:
     for setup_setting in po.OptimizationParameters.TreatmentSetupSettings:
      for beam_setting in setup_setting.BeamSettings:
        if beam_setting.ForBeam.Number == beam.Number:
          return beam_setting

# Checks whether a given segment has any MLC positions
# that violate the corner boundaries on an Elekta linac.
# Returns True if violation exists, False if not.
def check_mlc_corners(segment):
  violated = False
  if segment.LeafPositions.Length != 2:
    raise "Unexpected number of leaf positions for segment. Expected 2, got" + str(segment.LeafPositions.Length)
  else:
    if segment.LeafPositions[0].Length == 80:
      # Agility/Versa HD:
      limits = [20.0 for i in range(80)]
      limits[0] = limits[79] = 16.1
      limits[1] = limits[78] = 16.7
      limits[2] = limits[77] = 17.3
      limits[3] = limits[76] = 17.8
      limits[4] = limits[75] = 18.3
      limits[5] = limits[74] = 18.8
      limits[6] = limits[73] = 19.2
      limits[7] = limits[72] = 19.7
    elif segment.LeafPositions[0].Length == 40:
      # Synergy:
      limits = [20.0 for i in range(40)]
      limits[0] = limits[39] = 16.4
      limits[1] = limits[38] = 17.5
      limits[2] = limits[37] = 18.4
      limits[3] = limits[36] = 19.5
    else:
      raise "Unexpected number of leaves for segment. Expected 40 or 80, got" + str(segment.LeafPositions[0].Length)
    # Iterate leaf positions and check against limits:
    for i in range(len(limits)):
      if segment.LeafPositions[0][i] < -limits[i]:
        violated = True
      if segment.LeafPositions[1][i] > limits[i]:
        violated = True
  return violated

# Checks whether two points (e.g. isocenter point) are equal or not.
# The coordinates are checked with a precision of 2 decimals.
def equal_points(p1, p2):
  if round(p1.x, 2) == round(p2.x, 2) and round(p1.y, 2) == round(p2.y, 2) and round(p1.z, 2) == round(p2.z, 2):
    return True
  else:
    return False

# Gets the PlanOptimization that corresponds to the given beam set (and plan):
def plan_optimization(plan, beam_set):
  for plan_opt in plan.PlanOptimizations:
    for opt_beam_set in plan_opt.OptimizedBeamSets:
      if opt_beam_set.Number == beam_set.Number:
        return plan_opt

# Gives the arc rotation required in practice to go from the one angle to the next.
# This is valid for both collimator and gantry angles.
def practical_angle_delta(first, second):
  a1 = proper_angle(first)
  a2 = proper_angle(second)
  if a1 >= 0 and a1 < 180:
    a1 = 360 + a1
  if a2 >= 0 and a2 < 180:
    a2 = 360 + a2
  return abs(a1 - a2)

# Gives the proper angle (e.g. collimator or gantry) in the way presented by the TPS.
# I.e, for a value of 0-360, the paramater is returned unchanged.
# For values above 360, 360 is subtracted recursively until the value is below 360.
# For values below 0, 360 is added recursively until the value is above 0.
def proper_angle(value):
  if value > 360:
    return proper_angle(value - 360)
  elif value < 0:
    return proper_angle(value + 360)
  else:
    return value

# Gives the length of a ScriptObjecctCollection.
# (this object doesn't respond to the len() method usually called on lists)
def soc_length(collection):
  nr = 0
  for items in collection:
    nr += 1
  return nr
# Formats a string for output.
def f(str):
  if str:
    #return str.decode('utf8', 'replace')
    return str.decode('iso-8859-1', 'replace')
  else:
    return ''

# Gets the strucutre set POI geometry that corresponds to the given Point of Interest:
#def ss_poi_geometry(pm, poi):
  #for struct in pm.StructureSets:
    #for p in struct.PoiGeometries:
      #if p.OfPoi == poi:
        #return p

# Gets the strucutre set POI geometry that corresponds to the given Point of Interest (in a given beam set):
# This assumes there is a FractionDose structure.
def ss_poi_geometry(bs, poi):
  for p in bs.FractionDose.OnDensity.OutlineSource.PoiGeometries:
    if p.OfPoi == poi:
      return p


# Gets the strucutre set ROI geometry that corresponds to the given Region of Interest (in a given beam set):
def ss_roi_geometry(bs, roi):
  if bs.FractionDose.OnDensity: # (For e.g. imported plans, OnDensity may be missing)
    for r in bs.FractionDose.OnDensity.OutlineSource.RoiGeometries:
      if r.OfRoi == roi:
        return r


# Gets the accumulated "typed" (i.e. from beam set label) dose of a beam_set
# (i.e. different from the directly typed dose for beam sets which use background dose)
# This function works recursively.
def accumulated_label_dose(plan, beam_set, label):
  dose = 0
  if label.valid:
    # Get the "plan optimization" corresponding to this beam set (in order to see if background dose has been used):
    beam_set_opt = plan_optimization(plan, beam_set)
    dose = label.dose
    if beam_set_opt.BackgroundDose:
      dose += accumulated_label_dose(plan, beam_set_opt.BackgroundDose.ForBeamSet, label)
  return dose

# Checks if two isocenters are equal or not:
#def equal_iso(iso1, iso2):
  #if round(iso1.x, 2) == round(iso2.x, 2) and round(iso1.y, 2) == round(iso2.y, 2) and round(iso1.z, 2) == round(iso2.z, 2):
    #return True
  #else:
    #return False

# Returns the beam set (if any) which the given beam set depends on (with background dose).
def background_beam_set(plan, beam_set):
  beam_set_opt = plan_optimization(plan, beam_set)
  if beam_set_opt.BackgroundDose:
    return beam_set_opt.BackgroundDose.ForBeamSet
  else:
    return None

# Gives the prescription dose, in Gy:
def prescription_dose(beam_set):
  if beam_set.Prescription.PrimaryDosePrescription:
    return beam_set.Prescription.PrimaryDosePrescription.DoseValue / 100.0

# Gives the differential prescription dose, in Gy:
# For beam sets with background dose, this function will return the prescription dose used in
# practice for the plan optimization. E.g. for a 0-46 plan (depending on a 46-50 plan), it will give
# 46 Gy, instead of 50 Gy as the prescription_dose() function would.
# For non-background dose beam sets, the result is equal to the prescription_dose() function.
def differential_prescription_dose(plan, beam_set):
  return prescription_dose(beam_set) - background_prescription_dose(plan, beam_set)

# Gives the prescription dose (if any) that is contributed from beam sets that this
# beam set is depending on (through the background dose selection).
# E.g. for a 0-46 beam set, depending on a 46-50 beam set, this will return 4.
def background_prescription_dose(plan, beam_set):
  dose = 0
  bg_bs = background_beam_set(plan, beam_set)
  if bg_bs:
    dose = prescription_dose(bg_bs) + background_prescription_dose(plan, bg_bs)
  return dose

# Gives the fraction dose, in Gy:
def fraction_dose(beam_set):
  if beam_set.Prescription.PrimaryDosePrescription:
    return (beam_set.Prescription.PrimaryDosePrescription.DoseValue / 100.0) / beam_set.FractionationPattern.NumberOfFractions
  else:
    return 0

# Gives the dose in Gy:
def gy(dose):
  return dose / 100

#Returns true if a volume of the given type exists in the structure set
def roi_type(ss, type):
  match = False
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Type == type and roi.PrimaryShape:
      match = True
  return match


#Returns true if a volume of the given name exists in the structure set
def roi_name(ss, name):
  match = False
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Name == name and roi.PrimaryShape:
      match = True
  return match

#Finds the center point  in the x direction
def roi_center_x(ss, roi):
  roi_box = ss.RoiGeometries[roi].GetBoundingBox()
  roi_x_middle = (roi_box[1].x-roi_box[0].x)/2
  roi_x = roi_box[0].x + roi_x_middle
  return roi_x

#Finds the center point  in the y direction
def roi_center_y(ss, roi):
  roi_box = ss.RoiGeometries[roi].GetBoundingBox()
  roi_y_middle = (roi_box[1].y-roi_box[0].y)/2
  roi_y = roi_box[0].y + roi_y_middle
  return roi_y


# Returns true if the structure set contains a ROI with a defined volume matching the given name.
def has_roi_with_shape(ss, name):
  match = False
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Name == name and roi.PrimaryShape:
      match = True
  return match

# Returns the name of the appropriately defined body ROI (having contours),
# which in the case of stereotactic treatment is "Body", and otherwise it is "External".
def body_roi_name(ss):
  if has_roi_with_shape(ss, 'Body'):
    return 'Body'
  elif has_roi_with_shape(ss, 'External'):
    return 'External'
  else:
    return None