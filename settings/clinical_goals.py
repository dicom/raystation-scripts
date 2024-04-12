# encoding: utf8

# Import local files:
import clinical_goal as CG
import rois as ROIS
import tolerance_doses as TOL
import roi_functions as ROIF
import structure_set_functions as SSF
import region_codes as RC
import tolerance as EQD


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

# Brain (whole brain/partial brain/brain SRT):
def brain_oars(prescription, region_code):
  brain_oars = []
  if region_code in RC.brain_whole_codes:
    # Whole brain:
    brain_oars += [
      CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, average_dose, TOL.cochlea_mean_tinnitus, None, priority3),
      CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, average_dose, TOL.cochlea_mean_tinnitus, None, priority3),
      CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0_03, priority3),
      CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_v003_adx, cc0_03, priority3),
      CG.ClinicalGoal(ROIS.lacrimal_l.name, at_most, average_dose, TOL.lacrimal_mean, None, priority3),
      CG.ClinicalGoal(ROIS.lacrimal_r.name, at_most, average_dose, TOL.lacrimal_mean, None, priority3),
      CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_v003_adx, cc0_03, priority6)
		]
  elif region_code in RC.brain_partial_codes:
    # Partial brain (SBRT & conventional):
    brain_oars += [
      CG.ClinicalGoal(ROIS.hippocampus_l.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5),
      CG.ClinicalGoal(ROIS.hippocampus_r.name, at_most, average_dose, TOL.hippocampus_v40, None, priority5)
    ]
    if prescription.nr_fractions == 1:
      # Stereotactic, 1 fraction:
      brain_oars += [
        CG.ClinicalGoal(ROIS.brain.name, at_most, abs_volume_at_dose, 15, TOL.brain_srt_1fx, priority2),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_1fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_1fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_1fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_1fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, average_dose, TOL.cochlea_srt_1fx, None, priority3),
        CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, average_dose, TOL.cochlea_srt_1fx, None, priority3),
        CG.ClinicalGoal(ROIS.eye_r.name, at_most, dose_at_abs_volume, TOL.eye_srt_1fx, 0.1, priority3),
        CG.ClinicalGoal(ROIS.eye_l.name, at_most, dose_at_abs_volume, TOL.eye_srt_1fx, 0.1, priority3),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_srt_1fx_v10, 10, priority4),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_srt_1fx_v0_1, 0.1, priority4),
        CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_srt_1fx, 0.1, priority4),
        CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_srt_1fx, 0.1, priority4),
        CG.ClinicalGoal(ROIS.brain.name, at_most, abs_volume_at_dose, 10, TOL.brain_srt_1fx, priority4),
        CG.ClinicalGoal(ROIS.brain.name, at_most, abs_volume_at_dose, 5, TOL.brain_srt_1fx, priority6)
      ]
    elif prescription.nr_fractions == 3:
      # Stereotactic, 3 fractions:
      brain_oars += [
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_3fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_3fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p1, 0.035, priority2),
        CG.ClinicalGoal(ROIS.brain.name, at_most, abs_volume_at_dose, 30, TOL.brain_srt_3fx, priority3),
        CG.ClinicalGoal(ROIS.brainstem.name, at_most, dose_at_abs_volume, TOL.brainstem_srt_3fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.optic_chiasm.name, at_most, dose_at_abs_volume, TOL.optic_chiasm_srt_3fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_l.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.optic_nrv_r.name, at_most, dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p2, 0.035, priority3),
        CG.ClinicalGoal(ROIS.cochlea_l.name, at_most, average_dose, TOL.cochlea_srt_3fx, None, priority3),
        CG.ClinicalGoal(ROIS.cochlea_r.name, at_most, average_dose, TOL.cochlea_srt_3fx, None, priority3),
        CG.ClinicalGoal(ROIS.eye_r.name, at_most, dose_at_abs_volume, TOL.eye_srt_3fx, 0.1, priority3),
        CG.ClinicalGoal(ROIS.eye_l.name, at_most, dose_at_abs_volume, TOL.eye_srt_3fx, 0.1, priority3),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_srt_3fx_v0_1, 0.1, priority3),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_srt_3fx_v10, 10, priority3),
        CG.ClinicalGoal(ROIS.lens_r.name, at_most, dose_at_abs_volume, TOL.lens_srt_3fx, 0.1, priority4),
        CG.ClinicalGoal(ROIS.lens_l.name, at_most, dose_at_abs_volume, TOL.lens_srt_3fx, 0.1, priority4),
        CG.ClinicalGoal(ROIS.brain.name, at_most, abs_volume_at_dose, 20, TOL.brain_srt_3fx, priority4)
      ]
    else:
      # Partial brain:
      brain_oars += [ 
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
        CG.ClinicalGoal(ROIS.brain.name, at_most, dose_at_abs_volume, TOL.brain_v003, cc3, priority5),
        CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_v003_adx, cc0_03, priority6)
      ]
  return brain_oars


