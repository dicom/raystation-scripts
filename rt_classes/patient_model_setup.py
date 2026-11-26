# Import local files:
import patient_model_functions as PMF
import rois as ROIS


class PatientModelSetup(object):
  '''Class for setting up ROIs and POIs in a patient model.'''

  def __init__(self, patient_db, pm, examination, ss, choices, targets, oars):
    '''Configures a patient model in RayStation based on the given RayStation objects and settings.

    In addition to creating OAR and target ROIS, also sets up things like localization point,
    external, body (where needed) and couch.

    Args:
      patient_db (PyScriptObject): The RayStation patient database (PatientDB).
      pm (PyScriptObject): The RayStation PatientModel instance.
      examination (PyScriptObject): The RayStation Examination instance.
      ss (PyScriptObject): The RayStation StructureSet instance.
      choices (list[str]): A list of string choices from a GUI dialogue window.
      targets (list[ROI]): A list of target ROIs to be created in the patient model.
      oars (list[ROI]): A list of OAR ROIs to be created in the patient model.
    '''
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

  def add_targets(self, targets):
    '''Adds target ROIs to the PatientModelSetup.

    Args:
      targets (list[ROI]): A list of target ROIs to be added to the patient model.
    '''
    # Verify input:
    assert isinstance(targets, list), "targets is not a list: %r" % targets
    for target in targets:
      assert target.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "target is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % target
    # Assign targets:
    self.targets.extend(targets)

  def add_oars(self, oars):
    '''Adds OAR ROIs to the PatientModelSetup.

    Args:
      oars (list[ROI]): A list of OAR ROIs to be added to the patient model.
    '''
    # Verify input:
    assert isinstance(oars, list), "oars is not a list: %r" % oars
    for oar in oars:
      assert oar.__class__.__name__ in ['ROI', 'ROIDLS', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "oar is not a ROI (or ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): %r" % oar
    # Assign oars:
    self.oars.extend(oars)

  def create_rois(self):
    '''For all ROIs that are setup in this PatientModelSetup (targets + OARs), creates them in RayStation.'''
    group = self.grouped_rois()
    # Collect DLS ROIs in a list for group creation (because it is much faster than creating DLS ROIs one at a time):
    dls_rois = []
    for key in group:
      for roi in group[key]:
        if roi.__class__.__name__ == 'ROIDLS':
          # We will create the DLS geometry only if the ROI does not exist, or if it exists but has no geometry:
          if not PMF.has_roi(self.pm, roi.name) or self.ss.RoiGeometries[roi.name].PrimaryShape is None:
            dls_rois.append(roi)
    # Create the DLS ROIs:
    if len(dls_rois) > 0:
      PMF.create_dls_rois(self.pm, self.examination, dls_rois)
    # Create non-DLS ROIs (in reverse sorted order):
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

  def grouped_rois(self):
    '''Gives a dictionary where the ROIs (targets and OARs) are sorted
    by derived/underived and source_level (for derived ROIs).

    Returns:
      dict: A Dictionary containing ROIs sorted by source level (ROI algebra dependencies).
    '''
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

  def set_source_level(self, roi, level):
    '''Sets a source level for the given ROI.

    This is used to describe how the ROI depends on other ROIs. A non-derived ROI will have source level 0.
    A ROI which depends on another (underived) ROI (e.g. a ROIAlgebra or ROIExpanded/ROIWall) will have source level 1.

    ROIs which depends on other derived ROIS (which may in turn depend on other derived ROIs), may have higher
    source levels, like 2, 3, 4, etc.

    The source level is ultimately used to determine in which order ROIs are created in RayStation.
    I.e. ROIs need to be created in opposite source level order (0 first, highest number last)
    in order to avoid dependence errors when creating ROIs.

    Args:
      roi (ROI, ROIAlgebra, ROIDLS, ROIExpanded, ROIWall): The ROI for which to determine and set level.
      level (int): The level to set for the ROI.
    '''
    # Verify input:
    assert roi.__class__.__name__ in ['ROI', 'ROIDLS', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "roi is not a ROI (or ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): %r" % roi
    assert isinstance(level, int), "level is not a int: %r" % level
    # Set level:
    if not roi.__class__.__name__ in ['ROI', 'ROIDLS']:
      if level > roi.source_level:
        roi.source_level = level
      if roi.__class__.__name__ == 'ROIAlgebra':
        for roiA in roi.sourcesA:
          self.set_source_level(roiA, level+1)
        for roiB in roi.sourcesB:
          self.set_source_level(roiB, level+1)
      else:
        self.set_source_level(roi.source, level+1)
