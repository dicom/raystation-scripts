# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS

# Definitions script for palliative treatments (prostate/prostate bed, with or without lymph nodes, normo/hypofractionated).
class DefPalliative(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
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
    self.add_oars(pm, examination, site, stereotactic, region)
    # Set up target volumes:
    self.add_targets(pm, examination, site, stereotactic, region, nr_targets, with_gtv, mask)
    # Add bone union ROI:
    bone = self.add_bone(pm, site)
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Change type to "Other":
    if bone:
      pm.RegionsOfInterest[bone.name].OrganData.OrganType = "Other"
    try:
      if pm.RegionsOfInterest['BowelBag_Draft']:
        pm.RegionsOfInterest['BowelBag_Draft'].OrganData.OrganType = "Other"
    except:
      pass
    # Exclude some ROIs from export:
    #exclude = ["L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "FemurHeadNeck_L", "FemurHeadNeck_R"]
    if bone:
      exclude = bone.sourcesA + bone.sourcesB
      for roi in exclude:
        PMF.exclude_roi_from_export(pm, roi.name)


  # Adds a bone union ROI:
  def add_bone(self, pm, site):
    bone = None
    bone_rois = []
    vertebrae_rois = []
    # Create "Bone" ROI Algebra:
    bone_candidates = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r]
    vertebrae_candidatates = [ROIS.l2, ROIS.l3, ROIS.l4, ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    for roi in bone_candidates:
      try:
        if pm.RegionsOfInterest[roi.name]:
          bone_rois.insert(0, roi)
      except:
        pass
    for roi in vertebrae_candidatates:
      try:
        if pm.RegionsOfInterest[roi.name]:
          vertebrae_rois.insert(0, roi)
      except:
        pass
    if len(bone_rois) > 0 and len(vertebrae_rois) > 0:
      bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = bone_rois, sourcesB = vertebrae_rois)
      site.add_oars([bone])
    return bone
  
  
  # Adds organ at risk ROIs to the site object.
  def add_oars(self, pm, examination, site, stereotactic, region):
    if stereotactic == 'yes':
      # Stereotactic:
      if region in ['col cervical', 'col thorax', 'col pelvis']:
        if region == 'col cervical':
          self.add_oars_neck(pm, examination, site)
          # SBRT specific OARs:
          site.add_oars([ROIS.skin, ROIS.spinal_cord, ROIS.spinal_cord_prv])
        elif region == 'col thorax':
          self.add_oars_thorax(pm, examination, site)
          # SBRT specific OARs:
          site.add_oars([ROIS.skin, ROIS.spinal_cord, ROIS.spinal_cord_prv])
        elif region == 'col pelvis':
          self.add_oars_pelvis(pm, examination, site)
          # SBRT specific OARs:
          site.add_oars([ROIS.colon, ROIS.skin, ROIS.small_bowel, ROIS.spinal_cord, ROIS.spinal_cord_prv])
      else:
        # Non-columna SBRT (assumed pelvis):
        self.add_oars_pelvis(pm, examination, site)
        # SBRT specific OARs:
        site.add_oars([ROIS.colon, ROIS.skin, ROIS.small_bowel])
    else:
      # Non-stereotactic:
      # Region:
      if region == 'head':
        self.add_oars_head(pm, examination, site)
      elif region == 'neck':
        self.add_oars_neck(pm, examination, site)
      elif region == 'thorax':
        self.add_oars_thorax(pm, examination, site)
      elif region == 'costa':
        self.add_oars_thorax_abdomen(pm, examination, site)
      elif region == 'thorax_abdomen':
        self.add_oars_thorax_abdomen(pm, examination, site)
      elif region == 'abdomen':
        self.add_oars_abdomen(pm, examination, site)
      elif region == 'abdomen_pelvis':
        self.add_oars_abdomen_pelvis(pm, examination, site)
      elif region == 'pelvis':
        self.add_oars_pelvis(pm, examination, site)
  
  
  # Adds abdomen OARs to the site object.
  def add_oars_abdomen(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "Heart": "Heart_pa_separate",
        "Kidney_L": "Kidney_L",
        "Kidney_R": "Kidney_R",
        "Liver": "Liver",
        "Lung_L": "Lung_L",
        "Lung_R": "Lung_R",
        "Pancreas": "Pancreas",
        "SpinalCanal": "SpinalCanal",
        "Spleen": "Spleen",
        "Stomach": "Stomach"
      },
      'Alesund Male Pelvic CT': {
        "A_DescendingAorta": "A_DescendingAorta",
        "BowelBag_Draft": "BowelBag",
        "V_InferiorVenaCava": "V_InferiorVenaCava"
      }
    })
    # Exclude abdominal organs from BowelBag (and remove Bladder reference as it is not relevant here):
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pancreas, ROIS.spleen, ROIS.stomach])
    ROIS.bowel_bag.sourcesB.remove(ROIS.bladder)
    # Non-DL OARs:
    site.add_oars([ROIS.bowel_bag, ROIS.kidneys, ROIS.lungs])
  
  
  # Adds abdomen/pelvis OARs to the site object.
  def add_oars_abdomen_pelvis(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "Bladder": "Bladder",
        "Kidney_L": "Kidney_L",
        "Kidney_R": "Kidney_R",
        "Liver": "Liver",
        "Pancreas": "Pancreas",
        "SpinalCanal": "SpinalCanal",
        "Spleen": "Spleen",
        "Stomach": "Stomach"
      },
      'Alesund Male Pelvic CT': {
        "A_DescendingAorta": "A_DescendingAorta",
        "AnalCanal": "AnalCanal",
        "BowelBag_Draft": "BowelBag",
        "CaudaEquina": "CaudaEquina",
        "Coccyx": "Coccyx",
        "FemurHeadNeck_L": "FemurHeadNeck_L",
        "FemurHeadNeck_R": "FemurHeadNeck_R",
        "L2": "L2",
        "L3": "L3",
        "L4": "L4",
        "L5": "L5",
        "PelvicGirdle_L": "PelvicGirdle_L",
        "PelvicGirdle_R": "PelvicGirdle_R",
        "Rectum": "Rectum",
        "Sacrum": "Sacrum",
        "V_InferiorVenaCava": "V_InferiorVenaCava"
      }
    })
    # Exclude abdominal organs from BowelBag:
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pancreas, ROIS.spleen, ROIS.stomach])
    # Non-DL OARs:
    site.add_oars([ROIS.bowel_bag, ROIS.kidneys])
  
  
  # Adds head OARs to the site object.
  def add_oars_head(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "Brain": "Brain",
        "Brainstem": "Brainstem",
        "Cochlea_L": "Cochlea_L",
        "Cochlea_R": "Cochlea_R",
        "Eye_L": "Eye_L",
        "Eye_R": "Eye_R",
        "LacrimalGland_L": "LacrimalGland_L",
        "LacrimalGland_R": "LacrimalGland_R",
        "Lens_L": "Lens_L",
        "Lens_R": "Lens_R",
        "OpticChiasm": "OpticChiasm",
        "OpticNerve_L": "OpticNerve_L",
        "OpticNerve_R": "OpticNerve_R",
        "OralCavity": "OralCavity",
        "Parotid_L": "ParotidGland_L",
        "Parotid_R": "ParotidGland_R",
        "Pituitary": "Pituitary",
        "SpinalCanal": "SpinalCanal",
        "SubmandGland_L": "SubmandibularGland_L",
        "SubmandGland_R": "SubmandibularGland_R"
      }
    })
    # Non-DL OARs:
    site.add_oars([ROIS.parotids, ROIS.submands])
  
  
  # Adds neck OARs to the site object.
  def add_oars_neck(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "BrachialPlexus_L": "Brachial_Plexus_L",
        "BrachialPlexus_R": "Brachial_Plexus_R",
        "Brain": "Brain",
        "Brainstem": "Brainstem",
        "Esophagus": "Esophagus",
        "OpticChiasm": "OpticChiasm",
        "OpticNerve_L": "OpticNerve_L",
        "OpticNerve_R": "OpticNerve_R",
        "OralCavity": "OralCavity",
        "Parotid_L": "ParotidGland_L",
        "Parotid_R": "ParotidGland_R",
        "Pituitary": "Pituitary",
        "SpinalCanal": "SpinalCanal",
        "SubmandGland_L": "SubmandibularGland_L",
        "SubmandGland_R": "SubmandibularGland_R",
        "ThyroidGland": "ThyroidGland",
        "Trachea": "Trachea_1cm_sup_carina"
      }
    })
    # Non-DL OARs:
    site.add_oars([ROIS.parotids, ROIS.submands])
  
  
  # Adds pelvis OARs to the site object.
  def add_oars_pelvis(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "Bladder": "Bladder",
        "Kidney_L": "Kidney_L",
        "Kidney_R": "Kidney_R",
        "Liver": "Liver"
      },
      'Alesund Male Pelvic CT': {
        "AnalCanal": "AnalCanal",
        "BowelBag_Draft": "BowelBag",
        "CaudaEquina": "CaudaEquina",
        "Coccyx": "Coccyx",
        "FemurHeadNeck_L": "FemurHeadNeck_L",
        "FemurHeadNeck_R": "FemurHeadNeck_R",
        "L2": "L2",
        "L3": "L3",
        "L4": "L4",
        "L5": "L5",
        "PelvicGirdle_L": "PelvicGirdle_L",
        "PelvicGirdle_R": "PelvicGirdle_R",
        "Rectum": "Rectum",
        "Sacrum": "Sacrum"
      }
    })
    # Non-DL OARs:
    site.add_oars([ROIS.kidneys, ROIS.bowel_bag])
  
  
  # Adds thorax OARs to the site object.
  def add_oars_thorax(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "A_AorticArch": "A_Aorta_arcus",
        "A_AscendingAorta": "A_Aorta_Ascen",
        "A_DescendingAorta": "A_Aorta_Desc",
        "A_LAD": "A_LAD",
        "BronchusMain_L": "Bronchus_Main_L",
        "BronchusMain_R": "Bronchus_Main_R",
        "BronchusIntermedius": "Bronchus_InterM",
        "Carina": "Carina",
        "Esophagus": "Esophagus",
        "Heart": "Heart_pa_separate",
        "Kidney_L": "Kidney_L",
        "Kidney_R": "Kidney_R",
        "Liver": "Liver",
        "Lung_L": "Lung_L",
        "Lung_R": "Lung_R",
        "Pancreas": "Pancreas",
        "SpinalCanal": "SpinalCanal",
        "Spleen": "Spleen",
        "Stomach": "Stomach",
        "ThyroidGland": "ThyroidGland",
        "Trachea": "Trachea_1cm_sup_carina",
        "V_InferiorVenaCava": "V_Cava_inferior",
        "V_SuperiorVenaCava": "V_Cava_superior"
      }
    })
    # Non-DL OARs:
    site.add_oars([ROIS.greatves, ROIS.kidneys, ROIS.lungs])
  
  
  # Adds thorax/abdomen OARs to the site object.
  def add_oars_thorax_abdomen(self, pm, examination, site):
    # DL OARs:
    examination.RunDeepLearningSegmentationWithCustomRoiNames(ModelAndRoiNames={
      'RSL DLS CT': {
        "A_LAD": "A_LAD",
        "A_AorticArch": "A_Aorta_arcus",
        "A_AscendingAorta": "A_Aorta_Ascen",
        "A_DescendingAorta": "A_Aorta_Desc",
        "Esophagus": "Esophagus",
        "Heart": "Heart_pa_separate",
        "Kidney_L": "Kidney_L",
        "Kidney_R": "Kidney_R",
        "Liver": "Liver",
        "Lung_L": "Lung_L",
        "Lung_R": "Lung_R",
        "Pancreas": "Pancreas",
        "SpinalCanal": "SpinalCanal",
        "Spleen": "Spleen",
        "Stomach": "Stomach",
        "Trachea": "Trachea_1cm_sup_carina",
        "V_InferiorVenaCava": "V_Cava_inferior",
        "V_SuperiorVenaCava": "V_Cava_superior"
      },
      'Alesund Male Pelvic CT': {
        "BowelBag_Draft": "BowelBag",
      }
    })
    # Exclude abdominal organs from BowelBag (and remove Bladder reference as it is not relevant here):
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pancreas, ROIS.spleen, ROIS.stomach])
    ROIS.bowel_bag.sourcesB.remove(ROIS.bladder)
    # Non-DL OARs:
    site.add_oars([ROIS.bowel_bag, ROIS.greatves, ROIS.kidneys, ROIS.lungs])
  
  
  # Adds target ROIs to the site object.
  def add_targets(self, pm, examination, site, stereotactic, region, nr_targets, with_gtv, mask):
    # Determine PTV margins:
    ptv_margin = self.determine_ptv_margin(stereotactic, region, with_gtv, mask)
    if stereotactic == 'yes':
      # Stereotactic:
      if region in ['col cervical', 'col thorax', 'col pelvis']:
        # Targets:
        ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_med, ROIS.gtv, margins = MARGINS.uniform_3mm_expansion)
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB=[ROIS.vb], operator='Union', marginsA = ptv_margin, marginsB = ptv_margin)
        ptv_gtv = ROI.ROIAlgebra(ROIS.ptv_gtv.name, ROIS.ptv_gtv.type, COLORS.ptv_med, sourcesA = [ptv], sourcesB = [ROIS.gtv], operator='Subtraction')
        ptv_spinal = ROI.ROIAlgebra(ROIS.ptv_spinal.name, ROIS.ptv_spinal.type, COLORS.ptv_med, sourcesA = [ptv], sourcesB = [ROIS.spinal_cord_prv], operator='Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_1mm_expansion)
        site.add_targets([ROIS.gtv, ROIS.vb, ptv_gtv, ptv_spinal, ctv, ptv])
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        site.add_oars([ROIS.spinal_cord_prv, wall_ptv])
      else:
        # Non-columna SBRT:
        # Targets:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, ROIS.gtv, margins = ptv_margin)
        site.add_targets([ROIS.gtv, ptv])
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        site.add_oars([wall_ptv])
    else:
      # Conventional RT:
      if nr_targets == 1:
        # A single target:
        if with_gtv == 'with':
          ctv = ROIS.ctv_ext
          site.add_targets([ROIS.gtv, ctv])
        else:
          ctv = ROIS.ctv_underived
          site.add_targets([ctv])
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_targets([ptv])
      else:
        # Multiple targets (2 or 3):
        gtvs = []
        ctvs = []
        ptvs = []
        if with_gtv=='with':
          # With GTV:
          for i in range(0, nr_targets):
            gtvs.append(ROI.ROI('GTV'+str(i+1), 'Gtv', COLORS.gtv))
            ctvs.append(ROI.ROIAlgebra(ROIS.ctv.name+str(i+1), ROIS.ctv1.type, ROIS.ctv.color, sourcesA = [gtvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction))
            ptvs.append(ROI.ROIAlgebra(ROIS.ptv.name+str(i+1), ROIS.ptv1.type, ROIS.ptv.color, sourcesA = [ctvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction))
          # GTV union target volume:
          gtvs.append(ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[gtvs[0]], sourcesB=gtvs[1:]))
          site.add_targets(gtvs)
        else:
          # Without GTV:
          for i in range(0, nr_targets):
            ctvs.append(ROI.ROI('CTV'+str(i+1), 'Ctv', COLORS.ctv))
            ptvs.append(ROI.ROIAlgebra(ROIS.ptv.name+str(i+1), ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction))
        # Union target volumes:
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ctvs[0]], sourcesB=ctvs[1:])
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptvs[0]], sourcesB=ptvs[1:])
        ctvs.append(ctv)
        ptvs.append(ptv)
        site.add_targets(ctvs + ptvs)
      # Add PTV wall:
      wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
      site.add_oars([wall_ptv])
  
  
  # Determines the PTV margin to be used for the given region and target type (soft tissue or bone).
  def determine_ptv_margin(self, stereotactic, region, with_gtv, mask):
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