# Breast (Regional breast/Whole breast/Partial breast):
def breast_oars(ss, region_code, prescription):
  # Common for all breast variants:
  breast_oars = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinalcanal_breast, cc0_03, priority2),
    CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean_breast, None, priority3),
    CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, 0.30, TOL.lung_v30, priority6),
    CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, 0.45, TOL.lung_v45, priority6),
    CG.ClinicalGoal(ROIS.a_lad.name, at_most, dose_at_abs_volume, TOL.lad_max, cc0_03, priority6),
    CG.ClinicalGoal(ROIS.a_lad.name, at_most, average_dose, TOL.lad_mean, None, priority6),
    CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean_breast_low_priority, None, priority6)
  ]
  if region_code in RC.breast_l_codes:
    breast_oars += [
      CG.ClinicalGoal(ROIS.breast_r.name, at_most, average_dose, TOL.contralat_breast_mean, None, priority5),
      CG.ClinicalGoal(ROIS.breast_r.name, at_most, average_dose, TOL.contralat_breast_mean_young_patients, None, priority7),
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.contralateral_lung_mean, None, priority7)
    ]
  elif region_code in RC.breast_r_codes:
    breast_oars += [
      CG.ClinicalGoal(ROIS.breast_l.name, at_most, average_dose, TOL.contralat_breast_mean, None, priority5),
      CG.ClinicalGoal(ROIS.breast_l.name, at_most, average_dose, TOL.contralat_breast_mean_young_patients, None, priority7),
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.contralateral_lung_mean, None, priority7)
    ]
  if prescription.nr_fractions == 5:
    # Tolerances specific for FastForward (5 fractions):
    breast_oars += [
      CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.05, TOL.heart_v7_fastforward, priority6),
      CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.3, TOL.heart_v1_5_fastforward, priority6)
    ]
    if region_code in RC.breast_l_codes:
      breast_oars += [
        CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, 0.15, TOL.lung_v8_fastforward, priority6),
      ]
    else:
      breast_oars += [
        CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, 0.15, TOL.lung_v8_fastforward, priority6),
      ]
  if region_code in RC.breast_reg_codes:
    # Common for regional left & right:
    breast_oars += [
      CG.ClinicalGoal(ROIS.thyroid.name, at_most, average_dose, TOL.thyroid_mean, None, priority4),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, average_dose, TOL.esophagus_mean_brt, None, priority5),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, volume_at_dose, pc15, TOL.esophagus_v15_adx_brt, priority5),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, volume_at_dose, pc30, TOL.esophagus_v30_adx_brt, priority5),
      CG.ClinicalGoal(ROIS.thyroid.name, at_most, average_dose, TOL.thyroid_mean_brt, None, priority5)
    ]
    # Thyroid absolute volume CG for regional breast:
    if SSF.has_named_roi_with_contours(ss, ROIS.thyroid.name):
      volume = ss.RoiGeometries[ROIS.thyroid.name].GetRoiVolume()
      if volume > 8.5:
        breast_oars.append(CG.ClinicalGoal(ROIS.thyroid.name, at_most, abs_volume_at_dose, volume-8.5, TOL.thyroid_v8_5cc_adx_brt, priority5))
    if region_code in RC.breast_reg_l_codes:
      # Specific for regional left:
      breast_oars += [
        CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx_15, priority4),
        CG.ClinicalGoal(ROIS.humeral_l.name, at_most, volume_at_dose, pc33, TOL.humeral_v33_adx, priority6)
      ]
    else:
      # Specific for regional right:
      breast_oars += [
        CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx_15, priority4),
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
      breast_oars += [CG.ClinicalGoal(ROIS.breast_l.name, at_most, abs_volume_at_dose, 426, TOL.ipsilateral_breast_426cc, priority5)]
      breast_oars += [CG.ClinicalGoal(ROIS.breast_l.name, at_most, abs_volume_at_dose, 177, TOL.ipsilateral_breast_177cc, priority6)]
    elif region_code in RC.breast_partial_r_codes:
      # Specific for partial breast right:
      breast_oars += [CG.ClinicalGoal(ROIS.breast_r.name, at_most, abs_volume_at_dose, 426, TOL.ipsilateral_breast_426cc, priority5)]
      breast_oars += [CG.ClinicalGoal(ROIS.breast_r.name, at_most, abs_volume_at_dose, 177, TOL.ipsilateral_breast_177cc, priority6)]
  # SIB (Import HIGH protocol):
  if prescription.total_dose == 48:
    breast_oars += [CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.10, TOL.heart_v13gy_import_high, priority3)]
    breast_oars += [CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.02, TOL.heart_v13gy_import_high, priority7)]
    if region_code in RC.breast_l_codes:
      # Ipisilateral:
      breast_oars += [CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_mean_import_high, None, priority7)]
      # Contralateral:
      breast_oars += [CG.ClinicalGoal(ROIS.lung_r.name, at_most, volume_at_dose, 0.15, TOL.lung_v2_5gy_import_high, priority5)]
    else:
      # Ipisilateral:
      breast_oars += [CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_mean_import_high, None, priority7)]
      # Contralateral:
      breast_oars += [CG.ClinicalGoal(ROIS.lung_l.name, at_most, volume_at_dose, 0.15, TOL.lung_v2_5gy_import_high, priority5)]
  return breast_oars


