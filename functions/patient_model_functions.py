# encoding: utf8
from __future__ import division
from tkinter import *
from tkinter import messagebox

# Import local files:
import roi as ROI
import rois as ROIS
import colors as COLORS
import gui_functions as GUIF
import structure_set_functions as SSF


# Returns True if a ROI with type 'Bolus' exists in this patient model (and False if not).
def bolus(pm):
  match = False
  for roi in pm.RegionsOfInterest:
    if roi.Type == 'Bolus':
      match = True
  return match


# Returns a list with the names of all ROIs of type 'Bolus' which exists in this patient model (and an empty list if none).
def bolus_names(pm):
  match = []
  for roi in pm.RegionsOfInterest:
    if roi.Type == 'Bolus':
      match.append(roi.Name)
  return match


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


# Creates a couch (support) ROI from a couch template.
def create_couch(patient_db, pm, examination):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == "Couch":
      pm_roi.DeleteRoi()
      break
  templateInfo = patient_db.GetPatientModelTemplateInfo()
  for i in range(0, len(templateInfo)):
    template = patient_db.LoadTemplatePatientModel(templateName = templateInfo[i]['Name'], lockMode = 'Read')
    if template.Name == 'Bordtopp tykk':
      pm.CreateStructuresFromTemplate(
        SourceTemplate=template, 
        SourceExaminationName= "CT 1",
        SourceRoiNames=[ROIS.couch.name],
        SourcePoiNames=[],
        AssociateStructuresByName=False,
        TargetExamination=examination,
        InitializationOption="AlignImageCenters"
      )

# Creates an empty ROI from a ROI object.
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


# Creates an external ROI.
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
  except:
    try:
      pm.MBSAutoInitializer(
        MbsRois=[{'CaseType': roi.case, 'ModelName': roi.model, 'RoiName': roi.name, 'RoiColor': roi.color}],
        CreateNewRois=True, Examination=examination, UseAtlasBasedInitialization=False
      )
    except SystemError:
      # Display a message to the user:
      GUIF.handle_failed_model_based_segmentation(roi.name)


# Creates a ROI which is the posterior half of the source ROI in all slices.
# Note that this function is somewhat slow, since it has to create a new ROI for every slice.
def create_posterior_half(pm, examination, ss, source_roi, roi):
  if SSF.has_named_roi_with_contours(ss, source_roi.name):
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
  else:
    GUIF.handle_missing_roi_for_derived_rois(roi.name, source_roi.name)


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
    if not SSF.is_approved_roi_structure(ss, roi.name):
      if is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi.name):
        intersection = ROI.ROIAlgebra(roi.name+"1", roi.type, roi.color, sourcesA = [source_roi], sourcesB = [ROIS.box], operator = 'Intersection')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        create_algebra_roi(pm, examination, ss, intersection)
        GUIF.handle_creation_of_new_roi_because_of_approved_structure_set(intersection.name)
      else:
        intersection = ROI.ROIAlgebra(roi.name, roi.type, roi.color, sourcesA = [source_roi], sourcesB = [ROIS.box], operator = 'Intersection')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        create_algebra_roi(pm, examination, ss, intersection)
    delete_roi(pm, ROIS.box.name)
  else:
    GUIF.handle_missing_roi_for_derived_rois(roi.name, source_roi.name)


