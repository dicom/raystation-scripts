# encoding: utf8

# Import local files:
import clinical_goal as CG
import rois as ROIS
import tolerance_doses as TOL
import roi_functions as ROIF
import structure_set_functions as SSF
import region_codes as RC


# Criterias:
at_most = 'AtMost'
at_least = 'AtLeast'

# Types:
volume_at_dose = 'VolumeAtDose'
abs_volume_at_dose = 'AbsoluteVolumeAtDose'
dose_at_abs_volume = 'DoseAtAbsoluteVolume'
dose_at_volume = 'DoseAtVolume'
average_dose = 'AverageDose'
homogeneity_index = 'HomogeneityIndex'
conformity_index = 'ConformityIndex'

# Priorities:
priority1 = 1
priority2 = 2
priority3 = 3
priority4 = 4
priority5 = 5
priority6 = 6
priority7 = 7
priority8 = 8

# Absolute volumes:
cc0 = 0
cc0_1 = 0.1
cc0_2 = 0.2
cc0_03 = 0.03
cc0_35 = 0.35
cc0_5 = 0.5
cc1 = 1
cc1_2 = 1.2
cc2 = 2
cc3 = 3
cc4 = 4
cc5 = 5
cc10 = 10
cc15 = 15
cc20 = 20
cc30 = 30
cc195 = 195
cc200 = 200
cc700 = 700
cc1000 = 1000
cc1500 = 1500

# Percent volumes:
pc1 = 0.01
pc2 = 0.02
pc3 = 0.03
pc5 = 0.05
pc10 = 0.1
pc15 = 0.15
pc17 = 0.17
pc20 = 0.2
pc25 = 0.25
pc26 = 0.26
pc30 = 0.3
pc33 = 0.33
pc32 = 0.32
pc35 = 0.35
pc37 = 0.37
pc40 = 0.40
pc50 = 0.5
pc55 = 0.55
pc60 = 0.6
pc65 = 0.65
pc66 = 0.66
pc69_1 = 0.6909090909
pc70 = 0.7
pc71_3 = 0.713
pc72_36 = 0.7236363636
pc73_09 = 0.7309090909
pc75 = 0.75
pc76 = 0.76
pc76_36 = 0.763636363636
pc78 = 0.78
pc78_4 = 0.784
pc79_6 = 0.796
pc80 = 0.8
pc80_4 = 0.804
pc84 = 0.84
pc84_6 = 0.846
pc85 = 0.85
pc86 = 0.86
pc88 = 0.88
pc86_36 = 0.863636
pc88_36 = 0.8836
pc89_1 = 0.891
pc89_3 = 0.893
pc90 = 0.9
pc90_24 = 0.9024
pc90_25 = 0.9025
pc90_45 = 0.9045454545
pc91_36 = 0.9136363636
pc92 = 0.92
pc92_12 = 0.9212
pc93 = 0.93
pc93_53 = 0.9353
pc94_52 = 0.94525
pc94_47 = 0.9447
pc94 = 0.94
pc95 = 0.95
pc95_47 = 0.95475
pc95_88 = 0.9588
pc96 = 0.96
pc93_1 = 0.931
pc97 = 0.97
pc98 = 0.98
pc98_7 = 0.987
pc99 = 0.99
pc99_5 = 0.995
pc99_75 = 0.9975
pc100 = 1
pc100_5 = 1.005
pc105 = 1.05
pc102 = 1.02
pc132 = 1.32
pc139 = 1.386
pc140 = 1.4
pc147 = 1.469475655
pc150 = 1.5
pc170 = 1.7

# Create CG.ClinicalGoal objects:
# Example:
#ClinicalGoal(name, criteria, type, tolerance, value, priority)

# Create Clinical goals for ORGANS AT RISK
# (Sorted cranio-caudally)