# Lung (conventional):
# (In cases where a GTV/IGTV is present, clinical goals are created for 'Lungs-GTV'/'Lungs-IGTV' instead of 'Lungs')
def lung_oars(ss, prescription):
  # Create a tolerance equal to the prescription dose:
  prescription_dose = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', 3, prescription.nr_fractions, prescription.total_dose, 'Max', 'Conventional RT')
  lung_oars = []
  # Determine which variant to use for the general lungs CG:
  if SSF.has_roi_with_shape(ss, ROIS.lungs_gtv.name):
    lungs = ROIS.lungs_gtv.name
  elif SSF.has_roi_with_shape(ss, ROIS.lungs_igtv.name):
    lungs = ROIS.lungs_igtv.name
  else:
    lungs = ROIS.lungs.name
  # Once daily or bi-daily fractionation?
  if prescription.nr_fractions == 40 and prescription.total_dose == 60:
    # Bi-daily 40 fx:
    tol_spinalcanal = TOL.spinalcanal_bid_40fx
    tol_heart_mean = TOL.heart_mean_bid_40fx
    tol_heart_v25 = TOL.heart_v25_bid_40fx
    tol_lung_mean = TOL.lung_mean_bid_40fx
    tol_lung_v35 = TOL.lung_v35_bid_40fx
    tol_esophagus_mean = TOL.esophagus_mean_bid_40fx
    tol_esophagus_v17 = TOL.esophagus_v17_bid_40fx
    tol_spinalcanal_chemo = TOL.spinalcanal_chemo_bid_40fx
  elif prescription.nr_fractions == 30 and prescription.total_dose == 45:
    # Bi-daily 30 fx:
    tol_spinalcanal = TOL.spinalcanal_bid_30fx
    tol_heart_mean = TOL.heart_mean_bid_30fx
    tol_heart_v25 = TOL.heart_v25_bid_30fx
    tol_lung_mean = TOL.lung_mean_bid_30fx
    tol_lung_v35 = TOL.lung_v35_bid_30fx
    tol_esophagus_mean = TOL.esophagus_mean_bid_30fx
    tol_esophagus_v17 = TOL.esophagus_v17_bid_30fx
    tol_spinalcanal_chemo = TOL.spinalcanal_chemo_bid_30fx
  else:
    # Ordinary (once daily) fractionations:
    tol_spinalcanal = TOL.spinalcanal_v2_adx
    tol_heart_mean = TOL.heart_mean
    tol_heart_v25 = TOL.heart_v25_adx
    tol_lung_mean = TOL.lung_mean
    tol_lung_v35 = TOL.lung_v35_adx
    tol_esophagus_mean = TOL.esophagus_mean
    tol_esophagus_v17 = TOL.esophagus_v17_adx
    tol_spinalcanal_chemo = TOL.spinalcanal_chemo_v2_adx
  # Create clinical goals:
  lung_oars += [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, tol_spinalcanal, 0.03, priority2),
    CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, tol_heart_mean, None, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, pc25, tol_heart_v25, priority3),
    CG.ClinicalGoal(ROIS.a_lad.name, at_most, volume_at_dose, 0.10, TOL.lad_v10, priority3),
    CG.ClinicalGoal(lungs, at_most, average_dose, tol_lung_mean, None, priority3),
    CG.ClinicalGoal(lungs, at_most, volume_at_dose, pc35, tol_lung_v35, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, average_dose, tol_esophagus_mean, None, priority3),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, volume_at_dose, pc17, tol_esophagus_v17, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.1, TOL.heart_v10, priority4),
    CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.355, TOL.heart_v355, priority4),
    CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_lymphopenia_mean, None, priority6),
    CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.38, TOL.heart_lymphopenia_v38, priority6),
    CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.25, TOL.heart_lymphopenia_v25, priority6),
    CG.ClinicalGoal(ROIS.a_lad.name, at_most, volume_at_dose, 0.01, TOL.lad_v01, priority6),
    CG.ClinicalGoal(lungs, at_most, average_dose, TOL.lung_lymphopenia_mean, None, priority6),
    CG.ClinicalGoal(lungs, at_most, volume_at_dose, 0.30, TOL.lung_lymphopenia_v30, priority6),
    CG.ClinicalGoal(lungs, at_most, volume_at_dose, 0.45, TOL.lung_lymphopenia_v45, priority6),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, prescription_dose, 0.03, priority6),
    CG.ClinicalGoal(ROIS.spleen.name, at_most, average_dose, TOL.spleen_lymphopenia_mean, None, priority6),
    CG.ClinicalGoal(ROIS.spleen.name, at_most, volume_at_dose, 0.17, TOL.spleen_lymphopenia_v17, priority6),
    CG.ClinicalGoal(ROIS.spleen.name, at_most, volume_at_dose, 0.16, TOL.spleen_lymphopenia_v16, priority6),
    CG.ClinicalGoal(ROIS.spleen.name, at_most, volume_at_dose, 0.09, TOL.spleen_lymphopenia_v09, priority6),
    CG.ClinicalGoal(ROIS.spleen.name, at_most, volume_at_dose, 0.05, TOL.spleen_lymphopenia_v05, priority6),
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, tol_spinalcanal_chemo, 0.03, priority6)
  ]
  return lung_oars


# Lung SBRT (3 fx):
def lung_stereotactic_3fx_oars(region_code):
  lung_oars = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx, 0.035, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_3fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_3fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, average_dose, TOL.lung_sbrt_mean, None, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc15, TOL.lung_sbrt_v_15pc, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_secondary, 0.1, priority6),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, dose_at_abs_volume, TOL.chestwall_sbrt_3fx_v01, 0.1, priority6),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, abs_volume_at_dose, cc30, TOL.chestwall_sbrt_3fx_v30, priority6),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_3fx_cc01, cc0_1, priority6),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_3fx_cc10, cc10, priority6),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc10, TOL.lung_sbrt_v_10pc, priority6),
    CG.ClinicalGoal(ROIS.stomach.name, at_most, abs_volume_at_dose, cc0_1, TOL.stomach_sbrt_3fx_cc01, priority6)
  ]
  if region_code in [248, 250]:
    # Right:
    lung_oars += [
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_sbrt_contralat_mean, None, priority6),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx, cc0, priority6)
    ]
  elif region_code in [247, 249]:
    # Left:
    lung_oars += [
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_sbrt_contralat_mean, None, priority6),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx, cc0, priority6)
    ]
  else:
    # Include OARs for both sides:
    lung_oars += [
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx, cc0, priority6),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_3fx, cc0, priority6)
    ]
  return lung_oars


# Lung SBRT (5 fx):
def lung_stereotactic_5fx_oars(region_code):
  lung_oars = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_5fx, 0.035, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_5fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_5fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_5fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_5fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, average_dose, TOL.lung_sbrt_mean, None, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc15, TOL.lung_sbrt_v_15pc, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_5fx_secondary, 0.1, priority6),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, dose_at_abs_volume, TOL.chestwall_sbrt_5fx_v01, 0.1, priority6),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, abs_volume_at_dose, cc30, TOL.chestwall_sbrt_5fx_v30, priority6),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_5fx_cc01, cc0_1, priority6),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_5fx_cc10, cc10, priority6),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc10, TOL.lung_sbrt_v_10pc, priority6),
    CG.ClinicalGoal(ROIS.stomach.name, at_most, abs_volume_at_dose, cc0_1, TOL.stomach_sbrt_5fx_cc01, priority6)
  ]
  if region_code in [248, 250]:
    # Right:
    lung_oars += [
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_sbrt_contralat_mean, None, priority6),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx, cc0, priority6)
    ]
  elif region_code in [247, 249]:
    # Left:
    lung_oars += [
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_sbrt_contralat_mean, None, priority6),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx, cc0, priority6)
    ]
  else:
    # Include OARs for both sides:
    lung_oars += [
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx, cc0, priority6),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_5fx, cc0, priority6)
    ]
  return lung_oars


