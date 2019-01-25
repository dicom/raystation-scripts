# encoding: utf8

from __future__ import division
import math

# Import system libraries:
import clr, sys
from connect import *
import clr, sys
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("PresentationFramework")
from System.Windows import *
# Import local files:
import gui_functions as GUIF
import roi as ROI
import rois as ROIS
import patient_model_functions as PMF
import margin as MARGIN
import margins as MARGINS
import def_brain as DEF_BRAIN
import region_codes as RC



# Checks if a given roi takes part in a approved structure set
def is_approved_roi_structure(ss, roi_name):
  match = False
  for set in ss.ApprovedStructureSets:
    for roi in set.ApprovedRoiStructures:
      if roi.OfRoi.Name == roi_name:
        match = True
  if match:
    GUIF.handle_failed_translation_of_roi(roi_name)
  return match

# Returns the name of the appropriately defined body ROI (having contours),
# which in the case of stereotactic treatment is "Body", and otherwise it is "External".
def body_roi_name(ss):
  if has_roi_with_shape(ss, ROIS.body.name):
    return ROIS.body.name
  elif has_roi_with_shape(ss, ROIS.external.name):
    return ROIS.external.name
  else:
    return None


# Creates a derived ROI using ROI Algebra, where the derived ROI is expanded from the source roi with a margin
# such that the resulting ROI gets a volume approximately equal to the given threshold_volume. The ROI is also
# limited by the given intersect_roi (typically an external ROI) by an intersect operation.
def create_expanded_and_intersected_volume(pm, examination, ss, source_roi, intersect_roi, expanded_roi_name, threshold_volume):
  # Volume of source roi
  volume1 = ss.RoiGeometries[source_roi.name].GetRoiVolume()
  # Estimated radius of source roi calculated from volume (assuming perfect sphere)
  radius1 = math.pow((volume1 * 3)/ (4*math.pi), 1.0/3.0)
  # Estimated radius of expanded roi calculated from thresgold volume (assuming perfect sphere)
  radius2 = math.pow((threshold_volume * 3)/ (4*math.pi), 1.0/3.0)
  # Expansion radius
  r = round(radius2 - radius1, 1)
  # Expanded roi object
  expanded_roi = ROI.ROIAlgebra(expanded_roi_name, 'Undefined', 'Black', sourcesA = [source_roi], sourcesB = [intersect_roi], operator = 'Intersection', marginsA = MARGIN.Expansion(r, r, r, r, r, r), marginsB = MARGINS.zero)
  # Deletes roi if it already exists in RayStation
  PMF.delete_roi(pm, expanded_roi.name)
  # Create ROI in RayStation
  PMF.create_algebra_roi(pm, examination, ss, expanded_roi)

'''
def create_mask_ptv(pm, examination, ss, threshold):

  #threshold = 50
  margin = [MARGINS.uniform_30mm_expansion, MARGINS.uniform_40mm_expansion, MARGINS.uniform_50mm_expansion, MARGINS.uniform_60mm_expansion, MARGINS.uniform_70mm_expansion, MARGINS.uniform_80mm_expansion, MARGINS.uniform_90mm_expansion]
  i = 0
  mask_ptv = ROI.ROIExpanded('MASK_PTV', 'Undefined', 'Black', ROIS.ptv, margins = MARGINS.uniform_20mm_expansion)
  subtraction = ROI.ROIAlgebra('MASK_PTV' + '-' + 'Brain', 'Undefined', 'Black', sourcesA = [mask_ptv], sourcesB = [ROIS.brain], operator = 'Subtraction')
  PMF.delete_roi(pm, mask_ptv.name)
  PMF.create_expanded_roi(pm, examination, ss, mask_ptv)
  PMF.delete_roi(pm, subtraction.name)
  PMF.create_algebra_roi(pm, examination, ss, subtraction)
  while ss.RoiGeometries[subtraction.name].GetRoiVolume() < threshold:
    mask_ptv = ROI.ROIExpanded('MASK_PTV', 'Undefined', 'Black', ROIS.ptv, margins = margin[i])
    subtraction = ROI.ROIAlgebra('MASK_PTV' + '-' + 'Brain', 'Undefined', 'Black', sourcesA = [mask_ptv], sourcesB = [ROIS.brain], operator = 'Subtraction')
    PMF.delete_roi(pm, mask_ptv.name)
    PMF.create_expanded_roi(pm, examination, ss, mask_ptv)
    PMF.delete_roi(pm, subtraction.name)
    PMF.create_algebra_roi(pm, examination, ss, subtraction)
    i += 1

  PMF.delete_roi(pm, subtraction.name)

def create_mask_ptv(pm, examination, ss, threshold):
  volume1 = ss.RoiGeometries['PTV'].GetRoiVolume()
  radius1 = math.pow((volume1 * 3)/ (4*math.pi), 1.0/3.0)
  radius2 = math.pow((threshold * 3)/ (4*math.pi), 1.0/3.0)
  r_mask = round(radius2 - radius1, 1)
  margin = MARGIN.Expansion(r_mask, r_mask, r_mask, r_mask, r_mask, r_mask)
  mask_ptv = ROI.ROIExpanded('MASK_PTV', 'Undefined', 'Black', ROIS.ptv, margins = margin)
  PMF.delete_roi(pm, mask_ptv.name)
  PMF.create_expanded_roi(pm, examination, ss, mask_ptv)
'''