# Brain:
def brain_oars(nr_fractions, region_code):
  if region_code in RC.brain_whole_codes:
    brain_oars = [
      CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, average_dose, TOL.cochlea_mean_tinnitus, None, priority3),
      CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, average_dose, TOL.cochlea_mean_tinnitus, None, priority3),
      CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0_03, priority3),
      CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0_03, priority3),
      CG.ClinicalGoal(ROIS.lacrimal_l.name, at_most, average_dose, TOL.lacrimal_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lacrimal_r.name, at_most, average_dose, TOL.lacrimal_mean, None, priority3),
      CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_v003_adx, cc0_03, priority6)
		]
  elif region_code in RC.brain_partial_codes:
    if nr_fractions == 1: # Stereotactic, one fraction
      brain_oars = [
        CG.ClinicalGoal(ROIS.brain_ptv.name, at_most, dose_at_abs_volume, TOL.brain_srt_1fx_v10, cc10, priority2),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_1fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_1fx_v0_5, cc0_5, priority2),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_1fx_v0_2, cc0_2, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_v0_2, cc0_2, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_v0_2, cc0_2, priority3),
        CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, dose_at_abs_volume, TOL.cochlea_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, dose_at_abs_volume, TOL.cochlea_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.eye_r.name, at_most, dose_at_abs_volume, TOL.eye_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.eye_l.name, at_most, dose_at_abs_volume, TOL.eye_srt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_srt_1fx_v10, cc10, priority4),
        CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_srt_1fx_v0, cc0, priority4),
        CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_srt_1fx_v0, cc0, priority4),
        CG.ClinicalGoal(ROIS.hippocampus_l.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
        CG.ClinicalGoal(ROIS.hippocampus_r.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
        CG.ClinicalGoal(ROIS.brain_gtv.name, at_most, dose_at_abs_volume, TOL.brain_srt_1fx_v10, cc10, priority6)
      ]
    elif nr_fractions == 3: # Stereotactic, three fractions
      brain_oars = [
        CG.ClinicalGoal(ROIS.brain_ptv.name, at_most, dose_at_abs_volume, TOL.brain_srt_3fx_v10, cc10, priority2),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_3fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_3fx_v0_5, cc0_5, priority2),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_3fx_v0_2, cc0_2, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_v0_2, cc0_2, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_v0_2, cc0_2, priority3),
        CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, dose_at_abs_volume, TOL.cochlea_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, dose_at_abs_volume, TOL.cochlea_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.eye_r.name, at_most, dose_at_abs_volume, TOL.eye_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.eye_l.name, at_most, dose_at_abs_volume, TOL.eye_srt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_srt_3fx_v10, cc10, priority3),
        CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_srt_3fx_v0, cc0, priority4),
        CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_srt_3fx_v0, cc0, priority4),
        CG.ClinicalGoal(ROIS.hippocampus_l.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
        CG.ClinicalGoal(ROIS.hippocampus_r.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
        CG.ClinicalGoal(ROIS.brain_gtv.name, at_most, dose_at_abs_volume, TOL.brain_srt_3fx_v10, cc10, priority6)
      ]
    else: # Partial brain
      brain_oars = [ 
        CG.ClinicalGoal(ROIS.brainstem_surface.name, at_most, dose_at_abs_volume, TOL.brainstem_surface_v003_adx, cc0_03, priority2),
        CG.ClinicalGoal(ROIS.brainstem_core.name, at_most, dose_at_abs_volume, TOL.brainstem_core_v003_adx, cc0_03, priority2),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_v003_adx, cc0_03, priority2),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_v003_adx, cc0_03, priority2),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_v003_adx, cc0_03, priority2),
        CG.ClinicalGoal(ROIS.retina_l.name, at_most, dose_at_abs_volume, TOL.retina_v003_adx, cc0_03, priority3),
        CG.ClinicalGoal(ROIS.retina_r.name, at_most, dose_at_abs_volume, TOL.retina_v003_adx, cc0_03, priority3),
        CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, average_dose, TOL.cochlea_mean, None, priority3),
        CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, average_dose, TOL.cochlea_mean, None, priority3),
        CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, average_dose, TOL.cochlea_mean_tinnitus, None, priority4),
        CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, average_dose, TOL.cochlea_mean_tinnitus, None, priority4),
        CG.ClinicalGoal(ROIS.lacrimal_l.name, at_most, average_dose, TOL.lacrimal_mean, None, priority4),
        CG.ClinicalGoal(ROIS.lacrimal_r.name, at_most, average_dose, TOL.lacrimal_mean, None, priority4),
        CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0_03, priority4),
        CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0_03, priority4),
        CG.ClinicalGoal(ROIS.pituitary.name, at_most, average_dose, TOL.pituitary_mean, None, priority4),
        CG.ClinicalGoal(ROIS.pituitary.name, at_most, average_dose, TOL.pituitary_2_mean, None, priority4),
        CG.ClinicalGoal(ROIS.cornea_l.name, at_most, dose_at_abs_volume, TOL.cornea_v003_adx, cc0_03, priority4),
        CG.ClinicalGoal(ROIS.cornea_r.name, at_most, dose_at_abs_volume, TOL.cornea_v003_adx, cc0_03, priority4),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_v003_adx, cc0_03, priority5),
        CG.ClinicalGoal(ROIS.hippocampus_l.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
        CG.ClinicalGoal(ROIS.hippocampus_r.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
        CG.ClinicalGoal(ROIS.brain.name, at_most, dose_at_abs_volume, TOL.brain_v003, cc3, priority5)
      ]
  return brain_oars


# Breast (Regional breast/Whole breast/Partial breast):
def breast_oars(ss, region_code):
  # Common for all breast variants:
  breast_oars = [
    CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean_breast, None, priority3),
    CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, pc65, TOL.lung_v65_adx_25, priority5)
  ]
  if region_code in RC.breast_reg_codes:
    # Common for regional left & right:
    breast_oars += [
      CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinalcanal_v2_adx, cc2, priority2),
      CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean_breast_15, None, priority3),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, average_dose, TOL.esophagus_mean_brt, None, priority5),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, volume_at_dose, pc15, TOL.esophagus_v15_adx_brt, priority5),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, volume_at_dose, pc30, TOL.esophagus_v30_adx_brt, priority5),
      CG.ClinicalGoal(ROIS.thyroid.name, at_most, average_dose, TOL.thyroid_mean_brt, None, priority5)  
    ]
    # Thyroid absolute volume CG for regional breast:
    if SSF.has_named_roi_with_contours(ss, ROIS.thyroid.name):
      volume = ss.RoiGeometries[ROIS.thyroid.name].GetRoiVolume()
      breast_oars.append(CG.ClinicalGoal(ROIS.thyroid.name, at_most, abs_volume_at_dose, volume-8.5, TOL.thyroid_v8_5cc_adx_brt, priority5))
    if region_code in RC.breast_reg_l_codes:
      # Specific for regional left:
      breast_oars += [
        CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx_15, priority4),
        CG.ClinicalGoal(ROIS.breast_r.name, at_most, average_dose, TOL.contralat_breast_mean, None, priority5),
        CG.ClinicalGoal(ROIS.humeral_l.name, at_most, volume_at_dose, pc33, TOL.humeral_v33_adx, priority6)
      ]
    else:
      # Specific for regional right:
      breast_oars += [
        CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx_15, priority4),
        CG.ClinicalGoal(ROIS.breast_l.name, at_most, average_dose, TOL.contralat_breast_mean, None, priority5),
        CG.ClinicalGoal(ROIS.humeral_r.name, at_most, volume_at_dose, pc33, TOL.humeral_v33_adx, priority6)
      ]
  else:
    # Non-regional breast:
    if region_code in RC.breast_l_codes:
      # Common for whole breast & partial breast, left:
      breast_oars += [CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc15, TOL.lung_v15_adx, priority4)]
    elif region_code in RC.breast_r_codes:
      # Common for whole breast & partial breast, right:
      breast_oars += [CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc15, TOL.lung_v15_adx, priority4)]
    if region_code in RC.breast_partial_l_codes:
      # Specific for partial breast left:
      breast_oars += [CG.ClinicalGoal(ROIS.breast_l.name, at_most, volume_at_dose, pc50, TOL.ipsilateral_breast_v50_adx, priority5)]
    elif region_code in RC.breast_partial_r_codes:
      # Specific for partial breast right:
      breast_oars += [CG.ClinicalGoal(ROIS.breast_r.name, at_most, volume_at_dose, pc50, TOL.ipsilateral_breast_v50_adx, priority5)]
  return breast_oars