# Lung SBRT (8 fx):
def lung_stereotactic_8fx_oars(region_code):
  lung_oars = [
    CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_8fx, 0.035, priority2),
    CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_8fx, 0.1, priority2),
    CG.ClinicalGoal(ROIS.main_bronchus_r.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx, 0.01, priority2),
    CG.ClinicalGoal(ROIS.main_bronchus_l.name, at_most, dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx, 0.01, priority2),
    CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_8fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.greatves.name, at_most, dose_at_abs_volume, TOL.greatves_sbrt_8fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_8fx, 0.1, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, average_dose, TOL.lung_sbrt_mean, None, priority3),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc15, TOL.lung_sbrt_v_15pc, priority3),
    CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_8fx_secondary, 0.1, priority6),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, dose_at_abs_volume, TOL.chestwall_sbrt_8fx_v01, 0.1, priority6),
    CG.ClinicalGoal(ROIS.chestwall.name, at_most, abs_volume_at_dose, cc30, TOL.chestwall_sbrt_8fx_v30, priority6),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_8fx_cc01, cc0_1, priority6),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_8fx_cc10, cc10, priority6),
    CG.ClinicalGoal(ROIS.lungs_igtv.name, at_most, volume_at_dose, pc10, TOL.lung_sbrt_v_10pc, priority6),
    CG.ClinicalGoal(ROIS.stomach.name, at_most, abs_volume_at_dose, cc0_1, TOL.stomach_sbrt_8fx_cc01, priority6)
  ]
  if region_code in [248, 250]:
    # Right:
    lung_oars += [
      CG.ClinicalGoal(ROIS.lung_l.name, at_most, average_dose, TOL.lung_sbrt_contralat_mean, None, priority6),
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_8fx, cc0, priority6)
    ]
  elif region_code in [247, 249]:
    # Left:
    lung_oars += [
      CG.ClinicalGoal(ROIS.lung_r.name, at_most, average_dose, TOL.lung_sbrt_contralat_mean, None, priority6),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_8fx, cc0, priority6)
    ]
  else:
    # Include OARs for both sides:
    lung_oars += [
      CG.ClinicalGoal(ROIS.ribs_r.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_8fx, cc0, priority6),
      CG.ClinicalGoal(ROIS.ribs_l.name, at_most, dose_at_abs_volume, TOL.ribs_sbrt_8fx, cc0, priority6)
    ]
  return lung_oars


# Rectum:
rectum_oars = [
  CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_volume, TOL.spinalcanal_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowel_bag_v195cc, priority2),
  CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.41, TOL.bladder_v41pc_freq, priority3),
  CG.ClinicalGoal(ROIS.femur_head_neck_l.name, at_most, average_dose, TOL.femoral_head_mean, None, priority4),
  CG.ClinicalGoal(ROIS.femur_head_neck_r.name, at_most, average_dose, TOL.femoral_head_mean, None, priority4),
  CG.ClinicalGoal(ROIS.femur_head_neck_l.name, at_most, dose_at_volume, TOL.femoral_d02pc, 0.02, priority6),
  CG.ClinicalGoal(ROIS.femur_head_neck_r.name, at_most, dose_at_volume, TOL.femoral_d02pc, 0.02, priority6)
]


# Bladder:
bladder_oars = [
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowel_bag_v195cc, priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.22, TOL.rectum_v22pc,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.38, TOL.rectum_v38pc,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.51, TOL.rectum_v51pc,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.64, TOL.rectum_v64pc,  priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.80, TOL.rectum_v80pc,  priority3),
  CG.ClinicalGoal(ROIS.anal_canal.name, at_most, average_dose, TOL.anal_canal_mean, None, priority4),
  CG.ClinicalGoal(ROIS.femur_head_neck_l.name, at_most, average_dose, TOL.femoral_head_mean, None, priority4),
  CG.ClinicalGoal(ROIS.femur_head_neck_r.name, at_most, average_dose, TOL.femoral_head_mean, None, priority4),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.01, TOL.rectum_v01pc,  priority6),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.18, TOL.rectum_v18pc,  priority6),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.31, TOL.rectum_v31pc,  priority6),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.44, TOL.rectum_v44pc,  priority6),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.60, TOL.rectum_v60pc,  priority6),
  CG.ClinicalGoal(ROIS.femur_head_neck_l.name, at_most, dose_at_volume, TOL.femoral_d02pc, 0.02, priority6),
  CG.ClinicalGoal(ROIS.femur_head_neck_r.name, at_most, dose_at_volume, TOL.femoral_d02pc, 0.02, priority6)
]


# Prostate (palliative fx, 20 fx, 25 fx & 35 fx):
def prostate_oars(ss, region_code, prescription):
  prostate_oars = [
    # Higher priority:
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.22, TOL.rectum_v22pc,  priority3),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.38, TOL.rectum_v38pc,  priority3),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.51, TOL.rectum_v51pc,  priority3),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.64, TOL.rectum_v64pc,  priority3),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.80, TOL.rectum_v80pc,  priority3),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.01, TOL.bladder_v01pc,  priority3),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.20, TOL.bladder_v20pc,  priority3),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.05, TOL.bladder_v05pc,  priority3),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.41, TOL.bladder_v41pc,  priority3),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.02, TOL.bladder_v02pc,  priority3),
    # Medium priority:
    CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, 195, TOL.bowel_bag_v195cc, priority4),
    CG.ClinicalGoal(ROIS.anal_canal.name, at_most, average_dose, TOL.anal_canal_mean, None, priority4),
    CG.ClinicalGoal(ROIS.femur_head_neck_l.name, at_most, average_dose, TOL.femoral_head_mean, None, priority4),
    CG.ClinicalGoal(ROIS.femur_head_neck_r.name, at_most, average_dose, TOL.femoral_head_mean, None, priority4),
    # Lower priority:
    CG.ClinicalGoal(ROIS.penile_bulb.name, at_most, average_dose, TOL.penile_bulb_mean, None, priority6),
    CG.ClinicalGoal(ROIS.penile_bulb.name, at_most, dose_at_volume, TOL.penile_bulb_d02pc, 0.02, priority6),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.01, TOL.rectum_v01pc,  priority6),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.18, TOL.rectum_v18pc,  priority6),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.31, TOL.rectum_v31pc,  priority6),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.44, TOL.rectum_v44pc,  priority6),
    CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.60, TOL.rectum_v60pc,  priority6),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.19, TOL.bladder_v19pc,  priority6),
    CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, 0.41, TOL.bladder_v41pc_freq,  priority6),
    CG.ClinicalGoal(ROIS.femur_head_neck_l.name, at_most, dose_at_volume, TOL.femoral_d02pc, 0.02, priority6),
    CG.ClinicalGoal(ROIS.femur_head_neck_r.name, at_most, dose_at_volume, TOL.femoral_d02pc, 0.02, priority6),
    CG.ClinicalGoal(ROIS.bone.name, at_most, abs_volume_at_dose, 1000, TOL.bone_v1000cc, priority6)
  ]
  # Lymph node irradiation?
  if region_code in RC.prostate_node_codes:
    # Cauda equina:
    prostate_oars += [
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_volume, TOL.spinalcanal_v2_adx, pc2, priority2)
    ]
  return prostate_oars


