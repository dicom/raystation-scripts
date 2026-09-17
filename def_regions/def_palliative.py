# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import roi_functions as RF
import rois as ROIS


class DefPalliative(object):
  """Configuration of ROIs used for palliative cases."""

  def __init__(self, pm, ss, choices, pm_setup):
    """Initializes the palliative case configuration with the relevant RayStation instances
    and the user's GUI selections.

    Based on the settings given, a set of ROIs (Targets, OARs & Others) are created on the patient case in RayStation.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      ss (PyScriptObject): The RayStation StructureSet instance.
      choices (list): The choices made by the user in the definitions script GUI.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Choice 1: Stereotactic or not?
    stereotactic = choices[1]
    # Choice 2: Region
    region = choices[2]
    nr_targets = None
    with_gtv = None
    mask = None
    if stereotactic == 'no':
      # Choice 3: Number of targets:
      nr_targets = int(choices[3])
      # Choice 4: GTV included?
      with_gtv = choices[4]
      if region == 'neck':
        # Choice 5: Mask fixation or not?
        mask = choices[5]
    # Adds organ at risk ROIs:
    self.add_oars(pm, pm_setup, stereotactic, region)
    # Set up target volumes:
    self.add_targets(pm, pm_setup, stereotactic, region, nr_targets, with_gtv, mask)
    # Add bone union ROI:
    bone = self.add_bone(pm, pm_setup)
    # Create all targets and OARs in RayStation:
    pm_setup.create_rois()
    # Change type to "Other":
    if bone:
      RF.set_organ_type(pm.RegionsOfInterest[bone.name], "Other")
    try:
      if pm.RegionsOfInterest['BowelBag_Draft']:
        pm.RegionsOfInterest['BowelBag_Draft'].OrganData.OrganType = "Other"
    except:
      pass
    # Exclude some ROIs from export:
    if bone:
      exclude = bone.sourcesA + bone.sourcesB
      for roi in exclude:
        PMF.exclude_roi_from_export(pm, roi.name)


  def add_bone(self, pm, pm_setup):
    """Adds a bone union ROI.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.

    Returns:
      ROIAlgebra: The bone union ROI.
    """
    bone = None
    bone_rois = []
    vertebrae_rois = []
    # Create "Bone" ROI Algebra:
    bone_candidates = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_l, ROIS.femur_r]
    vertebrae_candidatates = [ROIS.l2, ROIS.l3, ROIS.l4, ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    for roi in bone_candidates:
      if roi in pm_setup.oars:
        bone_rois.insert(0, roi)
    for roi in vertebrae_candidatates:
      if roi in pm_setup.oars:
        vertebrae_rois.insert(0, roi)
    if len(bone_rois) > 0 and len(vertebrae_rois) > 0:
      bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = bone_rois, sourcesB = vertebrae_rois)
      pm_setup.add_oars([bone])
    return bone


  def add_oars(self, pm, pm_setup, stereotactic, region):
    """Adds OARs relevant to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      stereotactic (str): A string indicating SBRT ('yes') or conventional ('no').
      region (str): A string indicating body part (e.g. 'abdomen').
    """
    if stereotactic == 'yes':
      # Stereotactic:
      if region in ['col cervical', 'col thorax', 'col pelvis']:
        if region == 'col cervical':
          self.add_oars_neck(pm, pm_setup)
          # SBRT specific OARs:
          pm_setup.add_oars([ROIS.skin, ROIS.spinal_cord, ROIS.spinal_cord_prv])
        elif region == 'col thorax':
          self.add_oars_thorax(pm, pm_setup)
          # SBRT specific OARs:
          pm_setup.add_oars([ROIS.skin, ROIS.spinal_cord, ROIS.spinal_cord_prv])
        elif region == 'col pelvis':
          self.add_oars_pelvis(pm, pm_setup)
          # SBRT specific OARs:
          pm_setup.add_oars([ROIS.bowel_small, ROIS.colon, ROIS.skin, ROIS.spinal_cord, ROIS.spinal_cord_prv])
      else:
        # Non-columna SBRT (assumed pelvis):
        self.add_oars_pelvis(pm, pm_setup)
        # SBRT specific OARs:
        pm_setup.add_oars([ROIS.bowel_small, ROIS.colon, ROIS.skin])
    else:
      # Non-stereotactic:
      # Region:
      if region == 'head':
        self.add_oars_head(pm, pm_setup)
      elif region == 'neck':
        self.add_oars_neck(pm, pm_setup)
      elif region == 'thorax':
        self.add_oars_thorax(pm, pm_setup)
      elif region == 'costa':
        self.add_oars_thorax_abdomen(pm, pm_setup)
      elif region == 'thorax_abdomen':
        self.add_oars_thorax_abdomen(pm, pm_setup)
      elif region == 'abdomen':
        self.add_oars_abdomen(pm, pm_setup)
      elif region == 'abdomen_pelvis':
        self.add_oars_abdomen_pelvis(pm, pm_setup)
      elif region == 'pelvis':
        self.add_oars_pelvis(pm, pm_setup)


  def add_oars_abdomen(self, pm, pm_setup):
    """Adds abdomen OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.a_descending_aorta, ROIS.bowel_bag_draft, ROIS.heart,
      ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.lung_l, ROIS.lung_r, ROIS.pancreas,
      ROIS.spinal_canal, ROIS.spleen, ROIS.stomach, ROIS.v_inferior_vena_cava
    ])
    # Exclude abdominal organs from BowelBag (and remove Bladder reference as it is not relevant here):
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pancreas, ROIS.spleen, ROIS.stomach])
    ROIS.bowel_bag.sourcesB.remove(ROIS.bladder)
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.bowel_bag, ROIS.kidneys, ROIS.lungs])


  def add_oars_abdomen_pelvis(self, pm, pm_setup):
    """Adds abdomen/pelvis OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.a_descending_aorta, ROIS.anal_canal, ROIS.bladder, ROIS.bowel_bag_draft,
      ROIS.cauda_equina, ROIS.coccyx, ROIS.femoral_head_l, ROIS.femoral_head_r, ROIS.femur_l, ROIS.femur_r,
      ROIS.kidney_l, ROIS.kidney_r, ROIS.l2, ROIS.l3, ROIS.l4, ROIS.l5, ROIS.liver, ROIS.pancreas,
      ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.rectum, ROIS.sacrum, ROIS.spinal_canal,
      ROIS.spleen, ROIS.stomach, ROIS.v_inferior_vena_cava
    ])
    # Exclude abdominal organs from BowelBag:
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pancreas, ROIS.spleen, ROIS.stomach])
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.bowel_bag, ROIS.kidneys])


  def add_oars_head(self, pm, pm_setup):
    """Adds head OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.brain, ROIS.brainstem, ROIS.cochlea_l, ROIS.cochlea_r, ROIS.eye_l, ROIS.eye_r,
      ROIS.lacrimal_l, ROIS.lacrimal_r, ROIS.lens_l, ROIS.lens_r, ROIS.mandible, ROIS.optic_chiasm,
      ROIS.optic_nerve_l, ROIS.optic_nerve_r, ROIS.oral_cavity, ROIS.parotid_l, ROIS.parotid_r, ROIS.pituitary,
      ROIS.spinal_canal, ROIS.submand_l, ROIS.submand_r
    ])
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.parotids, ROIS.submands])


  def add_oars_neck(self, pm, pm_setup):
    """Adds neck OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.brachial_plexus_l, ROIS.brachial_plexus_r, ROIS.brain, ROIS.brainstem,
      ROIS.cricopharyngeus, ROIS.esophagus, ROIS.larynx_glottis, ROIS.larynx_supraglottis, ROIS.mandible,
      ROIS.optic_chiasm, ROIS.optic_nerve_l, ROIS.optic_nerve_r, ROIS.oral_cavity, ROIS.parotid_l, ROIS.parotid_r,
      ROIS.pituitary, ROIS.spinal_canal, ROIS.submand_l, ROIS.submand_r, ROIS.thyroid, ROIS.trachea
    ])
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.parotids, ROIS.submands])


  def add_oars_pelvis(self, pm, pm_setup):
    """Adds pelvic OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.bladder, ROIS.anal_canal, ROIS.bowel_bag_draft, ROIS.cauda_equina, ROIS.coccyx,
      ROIS.femoral_head_l, ROIS.femoral_head_r, ROIS.femur_l, ROIS.femur_r, ROIS.kidney_l, ROIS.kidney_r,
      ROIS.l2, ROIS.l3, ROIS.l4, ROIS.l5, ROIS.liver, ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r,
      ROIS.rectum, ROIS.sacrum
    ])
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.kidneys, ROIS.bowel_bag])


  def add_oars_thorax(self, pm, pm_setup):
    """Adds thorax OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.a_aortic_arch, ROIS.a_ascending_aorta, ROIS.a_descending_aorta, ROIS.a_lad,
      ROIS.bronchus_main_l, ROIS.bronchus_main_r, ROIS.bronchus_intermedius, ROIS.carina, ROIS.esophagus,
      ROIS.heart, ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.lung_l, ROIS.lung_r, ROIS.pancreas,
      ROIS.spinal_canal, ROIS.spleen, ROIS.stomach, ROIS.thyroid, ROIS.trachea,
      ROIS.v_inferior_vena_cava, ROIS.v_superior_vena_cava
    ])
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.greatves, ROIS.kidneys, ROIS.lungs])


  def add_oars_thorax_abdomen(self, pm, pm_setup):
    """Adds thorax/abdomen OARs to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.a_aortic_arch, ROIS.a_ascending_aorta, ROIS.a_descending_aorta, ROIS.a_lad,
      ROIS.bowel_bag_draft, ROIS.esophagus, ROIS.heart, ROIS.kidney_l, ROIS.kidney_r, ROIS.liver,
      ROIS.lung_l, ROIS.lung_r, ROIS.pancreas, ROIS.spinal_canal, ROIS.spleen, ROIS.stomach,
      ROIS.trachea, ROIS.v_inferior_vena_cava, ROIS.v_superior_vena_cava
    ])
    # Exclude abdominal organs from BowelBag (and remove Bladder reference as it is not relevant here):
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pancreas, ROIS.spleen, ROIS.stomach])
    ROIS.bowel_bag.sourcesB.remove(ROIS.bladder)
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.bowel_bag, ROIS.greatves, ROIS.kidneys, ROIS.lungs])


  def add_targets(self, pm, pm_setup, stereotactic, region, nr_targets, with_gtv, mask):
    """Adds target ROIs relevant to the treatment site.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      stereotactic (str): A string indicating SBRT ('yes') or conventional ('no').
      region (str): A string indicating body part (e.g. 'abdomen').
      nr_targets (int): The number of targets to setup.
      with_gtv (str): A string indicating whether to setup a GTV ('with') or not.
      mask (str): A string indicating presence of mask fixation ('mask') - used for PTV margin determination.
    """
    # Determine PTV margins:
    ptv_margin = self.determine_ptv_margin(stereotactic, region, with_gtv, mask)
    if stereotactic == 'yes':
      # Stereotactic:
      if region in ['col cervical', 'col thorax', 'col pelvis']:
        # Targets:
        ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_med, ROIS.gtv,
          margins = MARGINS.uniform_3mm_expansion
        )
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB=[ROIS.vb],
          operator='Union', marginsA = ptv_margin, marginsB = ptv_margin
        )
        ptv_gtv = ROI.ROIAlgebra(ROIS.ptv_gtv.name, ROIS.ptv_gtv.type, COLORS.ptv_med,
          sourcesA = [ptv], sourcesB = [ROIS.gtv], operator='Subtraction'
        )
        ptv_spinal = ROI.ROIAlgebra(ROIS.ptv_spinal.name, ROIS.ptv_spinal.type, COLORS.ptv_med,
          sourcesA = [ptv], sourcesB = [ROIS.spinal_cord_prv], operator='Subtraction',
          marginsA = MARGINS.zero, marginsB = MARGINS.uniform_1mm_expansion
        )
        pm_setup.add_targets([ROIS.gtv, ROIS.vb, ptv_gtv, ptv_spinal, ctv, ptv])
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        pm_setup.add_oars([ROIS.spinal_cord_prv, wall_ptv])
      else:
        # Non-columna SBRT:
        # Targets:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, ROIS.gtv, margins = ptv_margin)
        pm_setup.add_targets([ROIS.gtv, ptv])
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        pm_setup.add_oars([wall_ptv])
    else:
      # Conventional RT:
      if nr_targets == 1:
        # A single target:
        if with_gtv == 'with':
          ctv = ROIS.ctv_ext
          pm_setup.add_targets([ROIS.gtv, ctv])
        else:
          ctv = ROIS.ctv_underived
          pm_setup.add_targets([ctv])
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color,
          sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection',
          marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction
        )
        pm_setup.add_targets([ptv])
      else:
        # Multiple targets (2 or 3):
        gtvs = []
        ctvs = []
        ptvs = []
        if with_gtv=='with':
          # With GTV:
          for i in range(0, nr_targets):
            gtvs.append(ROI.ROI('GTV'+str(i+1), 'Gtv', COLORS.gtv))
            ctvs.append(ROI.ROIAlgebra(ROIS.ctv.name+str(i+1), ROIS.ctv1.type, ROIS.ctv.color,
              sourcesA = [gtvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection',
              marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction)
            )
            ptvs.append(ROI.ROIAlgebra(ROIS.ptv.name+str(i+1), ROIS.ptv1.type, ROIS.ptv.color,
              sourcesA = [ctvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection',
              marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction)
            )
          # GTV union target volume:
          gtvs.append(ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color,
            sourcesA=[gtvs[0]], sourcesB=gtvs[1:])
          )
          pm_setup.add_targets(gtvs)
        else:
          # Without GTV:
          for i in range(0, nr_targets):
            ctvs.append(ROI.ROI('CTV'+str(i+1), 'Ctv', COLORS.ctv))
            ptvs.append(ROI.ROIAlgebra(ROIS.ptv.name+str(i+1), ROIS.ptv.type, ROIS.ptv.color,
              sourcesA = [ctvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection',
              marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction)
            )
        # Union target volumes:
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ctvs[0]], sourcesB=ctvs[1:])
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptvs[0]], sourcesB=ptvs[1:])
        ctvs.append(ctv)
        ptvs.append(ptv)
        pm_setup.add_targets(ctvs + ptvs)
      # Add PTV wall:
      wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
      pm_setup.add_oars([wall_ptv])


  def determine_ptv_margin(self, stereotactic, region, with_gtv, mask):
    """Determines the PTV margin to use for this treatment site.

    Args:
      stereotactic (str): A string indicating SBRT ('yes') or conventional ('no').
      region (str): A string indicating body part (e.g. 'abdomen').
      with_gtv (str): A string indicating whether to setup a GTV ('with') or not.
      mask (str): A string indicating presence of mask fixation ('mask') - used for PTV margin determination.

    Returns:
      Expansion: The PTV margin determined to be appropriate for the given treatment site.
    """
    ptv_margin = None
    if stereotactic == 'yes':
      if region in ['col cervical', 'col thorax']:
        ptv_margin = MARGINS.uniform_2mm_expansion
      else:
        ptv_margin = MARGINS.uniform_3mm_expansion
    else:
      # Conventional RT:
      if with_gtv == 'with':
        # Soft tissue target:
        if region in ['head']:
          # Head: 3 mm
          ptv_margin = MARGINS.uniform_3mm_expansion
        elif region in ['neck']:
          # Neck: 3 mm (mask) or 5 mm (no mask)
          if mask == 'mask':
            ptv_margin = MARGINS.uniform_3mm_expansion
          else:
            ptv_margin = MARGINS.uniform_5mm_expansion
        elif region in ['thorax_abdomen']:
          # Near lung (affected by breathing motion):
          ptv_margin = MARGINS.abdomen_near_lung_soft_tissue_expansion
        else:
          # All others: 7 mm
          ptv_margin = MARGINS.uniform_7mm_expansion
      else:
        # Bone target:
        if region in ['head']:
          # Head: 3 mm
          ptv_margin = MARGINS.uniform_3mm_expansion
        elif region in ['neck']:
          # Neck: 3 mm (mask) or 5 mm (no mask)
          if mask == 'mask':
            ptv_margin = MARGINS.uniform_3mm_expansion
          else:
            ptv_margin = MARGINS.uniform_5mm_expansion
        elif region in ['costa', 'other']:
          # Costa/Extremities: 7 mm
          ptv_margin = MARGINS.uniform_7mm_expansion
        else:
          # Other torso: 5 mm
          ptv_margin = MARGINS.uniform_5mm_expansion
    return ptv_margin
