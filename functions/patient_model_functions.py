# encoding: utf8
from __future__ import division

# Import local files:
import roi as ROI
import rois as ROIS
import colors as COLORS
import gui_functions as GUIF
import structure_set_functions as SSF


# Creates an algebra roi from a ROIAlgebra object.
def create_algebra_roi(pm, examination, ss, roi):
  pm.CreateRoi(Name = roi.name, Color = roi.color, Type = roi.type)
  # Get ROI geometry:
  roi_geometry = SSF.rg(ss, roi.name)
  # Make sure that all ROI sources exists:
  missing = []
  sources = list(roi.sourcesA) # (we need to make sure that we're working on a copy of this list)
  sources.extend(roi.sourcesB)
  for source_roi in sources:
    if not SSF.has_roi(ss, source_roi.name):
      missing.append(source_roi.name)
  if len(missing) == 0:
    roi_geometry.OfRoi.CreateAlgebraGeometry(
      Examination = examination,
      ExpressionA = roi.expressionA(),
      ExpressionB = roi.expressionB(),
      ResultOperation =roi.operator,
      ResultMarginSettings = roi.result_margin_settings()
    )
    roi_geometry.OfRoi.SetAlgebraExpression(
      ExpressionA = roi.expressionA(),
      ExpressionB = roi.expressionB(),
      ResultOperation =roi.operator,
      ResultMarginSettings = roi.result_margin_settings()
    )
    roi_geometry.OfRoi.UpdateDerivedGeometry(Examination = examination)
  else:
    GUIF.handle_missing_roi_for_derived_rois(roi.name, missing)


# Creates the couch templated based support ROI:
def create_couch(pm, examination):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == ROIS.couch.name:
      pm_roi.DeleteRoi()
      break
  pm.CreateStructuresFromTemplate(
    SourceTemplateName="Bordtopp tykk",
    SourceExaminationName= "CT 1",
    SourceRoiNames=[ROIS.couch.name],
    SourcePoiNames=[],
    AssociateStructuresByName=False,
    TargetExamination=examination,
    InitializationOption="AlignImageCenters"
  )


# Creates an empty roi from a roi object
def create_empty_roi(pm, roi):
  pm.CreateRoi(Name = roi.name, Color = roi.color, Type = roi.type)


# Creates a derived ROI geometry with a uniform margin expanded from a specified ROIExpanded object.
def create_expanded_roi(pm, examination, ss, roi):
  pm.CreateRoi(Name = roi.name, Color = roi.color, Type = roi.type)
  # Get ROI geometry:
  roi_geometry = SSF.rg(ss, roi.name)
  # Make sure that the source ROI exists:
  if SSF.has_roi(ss, roi.source.name):
    roi_geometry.OfRoi.CreateMarginGeometry(
      Examination = examination,
      SourceRoiName = roi.source.name,
      MarginSettings = roi.margin_settings
    )
    roi_geometry.OfRoi.SetMarginExpression(
      SourceRoiName = roi.source.name,
      MarginSettings = roi.margin_settings
    )
    roi_geometry.OfRoi.UpdateDerivedGeometry(Examination = examination)
  else:
    GUIF.handle_missing_roi_for_derived_rois(roi.name, [roi.source.name])


# Creates an external ROI
def create_external_geometry(pm, examination, ss):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == ROIS.external.name:
      pm_roi.DeleteRoi()
      break
  pm.CreateRoi(Name = ROIS.external.name, Color = ROIS.external.color, Type = ROIS.external.type)
  ss.RoiGeometries[ROIS.external.name].OfRoi.CreateExternalGeometry(Examination = examination, ThresholdLevel = None)


# Creates a localization point (if one doesn't already exist).
def create_localization_point(pm, examination):
  match = False
  for poi in pm.PointsOfInterest:
    if poi.Type == 'LocalizationPoint':
      match = True
  if not match:
    pm.CreatePoi(Examination = examination, Name = 'Ref', Color = COLORS.ref , Type = 'LocalizationPoint')


# Creates model based ROIs.
def create_model_roi(pm, examination, roi):
  # Model based segmentation sometimes crashes. We need to catch these situations to allow scripts to go on:
  try:
    pm.MBSAutoInitializer(
      MbsRois=[{'CaseType': roi.case, 'ModelName': roi.model, 'RoiName': roi.name, 'RoiColor': roi.color}],
      CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=True
    )
    pm.AdaptMbsMeshes(Examination=examination, RoiNames=[roi.name])
  except SystemError:
    # Display a message to the user:
    GUIF.handle_failed_model_based_segmentation(roi.name)