# Bone SBRT (1 fx, thoracic/pelvis, spine/non-spine):
def bone_stereotactic_1fx_oars(region_code):
  # Common for all bone SBRT:
  bone_oars = [
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_1fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_sbrt_1fx_v0, cc0, priority4)
  ]
  if region_code in RC.stereotactic_spine_thorax_codes:
    # Spine thorax:
    bone_oars += [
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0_35, cc0_35, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0_1, cc0_1, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_1fx_v4, cc4, priority2),
      CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_1fx_v15, cc15, priority3),
      CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.lungs.name, at_most, dose_at_abs_volume, TOL.lungs_sbrt_1fx_v1000, cc1000, priority3),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_1fx_v5, cc5, priority3),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_hilum_1fx_v66, pc66, priority3),
      CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_hilum_1fx_v66, pc66, priority3),
      CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.kidneys.name, at_most, dose_at_abs_volume, TOL.kidneys_col_1fx_v200, cc200, priority3)
    ]
  elif region_code in RC.stereotactic_spine_pelvis_codes or region_code in RC.stereotactic_pelvis_codes:
    # Common for pelvis spine/non-spine:
    bone_oars += [
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_1fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_1fx_v0, cc5, priority2),
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_1fx_v5, cc5, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_1fx_v20, cc20, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_1fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_1fx_v20, cc20, priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, dose_at_abs_volume, TOL.bladder_1fx_v003, cc0_03, priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, dose_at_abs_volume, TOL.bladder_1fx_v15, cc15, priority3)
    ]
    if region_code in RC.stereotactic_spine_pelvis_codes:
      # Spine pelvis:
      bone_oars += [
        CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0_35, cc0_35, priority2),
        CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0_1, cc0_1, priority2),
        CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_hilum_1fx_v66, pc66, priority3),
        CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_hilum_1fx_v66, pc66, priority3),
        CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_sbrt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_sbrt_1fx_v0, cc0, priority3),
        CG.ClinicalGoal(ROIS.kidneys.name, at_most, dose_at_abs_volume, TOL.kidneys_col_1fx_v200, cc200, priority3)
      ]
  return bone_oars


