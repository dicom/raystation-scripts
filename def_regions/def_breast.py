# Import local files:
import colors as COLORS
import def_oars as DEF
import margin as MARGIN
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS


class DefBreast(object):
  """Configuration of ROIs used for cases of breast cancer."""

  def __init__(self, pm, ss, choices, pm_setup):
    """Initializes the breast case configuration with the relevant RayStation instances and the user's GUI selections.

    Based on the settings given, a set of ROIs (Targets, OARs & Others) are created on the patient case in RayStation.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
      pm (PyScriptObject): The RayStation PatientModel instance.
      ss (PyScriptObject): The RayStation StructureSet instance.
      choices (list): The choices made by the user in the definitions script GUI.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Choice 1: Local/Regional/Regional with IMN
    region = choices[1]
    # Choice 2: Side - Left or right?
    side = choices[2]
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, pm_setup)
    # Region:
    if region == 'partial':
      # Partial breast only:
      boost = 'without'
      bilateral = False
      self.add_partial_breast(pm, pm_setup, side, bilateral)
    else:
      # Choice 3: With our without boost?
      boost = choices[3]
      if region == 'whole':
        # Whole breast (with or without regional nodes):
        bilateral = False
        self.add_whole_breast(pm, pm_setup, side, boost, bilateral)
      elif region in ['regional', 'regional_imn']:
        # Regional breast (with or without IMN):
        bilateral = False
        if region == 'regional_imn':
          self.add_regional_breast(pm, pm_setup, side, boost, bilateral, include_imn=True)
        else:
          self.add_regional_breast(pm, pm_setup, side, boost, bilateral, include_imn=False)
      else:
        # Bilateral:
        bilateral = True
        bilateral_left_side_target = choices[2]
        bilateral_right_side_target = choices[3]
        if bilateral_left_side_target == 'bilateral_left_partial':
          self.add_partial_breast(pm, pm_setup, 'left', bilateral)
          ctv_l = ROIS.ctv_sb_l
          ptv_l = ROIS.ptv_sbc_l
        elif bilateral_left_side_target == 'bilateral_left_whole':
          self.add_whole_breast(pm, pm_setup, 'left', boost, bilateral)
          ctv_l = ROIS.ctv_l
          ptv_l = ROIS.ptvc_l
        else:
          self.add_regional_breast(pm, pm_setup, 'left', boost, bilateral, include_imn=True)
          ctv_l = ROIS.ctv_l
          ptv_l = ROIS.ptvc_l
        if bilateral_right_side_target == 'bilateral_right_partial':
          self.add_partial_breast(pm, pm_setup, 'right', bilateral)
          ctv_r = ROIS.ctv_sb_r
          ptv_r = ROIS.ptv_sbc_r
        elif bilateral_right_side_target == 'bilateral_right_whole':
          self.add_whole_breast(pm, pm_setup, 'right', boost, bilateral)
          ctv_r = ROIS.ctv_r
          ptv_r = ROIS.ptvc_r
        else:
          self.add_regional_breast(pm, pm_setup, 'right', boost, bilateral, include_imn=True)
          ctv_r = ROIS.ctv_r
          ptv_r = ROIS.ptvc_r
        # If at least one side is locoregional, and the other side is not partial, we add a PTVpc union:
        if bilateral_left_side_target == 'bilateral_left_regional' or bilateral_right_side_target == 'bilateral_right_regional':
          if bilateral_left_side_target != 'bilateral_left_partial' and bilateral_right_side_target != 'bilateral_right_partial':
            if bilateral_left_side_target == 'bilateral_left_whole':
              left_primary = ROIS.ptvc_l
            else:
              left_primary = ROIS.ptv_pc_l
            if bilateral_right_side_target == 'bilateral_right_whole':
              right_primary = ROIS.ptvc_r
            else:
              right_primary = ROIS.ptv_pc_r
            ptv_pc = ROI.ROIAlgebra(ROIS.ptv_pc.name, ROIS.ptv_pc.type, ROIS.ptv_pc.color,
              sourcesA = [left_primary, right_primary], sourcesB = [ROIS.external],
              operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
            )
            pm_setup.add_targets([ptv_pc])
        # Targets (L+R union):
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ctv_l], sourcesB = [ctv_r],
          operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero
        )
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color,
          sourcesA = [ptv_l, ptv_r], sourcesB = [ROIS.external],
          operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
        )
        pm_setup.add_targets([ctv, ptv])
    # Add wall:
    self.add_wall(pm_setup, side, region, boost)
    # Create all targets and OARs in RayStation:
    pm_setup.create_rois()
    # Change organ type to 'Other' for selected ROIs:
    for roi_name in ['Clips_L','Clips_R','BreastString_L','BreastString_R','Breast_L_Draft','Breast_R_Draft'
      'SurgicalBed_L','SurgicalBed_R','LN_Ax_Pectoral_L','LN_Ax_Pectoral_R','LN_Ax_L1_L','LN_Ax_L1_R','LN_Ax_L2_L',
      'LN_Ax_L2_R','LN_Ax_L3_L','LN_Ax_L3_R','LN_Ax_L4_L','LN_Ax_L4_R','LN_IMN_L','LN_IMN_R','ScaleneMuscle_Ant_L',
      'A_Carotid_L','A_Subclavian_L','V_Brachiocephalic_L','V_Jugular_Int_L','V_Subclavian_L','ScaleneMuscle_Ant_R',
      'A_Brachiocephalic','A_Carotid_R','A_Subclavian_R','V_Brachiocephalic_R','V_Jugular_Int_R','V_Subclavian_R'
    ]:
      # Some of these ROIs may not always be defined, and give an error:
      try:
        pm.RegionsOfInterest[roi_name].OrganData.OrganType = 'Other'
      except:
        pass
    # Exclude some ROIs from export:
    for roi_name in [ROIS.breast_l_draft.name, ROIS.breast_r_draft.name, 'LN_Ax_L1_L','LN_Ax_L2_L','LN_Ax_L3_L',
      'LN_Ax_L4_L','LN_Ax_Pectoral_L','LN_IMN_L','LN_Ax_L1_R','LN_Ax_L2_R','LN_Ax_L3_R','LN_Ax_L4_R',
      'LN_Ax_Pectoral_R','LN_IMN_R','ScaleneMuscle_Ant_L','A_Carotid_L','A_Subclavian_L','V_Brachiocephalic_L',
      'V_Jugular_Int_L','V_Subclavian_L','ScaleneMuscle_Ant_R','A_Brachiocephalic','A_Carotid_R','A_Subclavian_R',
      'V_Brachiocephalic_R','V_Jugular_Int_R','V_Subclavian_R'
    ]:
      PMF.exclude_roi_from_export(pm, roi_name)
      # Exclude SurgicalBed_L/R (where relevant we have the CTVsb ROI available anyway):
      if side == 'right':
        PMF.exclude_roi_from_export(pm, 'SurgicalBed_R')
      else:
        PMF.exclude_roi_from_export(pm, 'SurgicalBed_L')
    # Only some patients actually have breast string. Delete the ROI if its volume is less than 0.5 cm^3:
    for rg in ss.RoiGeometries:
      if rg.OfRoi.Name in ['BreastString_L', 'BreastString_R']:
        # Delete the ROI if the patient doesnt seem to have a breast string:
        if rg.HasContours():
          if rg.GetRoiVolume() < 0.5:
            if not PMF.is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi_name):
              pm.RegionsOfInterest[rg.OfRoi.Name].DeleteRoi()
        else:
          if not PMF.is_approved_roi_structure_in_one_of_all_structure_sets(pm, roi_name):
            pm.RegionsOfInterest[rg.OfRoi.Name].DeleteRoi()
    # Override the density of the breast string to 'Air' (since it is not present on treatments):
    self.set_breaststring_density(pm)


  def add_boost(self, pm_setup, side, ctv, ptv, ctv_p=None, ptv_pc=None):
    """Adds boost target ROIs.

    Args:
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
      ctv (ROIAlgebra): The target ROI which the ctv_sb is confined to.
      ptv (ROIAlgebra): A target ROI which is used to create a subtraction ROI.
      ctv_p (ROIAlgebra, optional): The target to be used for boost subtraction for regional breast. Defaults to None,
        which is interpreted as whole breast and the use of ROIS.ctv_ptv_sbc.
      ptv_pc (ROIAlgebra, optional): The target to be used for boost subtraction regional breast. Defaults to None,
        which is interpreted as whole breast and the use of ROIS.ptv_c_ptv_sbc.
    """
    if side == 'right':
      sb = ROIS.surgical_bed_r
    else:
      sb = ROIS.surgical_bed_l
    ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [sb], sourcesB = [ctv],
      operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv_sb.type, ROIS.ptv.color,
      sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    ctv_ctv_sb = ROI.ROIAlgebra(ROIS.ctv_ctv_sb.name, ROIS.ctv_ctv_sb.type, ROIS.ctv_ctv_sb.color,
      sourcesA = [ctv], sourcesB = [ctv_sb], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    ctv_ptv_sbc = ROI.ROIAlgebra(ROIS.ctv_ptv_sbc.name, ROIS.ctv_ptv_sbc.type, ROIS.ctv_ptv_sbc.color,
      sourcesA = [ctv], sourcesB = [ptv_sbc], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    ptv_c_ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_c_ptv_sbc.name, ROIS.ptv_c_ptv_sbc.type, ROIS.ptv_c_ptv_sbc.color,
      sourcesA = [ptv], sourcesB = [ptv_sbc], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    pm_setup.add_targets([ctv_sb, ptv_sbc, ctv_ctv_sb, ctv_ptv_sbc, ptv_c_ptv_sbc])
    if ctv_p:
      # For regional breast we need separate subracted ROIs for the whole CTV/PTV and the breast CTVp/PTVp:
      ctv_p_ctv_sb = ROI.ROIAlgebra(ROIS.ctv_p_ctv_sb.name, ROIS.ctv_p_ctv_sb.type, ROIS.ctv_p_ctv_sb.color,
        sourcesA = [ctv_p], sourcesB = [ctv_sb], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ctv_p_ptv_sbc = ROI.ROIAlgebra(ROIS.ctv_p_ptv_sbc.name, ROIS.ctv_p_ptv_sbc.type, ROIS.ctv_p_ptv_sbc.color,
        sourcesA = [ctv_p], sourcesB = [ptv_sbc], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      ptv_pc_ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_pc_ptv_sbc.name, ROIS.ptv_pc_ptv_sbc.type, ROIS.ptv_pc_ptv_sbc.color,
        sourcesA = [ptv_pc], sourcesB = [ptv_sbc], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      zctv_p_ptv_sbc = ROI.ROIAlgebra('z' + ROIS.ctv_p_ptv_sbc.name, ROIS.ctv_p_ptv_sbc.type, ROIS.ctv_p_ptv_sbc.color,
        sourcesA = [ctv_p_ptv_sbc], sourcesB = [ptv_sbc], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGIN.Expansion(0.4, 0.4, 0.4, 0.4, 0.4, 0.4)
      )
      zptv_pc_ptv_sbc = ROI.ROIAlgebra('z' + ROIS.ptv_pc_ptv_sbc.name, ROIS.ptv_pc_ptv_sbc.type,
        ROIS.ptv_pc_ptv_sbc.color, sourcesA = [ptv_pc_ptv_sbc], sourcesB = [ptv_sbc], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGIN.Expansion(0.4, 0.4, 0.4, 0.4, 0.4, 0.4)
      )
      pm_setup.add_targets([ctv_p_ctv_sb, ctv_p_ptv_sbc, ptv_pc_ptv_sbc, zctv_p_ptv_sbc, zptv_pc_ptv_sbc])
    else:
      # Whole breast:
      zctv_ptv_sbc = ROI.ROIAlgebra('z' + ROIS.ctv_ptv_sbc.name, ROIS.ctv_ptv_sbc.type, ROIS.ctv_ptv_sbc.color,
        sourcesA = [ctv_ptv_sbc], sourcesB = [ptv_sbc], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGIN.Expansion(0.4, 0.4, 0.4, 0.4, 0.4, 0.4)
      )
      zptv_c_ptv_sbc = ROI.ROIAlgebra('z' + ROIS.ptv_c_ptv_sbc.name, ROIS.ptv_c_ptv_sbc.type, ROIS.ptv_c_ptv_sbc.color,
        sourcesA = [ptv_c_ptv_sbc], sourcesB = [ptv_sbc], operator = 'Subtraction',
        marginsA = MARGINS.zero, marginsB = MARGIN.Expansion(0.4, 0.4, 0.4, 0.4, 0.4, 0.4)
      )
      pm_setup.add_targets([zctv_ptv_sbc, zptv_c_ptv_sbc])


  def add_common_rois(self, pm, pm_setup):
    """Adds ROIs for this particular treatment site that are common across all scopes.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL ROIs:
    pm_setup.add_oars([ROIS.a_lad, ROIS.breast_l_draft, ROIS.breast_r_draft, ROIS.esophagus, ROIS.heart,
      ROIS.lung_l, ROIS.lung_r, ROIS.sternum, ROIS.thyroid
    ])
    # Add derived ROIs:
    pm_setup.add_oars([ROIS.breast_l, ROIS.breast_r, ROIS.lungs])


  def add_partial_breast(self, pm, pm_setup, side, bilateral):
    """Adds ROIs for partial breast treatment.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
      bilateral (bool): A boolean indicating whether the case is bilateral (True) or not (False).
    """
    self.add_sided_rois(pm, pm_setup, side)
    # Laterality suffix for targets for bilateral cases:
    suffix = ''
    if bilateral:
      if side == 'right':
        suffix = '_R'
      else:
        suffix = '_L'
    # ROIs are dependent on side:
    if side == 'right':
      sb = ROIS.surgical_bed_r
      breast = ROIS.breast_r
    else:
      sb = ROIS.surgical_bed_l
      breast = ROIS.breast_l
    # Targets:
    ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name+suffix, ROIS.ctv.type, ROIS.ctv.color,
      sourcesA = [sb], sourcesB = [breast], operator = 'Intersection',
      marginsA = MARGINS.uniform_15mm_expansion, marginsB = MARGINS.zero
    )
    ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name+suffix, ROIS.ptv.type, ROIS.ptv.color,
      sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    # Image verification volume:
    clips_control = ROI.ROIAlgebra('ClipsControl'+suffix, ROIS.markers.type, ROIS.markers.color,
      sourcesA = [sb], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    # Targets for whole breast:
    pm_setup.add_targets([ctv_sb, ptv_sbc, clips_control])


  def add_regional_breast(self, pm, pm_setup, side, boost, bilateral, include_imn):
    """Adds ROIs for regional breast treatment.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
      boost (str): A string indicating use of a boost ('with').
      bilateral (bool): A boolean indicating whether the case is bilateral (True) or not (False).
      include_imn (bool): A boolean indicating whether IMN target is to be included (True) or not (False).
    """
    # Common ROIs for regional breast:
    pm_setup.add_oars([ROIS.carina, ROIS.spinal_canal, ROIS.trachea])
    self.add_sided_rois(pm, pm_setup, side)
    # Laterality suffix for targets for bilateral cases:
    suffix = ''
    if bilateral:
      if side == 'right':
        suffix = '_R'
      else:
        suffix = '_L'
    # Side dependent targets and support structures for regional treatment:
    if side == 'right':
      # ROIs for right sided regional nodes:
      pm_setup.add_oars([ROIS.a_brachiocephalic, ROIS.a_carotid_r, ROIS.a_subclavian_r, ROIS.brachial_plexus_r,
        ROIS.bronchus_main_r, ROIS.bronchus_intermedius, ROIS.ln_ax_l1_r, ROIS.ln_ax_l2_r, ROIS.ln_ax_l3_r,
        ROIS.ln_ax_l4_r, ROIS.ln_ax_pectoral_r, ROIS.ln_imn_r, ROIS.scalene_muscle_ant_r, ROIS.v_brachiocephalic_r,
        ROIS.v_jugular_int_r, ROIS.v_subclavian_r
      ])
      # Targets:
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name+suffix, ROIS.ctv_p.type, ROIS.ctv.color,
        sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection',
        marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
      )
      ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name+suffix, ROIS.ctv_n.type, ROIS.ctv.color,
        sourcesA = [ROIS.ln_ax_pectoral_r, ROIS.ln_ax_l1_r, ROIS.ln_ax_l2_r, ROIS.ln_ax_l3_r, ROIS.ln_ax_l4_r],
        sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      if include_imn:
        imn = ROIS.ln_imn_r
    else:
      # ROIs for left sided regional nodes:
      pm_setup.add_oars([ROIS.a_carotid_l, ROIS.a_subclavian_l, ROIS.brachial_plexus_l, ROIS.bronchus_main_l,
        ROIS.ln_ax_l1_l, ROIS.ln_ax_l2_l, ROIS.ln_ax_l3_l, ROIS.ln_ax_l4_l, ROIS.ln_ax_pectoral_l, ROIS.ln_imn_l,
        ROIS.scalene_muscle_ant_l, ROIS.v_brachiocephalic_l, ROIS.v_jugular_int_l, ROIS.v_subclavian_l
      ])
      # Targets:
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name+suffix, ROIS.ctv_p.type, ROIS.ctv.color,
        sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection',
        marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
      )
      ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name+suffix, ROIS.ctv_n.type, ROIS.ctv.color,
        sourcesA = [ROIS.ln_ax_pectoral_l, ROIS.ln_ax_l1_l, ROIS.ln_ax_l2_l, ROIS.ln_ax_l3_l, ROIS.ln_ax_l4_l],
        sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero
      )
      if include_imn:
        imn = ROIS.ln_imn_l
    # Common targets for left and right:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name+suffix, ROIS.ctv.type, ROIS.ctv.color,
      sourcesA = [ctv_n], sourcesB = [ctv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    ptv_p = ROI.ROIAlgebra(ROIS.ptv_pc.name+suffix, ROIS.ptv_pc.type, ROIS.ptv.color,
      sourcesA = [ctv_p], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv_n = ROI.ROIAlgebra(ROIS.ptv_nc.name+suffix, ROIS.ptv_nc.type, ROIS.ptv.color,
      sourcesA = [ctv_n], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv_c.name+suffix, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ptv_n], sourcesB = [ptv_p],
      operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero
    )
    # IMN:
    if include_imn:
      ctv_n.sourcesA.extend([imn])
    # Common targets for all regional:
    pm_setup.add_targets([ctv_p, ctv_n, ctv, ptv_p, ptv_n, ptv])
    # Add targets for boost (2 Gy x 8) if indicated:
    if boost == 'with':
      self.add_boost(pm_setup, side, ctv, ptv, ctv_p, ptv_p)


  def add_sided_rois(self, pm, pm_setup, side):
    """Adds ROIs for this particular treatment site that are specific for left or right side.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
    """
    if side == 'right':
      pm_setup.add_oars([ROIS.breast_string_r, ROIS.clips_r, ROIS.humeral_head_r, ROIS.liver, ROIS.surgical_bed_r])
    else:
      pm_setup.add_oars([ROIS.breast_string_l, ROIS.clips_l, ROIS.humeral_head_l, ROIS.surgical_bed_l])


  # Adds a target wall ROI.
  def add_wall(self, pm_setup, side, region, boost, target_roi=None):
    """Adds a target wall ROI.

    Args:
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
      region (str): A string indicating scope ('partial', 'whole', 'regional' or 'reqional_imn').
      boost (str): A string indicating use of a boost ('with').
      target_roi (ROI, optional): The target_roi on which to create a wall. Defaults to None,
        which initializes ROIS.ctv_sb for partial breast or ROIS.ctv for other cases.
    """
    if 'bilateral' in side:
      # For bilateral cases, recursively use this function two times to create left and right walls:
      l_region = side.split('_')[-1]
      if l_region == 'partial':
        t = ROIS.ctv_sb_l
      else:
        t = ROIS.ctv_l
      self.add_wall(pm_setup, 'left', l_region, '', target_roi=t)
      r_region = boost.split('_')[-1]
      if r_region == 'partial':
        t = ROIS.ctv_sb_r
      else:
        t = ROIS.ctv_r
      self.add_wall(pm_setup, 'right', r_region, '', target_roi=t)
    else:
      # Configure values for left or right:
      if side == 'right':
        wall_draft_name = 'zCTV_R_Wall_Draft'
        wall_name = 'zCTV_R_Wall'
        right_margin = 1.5
        left_margin = 0.5
      else:
        wall_draft_name = 'zCTV_L_Wall_Draft'
        wall_name = 'zCTV_L_Wall'
        right_margin = 0.5
        left_margin = 1.5
      # Which target to use for wall:
      if region == 'partial':
        if target_roi is not None:
          t = target_roi
        else:
          t = ROIS.ctv_sb
      else:
        if target_roi is not None:
          t = target_roi
        else:
          t = ROIS.ctv
      if boost == 'with':
        # For SIB cases, we will need to ensure that the wall has a minimum distance to the boost PTV for dose fall off.
        # We accomplish this by first creating a wall draft, and then using a ROI algebra for the final wall.
        wall_draft = ROI.ROIWall(wall_draft_name, ROIS.z_ptv_wall.type, COLORS.wall, t, 1.5, 0)
        wall = ROI.ROIAlgebra(wall_name, ROIS.z_ptv_wall.type, COLORS.wall,
          sourcesA = [wall_draft], sourcesB = [ROIS.ptv_sbc], operator = 'Subtraction',
          marginsA = MARGINS.zero, marginsB = MARGIN.Expansion(0.5, 0.5, 1.5, 0.5, right_margin, left_margin)
        )
        pm_setup.add_targets([wall_draft])
      else:
        # For non-SIB we have a plain wall:
        wall = ROI.ROIWall(wall_name, ROIS.z_ptv_wall.type, COLORS.wall, t, 1.5, 0)
      pm_setup.add_targets([wall])


  def add_whole_breast(self, pm, pm_setup, side, boost, bilateral):
    """Adds ROIs for whole breast treatment.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
      boost (str): A string indicating use of a boost ('with').
      bilateral (bool): A boolean indicating whether the case is bilateral (True) or not (False).
    """
    self.add_sided_rois(pm, pm_setup, side)
    # Laterality suffix for targets for bilateral cases:
    suffix = ''
    if bilateral:
      if side == 'right':
        suffix = '_R'
      else:
        suffix = '_L'
    # ROIs are dependent on side:
    if side == 'right':
      breast_draft = ROIS.breast_r_draft
    else:
      breast_draft = ROIS.breast_l_draft
    # Targets:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name+suffix, ROIS.ctv.type, ROIS.ctv.color,
      sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv_c.name+suffix, ROIS.ptv.type, ROIS.ptv.color,
      sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    # Targets for whole breast:
    pm_setup.add_targets([ctv, ptv])
    # Add targets for boost (2 Gy x 8) if indicated:
    if boost == 'with':
      self.add_boost(pm_setup, side, ctv, ptv)


  def set_breaststring_density(self, pm):
    """Sets the density of the BreastString_L/R ROIs (if present) as air.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
    """
    breaststring_rois = []
    for roi_name in ['BreastString_L', 'BreastString_R']:
      try:
        if pm.RegionsOfInterest[roi_name]:
          breaststring_rois.append(roi_name)
      except:
        pass
    air = None
    for material in pm.Materials:
      if material.Name == 'Air':
        air = material
        break
    if air:
      for roi_name in breaststring_rois:
        pm.RegionsOfInterest[roi_name].SetRoiMaterial(Material=air)