# Lung:
# (In cases where a GTV/IGTV is present, clinical goals are created for 'Lungs-GTV'/'Lungs-IGTV' instead of 'Lungs')
def lung_oars(ss):
  lung = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcanal_v2_adx, pc2, priority2),
    CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean, None, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc25, TOL.heart_v25_adx, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, average_dose, TOL.esophagus_mean, None, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, volume_at_dose, pc17, TOL.esophagus_v17_adx, priority3),
    CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority6),
    CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority6),
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcanal_chemo_v2_adx, pc2, priority6)
  ]
  if SSF.has_roi_with_shape(ss, ROIS.lungs_gtv.name):
    l = ROIS.lungs_gtv.name
  elif SSF.has_roi_with_shape(ss, ROIS.lungs_igtv.name):
    l = ROIS.lungs_igtv.name
  else:
    l = ROIS.lungs.name
  lung.extend([
    CG.ClinicalGoal(l, at_most, average_dose, TOL.lung_mean, None, priority3),
    CG.ClinicalGoal(l, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority3)
  ])
  return lung


# Lung SBRT:
# For a treatment with three fractions, from the region code, one finds if the
# tumor is right or left sided and clinical goals are added accordingly.
def lung_stereotactic_3fx_oars(region_code):
  lung = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v1_2, cc1_2, priority2),
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0, cc0, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_3fx_v4, cc4, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_3fx_v0, cc0, priority2),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v5, cc5, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_3fx_v10, cc10, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_3fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_v15, cc15, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_sbrt_3fx_mean, None, priority3),
    CG.ClinicalGoal(ROIS.liver.name, at_most, dose_at_abs_volume, TOL.liver_sbrt_3fx_v700 , cc700, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc10, TOL.lung_sbrt_3fx_v10, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_3fx_v1500, cc1500, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_3fx_v1000, cc1000, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc37, TOL.lung_sbrt_3fx_v37, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc40, TOL.lung_sbrt_3fx_v40, priority3),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, abs_volume_at_dose, cc30, TOL.chestwall_sbrt_3fx_v30, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_3fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_3fx_v0, cc0, priority4)
  ]
  if region_code in [248, 250]: # Right
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_contra_sbrt_3fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v2, cc2, priority6)
    ])
  elif region_code in [247, 249]: # Left
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_contra_sbrt_3fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v2, cc2, priority6)
    ])
  else:
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_contra_sbrt_3fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_contra_sbrt_3fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v2, cc2, priority6),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v2, cc2, priority6)
    ])
  return lung