# Creates a grey value theshold ROI (grei_level_roi), which is intersected with source_roi. The end result is intersect_roi.
# grei_level_roi is only used temporary and is deleted after use. If unsuccessful, the intersect_roi is also deleted.
def create_grey_value_intersection_roi(pm, examination, ss, grey_level_roi, source_roi, intersection_roi, low_threshold, high_threshold):
  # If the grey level threshold ROI already exists, delete it and re-create an empty ROI:
  delete_roi(pm, grey_level_roi.name)
  pm.CreateRoi(Name = grey_level_roi.name, Type = grey_level_roi.type, Color = grey_level_roi.color)
  ss.RoiGeometries[grey_level_roi.name].OfRoi.GrayLevelThreshold(Examination = examination, LowThreshold = low_threshold, HighThreshold = high_threshold)
  # Create the intersection ROI:
  if not SSF.is_approved_roi_structure(ss, intersection_roi.name):
    if is_approved_roi_structure_in_one_of_all_structure_sets(pm, intersection_roi.name):
      intersection = ROI.ROIAlgebra(intersection_roi.name+"1", intersection_roi.type, intersection_roi.color, sourcesA = [source_roi], sourcesB = [grey_level_roi], operator = 'Intersection')
      create_algebra_roi(pm, examination, ss, intersection)
    else:
      delete_roi(pm, intersection_roi.name)
      intersection = ROI.ROIAlgebra(intersection_roi.name, intersection_roi.type, intersection_roi.color, sourcesA = [source_roi], sourcesB = [grey_level_roi], operator = 'Intersection')
      create_algebra_roi(pm, examination, ss, intersection)
  # Clean up: Delete the threshold ROI which was created:
  if ss.RoiGeometries[grey_level_roi.name]:
    delete_roi(pm, grey_level_roi.name)
  # In case of failure (no volume or volume < 0.1 cm^3), delete the intersection ROI:
  if ss.RoiGeometries[intersection_roi.name].HasContours():
    if ss.RoiGeometries[intersection_roi.name].GetRoiVolume() < 0.1:
      delete_roi(pm, intersection_roi.name)
  else:
    delete_roi(pm, intersection_roi.name)

# Creates Retina and Cornea ROIs (based on an Eye ROI).
def create_retina_and_cornea(pm, examination, ss, source_roi, box_roi, roi, intersection_roi, subtraction_roi):
  if SSF.has_named_roi_with_contours(ss, source_roi.name):
    center_x = SSF.roi_center_x(ss, source_roi.name)
    center_z = SSF.roi_center_z(ss, source_roi.name)
    source_roi_box = ss.RoiGeometries[source_roi.name].GetBoundingBox()
    y_min = source_roi_box[1].y
    if y_min > 0:
      y_min = -source_roi_box[1].y
    delete_roi(pm, box_roi.name)
    box = pm.CreateRoi(Name = box_roi.name, Color = box_roi.color, Type = box_roi.type)
    pm.RegionsOfInterest[box_roi.name].CreateBoxGeometry(Size={ 'x': 5, 'y': 5, 'z': 4}, Examination = examination, Center = { 'x': center_x, 'y': y_min+2.5, 'z': center_z })
    exclude_roi_from_export(pm, box_roi.name)
    if source_roi.name == ROIS.lens_l.name:
      wall_roi = ROIS.z_eye_l
    elif source_roi.name == ROIS.lens_r.name:
      wall_roi = ROIS.z_eye_r
    delete_roi(pm, wall_roi.name)
    create_wall_roi(pm, examination, ss, wall_roi)
    exclude_roi_from_export(pm, wall_roi.name)
    if not SSF.is_approved_roi_structure(ss, roi.name):
      if is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi.name):
        intersection = ROI.ROIAlgebra(roi.name+"1", roi.type, roi.color, sourcesA = [source_roi], sourcesB = [box_roi], operator = 'Intersection')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        create_algebra_roi(pm, examination, ss, intersection)
        GUIF.handle_creation_of_new_roi_because_of_approved_structure_set(intersection.name)
      else:
        intersection = ROI.ROIAlgebra(intersection_roi.name, intersection_roi.type, intersection_roi.color, sourcesA = [wall_roi], sourcesB = [box_roi], operator = 'Intersection')
        subtraction = ROI.ROIAlgebra(subtraction_roi.name, subtraction_roi.type, subtraction_roi.color, sourcesA = [wall_roi], sourcesB = [box_roi], operator = 'Subtraction')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        delete_roi(pm, subtraction.name)
        create_algebra_roi(pm, examination, ss, intersection)
        create_algebra_roi(pm, examination, ss, subtraction)
  else:
    GUIF.handle_missing_roi_for_derived_rois(intersection_roi.name, source_roi.name)


