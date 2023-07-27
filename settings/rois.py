# encoding: utf8

# Import local files:
import colors as COLORS
import margins as MARGINS
import roi as ROI


# External:
external = ROI.ROI('External', 'External', COLORS.external)
body = ROI.ROI('Body', 'Organ', COLORS.external)


# Support:
couch = ROI.ROI('Couch', 'Support', COLORS.couch)


# Target volumes:
gtv = ROI.ROI('GTV', 'Gtv', COLORS.gtv)
ctv = ROI.ROIExpanded('CTV', 'Ctv', COLORS.ctv, gtv, margins = MARGINS.uniform_5mm_expansion)
ptv = ROI.ROIExpanded('PTV', 'Ptv', COLORS.ptv, ctv, margins = MARGINS.uniform_5mm_expansion)
ctv_ext = ROI.ROIAlgebra('CTV', 'Ctv', COLORS.ctv, sourcesA = [gtv], sourcesB = [external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
ctv_underived = ROI.ROI('CTV', 'Ctv', COLORS.ctv)
igtv = ROI.ROI('IGTV', 'Gtv', COLORS.gtv)
igtv1 = ROI.ROI('IGTV1', 'Gtv', COLORS.gtv)
igtv2 = ROI.ROI('IGTV2', 'Gtv', COLORS.gtv)
igtv3 = ROI.ROI('IGTV3', 'Gtv', COLORS.gtv)
ictv = ROI.ROIExpanded('ICTV', 'Ctv', COLORS.ctv, igtv, margins = MARGINS.uniform_5mm_expansion)
ictv1 = ROI.ROIExpanded('ICTV1', 'Ctv', COLORS.ctv, igtv1, margins = MARGINS.uniform_5mm_expansion)
ictv2 = ROI.ROIExpanded('ICTV2', 'Ctv', COLORS.ctv, igtv2, margins = MARGINS.uniform_5mm_expansion)
ictv3 = ROI.ROIExpanded('ICTV3', 'Ctv', COLORS.ctv, igtv3, margins = MARGINS.uniform_5mm_expansion)
iptv = ROI.ROIExpanded('PTV', 'Ptv', COLORS.ptv, ictv, margins = MARGINS.uniform_5mm_expansion)
iptv_gtv = ROI.ROIExpanded('PTV', 'Ptv', COLORS.ptv, igtv, margins = MARGINS.uniform_5mm_expansion)
iptv1 = ROI.ROIExpanded('PTV1', 'Ptv', COLORS.ptv, ictv1, margins = MARGINS.uniform_5mm_expansion)
iptv2 = ROI.ROIExpanded('PTV2', 'Ptv', COLORS.ptv, ictv2, margins = MARGINS.uniform_5mm_expansion)
iptv3 = ROI.ROIExpanded('PTV3', 'Ptv', COLORS.ptv, ictv3, margins = MARGINS.uniform_5mm_expansion)
gtv_p = ROI.ROI('GTVp','Gtv', COLORS.gtv)
gtv_n = ROI.ROI('GTVn','Gtv', COLORS.gtv)
gtv_n1 = ROI.ROI('GTVn','Gtv', COLORS.gtv)
ctv_e = ROI.ROI('CTVe','Ctv', COLORS.ctv_med)
ptv_e = ROI.ROI('PTVe','Ptv', COLORS.ptv)
gtv_groin_l = ROI.ROI('GTV_Groin_L','Gtv', COLORS.gtv)
gtv_groin_r = ROI.ROI('GTV_Groin_R','Gtv', COLORS.gtv)
ctv_groin_l = ROI.ROI('CTV_Groin_L','Ctv', COLORS.ctv_med)
ctv_groin_r = ROI.ROI('CTV_Groin_R','Ctv', COLORS.ctv_med)
ptv_groin_l = ROI.ROI('PTV_Groin_L','Ptv', COLORS.ptv)
ptv_groin_r = ROI.ROI('PTV_Groin_R','Ptv', COLORS.ptv)
ctv_p = ROI.ROI('CTVp', 'Ctv', COLORS.ctv)
ctv_n = ROI.ROI('CTVn','Ctv', COLORS.ctv)
igtv_p = ROI.ROI('IGTVp','Gtv', COLORS.gtv)
igtv_n = ROI.ROI('IGTVn','Gtv', COLORS.gtv)
ictv_p = ROI.ROI('ICTVp', 'Ctv', COLORS.ctv)
ictv_n = ROI.ROI('ICTVn', 'Ctv', COLORS.ctv)
gtv1 = ROI.ROI('GTV1', 'Gtv', COLORS.gtv)
gtv2 = ROI.ROI('GTV2', 'Gtv', COLORS.gtv)
gtv3 = ROI.ROI('GTV3', 'Gtv', COLORS.gtv)
gtv4 = ROI.ROI('GTV4', 'Gtv', COLORS.gtv)
ctv1 = ROI.ROI('CTV1', 'Ctv', COLORS.ctv)
ctv2 = ROI.ROI('CTV2', 'Ctv', COLORS.ctv)
ctv3 = ROI.ROI('CTV3', 'Ctv', COLORS.ctv)
ctv4 = ROI.ROI('CTV4', 'Ctv', COLORS.ctv)
gtv_sb = ROI.ROI('GTVsb', 'Gtv', COLORS.gtv)
ctv_sb = ROI.ROI('CTVsb', 'Ctv', COLORS.ctv)
vb = ROI.ROI('VB','Ctv', COLORS.ctv_med)
ctv_l = ROI.ROI('CTV_L', 'Ctv', COLORS.ctv)
ctv_r = ROI.ROI('CTV_R', 'Ctv', COLORS.ctv)
ptvc_l = ROI.ROI('PTVc_L', 'Ptv', COLORS.ptv)
ptvc_r = ROI.ROI('PTVc_R', 'Ptv', COLORS.ptv)


# OARs: Empty (will be delineated manually):
# Head:
eye_l = ROI.ROI('Eye_L', 'Organ', COLORS.eye)
eye_r = ROI.ROI('Eye_R', 'Organ', COLORS.eye)
lens_l = ROI.ROI('Lens_L', 'Organ', COLORS.lens)
lens_r = ROI.ROI('Lens_R', 'Organ', COLORS.lens)
optic_nrv_l = ROI.ROI('OpticNerve_L', 'Organ', COLORS.optic_nrv)
optic_nrv_r = ROI.ROI('OpticNerve_R', 'Organ', COLORS.optic_nrv)
optic_chiasm = ROI.ROI('OpticChiasm','Organ', COLORS.chiasma)
lacrimal_l =ROI.ROI('LacrimalGland_L', 'Organ', COLORS.lacrimal)
lacrimal_r =ROI.ROI('LacrimalGland_R', 'Organ', COLORS.lacrimal)
cochlea_l = ROI.ROI('Cochlea_L','Organ', COLORS.cochlea)
cochlea_r = ROI.ROI('Cochlea_R','Organ', COLORS.cochlea)
hippocampus_l = ROI.ROI('Hippocampus_L','Organ', COLORS.hippocampus)
hippocampus_r = ROI.ROI('Hippocampus_R','Organ', COLORS.hippocampus)
brainstem = ROI.ROI('Brainstem', 'Organ', COLORS.brainstem)
nasal_cavity = ROI.ROI('NasalCavity', 'Organ', COLORS.nasal_cavity)
oral_cavity = ROI.ROI('OralCavity', 'Organ', COLORS.oral_cavity)
pituitary = ROI.ROI('Pituitary', 'Organ', COLORS.pituitary)
submand_l = ROI.ROI('SubmandGland_L', 'Organ', COLORS.submand)
submand_r = ROI.ROI('SubmandGland_R', 'Organ', COLORS.submand)
cornea_l = ROI.ROI('Cornea_L', 'Organ', COLORS.cornea) 
cornea_r = ROI.ROI('Cornea_R', 'Organ', COLORS.cornea)
retina_l = ROI.ROI('Retina_L', 'Organ', COLORS.retina) 
retina_r = ROI.ROI('Retina_R', 'Organ', COLORS.retina)
brainstem_core = ROI.ROIExpanded('BrainstemCore', 'Organ', COLORS.brainstem_core, brainstem, margins = MARGINS.uniform_2mm_contraction)
brainstem_surface = ROI.ROIAlgebra('BrainstemSurface', 'Organ', COLORS.brainstem_surface, sourcesA = [brainstem], sourcesB = [brainstem_core], operator = 'Subtraction')
# Thorax:
esophagus = ROI.ROI('Esophagus', 'Organ', COLORS.esophagus)
spinal_cord = ROI.ROI('SpinalCord', 'Organ', COLORS.spinal_cord)
heart = ROI.ROI('Heart', 'Organ', COLORS.heart)
# Breast:
thyroid = ROI.ROI('ThyroidGland','Organ', COLORS.thyroid)
a_lad = ROI.ROI('A_LAD','Organ', COLORS.lad)
# Lung, stereotactic:
chestwall = ROI.ROI('Chestwall', 'Organ', COLORS.chestwall)
greatves = ROI.ROI('GreatVessel','Organ', COLORS.heart)
trachea = ROI.ROI('Trachea','Organ', COLORS.trachea)
spleen = ROI.ROI('Spleen','Organ', COLORS.spleen)
stomach = ROI.ROI('Stomach','Organ', COLORS.stomach)
liver = ROI.ROI('Liver','Organ', COLORS.liver)
rib_x_l = ROI.ROI('Ribx_L','Organ', COLORS.rib)
rib_x_r = ROI.ROI('Ribx_R','Organ', COLORS.rib)
rib_y_l = ROI.ROI('Riby_L','Organ', COLORS.rib)
rib_y_r = ROI.ROI('Riby_R','Organ', COLORS.rib)
ribs = ROI.ROI('Ribs','Organ', COLORS.ribs)
main_bronchus_l = ROI.ROI('BronchusMain_L','Organ', COLORS.main_bronchus)
main_bronchus_r = ROI.ROI('BronchusMain_R','Organ', COLORS.main_bronchus)
# Spine SBRT:
cauda_equina = ROI.ROI('CaudaEquina','Organ', COLORS.cauda)
small_bowel = ROI.ROI('BowelSmall','Organ', COLORS.small_bowel)
colon = ROI.ROI('Colon','Organ', COLORS.colon)
brachial = ROI.ROI('BrachialPlexus','Organ', COLORS.brachial)
# Pelvis, prostate:
bowel_space = ROI.ROI('BowelBag', 'Organ', COLORS.bowel_space)
rectum = ROI.ROI('Rectum', 'Organ', COLORS.rectum)
pelvic_nodes = ROI.ROI('LN_Iliac', 'Ctv', COLORS.pelvic_nodes)
prostate = ROI.ROI('Prostate', 'Ctv', COLORS.prostate)
prostate_bed = ROI.ROI('SurgicalBed', 'Ctv', COLORS.prostate_bed)
urethra = ROI.ROI('Urethra', 'Organ', COLORS.urethra)
vesicles = ROI.ROI('SeminalVes', 'Ctv', COLORS.vesicles)
penile_bulb = ROI.ROI('PenileBulb', 'Organ', COLORS.penile_bulb)
anal_canal = ROI.ROI('AnalCanal','Organ', COLORS.anal_canal)
levator_ani = ROI.ROI('LevatorAni', 'Organ', COLORS.levator_ani)

# Bone ROIs:
humeral_l = ROI.ROI('HumeralHead_L', 'Organ', COLORS.bone_color1)
humeral_r = ROI.ROI('HumeralHead_R', 'Organ', COLORS.bone_color1)
sternum = ROI.ROI('Sternum', 'Organ', COLORS.bone_color3)
l2 = ROI.ROI('L2', 'Organ', COLORS.bone_color1)
l3 = ROI.ROI('L3', 'Organ', COLORS.bone_color2)
l4 = ROI.ROI('L4', 'Organ', COLORS.bone_color1)
l5 = ROI.ROI('L5', 'Organ', COLORS.bone_color2)
sacrum = ROI.ROI('Sacrum', 'Organ', COLORS.bone_color1)
coccyx = ROI.ROI('Coccyx', 'Organ', COLORS.bone_color2)
pelvic_girdle_l = ROI.ROI('PelvicGirdle_L', 'Organ', COLORS.bone_color3)
pelvic_girdle_r = ROI.ROI('PelvicGirdle_R', 'Organ', COLORS.bone_color3)
femur_head_neck_l = ROI.ROI('FemurHeadNeck_L', 'Organ', COLORS.bone_color1)
femur_head_neck_r = ROI.ROI('FemurHeadNeck_R', 'Organ', COLORS.bone_color1)

# Vessels:
a_descending_aorta = ROI.ROI('A_DescendingAorta', 'Organ', COLORS.artery_color1)
a_common_iliac_l = ROI.ROI('A_CommonIliac_L', 'Organ', COLORS.artery_color2)
a_common_iliac_r = ROI.ROI('A_CommonIliac_R', 'Organ', COLORS.artery_color2)
a_internal_iliac_l = ROI.ROI('A_InternalIliac_L', 'Organ', COLORS.artery_color3)
a_internal_iliac_r = ROI.ROI('A_InternalIliac_R', 'Organ', COLORS.artery_color3)
a_external_iliac_l = ROI.ROI('A_ExternalIliac_L', 'Organ', COLORS.artery_color4)
a_external_iliac_r = ROI.ROI('A_ExternalIliac_R', 'Organ', COLORS.artery_color4)
v_inferior_vena_cava = ROI.ROI('V_InferiorVenaCava', 'Organ', COLORS.vein_color1)
v_common_iliac_l = ROI.ROI('V_CommonIliac_L', 'Organ', COLORS.vein_color2)
v_common_iliac_r = ROI.ROI('V_CommonIliac_R', 'Organ', COLORS.vein_color2)
v_internal_iliac_l = ROI.ROI('V_InternalIliac_L', 'Organ', COLORS.vein_color3)
v_internal_iliac_r = ROI.ROI('V_InternalIliac_R', 'Organ', COLORS.vein_color3)
v_external_iliac_l = ROI.ROI('V_ExternalIliac_L', 'Organ', COLORS.vein_color4)
v_external_iliac_r = ROI.ROI('V_ExternalIliac_R', 'Organ', COLORS.vein_color4)

# Undefined / Other ROIs
# Breast organs:
surgical_bed_l = ROI.ROI('SurgicalBed_L','Undefined', COLORS.breast_draft)
surgical_bed_r = ROI.ROI('SurgicalBed_R','Undefined', COLORS.breast_draft)
imn_l = ROI.ROI('LN_IMN_L', 'Undefined', COLORS.imn)
imn_r = ROI.ROI('LN_IMN_R', 'Undefined', COLORS.imn)
breast_l_draft = ROI.ROI('Breast_L_Draft', 'Undefined', COLORS.contralat_draft)
breast_r_draft = ROI.ROI('Breast_R_Draft', 'Undefined', COLORS.contralat_draft)
level4_l = ROI.ROI('LN_Ax_L4_L', 'Undefined', COLORS.level4)
level3_l = ROI.ROI('LN_Ax_L3_L', 'Undefined', COLORS.level3)
level2_l = ROI.ROI('LN_Ax_L2_L', 'Undefined', COLORS.level2)
level1_l = ROI.ROI('LN_Ax_L1_L', 'Undefined', COLORS.level1)
level_l = ROI.ROI('LN_Ax_Pectoral_L', 'Undefined', COLORS.level)
level4_r = ROI.ROI('LN_Ax_L4_R', 'Undefined', COLORS.level4)
level3_r = ROI.ROI('LN_Ax_L3_R', 'Undefined', COLORS.level3)
level2_r = ROI.ROI('LN_Ax_L2_R', 'Undefined', COLORS.level2)
level1_r = ROI.ROI('LN_Ax_L1_R', 'Undefined', COLORS.level1)
level_r = ROI.ROI('LN_Ax_Pectoral_R', 'Undefined', COLORS.level)
artery1_l = ROI.ROI('A_Subclavian_L+A_Axillary_L', 'Undefined', COLORS.artery2)
artery2_l = ROI.ROI('A_Carotid_L', 'Undefined', COLORS.artery2)
vein1_l = ROI.ROI('V_Brachioceph', 'Undefined', COLORS.vein2)
vein2_l = ROI.ROI('V_Subclavian_L+V_Axillary_L','Undefined', COLORS.vein2)
vein3_l = ROI.ROI('V_Jugular_L','Undefined', COLORS.vein2)
scalene_muscle_l = ROI.ROI('ScaleneMusc_Ant_L', 'Undefined', COLORS.muscle)
scalene_muscle_r = ROI.ROI('ScaleneMusc_Ant_R', 'Undefined', COLORS.muscle)
artery1_r = ROI.ROI('A_Brachioceph', 'Undefined', COLORS.artery2)
artery2_r = ROI.ROI('A_Subclavian_R+A_Axillary_R', 'Undefined', COLORS.artery2)
artery3_r = ROI.ROI('A_Carotid_R', 'Undefined', COLORS.artery2)
vein1_r = ROI.ROI('V_Brachioceph_R', 'Undefined', COLORS.vein2)
vein2_r = ROI.ROI('V_Subclavian_R+V_Axillary_R', 'Undefined', COLORS.vein2)
vein3_r = ROI.ROI('V_Jugular_R','Undefined', COLORS.vein2)
prosthesis = ROI.ROI('Prosthesis','Undefined', COLORS.prosthesis)
prosthesis_l = ROI.ROI('Prosthesis_L','Undefined', COLORS.prosthesis)
prosthesis_r = ROI.ROI('Prosthesis_R','Undefined', COLORS.prosthesis)
# Markers:
markers = ROI.ROI('Markers', 'Marker', COLORS.clips)
seed1 = ROI.ROI('Marker1', 'Marker', COLORS.seed)
seed2 = ROI.ROI('Marker2', 'Marker', COLORS.seed)
seed3 = ROI.ROI('Marker3', 'Marker', COLORS.seed)
seed4 = ROI.ROI('Marker4', 'Marker', COLORS.seed)
marker1 = ROI.ROI('Marker1', 'Marker', COLORS.seed)
marker2 = ROI.ROI('Marker2', 'Marker', COLORS.seed)
marker3 = ROI.ROI('Marker3', 'Marker', COLORS.seed)
marker4 = ROI.ROI('Marker4', 'Marker', COLORS.seed)


# OARs: MBS (delineated by model based segmentation):
brain = ROI.ROI('Brain', 'Organ', COLORS.brain, case ='HeadNeck', model = 'Brain')
#brainstem = ROI.ROI('Brainstem', 'Organ', COLORS.brainstem, case ='HeadNeck',  model = 'Brainstem')
spinal_canal = ROI.ROI('SpinalCanal', 'Organ', COLORS.spinal_canal, case ='Thorax',  model = 'SpinalCord (Thorax)')
spinal_canal_head = ROI.ROI('SpinalCanal', 'Organ', COLORS.spinal_canal, case ='HeadNeck',  model =  'SpinalCord')
parotid_l = ROI.ROI('Parotid_L', 'Organ', COLORS.parotid, case ='HeadNeck',  model = 'ParotidGland (Left)')
parotid_r = ROI.ROI('Parotid_R', 'Organ', COLORS.parotid, case ='HeadNeck',  model = 'ParotidGland (Right)')
lung_l =  ROI.ROI('Lung_L', 'Organ', COLORS.lung, case ='Thorax',  model =  'Lung (Left)')
lung_r =  ROI.ROI('Lung_R', 'Organ', COLORS.lung, case ='Thorax',  model = 'Lung (Right)')
kidney_l = ROI.ROI('Kidney_L', 'Organ', COLORS.kidney, case ='Abdomen',  model = 'Kidney (Left)')
kidney_r = ROI.ROI('Kidney_R', 'Organ', COLORS.kidney, case ='Abdomen',  model = 'Kidney (Right)')
bladder = ROI.ROI('Bladder', 'Organ', COLORS.bladder, case ='PelvicMale',  model = 'Bladder')
femoral_l = ROI.ROI('FemoralHead_L', 'Organ', COLORS.femoral, case = 'PelvicMale', model = 'FemoralHead (Left)')
femoral_r = ROI.ROI('FemoralHead_R', 'Organ', COLORS.femoral, case = 'PelvicMale', model = 'FemoralHead (Right)')


# OARs: Unions:
parotids = ROI.ROIAlgebra('Parotids', 'Organ', COLORS.parotid, sourcesA=[parotid_l], sourcesB=[parotid_r])
submands = ROI.ROIAlgebra('SubmandGlands', 'Organ', COLORS.submand, sourcesA=[submand_l], sourcesB=[submand_r])
lungs =  ROI.ROIAlgebra('Lungs', 'Organ', COLORS.lungs, sourcesA=[lung_l], sourcesB=[lung_r])
kidneys =  ROI.ROIAlgebra('Kidneys', 'Organ', COLORS.kidneys, sourcesA=[kidney_l], sourcesB=[kidney_r])
ribs_l = ROI.ROIAlgebra('Ribs_L','Organ', COLORS.ribs, sourcesA=[rib_x_l], sourcesB=[rib_y_l])
ribs_r = ROI.ROIAlgebra('Ribs_R','Organ', COLORS.ribs, sourcesA=[rib_x_r], sourcesB=[rib_y_r])
lungs_igtv = ROI.ROIAlgebra('Lungs-IGTV', 'Organ', COLORS.lungs, sourcesA=[lungs], sourcesB=[igtv], operator = 'Subtraction')
breast_l = ROI.ROIAlgebra('Breast_L', 'Organ', COLORS.contralat, sourcesA = [breast_l_draft], sourcesB = [external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
breast_r = ROI.ROIAlgebra('Breast_R', 'Organ', COLORS.contralat, sourcesA = [breast_r_draft], sourcesB = [external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)


# OARs: Target subtracted
# Other:
other_ptv = ROI.ROI('Other_PTV', 'Organ', COLORS.other_ptv)


# PRVs:
spinal_cord_prv = ROI.ROIExpanded('SpinalCord_PRV', 'Avoidance', COLORS.prv, source=spinal_cord, margins=MARGINS.uniform_2mm_expansion)


# Walls:
skin_srt = ROI.ROIWall('Skin','Organ', COLORS.skin, body, 0, 0.3)
skin = ROI.ROIWall('Skin','Organ', COLORS.skin, external, 0, 0.3)
skin_brain_5 = ROI.ROIWall('Skin','Organ', COLORS.skin, body, 0, 0.5)
skin_brain = ROI.ROIWall('Skin','Organ', COLORS.skin, external, 0, 0.5)
wall_ptv = ROI.ROIWall('zPTV_Wall', 'Undefined', COLORS.wall, iptv, 1, 0)
wall_ptv1 = ROI.ROIWall('zPTV1_Wall', 'Undefined', COLORS.wall, iptv1, 1, 0)
wall_ptv2 = ROI.ROIWall('zPTV2_Wall', 'Undefined', COLORS.wall, iptv2, 1, 0)
wall_ptv3 = ROI.ROIWall('zPTV3_Wall', 'Undefined', COLORS.wall, iptv3, 1, 0)

# ROIs for optimization:
z_water =  ROI.ROI('zWater', 'Undefined', COLORS.other_ptv)
z_heart =  ROI.ROI('zHeart', 'Undefined', COLORS.heart)
z_esophagus =  ROI.ROI('zEsophagus', 'Undefined', COLORS.esophagus)
z_bladder = ROI.ROI('zBladder','Undefined', COLORS.bladder)
z_spc_bowel = ROI.ROI('zBowelBag','Undefined', COLORS.bowel_space)
z_rectum = ROI.ROI('zRectum', 'Undefined', COLORS.rectum)
dorso_rectum = ROI.ROI('zRectum_P', 'Undefined', COLORS.dorso_rectum)
z_rectum_p = ROI.ROI('zRectum_P', 'Undefined', COLORS.dorso_rectum)
z_ptv_77_wall = ROI.ROI('zPTV_77_Wall', 'Undefined', COLORS.wall)
z_ptv_70_77_wall = ROI.ROI('zPTV_70+77_Wall', 'Undefined', COLORS.wall)
z_ptv_67_5_wall = ROI.ROI('zPTV_67.5_Wall', 'Undefined', COLORS.wall)
z_ptv_62_5_67_5_wall = ROI.ROI('zPTV_62.5+67.5_Wall', 'Undefined', COLORS.wall)
z_ptv_50_62_5_67_5_wall = ROI.ROI('zPTV_50+62.5+67.5_Wall', 'Undefined', COLORS.wall)
z_ptv_60_wall = ROI.ROI('zPTV_60_Wall', 'Undefined', COLORS.wall)
z_ptv_50_wall = ROI.ROI('zPTV_50_Wall', 'Undefined', COLORS.wall)
z_ptv_47_50_wall = ROI.ROI('zPTV_47+50_Wall', 'Undefined', COLORS.wall)
z_ptv_57_60_wall = ROI.ROI('zPTV_57+60_Wall', 'Undefined', COLORS.wall)
z_ptv_70_wall = ROI.ROI('zPTV_70_Wall', 'Undefined', COLORS.wall)
z_ptv_62_5_wall = ROI.ROI('zPTV_62.5_Wall', 'Undefined', COLORS.wall)
z_ptv_56_temp = ROI.ROI('zPTV_56_Temp', 'Undefined', COLORS.wall)
z_ptv_56_wall = ROI.ROI('zPTV_56_Wall', 'Undefined', COLORS.wall)
z_ptv_50_temp = ROI.ROI('zPTV_50_Temp', 'Undefined', COLORS.wall)
z_ptv_50_wall = ROI.ROI('zPTV_50_Wall', 'Undefined', COLORS.wall)
z_ptv_wall = ROI.ROI('zPTV_Wall', 'Undefined', COLORS.wall)
z_ptv1_wall = ROI.ROI('zPTV1_Wall', 'Undefined', COLORS.wall)
z_ptv2_wall = ROI.ROI('zPTV2_Wall', 'Undefined', COLORS.wall)
z_ptv3_wall = ROI.ROI('zPTV3_Wall', 'Undefined', COLORS.wall)
z_ptv4_wall = ROI.ROI('zPTV4_Wall', 'Undefined', COLORS.wall)
ctv_oars = ROI.ROI('zCTV-OARs', 'Ctv', COLORS.ctv)
ptv_oars = ROI.ROI('zPTV-OARs', 'Ptv', COLORS.ptv)
ptv_and_oars = ROI.ROI('zPTV_AND_OARs', 'Ptv', COLORS.other_ptv)
z_eye_l = ROI.ROIWall('zEye_L','Undefined', COLORS.wall, eye_l, 0, 0.2)
z_eye_r = ROI.ROIWall('zEye_R','Undefined', COLORS.wall, eye_r, 0, 0.2)

# Substitute ROI objects (only used for naming):
# Targets:
ptv_77 = ROI.ROI('PTV_77', 'Ptv', COLORS.ptv_high)
ptv_70 = ROI.ROI('PTV_70', 'Ptv', COLORS.ptv_med)
ptv_70_sib = ROI.ROI('PTV!_70', 'Ptv', COLORS.ptv_med)
ctv_77 = ROI.ROI('CTV_77', 'Ctv', COLORS.ctv_high)
ctv_70 = ROI.ROI('CTV_70', 'Ctv', COLORS.ctv_med)
ctv_70_sib = ROI.ROI('CTV!_70', 'Ctv', COLORS.ctv_med)
ptv_56 = ROI.ROI('PTV!_56', 'Ptv', COLORS.ptv_low)
ctv_56 = ROI.ROI('CTV!_56', 'Ctv', COLORS.ctv_low)
ptv_70_77 = ROI.ROI('PTV_70+77', 'Ptv', COLORS.ptv_low)
ctv_70_77 = ROI.ROI('CTV_70+77', 'Ctv', COLORS.ctv_low)
ptv_56_70_77 = ROI.ROI('PTV_56+70+77', 'Ptv', COLORS.ptv_low)
ptv_56_70 = ROI.ROI('PTV_56+70', 'Ptv', COLORS.ptv_low)

ptv_67_5 = ROI.ROI('PTV_67.5', 'Ptv', COLORS.ptv_high)
ptv_62_5 = ROI.ROI('PTV_62.5', 'Ptv', COLORS.ptv_med)
ptv_62_5_sib = ROI.ROI('PTV!_62.5', 'Ptv', COLORS.ptv_med)
ctv_67_5 = ROI.ROI('CTV_67.5', 'Ctv', COLORS.ctv_high)
ctv_62_5 = ROI.ROI('CTV_62.5', 'Ctv', COLORS.ctv_med)
ctv_62_5_sib = ROI.ROI('CTV!_62.5', 'Ctv', COLORS.ctv_med)
ptv__50 = ROI.ROI('PTV!_50', 'Ptv', COLORS.ptv_low)
ctv__50 = ROI.ROI('CTV!_50', 'Ctv', COLORS.ctv_low)
ptv_62_5_67_5 = ROI.ROI('PTV_62.5+67.5', 'Ptv', COLORS.ptv_low)
ctv_62_5_67_5 = ROI.ROI('CTV_62.5+67.5', 'Ctv', COLORS.ctv_low)
ptv_50_62_5_67_5 = ROI.ROI('PTV_50+62.5+67.5', 'Ptv', COLORS.ptv_low)
ptv_50_62_5 = ROI.ROI('PTV_50+62.5', 'Ptv', COLORS.ptv_low)

ptv_57_60 = ROI.ROI('PTV_57+60', 'Ptv', COLORS.ptv_low)
ctv_57_60 = ROI.ROI('CTV_57+60', 'Ctv', COLORS.ctv_low)
ptv_60 = ROI.ROI('PTV_60', 'Ptv', COLORS.ptv_high)
ctv_60 = ROI.ROI('CTV_60', 'Ctv', COLORS.ctv_high)
ptv_57 = ROI.ROI('PTV!_57', 'Ptv', COLORS.ptv_med)
ctv_57 = ROI.ROI('CTV!_57', 'Ctv', COLORS.ctv_med)

ptv_semves = ROI.ROI('PTV_SeminalVes', 'Ptv', COLORS.ptv_med)

ptv_pc =  ROI.ROI('PTVpc', 'Ptv', COLORS.ptv)
ptv_pc_l =  ROI.ROI('PTVpc_L', 'Ptv', COLORS.ptv)
ptv_pc_r =  ROI.ROI('PTVpc_R', 'Ptv', COLORS.ptv)
ptv_p = ROI.ROI('PTVp', 'Ptv', COLORS.ptv)
ptv_n =  ROI.ROI('PTVn', 'Ptv', COLORS.ptv)
ptv_nc =  ROI.ROI('PTVnc', 'Ptv', COLORS.ptv)
ptv1 =  ROI.ROI('PTV1', 'Ptv', COLORS.ptv)
ptv2 =  ROI.ROI('PTV2', 'Ptv', COLORS.ptv)
ptv3 =  ROI.ROI('PTV3', 'Ptv', COLORS.ptv)
ptv4 =  ROI.ROI('PTV4', 'Ptv', COLORS.ptv)
ptv_c = ROI.ROI('PTVc', 'Ptv', COLORS.ptv)
ptv_sb = ROI.ROI('PTVsb', 'Ptv', COLORS.ptv)
ptv_sbc = ROI.ROI('PTVsbc', 'Ptv', COLORS.ptv)

ctv_47_50 =  ROI.ROI('CTV_47+50', 'Ctv', COLORS.ctv_low)
ptv_47_50 =  ROI.ROI('PTV_47+50', 'Ptv', COLORS.ptv_low)
ptv_50 = ROI.ROI('PTV_50', 'Ptv', COLORS.ptv_high)
ptv_50c = ROI.ROI('PTV_50c', 'Ptv', COLORS.ptv_high)
ctv_50 = ROI.ROI('CTV_50', 'Ctv', COLORS.ctv_high)
ctv_47 =  ROI.ROI('CTV!_47', 'Ctv', COLORS.ctv_low)
ctv_47_tot =  ROI.ROI('CTV_47', 'Ctv', COLORS.ctv_low)
ptv_47 =  ROI.ROI('PTV!_47', 'Ptv', COLORS.ptv_med)
ptv_47_tot =  ROI.ROI('PTV_47', 'Ptv', COLORS.ptv_med)
ptv_47c =  ROI.ROI('PTV!_47c', 'Ptv', COLORS.ptv_med)


# Miscellaneous:
brain_gtv = ROI.ROI('Brain-GTV','Organ', COLORS.brain)
brain_ptv = ROI.ROI('Brain-PTV','Organ', COLORS.other_ptv)
lungs_gtv = ROI.ROI('Lungs-GTV', 'Organ', COLORS.lungs)
lungs_ctv = ROI.ROI('Lungs-CTV', 'Organ', COLORS.lungs)
ctv_p_ctv_sb = ROI.ROI('CTVp-CTVsb', 'Ctv', COLORS.ctv)
ctv_ctv_sb = ROI.ROI('CTV-CTVsb', 'Ctv', COLORS.ctv)
ptv_pc_ptv_sbc = ROI.ROI('PTVpc-PTVsbc', 'Ptv', COLORS.ptv)
ptv_c_ptv_sbc = ROI.ROI('PTVc-PTVsbc', 'Ptv', COLORS.ptv)
ptv_gtv = ROI.ROI('PTV-GTV', 'Ptv', COLORS.ptv_med)
ptv_spinal = ROI.ROI('PTV-SpinalCord_PRV', 'Ptv', COLORS.ptv_med)
mask_ptv = ROI.ROI('Mask_PTV','Undefined', COLORS.mask_ptv)
mask_ptv1 = ROI.ROI('Mask_PTV1','Undefined', COLORS.mask_ptv)
mask_ptv2 = ROI.ROI('Mask_PTV2','Undefined', COLORS.mask_ptv)
mask_ptv3 = ROI.ROI('Mask_PTV3','Undefined', COLORS.mask_ptv)
box = ROI.ROI('zBox','Undefined', COLORS.mask_ptv)
box1 = ROI.ROI('zBox1','Undefined', COLORS.mask_ptv)
box_l = ROI.ROI('zBox_L','Undefined', COLORS.mask_ptv)
box_r = ROI.ROI('zBox_R','Undefined', COLORS.mask_ptv)
box3 = ROI.ROI('zBox3','Undefined', COLORS.mask_ptv)
box4 = ROI.ROI('zBox4','Undefined', COLORS.mask_ptv)