# Lung SBRT:
# For a treatment with five fractions, from the region code, one finds if the
# tumor is right or left sided and clinical goals are added accordingly.
def lung_stereotactic_5fx_oars(region_code):
  lung = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_5fx_v1_2, cc1_2, priority2),
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_5fx_v0, cc0, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_5fx_v4, cc4, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_5fx_v0, cc0, priority2),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_5fx_v5, cc5, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_5fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_5fx_v10, cc10, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_5fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_5fx_v15, cc15, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_5fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_sbrt_3fx_mean, None, priority3),
    CG.ClinicalGoal(ROIS.liver.name, at_most, dose_at_abs_volume, TOL.liver_sbrt_5fx_v700 , cc700, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc10, TOL.lung_sbrt_3fx_v10, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_5fx_v1500, cc1500, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_5fx_v1000, cc1000, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc37, TOL.lung_sbrt_5fx_v37, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc40, TOL.lung_sbrt_3fx_v40, priority3),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, abs_volume_at_dose, cc30, TOL.chestwall_sbrt_5fx_v30, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_5fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_5fx_v0, cc0, priority4)
  ]
  if region_code in [248, 250]: # Right
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6)
    ])
  elif region_code in [247, 249]: # Left
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6)
    ])
  else:
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.rib_y_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.rib_y_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.rib_x_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6),
      CG.ClinicalGoal(ROIS.rib_x_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6)
    ])
  return lung


# Lung SBRT:
# For a treatment with eight fractions, from the region code, one finds if the
# tumor is right or left sided and clinical goals are added accordingly.
def lung_stereotactic_8fx_oars(region_code):
  lung = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_5fx_v1_2, cc1_2, priority2),
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_8fx_v0, cc0, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_5fx_v4, cc4, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_8fx_v0, cc0, priority2),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_5fx_v5, cc5, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_8fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_5fx_v10, cc10, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_5fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_5fx_v15, cc15, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_8fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_sbrt_3fx_mean, None, priority3),
    CG.ClinicalGoal(ROIS.liver.name, at_most, dose_at_abs_volume, TOL.liver_sbrt_5fx_v700 , cc700, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc10, TOL.lung_sbrt_3fx_v10, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_5fx_v1500, cc1500, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_5fx_v1000, cc1000, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc37, TOL.lung_sbrt_5fx_v37, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc40, TOL.lung_sbrt_3fx_v40, priority3),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, abs_volume_at_dose, cc30, TOL.chestwall_sbrt_5fx_v30, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_5fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_5fx_v0, cc0, priority4)
  ]
  if region_code in [248, 250]: # Right
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_contra_sbrt_8fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6)
    ])
  elif region_code in [247, 249]: # Left
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_contra_sbrt_8fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6)
    ])
  else:
    lung.extend([
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_contra_sbrt_8fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_contra_sbrt_8fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_contra_sbrt_5fx_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc26, TOL.lung_contra_sbrt_5fx_v26, priority3),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx_v0, cc0, priority4),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx_v1, cc1, priority6)
    ])
  return lung


# Rectum:
rectum_oars = [
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority2),
  CG.ClinicalGoal(ROIS.femoral_l.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority3),
  CG.ClinicalGoal(ROIS.femoral_r.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority3),
  CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc2, TOL.bladder_v2_adx, priority4)
]


# Bladder:
bladder_oars = [
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc50, TOL.rectum_v50_adx,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc35, TOL.rectum_v35_adx,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc25, TOL.rectum_v25_adx,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc15, TOL.rectum_v15_adx,  priority3),
  CG.ClinicalGoal(ROIS.femoral_l.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4),
  CG.ClinicalGoal(ROIS.femoral_r.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4)
]


# Prostate:
def prostate_oars(ss, total_dose):
  if total_dose in [55, 60]:
    prostate = [
      CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc60, TOL.rectum_v40_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc50, TOL.rectum_v48_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc30, TOL.rectum_v52_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc15, TOL.rectum_v57_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc3, TOL.rectum_v60_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc60, TOL.rectum_v40_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc50, TOL.rectum_v48_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc30, TOL.rectum_v52_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc15, TOL.rectum_v57_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc3, TOL.rectum_v60_adx_hypo,  priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v40_adx_hypo, priority4),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc25, TOL.bladder_v48_adx_hypo, priority4),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc5, TOL.bladder_v60_adx_hypo, priority4),
      CG.ClinicalGoal(ROIS.femoral_l.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4),
      CG.ClinicalGoal(ROIS.femoral_r.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4)
    ]
  elif total_dose > 60:
    prostate = [
      CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc50, TOL.rectum_v50_adx,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc35, TOL.rectum_v35_adx,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc25, TOL.rectum_v25_adx,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc20, TOL.rectum_v20_adx,  priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc15, TOL.rectum_v15_adx,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc50, TOL.rectum_v50_adx,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc35, TOL.rectum_v35_adx,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc25, TOL.rectum_v25_adx,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc20, TOL.rectum_v20_adx,  priority3),
      CG.ClinicalGoal(ROIS.anal_canal.name, at_most, volume_at_dose, pc15, TOL.rectum_v15_adx,  priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v50_adx, priority4),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc35, TOL.bladder_v35_adx, priority4),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc25, TOL.bladder_v25_adx, priority4),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc15, TOL.bladder_v15_adx, priority4),
      CG.ClinicalGoal(ROIS.femoral_l.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4),
      CG.ClinicalGoal(ROIS.femoral_r.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4)
    ]
  elif total_dose <40:
    prostate = [
      CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc50, TOL.rectum_v50_adx,  priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v50_adx, priority3),
      CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3),
      CG.ClinicalGoal(ROIS.femoral_l.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4),
      CG.ClinicalGoal(ROIS.femoral_r.name, at_most, average_dose, TOL.femoral_mean_adx, None, priority4)
    ]
  return prostate