def is_target_oar_overlapping(ss, target, oar):
  center = ss.RoiGeometries[oar].GetCenterOfRoi()
  roi_box = ss.RoiGeometries[target].GetBoundingBox()
  match = False 
  if center.x > roi_box[0].x and center.x < roi_box[1].x and center.y > roi_box[0].y and center.y < roi_box[1].y:
    match = True

  return match


# Creates a ROI where roi2 is subtracted from roi1 (if an overlap exists).
# Note that these are our own ROI objects (not RayStation ROI objects).
# (This check is achieved by temporarily creating a ROI in the patient model)
#
# Returns a boolean indicating whether there actually was an overlap between roi1 and roi2 or not.
# Note that this means the created subtraction roi is not returned (just created).
def create_roi_subtraction(pm, examination, ss, roi1, roi2, subtraction_name, threshold):
  overlap = False
  if has_named_roi_with_contours(ss, roi1.name) and has_named_roi_with_contours(ss, roi2.name):
    subtraction = ROI.ROIAlgebra(subtraction_name, 'Undefined', 'Black', sourcesA = [roi1], sourcesB = [roi2], operator = 'Subtraction')
    # In the rare case that this ROI already exists, delete it (to avoid a crash):
    PMF.delete_roi(pm, subtraction.name)
    PMF.create_algebra_roi(pm, examination, ss, subtraction)
    # Is overlapping volume less than threshold?
    if ss.RoiGeometries[roi1.name].GetRoiVolume() - ss.RoiGeometries[subtraction.name].GetRoiVolume() > threshold:
      overlap = True
  return overlap

# Determines from the region code if the plan is a tangential breast or if it is a breast with regional lymph nodes usign VMAT or 3D-CRT,
# In those cases specific functions are used to find the isocenter, in all other cases the same function is used.
def determine_isocenter(examination, ss, region_code, technique_name, target, external, multiple_targets=False):
  # Determine the point which will be our isocenter:
  iso = False
  for p in ss.PoiGeometries:
    if p.OfPoi.Name in ['Iso', 'ISO']:
      name = p.OfPoi.Name
      if ss.PoiGeometries[name].Point.x != sys.float_info.min:
        isocenter = ss.PoiGeometries[name].Point
        iso = True

  if iso == False:
    if region_code in RC.breast_tang_codes:
      # When tangential fields are used
      isocenter = find_isocenter_conv_breast(ss, target)
    elif region_code in RC.breast_reg_codes:
      # If VMAT technique is used
      if technique_name == 'VMAT':
        if is_breast_hypo(ss):
          isocenter = find_isocenter_vmat_breast(ss, ROIS.ctv.name)
        else:
          if has_roi_with_shape(ss, ROIS.ctv_47_50.name):
            isocenter = find_isocenter_vmat_breast(ss, ROIS.ctv_47_50.name)
          else: # (If the 47 dose level is not defined, use target as "backup")
            isocenter = find_isocenter_vmat_breast(ss, target)
      else:
        # If 3D-CRT technique is used
        if region_code in RC.breast_reg_l_codes:
          level = ROIS.level4_l.name
        else:
          level = ROIS.level4_r.name
        if is_breast_hypo(ss):
          isocenter = find_isocenter_conv_reg_breast(ss, region_code, ROIS.ctv.name, level)
        else:
          isocenter = find_isocenter_conv_reg_breast(ss, region_code, ROIS.ctv_47_50.name, level)
    else:
      # In all other cases
      isocenter = find_isocenter(examination, ss, target, external, multiple_targets=multiple_targets)
  return isocenter


