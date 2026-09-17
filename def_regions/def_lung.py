# Import local files:
import colors as COLORS
import def_oars as DEF
import def_quality_control as DEFQC
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS


class DefLung(object):
  """Configuration of ROIs used for cases of lung cancer."""

  def __init__(self, pm, examination, ss, choices, pm_setup):
    """Initializes the lung case configuration with the relevant RayStation instances and the user's GUI selections.

    Based on the settings given, a set of ROIs (Targets, OARs & Others) are created on the patient case in RayStation.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      examination (PyScriptObject): The RayStation Examination instance.
      ss (PyScriptObject): The RayStation StructureSet instance.
      choices (list): The choices made by the user in the definitions script GUI.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, pm_setup)
    # Choice 1: Intent (curative or palliative)
    intent = choices[1]
    if intent == 'curative':
      # Curative:
      # Choice 2: Diagnosis
      diagnosis = choices[2]
      if diagnosis == '4dct':
        # Curative (with 4DCT or DIBH):
        self.add_curative_4dct_dibh(pm, pm_setup)
      elif diagnosis == 'freebreath':
        # Curative (free breath):
        self.add_curative_free_breath(pm, pm_setup)
      elif diagnosis =='postop':
        # Curative post operative:
        self.add_curative_postop(pm, pm_setup)
    elif intent == 'palliative':
      # Palliative:
      # Choice 2: 4DCT - with or without?
      with_4dct = choices[2]
      if with_4dct == 'with':
        # Palliative 4DCT:
        self.add_palliative_4dct(pm, pm_setup)
      else:
        # Palliative free breathing:
        self.add_palliative_free_breath(pm, pm_setup)
    elif intent == 'stereotactic':
      # Choice 2: Side - left or right?
      side = choices[2]
      # Choice 3: Number of target volumes?
      nr_targets = int(choices[3])
      # Stereotactic:
      self.add_stereotactic_lung(pm, examination, pm_setup, side, nr_targets)
    # Create all targets and OARs in RayStation:
    pm_setup.create_rois()
    # Change type to 'Other' for selected ROIs:
    for roi_name in [ROIS.mask_ptv, ROIS.mask_ptv1, ROIS.mask_ptv2, ROIS.mask_ptv3]:
      try:
        if pm.RegionsOfInterest[roi_name]:
          if pm.RegionsOfInterest[roi_name].OrganData.OrganType != "Other":
            pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      except:
        pass


  def add_common_rois(self, pm, pm_setup):
    """Adds ROIs for this particular treatment site that are common across all scopes.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # DL OARs:
    pm_setup.add_oars([ROIS.a_aortic_arch, ROIS.a_ascending_aorta, ROIS.a_descending_aorta, ROIS.a_lad,
      ROIS.brachial_plexus_l, ROIS.brachial_plexus_r, ROIS.bronchus_intermedius, ROIS.bronchus_main_l,
      ROIS.bronchus_main_r, ROIS.carina, ROIS.esophagus, ROIS.heart, ROIS.kidney_l, ROIS.kidney_r, ROIS.liver,
      ROIS.lung_l, ROIS.lung_r, ROIS.pancreas, ROIS.spinal_canal, ROIS.spleen, ROIS.sternum, ROIS.stomach,
      ROIS.thyroid, ROIS.trachea, ROIS.v_inferior_vena_cava, ROIS.v_superior_vena_cava
    ])
    # Non-DL OARs:
    pm_setup.add_oars([ROIS.a_pulmonary, ROIS.greatves, ROIS.lungs])


  def add_curative_4dct_dibh(self, pm, pm_setup):
    """Adds ROIs for curative 4DCT or DIBH cases.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Targets:
    igtv = ROI.ROIAlgebra(
      ROIS.igtv.name, ROIS.igtv.type, ROIS.gtv.color, sourcesA=[ROIS.igtv_p], sourcesB=[ROIS.igtv_n]
    )
    ictv_p = ROI.ROIExpanded(ROIS.ictv_p.name, ROIS.ictv_p.type, COLORS.ctv_high,
      source = ROIS.igtv_p, margins = MARGINS.uniform_5mm_expansion
    )
    ictv_n = ROI.ROIExpanded(ROIS.ictv_n.name, ROIS.ictv_n.type, COLORS.ctv_high,
      source = ROIS.igtv_n, margins = MARGINS.uniform_5mm_expansion
    )
    ictv = ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color,
      sourcesA=[ictv_p, ictv_n], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high,
      sourcesA = [ictv], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ROIS.igtv_p, ROIS.igtv_n, igtv, ictv_p, ictv_n, ictv, ptv])
    # Other derived ROIs:
    lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs,
      sourcesA = [ROIS.lungs], sourcesB = [igtv], operator='Subtraction'
    )
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv,
      sourcesA=[ROIS.lungs, ptv], sourcesB=[igtv], operator='Subtraction', operatorA = 'Intersection'
    )
    pm_setup.add_oars([lungs_igtv, water])


  def add_curative_free_breath(self, pm, pm_setup):
    """Adds ROIs for curative free breath cases.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Targets:
    gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n])
    ctv_p = ROI.ROIExpanded(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv_high,
      source = ROIS.gtv_p, margins = MARGINS.uniform_5mm_expansion
    )
    ctv_n = ROI.ROIExpanded(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.ctv_high,
      source = ROIS.gtv_n, margins = MARGINS.uniform_5mm_expansion
    )
    ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color,
      sourcesA=[ctv_p, ctv_n], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high,
      sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ROIS.gtv_p, ROIS.gtv_n, gtv, ctv_p, ctv_n, ctv, ptv])
    # Other derived ROIs:
    lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_gtv.name, ROIS.lungs_gtv.type, COLORS.lungs,
      sourcesA = [ROIS.lungs], sourcesB = [gtv], operator='Subtraction'
    )
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv,
      sourcesA=[ROIS.lungs, ptv], sourcesB=[gtv], operator='Subtraction', operatorA = 'Intersection'
    )
    pm_setup.add_oars([lungs_gtv, water])


  def add_curative_postop(self, pm, pm_setup):
    """Adds ROIs for curative post-operation cases.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Targets:
    ctv = ROI.ROI(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB = [ROIS.external],
      operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ctv, ptv])
    # Other derived ROIs:
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv,
      sourcesA=[ROIS.lungs, ptv], sourcesB=[ctv], operator='Subtraction', operatorA = 'Intersection'
    )
    pm_setup.add_oars([water])


  def add_palliative_4dct(self, pm, pm_setup):
    """Adds ROIs for palliative 4DCT cases.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Targets:
    ictv = ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color,
      sourcesA=[ROIS.igtv], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color,
      sourcesA=[ictv], sourcesB = [ROIS.external], operator = 'Intersection',
      marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ROIS.igtv, ictv, ptv])
    # Other derived ROIs:
    lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs,
      sourcesA = [ROIS.lungs], sourcesB = [ROIS.igtv], operator='Subtraction'
    )
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv,
      sourcesA=[ROIS.lungs, ptv], sourcesB=[ROIS.igtv], operator='Subtraction', operatorA = 'Intersection'
    )
    pm_setup.add_oars([lungs_gtv, water])


  def add_palliative_free_breath(self, pm, pm_setup):
    """Adds ROIs for palliative free breath cases.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
    """
    # Targets:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ROIS.gtv], sourcesB = [ROIS.external],
      operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB = [ROIS.external],
      operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction
    )
    pm_setup.add_targets([ROIS.gtv, ctv, ptv])
    # Other derived ROIs:
    lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_gtv.name, ROIS.lungs_gtv.type, COLORS.lungs,
      sourcesA = [ROIS.lungs], sourcesB = [ROIS.gtv], operator='Subtraction'
    )
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv,
      sourcesA=[ROIS.lungs, ptv], sourcesB=[ROIS.gtv], operator='Subtraction', operatorA = 'Intersection'
    )
    pm_setup.add_oars([lungs_gtv, water])


  def add_stereotactic_lung(self, pm, examination, pm_setup, side, nr_targets):
    """Adds ROIs for SBRT cases.

    Args:
      pm (PyScriptObject): The RayStation PatientModel instance.
      examination (PyScriptObject): The RayStation Examination instance.
      pm_setup (PatientModelSetup): The patient model setup to be used for this case.
      side (str): A string indicating target side ('left' or 'right').
      nr_targets (int): The number of targets to setup.
    """
    # Slice thickness quality control:
    DEFQC.test_slice_thickness(examination, 0.2, "Lunge SBRT")
    # Add a POI for breath hold measurement:
    PMF.create_poi(pm, examination, 'Pust', 'Marker', 'Magenta')
    # Non-DL OARs:
    pm_setup.add_oars(DEF.lung_stereotactic_oars)
    # Side dependent OARs:
    if side == 'right':
      pm_setup.add_oars([ROIS.ribs_r])
    elif side == 'left':
      pm_setup.add_oars([ROIS.ribs_l])
    # Targets:
    if nr_targets == 1:
      # Single target:
      mask_ptv = ROI.ROIAlgebra(ROIS.mask_ptv.name, ROIS.mask_ptv.type, COLORS.mask_ptv,
        sourcesA = [ROIS.iptv_gtv], sourcesB = [ROIS.chestwall], operator='Subtraction'
      )
      pm_setup.add_targets([ROIS.igtv, ROIS.iptv_gtv, ROIS.wall_ptv, mask_ptv])
      pm_setup.add_oars([ROIS.lungs_igtv])
    else:
      # Multiple targets:
      igtvs = []
      ptvs = []
      walls = []
      masks = []
      for i in range(0, nr_targets):
        # Targets:
        igtvs.append(ROI.ROI('IGTV'+str(i+1), 'Gtv', ROIS.igtv.color))
        ptvs.append(ROI.ROIExpanded(ROIS.ptv.name+str(i+1), ROIS.ptv.type, COLORS.ptv, igtvs[-1],
          margins = MARGINS.uniform_5mm_expansion)
        )
        # Other derived ROIs:
        walls.append(ROI.ROIWall("zPTV"+str(i+1)+"_Wall", ROIS.z_ptv_wall.type, COLORS.wall, ptvs[-1], 1, 0))
        masks.append(ROI.ROIAlgebra(ROIS.mask_ptv.name+str(i+1), ROIS.mask_ptv.type, COLORS.mask_ptv,
          sourcesA = [ptvs[-1]], sourcesB = [ROIS.chestwall], operator='Subtraction')
        )
      # Union target volumes:
      igtv = ROI.ROIAlgebra(ROIS.igtv.name, ROIS.igtv.type, ROIS.igtv.color, sourcesA=[igtvs[0]], sourcesB=igtvs[1:])
      ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptvs[0]], sourcesB=ptvs[1:])
      igtvs.append(igtv)
      ptvs.append(ptv)
      # Targets:
      pm_setup.add_targets(igtvs + ptvs)
      # Other derived ROIs:
      lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, 'Organ', COLORS.lungs,
        sourcesA=[ROIS.lungs], sourcesB=[igtv], operator = 'Subtraction'
      )
      pm_setup.add_oars([lungs_igtv] + walls + masks)