# Bone/Spine SBRT:
# For a treatment with one fraction, from the region code, one finds whether the
# tumor is in the thoracic or pelvis area, and clinical goals are added accordingly.
# There is also a separation between spine/non-spine treatment.
def bone_stereotactic_1fx_oars(region_code):
  spine = [
    CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_hilum_1fx_v66, pc66, priority3),
    CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_hilum_1fx_v66, pc66, priority3),
    CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_sbrt_1fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_sbrt_1fx_v0, cc0, priority3),
    CG.ClinicalGoal(ROIS.kidneys.name, at_most, dose_at_abs_volume, TOL.kidneys_col_1fx_v200, cc200, priority3),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_1fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_1fx_v0, cc0, priority4)
  ]
  if region_code in RC.stereotactic_spine_thorax_codes or region_code in RC.stereotactic_spine_pelvis_codes:
    spine.extend([
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0_35, cc0_35, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0_1, cc0_1, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_1fx_v0, cc5, priority2)
    ])
    if region_code in RC.stereotactic_spine_thorax_codes:
      spine.extend([
        CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_1fx_v4, cc4, priority2),
        CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_1fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_1fx_v15, cc15, priority3),
        CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.lungs.name, at_most, dose_at_abs_volume, TOL.lungs_sbrt_1fx_v1000, cc1000, priority3),
        CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_1fx_v5, cc5, priority3),
        CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_1fx_v0, cc0, priority3)
      ])
  if region_code in RC.stereotactic_spine_pelvis_codes or region_code in RC.stereotactic_pelvis_codes:
    spine.extend([
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_1fx_v5, cc5, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_1fx_v20, cc20, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_1fx_v20, cc20, priority3)
    ])
  return spine


# Bone/Spine SBRT:
# For a treatment with three fractions, from the region code, one finds whether the
# tumor is in the thoracic or pelvis area, and clinical goals are added accordingly.
# There is also a separation between spine/non-spine treatment.
def bone_stereotactic_3fx_oars(region_code):
  spine = [
    CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_3fx_v10, pc10, priority3),
    CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_3fx_v10, pc10, priority3),
    CG.ClinicalGoal(ROIS.kidneys.name, at_most, dose_at_abs_volume, TOL.kidneys_col_3fx_v200, cc200, priority3),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_col_sbrt_3fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_col_sbrt_3fx_v0, cc0, priority4)
  ]
  if region_code in RC.stereotactic_spine_thorax_codes or region_code in RC.stereotactic_spine_pelvis_codes:
    spine.extend([
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_3fx_v5, cc5, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0_35, cc0_35, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0, cc0, priority2)
    ])
    if region_code in RC.stereotactic_spine_thorax_codes:
      spine.extend([
        CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_3fx_v4, cc4, priority2),
        CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_3fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_v15, cc15, priority3),
        CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.lungs.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_3fx_v1000, cc1000, priority3),
        CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v5, cc5, priority3),
        CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v0, cc0, priority3)
      ])
  if region_code in RC.stereotactic_spine_pelvis_codes or region_code in RC.stereotactic_pelvis_codes:
    spine.extend([
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_3fx_v5, cc5, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_3fx_v20, cc20, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_3fx_v20, cc20, priority3)
    ])
  return spine


