# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import roi_functions as RF
import rois as ROIS


class DefBladder(object):
  """Configuration of ROIs used for cases of bladder cancer."""

  def __init__(self, patient, pm, ss, choices, pm_setup):
    """Initializes the bladder case configuration with the relevant RayStation instances and the user's GUI selections.

    Based on the settings given, a set of ROIs (Targets, OARs & Others) are created on the patient case in RayStation.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
      pm (PyScriptObject): The RayStation PatientModel instance.
      ss (PyScriptObject): The RayStation StructureSet instance.
      choices (list): The choices made by the user in the definitions script GUI.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, pm_setup)
    # Add ROIs based on gender:
    self.add_gender_based_rois(patient, pm, pm_setup)
    # Choice 1: Intent
    intent = choices[1]
    if intent == 'palliative':
      self.add_palliative_targets(pm, pm_setup)
    else:
      self.add_curative_targets(pm, pm_setup)
    # Create all targets and OARs in RayStation:
    pm_setup.create_rois()
    # Change type to "Other":
    RF.set_organ_type(pm.RegionsOfInterest['Bone'], "Other")
    RF.set_organ_type(pm.RegionsOfInterest['BowelBag_Draft'], "Other")
    # Exclude some ROIs from export:
    exclude = ["L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "Femur_L", "Femur_R"]
    for roi_name in exclude:
      PMF.exclude_roi_from_export(pm, roi_name)


  def add_common_rois(self, pm, pm_setup):
    """Adds ROIs for this particular treatment site that are common across all scopes.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Create "Bone" ROI Algebra:
    pelvic_bone_rois = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_l, ROIS.femur_r]
    vertebrae_rois = [ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = pelvic_bone_rois, sourcesB = vertebrae_rois)
    pm_setup.add_oars([ROIS.anal_canal, ROIS.bladder, bone, ROIS.bowel_bag_draft, ROIS.bowel_bag,
      ROIS.cauda_equina, ROIS.coccyx, ROIS.l5, ROIS.femoral_head_l, ROIS.femoral_head_r, ROIS.femur_l,
      ROIS.femur_r, ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.rectum, ROIS.sacrum
    ])


  def add_curative_targets(self, pm, pm_setup):
    """Adds target ROIs for curative treatment.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    ctv_p = ROI.ROIExpanded(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv,
      source = ROIS.gtv_p, margins = MARGINS.uniform_5mm_expansion
    )
    ctv_e = ROI.ROIExpanded(ROIS.ctv_e.name, ROIS.ctv_e.type, COLORS.ctv, source = ROIS.bladder, margins = MARGINS.zero)
    ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv,
      sourcesA=[ctv_p], sourcesB=[ctv_e], marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color,
      sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ROIS.gtv_p, ctv_p, ctv_e, ctv, ptv])


  def add_gender_based_rois(self, patient, pm, pm_setup):
    """Adds ROIs for this particular treatment site that are dependent on the patient's gender.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    if patient.Gender == 'Female':
      pm_setup.add_oars([ROIS.uterus])
    elif patient.Gender == 'Male':
      pm_setup.add_oars([ROIS.penile_bulb])


  def add_palliative_targets(self, pm, pm_setup):
    """Adds target ROIs for palliative treatment.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color,
      sourcesA = [ROIS.ctv_underived], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.bladder_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ROIS.ctv_underived, ptv])
