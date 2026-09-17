# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS


class DefProstate(object):
  """Configuration of ROIs used for cases of prostate cancer."""

  def __init__(self, pm, ss, choices, pm_setup):
    """Initializes the prostate case configuration with the relevant RayStation instances and the user's GUI selections.

    Based on the settings given, a set of ROIs (Targets, OARs & Others) are created on the patient case in RayStation.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      ss (PyScriptObject): The RayStation StructureSet instance.
      choices (list): The choices made by the user in the definitions script GUI.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Choice 1: Region - prostate or bed?
    region = choices[1]
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, pm_setup, region)
    # Setup targets and site specific ROIs:
    if region == 'prostate':
      self.setup_prostate(pm, pm_setup, choices)
    else:
      self.setup_bed(pm, pm_setup, choices)
    # Create "Bone" ROI Algebra:
    pelvic_bone_rois = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_l, ROIS.femur_r]
    vertebrae_rois = [ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    # Add L3 and L4 to bone roi if relevant (for lymph node irradiation):
    for roi in [ROIS.l4, ROIS.l3]:
      try:
        if roi in pm_setup.oars:
          vertebrae_rois.insert(0, roi)
      except:
        pass
    bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = pelvic_bone_rois, sourcesB = vertebrae_rois)
    pm_setup.add_oars([bone])
    # Create all targets and OARs in RayStation:
    pm_setup.create_rois()
    # Change type to 'Other' for selected ROIs:
    for roi_name in ['Prostate', 'SeminalVes', 'LN_Iliac', 'Bladder_Draft', 'BowelBag_Draft', bone.name]:
      try:
        if pm.RegionsOfInterest[roi_name]:
          if pm.RegionsOfInterest[roi_name].OrganData.OrganType != "Other":
            pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      except:
        pass
    # Override density for arteries (for cases where IV contrast is used - which is cases with a GTVn):
    iv_contrast = None
    try:
      if pm.RegionsOfInterest['GTVn']:
        iv_contrast = True
    except:
      pass
    if iv_contrast:
      water = None
      for material in pm.Materials:
        if material.Name == 'Water':
          water = material
          break
      if water:
        for roi in [ROIS.a_descending_aorta, ROIS.a_common_iliac_l, ROIS.a_common_iliac_r,
          ROIS.a_internal_iliac_l, ROIS.a_internal_iliac_r, ROIS.a_external_iliac_l, ROIS.a_external_iliac_r
        ]:
          pm.RegionsOfInterest[roi.name].SetRoiMaterial(Material=water)
    # Override density for gold seeds (if present):
    gold = None
    for material in pm.Materials:
      if material.Name == 'Gold [Au]':
        gold = material
        break
    if gold:
      for roi_name in [ROIS.seed1.name, ROIS.seed2.name, ROIS.seed3.name]:
        try:
          pm.RegionsOfInterest[roi_name].SetRoiMaterial(Material=gold)
        except:
          pass
    # Exclude some ROIs from export:
    exclude = pelvic_bone_rois + vertebrae_rois + [ROIS.a_descending_aorta, ROIS.a_common_iliac_l,
      ROIS.a_common_iliac_r, ROIS.a_internal_iliac_l, ROIS.a_internal_iliac_r, ROIS.a_external_iliac_l,
      ROIS.a_external_iliac_r, ROIS.v_inferior_vena_cava, ROIS.v_common_iliac_l, ROIS.v_common_iliac_r,
      ROIS.v_internal_iliac_l, ROIS.v_internal_iliac_r, ROIS.v_external_iliac_l, ROIS.v_external_iliac_r
    ]
    for roi in exclude:
      PMF.exclude_roi_from_export(pm, roi.name)


  def add_bed_only_targets(self, pm, pm_setup, fractionation):
    """Adds target ROIs for prostate bed only.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      fractionation (str): A string indicating fractionation ('normo' for 70 Gy / 35 fx).
    """
    if fractionation == 'normo':
      pm_setup.add_targets([ROIS.ctv_sb])
      ctv = ROI.ROIExpanded(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_high, source = ROIS.ctv_sb)
      ptv = ROI.ROIExpanded(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv,
        source = ctv, margins = MARGINS.prostate_bed
      )
    else:
      ctv = ROIS.ctv_sb
      ptv = ROI.ROIExpanded(ROIS.ptv_sb.name, ROIS.ptv_sb.type, COLORS.ptv_high,
        source = ROIS.ctv_sb, margins = MARGINS.prostate_bed
      )
    # Targets:
    pm_setup.add_targets([ctv, ptv])
    # Other derived ROIs:
    wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv, 1, 0)
    pm_setup.add_oars([wall_ptv])


  def add_bed_with_nodes_targets(self, pm, pm_setup, nodes):
    """Adds target ROIs for prostate bed with elective nodal irradiation.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      nodes (str): A string indicating state of elective nodal irradiation (e.g. 'with' or 'with_node_70').
    """
    higher_dose_targets = []
    if nodes == 'with':
      # Elective nodes only:
      ctv_70 = ROI.ROIExpanded(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_high, source = ROIS.ctv_sb)
      ptv_70 = ROI.ROIExpanded(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv,
        source = ctv_70, margins = MARGINS.prostate_bed
      )
      higher_dose_targets.extend([ptv_70])
    else:
      # Positive node (in addition to elective nodes):
      ctv_n = ROI.ROIExpanded(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.pelvic_nodes,
        source = ROIS.gtv_n, margins = MARGINS.uniform_5mm_expansion
      )
      ptv_n = ROI.ROIExpanded(ROIS.ptv_n.name, ROIS.ptv_n.type, ROIS.ptv_n.color,
        source = ctv_n, margins = MARGINS.uniform_5mm_expansion
      )
      ptv_sb = ROI.ROIExpanded(ROIS.ptv_sb.name, ROIS.ptv_sb.type, ROIS.ptv_sb.color,
        source = ROIS.ctv_sb, margins = MARGINS.prostate_bed
      )
      if nodes == 'with_node_70':
        # Positive node will have 70 Gy:
        ctv_70 = ROI.ROIAlgebra(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_med,
          sourcesA = [ROIS.ctv_sb], sourcesB = [ctv_n], operator = 'Union'
        )
        ptv_70 = ROI.ROIAlgebra(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv, sourcesA = [ptv_sb],
          sourcesB = [ptv_n], operator = 'Union', marginsA = MARGINS.zero , marginsB = MARGINS.zero
        )
        pm_setup.add_targets([ROIS.gtv_n, ctv_n, ptv_n, ptv_sb])
        higher_dose_targets.extend([ptv_70])
      else:
        # Positive node will have 66 Gy:
        ctv_70 = ROI.ROIExpanded(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_high, source = ROIS.ctv_sb)
        ptv_70 = ROI.ROIExpanded(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv,
          source = ctv_70, margins = MARGINS.prostate_bed
        )
        ctv_66 = ROI.ROIAlgebra(ROIS.ctv_66.name, ROIS.ctv_66.type, COLORS.ctv_med,
          sourcesA = [ctv_n], sourcesB = [ptv_70], operator = 'Subtraction',
          marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_66 = ROI.ROIAlgebra(ROIS.ptv_66.name, ROIS.ptv_66.type, COLORS.ptv_med,
          sourcesA = [ctv_n], sourcesB = [ptv_70], operator = 'Subtraction',
          marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero
        )
        pm_setup.add_targets([ROIS.gtv_n, ctv_n, ptv_n, ptv_sb, ctv_66, ptv_66])
        higher_dose_targets.extend([ptv_70, ptv_66])
    # Common for elective nodes (with or without positive node):
    ctv_56 = ROI.ROIAlgebra(ROIS.ctv_56.name, ROIS.ctv_56.type, COLORS.ctv_low,
      sourcesA = [ROIS.pelvic_nodes], sourcesB = higher_dose_targets,
      operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    ptv_56 = ROI.ROIAlgebra(ROIS.ptv_56.name, ROIS.ptv_56.type, COLORS.ptv_low,
      sourcesA = [ROIS.pelvic_nodes], sourcesB = higher_dose_targets,
      operator = 'Subtraction', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero
    )
    ptv_56_70 = ROI.ROIAlgebra(ROIS.ptv_56_70.name, ROIS.ptv_56_70.type, COLORS.ptv_low,
      sourcesA = [ptv_56], sourcesB = [ptv_70], marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    pm_setup.add_targets([ROIS.ctv_sb, ctv_70, ptv_70, ctv_56, ptv_56, ptv_56_70])
    # Other derived ROIs:
    wall_ptv_70 = ROI.ROIWall(ROIS.z_ptv_70_wall.name, ROIS.z_ptv_70_wall.type, COLORS.wall, ptv_70, 1, 0)
    wall_ptv_56_temp = ROI.ROIWall(ROIS.z_ptv_56_temp.name, ROIS.z_ptv_56_temp.type, COLORS.wall, ptv_56, 1, 0)
    wall_ptv_56 = ROI.ROIAlgebra(ROIS.z_ptv_56_wall.name, ROIS.z_ptv_56_wall.type, COLORS.wall,
      sourcesA = [wall_ptv_56_temp], sourcesB = [ptv_70, wall_ptv_70], operator='Subtraction', marginsB = MARGINS.zero
    )
    pm_setup.add_oars([wall_ptv_70, wall_ptv_56_temp, wall_ptv_56])


  def add_common_rois(self, pm, pm_setup, region):
    """Adds ROIs for this particular treatment site that are common across all scopes.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      region (str): A string indicating anatomy (e.g. intact ('prostate') or post-op).
    """
    if region == 'prostate':
      pm_setup.add_oars([ROIS.bladder_draft, ROIS.bladder_derived])
    else:
      pm_setup.add_oars([ROIS.bladder])
    # Exclude Rectum from BowelBag:
    ROIS.bowel_bag.sourcesB.append(ROIS.rectum)
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.anal_canal, ROIS.bowel_bag_draft, ROIS.bowel_bag, ROIS.cauda_equina, ROIS.coccyx,
      ROIS.l5, ROIS.femoral_head_l, ROIS.femoral_head_r, ROIS.femur_l, ROIS.femur_r,
      ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.penile_bulb, ROIS.rectum, ROIS.sacrum
    ])


  def add_lymph_node_rois(self, pm, pm_setup):
    """Adds ROIs that are relevant for elective lymph node irradiation.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Exclude Kidneys, Liver and LN_Iliac from BowelBag:
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pelvic_nodes])
    pm_setup.add_oars([ROIS.a_common_iliac_l, ROIS. a_common_iliac_r, ROIS.a_descending_aorta,
      ROIS.a_external_iliac_l, ROIS.a_external_iliac_r, ROIS.a_internal_iliac_l, ROIS.a_internal_iliac_r,
      ROIS.iliopsoas_muscle_l, ROIS.iliopsoas_muscle_r, ROIS.kidney_l, ROIS.kidney_r, ROIS.l2, ROIS.l3, ROIS.l4,
      ROIS.liver, ROIS.pelvic_nodes, ROIS.v_common_iliac_l, ROIS.v_common_iliac_r, ROIS.v_external_iliac_l,
      ROIS.v_external_iliac_r, ROIS.v_inferior_vena_cava, ROIS.v_internal_iliac_l, ROIS.v_internal_iliac_r
    ])


  def add_prostate_high_risk_targets(self, pm, pm_setup, choices):
    """Adds target ROIs for high risk prostate.

    Based on the given choices, ROI targets are setup in categories of prostate only, prostate with
    elective nodal irradiation, prostate + ENI + boost to positive lymph node(s) at 60 Gy / 25 fx or
    prostate + ENI + boost to positve lymph node(s) at 62.5 Gy / 25 fx.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      choices (list): The choices made by the user in the definitions script GUI.
    """
    # Choice 2: Fractionation:
    fractionation = choices[2]
    # Choice 3: Nodes - none, elective only or elective + positive node?
    nodes = choices[3]
    # Seminal vesicles (which for high risk is 20 mm):
    semves20 = ROI.ROIAlgebra('SeminalVes20', ROIS.ctv.type, COLORS.vesicles,
      sourcesA = [ROIS.seminal_vesicles], sourcesB = [ROIS.prostate], operator = 'Intersection',
      marginsA = MARGINS.zero, marginsB = MARGINS.uniform_20mm_expansion
    )
    # Setup dose named ROIs:
    ctv3s = ROIS.ctv_67_5
    ptv3s = ROIS.ptv_67_5
    ptv3w = ROIS.z_ptv_67_5_wall
    ctv2s = ROIS.ctv_62_5_sib
    ptv2s = ROIS.ptv_62_5_sib
    ptv_2_3s = ROIS.ptv_62_5_67_5
    ptv_2_3w = ROIS.z_ptv_62_5_67_5_wall
    ptv_1_2_3w = ROIS.z_ptv_50_62_5_67_5_wall
    ctv1s = ROIS.ctv__50
    ptv1s = ROIS.ptv__50
    ptv_1_2_3s = ROIS.ptv_50_62_5_67_5
    # Prostate targets:
    ctv3 = ROI.ROIAlgebra(ctv3s.name, ctv3s.type, COLORS.ctv_high,
      sourcesA = [ROIS.prostate], sourcesB = [ROIS.rectum, ROIS.anal_canal, ROIS.levator_ani],
      operator = 'Subtraction', marginsA = MARGINS.prostate_ctv, marginsB = MARGINS.zero
    )
    ptv3 = ROI.ROIExpanded(ptv3s.name, ptv3s.type, COLORS.ptv_high,
      source = ctv3, margins = MARGINS.prostate_seed_expansion
    )
    # Other derived ROIs:
    wall_ptv3 = ROI.ROIWall(ptv3w.name, ptv3w.type, COLORS.wall, ptv3, 0.5, 0)
    if nodes == 'no':
      # Prostate only:
      # Vesicle targets:
      ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20], sourcesB = [ptv3],
        operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, COLORS.ptv_med, sourcesA = [semves20], sourcesB = [ptv3],
        operator = 'Subtraction', marginsA = MARGINS.uniform_6mm_expansion, marginsB = MARGINS.zero
      )
      ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low, sourcesA = [ctv3], sourcesB = [semves20],
        marginsA = MARGINS.prostate_seed_expansion, marginsB = MARGINS.uniform_6mm_expansion
      )
      pm_setup.add_targets([ptv_2_3])
      # Other derived ROIs:
      pm_setup.add_oars([wall_ptv3])
    elif nodes == 'with':
      # Elective nodes:
      # Targets:
      ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20], sourcesB = [ptv3],
        operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, COLORS.ptv_med, sourcesA = [semves20], sourcesB = [ptv3],
        operator = 'Subtraction', marginsA = MARGINS.uniform_6mm_expansion, marginsB = MARGINS.zero
      )
      ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low, sourcesA = [ctv3], sourcesB = [semves20],
        marginsA = MARGINS.prostate_seed_expansion, marginsB = MARGINS.uniform_6mm_expansion
      )
      ptv1 = ROI.ROIAlgebra(ptv1s.name, ptv1s.type, COLORS.ptv_low,
        sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction',
        marginsA = MARGINS.prostate_lymph_nodes_seed_match, marginsB = MARGINS.zero
      )
      ctv1 = ROI.ROIAlgebra(ctv1s.name, ctv1s.type, COLORS.ctv_low,
        sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv_1_2_3 = ROI.ROIAlgebra(ptv_1_2_3s.name, ptv_1_2_3s.type, COLORS.ptv_low,
        sourcesA = [ptv1, ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      pm_setup.add_targets([ctv1, ptv1, ptv_2_3, ptv_1_2_3])
      # OARs:
      wall_ptv_2_3 = ROI.ROIWall(ptv_2_3w.name, ptv_2_3w.type, COLORS.wall, ptv_2_3, 1, 0)
      wall_ptv_1_2_3 = ROI.ROIWall(ptv_1_2_3w.name, ptv_1_2_3w.type, COLORS.wall, ptv_1_2_3, 1, 0)
      # Non-DL OARs:
      pm_setup.add_oars([wall_ptv3, wall_ptv_2_3, wall_ptv_1_2_3])
    else:
      # Positive node (in addition to elective nodes):
      ctv_n = ROI.ROIExpanded(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.pelvic_nodes,
        source = ROIS.gtv_n, margins = MARGINS.uniform_5mm_expansion
      )
      ptv_n = ROI.ROIExpanded(ROIS.ptv_n.name, ROIS.ptv_n.type, ROIS.ptv_n.color,
        source = ctv_n, margins = MARGINS.prostate_lymph_nodes_seed_match
      )
      if nodes == 'with_node_62.5':
        # Positive node will have 62.5 Gy:
        # Targets:
        ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20, ctv_n], sourcesB = [ptv3],
          operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_semves = ROI.ROIAlgebra(ROIS.ptv_semves.name, ROIS.ptv_semves.type, COLORS.ptv_med,
          sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction',
          marginsA = MARGINS.uniform_6mm_expansion, marginsB = MARGINS.zero
        )
        ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, ptv2s.color, sourcesA = [ptv_semves, ptv_n], sourcesB = [ptv3],
          operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low, sourcesA = [ptv2], sourcesB = [ptv3],
          marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv1 = ROI.ROIAlgebra(ptv1s.name, ptv1s.type, COLORS.ptv_low,
          sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction',
          marginsA = MARGINS.prostate_lymph_nodes_seed_match, marginsB = MARGINS.zero
        )
        ctv1 = ROI.ROIAlgebra(ctv1s.name, ctv1s.type, COLORS.ctv_low,
          sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction',
          marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_1_2_3 = ROI.ROIAlgebra(ptv_1_2_3s.name, ptv_1_2_3s.type, COLORS.ptv_low,
          sourcesA = [ptv1, ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        pm_setup.add_targets([ROIS.gtv_n, ctv_n, ctv1, ptv_n, ptv_semves, ptv1, ptv_2_3, ptv_1_2_3])
        # OARs:
        wall_ptv_2_3 = ROI.ROIWall(ptv_2_3w.name, ptv_2_3w.type, COLORS.wall, ptv_2_3, 1, 0)
        wall_ptv_1_2_3 = ROI.ROIWall(ptv_1_2_3w.name, ptv_1_2_3w.type, COLORS.wall, ptv_1_2_3, 1, 0)
        # Non-DL OARs:
        pm_setup.add_oars([wall_ptv3, wall_ptv_2_3, wall_ptv_1_2_3])
      else:
        # Positive node will have 60 Gy:
        # Targets:
        ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20], sourcesB = [ptv3],
          operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_semves = ROI.ROIAlgebra(ROIS.ptv_semves.name, ROIS.ptv_semves.type, COLORS.ptv_med,
          sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction',
          marginsA = MARGINS.uniform_6mm_expansion, marginsB = MARGINS.zero
        )
        ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, ptv2s.color, sourcesA = [ptv_semves], sourcesB = [ptv3],
          operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low,
          sourcesA = [ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ctv_60 = ROI.ROIAlgebra(ROIS.ctv__60.name, ROIS.ctv__60.type, COLORS.ctv_med,
          sourcesA = [ctv_n], sourcesB = [ptv2, ptv3], operator = 'Subtraction',
          marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_60 = ROI.ROIAlgebra(ROIS.ptv__60.name, ROIS.ptv__60.type, COLORS.ptv_med,
          sourcesA = [ctv_n], sourcesB = [ptv2, ptv3], operator = 'Subtraction',
          marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero
        )
        ptv1 = ROI.ROIAlgebra(ptv1s.name, ptv1s.type, COLORS.ptv_low,
          sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2, ptv_60], operator = 'Subtraction',
          marginsA = MARGINS.prostate_lymph_nodes_seed_match, marginsB = MARGINS.zero
        )
        ctv1 = ROI.ROIAlgebra(ctv1s.name, ctv1s.type, COLORS.ctv_low,
          sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2, ptv_60], operator = 'Subtraction',
          marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv_1_2_3 = ROI.ROIAlgebra(ptv_1_2_3s.name, ptv_1_2_3s.type, COLORS.ptv_low,
          sourcesA = [ptv1, ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        pm_setup.add_targets([ROIS.gtv_n, ctv_n, ctv_60, ctv1, ptv_n, ptv_semves, ptv_60, ptv1, ptv_2_3, ptv_1_2_3])
        # OARs:
        wall_ptv_2_3 = ROI.ROIWall(ptv_2_3w.name, ptv_2_3w.type, COLORS.wall, ptv_2_3, 1, 0)
        wall_ptv_1_2_3 = ROI.ROIWall(ptv_1_2_3w.name, ptv_1_2_3w.type, COLORS.wall, ptv_1_2_3, 1, 0)
        # Non-DL OARs:
        pm_setup.add_oars([wall_ptv3, wall_ptv_2_3, wall_ptv_1_2_3])
    # Common ROIs for all conventional fractionation:
    pm_setup.add_targets([semves20, ctv3, ctv2, ptv3, ptv2])


  def add_prostate_intermediate_or_high_risk_targets(self, pm, pm_setup, high_risk=False, sbrt=False):
    """Adds target ROIs for intermediate risk or high risk localized prostate cancer.

    Sets up target ROIs with proper dose (e.g. for 5 or 20 fx) and scope (e.g. seminal vesicles)
    based on the given parameters.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      high_risk (bool, optional): A boolean indicating whether the case is high risk (True) or
        intermediate risk (False). Defaults to False.
      sbrt (bool, optional): A boolean indicating whether this is a SBRT case (True) or
        conventional case (False). Defaults to False.
    """
    # Intact prostate and vesicles, but no elective nodes:
    # Seminal vesicles (which for intermediate risk is 10 mm and for high risk is 20 mm):
    if high_risk:
      semves = ROI.ROIAlgebra('SeminalVes20', ROIS.ctv.type, COLORS.vesicles,
        sourcesA = [ROIS.seminal_vesicles], sourcesB = [ROIS.prostate], operator = 'Intersection',
        marginsA = MARGINS.zero, marginsB = MARGINS.uniform_20mm_expansion
      )
    else:
      semves = ROI.ROIAlgebra('SeminalVes10', ROIS.ctv.type, COLORS.vesicles,
        sourcesA = [ROIS.seminal_vesicles], sourcesB = [ROIS.prostate], operator = 'Intersection',
        marginsA = MARGINS.zero, marginsB = MARGINS.uniform_10mm_expansion
      )
    # Targets:
    if sbrt:
      # For SBRT we use Anorectum instead of Rectum and AnalCanal:
      anorectum = ROI.ROIAlgebra(ROIS.anorectum.name, ROIS.anorectum.type, COLORS.rectum,
        sourcesA = [ROIS.rectum], sourcesB = [ROIS.anal_canal], operator = 'Union',
        marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      # Targets:
      ctv_40 = ROI.ROIAlgebra(ROIS.ctv_40.name, ROIS.ctv_40.type, COLORS.ctv_high, sourcesA = [ROIS.prostate],
        sourcesB = [semves], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv_36_25 = ROI.ROIExpanded(ROIS.ptv_36_25.name, ROIS.ptv_36_25.type, COLORS.ptv_high,
        source = ctv_40, margins = MARGINS.prostate_seed_expansion
      )
      pm_setup.add_targets([semves, ctv_40, ptv_36_25])
      wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv_36_25, 0.5, 0)
      pm_setup.add_oars([anorectum, wall_ptv])
    else:
      ctv_60 = ROI.ROIAlgebra(ROIS.ctv_60.name, ROIS.ctv_60.type, COLORS.ctv_high,
        sourcesA = [ROIS.prostate], sourcesB = [ROIS.rectum, ROIS.anal_canal, ROIS.levator_ani],
        operator = 'Subtraction', marginsA = MARGINS.prostate_ctv, marginsB = MARGINS.zero
      )
      ctv_57_60 = ROI.ROIAlgebra(ROIS.ctv_57_60.name, ROIS.ctv_57_60.type, COLORS.ctv_low,
        sourcesA = [ctv_60], sourcesB = [semves], marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv_57_60 = ROI.ROIAlgebra(ROIS.ptv_57_60.name, ROIS.ptv_57_60.type, COLORS.ptv_low,
        sourcesA = [ctv_60], sourcesB = [semves],
        marginsA = MARGINS.prostate_seed_expansion, marginsB = MARGINS.uniform_6mm_expansion
      )
      ptv_60 = ROI.ROIExpanded(ROIS.ptv_60.name, ROIS.ptv_60.type, COLORS.ptv_high,
        source = ctv_60, margins = MARGINS.prostate_seed_expansion
      )
      ctv_57 = ROI.ROIAlgebra(ROIS.ctv_57.name, ROIS.ctv_57.type, COLORS.ctv_med, sourcesA = [ctv_57_60],
        sourcesB = [ptv_60], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv_57 = ROI.ROIAlgebra(ROIS.ptv_57.name, ROIS.ptv_57.type, COLORS.ptv_med, sourcesA = [ptv_57_60],
        sourcesB = [ptv_60], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      pm_setup.add_targets([semves, ctv_60, ctv_57, ctv_57_60, ptv_57_60, ptv_60, ptv_57])
      # Other derived ROIs:
      wall_ptv_60 = ROI.ROIWall(ROIS.z_ptv_60_wall.name, ROIS.z_ptv_60_wall.type, COLORS.wall, ptv_60, 0.5, 0)
      wall_ptv_57_60 = ROI.ROIWall(ROIS.z_ptv_57_60_wall.name, ROIS.z_ptv_57_60_wall.type, COLORS.wall, ptv_57_60, 1, 0)
      pm_setup.add_oars([wall_ptv_60, wall_ptv_57_60])


  def add_prostate_palliative_targets(self, pm, pm_setup, choices):
    """Adds target ROIs for palliative prostate.

    Based on the given choices, ROI targets are setup with margins for either bone or seed match.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      choices (list): The choices made by the user in the definitions script GUI.
    """
    # Choice 2: Fractionation - STAMPEDE or palliative?
    fractionation = choices[2]
    # Targets:
    ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_low, source = ROIS.prostate, margins = MARGINS.zero)
    if fractionation == 'hypo_55':
      # Choice 3: Seed match or bone match?
      match = choices[3]
      if match == 'seeds':
        # Seed match:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high,
          source = ctv, margins = MARGINS.prostate_seed_expansion
        )
      else:
        # Bone match:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high,
          source = ctv, margins = MARGINS.prostate_bone_match_expansion
        )
    else:
      # Assuming no markers:
      ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high,
        source = ctv, margins = MARGINS.prostate_bone_match_expansion
      )
    pm_setup.add_targets([ctv, ptv])
    # Other derived ROIs:
    wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv, 1, 0)
    pm_setup.add_oars([wall_ptv])


  def add_prostate_rois(self, pm, pm_setup, match):
    """Adds ROIs for intact prostate cases.

    If seeds are present, relevant ROIs are added.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      match (str): A string indicating if fiducial markers are present ('seeds').
    """
    pm_setup.add_oars([ROIS.prostate, ROIS.seminal_vesicles])
    if match == 'seeds':
      # Non-DL OARs:
      pm_setup.add_oars([ROIS.levator_ani, ROIS.seed1, ROIS.seed2, ROIS.seed3, ROIS.urethra])


  def setup_bed(self, pm, pm_setup, choices):
    """Sets up ROIs used for prostate bed cases.

    Based on the given choices, sets up bed only or elective nodal irradiation.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      choices (list): The choices made by the user in the definitions script GUI.
    """
    # Choice 2: Fractionation - normal or palliative?
    fractionation = choices[2]
    # Fractionation:
    if fractionation == 'normo':
      # Conventional fractionation (2 Gy):
      # Choice 3: Nodes - included or not?
      nodes = choices[3]
      if nodes == 'no':
        # Prostate bed only:
        self.add_bed_only_targets(pm, pm_setup, fractionation)
      else:
        # Bed with elective nodes (and possibly also positive node):
        self.add_lymph_node_rois(pm, pm_setup)
        self.add_bed_with_nodes_targets(pm, pm_setup, nodes)
    else:
      # Palliative prostate bed only:
      self.add_bed_only_targets(pm, pm_setup, fractionation)


  def setup_prostate(self, pm, pm_setup, choices):
    """Sets up ROIs used for intact prostate cases.

    Based on the given choices, sets up fractionation and scope (elective nodal irradiation).

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      choices (list): The choices made by the user in the definitions script GUI.
    """
    # Choice 2: Fractionation (e.g. conventional, hypo, palliative)
    fractionation = choices[2]
    # Fractionation:
    if fractionation in ['hypo_bergen']:
      # Hypofractionated 25 fx: prostate (67.5 Gy) with vesicles (62.5 Gy) and nodes (50 Gy):
      self.add_prostate_rois(pm, pm_setup, 'seeds')
      # Lymph nodes?
      nodes = choices[3]
      if nodes != 'no':
        self.add_lymph_node_rois(pm, pm_setup)
      self.add_prostate_high_risk_targets(pm, pm_setup, choices)
    elif fractionation in ['sbrt_5fx', 'hypo_60', 'hypo_60_highrisk']:
      # Intermediate (5 or 20 fx) or high risk without elective nodes (20 fx):
      high_risk = False
      sbrt = False
      if fractionation == 'hypo_60_highrisk':
        high_risk = True
      elif fractionation == 'sbrt_5fx':
        sbrt = True
      self.add_prostate_rois(pm, pm_setup, 'seeds')
      self.add_prostate_intermediate_or_high_risk_targets(pm, pm_setup, high_risk, sbrt)
    elif fractionation in ['hypo_55','palliative']:
      if fractionation == 'hypo_55':
        self.add_prostate_rois(pm, pm_setup, choices[3])
      else:
        self.add_prostate_rois(pm, pm_setup, 'bone')
      # STAMPEDE (2.75 Gy x 20) or palliative prostate (e.q. 3 Gy x 13):
      self.add_prostate_palliative_targets(pm, pm_setup, choices)