# Palliative:
head = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.brain.name, at_most, dose_at_abs_volume, TOL.brain_v003, cc0, priority3),
  CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0, priority4),
  CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0, priority4)
]
neck = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.parotids.name, at_most, average_dose, TOL.parotids_mean, None, priority3)
]
thorax = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean, None, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc30, TOL.heart_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc60, TOL.heart_v60_adx, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc80, TOL.heart_v80_adx, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, average_dose, TOL.lung_mean, None, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority3)
]
thorax_and_abdomen = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean, None, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc30, TOL.heart_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc60, TOL.heart_v60_adx, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc80, TOL.heart_v80_adx, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, average_dose, TOL.lung_mean, None, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, average_dose, TOL.kidney_mean, None, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc55, TOL.kidney_v55_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc32, TOL.kidney_v32_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc30, TOL.kidney_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc20, TOL.kidney_v20_adx, priority3),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3)
]
abdomen = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, average_dose, TOL.kidney_mean, None, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc55, TOL.kidney_v55_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc32, TOL.kidney_v32_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc30, TOL.kidney_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc20, TOL.kidney_v20_adx, priority3),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3)
]
abdomen_and_pelvis = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, average_dose, TOL.kidney_mean, None, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc55, TOL.kidney_v55_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc32, TOL.kidney_v32_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc30, TOL.kidney_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc20, TOL.kidney_v20_adx, priority3),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc50, TOL.rectum_v50_adx,  priority3),
  CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v50_adx, priority4)
]
pelvis = [
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowelspace_v195_adx, priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, pc50, TOL.rectum_v50_adx,  priority3),
  CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v50_adx, priority4)
]
other = []




# Create Clinical goals for TARGETS
# (Sorted cranio-caudally)

# Common targets:
# Used for simple cases and most palliative cases.
targets = [
  CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
  CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
  CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
  CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98, priority4),
  CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
  CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
  CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5)
]


# Palliative thorax targets:
# FIXME: Er det riktig å ha andre krav for thorax relaterte palliative MV?!? Vurdere å ta bort.
thorax_targets = [
  CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
  CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
  CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc95, pc98, priority2),
  CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
  CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
  CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc95, pc95, priority5),
  CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc90, pc95, priority5)
]


# Palliative:
def palliative_targets(ss, plan, target):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  targets = [CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4)]
  if nr_targets > 1 and len(list(plan.BeamSets)) > 1:
    for i in range(0, nr_targets):
      targets.extend([
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_least, dose_at_volume, pc99_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_most, dose_at_volume, pc100_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_least, dose_at_volume, pc98, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, dose_at_volume, pc95, pc98, priority4),
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_least, homogeneity_index, pc95, pc98, priority5),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, conformity_index, pc90, pc95, priority5)
      ])
  else:
    targets.extend([
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(target, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(target.replace("C", "P"), at_least, dose_at_volume, pc95, pc98, priority4),
      CG.ClinicalGoal(target, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(target.replace("C", "P"), at_least, conformity_index, pc90, pc95, priority5)
    ])

  return targets


# Brain:
def brain_targets(ss, nr_fractions):
  if nr_fractions in [1,3]: # Stereotactic, one target
    brain_targets = [
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc100, pc99, priority1),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc170, cc0, priority4),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc100, priority5)
    ]
    nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
    if nr_targets in [2, 3, 4]: # Stereotactic, 2, 3 or 4 targets
      brain_targets.extend([
        CG.ClinicalGoal(ROIS.ptv1.name, at_least, dose_at_volume, pc100, pc99, priority1),
        CG.ClinicalGoal(ROIS.ptv2.name, at_least, dose_at_volume, pc100, pc99, priority1),
        CG.ClinicalGoal(ROIS.ptv1.name, at_least, conformity_index, pc90, pc100, priority5),
        CG.ClinicalGoal(ROIS.ptv2.name, at_least, conformity_index, pc90, pc100, priority5)
      ])
      if nr_targets in [3, 4]: # Stereotactic, 3 or 4 targets
        brain_targets.extend([
          CG.ClinicalGoal(ROIS.ptv3.name, at_least, dose_at_volume, pc100, pc99, priority1),
          CG.ClinicalGoal(ROIS.ptv3.name, at_least, conformity_index, pc90, pc100, priority5)
        ])
        if nr_targets == 4: # Stereotactic, 4 targets
          brain_targets.extend([
            CG.ClinicalGoal(ROIS.ptv4.name, at_least, dose_at_volume, pc100, pc99, priority1),
            CG.ClinicalGoal(ROIS.ptv4.name, at_least, conformity_index, pc90, pc100, priority5)
        ])
  else: # Whole brain or partial brain
    brain_targets = [
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98, priority4),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc95, pc95, priority5)
    ]
  return brain_targets