# Creates a ROI which is the posterior half of the source roi in all slices.
# Note that this function is somewhat slow, since it has to create a new ROI for every slice.
def create_posterior_half(pm, examination, ss, source_roi, roi):
  center_x = SSF.roi_center_x(ss, source_roi.name)
  center_y = SSF.roi_center_y(ss, source_roi.name)
  center_z = SSF.roi_center_z(ss, source_roi.name)
  source_roi_box = ss.RoiGeometries[source_roi.name].GetBoundingBox()
  x_min = source_roi_box[0].x
  x_max = source_roi_box[1].x
  x = source_roi_box[1].x - source_roi_box[0].x
  boxes = []
  boxes2 = []
  for [contour_index, contour] in enumerate(ss.RoiGeometries[source_roi.name].PrimaryShape.Contours):
    y_min = 9999
    y_max = -9999
    for coordinate in contour:
      if coordinate.y > y_max:
        y_max = coordinate.y
      elif coordinate.y < y_min:
        y_min = coordinate.y
    length = round((abs(y_max - y_min)), 1)
    center_y =y_max
    delete_roi(pm, ROIS.box.name + str(contour_index))
    box = pm.CreateRoi(Name = ROIS.box.name + str(contour_index), Color = ROIS.box.color, Type = ROIS.box.type)
    pm.RegionsOfInterest[ROIS.box.name + str(contour_index)].CreateBoxGeometry(Size={ 'x': x, 'y': length, 'z': 0.3 }, Examination = examination, Center = { 'x': center_x, 'y': center_y, 'z': coordinate.z })
    boxes.append(box)
    boxes2.append(ROI.ROI(ROIS.box.name + str(contour_index), ROIS.box.type, ROIS.box.color))

  subtraction = ROI.ROIAlgebra(roi.name, roi.type, roi.color, sourcesA = [source_roi], sourcesB = boxes2, operator = 'Intersection')
  # In the rare case that this ROI already exists, delete it (to avoid a crash):
  delete_roi(pm, subtraction.name)
  create_algebra_roi(pm, examination, ss, subtraction)
  for i in range(0, len(boxes)):
    delete_roi(pm, boxes[i].Name)


# Creates a ROI which is the posterior half of the source roi in all slices.
# Note that this function is somewhat slow, since it has to create a new ROI for every slice.
def create_posterior_half_fast(pm, examination, ss, source_roi, roi):
  center_x = SSF.roi_center_x(ss, source_roi.name)
  center_y = SSF.roi_center_y(ss, source_roi.name)
  center_z = SSF.roi_center_z(ss, source_roi.name)
  source_roi_box = ss.RoiGeometries[source_roi.name].GetBoundingBox()
  x_min = source_roi_box[0].x
  x_max = source_roi_box[1].x
  x = source_roi_box[1].x - source_roi_box[0].x
  boxes = []
  boxes2 = []
  for [contour_index, contour] in enumerate(ss.RoiGeometries[source_roi.name].PrimaryShape.Contours):
    y_min = 9999
    y_max = -9999
    for coordinate in contour:
      if coordinate.y > y_max:
        y_max = coordinate.y
      elif coordinate.y < y_min:
        y_min = coordinate.y
    length = round((abs(y_max - y_min)), 1)
    center_y =y_max
    delete_roi(pm, ROIS.box.name + str(contour_index))
    box = pm.CreateRoi(Name = ROIS.box.name + str(contour_index), Color = ROIS.box.color, Type = ROIS.box.type)
    i = 0
    for i in range(0, contour_index):
      if i % 3 == 0:
        pm.RegionsOfInterest[ROIS.box.name + str(contour_index)].CreateBoxGeometry(Size={ 'x': x, 'y': length, 'z': 0.3 }, Examination = examination, Center = { 'x': center_x, 'y': center_y, 'z': coordinate.z })

    boxes.append(box)
    boxes2.append(ROI.ROI(ROIS.box.name + str(contour_index), ROIS.box.type, ROIS.box.color))

  subtraction = ROI.ROIAlgebra(roi.name, roi.type, roi.color, sourcesA = [source_roi], sourcesB = boxes2, operator = 'Intersection')
  # In the rare case that this ROI already exists, delete it (to avoid a crash):
  delete_roi(pm, subtraction.name)
  create_algebra_roi(pm, examination, ss, subtraction)
  for i in range(0, len(boxes)):
    delete_roi(pm, boxes[i].Name)

