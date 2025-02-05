# encoding: utf8

# A class with clinical goal settings for OtherSBRT treatments.
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


class OtherSBRT:

  # Creates a OtherSBRT clinical goals instance.
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
    if prescription.nr_fractions == 1:
      # Common for all single fx bone SBRT:
      oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_1fx_v10, 10, 4))
      oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_1fx_v0, 0.035, 4))
      if prescription.region_code in RC.stereotactic_spine_thorax_codes:
        # Spine thorax:
        oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0_35, 0.35, 2))
        oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0, 0.027, 2))
        oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0_1, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_1fx_v4, 4, 2))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_1fx_v0, 0, 2))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_1fx_v15, 15, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_1fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.dose_at_abs_volume, TOL.lungs_sbrt_1fx_v1000, 1000, 3))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_1fx_v5, 5, 3))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_1fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.kidney_l.name, CG.at_most, CG.dose_at_volume, TOL.kidney_hilum_1fx_v66, 0.66, 3))
        oars.append(CG.ClinicalGoal(ROIS.kidney_r.name, CG.at_most, CG.dose_at_volume, TOL.kidney_hilum_1fx_v66, 0.66, 3))
        oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.dose_at_abs_volume, TOL.kidneys_col_1fx_v200, 200, 3))
      elif prescription.region_code in RC.stereotactic_spine_pelvis_codes or prescription.region_code in RC.stereotactic_pelvis_codes:
        # Common for pelvis spine/non-spine:
        oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_abs_volume, TOL.cauda_equina_sbrt_1fx_v0, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_abs_volume, TOL.cauda_equina_sbrt_1fx_v0, 5, 2))
        oars.append(CG.ClinicalGoal(ROIS.small_bowel.name, CG.at_most, CG.dose_at_abs_volume, TOL.small_bowel_sbrt_1fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.small_bowel.name, CG.at_most, CG.dose_at_abs_volume, TOL.small_bowel_sbrt_1fx_v5, 5, 3))
        oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.dose_at_abs_volume, TOL.rectum_sbrt_1fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.dose_at_abs_volume, TOL.rectum_sbrt_1fx_v20, 20, 3))
        oars.append(CG.ClinicalGoal(ROIS.colon.name, CG.at_most, CG.dose_at_abs_volume, TOL.colon_sbrt_1fx_v0, 0, 3))
        oars.append(CG.ClinicalGoal(ROIS.colon.name, CG.at_most, CG.dose_at_abs_volume, TOL.colon_sbrt_1fx_v20, 20, 3))
        oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.dose_at_abs_volume, TOL.bladder_1fx_v003, 0.03, 3))
        oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.dose_at_abs_volume, TOL.bladder_1fx_v15, 15, 3))
        if prescription.region_code in RC.stereotactic_spine_pelvis_codes:
          # Spine pelvis:
          oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0_35, 0.35, 2))
          oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_1fx_v0, 0, 2))
          oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0_1, 0.1, 2))
          oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_3mm_sbrt_1fx_v0, 0, 2))
          oars.append(CG.ClinicalGoal(ROIS.kidney_l.name, CG.at_most, CG.dose_at_volume, TOL.kidney_hilum_1fx_v66, 0.66, 3))
          oars.append(CG.ClinicalGoal(ROIS.kidney_r.name, CG.at_most, CG.dose_at_volume, TOL.kidney_hilum_1fx_v66, 0.66, 3))
          oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.dose_at_abs_volume, TOL.kidneys_col_1fx_v200, 200, 3))
    else:
      # Common for all 3 fx bone SBRT:
      oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_col_sbrt_3fx_v10, 10, 4))
      oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_col_sbrt_3fx_v0, 0.035, 4))
      if prescription.region_code in RC.stereotactic_spine_thorax_codes:
        # Spine thorax:
        oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0_35, 0.35, 2))
        oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0, 0.027, 2))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_3fx, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_3fx_v15, 15, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_3fx_v0_035, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.dose_at_abs_volume, TOL.lungs_sbrt_3fx_v1000, 1000, 3))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v5, 5, 3))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_3fx_v0_035, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.kidney_l.name, CG.at_most, CG.dose_at_volume, TOL.kidney_3fx_v10, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.kidney_r.name, CG.at_most, CG.dose_at_volume, TOL.kidney_3fx_v10, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.dose_at_abs_volume, TOL.kidneys_col_3fx_v200, 200, 3))
      elif prescription.region_code in RC.stereotactic_spine_pelvis_codes or prescription.region_code in RC.stereotactic_pelvis_codes:
        # Common for pelvis spine/non-spine:
        oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_abs_volume, TOL.cauda_equina_sbrt_3fx_v0, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_abs_volume, TOL.cauda_equina_sbrt_3fx_v5, 5, 2))
        oars.append(CG.ClinicalGoal(ROIS.small_bowel.name, CG.at_most, CG.dose_at_abs_volume, TOL.small_bowel_sbrt_3fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.small_bowel.name, CG.at_most, CG.dose_at_abs_volume, TOL.small_bowel_sbrt_3fx_v5, 5, 3))
        oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.dose_at_abs_volume, TOL.rectum_sbrt_3fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.dose_at_abs_volume, TOL.rectum_sbrt_3fx_v20, 20, 3))
        oars.append(CG.ClinicalGoal(ROIS.colon.name, CG.at_most, CG.dose_at_abs_volume, TOL.colon_sbrt_3fx_v0, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.colon.name, CG.at_most, CG.dose_at_abs_volume, TOL.colon_sbrt_3fx_v20, 20, 3))
        oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.dose_at_abs_volume, TOL.bladder_3fx_v003, 0.03, 3))
        oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.dose_at_abs_volume, TOL.bladder_3fx_v15, 15, 3))
        if prescription.region_code in RC.stereotactic_spine_pelvis_codes:
          # Spine pelvis:
          oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0_35, 0.35, 2))
          oars.append(CG.ClinicalGoal(ROIS.spinal_cord.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx_v0, 0.027, 2))
          oars.append(CG.ClinicalGoal(ROIS.kidney_l.name, CG.at_most, CG.dose_at_volume, TOL.kidney_3fx_v10, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.kidney_r.name, CG.at_most, CG.dose_at_volume, TOL.kidney_3fx_v10, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.dose_at_abs_volume, TOL.kidneys_col_3fx_v200, 200, 3))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 1.0, 0.99, 1))
    targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.4, 2.0, 4))
    targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_most, CG.dose_at_volume, 1.4, 0.02, 4))
    targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.9, 1.0, 5))
    return targets
  