# Breast:
def breast_targets(ss, region_code, target):
  breast_targets = []
  if region_code in RC.breast_reg_codes:
    # Regional breast:
    if SSF.has_roi_with_shape(ss, ROIS.ctv_p.name):
      # Hypofractionated regional breast:
      breast_targets += [
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc95, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, dose_at_volume, pc90, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_pc.name, at_least, dose_at_volume, pc90, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_nc.name, at_least, dose_at_volume, pc90, pc98, priority3),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc96, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, dose_at_volume, pc95, pc98, priority4),
        CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, conformity_index, pc75, pc95, priority5)
      ]
    elif SSF.has_roi_with_shape(ss, ROIS.ctv_50.name):
      # Conventionally fractionated regional breast (SIB):
      breast_targets += [
        CG.ClinicalGoal(ROIS.ctv_50.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_50.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_47.name, at_least, dose_at_volume, pc93_53, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_47.name, at_most, dose_at_volume, pc94_47, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_47.name, at_least, dose_at_volume, pc89_3, pc98,  priority2),
        CG.ClinicalGoal(ROIS.ctv_50.name, at_least, dose_at_volume, pc95, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_47c.name, at_least, dose_at_volume, pc84_6, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_50c.name, at_least, dose_at_volume, pc90, pc98,  priority2),
        CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
        CG.ClinicalGoal(ROIS.ctv_47.name, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ctv_50.name, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_47c.name, at_most, dose_at_volume, pc98_7, pc5, priority5),
        CG.ClinicalGoal(ROIS.ptv_50c.name, at_least, conformity_index, pc70, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, conformity_index, pc65, pc90, priority5),
        CG.ClinicalGoal(ROIS.ctv_47.name, at_least, dose_at_volume, pc90_24, pc98, priority6),
        CG.ClinicalGoal(ROIS.ctv_50.name, at_least, dose_at_volume, pc96, pc98, priority6),
        CG.ClinicalGoal(ROIS.ptv_47c.name, at_least, dose_at_volume, pc89_3, pc98, priority6),
        CG.ClinicalGoal(ROIS.ptv_50c.name, at_least, dose_at_volume, pc95, pc98, priority6)
      ]
  else:
    # Non-regional breast (whole or partial breast):
    breast_targets += [
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(target, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc95, pc98, priority2),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(target, at_least, homogeneity_index, pc95, pc95, priority5),
      CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, conformity_index, pc75, pc95, priority5)
    ]
    if target == ROIS.ctv_sb.name:
      # Partial breast:
      breast_targets += [
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, dose_at_volume, pc95, pc98, priority2),
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, conformity_index, pc75, pc95, priority5)
      ]
    else:
      # Whole breast:
      breast_targets += [
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, dose_at_volume, pc90, pc98, priority2),
        CG.ClinicalGoal(target, at_least, dose_at_volume, pc96, pc98, priority5),
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, dose_at_volume, pc95, pc98, priority5)
      ]
  if SSF.has_roi_with_shape(ss, ROIS.ctv_sb.name) and region_code not in RC.breast_partial_codes:
    # Tumour bed boost:
    breast_targets += [
      CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, dose_at_volume, 15.92*100, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_sb.name, at_most, dose_at_volume, 16.08*100, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, dose_at_volume, 15.2*100, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv_sbc.name, at_least, dose_at_volume, 15.2*100,  pc95, priority2),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc147, cc2, priority4),
      CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, homogeneity_index, pc95, pc95, priority5),
      CG.ClinicalGoal(ROIS.ptv_sbc.name, at_least, conformity_index, pc75, pc95*16*100, priority5)
    ]
  return breast_targets


# Lung SBRT:
def lung_stereotactic_targets(ss):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  targets = [
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc140, cc2, priority4),
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc150, cc0, priority4)
  ]
  if nr_targets == 1:
    targets.extend([
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc100, pc99, priority1),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc88, pc100, priority5),
      CG.ClinicalGoal(ROIS.igtv.name, at_most, dose_at_abs_volume, pc150, cc0, priority5)
    ])
  else:
    for i in range(0, nr_targets):
      targets.extend([
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, dose_at_volume, pc100, pc99, priority1),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, conformity_index, pc88, pc100, priority5),
        CG.ClinicalGoal(ROIS.igtv.name+str(i+1), at_most, dose_at_abs_volume, pc150, cc0, priority5)
      ])
  return targets


# Lung:
def lung_targets(ss):
  lung = [
    CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc90, pc98, priority2),
    CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc93, pc98, priority5),
    CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5),
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority5)
  ]
  # Some variation in clinical goals whether GTV, CTV or IGTV is defined:
  if SSF.has_roi_with_shape(ss, ROIS.igtv.name):
    lung.extend([
      CG.ClinicalGoal(ROIS.ictv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ictv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.igtv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ictv.name, at_least, dose_at_volume, pc95, pc98, priority2),
      CG.ClinicalGoal(ROIS.ictv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ictv.name, at_least, dose_at_volume, pc98, pc98, priority5)
    ])
  elif SSF.has_roi_with_shape(ss, ROIS.ctv.name):
    lung.extend([
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc95, pc98, priority2),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority5)
    ])
    if SSF.has_roi_with_shape(ss, ROIS.gtv.name):
      lung.extend([
        CG.ClinicalGoal(ROIS.gtv.name, at_least, dose_at_volume, pc98, pc98, priority2)
      ])
  return lung


# Bone/Spine SBRT:
bone_stereotactic_targets = [
  CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc100, pc99, priority1),
  CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc100, priority5),
  CG.ClinicalGoal(ROIS.gtv.name, at_most, dose_at_abs_volume, pc150, cc0, priority5)
]


