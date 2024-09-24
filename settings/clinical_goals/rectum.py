# encoding: utf8

# A class with clinical goal settings for Rectum.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import clinical_goal as CG
import rois as ROIS
import tolerance_doses as TOL


class Rectum:

  # Creates a Rectum clinical goals instance.
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
    oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_volume, TOL.spinalcanal_v2_adx, 0.02, 2))
    oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195.0, TOL.bowel_bag_v195cc, 2))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.41, TOL.bladder_v41pc_freq, 3))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_l.name, CG.at_most, CG.average_dose, TOL.femoral_head_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_r.name, CG.at_most, CG.average_dose, TOL.femoral_head_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_l.name, CG.at_most, CG.dose_at_volume, TOL.femoral_d02pc, 0.02, 6))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_r.name, CG.at_most, CG.dose_at_volume, TOL.femoral_d02pc, 0.02, 6))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    if prescription.total_dose == 50:
      # SIB 47 & 50 Gy in 25 fractions:
      targets.append(CG.ClinicalGoal(ROIS.ctv_50.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_50.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_47.name, CG.at_least, CG.dose_at_volume, 0.9353, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_47.name, CG.at_most, CG.dose_at_volume, 0.9447, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_50.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ctv_47.name, CG.at_least, CG.dose_at_volume, 0.9212, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv_50.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
      targets.append(CG.ClinicalGoal(ROIS.ptv_47.name, CG.at_least, CG.dose_at_volume, 0.893, 0.98, 4))
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
      targets.append(CG.ClinicalGoal(ROIS.ctv_50.name, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
      targets.append(CG.ClinicalGoal(ROIS.ctv_47.name, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv_47_50.name, CG.at_least, CG.conformity_index, 0.9, 0.893, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv_50.name, CG.at_least, CG.conformity_index, 0.86, 0.95, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv_47.name, CG.at_most, CG.dose_at_volume, 0.98_7, 0.02, 5))
    else:
      # 25 Gy in 5 fractions:
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
    return targets
  