# Creates a Retina ROI (based on an Eye ROI).
def create_retina(pm, examination, ss, source_roi, box_roi, roi, intersection_roi):
  if SSF.has_named_roi_with_contours(ss, source_roi.name):
    center_x = SSF.roi_center_x(ss, source_roi.name)
    center_z = SSF.roi_center_z(ss, source_roi.name)
    source_roi_box = ss.RoiGeometries[source_roi.name].GetBoundingBox()
    y_min = source_roi_box[1].y
    if y_min > 0:
      y_min = -source_roi_box[1].y
    delete_roi(pm, box_roi.name)
    box = pm.CreateRoi(Name = box_roi.name, Color = box_roi.color, Type = box_roi.type)
    pm.RegionsOfInterest[box_roi.name].CreateBoxGeometry(Size={ 'x': 5, 'y': 5, 'z': 4}, Examination = examination, Center = { 'x': center_x, 'y': y_min+2.5, 'z': center_z })
    exclude_roi_from_export(pm, box_roi.name)
    if source_roi.name == ROIS.lens_l.name:
      wall_roi = ROIS.z_eye_l
    elif source_roi.name == ROIS.lens_r.name:
      wall_roi = ROIS.z_eye_r
    delete_roi(pm, wall_roi.name)
    create_wall_roi(pm, examination, ss, wall_roi)
    exclude_roi_from_export(pm, wall_roi.name)
    if not SSF.is_approved_roi_structure(ss, roi.name):
      if is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi.name):
        intersection = ROI.ROIAlgebra(roi.name+"1", roi.type, roi.color, sourcesA = [source_roi], sourcesB = [box_roi], operator = 'Intersection')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        create_algebra_roi(pm, examination, ss, intersection)
        GUIF.handle_creation_of_new_roi_because_of_approved_structure_set(intersection.name)
      else:
        intersection = ROI.ROIAlgebra(intersection_roi.name, intersection_roi.type, intersection_roi.color, sourcesA = [wall_roi], sourcesB = [box_roi], operator = 'Intersection')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        create_algebra_roi(pm, examination, ss, intersection)
  else:
    GUIF.handle_missing_roi_for_derived_rois(intersection_roi.name, source_roi.name)


# Creates a Cornea ROI (based on an Eye ROI).
def create_cornea(pm, examination, ss, source_roi, box_roi, roi, subtraction_roi):
  if SSF.has_named_roi_with_contours(ss, source_roi.name):
    center_x = SSF.roi_center_x(ss, source_roi.name)
    center_z = SSF.roi_center_z(ss, source_roi.name)
    source_roi_box = ss.RoiGeometries[source_roi.name].GetBoundingBox()
    y_min = source_roi_box[1].y
    if y_min > 0:
      y_min = -source_roi_box[1].y
    delete_roi(pm, box_roi.name)
    box = pm.CreateRoi(Name = box_roi.name, Color = box_roi.color, Type = box_roi.type)
    pm.RegionsOfInterest[box_roi.name].CreateBoxGeometry(Size={ 'x': 5, 'y': 5, 'z': 4}, Examination = examination, Center = { 'x': center_x, 'y': y_min+2.5, 'z': center_z })
    exclude_roi_from_export(pm, box_roi.name)
    if source_roi.name == ROIS.lens_l.name:
      wall_roi = ROIS.z_eye_l
    elif source_roi.name == ROIS.lens_r.name:
      wall_roi = ROIS.z_eye_r
    delete_roi(pm, wall_roi.name)
    create_wall_roi(pm, examination, ss, wall_roi)
    exclude_roi_from_export(pm, wall_roi.name)
    if not SSF.is_approved_roi_structure(ss, roi.name):
      if is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi.name):
        intersection = ROI.ROIAlgebra(roi.name+"1", roi.type, roi.color, sourcesA = [source_roi], sourcesB = [box_roi], operator = 'Intersection')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, intersection.name)
        create_algebra_roi(pm, examination, ss, intersection)
        GUIF.handle_creation_of_new_roi_because_of_approved_structure_set(intersection.name)
      else:
        subtraction = ROI.ROIAlgebra(subtraction_roi.name, subtraction_roi.type, subtraction_roi.color, sourcesA = [wall_roi], sourcesB = [box_roi], operator = 'Subtraction')
        # In the rare case that this ROI already exists, delete it (to avoid a crash):
        delete_roi(pm, subtraction.name)
        create_algebra_roi(pm, examination, ss, subtraction)
  else:
    GUIF.handle_missing_roi_for_derived_rois(subtraction_roi.name, source_roi.name)

 