# Bone SBRT (3 fx, thoracic/pelvis, spine/non-spine):
def bone_stereotactic_3fx_oars(region_code):
  # Common for all bone SBRT:
  bone_oars = [
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_col_sbrt_3fx_v10, cc10, priority4),
    CG.ClinicalGoal(ROIS.skin.name, at_most, dose_at_abs_volume, TOL.skin_col_sbrt_3fx_v0, cc0, priority4),
  ]
  if region_code in RC.stereotactic_spine_thorax_codes:
    # Spine thorax:
    bone_oars += [
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0_35, cc0_35, priority2),
      CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.trachea.name, at_most, dose_at_abs_volume, TOL.trachea_sbrt_3fx, 0.1, priority2),
      CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_v15, cc15, priority3),
      CG.ClinicalGoal(ROIS.heart.name, at_most, dose_at_abs_volume, TOL.heart_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.lungs.name, at_most, dose_at_abs_volume, TOL.lung_sbrt_3fx_v1000, cc1000, priority3),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v5, cc5, priority3),
      CG.ClinicalGoal(ROIS.esophagus.name, at_most, dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_3fx_v10, pc10, priority3),
      CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_3fx_v10, pc10, priority3),
      CG.ClinicalGoal(ROIS.kidneys.name, at_most, dose_at_abs_volume, TOL.kidneys_col_3fx_v200, cc200, priority3)
    ]
  elif region_code in RC.stereotactic_spine_pelvis_codes or region_code in RC.stereotactic_pelvis_codes:
    # Common for pelvis spine/non-spine:
    bone_oars += [
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_3fx_v0, cc0, priority2),
      CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_abs_volume, TOL.cauda_equina_sbrt_3fx_v5, cc5, priority2),
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.small_bowel.name, at_most, dose_at_abs_volume, TOL.small_bowel_sbrt_3fx_v5, cc5, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.rectum.name, at_most, dose_at_abs_volume, TOL.rectum_sbrt_3fx_v20, cc20, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_3fx_v0, cc0, priority3),
      CG.ClinicalGoal(ROIS.colon.name, at_most, dose_at_abs_volume, TOL.colon_sbrt_3fx_v20, cc20, priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, dose_at_abs_volume, TOL.bladder_3fx_v003, cc0_03, priority3),
      CG.ClinicalGoal(ROIS.bladder.name, at_most, dose_at_abs_volume, TOL.bladder_3fx_v15, cc15, priority3)
    ]
    if region_code in RC.stereotactic_spine_pelvis_codes:
      # Spine pelvis:
      bone_oars += [
        CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0_35, cc0_35, priority2),
        CG.ClinicalGoal(ROIS.spinal_cord.name, at_most, dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0, cc0, priority2),
        CG.ClinicalGoal(ROIS.kidney_l.name, at_most, dose_at_volume, TOL.kidney_3fx_v10, pc10, priority3),
        CG.ClinicalGoal(ROIS.kidney_r.name, at_most, dose_at_volume, TOL.kidney_3fx_v10, pc10, priority3),
        CG.ClinicalGoal(ROIS.kidneys.name, at_most, dose_at_abs_volume, TOL.kidneys_col_3fx_v200, cc200, priority3)
      ]
  return bone_oars


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
  CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean_quantec, None, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.46, TOL.heart_v46_quantec, priority3),
  CG.ClinicalGoal(ROIS.esophagus.name, at_most, average_dose, TOL.esophagus_mean, None, priority3),
  CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_mean, None, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, average_dose, TOL.lung_mean, None, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority3)
]
thorax_and_abdomen = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.heart.name, at_most, average_dose, TOL.heart_mean_quantec, None, priority3),
  CG.ClinicalGoal(ROIS.heart.name, at_most, volume_at_dose, 0.46, TOL.heart_v46_quantec, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, average_dose, TOL.lung_mean, None, priority3),
  CG.ClinicalGoal(ROIS.lungs.name, at_most, volume_at_dose, pc35, TOL.lung_v35_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, average_dose, TOL.kidney_mean, None, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc55, TOL.kidney_v55_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc32, TOL.kidney_v32_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc30, TOL.kidney_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc20, TOL.kidney_v20_adx, priority3),
  CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_mean, None, priority3),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowel_bag_v195cc, priority3),
  CG.ClinicalGoal(ROIS.spleen.name, at_most, average_dose, TOL.spleen_mean, None, priority3),
  CG.ClinicalGoal(ROIS.stomach.name, at_most, abs_volume_at_dose, 0, TOL.stomach_min, priority3)
]
abdomen = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, average_dose, TOL.kidney_mean, None, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc55, TOL.kidney_v55_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc32, TOL.kidney_v32_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc30, TOL.kidney_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc20, TOL.kidney_v20_adx, priority3),
  CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_mean, None, priority3),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowel_bag_v195cc, priority3),
  CG.ClinicalGoal(ROIS.spleen.name, at_most, average_dose, TOL.spleen_mean, None, priority3),
  CG.ClinicalGoal(ROIS.stomach.name, at_most, abs_volume_at_dose, 0, TOL.stomach_min, priority3)
]
abdomen_and_pelvis = [
  CG.ClinicalGoal(ROIS.spinal_canal.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, average_dose, TOL.kidney_mean, None, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc55, TOL.kidney_v55_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc32, TOL.kidney_v32_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc30, TOL.kidney_v30_adx, priority3),
  CG.ClinicalGoal(ROIS.kidneys.name, at_most, volume_at_dose, pc20, TOL.kidney_v20_adx, priority3),
  CG.ClinicalGoal(ROIS.liver.name, at_most, average_dose, TOL.liver_mean, None, priority3),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowel_bag_v195cc, priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.51, TOL.rectum_v51pc,  priority3),
  CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v50_quantec, priority4)
]
pelvis = [
  CG.ClinicalGoal(ROIS.cauda_equina.name, at_most, dose_at_volume, TOL.spinalcord_v2_adx, pc2, priority2),
  CG.ClinicalGoal(ROIS.bowel_space.name, at_most, abs_volume_at_dose, cc195, TOL.bowel_bag_v195cc, priority3),
  CG.ClinicalGoal(ROIS.rectum.name, at_most, volume_at_dose, 0.51, TOL.rectum_v51pc,  priority3),
  CG.ClinicalGoal(ROIS.bladder.name, at_most, volume_at_dose, pc50, TOL.bladder_v50_quantec, priority4)
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


# Palliative:
def palliative_targets(ss, plan, target):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  palliative_targets = [CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4)]
  if nr_targets > 1 and len(list(plan.BeamSets)) > 1:
    for i in range(0, nr_targets):
      palliative_targets += [
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_least, dose_at_volume, pc99_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_most, dose_at_volume, pc100_5, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_least, dose_at_volume, pc98, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, dose_at_volume, pc95, pc98, priority4),
        CG.ClinicalGoal(ROIS.ctv.name+str(i+1), at_least, homogeneity_index, pc95, pc98, priority5),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, conformity_index, pc90, pc95, priority5)
      ]
  else:
    palliative_targets += [
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(target, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(target.replace("C", "P"), at_least, dose_at_volume, pc95, pc98, priority4),
      CG.ClinicalGoal(target, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(target.replace("C", "P"), at_least, conformity_index, pc90, pc95, priority5)
    ]
  return palliative_targets


# Brain (whole brain/partial brain/SRT with single or multiple targets):
def brain_targets(ss, prescription):
  brain_targets = []
  if prescription.is_stereotactic():
    # SRT:
    brain_targets += [
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc150, cc2, priority4),
    ]
    nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
    if nr_targets == 1:
      # Single target:
      brain_targets += [
        CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc100, pc99, priority1),
        CG.ClinicalGoal(ROIS.ptv.name, at_most, dose_at_volume, pc150, 0.02, priority4),
        CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc100, priority5)
      ]
    else:
      # Multiple targets:
      for i in range(0, nr_targets):
        brain_targets += [
          CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, dose_at_volume, pc100, pc99, priority1),
          CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_most, dose_at_volume, pc140, 0.02, priority4),
          CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, conformity_index, pc90, pc100, priority5)
        ]
  else:
    # Whole brain or partial brain:
    brain_targets += [
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98, priority4),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc95, pc95, priority5)
    ]
  return brain_targets


