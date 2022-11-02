# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS


# Definitions script for breast treatments (local/locoregional, with/without IMN, with/without boost).
class DefBreast(object):


  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Local/Regional/Regional with IMN
    region = choices[1]
    # Choice 2: Side - Left or right?
    side = choices[2]
    # Region:
    if region == 'partial':
      # Partial breast only:
      self.add_partial_breast(pm, examination, site, side)
    else:
      # Whole breast (with or without regional nodes):
      # Choice 3: With our without boost?
      boost = choices[3]
      if region == 'whole':
        self.add_whole_breast(pm, examination, site, side, boost, bilateral=False, include_common_oars=True)
      elif region in ['regional', 'regional_imn']:
        # Regional breast (with or without IMN):
        if region == 'regional_imn':
          self.add_regional_breast(pm, examination, site, side, boost, bilateral=False, include_common_oars=True, include_imn=True)
        else:
          self.add_regional_breast(pm, examination, site, side, boost, bilateral=False, include_common_oars=True, include_imn=False)
      else:
        # Bilateral:
        bilateral_left_side_target = choices[2]
        bilateral_right_side_target = choices[3]
        if bilateral_left_side_target == 'bilateral_left_whole':
          self.add_whole_breast(pm, examination, site, 'left', boost, bilateral=True, include_common_oars=True)
        else:
          self.add_regional_breast(pm, examination, site, 'left', boost, bilateral=True, include_common_oars=True, include_imn=True)
        if bilateral_right_side_target == 'bilateral_right_whole':
          self.add_whole_breast(pm, examination, site, 'right', boost, bilateral=True, include_common_oars=False)
        else:
          self.add_regional_breast(pm, examination, site, 'right', boost, bilateral=True, include_common_oars=False, include_imn=True)
        # Targets (L+R union):
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.ctv_l], sourcesB = [ROIS.ctv_r], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ROIS.ptvc_l, ROIS.ptvc_r], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_targets([ctv, ptv])
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Modify ROI types:
    for r in ['PTV_Robustness', 'PTV_Robustness_L', 'PTV_Robustness_R']:
      try:
        pm.RegionsOfInterest[r].Type = "Control"
        pm.RegionsOfInterest[r].OrganData.OrganType = "Other"
      except:
        pass
    # Override the density of the breast string to 'Air' (since it is not present on treatments):
    # root and db are not reliable variables obviously. We need some reliable way of getting this database parameter...
    '''
    if side == 'right':
      #pm.RegionsOfInterest['BreastString_R'].SetRoiMaterial(Material=pm.Materials[4])      
      pm.RegionsOfInterest['BreastString_R'].SetRoiMaterial(Material=root.TemplateMaterials["'Adipose' 'Air' 'Aluminum 1' 'Aluminum 2' 'Brass' 'Carbon fiber' 'Cartilage' 'Cork' 'Gold' 'Iron' 'Lead' 'Muscle' 'PlasticAE C-552' 'PlasticBE B-100' 'PlasticTE A-150' 'PMI foam' 'PMMA' 'Polystyrene' 'PVC' 'RW3' 'Steel' 'Titanium' 'Water' 'Wax' 'Bone 1' 'Bone 2' 'Lung' 'Aluminum2 Bone1' 'Cartilage1 Bone2' 'Cartilage2 Bone1' 'Cerrobend' 'PLA' 'Polyethylene' 'LiF PE' 'Cranial bone' 'Brain' 'Eye lens' 'Skin' 'Tissue soft' 'Heart' 'Kidney' 'Liver' 'Spleen' 'LN10' 'SB5' 'WT1' 'RB2' 'Silicon' 'Tantalum' "].Materials[1])
    else:
      #pm.RegionsOfInterest['BreastString_L'].SetRoiMaterial(Material=pm.Materials[4])
      pm.RegionsOfInterest['BreastString_L'].SetRoiMaterial(Material=root.TemplateMaterials["'Adipose' 'Air' 'Aluminum 1' 'Aluminum 2' 'Brass' 'Carbon fiber' 'Cartilage' 'Cork' 'Gold' 'Iron' 'Lead' 'Muscle' 'PlasticAE C-552' 'PlasticBE B-100' 'PlasticTE A-150' 'PMI foam' 'PMMA' 'Polystyrene' 'PVC' 'RW3' 'Steel' 'Titanium' 'Water' 'Wax' 'Bone 1' 'Bone 2' 'Lung' 'Aluminum2 Bone1' 'Cartilage1 Bone2' 'Cartilage2 Bone1' 'Cerrobend' 'PLA' 'Polyethylene' 'LiF PE' 'Cranial bone' 'Brain' 'Eye lens' 'Skin' 'Tissue soft' 'Heart' 'Kidney' 'Liver' 'Spleen' 'LN10' 'SB5' 'WT1' 'RB2' 'Silicon' 'Tantalum' "].Materials[1])
    '''
    # Exclude some ROIs from export:
    for roi_name in [ROIS.breast_l_draft.name, ROIS.breast_r_draft.name]:
      PMF.exclude_roi_from_export(pm, roi_name)
    # Only some patients have breast string. Delete the ROI if its volume is less than 0.5 cm^3:
    for rg in ss.RoiGeometries:
      if rg.OfRoi.Name in ['BreastString_L', 'BreastString_R']:
        if rg.GetRoiVolume() < 0.5:
          # Delete the ROI, as it seems like this patient didnt actually have a breast string:
          pm.RegionsOfInterest[rg.OfRoi.Name].DeleteRoi()

  
  # Adds partial breast (left or right) ROIs to the site object.
  def add_partial_breast(self, pm, examination, site, side):
    # ROIs are dependent on side:
    if side == 'right':
      breast_draft = ROIS.breast_r_draft
      sb = ROIS.surgical_bed_r
      # DL model for right sided breast:
      examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_R", "Breast_R_Draft", "Clips_R", "Breast_L_Draft", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_R", "Trachea"])
      #breast = ROI.ROIAlgebra(ROIS.breast_r.name, ROIS.breast_r.type, ROIS.breast_r.color, sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      breast = ROIS.breast_r
      # Change type to 'Other' for selected ROIs:
      for roi_name in ['Clips_R','BreastString_R','Breast_L_Draft','Breast_R_Draft','SurgicalBed_R']:
        if pm.RegionsOfInterest[roi_name].OrganData.OrganType != "Other":
          pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      # OARs:
      site.add_oars([ROIS.breast_l, ROIS.breast_r, ROIS.lungs])
    else:
      breast_draft = ROIS.breast_l_draft
      sb = ROIS.surgical_bed_l
      # DL model for left sided whole breast:
      examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_L", "Breast_L_Draft", "Clips_L", "Breast_R_Draft", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_L", "Trachea"])
      #breast = ROI.ROIAlgebra(ROIS.breast_l.name, ROIS.breast_l.type, ROIS.breast_l.color, sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      breast = ROIS.breast_l
      # Change type to 'Other' for selected ROIs:
      for roi_name in ['Clips_L','BreastString_L','Breast_L_Draft','Breast_R_Draft','SurgicalBed_L']:
        # Some of these ROIs may not always be defined, and give an error:
        try:
          pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
        except:
          pass
      # OARs:
      site.add_oars([ROIS.breast_l, ROIS.breast_r, ROIS.lungs])
    # Rename DL ROI(s):
    pm.RegionsOfInterest['SpinalCanalFull'].Name = 'SpinalCanal'
    # Targets:
    ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [sb], sourcesB = [breast], operator = 'Intersection', marginsA = MARGINS.uniform_15mm_expansion, marginsB = MARGINS.zero)
    ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    # Targets for whole breast:
    site.add_targets([ctv_sb, ptv_sbc])
  
  
  # Adds regional breast (left or right) ROIs to the site object.
  def add_regional_breast(self, pm, examination, site, side, boost, bilateral, include_common_oars, include_imn):
    # Laterality suffix for targets for bilateral cases:
    suffix = ''
    if bilateral:
      if side == 'right':
        suffix = '_R'
      else:
        suffix = '_L'
    # Side dependent OARs and support structures for regional treatment:
    if side == 'right':
      # Non-DL OARs:
      site.add_oars([ROIS.liver, ROIS.scalene_muscle_r, ROIS.artery1_r, ROIS.artery2_r, ROIS.artery3_r, ROIS.vein1_r, ROIS.vein2_r, ROIS.vein3_r])
      # DL model for right sided regional breast:
      if include_common_oars:
        # Do not include contralateral breast for bilateral cases:
        if bilateral:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_R", "Breast_R_Draft", "Clips_R", "Esophagus", "Heart", "HumeralHead_R", "LN_Ax_L1_R", "LN_Ax_L2_R", "LN_Ax_L3_R", "LN_Ax_L4_R", "LN_Ax_Pectoral_R", "LN_IMN_R", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_R", "ThyroidGland", "Trachea"])
        else:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_R", "Breast_R_Draft", "Clips_R", "Breast_L_Draft", "Esophagus", "Heart", "HumeralHead_R", "LN_Ax_L1_R", "LN_Ax_L2_R", "LN_Ax_L3_R", "LN_Ax_L4_R", "LN_Ax_Pectoral_R", "LN_IMN_R", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_R", "ThyroidGland", "Trachea"])
      else:
        examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["BreastString_R", "Breast_R_Draft", "Clips_R", "HumeralHead_R", "LN_Ax_L1_R", "LN_Ax_L2_R", "LN_Ax_L3_R", "LN_Ax_L4_R", "LN_Ax_Pectoral_R", "LN_IMN_R", "SurgicalBed_R"])
      # Rename DL ROI(s):
      try:
        pm.RegionsOfInterest['SpinalCanalFull'].Name = 'SpinalCanal'
      except:
        pass
      # Change type to 'Other' for selected ROIs:
      for roi_name in ['Clips_R','BreastString_R','Breast_L_Draft','LN_Ax_Pectoral_R','LN_Ax_L1_R','LN_Ax_L2_R','LN_Ax_L3_R','LN_Ax_L4_R','Breast_R_Draft','LN_IMN_R','SurgicalBed_R']:
        try:
          pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
        except:
          pass
      # Targets:
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name+suffix, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name+suffix, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      if include_imn:
        imn = ROIS.imn_r
      # OARs:
      if bilateral:
        site.add_oars([ROIS.lungs])
      else:
        site.add_oars([ROIS.breast_l, ROIS.lungs])
    else:
      # DL model for left sided regional breast:
      if include_common_oars:
        # Do not include contralateral breast for bilateral cases:
        if bilateral:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_Carotid_L", "A_LAD", "A_Subclavian_L+A_Axillary_L", "BreastString_L", "Breast_L_Draft", "Clips_L", "Esophagus", "Heart", "HumeralHead_L", "LN_Ax_L1_L", "LN_Ax_L2_L", "LN_Ax_L3_L", "LN_Ax_L4_L", "LN_Ax_Pectoral_L", "LN_IMN_L", "Lung_L", "Lung_R", "ScaleneMusc_Ant_L", "SpinalCanalFull", "Sternum", "SurgicalBed_L", "ThyroidGland", "Trachea", "V_Brachioceph_L", "V_Jugular_L", "V_Subclavian_L+V_Axillary_L"])
        else:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_Carotid_L", "A_LAD", "A_Subclavian_L+A_Axillary_L", "BreastString_L", "Breast_L_Draft", "Clips_L", "Breast_R_Draft", "Esophagus", "Heart", "HumeralHead_L", "LN_Ax_L1_L", "LN_Ax_L2_L", "LN_Ax_L3_L", "LN_Ax_L4_L", "LN_Ax_Pectoral_L", "LN_IMN_L", "Lung_L", "Lung_R", "ScaleneMusc_Ant_L", "SpinalCanalFull", "Sternum", "SurgicalBed_L", "ThyroidGland", "Trachea", "V_Brachioceph_L", "V_Jugular_L", "V_Subclavian_L+V_Axillary_L"])
      else:
        examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_Carotid_L", "A_Subclavian_L+A_Axillary_L", "BreastString_L", "Breast_L_Draft", "Clips_L", "HumeralHead_L", "LN_Ax_L1_L", "LN_Ax_L2_L", "LN_Ax_L3_L", "LN_Ax_L4_L", "LN_Ax_Pectoral_L", "LN_IMN_L", "ScaleneMusc_Ant_L", "SurgicalBed_L", "V_Brachioceph_L", "V_Jugular_L", "V_Subclavian_L+V_Axillary_L"])
      # Rename DL ROI(s) (note that this ROI doesn't exist if this has been exectued without include_common_oars):
      try:
        pm.RegionsOfInterest['SpinalCanalFull'].Name = 'SpinalCanal'
      except:
        pass
      # Change type to 'Other' for selected ROIs:
      for roi_name in ['Clips_L','BreastString_L','Breast_L_Draft','LN_Ax_Pectoral_L','LN_Ax_L1_L','LN_Ax_L2_L','LN_Ax_L3_L','LN_Ax_L4_L','Breast_R_Draft','ScaleneMusc_Ant_L','A_Subclavian_L+A_Axillary_L','A_Carotid_L','V_Brachioceph_L','V_Subclavian_L+V_Axillary_L','V_Jugular_L','LN_IMN_L','SurgicalBed_L']:
        try:
          pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
        except:
          pass
      # Targets:
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name+suffix, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name+suffix, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      if include_imn:
        imn = ROIS.imn_l
      # OARs:
      if bilateral:
        site.add_oars([ROIS.lungs])
      else:
        site.add_oars([ROIS.breast_r, ROIS.lungs])
    # Common targets for left and right:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name+suffix, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ctv_n], sourcesB = [ctv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv_p = ROI.ROIAlgebra(ROIS.ptv_pc.name+suffix, ROIS.ptv_pc.type, ROIS.ptv.color, sourcesA = [ctv_p], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    ptv_n = ROI.ROIAlgebra(ROIS.ptv_nc.name+suffix, ROIS.ptv_nc.type, ROIS.ptv.color, sourcesA = [ctv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv_c.name+suffix, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ptv_n], sourcesB = [ptv_p], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    # IMN:
    if include_imn:
      ctv_n.sourcesA.extend([imn])
    # Robustness evaluation volume:
    if side == 'right':
      ptv_robustness = ROI.ROIExpanded('PTV_Robustness'+suffix, ROIS.ptv.type, COLORS.ptv_breast, ptv_p, margins = MARGINS.breast_right_robustness)
    else:
      ptv_robustness = ROI.ROIExpanded('PTV_Robustness'+suffix, ROIS.ptv.type, COLORS.ptv_breast, ptv_p, margins = MARGINS.breast_left_robustness)
    # Common targets for all regional:
    site.add_targets([ctv_p, ctv_n, ctv, ptv_p, ptv_n, ptv, ptv_robustness])
    # Add targets for boost (2 Gy x 8) if indicated:
    if boost == 'with':
      self.add_boost(site, side, ctv)
  
  
  # Adds whole breast (left or right) ROIs to the site object.
  def add_whole_breast(self, pm, examination, site, side, boost, bilateral, include_common_oars):
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
      # DL model for right sided whole breast:
      if include_common_oars:
        # Do not include contralateral breast for bilateral cases:
        if bilateral:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_R", "Breast_R_Draft", "Clips_R", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_R", "Trachea"])
        else:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_R", "Breast_R_Draft", "Clips_R", "Breast_L_Draft", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_R", "Trachea"])
      else:
        examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Right Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["BreastString_R", "Breast_R_Draft", "Clips_R", "SurgicalBed_R"])
      # Change type to 'Other' for selected ROIs:
      for roi_name in ['Clips_R','BreastString_R','Breast_L_Draft','Breast_R_Draft','SurgicalBed_R']:
        if pm.RegionsOfInterest[roi_name].OrganData.OrganType != "Other":
          pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      # OARs:
      if bilateral:
        site.add_oars([ROIS.liver, ROIS.lungs])
      else:
        site.add_oars([ROIS.breast_l, ROIS.liver, ROIS.lungs])
    else:
      breast_draft = ROIS.breast_l_draft
      # DL model for left sided whole breast:
      if include_common_oars:
        # Do not include contralateral breast for bilateral cases:
        if bilateral:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_L", "Breast_L_Draft", "Clips_L", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_L", "Trachea"])
        else:
          examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "BreastString_L", "Breast_L_Draft", "Clips_L", "Breast_R_Draft", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "SurgicalBed_L", "Trachea"])
      else:
        examination.RunOarSegmentation(ModelName="St. Olavs-Ålesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["BreastString_L", "Breast_L_Draft", "Clips_L", "SurgicalBed_L"])
      # Change type to 'Other' for selected ROIs:
      for roi_name in ['Clips_L','BreastString_L','Breast_L_Draft','Breast_R_Draft','SurgicalBed_L']:
        # Some of these ROIs may not always be defined, and give an error:
        try:
          pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
        except:
          pass
      # OARs:
      if bilateral:
        site.add_oars([ROIS.lungs])
      else:
        site.add_oars([ROIS.breast_r, ROIS.lungs])
    try:
      # Rename the spinal canal ROI (note that this ROI doesn't exist if this has been exectued without include_common_oars):
      pm.RegionsOfInterest['SpinalCanalFull'].Name = 'SpinalCanal'
    except:
      pass
    # Targets:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name+suffix, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [breast_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv_c.name+suffix, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    # Robustness evaluation volume:
    if side == 'right':
      ptv_robustness = ROI.ROIExpanded('PTV_Robustness'+suffix, ROIS.ptv.type, COLORS.ptv_breast, ptv, margins = MARGINS.breast_right_robustness)
    else:
      ptv_robustness = ROI.ROIExpanded('PTV_Robustness'+suffix, ROIS.ptv.type, COLORS.ptv_breast, ptv, margins = MARGINS.breast_left_robustness)
    # Targets for whole breast:
    site.add_targets([ctv, ptv, ptv_robustness])
    # Add targets for boost (2 Gy x 8) if indicated:
    if boost == 'with':
      self.add_boost(site, side, ctv)
  
  
  # Adds a boost target volume.
  def add_boost(self, site, side, ctv):
    if side == 'right':
      sb = ROIS.surgical_bed_r
    else:
      sb = ROIS.surgical_bed_l
    ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [sb], sourcesB = [ctv], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
    ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv_sb.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ctv_sb, ptv_sbc])
