# encoding: utf8

# A class with clinical goal settings for Bladder.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import clinical_goal as CG
import rois as ROIS
import tolerance_doses as TOL


class Bladder:

  # Creates a Bladder clinical goals instance.
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
    oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195.0, TOL.bowel_bag_v195cc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.22, TOL.rectum_v22pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.38, TOL.rectum_v38pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.51, TOL.rectum_v51pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.64, TOL.rectum_v64pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.80, TOL.rectum_v80pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.anal_canal.name, CG.at_most, CG.average_dose, TOL.anal_canal_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.femoral_head_l.name, CG.at_most, CG.average_dose, TOL.femoral_head_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.femoral_head_r.name, CG.at_most, CG.average_dose, TOL.femoral_head_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.01, TOL.rectum_v01pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.18, TOL.rectum_v18pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.31, TOL.rectum_v31pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.44, TOL.rectum_v44pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.60, TOL.rectum_v60pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.femoral_head_l.name, CG.at_most, CG.dose_at_volume, TOL.femoral_d02pc, 0.02, 6))
    oars.append(CG.ClinicalGoal(ROIS.femoral_head_r.name, CG.at_most, CG.dose_at_volume, TOL.femoral_d02pc, 0.02, 6))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
    targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
    targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
    targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
    targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
    targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
    targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
    return targets
  