# Breast (partial/whole/regional):
def breast_targets(ss, region_code, target, prescription):
  breast_targets = []
  # Set a modifier to use with nominal target dose for SIB/no-SIB:
  mod = 1.0
  if prescription.total_dose == 48:
    mod = 0.834375
    homogeneity_target = ROIS.ctv_ptv_sbc.name
    prescription_target = ROIS.ctv_ptv_sbc.name
  else:
    homogeneity_target = target
    prescription_target = target
  if region_code in RC.breast_reg_codes:
    # Regional breast:
    if region_code in RC.breast_bilateral_codes:
      # Bilateral regional:
      breast_targets += [
        CG.ClinicalGoal(prescription_target, at_least, dose_at_volume, pc99_5*mod, pc50, priority1),
        CG.ClinicalGoal(prescription_target, at_most, dose_at_volume, pc100_5*mod, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc95*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, dose_at_volume, pc90*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_pc.name, at_least, dose_at_volume, pc90*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc96*mod, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, dose_at_volume, pc95*mod, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_pc.name, at_least, dose_at_volume, pc95*mod, pc98, priority4),
        CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
        CG.ClinicalGoal(homogeneity_target, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, conformity_index, pc75, pc95*mod, priority5)
      ]
    else:
      # Single-sided regional:
      breast_targets += [
        CG.ClinicalGoal(prescription_target, at_least, dose_at_volume, pc99_5*mod, pc50, priority1),
        CG.ClinicalGoal(prescription_target, at_most, dose_at_volume, pc100_5*mod, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc95*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ctv_p.name, at_least, dose_at_volume, pc95*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ctv_n.name, at_least, dose_at_volume, pc95*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, dose_at_volume, pc90*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_pc.name, at_least, dose_at_volume, pc90*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_nc.name, at_least, dose_at_volume, pc90*mod, pc98, priority2),
        CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc96*mod, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, dose_at_volume, pc95*mod, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_pc.name, at_least, dose_at_volume, pc95*mod, pc98, priority4),
        CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
        CG.ClinicalGoal(homogeneity_target, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_c.name, at_least, conformity_index, pc75, pc95*mod, priority5)
      ]
  else:
    # Non-regional breast (whole or partial breast):
    breast_targets += [
      CG.ClinicalGoal(prescription_target, at_least, dose_at_volume, pc99_5*mod, pc50, priority1),
      CG.ClinicalGoal(prescription_target, at_most, dose_at_volume, pc100_5*mod, pc50, priority1),
      CG.ClinicalGoal(target, at_least, dose_at_volume, pc95*mod, pc98, priority2),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(homogeneity_target, at_least, homogeneity_index, pc95, pc95, priority5),
      CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, conformity_index, pc75, pc95*mod, priority5)
    ]
    if target == ROIS.ctv_sb.name:
      # Partial breast:
      breast_targets += [
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, dose_at_volume, pc95, pc98, priority2),
      ]
    else:
      # Whole breast:
      breast_targets += [
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, dose_at_volume, pc90*mod, pc98, priority2),
        CG.ClinicalGoal(target, at_least, dose_at_volume, pc96*mod, pc98, priority5),
        CG.ClinicalGoal(target.replace("C", "P")+"c", at_least, dose_at_volume, pc95*mod, pc98, priority5)
      ]
  if SSF.has_roi_with_shape(ss, ROIS.ctv_sb.name) and region_code not in RC.breast_partial_codes:
    if prescription.total_dose == 48:
      # SIB boost (40.05 & 48 Gy in 15 fx):
      breast_targets += [
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, dose_at_volume, 48*0.995*100, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_most, dose_at_volume, 48*1.005*100, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, dose_at_volume, 48*0.95*100, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_sbc.name, at_least, dose_at_volume, 48*0.95*100,  pc95, priority2),
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_sbc.name, at_least, conformity_index, pc75, pc95*48*100, priority5)
      ]
    else:
      # Sequenctial boost (40.05/15 fx & 16 Gy/8 fx):
      breast_targets += [
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, dose_at_volume, 15.92*100, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_most, dose_at_volume, 16.08*100, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, dose_at_volume, 15.2*100, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_sbc.name, at_least, dose_at_volume, 15.2*100,  pc95, priority2),
        CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc147, cc2, priority4),
        CG.ClinicalGoal(ROIS.ctv_sb.name, at_least, homogeneity_index, pc95, pc95, priority5),
        CG.ClinicalGoal(ROIS.ptv_sbc.name, at_least, conformity_index, pc75, pc95*16*100, priority5)
      ]
  # Breast tolerance speficic for 18 fx SIB (Skagen trial):
  # (For regional use CTVp-CTVsb, for whole breast use CTV-CTVsb)
  if SSF.has_roi_with_shape(ss, ROIS.ctv_p_ctv_sb.name):
    breast_targets += [CG.ClinicalGoal(ROIS.ctv_p_ctv_sb.name, at_most, volume_at_dose, 0.40, 43.46*100, priority5)]
  elif SSF.has_roi_with_shape(ss, ROIS.ctv_ctv_sb.name):
    breast_targets += [CG.ClinicalGoal(ROIS.ctv_ctv_sb.name, at_most, volume_at_dose, 0.40, 43.46*100, priority5)]
  return breast_targets


# Lung SBRT (single or multiple targets):
def lung_stereotactic_targets(ss):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  lung_targets = [
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc140, cc2, priority4)
  ]
  if nr_targets == 1:
    lung_targets += [
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc100, 0.98, priority1),
      CG.ClinicalGoal(ROIS.ptv.name, at_most, dose_at_volume, pc140, 0.02, priority4),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc88, pc100, priority5)
    ]
  else:
    for i in range(0, nr_targets):
      lung_targets += [
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, dose_at_volume, pc100, pc99, priority1),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_most, dose_at_volume, pc140, 0.02, priority4),
        CG.ClinicalGoal(ROIS.ptv.name+str(i+1), at_least, conformity_index, pc88, pc100, priority5)
      ]
  return lung_targets


# Lung (conventional):
def lung_targets(ss):
  lung_targets = [
    CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc90, pc98, priority2),
    CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc93, pc98, priority5),
    CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5),
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority5)
  ]
  # Some variation in clinical goals whether GTV, CTV or IGTV is defined:
  if SSF.has_roi_with_shape(ss, ROIS.igtv.name):
    lung_targets += [
      CG.ClinicalGoal(ROIS.ictv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ictv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.igtv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ictv.name, at_least, dose_at_volume, pc95, pc98, priority2),
      CG.ClinicalGoal(ROIS.ictv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ictv.name, at_least, dose_at_volume, pc98, pc98, priority5)
    ]
  elif SSF.has_roi_with_shape(ss, ROIS.ctv.name):
    lung_targets += [
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc95, pc98, priority2),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority5)
    ]
    if SSF.has_roi_with_shape(ss, ROIS.gtv.name):
      lung_targets += [
        CG.ClinicalGoal(ROIS.gtv.name, at_least, dose_at_volume, pc98, pc98, priority2)
      ]
  return lung_targets