# Creates a ROI which is the posterior half of the source roi in all slices.
# Note that this function is somewhat slow, since it has to create a new ROI for every slice.
def create_bottom_part_x_cm(pm, examination, ss, source_roi, roi, distance):
  if SSF.has_named_roi_with_contours(ss, source_roi.name):
    center_x = SSF.roi_center_x(ss, source_roi.name)
    center_y = SSF.roi_center_y(ss, source_roi.name)
    center_z = SSF.roi_center_z(ss, source_roi.name)
    source_roi_box = ss.RoiGeometries[source_roi.name].GetBoundingBox()
    x_min = source_roi_box[0].x
    x_max = source_roi_box[1].x
    x = source_roi_box[1].x - source_roi_box[0].x
    y_min = source_roi_box[0].y
    y_max = source_roi_box[1].y
    y = source_roi_box[1].y - source_roi_box[0].y
    z_min = source_roi_box[0].z

    z = source_roi_box[1].z - source_roi_box[0].z
    z_cutoff = z_min + distance/2
    delete_roi(pm, ROIS.box.name)
    box = pm.CreateRoi(Name = ROIS.box.name, Color = ROIS.box.color, Type = ROIS.box.type)
    pm.RegionsOfInterest[ROIS.box.name].CreateBoxGeometry(Size={ 'x': x, 'y': y, 'z': distance}, Examination = examination, Center = { 'x': center_x, 'y': center_y, 'z': z_cutoff })

    intersection = ROI.ROIAlgebra(roi.name, roi.type, roi.color, sourcesA = [source_roi], sourcesB = [ROIS.box], operator = 'Intersection')
    # In the rare case that this ROI already exists, delete it (to avoid a crash):
    delete_roi(pm, intersection.name)
    create_algebra_roi(pm, examination, ss, intersection)
    delete_roi(pm, ROIS.box.name)


# As there can only be one external, another external is created for brain stereotactic treatments, called 'Body', where only the patient geometry is included, The same as the normal 'External' for all other patient groups
def create_stereotactic_body_geometry(pm, examination, ss):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == ROIS.body.name:
      pm_roi.DeleteRoi()
      break
  pm.CreateRoi(Name = ROIS.body.name, Color = ROIS.body.color, Type = ROIS.body.type)
  ss.RoiGeometries[ROIS.body.name].OfRoi.CreateExternalGeometry(Examination = examination, ThresholdLevel = None)


# Creates an external ROI used for brain stereotactic treatments where fixation and mask is included in the ROI
def create_stereotactic_external_geometry(pm, examination, ss):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == ROIS.external.name:
      pm_roi.DeleteRoi()
      break
  pm.CreateRoi(Name = ROIS.external.name, Color = ROIS.external.color, Type = ROIS.external.type)
  ss.RoiGeometries[ROIS.external.name].OfRoi.CreateExternalGeometry(Examination = examination, ThresholdLevel = -980)


# Creates a wall roi from a roi object
def create_wall_roi(pm, examination, ss, roi):
  pm.CreateRoi(Name=roi.name, Color=roi.color, Type=roi.type)
  roi_geometry = SSF.rg(ss, roi.name)
  # Make sure that the source ROI exists:
  if SSF.has_roi(ss, roi.source.name):
    roi_geometry.OfRoi.SetWallExpression(SourceRoiName=roi.source.name, OutwardDistance=roi.outward_dist, InwardDistance=roi.inward_dist)
    roi_geometry.OfRoi.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
  else:
    GUIF.handle_missing_roi_for_derived_rois(roi.name, [roi.source.name])


# Delete all ROIs from the patient model.
def delete_all_rois(pm):
  for roi in pm.RegionsOfInterest:
    roi.DeleteRoi()


# Delete any ROIs which already exists.
def delete_matching_rois(pm, rois):
  for pm_roi in pm.RegionsOfInterest:
    for roi in rois:
      if pm_roi.Name == roi.name:
        pm_roi.DeleteRoi()
        break


# Delete any ROIs which already exists, except those which are manually contoured.
# Ikke i bruk lenger?
def delete_rois_except_manually_contoured(pm, ss):
  delete_list = []
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.DerivedRoiExpression:
      # Delete all derived ROIs:
      delete_list.append(pm_roi.Name)
    else:
      # For manual ROIs, only empty ones are deleted:
      if is_empty_by_name(ss, pm_roi.Name):
        delete_list.append(pm_roi.Name)
  #for pm_roi in pm.RegionsOfInterest:
  for roi_name in delete_list:
    pm.RegionsOfInterest[roi_name].DeleteRoi()


# Deletes the ROI from the RayStation Patient Model, unless it is manually contoured.
def delete_matching_roi_except_manually_contoured(pm, ss, roi):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == roi.name:
      if pm_roi.DerivedRoiExpression:
        # When it is derived, we delete it:
        pm_roi.DeleteRoi()
      else:
        # When it is manual, we only delete it if it is empty:
        if is_empty(ss, roi):
          pm_roi.DeleteRoi()
      break