# Determine the treatment machine (i.e. with or without filter) from the size of the target volume.
# Returns the machine name (e.g. 'ALVersa' or 'ALVersa_FFF').
def determine_machine(ss, target):
  threshold = 13
  # Establish start values:
  center = ss.RoiGeometries[target].GetCenterOfRoi()
  ptv_max_z = center.z #longitudinal direction
  ptv_min_z = center.z
  ptv_max_x = center.x #left - right / medial direction
  ptv_min_x = center.x
  ptv_max_y = center.y # anterior - posterior direction
  ptv_min_y = center.y
  # Iterate targets to find extreme boundary coordinates:
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Type in ['Ptv', 'Ctv'] and roi.HasContours():
      ptv_box = roi.GetBoundingBox()
      ptv_box_max_z = ptv_box[1].z
      ptv_box_min_z = ptv_box[0].z
      ptv_box_max_x = ptv_box[1].x
      ptv_box_min_x = ptv_box[0].x
      ptv_box_max_y = ptv_box[1].y
      ptv_box_min_y = ptv_box[0].y
      if ptv_box_min_z < ptv_min_z:
        ptv_min_z = ptv_box_min_z
      if ptv_box_max_z > ptv_max_z:
        ptv_max_z = ptv_box_max_z
      if ptv_box_min_x < ptv_min_x:
        ptv_min_x = ptv_box_min_x
      if ptv_box_max_x > ptv_max_x:
        ptv_max_x = ptv_box_max_x
      if ptv_box_min_y < ptv_min_y:
        ptv_min_y = ptv_box_min_y
      if ptv_box_max_y > ptv_max_y:
        ptv_max_y = ptv_box_max_y
  dist_z = abs(ptv_max_z - ptv_min_z)
  dist_y = abs(ptv_max_y - ptv_min_y)
  dist_x = abs(ptv_max_x - ptv_min_x)
  if dist_x < threshold and dist_y < threshold and dist_z < threshold:
    machine = "ALVersa_FFF"
  else:
    machine = "ALVersa"
  return machine


# Determines the number of targets from indexed PTV's (for example used for stereotactic brain with multiple targets):
def determine_nr_of_indexed_ptvs(ss):
  nr_targets = 1
  if has_roi_with_shape(ss, ROIS.ptv2.name):
    nr_targets += 1
    if has_roi_with_shape(ss, ROIS.ptv3.name):
      nr_targets += 1
      if has_roi_with_shape(ss, ROIS.ptv4.name):
        nr_targets += 1
  return nr_targets


