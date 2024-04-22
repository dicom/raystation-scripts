# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS

# Definitions script for prostate treatments (prostate/prostate bed, with or without lymph nodes, normo/hypofractionated).
class DefProstate(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Region - prostate or bed?
    region = choices[1]
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, examination, site)
    # Setup targets and site specific ROIs:
    if region == 'prostate':
      self.setup_prostate(pm, examination, site, choices)
    else:
      self.setup_bed(pm, examination, site, choices)
    # Create "Bone" ROI Algebra:
    bone_rois = [ROIS.pelvic_girdle_l, ROIS.pelvic_girdle_r, ROIS.femur_head_neck_l, ROIS.femur_head_neck_r]
    vertebrae_rois = [ROIS.l5, ROIS.sacrum, ROIS.coccyx]
    for roi in [ROIS.l4, ROIS.l3, ROIS.l2]:
      try:
        if pm.RegionsOfInterest[roi.name]:
          vertebrae_rois.insert(0, roi)
      except:
        pass
    bone = ROI.ROIAlgebra("Bone", 'Organ', COLORS.bone_color1, sourcesA = bone_rois, sourcesB = vertebrae_rois)
    site.add_oars([bone])
    # Create all targets and OARs in RayStation:
    site.create_rois()
    # Change type to 'Other' for selected ROIs:
    for roi_name in ['Prostate', 'SeminalVes', 'LN_Iliac', 'BowelBag_Draft', bone.name]:
      try:
        if pm.RegionsOfInterest[roi_name]:
          if pm.RegionsOfInterest[roi_name].OrganData.OrganType != "Other":
            pm.RegionsOfInterest[roi_name].OrganData.OrganType = "Other"
      except:
        pass
    # Exclude some ROIs from export:
    exclude = bone_rois + vertebrae_rois + [ROIS.a_descending_aorta, ROIS.a_common_iliac_l, ROIS.a_common_iliac_r, ROIS.a_internal_iliac_l, ROIS.a_internal_iliac_r, ROIS.a_external_iliac_l, ROIS.a_external_iliac_r, ROIS.v_inferior_vena_cava, ROIS.v_common_iliac_l, ROIS.v_common_iliac_r, ROIS.v_internal_iliac_l, ROIS.v_internal_iliac_r, ROIS.v_external_iliac_l, ROIS.v_external_iliac_r]
    for roi in exclude:
      PMF.exclude_roi_from_export(pm, roi.name)
    # Override density for vessel ROIs (may contain contrast and should be set to water for correct dose calculation):
    vessel_rois = []
    for roi_name in ["A_DescendingAorta", "A_CommonIliac_L", "A_CommonIliac_R", "A_ExternalIliac_L", "A_ExternalIliac_R", "A_InternalIliac_L", "A_InternalIliac_R", "V_InferiorVenaCava", "V_CommonIliac_L", "V_CommonIliac_R", "V_ExternalIliac_L", "V_ExternalIliac_R", "V_InternalIliac_L", "V_InternalIliac_R"]:
      try:
        if pm.RegionsOfInterest[roi_name]:
          vessel_rois.append(roi_name)
      except:
        pass
    water = None
    for material in pm.Materials:
      if material.Name == 'Water':
        water = material
        break
    if water:
      for roi_name in vessel_rois:
        pm.RegionsOfInterest[roi_name].SetRoiMaterial(Material=water)


  # Adds target ROIs for prostate bed only to the site object.
  def add_bed_only_targets(self, pm, examination, site, fractionation):
    if fractionation == 'normo':
      ctv = ROI.ROIExpanded(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_high, source = ROIS.ctv_sb)
      ptv = ROI.ROIExpanded(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv, source = ctv, margins = MARGINS.prostate_bone_match_expansion)
    else:      
      ctv = ROIS.ctv_sb
      ptv = ROI.ROIExpanded(ROIS.ptv_sb.name, ROIS.ptv_sb.type, COLORS.ptv_high, source = ROIS.ctv_sb, margins = MARGINS.prostate_bone_match_expansion)
    # Targets:
    site.add_targets([ctv, ptv])
    # Other derived ROIs:
    bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    rectum_ptv = ROI.ROIAlgebra(ROIS.z_rectum.name, ROIS.z_rectum.type, COLORS.rectum, sourcesA = [ROIS.rectum], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_2mm_expansion)
    wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv, 1, 0)
    site.add_oars([bladder_ptv, rectum_ptv, wall_ptv])
  
  
  # Adds target ROIs for prostate bed with elective nodes to the site object.
  def add_bed_with_nodes_targets(self, pm, examination, site, nodes):
    if nodes == 'with':
      # Elective nodes only:
      ctv_70 = ROI.ROIExpanded(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_high, source = ROIS.ctv_sb)
      ptv_70 = ROI.ROIExpanded(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv, source = ctv_70, margins = MARGINS.prostate_bone_match_expansion)
    else:
      # Positive node (in addition to elective nodes):
      ctv_n = ROI.ROIExpanded(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.pelvic_nodes, source = ROIS.gtv_n, margins = MARGINS.uniform_5mm_expansion)
      ptv_n = ROI.ROIExpanded(ROIS.ptv_n.name, ROIS.ptv_n.type, ROIS.ptv_n.color, source = ctv_n, margins = MARGINS.uniform_5mm_expansion)
      ptv_sb = ROI.ROIExpanded(ROIS.ptv_sb.name, ROIS.ptv_sb.type, ROIS.ptv_sb.color, source = ROIS.ctv_sb, margins = MARGINS.prostate_bone_match_expansion)
      ctv_70 = ROI.ROIAlgebra(ROIS.ctv_70.name, ROIS.ctv_70.type, COLORS.ctv_med, sourcesA = [ROIS.ctv_sb], sourcesB = [ctv_n], operator = 'Union')
      ptv_70 = ROI.ROIAlgebra(ROIS.ptv_70.name, ROIS.ptv_70.type, COLORS.ptv, sourcesA = [ptv_sb], sourcesB = [ptv_n], operator = 'Union', marginsA = MARGINS.zero , marginsB = MARGINS.zero)
      site.add_targets([ROIS.gtv_n, ctv_n, ptv_n, ptv_sb])
    # Common for elective nodes (with or without positive node):
    ctv_56 = ROI.ROIAlgebra(ROIS.ctv_56.name, ROIS.ctv_56.type, COLORS.ctv_low, sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv_70], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    ptv_56 = ROI.ROIAlgebra(ROIS.ptv_56.name, ROIS.ptv_56.type, COLORS.ptv_low, sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv_70], operator = 'Subtraction', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.zero)
    ptv_56_70 = ROI.ROIAlgebra(ROIS.ptv_56_70.name, ROIS.ptv_56_70.type, COLORS.ptv_low, sourcesA = [ptv_56], sourcesB = [ptv_70], marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    site.add_targets([ROIS.ctv_sb, ctv_70, ptv_70, ctv_56, ptv_56, ptv_56_70])
    # Other derived ROIs:
    bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv_70, ptv_56], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    rectum_ptv = ROI.ROIAlgebra(ROIS.z_rectum.name, ROIS.z_rectum.type, COLORS.rectum, sourcesA = [ROIS.rectum], sourcesB = [ptv_70, ptv_56], operator='Subtraction', marginsB = MARGINS.uniform_2mm_expansion)
    bowel_ptv = ROI.ROIAlgebra(ROIS.z_spc_bowel.name, ROIS.z_spc_bowel.type, COLORS.bowel_space, sourcesA = [ROIS.bowel_bag], sourcesB = [ptv_70, ptv_56], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    wall_ptv_70 = ROI.ROIWall(ROIS.z_ptv_70_wall.name, ROIS.z_ptv_70_wall.type, COLORS.wall, ptv_70, 1, 0)
    wall_ptv_56_temp = ROI.ROIWall(ROIS.z_ptv_56_temp.name, ROIS.z_ptv_56_temp.type, COLORS.wall, ptv_56, 1, 0)
    wall_ptv_56 = ROI.ROIAlgebra(ROIS.z_ptv_56_wall.name, ROIS.z_ptv_56_wall.type, COLORS.wall, sourcesA = [wall_ptv_56_temp], sourcesB = [ptv_70, wall_ptv_70], operator='Subtraction', marginsB = MARGINS.zero)
    site.add_oars([bladder_ptv, bowel_ptv, rectum_ptv, wall_ptv_70, wall_ptv_56_temp, wall_ptv_56])
  
  
  # Adds rois that are common across all cases.
  def add_common_rois(self, pm, examination, site):
    # DL OARs:
    examination.RunOarSegmentation(ModelName="RSL DLS Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Bladder"])
    examination.RunOarSegmentation(ModelName="Alesund Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["CaudaEquina", "BowelBag_Draft", "Rectum", "AnalCanal", "Testis_L", "Testis_R", "L5", "Sacrum", "Coccyx", "PelvicGirdle_L", "PelvicGirdle_R", "FemurHeadNeck_L", "FemurHeadNeck_R"])
    # Exclude Rectum from BowelBag:
    ROIS.bowel_bag.sourcesB.append(ROIS.rectum)
    # Non-DL OARs:
    site.add_oars([ROIS.bowel_bag, ROIS.penile_bulb])
  
  
  # Adds rois that are relevant for lymph node treatment.
  def add_lymph_node_rois(self, pm, examination, site):
    # DL OARs:
    examination.RunOarSegmentation(ModelName="Alesund Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["LN_Iliac", "Kidney_L", "Kidney_R", "Liver", "IliopsoasMuscle_L", "IliopsoasMuscle_R", "L2", "L3", "L4", "A_DescendingAorta", "A_CommonIliac_L", "A_CommonIliac_R", "A_ExternalIliac_L", "A_ExternalIliac_R", "A_InternalIliac_L", "A_InternalIliac_R", "V_InferiorVenaCava", "V_CommonIliac_L", "V_CommonIliac_R", "V_ExternalIliac_L", "V_ExternalIliac_R", "V_InternalIliac_L", "V_InternalIliac_R"])
    # Exclude Kidneys, Liver and LN_Iliac from BowelBag:
    ROIS.bowel_bag.sourcesB.extend([ROIS.kidney_l, ROIS.kidney_r, ROIS.liver, ROIS.pelvic_nodes])
  
  
  # Adds rois that are relevant for intact prostate treatment.
  def add_prostate_rois(self, pm, examination, site, match):
    # DL OARs:
    examination.RunOarSegmentation(ModelName="RSL DLS Male Pelvic CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Prostate_1", "SeminalVes"])
    # Rename DL ROI(s):
    pm.RegionsOfInterest['Prostate_1'].Name = 'Prostate'
    if match == 'seeds':
      # Non-DL OARs:
      site.add_oars([ROIS.levator_ani, ROIS.seed1, ROIS.seed2, ROIS.seed3, ROIS.urethra])
  
  
  # Adds target ROIs for high risk (35 or 25 fx) prostate treatment to the site object.
  def add_prostate_high_risk_targets(self, pm, examination, site, choices):
    # Choice 2: Fractionation - normo or hypo_bergen?
    fractionation = choices[2]
    # Choice 3: Nodes - none, elective only or elective + positive node?
    nodes = choices[3]
    # Seminal vesicles (which for high risk is 20 mm):
    semves20 = ROI.ROIAlgebra('SeminalVes20', ROIS.ctv.type, COLORS.vesicles, sourcesA = [ROIS.vesicles], sourcesB = [ROIS.prostate], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_20mm_expansion)
    # Setup dose named ROIs:
    if fractionation == 'normo':
      ctv3s = ROIS.ctv_77
      ptv3s = ROIS.ptv_77
      ptv3w = ROIS.z_ptv_77_wall
      ctv2s = ROIS.ctv_70_sib
      ptv2s = ROIS.ptv_70_sib
      ptv_2_3s = ROIS.ptv_70_77
      ptv_2_3w = ROIS.z_ptv_70_77_wall
      ctv1s = ROIS.ctv_56
      ptv1s = ROIS.ptv_56
      ptv_1_2_3s = ROIS.ptv_56_70_77
    else:
      ctv3s = ROIS.ctv_67_5
      ptv3s = ROIS.ptv_67_5
      ptv3w = ROIS.z_ptv_67_5_wall
      ctv2s = ROIS.ctv_62_5_sib
      ptv2s = ROIS.ptv_62_5_sib
      ptv_2_3s = ROIS.ptv_62_5_67_5
      ptv_2_3w = ROIS.z_ptv_62_5_67_5_wall
      ctv1s = ROIS.ctv__50
      ptv1s = ROIS.ptv__50
      ptv_1_2_3s = ROIS.ptv_50_62_5_67_5
    # Prostate targets:
    ctv3 = ROI.ROIAlgebra(ctv3s.name, ctv3s.type, COLORS.ctv_high, sourcesA = [ROIS.prostate], sourcesB = [ROIS.rectum, ROIS.anal_canal, ROIS.levator_ani], operator = 'Subtraction', marginsA = MARGINS.prostate_ctv, marginsB = MARGINS.zero)
    ptv3 = ROI.ROIExpanded(ptv3s.name, ptv3s.type, COLORS.ptv_high, source = ctv3, margins = MARGINS.prostate_seed_expansion)
    # Other derived ROIs:
    bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv3], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    rectum_ptv = ROI.ROIAlgebra(ROIS.z_rectum.name, ROIS.z_rectum.type, COLORS.rectum, sourcesA = [ROIS.rectum], sourcesB = [ptv3], operator='Subtraction', marginsB = MARGINS.uniform_2mm_expansion)
    wall_ptv3 = ROI.ROIWall(ptv3w.name, ptv3w.type, COLORS.wall, ptv3, 0.5, 0)
    if nodes == 'no':
      # Prostate only:
      # Vesicle targets:
      ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, COLORS.ptv_med, sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.uniform_8mm_expansion, marginsB = MARGINS.zero)
      ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low, sourcesA = [ctv3], sourcesB = [semves20], marginsA = MARGINS.prostate_seed_expansion, marginsB = MARGINS.uniform_8mm_expansion)
      site.add_targets([ptv_2_3])
      # Other derived ROIs:
      bladder_ptv.sourcesB.extend([ptv2])
      rectum_ptv.sourcesB.extend([ptv2])
      site.add_oars([bladder_ptv, rectum_ptv, wall_ptv3])
    elif nodes == 'with_node':
      # Elective nodes (with positive node):
      # Targets:
      ctv_n = ROI.ROIExpanded(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.pelvic_nodes, source = ROIS.gtv_n, margins = MARGINS.uniform_5mm_expansion)
      ptv_n = ROI.ROIExpanded(ROIS.ptv_n.name, ROIS.ptv_n.type, ROIS.ptv_n.color, source = ctv_n, margins = MARGINS.prostate_lymph_nodes_seed_expansion)
      ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20, ctv_n], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv_semves = ROI.ROIAlgebra(ROIS.ptv_semves.name, ROIS.ptv_semves.type, COLORS.ptv_med, sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.uniform_8mm_expansion, marginsB = MARGINS.zero)
      ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, ptv2s.color, sourcesA = [ptv_semves, ptv_n], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low, sourcesA = [ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv1 = ROI.ROIAlgebra(ptv1s.name, ptv1s.type, COLORS.ptv_low, sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction', marginsA = MARGINS.prostate_lymph_nodes_seed_expansion, marginsB = MARGINS.zero)
      ctv1 = ROI.ROIAlgebra(ctv1s.name, ctv1s.type, COLORS.ctv_low, sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv_1_2_3 = ROI.ROIAlgebra(ptv_1_2_3s.name, ptv_1_2_3s.type, COLORS.ptv_low, sourcesA = [ptv1, ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      site.add_targets([ROIS.gtv_n, ctv_n, ctv1, ptv_n, ptv_semves, ptv1, ptv_2_3, ptv_1_2_3])
      # OARs:
      bladder_ptv.sourcesB.extend([ptv2, ptv1])
      rectum_ptv.sourcesB.extend([ptv2, ptv1])
      bowel_ptv = ROI.ROIAlgebra(ROIS.z_spc_bowel.name, ROIS.z_spc_bowel.type, COLORS.bowel_space, sourcesA = [ROIS.bowel_space], sourcesB = [ptv3, ptv2, ptv1], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      wall_ptv_2_3 = ROI.ROIWall(ptv_2_3w.name, ptv_2_3w.type, COLORS.wall, ptv_2_3, 1, 0)
      # Non-DL OARs:
      site.add_oars([bladder_ptv, rectum_ptv, wall_ptv3, bowel_ptv, wall_ptv_2_3])
    elif nodes == 'with':
      # Elective nodes:
      # Targets:
      ctv2 = ROI.ROIAlgebra(ctv2s.name, ctv2s.type, COLORS.ctv_med, sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv2 = ROI.ROIAlgebra(ptv2s.name, ptv2s.type, COLORS.ptv_med, sourcesA = [semves20], sourcesB = [ptv3], operator = 'Subtraction', marginsA = MARGINS.uniform_8mm_expansion, marginsB = MARGINS.zero)
      ptv_2_3 = ROI.ROIAlgebra(ptv_2_3s.name, ptv_2_3s.type, COLORS.ptv_low, sourcesA = [ctv3], sourcesB = [semves20], marginsA = MARGINS.prostate_seed_expansion, marginsB = MARGINS.uniform_8mm_expansion)
      ptv1 = ROI.ROIAlgebra(ptv1s.name, ptv1s.type, COLORS.ptv_low, sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction', marginsA = MARGINS.prostate_lymph_nodes_seed_expansion, marginsB = MARGINS.zero)
      ctv1 = ROI.ROIAlgebra(ctv1s.name, ctv1s.type, COLORS.ctv_low, sourcesA = [ROIS.pelvic_nodes], sourcesB = [ptv3, ptv2], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      ptv_1_2_3 = ROI.ROIAlgebra(ptv_1_2_3s.name, ptv_1_2_3s.type, COLORS.ptv_low, sourcesA = [ptv1, ptv2], sourcesB = [ptv3], marginsA = MARGINS.zero, marginsB = MARGINS.zero)
      site.add_targets([ctv1, ptv1, ptv_2_3, ptv_1_2_3])
      # OARs:
      bladder_ptv.sourcesB.extend([ptv2, ptv1])
      rectum_ptv.sourcesB.extend([ptv2, ptv1])
      bowel_ptv = ROI.ROIAlgebra(ROIS.z_spc_bowel.name, ROIS.z_spc_bowel.type, COLORS.bowel_space, sourcesA = [ROIS.bowel_space], sourcesB = [ptv3, ptv2, ptv1], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      wall_ptv_2_3 = ROI.ROIWall(ptv_2_3w.name, ptv_2_3w.type, COLORS.wall, ptv_2_3, 1, 0)
      # Non-DL OARs:
      site.add_oars([bladder_ptv, rectum_ptv, wall_ptv3, bowel_ptv, wall_ptv_2_3])
    # Common ROIs for all conventional fractionation:
    site.add_targets([semves20, ctv3, ctv2, ptv3, ptv2])
  
  
  # Adds target ROIs for intermediate risk (20 fx) prostate treatment to the site object.
  def add_prostate_intermediate_targets(self, pm, examination, site):
    # Hypofractionated prostate with vesicles (3 Gy x 20):
    # Seminal vesicles (which for intermediate risk is 10 mm):
    semves10 = ROI.ROIAlgebra('SeminalVes10', ROIS.ctv.type, COLORS.vesicles, sourcesA = [ROIS.vesicles], sourcesB = [ROIS.prostate], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_10mm_expansion)
    # Targets:
    ctv_60 = ROI.ROIAlgebra(ROIS.ctv_60.name, ROIS.ctv_60.type, COLORS.ctv_high, sourcesA = [ROIS.prostate], sourcesB = [ROIS.rectum, ROIS.anal_canal, ROIS.levator_ani], operator = 'Subtraction', marginsA = MARGINS.prostate_ctv, marginsB = MARGINS.zero)
    ctv_57_60 = ROI.ROIAlgebra(ROIS.ctv_57_60.name, ROIS.ctv_57_60.type, COLORS.ctv_low, sourcesA = [ctv_60], sourcesB = [semves10], marginsA = MARGINS.zero, marginsB = MARGINS.zero)        
    ptv_57_60 = ROI.ROIAlgebra(ROIS.ptv_57_60.name, ROIS.ptv_57_60.type, COLORS.ptv_low, sourcesA = [ctv_60], sourcesB = [semves10], marginsA = MARGINS.prostate_seed_expansion, marginsB = MARGINS.uniform_8mm_expansion)
    ptv_60 = ROI.ROIExpanded(ROIS.ptv_60.name, ROIS.ptv_60.type, COLORS.ptv_high, source = ctv_60, margins = MARGINS.prostate_seed_expansion)
    ctv_57 = ROI.ROIAlgebra(ROIS.ctv_57.name, ROIS.ctv_57.type, COLORS.ctv_med, sourcesA = [ctv_57_60], sourcesB = [ptv_60], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)        
    ptv_57 = ROI.ROIAlgebra(ROIS.ptv_57.name, ROIS.ptv_57.type, COLORS.ptv_med, sourcesA = [ptv_57_60], sourcesB = [ptv_60], operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.zero)
    site.add_targets([semves10, ctv_60, ctv_57, ctv_57_60, ptv_57_60, ptv_60, ptv_57])
    # Other derived ROIs:
    bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv_60, ptv_57], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    rectum_ptv = ROI.ROIAlgebra(ROIS.z_rectum.name, ROIS.z_rectum.type, COLORS.rectum, sourcesA = [ROIS.rectum], sourcesB = [ptv_60, ptv_57], operator='Subtraction', marginsB = MARGINS.uniform_2mm_expansion)
    wall_ptv_60 = ROI.ROIWall(ROIS.z_ptv_60_wall.name, ROIS.z_ptv_60_wall.type, COLORS.wall, ptv_60, 0.5, 0)
    wall_ptv_57_60 = ROI.ROIWall(ROIS.z_ptv_57_60_wall.name, ROIS.z_ptv_57_60_wall.type, COLORS.wall, ptv_57_60, 1, 0)
    site.add_oars([bladder_ptv, rectum_ptv, wall_ptv_60, wall_ptv_57_60])
  
  
  # Adds target ROIs for palliative prostate treatment to the site object.
  def add_prostate_palliative_targets(self, pm, examination, site, choices):
    # Choice 2: Fractionation - STAMPEDE or palliative?
    fractionation = choices[2]
    # Targets:
    ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_low, source = ROIS.prostate, margins = MARGINS.zero)
    if fractionation == 'hypo_55':
      # Choice 3: Seed match or bone match?
      match = choices[3]
      if match == 'seeds':
        # Seed match:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high, source = ctv, margins = MARGINS.prostate_seed_expansion)
      else:
        # Bone match:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high, source = ctv, margins = MARGINS.prostate_bone_match_expansion)
    else:
      # Assuming no markers:
      ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high, source = ctv, margins = MARGINS.prostate_bone_match_expansion)
    site.add_targets([ctv, ptv])
    # Other derived ROIs:
    bladder_ptv = ROI.ROIAlgebra(ROIS.z_bladder.name, ROIS.z_bladder.type, COLORS.bladder, sourcesA = [ROIS.bladder], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    rectum_ptv = ROI.ROIAlgebra(ROIS.z_rectum.name, ROIS.z_rectum.type, COLORS.rectum, sourcesA = [ROIS.rectum], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_2mm_expansion)
    wall_ptv = ROI.ROIWall(ROIS.z_ptv_wall.name, ROIS.z_ptv_wall.type, COLORS.wall, ptv, 1, 0)
    site.add_oars([bladder_ptv, rectum_ptv, wall_ptv])
  
  
  # Setup ROIs used for prostate bed treatment.
  def setup_bed(self, pm, examination, site, choices):
    # Choice 2: Fractionation - normal or palliative?
    fractionation = choices[2]
    # Fractionation:
    if fractionation == 'normo':
      # Conventional fractionation (2 Gy):
      # Choice 3: Nodes - included or not?
      nodes = choices[3]
      if nodes == 'no':
        # Prostate bed only:
        self.add_bed_only_targets(pm, examination, site, fractionation)
      else:
        # Bed with elective nodes (and possibly also positive node):
        self.add_lymph_node_rois(pm, examination, site)
        self.add_bed_with_nodes_targets(pm, examination, site, nodes)
    else:
      # Palliative prostate bed only:
      self.add_bed_only_targets(pm, examination, site, fractionation)
  
  
  # Setup ROIs used for intact prostate treatment.
  def setup_prostate(self, pm, examination, site, choices):
    # Choice 2: Fractionation (e.g. conventional, hypo, palliative)
    fractionation = choices[2]
    # Fractionation:
    if fractionation in ['normo', 'hypo_bergen']:
      # Conventional fractionation (35 fx): prostate (77 Gy) with vesicles (70 Gy) and nodes (56 Gy), or
      # Hypofractionated 25 fx: prostate (67.5 Gy) with vesicles (62.5 Gy) and nodes (50 Gy):
      self.add_prostate_rois(pm, examination, site, 'seeds')
      # Lymph nodes?
      nodes = choices[3]
      if nodes != 'no':
        self.add_lymph_node_rois(pm, examination, site)
      self.add_prostate_high_risk_targets(pm, examination, site, choices)
    elif fractionation == 'hypo_60':
      # Hypofractionated prostate with vesicles (3 Gy x 20):
      self.add_prostate_rois(pm, examination, site, 'seeds')
      self.add_prostate_intermediate_targets(pm, examination, site)
    elif fractionation in ['hypo_55','palliative']:
      if fractionation == 'hypo_55':
        self.add_prostate_rois(pm, examination, site, choices[3])
      else:
        self.add_prostate_rois(pm, examination, site, 'bone')
      # STAMPEDE (2.75 Gy x 20) or palliative prostate (e.q. 3 Gy x 13):
      self.add_prostate_palliative_targets(pm, examination, site, choices)
  