# Delete all ROIs from the patient model.
def delete_roi(pm, name):
  for roi in pm.RegionsOfInterest:
    if roi.Name == name:
      roi.DeleteRoi()


# Returns the structure set that corresponds to the given examination in this patient model.
def get_structure_set(pm, examination):
  ss = pm.StructureSets[examination.Name]
  if ss:
    return ss


# Returns a boolean indicating whether the given structure set contains a CTV with contours defined.
def has_defined_ctv_or_ptv(pm, examination):
  match = False
  structure_set = get_structure_set(pm, examination)
  for rg in structure_set.RoiGeometries:
    if rg.OfRoi.Type == 'Ctv' and rg.HasContours():
      match = True
    elif rg.OfRoi.Type == 'Ptv' and rg.HasContours():
      match = True
  return match


# Returns true if a ROI with the given name exists in this patient model.
def has_roi(pm, roi_name):
  match = False
  for roi in pm.RegionsOfInterest:
    if roi.Name == roi_name:
      match = True
  return match


# Checks if the given ROI has a contour or not (returns True/False).
def is_empty_by_name(ss, roi_name):
  for rg in ss.RoiGeometries:
    if rg.OfRoi.Name == roi_name:
      if not rg.HasContours():
        return True
      else:
        return False


# Checks if the given ROI has a contour or not (returns True/False).
def is_empty(ss, roi):
  for rg in ss.RoiGeometries:
    if rg.OfRoi.Name == roi.name:
      if not rg.HasContours():
        return True
      else:
        return False


# Changes OrganType to "Other" for all ROIs in the given patient model which are of type "Undefined" or "Marker".
def set_all_undefined_to_organ_type_other(pm):
  for roi in pm.RegionsOfInterest:
    if roi.Type in ['Undefined','Marker']:
      roi.OrganData.OrganType = 'Other'



# Translates the couch such that it lies close to the patient in the anterior-posterior direction and centers it in the left-right direction.
def translate_couch(pm, ss, examination, external, couch_thickness = 5.55):
  #couch_thickness = 5.55
  ext_box = ss.RoiGeometries[external].GetBoundingBox()
  ext_center = SSF.roi_center_x(ss, external)
  if abs(ext_center) > 5:
    ext_center = 0
  couch_center_x = SSF.roi_center_x(ss, ROIS.couch.name)
  couch_box = ss.RoiGeometries[ROIS.couch.name].GetBoundingBox()
  y_translation = -(abs(couch_box[1].y - ext_box[1].y)-couch_thickness)
  x_translation = ext_center - couch_center_x
  transMat = {
    'M11':1.0,'M12':0.0,'M13':0.0,'M14':x_translation,
    'M21':0.0,'M22':1.0,'M23':0.0,'M24':y_translation,
    'M31':0.0,'M32':0.0,'M33':1.0,'M34':0.0,
    'M41':0.0,'M42':0.0,'M43':0.0,'M44':1.0
    }
  pm.RegionsOfInterest[ROIS.couch.name].TransformROI3D(Examination=examination, TransformationMatrix=transMat)


# Translates the couch in the longitudinal direction based on where the target volume is situated.
def translate_couch_long(pm, ss, examination, target):
  isocenter_z = SSF.find_isocenter_z(ss, target)
  new_couch_z = isocenter_z
  couch_center_z = SSF.roi_center_z(ss, ROIS.couch.name)

  img_box = ss.OnExamination.Series[0].ImageStack.GetBoundingBox()
  img_upper = img_box[1].z
  img_lower = img_box[0].z
  couch_length = 36.4
  if abs(new_couch_z - img_lower) < couch_length/2:
    new_couch_z = img_lower + couch_length/2
  elif abs(new_couch_z - img_upper) < couch_length/2:
    new_couch_z = img_upper -couch_length/2

  z_translation = new_couch_z - couch_center_z

  transMat = {
    'M11':1.0,'M12':0.0,'M13':0.0,'M14':0.0,
    'M21':0.0,'M22':1.0,'M23':0.0,'M24':0.0,
    'M31':0.0,'M32':0.0,'M33':1.0,'M34':z_translation,
    'M41':0.0,'M42':0.0,'M43':0.0,'M44':1.0
    }
  # Only move couch if the translation is above threshold:
  if z_translation > 1 and SSF.is_approved_roi_structure(ss, ROIS.couch.name) == False:
    pm.RegionsOfInterest[ROIS.couch.name].TransformROI3D(Examination=examination, TransformationMatrix=transMat)