# Determines the prescription target volume of the plan.
def determine_target(ss, nr_fractions, fraction_dose):
  total_dose = int(nr_fractions*fraction_dose)
  match = False
  target = None
  # Stereotactic brain treatments with multiple targets, PTV is the target
  if nr_fractions == 3 and fraction_dose in [7, 8, 9] or nr_fractions == 1 and fraction_dose > 14:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == ROIS.ptv1.name and roi.HasContours():
        target = ROIS.ptv1.name
        match = True

  # Stereotactic treatments, PTV is the target
  if match == False:
    if nr_fractions in [3, 5, 8] and fraction_dose in [15, 11, 7, 8, 9] or nr_fractions == 1 and fraction_dose > 14:
      if determine_nr_of_indexed_ptvs(ss) > 1:
        for roi in ss.RoiGeometries:
          if roi.OfRoi.Name == ROIS.ptv1.name and roi.HasContours():
            target = ROIS.ptv1.name
            match = True
      else:
        for roi in ss.RoiGeometries:
          if roi.OfRoi.Name == ROIS.ptv.name and roi.HasContours():
            target = ROIS.ptv.name
            match = True

 # CTV is the target in most other cases
  if match == False:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == ROIS.ctv.name and roi.HasContours():
        target = ROIS.ctv.name
        match = True

 # CTV based on total dose, for example CTV_50
  if match == False:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == 'CTV_'+ str(total_dose) and roi.HasContours():
        target = 'CTV_'+ str(total_dose)
        match = True

  # CTVp, for breast plans (for now)
  if match == False:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == ROIS.ctv_p.name and roi.HasContours():
        target = ROIS.ctv_p.name
        match = True

  #ICTV
  if match == False:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == ROIS.ictv.name and roi.HasContours():
        target = ROIS.ictv.name
        match = True

  # CTV1
  if match == False:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == ROIS.ctv1.name and roi.HasContours():
        target = ROIS.ctv1.name
        match = True

  # CTVsb
  if match == False:
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Name == ROIS.ctv_sb.name and roi.HasContours():
        target = ROIS.ctv_sb.name
        match = True

  if target:
    return target
  else:
    #raise IOError("Mislyktes i å opprette 'Prescription', årsaken er at ROIen mangler eller at navnet ikke er som forventet.")
    GUIF.handle_missing_target()
    


# Determines the isocenter based on the CTV, and if it does not exist, the PTV, and External contour, (or the Body contour) provided for the given structure set.
def find_isocenter(examination, ss, target, external, multiple_targets=False):
  # Find center of target:
  if has_named_roi_with_contours(ss, target):
    isocenter = ss.RoiGeometries[target].GetCenterOfRoi()
  # Determine x and y coordinate:
  patient_center_y = roi_center_y(ss, external)
  patient_center_x = roi_center_x(ss, external)
  # Patient should always be somewhat centered on the couch. A big offset in x value may be false (e.g. superman position).
  if abs(patient_center_x) > 5:
    patient_center_x = 0

  # Difference between isocenter and patient center:
  dx = isocenter.x - patient_center_x
  dy = isocenter.y - patient_center_y
  length = math.sqrt((dx)**2 +(dy)**2)
  max_length = 12
  if length > max_length:
    dx1 = max_length * dx/length
    dy1 = max_length *dy/length
    isocenter.x = dx1 + patient_center_x
    isocenter.y = dy1 + patient_center_y

  # Determine z coordinate for multiple targets:
  if multiple_targets:
    ctv_upper = abs(isocenter.z)
    ctv_lower = abs(isocenter.z)
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Type in ['Ctv','Ptv'] and roi.HasContours():
        ctv_box = roi.GetBoundingBox()
        ctv_box_upper = ctv_box[1].z
        ctv_box_lower = ctv_box[0].z
        if abs(ctv_box_upper) < abs(ctv_upper):
          ctv_upper = ctv_box_upper
        if abs(ctv_box_lower) > abs(ctv_lower):
          ctv_lower = ctv_box_lower
      middle_point = abs(ctv_upper - ctv_lower)/2
      isocenter.z = ctv_lower + middle_point
  return isocenter


# Determines the isocenter based on a given target and External contour provided for the given structure set.
# Used for tangential 3D-CRT breast plans
def find_isocenter_conv_breast(ss, target):
  if has_named_roi_with_contours(ss, target):
    box = ss.RoiGeometries[target].GetBoundingBox()
    ctv_long_senter = abs(box[0].z - box[1].z)/2
    ctv_long_point = box[0].z + ctv_long_senter
    ctv_lat_senter = abs(box[0].x - box[1].x)/2
    ctv_lat_point = box[0].x + ctv_lat_senter
    ctv_ant_senter = abs(box[0].y - box[1].y)/2
    ctv_ant_point = box[0].y + ctv_ant_senter
    isocenter = ss.RoiGeometries[target].GetCenterOfRoi()
    if ctv_lat_point < 0:
      isocenter.x = ctv_lat_point + 1.5
    else:
      isocenter.x = ctv_lat_point - 1.5
    isocenter.y = ctv_ant_point + 2
    isocenter.z = ctv_long_point
    return isocenter


