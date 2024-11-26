# encoding: utf8

# A class with clinical goal settings for Breast.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import clinical_goal as CG
import region_codes as RC
import rois as ROIS
import tolerance_doses as TOL
import structure_set_functions as SSF


class Breast:

  # Creates a Breast clinical goals instance.
  def __init__(self, ss, plan, prescription):
    # Database attributes:
    self.ss = ss
    self.plan = plan
    self.prescription = prescription
    self.targets = self.create_target_clinical_goals(ss, plan, prescription)
    self.oars = self.create_oar_clinical_goals(ss, plan, prescription)


  # Create OAR clinical goals.
  def create_oar_clinical_goals(self, ss, plan, prescription):
    oars = []
    # Common for all breast variants:
    oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.average_dose, TOL.heart_mean_breast, None, 3))
    oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.volume_at_dose, 0.30, TOL.lung_v30, 6))
    oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.volume_at_dose, 0.45, TOL.lung_v45, 6))
    oars.append(CG.ClinicalGoal(ROIS.a_lad.name, CG.at_most, CG.dose_at_abs_volume, TOL.lad_max, 0.03, 6))
    oars.append(CG.ClinicalGoal(ROIS.a_lad.name, CG.at_most, CG.average_dose, TOL.lad_mean, None, 6))
    oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.average_dose, TOL.heart_mean_breast_low_priority, None, 6))
    if prescription.region_code in RC.breast_l_codes:
      # Left side:
      oars.append(CG.ClinicalGoal(ROIS.breast_r.name, CG.at_most, CG.average_dose, TOL.contralat_breast_mean, None, 5))
      oars.append(CG.ClinicalGoal(ROIS.breast_r.name, CG.at_most, CG.average_dose, TOL.contralat_breast_mean_young_patients, None, 7))
      oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.average_dose, TOL.contralateral_lung_mean, None, 7))
    elif prescription.region_code in RC.breast_r_codes:
      # Right side:
      oars.append(CG.ClinicalGoal(ROIS.breast_l.name, CG.at_most, CG.average_dose, TOL.contralat_breast_mean, None, 5))
      oars.append(CG.ClinicalGoal(ROIS.breast_l.name, CG.at_most, CG.average_dose, TOL.contralat_breast_mean_young_patients, None, 7))
      oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.average_dose, TOL.contralateral_lung_mean, None, 7))
    if prescription.nr_fractions == 5:
      # Tolerances specific for FastForward (5 fractions):
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.05, TOL.heart_v7_fastforward, 6))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.3, TOL.heart_v1_5_fastforward, 6))
      if prescription.region_code in RC.breast_l_codes:
        # Left side:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v8_fastforward, 5))
      else:
        # Right side:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v8_fastforward, 5))
    if prescription.region_code in RC.breast_reg_codes:
      # Common for regional left & right:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinalcanal_breast, 0.03, 2))
      oars.append(CG.ClinicalGoal(ROIS.thyroid.name, CG.at_most, CG.average_dose, TOL.thyroid_mean, None, 4))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.average_dose, TOL.esophagus_mean_brt, None, 5))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.esophagus_v15_adx_brt, 5))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.volume_at_dose, 0.3, TOL.esophagus_v30_adx_brt, 5))
      oars.append(CG.ClinicalGoal(ROIS.thyroid.name, CG.at_most, CG.average_dose, TOL.thyroid_mean_brt, None, 5))
      # Thyroid absolute volume CG for regional breast:
      if SSF.has_named_roi_with_contours(ss, ROIS.thyroid.name):
        volume = ss.RoiGeometries[ROIS.thyroid.name].GetRoiVolume()
        if volume > 8.5:
          oars.append(CG.ClinicalGoal(ROIS.thyroid.name, CG.at_most, CG.abs_volume_at_dose, volume-8.5, TOL.thyroid_v8_5cc_adx_brt, 5))
      if prescription.region_code in RC.breast_reg_l_codes:
        # Left side:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.volume_at_dose, 0.35, TOL.lung_v35_adx_15, 4))
        oars.append(CG.ClinicalGoal(ROIS.humeral_l.name, CG.at_most, CG.volume_at_dose, 0.33, TOL.humeral_v33_adx, 6))
      elif prescription.region_code in RC.breast_reg_r_codes:
        # Right side:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.volume_at_dose, 0.35, TOL.lung_v35_adx_15, 4))
        oars.append(CG.ClinicalGoal(ROIS.humeral_r.name, CG.at_most, CG.volume_at_dose, 0.33, TOL.humeral_v33_adx, 6))
    else:
      # Non-regional breast:
      if prescription.region_code in RC.breast_l_codes:
        # Common for whole breast & partial breast, left:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v15_adx, 4))
      elif prescription.region_code in RC.breast_r_codes:
        # Common for whole breast & partial breast, right:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v15_adx, 4))
      if prescription.region_code in RC.breast_partial_l_codes:
        # Specific for partial breast left:
        oars.append(CG.ClinicalGoal(ROIS.breast_l.name, CG.at_most, CG.abs_volume_at_dose, 426, TOL.ipsilateral_breast_426cc, 5))
        oars.append(CG.ClinicalGoal(ROIS.breast_l.name, CG.at_most, CG.abs_volume_at_dose, 177, TOL.ipsilateral_breast_177cc, 6))
      elif prescription.region_code in RC.breast_partial_r_codes:
        # Specific for partial breast right:
        oars.append(CG.ClinicalGoal(ROIS.breast_r.name, CG.at_most, CG.abs_volume_at_dose, 426, TOL.ipsilateral_breast_426cc, 5))
        oars.append(CG.ClinicalGoal(ROIS.breast_r.name, CG.at_most, CG.abs_volume_at_dose, 177, TOL.ipsilateral_breast_177cc, 6))
    # SIB (Import HIGH protocol):
    if prescription.total_dose == 48:
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.10, TOL.heart_v13gy_import_high, 3))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.02, TOL.heart_v13gy_import_high, 7))
      if prescription.region_code in RC.breast_l_codes:
        # Ipisilateral:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.average_dose, TOL.lung_mean_import_high, None, 7))
        # Contralateral:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v2_5gy_import_high, 5))
      else:
        # Ipisilateral:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.average_dose, TOL.lung_mean_import_high, None, 7))
        # Contralateral:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v2_5gy_import_high, 5))
    # Bilateral: Add relevant goals for each "ipsilateral" lung:
    if prescription.region_code in RC.breast_bilateral_codes:
      # Left:
      if SSF.has_roi_with_shape(ss, 'PTVnc_L'):
        # Regional:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.volume_at_dose, 0.35, TOL.lung_v35_adx_15, 4))
      else:
        oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v15_adx, 4))
      # Right:
      if SSF.has_roi_with_shape(ss, 'PTVnc_R'):
        # Regional:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.volume_at_dose, 0.35, TOL.lung_v35_adx_15, 4))
      else:
        oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_v15_adx, 4))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
    # Set a modifier to use with nominal target dose for SIB/no-SIB:
    mod = 1.0
    if prescription.total_dose == 48:
      mod = 0.834375
      homogeneity_target = ROIS.ctv_ptv_sbc.name
      prescription_target = ROIS.ctv_ptv_sbc.name
      if prescription.region_code in RC.breast_reg_codes:
        conformity_target = ROIS.ptv.name
      else:
        conformity_target = ROIS.ptv_c.name
    else:
      homogeneity_target = prescription.target
      prescription_target = prescription.target
      conformity_target = prescription.target
    if prescription.region_code in RC.breast_reg_codes:
      # Regional breast:
      if prescription.region_code in RC.breast_bilateral_codes:
        # Bilateral regional:
        targets.append(CG.ClinicalGoal(prescription_target, CG.at_least, CG.dose_at_volume, 0.995*mod, 0.50, 1))
        targets.append(CG.ClinicalGoal(prescription_target, CG.at_most, CG.dose_at_volume, 1.005*mod, 0.50, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_L', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_R', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name, CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_L', CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_R', CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name, CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name + '_L', CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name + '_R', CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_L', CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_R', CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_L', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_R', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name + '_L', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name + '_R', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(homogeneity_target, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name, CG.at_least, CG.conformity_index, 0.75, 0.95*mod, 5))
      else:
        # Single-sided regional:
        targets.append(CG.ClinicalGoal(prescription_target, CG.at_least, CG.dose_at_volume, 0.995*mod, 0.50, 1))
        targets.append(CG.ClinicalGoal(prescription_target, CG.at_most, CG.dose_at_volume, 1.005*mod, 0.50, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv_p.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv_n.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name, CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name, CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_nc.name, CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_pc.name, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 4))
        targets.append(CG.ClinicalGoal(homogeneity_target, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name, CG.at_least, CG.conformity_index, 0.75, 0.95*mod, 5))
    else:
      # Non-regional breast (whole or partial breast):
      targets.append(CG.ClinicalGoal(prescription_target, CG.at_least, CG.dose_at_volume, 0.995*mod, 0.50, 1))
      targets.append(CG.ClinicalGoal(prescription_target, CG.at_most, CG.dose_at_volume, 1.005*mod, 0.50, 1))
      targets.append(CG.ClinicalGoal(prescription.target, CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
      targets.append(CG.ClinicalGoal(homogeneity_target, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
      targets.append(CG.ClinicalGoal(conformity_target, CG.at_least, CG.conformity_index, 0.75, 0.95*mod, 5))
      if prescription.target == ROIS.ctv_sb.name:
        # Partial breast:
        targets.append(CG.ClinicalGoal(prescription.target.replace("C", "P")+"c", CG.at_least, CG.dose_at_volume, 0.95, 0.98, 2))
      else:
        # Whole breast:
        targets.append(CG.ClinicalGoal(prescription.target.replace("C", "P")+"c", CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(prescription.target, CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 5))
        targets.append(CG.ClinicalGoal(prescription.target.replace("C", "P")+"c", CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 5))
      if prescription.region_code in RC.breast_bilateral_codes:
        # Bilateral whole breast:
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_L', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_R', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_L', CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_R', CG.at_least, CG.dose_at_volume, 0.9*mod, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_L', CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name + '_R', CG.at_least, CG.dose_at_volume, 0.96*mod, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_L', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_c.name + '_R', CG.at_least, CG.dose_at_volume, 0.95*mod, 0.98, 5))
    if SSF.has_roi_with_shape(ss, ROIS.ctv_sb.name) and prescription.region_code not in RC.breast_partial_codes:
      # SIB boost (40.05 & 48 Gy in 15 fx):
      targets.append(CG.ClinicalGoal(ROIS.ctv_sb.name, CG.at_least, CG.dose_at_volume, 48*0.995*100, 0.50, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_sb.name, CG.at_most, CG.dose_at_volume, 48*1.005*100, 0.50, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_sb.name, CG.at_least, CG.dose_at_volume, 48*0.95*100, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv_sbc.name, CG.at_least, CG.dose_at_volume, 48*0.95*100,  0.95, 2))
      targets.append(CG.ClinicalGoal(ROIS.ctv_sb.name, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv_sbc.name, CG.at_least, CG.conformity_index, 0.75, 0.95*48*100, 5))
    # Breast tolerance speficic for 18 fx SIB (Skagen trial):
    # (For regional use CTVp-CTVsb, for whole breast use CTV-CTVsb)
    if SSF.has_roi_with_shape(ss, ROIS.ctv_p_ctv_sb.name):
      targets.append(CG.ClinicalGoal(ROIS.ctv_p_ctv_sb.name, CG.at_most, CG.volume_at_dose, 0.40, 43.46*100, 5))
    elif SSF.has_roi_with_shape(ss, ROIS.ctv_ctv_sb.name):
      targets.append(CG.ClinicalGoal(ROIS.ctv_ctv_sb.name, CG.at_most, CG.volume_at_dose, 0.40, 43.46*100, 5))
    return targets
  