# Prostate:
def prostate_targets(ss, total_dose):
  prostate = [CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4)]
  if total_dose == 77: # Normo-fractionation
    prostate.extend([
      CG.ClinicalGoal(ROIS.ctv_77.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_77.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_70_sib.name, at_least, dose_at_volume, pc90_45, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_70_sib.name, at_most, dose_at_volume, pc91_36, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_77.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ctv_70_sib.name, at_least, dose_at_volume, pc89_1, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv_77.name, at_least, dose_at_volume, pc95, pc98,  priority4),
      CG.ClinicalGoal(ROIS.ptv_70_sib.name, at_least, dose_at_volume, pc86_36, pc98, priority4),
      CG.ClinicalGoal(ROIS.ctv_77.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ctv_70_sib.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv_77.name, at_least, conformity_index, pc90, pc95, priority5),
      CG.ClinicalGoal(ROIS.ptv_70_sib.name, at_most, dose_at_volume, pc95, pc10, priority5),
      CG.ClinicalGoal(ROIS.ptv_70_77.name, at_least, conformity_index, pc75, pc86_36, priority5)
    ])
    if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name): # With lymph node volume
      prostate.extend([
        CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc72_36, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_56.name, at_most, dose_at_volume, pc73_09, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc71_3, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_56.name, at_least, dose_at_volume, pc69_1, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_56_70_77.name, at_least, conformity_index, pc78, pc69_1, priority5),
        CG.ClinicalGoal(ROIS.ptv_56.name, at_most, dose_at_volume, pc76_36, pc10, priority5),
        CG.ClinicalGoal(ROIS.ctv_56.name, at_least, homogeneity_index, pc95, pc95, priority5)
      ])
  elif total_dose == 60: # Hypofractionation
    prostate.extend([
      CG.ClinicalGoal(ROIS.ctv_60.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_60.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_57.name, at_least, dose_at_volume, pc94_52, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_57.name, at_most, dose_at_volume, pc95_47, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_60.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ctv_57.name, at_least, dose_at_volume, pc93_1, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv_60.name, at_least, dose_at_volume, pc95, pc98,  priority4),
      CG.ClinicalGoal(ROIS.ptv_57.name, at_least, dose_at_volume, pc90_25, pc98, priority4),
      CG.ClinicalGoal(ROIS.ctv_60.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ctv_57.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv_60.name, at_least, conformity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv_57.name, at_most, dose_at_volume, pc99_75, pc2, priority5),
      CG.ClinicalGoal(ROIS.ptv_57_60.name, at_least, conformity_index, pc80, pc90_25, priority5)
    ])
  else: # Hypofractionation
    prostate.extend([
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98,  priority4),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5)
    ])
  return prostate


# Prostate bed:
def prostate_bed_targets(ss):
  prostate_bed = [
    CG.ClinicalGoal(ROIS.ctv_70.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
    CG.ClinicalGoal(ROIS.ctv_70.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
    CG.ClinicalGoal(ROIS.ctv_70.name, at_least, dose_at_volume, pc98, pc98, priority2),
    CG.ClinicalGoal(ROIS.ptv_70.name, at_least, dose_at_volume, pc95, pc98, priority4),
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
    CG.ClinicalGoal(ROIS.ctv_70.name, at_least, homogeneity_index, pc95, pc95, priority5),
    CG.ClinicalGoal(ROIS.ptv_70.name, at_least, conformity_index, pc90, pc95, priority5)    
  ]
  if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name): # With lymph node volume
    prostate_bed.extend([
      CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc79_6, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_56.name, at_most, dose_at_volume, pc80_4, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc78_4, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv_56.name, at_least, dose_at_volume, pc76, pc98, priority4),
      CG.ClinicalGoal(ROIS.ptv_56.name, at_most, dose_at_volume,  pc84, pc5, priority5),
      CG.ClinicalGoal(ROIS.ptv_56_70.name, at_least, conformity_index, pc70, pc76, priority5)
    ])
  return prostate_bed


# Rectum:
def rectum_targets(total_dose):
  if total_dose == 50:
    rectum_targets = [
      CG.ClinicalGoal(ROIS.ctv_50.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_50.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_47.name, at_least, dose_at_volume, pc93_53, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_47.name, at_most, dose_at_volume, pc94_47, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_50.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ctv_47.name, at_least, dose_at_volume, pc92_12, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv_50.name, at_least, dose_at_volume, pc95, pc98,  priority4),
      CG.ClinicalGoal(ROIS.ptv_47.name, at_least, dose_at_volume, pc89_3, pc98, priority4),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(ROIS.ctv_50.name, at_least, homogeneity_index, pc95, pc95, priority5),
      CG.ClinicalGoal(ROIS.ctv_47.name, at_least, homogeneity_index, pc95, pc95, priority5),
      CG.ClinicalGoal(ROIS.ptv_47_50.name, at_least, conformity_index, pc90, pc89_3, priority5),
      CG.ClinicalGoal(ROIS.ptv_50.name, at_least, conformity_index, pc86, pc95, priority5),
      CG.ClinicalGoal(ROIS.ptv_47.name, at_most, dose_at_volume, pc98_7, pc2, priority5),
    ]
  else:
    rectum_targets = [
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98, priority4),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5)
    ]
  return rectum_targets