# Determines the isocenter based on a given target, the structure LN_Ax_L4 and External contour provided for the given structure set.
# Used for 3D-CRT breast with regional lymph nodes
def find_isocenter_conv_reg_breast(ss, region_code, target, node_target):
  if has_named_roi_with_contours(ss, target):
    isocenter = ss.RoiGeometries[target].GetCenterOfRoi()
    ctv = ss.RoiGeometries[target].GetBoundingBox()

    ctv_lat_senter = abs(ctv[0].x - ctv[1].x)/2
    ctv_lat_point = ctv[0].x + ctv_lat_senter #+ 2
    ctv_ant_senter = abs(ctv[0].y - ctv[1].y)/2
    ctv_ant_point = ctv[0].y + ctv_ant_senter #- 2

    if region_code in [242, 244]:
      isocenter.x = ctv_lat_point + 2.5
    else:
      isocenter.x = ctv_lat_point - 2.5

    isocenter.y = ctv_ant_point + 2.5
    if has_named_roi_with_contours(ss, node_target):
      ctv_n = ss.RoiGeometries[node_target].GetBoundingBox()
      ctv_long_point = ctv_n[0].z
    else:
      ctv_long_point = ctv[0].z
    isocenter.z = ctv_long_point -1.5
    return isocenter


# Determines the isocenter for VMAT breast with regional lymph nodes
def find_isocenter_vmat_breast(ss, target):
  # Find center of target:
  if has_named_roi_with_contours(ss, target):
    isocenter = ss.RoiGeometries[target].GetCenterOfRoi()
    # Determine x and y coordinate:
    patient_center_x = roi_center_x(ss, ROIS.external.name)
    patient_center_y = roi_center_y(ss, ROIS.external.name)
    length = math.sqrt((isocenter.x - patient_center_x)**2 +(isocenter.y - patient_center_y)**2)
    max_length = 9
    if length > max_length:
      y = isocenter.y - patient_center_y
      x = abs(isocenter.x - patient_center_x)
      x1 = max_length * x/length
      y1 = max_length * y/length * (isocenter.y)/(abs(isocenter.y))
      isocenter.x =  x1 * (isocenter.x)/(abs(isocenter.x))
      isocenter.y = patient_center_y - y1* (isocenter.x)/(abs(isocenter.x))
    return isocenter


# Finds the isocenter coordinate in the longitudinal, or z-direction:
def find_isocenter_z(ss, target):
  if has_named_roi_with_contours(ss, target):
    isocenter = ss.RoiGeometries[target].GetCenterOfRoi()

    ctv_upper = abs(isocenter.z)
    ctv_lower = abs(isocenter.z)
    for roi in ss.RoiGeometries:
      if roi.OfRoi.Type in ['Ctv','Ptv'] and roi.HasContours():
        ctv_box = roi.GetBoundingBox()
        ctv_box_upper = ctv_box[1].z
        ctv_box_lower = ctv_box[0].z
        if abs(ctv_box_upper) < abs(ctv_upper):
          ctv_upper = ctv_box_upper
        if abs(ctv_box_lower) > abs(ctv_lower):
          ctv_lower = ctv_box_lower
    middle_point = abs(ctv_upper - ctv_lower)/2
    isocenter.z = ctv_lower + middle_point
    return isocenter.z


# Returns the most caudal coordinate of the given roi geometry.
def find_lower_z(ss, roi_geometry):
  box = ss.RoiGeometries[roi_geometry].GetBoundingBox()
  return box[0].z


# Returns the most caudal coordinate of the given roi geometry.
def find_upper_z(ss, roi_geometry):
  box = ss.RoiGeometries[roi_geometry].GetBoundingBox()
  return box[1].z


# Returns true if the structure set contains a ROI with the given name.
def has_roi(ss, name):
  match = False
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Name == name:
      match = True
      break
  return match