# Checks if a given ROI takes part in an approved structure set.
def is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi_name):
  match = False
  for set in pm.StructureSets:
    for app_set in set.ApprovedStructureSets:
      for roi in app_set.ApprovedRoiStructures:
        if roi.OfRoi.Name == roi_name:
          match = True
  return match  


# As there can only be one External ROI, another "External" is created for brain stereotactic treatments,
# called 'Body', where only the patient geometry is included (Fixation equipment is excluded).
# This Body ROI is the same as the normal 'External' for other patient groups.
def create_stereotactic_body_geometry(pm, examination, ss):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == ROIS.body.name:
      pm_roi.DeleteRoi()
      break
  pm.CreateRoi(Name = ROIS.body.name, Color = ROIS.body.color, Type = ROIS.body.type)
  ss.RoiGeometries[ROIS.body.name].OfRoi.CreateExternalGeometry(Examination = examination, ThresholdLevel = None)


# Creates an external ROI used for brain stereotactic treatments where fixation and mask is included in the ROI.
def create_stereotactic_external_geometry(pm, examination, ss):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == ROIS.external.name:
      pm_roi.DeleteRoi()
      break
  pm.CreateRoi(Name = ROIS.external.name, Color = ROIS.external.color, Type = ROIS.external.type)
  ss.RoiGeometries[ROIS.external.name].OfRoi.CreateExternalGeometry(Examination = examination, ThresholdLevel = -980)


# Creates a wall ROI from a ROI object.
def create_wall_roi(pm, examination, ss, roi):
  pm.CreateRoi(Name=roi.name, Color=roi.color, Type=roi.type)
  roi_geometry = SSF.rg(ss, roi.name)
  # Make sure that the source ROI exists:
  if SSF.has_roi(ss, roi.source.name):
    roi_geometry.OfRoi.SetWallExpression(SourceRoiName=roi.source.name, OutwardDistance=roi.outward_dist, InwardDistance=roi.inward_dist)
    roi_geometry.OfRoi.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")
  else:
    GUIF.handle_missing_roi_for_derived_rois(roi.name, [roi.source.name])


# Deletes all ROIs from the patient model.
def delete_all_rois(pm):
  rois = pm.RegionsOfInterest
  for i in reversed(range(len(rois))):
    rois[i].DeleteRoi()

# Delete any ROIs in the patient model which matches the given list of ROIs.
def delete_matching_rois(pm, rois):
  delete_list = []
  for pm_roi in pm.RegionsOfInterest:
    for roi in rois:
      if pm_roi.Name == roi.name:
        delete_list.append(pm_roi.Name)
  for roi_name in delete_list:
    pm.RegionsOfInterest[roi_name].DeleteRoi()


# Delete any ROIs which already exists, except those which are manually contoured.
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


# Exclude 'Undefined' ROIs from the export.
def exclude_rois_from_export(pm):
  exclude_list = []
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Type == 'Undefined':
      if not pm_roi.ExcludeFromExport:
        exclude_list.append(pm_roi.Name)
  if len(exclude_list) > 0:
    pm.ToggleExcludeFromExport(ExcludeFromExport = True, RegionOfInterests=exclude_list, PointsOfInterests=[])


# Exclude the given ROI from from the export.
def exclude_roi_from_export(pm, roi_name):
  for pm_roi in pm.RegionsOfInterest:
    if pm_roi.Name == roi_name:
      if not pm_roi.ExcludeFromExport:
        pm.ToggleExcludeFromExport(ExcludeFromExport = True, RegionOfInterests=[roi_name], PointsOfInterests=[])


# Delete the given ROI (specified by name) from the patient model.
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
