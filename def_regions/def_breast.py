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
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, examination, site)
    # Region:
    if region == 'partial':
      # Partial breast only:
      self.add_partial_breast(pm, examination, site, side)
    else:
      # Whole breast (with or without regional nodes):
      # Choice 3: With our without boost?
      boost = choices[3]
      if region == 'whole':
        self.add_whole_breast(pm, examination, site, side, boost, bilateral=False)
      elif region in ['regional', 'regional_imn']:
        # Regional breast (with or without IMN):
        if region == 'regional_imn':
          self.add_regional_breast(pm, examination, site, side, boost, bilateral=False, include_imn=True)
        else:
          self.add_regional_breast(pm, examination, site, side, boost, bilateral=False, include_imn=False)
      else:
        # Bilateral:
        bilateral_left_side_target = choices[2]
        bilateral_right_side_target = choices[3]
        if bilateral_left_side_target == 'bilateral_left_whole':
          self.add_whole_breast(pm, examination, site, 'left', boost, bilateral=True)
        else:
          self.add_regional_breast(pm, examination, site, 'left', boost, bilateral=True, include_imn=True)
        if bilateral_right_side_target == 'bilateral_right_whole':
          self.add_whole_breast(pm, examination, site, 'right', boost, bilateral=True)
        else:
          self.add_regional_breast(pm, examination, site, 'right', boost, bilateral=True, include_imn=True)
        # If at least one side is locoregional, we should have a PTVpc union:
        if bilateral_left_side_target != 'bilateral_left_whole' or bilateral_right_side_target != 'bilateral_right_whole':
          if bilateral_left_side_target == 'bilateral_left_whole':
            left_primary = ROIS.ptvc_l
          else:
            left_primary = ROIS.ptv_pc_l
          if bilateral_right_side_target == 'bilateral_right_whole':
            right_primary = ROIS.ptvc_r
          else:
            right_primary = ROIS.ptv_pc_r
          ptv_pc = ROI.ROIAlgebra(ROIS.ptv_pc.name, ROIS.ptv_pc.type, ROIS.ptv_pc.color, sourcesA = [left_primary, right_primary], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
          site.add_targets([ptv_pc])
        # Targets (L+R union):
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [ROIS.ctv_l], sourcesB = [ROIS.ctv_r], operator = 'Union', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
        ptv = ROI.ROIAlgebra(ROIS.ptv_c.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ROIS.ptvc_l, ROIS.ptvc_r], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        site.add_targets([ctv, ptv])
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Modify ROI type/organ type:
    for roi_name in ['PTV_Robustness', 'PTV_Robustness_L', 'PTV_Robustness_R']:
      try:
        pm.RegionsOfInterest[roi_name].Type = "Control"
        pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      except:
        pass
    # Change organ type to 'Other' for selected ROIs:
    for roi_name in ['Clips_L','Clips_R','BreastString_L','BreastString_R','Breast_L_Draft','Breast_R_Draft','SurgicalBed_L','SurgicalBed_R','LN_Ax_Pectoral_L','LN_Ax_Pectoral_R','LN_Ax_L1_L','LN_Ax_L1_R','LN_Ax_L2_L','LN_Ax_L2_R','LN_Ax_L3_L','LN_Ax_L3_R','LN_Ax_L4_L','LN_Ax_L4_R','LN_IMN_L','LN_IMN_R','ScaleneMusc_Ant_L','A_Carotid_L','A_Subclavian_L+A_Axillary_L','V_Brachioceph_L','V_Jugular_L','V_Subclavian_L+V_Axillary_L']:
      # Some of these ROIs may not always be defined, and give an error:
      try:
        pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      except:
        pass
    # Exclude some ROIs from export:
    for roi_name in [ROIS.breast_l_draft.name, ROIS.breast_r_draft.name, "LN_Ax_L1_L", "LN_Ax_L2_L", "LN_Ax_L3_L", "LN_Ax_L4_L", "LN_Ax_Pectoral_L", "LN_IMN_L", "LN_Ax_L1_R", "LN_Ax_L2_R", "LN_Ax_L3_R", "LN_Ax_L4_R", "LN_Ax_Pectoral_R", "LN_IMN_R", "ScaleneMusc_Ant_L", "A_Carotid_L", "A_Subclavian_L+A_Axillary_L", "V_Brachioceph_L", "V_Jugular_L", "V_Subclavian_L+V_Axillary_L"]:
      PMF.exclude_roi_from_export(pm, roi_name)
      # Exclude surgical bed for boost cases:
      if PMF.has_roi(pm, 'CTVsb'):
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
            pm.RegionsOfInterest[rg.OfRoi.Name].DeleteRoi()
        else:
          pm.RegionsOfInterest[rg.OfRoi.Name].DeleteRoi()
    # Override the density of the breast string to 'Air' (since it is not present on treatments):
    self.set_breaststring_density(pm)

  
  # Adds rois that are common across all cases.
  def add_common_rois(self, pm, examination, site):
    # DL ROIs:
    examination.RunOarSegmentation(ModelName="St. Olavs-Alesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "Breast_L_Draft", "Breast_R_Draft", "Esophagus", "Heart", "Lung_L", "Lung_R", "SpinalCanalFull", "Sternum", "Trachea", "ThyroidGland"])
    # Add derived ROIs:
    site.add_oars([ROIS.breast_l, ROIS.breast_r, ROIS.lungs])
    # Rename the spinal canal ROI:
    try:
      pm.RegionsOfInterest['SpinalCanalFull'].Name = 'SpinalCanal'
    except:
      pass
  
  
  # Adds rois that are specific for left or right side.
  def add_sided_rois(self, pm, examination, site, side):
    if side == 'right':
      # DL model for right sided breast:
      examination.RunOarSegmentation(ModelName="St. Olavs-Alesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["BreastString_R", "Clips_R", "HumeralHead_R", "SurgicalBed_R"])
      examination.RunOarSegmentation(ModelName="RSL Thorax-Abdomen CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Liver"])
    else:
      # DL model for left sided whole breast:
      examination.RunOarSegmentation(ModelName="St. Olavs-Alesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["BreastString_L", "Clips_L", "HumeralHead_L", "SurgicalBed_L"])
  
  
  # Adds partial breast (left or right) ROIs to the site object.
  def add_partial_breast(self, pm, examination, site, side):
    self.add_sided_rois(pm, examination, site, side)
    # ROIs are dependent on side:
    if side == 'right':
      sb = ROIS.surgical_bed_r
      breast = ROIS.breast_r
    else:
      sb = ROIS.surgical_bed_l
      breast = ROIS.breast_l
    # Targets:
    ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [sb], sourcesB = [breast], operator = 'Intersection', marginsA = MARGINS.uniform_15mm_expansion, marginsB = MARGINS.zero)
    ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    # Image verification volume:
    clips_control = ROI.ROIAlgebra('ClipsControl', ROIS.markers.type, ROIS.markers.color, sourcesA = [sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    # Targets for whole breast:
    site.add_targets([ctv_sb, ptv_sbc, clips_control])
  
  
  # Adds regional breast (left or right) ROIs to the site object.
  def add_regional_breast(self, pm, examination, site, side, boost, bilateral, include_imn):
    self.add_sided_rois(pm, examination, site, side)
    # Laterality suffix for targets for bilateral cases:
    suffix = ''
    if bilateral:
      if side == 'right':
        suffix = '_R'
      else:
        suffix = '_L'
    # Side dependent targets and support structures for regional treatment:
    if side == 'right':
      # Non-DL right sided support structures:
      site.add_oars([ROIS.scalene_muscle_r, ROIS.artery1_r, ROIS.artery2_r, ROIS.artery3_r, ROIS.vein1_r, ROIS.vein2_r, ROIS.vein3_r])
      # DL model for right sided regional nodes:
      examination.RunOarSegmentation(ModelName="St. Olavs-Alesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["LN_Ax_L1_R", "LN_Ax_L2_R", "LN_Ax_L3_R", "LN_Ax_L4_R", "LN_Ax_Pectoral_R", "LN_IMN_R"])
      # Targets:
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name+suffix, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_r_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name+suffix, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_r, ROIS.level1_r, ROIS.level2_r, ROIS.level3_r, ROIS.level4_r], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      if include_imn:
        imn = ROIS.imn_r
    else:
      # DL model for left sided regional nodes and support structures:
      examination.RunOarSegmentation(ModelName="St. Olavs-Alesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_Carotid_L", "A_Subclavian_L+A_Axillary_L", "LN_Ax_L1_L", "LN_Ax_L2_L", "LN_Ax_L3_L", "LN_Ax_L4_L", "LN_Ax_Pectoral_L", "LN_IMN_L", "ScaleneMusc_Ant_L", "V_Brachioceph_L", "V_Jugular_L", "V_Subclavian_L+V_Axillary_L"])
      # Targets:
      ctv_p = ROI.ROIAlgebra(ROIS.ctv_p.name+suffix, ROIS.ctv_p.type, ROIS.ctv.color, sourcesA = [ROIS.breast_l_draft], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
      ctv_n = ROI.ROIAlgebra(ROIS.ctv_n.name+suffix, ROIS.ctv_n.type, ROIS.ctv.color, sourcesA = [ROIS.level_l, ROIS.level1_l, ROIS.level2_l, ROIS.level3_l, ROIS.level4_l], sourcesB = [ctv_p], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      if include_imn:
        imn = ROIS.imn_l
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
      self.add_boost(site, side, ctv, ptv, ctv_p, ptv_p)
  
  
  # Adds whole breast (left or right) ROIs to the site object.
  def add_whole_breast(self, pm, examination, site, side, boost, bilateral):
    self.add_sided_rois(pm, examination, site, side)
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
      self.add_boost(site, side, ctv, ptv)
  
  
  # Adds a boost target volume.
  def add_boost(self, site, side, ctv, ptv, ctv_p=None, ptv_pc=None):
    if side == 'right':
      sb = ROIS.surgical_bed_r
    else:
      sb = ROIS.surgical_bed_l
    ctv_sb = ROI.ROIAlgebra(ROIS.ctv_sb.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA = [sb], sourcesB = [ctv], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_sbc.name, ROIS.ptv_sb.type, ROIS.ptv.color, sourcesA = [ctv_sb], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    ctv_ctv_sb = ROI.ROIAlgebra(ROIS.ctv_ctv_sb.name, ROIS.ctv_ctv_sb.type, ROIS.ctv_ctv_sb.color, sourcesA = [ctv], sourcesB = [ctv_sb], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ctv_ptv_sbc = ROI.ROIAlgebra(ROIS.ctv_ptv_sbc.name, ROIS.ctv_ptv_sbc.type, ROIS.ctv_ptv_sbc.color, sourcesA = [ctv], sourcesB = [ptv_sbc], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv_c_ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_c_ptv_sbc.name, ROIS.ptv_c_ptv_sbc.type, ROIS.ptv_c_ptv_sbc.color, sourcesA = [ptv], sourcesB = [ptv_sbc], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    site.add_targets([ctv_sb, ptv_sbc, ctv_ctv_sb, ctv_ptv_sbc, ptv_c_ptv_sbc])
    # For regional breast we need separate subracted ROIs for the whole CTV/PTV and the breast CTVp/PTVp:
    if ctv_p:
      ctv_p_ctv_sb = ROI.ROIAlgebra(ROIS.ctv_p_ctv_sb.name, ROIS.ctv_p_ctv_sb.type, ROIS.ctv_p_ctv_sb.color, sourcesA = [ctv_p], sourcesB = [ctv_sb], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ctv_p_ptv_sbc = ROI.ROIAlgebra(ROIS.ctv_p_ptv_sbc.name, ROIS.ctv_p_ptv_sbc.type, ROIS.ctv_p_ptv_sbc.color, sourcesA = [ctv_p], sourcesB = [ptv_sbc], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv_pc_ptv_sbc = ROI.ROIAlgebra(ROIS.ptv_pc_ptv_sbc.name, ROIS.ptv_pc_ptv_sbc.type, ROIS.ptv_pc_ptv_sbc.color, sourcesA = [ptv_pc], sourcesB = [ptv_sbc], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      site.add_targets([ctv_p_ctv_sb, ctv_p_ptv_sbc, ptv_pc_ptv_sbc])


  # Sets the density of any breast string ROIs as air.
  def set_breaststring_density(self, pm):
    breaststring_rois = []
    for roi_name in ["BreastString_L", "BreastString_R"]:
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