# Returns true if any rois have a contour in this stucture set.
def has_roi_with_contours(ss):
  match = False
  for roi in ss.RoiGeometries:
    if roi.HasContours():
      match = True
      break
  return match


# Returns true if any rois have a contour in this stucture set.
def has_named_roi_with_contours(ss, name):
  match = False
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Name == name and roi.HasContours():
      match = True
      break
  return match


# Returns true if the structure set contains a ROI with a defined volume matching the given name.
def has_roi_with_shape(ss, name):
  match = False
  for roi in ss.RoiGeometries:
    if roi.OfRoi.Name == name and roi.PrimaryShape:
      match = True
      break
  return match


def is_breast_hypo(ss):
  if has_roi_with_shape(ss, ROIS.ptv_pc.name):
    return True
  else:
    return False


# Determines if the volume of PTV that overlaps with OARs is less than a given threshold
# (Used to determine whether to use single or dual arc VMAT at the moment)
def partial_brain_conflict_oars(ss):
  threshold = 3
  if has_roi_with_shape(ss, ROIS.ptv_and_oars.name):
    if ss.RoiGeometries[ROIS.ptv.name].GetRoiVolume() - ss.RoiGeometries[ROIS.ptv_and_oars.name].GetRoiVolume() < threshold:
      return True
    else:
      return False


# Checks if there is an overlap between the two given ROI objects.
# Note that these are our own ROI objects (not RayStation ROI objects).
# (This check is achieved by temporarily creating a ROI in the patient model)
def roi_overlap(pm, examination, ss, roi1, roi2, threshold):
  subtraction = ROI.ROIAlgebra(roi1.name + '-' + roi2.name, 'Undefined', 'Black', sourcesA = [roi1], sourcesB = [roi2], operator = 'Subtraction')
  # In the rare case that this ROI already exists, delete it (to avoid a crash):
  PMF.delete_roi(pm, subtraction.name)
  PMF.create_algebra_roi(pm, examination, ss, subtraction)
  # Is overlapping volume less than threshold?
  overlap = False
  if ss.RoiGeometries[roi1.name].GetRoiVolume() - ss.RoiGeometries[subtraction.name].GetRoiVolume() > threshold:
    overlap = True
  PMF.delete_roi(pm, subtraction.name)
  return overlap


# Returns a ROI Geometry matching the given ROI name in the given structure set.
def rg(ss, roi_name):
  for rg in ss.RoiGeometries:
    if rg.OfRoi.Name == roi_name:
      return rg


#Finds the center point of a roi in the x, y and z direction, returns a dictionary object.
#def roi_center_point(ss, roi):
  #roi_box = ss.RoiGeometries[roi].GetBoundingBox()
  #roi_x_middle = (roi_box[1].x-roi_box[0].x)/2
  #roi_x = roi_box[0].x + roi_x_middle
  #roi_y_middle = (roi_box[1].y-roi_box[0].y)/2
  #roi_y = roi_box[0].y + roi_y_middle
  #roi_z_middle = (roi_box[1].z-roi_box[0].z)/2
  #roi_z = roi_box[0].z + roi_z_middle
  #roi = {'x':roi_x,'y':roi_y, 'z':roi_z}
  #return roi


# Finds the center point  in the x direction
def roi_center_x(ss, roi):
  roi_box = ss.RoiGeometries[roi].GetBoundingBox()
  roi_x_middle = (roi_box[1].x-roi_box[0].x)/2
  roi_x = roi_box[0].x + roi_x_middle
  return roi_x


# Finds the center point  in the y direction
def roi_center_y(ss, roi):
  roi_box = ss.RoiGeometries[roi].GetBoundingBox()
  roi_y_middle = (roi_box[1].y-roi_box[0].y)/2
  roi_y = roi_box[0].y + roi_y_middle
  return roi_y


# Finds the center point  in the z direction
def roi_center_z(ss, roi):
  roi_box = ss.RoiGeometries[roi].GetBoundingBox()
  roi_z_middle = (roi_box[1].z-roi_box[0].z)/2
  roi_z = roi_box[0].z + roi_z_middle
  return roi_z