# Bone/Spine SBRT:
bone_stereotactic_targets = [
  CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc100, pc99, priority1),
  CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc140, cc2, priority4),
  CG.ClinicalGoal(ROIS.ptv.name, at_most, dose_at_volume, pc140, 0.02, priority4),
  CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc100, priority5)
]


# Prostate (hypofractionated/conventional fractionation, with or without lymph nodes):
def prostate_targets(ss, prescription):
  prostate_targets = [CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4)]
  if prescription.total_dose == 77:
    # Normo-fractionation:
    prostate_targets += [
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
    ]
    if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name):
      # With lymph nodes:
      prostate_targets += [
        CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc72_36, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_56.name, at_most, dose_at_volume, pc73_09, pc50, priority1),
        CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc71_3, pc98, priority2),
        CG.ClinicalGoal(ROIS.ptv_56.name, at_least, dose_at_volume, pc69_1, pc98, priority4),
        CG.ClinicalGoal(ROIS.ptv_56_70_77.name, at_least, conformity_index, pc78, pc69_1, priority5),
        CG.ClinicalGoal(ROIS.ptv_56.name, at_most, dose_at_volume, pc76_36, pc10, priority5),
        CG.ClinicalGoal(ROIS.ctv_56.name, at_least, homogeneity_index, pc95, pc95, priority5)
      ]
  elif prescription.total_dose == 67.5:
    # Hypofractionated high risk prostate:
    prostate_targets += [
      CG.ClinicalGoal('CTV_67.5', at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal('CTV_67.5', at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal('CTV!_62.5', at_least, dose_at_volume, 0.921296, pc50, priority1),
      CG.ClinicalGoal('CTV!_62.5', at_most, dose_at_volume, 0.930555, pc50, priority1),
      CG.ClinicalGoal('CTV_67.5', at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal('CTV!_62.5', at_least, dose_at_volume, 0.907407, pc98, priority2),
      CG.ClinicalGoal('PTV_67.5', at_least, dose_at_volume, pc95, pc98,  priority4),
      CG.ClinicalGoal('PTV!_62.5', at_least, dose_at_volume, 0.879630, pc98, priority4),
      CG.ClinicalGoal('CTV_67.5', at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal('CTV!_62.5', at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal('PTV_67.5', at_least, conformity_index, pc90, pc95, priority5),
      CG.ClinicalGoal('PTV!_62.5', at_most, dose_at_volume, pc95, pc10, priority5),
      CG.ClinicalGoal('PTV_62.5+67.5', at_least, conformity_index, pc75, 0.879630, priority5)
    ]
    if SSF.has_roi_with_shape(ss, ROIS.ptv__50.name):
      # With lymph nodes:
      prostate_targets += [
        CG.ClinicalGoal('CTV!_50', at_least, dose_at_volume, 0.737037, pc50, priority1),
        CG.ClinicalGoal('CTV!_50', at_most, dose_at_volume, 0.744444, pc50, priority1),
        CG.ClinicalGoal('CTV!_50', at_least, dose_at_volume, 0.726, pc98, priority2),
        CG.ClinicalGoal('PTV!_50', at_least, dose_at_volume, 0.703704, pc98, priority4),
        CG.ClinicalGoal('PTV_50+62.5+67.5', at_least, conformity_index, pc78, 0.703704, priority5),
        CG.ClinicalGoal('PTV!_50', at_most, dose_at_volume, 0.777778, pc10, priority5),
        CG.ClinicalGoal('CTV!_50', at_least, homogeneity_index, pc95, pc95, priority5)
      ]
  elif prescription.total_dose == 60:
    # Hypofractionation:
    prostate_targets += [
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
    ]
  else:
    # Palliative:
    prostate_targets += [
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98,  priority4),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5)
    ]
  return prostate_targets


# Prostate bed (with or without lymph nodes):
def prostate_bed_targets(ss):
  prostate_bed_targets = [
    CG.ClinicalGoal(ROIS.ctv_70.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
    CG.ClinicalGoal(ROIS.ctv_70.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
    CG.ClinicalGoal(ROIS.ctv_70.name, at_least, dose_at_volume, pc98, pc98, priority2),
    CG.ClinicalGoal(ROIS.ptv_70.name, at_least, dose_at_volume, pc95, pc98, priority4),
    CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
    CG.ClinicalGoal(ROIS.ctv_70.name, at_least, homogeneity_index, pc95, pc95, priority5),
    CG.ClinicalGoal(ROIS.ptv_70.name, at_least, conformity_index, pc90, pc95, priority5)    
  ]
  if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name):
    # With lymph nodes:
    prostate_bed_targets += [
      CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc79_6, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_56.name, at_most, dose_at_volume, pc80_4, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv_56.name, at_least, dose_at_volume, pc78_4, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv_56.name, at_least, dose_at_volume, pc76, pc98, priority4),
      CG.ClinicalGoal(ROIS.ptv_56.name, at_most, dose_at_volume,  pc84, pc5, priority5),
      CG.ClinicalGoal(ROIS.ptv_56_70.name, at_least, conformity_index, pc70, pc76, priority5)
    ]
  return prostate_bed_targets


# Rectum (hypofractionated or conventional fractionation):
def rectum_targets(prescription):
  rectum_targets = []
  if prescription.total_dose == 50:
    rectum_targets += [
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
    rectum_targets += [
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc99_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_most, dose_at_volume, pc100_5, pc50, priority1),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, dose_at_volume, pc98, pc98, priority2),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, dose_at_volume, pc95, pc98, priority4),
      CG.ClinicalGoal(ROIS.external.name, at_most, dose_at_abs_volume, pc105, cc2, priority4),
      CG.ClinicalGoal(ROIS.ctv.name, at_least, homogeneity_index, pc95, pc98, priority5),
      CG.ClinicalGoal(ROIS.ptv.name, at_least, conformity_index, pc90, pc95, priority5)
    ]
  return rectum_targets
