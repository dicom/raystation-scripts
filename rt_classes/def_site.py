# encoding: utf8

# Import local files:
import patient_model_functions as PMF
import rois as ROIS


# Site class for ROI definition.
class DefSite(object):

  # Creates a DefSite object.
  # Sets up objects associated with the DefSite:
  # -Patient model
  # -Examination
  # -Structure Set
  # -GUI choices from the Def script
  # -Target ROIs
  # -OARs
  # Additionally creates the following structures:
  # -Localization point
  # -External ROI (and Body ROI for brain treatments)
  # -Couch ROI and positions it in the lateral and AP directions (not long direction as we dont know target volume position yet).
  def __init__(self, patient_db, pm, examination, ss, choices, targets, oars):
    # Verify input:
    assert isinstance(choices, list), "choices is not a list: %r" % choices
    assert isinstance(targets, list), "targets is not a list: %r" % targets
    assert isinstance(oars, list), "oars is not a list: %r" % oars
    # Assign parameters:
    self.patient_db = patient_db
    self.pm = pm
    self.examination = examination
    self.ss = ss
    self.choices = choices
    self.targets = targets
    self.oars = oars
    # Create localization point:
    PMF.create_localization_point(self.pm, self.examination)
    # Handle creation of external and couch ROIs:
    if self.choices[0] == 'brain':
      if self.choices[1] == 'stereotactic':
        # Create external geometry:
        PMF.create_stereotactic_body_geometry(self.pm, self.examination, self.ss)
        PMF.create_stereotactic_external_geometry(self.pm, self.examination, self.ss)
      elif self.choices[1] == 'part':
        # Create external geometry:
        PMF.create_stereotactic_body_geometry(self.pm, self.examination, self.ss)
        PMF.create_stereotactic_external_geometry(self.pm, self.examination, self.ss)
        # Create couch:
        PMF.create_couch(self.patient_db, self.pm, self.ss, self.examination)
        PMF.translate_couch(self.pm, self.ss, self.examination, ROIS.external.name, couch_thickness = 11)
      else:
        # Create external geometry:
        PMF.create_external_geometry(self.pm, self.examination, self.ss)
        # Create couch:
        PMF.create_couch(self.patient_db, self.pm, self.ss, self.examination)
        PMF.translate_couch(self.pm, self.ss, self.examination, ROIS.external.name, couch_thickness = 11)
    else:
      # Create external geometry:
      PMF.create_external_geometry(self.pm, self.examination, self.ss)
      # Create couch:
      PMF.create_couch(self.patient_db, self.pm, self.ss, self.examination)
      PMF.translate_couch(self.pm, self.ss, self.examination, ROIS.external.name)


  # Adds target ROIs to the DefSite.
  def add_targets(self, targets):
    # Verify input:
    assert isinstance(targets, list), "targets is not a list: %r" % targets
    for target in targets:
      assert target.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "target is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % target
    # Assign targets:
    self.targets.extend(targets)


  # Add OARs to the DefSite.
  def add_oars(self, oars):
    # Verify input:
    assert isinstance(oars, list), "oars is not a list: %r" % oars
    for oar in oars:
      assert oar.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "oar is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % oar
    # Assign oars:
    self.oars.extend(oars)


  # Creates all ROIs that are setup in this DefSite (targets + OARs) in RayStation.
  def create_rois(self):
    # Delete pre-existing ROIs (except those which are manually contoured) in sorted order:
    group = self.grouped_rois()
    for key in sorted(iter(group)):
      for roi in group[key]:
        PMF.delete_matching_roi_except_manually_contoured(self.pm, self.ss, roi)
    group = self.grouped_rois()
    # Create ROIs (in reverse sorted order):
    for key in reversed(sorted(iter(group))):
      for roi in group[key]:
        # Only create ROI if it doesn't already exist:
        if not PMF.has_roi(self.pm, roi.name):
          if roi.__class__.__name__ == 'ROI':
            if roi.model:
              PMF.create_model_roi(self.pm, self.examination, roi)
            else:
              PMF.create_empty_roi(self.pm, roi)
          elif roi.__class__.__name__ == 'ROIExpanded':
            PMF.create_expanded_roi(self.pm, self.examination, self.ss, roi)
          elif roi.__class__.__name__ == 'ROIAlgebra':
            PMF.create_algebra_roi(self.pm, self.examination, self.ss, roi)
          elif roi.__class__.__name__ == 'ROIWall':
            PMF.create_wall_roi(self.pm, self.examination, self.ss, roi)


  # Returns a dictionary where the site's ROIs (targets and OARs) are sorted
  # by derived/underived and source_level (for derived ROIs):
  def grouped_rois(self):
    rois = self.oars + self.targets
    # Establish source levels:
    for roi in rois:
      self.set_source_level(roi, 0)
    grouped = {}
    for roi in rois:
      if roi.source_level in grouped:
        grouped[roi.source_level].append(roi)
      else:
        grouped[roi.source_level] = [roi]
    return grouped


  # Sets a source level for the given ROI.
  # This is used to describe how the ROI depends on other ROIs. A non-derived ROI will have source level 0.
  # A ROI which depends on another (underived) ROI (e.g. a ROIAlgebra or ROIExpanded/ROIWall) will have source level 1.
  # ROIs which depends on other derived ROIS (which may in turn depend on other derived ROIs), may have higher
  # source levels, like 2, 3, 4, etc.
  # The source level is ultimately used to determine in which order ROIs are created in RayStation. I.e. ROIs need to
  # be created in opposite source level order (0 first, highest number last) in order to avoid dependence errors when creating ROIs.
  def set_source_level(self, roi, level):
    # Verify input:
    assert roi.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "roi is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % roi
    assert isinstance(level, int), "level is not a int: %r" % level
    # Set level:
    if roi.__class__.__name__ != 'ROI':
      if level > roi.source_level:
        roi.source_level = level
      if roi.__class__.__name__ == 'ROIAlgebra':
        for roiA in roi.sourcesA:
          self.set_source_level(roiA, level+1)
        for roiB in roi.sourcesB:
          self.set_source_level(roiB, level+1)
      else:
        self.set_source_level(roi.source, level+1)
