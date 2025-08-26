# encoding: utf8

# A class with clinical goal settings for Prostate.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import clinical_goal as CG
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF
import tolerance_doses as TOL


class Prostate:

  # Creates a Prostate clinical goals instance.
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
    # Higher priority:
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.22, TOL.rectum_v22pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.38, TOL.rectum_v38pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.51, TOL.rectum_v51pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.64, TOL.rectum_v64pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.80, TOL.rectum_v80pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.01, TOL.bladder_v01pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.20, TOL.bladder_v20pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.05, TOL.bladder_v05pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.41, TOL.bladder_v41pc, 3))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.02, TOL.bladder_v02pc, 3))
    # Medium priority:
    oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195, TOL.bowel_bag_v195cc, 4))
    oars.append(CG.ClinicalGoal(ROIS.anal_canal.name, CG.at_most, CG.average_dose, TOL.anal_canal_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_l.name, CG.at_most, CG.average_dose, TOL.femoral_head_mean, None, 4))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_r.name, CG.at_most, CG.average_dose, TOL.femoral_head_mean, None, 4))
    # Lower priority:
    oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.dose_at_abs_volume, TOL.bowel_bag_dmax, 0.03, 6))
    oars.append(CG.ClinicalGoal(ROIS.penile_bulb.name, CG.at_most, CG.average_dose, TOL.penile_bulb_mean, None, 6))
    oars.append(CG.ClinicalGoal(ROIS.penile_bulb.name, CG.at_most, CG.dose_at_volume, TOL.penile_bulb_d02pc, 0.02, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.01, TOL.rectum_v01pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.18, TOL.rectum_v18pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.31, TOL.rectum_v31pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.44, TOL.rectum_v44pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.60, TOL.rectum_v60pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.19, TOL.bladder_v19pc, 6))
    oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.41, TOL.bladder_v41pc_freq, 6))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_l.name, CG.at_most, CG.dose_at_volume, TOL.femoral_d02pc, 0.02, 6))
    oars.append(CG.ClinicalGoal(ROIS.femur_head_neck_r.name, CG.at_most, CG.dose_at_volume, TOL.femoral_d02pc, 0.02, 6))
    oars.append(CG.ClinicalGoal(ROIS.bone.name, CG.at_most, CG.abs_volume_at_dose, 1000, TOL.bone_v1000cc, 6))
    oars.append(CG.ClinicalGoal(ROIS.bone.name, CG.at_most, CG.abs_volume_at_dose, 1520, TOL.bone_v1520cc, 6))
    oars.append(CG.ClinicalGoal(ROIS.bone.name, CG.at_most, CG.abs_volume_at_dose, 1250, TOL.bone_v1250cc, 6))
    oars.append(CG.ClinicalGoal(ROIS.bone.name, CG.at_most, CG.abs_volume_at_dose, 850, TOL.bone_v850cc, 6))
    if prescription.region_code in RC.prostate_node_codes:
      # Lymph node irradiation:
      oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_volume, TOL.spinalcanal_v2_adx, 0.02, 2))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
    if prescription.region_code in RC.prostate_intact_codes:
      # Intact prostate:
      if prescription.total_dose == 67.5:
        # Hypofractionated high risk prostate:
        targets.append(CG.ClinicalGoal('CTV_67.5', CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
        targets.append(CG.ClinicalGoal('CTV_67.5', CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
        targets.append(CG.ClinicalGoal('CTV!_62.5', CG.at_least, CG.dose_at_volume, 0.921296, 0.5, 1))
        targets.append(CG.ClinicalGoal('CTV!_62.5', CG.at_most, CG.dose_at_volume, 0.930555, 0.5, 1))
        targets.append(CG.ClinicalGoal('CTV_67.5', CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
        targets.append(CG.ClinicalGoal('CTV!_62.5', CG.at_least, CG.dose_at_volume, 0.907407, 0.98, 2))
        targets.append(CG.ClinicalGoal('PTV_67.5', CG.at_least, CG.dose_at_volume, 0.95, 0.98,  4))
        targets.append(CG.ClinicalGoal('PTV!_62.5', CG.at_least, CG.dose_at_volume, 0.879630, 0.98, 4))
        targets.append(CG.ClinicalGoal('CTV_67.5', CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal('CTV!_62.5', CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal('PTV_67.5', CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
        targets.append(CG.ClinicalGoal('PTV!_62.5', CG.at_most, CG.dose_at_volume, 0.95, 0.1, 5))
        targets.append(CG.ClinicalGoal('PTV_62.5+67.5', CG.at_least, CG.conformity_index, 0.75, 0.879630, 5))
        if prescription.region_code in RC.prostate_node_codes:
          # With lymph nodes:
          targets.append(CG.ClinicalGoal('CTV!_50', CG.at_least, CG.dose_at_volume, 0.737037, 0.5, 1))
          targets.append(CG.ClinicalGoal('CTV!_50', CG.at_most, CG.dose_at_volume, 0.744444, 0.5, 1))
          targets.append(CG.ClinicalGoal('CTV!_50', CG.at_least, CG.dose_at_volume, 0.726, 0.98, 2))
          targets.append(CG.ClinicalGoal('PTV!_50', CG.at_least, CG.dose_at_volume, 0.703704, 0.98, 4))
          targets.append(CG.ClinicalGoal('PTV_50+62.5+67.5', CG.at_least, CG.conformity_index, 0.78, 0.703704, 5))
          targets.append(CG.ClinicalGoal('PTV!_50', CG.at_most, CG.dose_at_volume, 0.777778, 0.1, 5))
          targets.append(CG.ClinicalGoal('CTV!_50', CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
          # Plan includes positive nodes to be treated with 60 Gy?
          if SSF.has_roi(ss, ROIS.ptv__60.name):
            targets.append(CG.ClinicalGoal('CTV!_60', CG.at_least, CG.dose_at_volume, 0.884444, 0.5, 1))
            targets.append(CG.ClinicalGoal('CTV!_60', CG.at_most, CG.dose_at_volume, 0.893333, 0.5, 1))
            targets.append(CG.ClinicalGoal('CTV!_60', CG.at_least, CG.dose_at_volume, 0.871111, 0.98, 2))
            targets.append(CG.ClinicalGoal('PTV!_60', CG.at_least, CG.dose_at_volume, 0.844444, 0.98, 4))
            targets.append(CG.ClinicalGoal('CTV!_60', CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
            targets.append(CG.ClinicalGoal('PTV!_60', CG.at_most, CG.dose_at_volume, 0.933333, 0.1, 5))
      elif prescription.total_dose == 60:
        # Hypofractionated localized prostate:
        targets.append(CG.ClinicalGoal(ROIS.ctv_60.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv_60.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv_57.name, CG.at_least, CG.dose_at_volume, 0.9452, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv_57.name, CG.at_most, CG.dose_at_volume, 0.9547, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv_60.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv_57.name, CG.at_least, CG.dose_at_volume, 0.931, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_60.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98,  4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_57.name, CG.at_least, CG.dose_at_volume, 0.9025, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ctv_60.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ctv_57.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_60.name, CG.at_least, CG.conformity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_57.name, CG.at_most, CG.dose_at_volume, 0.9975, 0.02, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_57_60.name, CG.at_least, CG.conformity_index, 0.8, 0.9025, 5))
      else:
        # Palliative prostate:
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98,  4))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
    else:
      # Prostate bed:
      targets.append(CG.ClinicalGoal(ROIS.ctv_70.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_70.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv_70.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv_70.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
      targets.append(CG.ClinicalGoal(ROIS.ctv_70.name, CG.at_least, CG.homogeneity_index, 0.95, 0.95, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv_70.name, CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
      if prescription.region_code in RC.prostate_node_codes:
        # With lymph nodes:
        targets.append(CG.ClinicalGoal(ROIS.ctv_56.name, CG.at_least, CG.dose_at_volume, 0.796, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv_56.name, CG.at_most, CG.dose_at_volume, 0.804, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv_56.name, CG.at_least, CG.dose_at_volume, 0.784, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ptv_56.name, CG.at_least, CG.dose_at_volume, 0.76, 0.98, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv_56.name, CG.at_most, CG.dose_at_volume,  0.84, 0.05, 5))
        targets.append(CG.ClinicalGoal(ROIS.ptv_56_70.name, CG.at_least, CG.conformity_index, 0.7, 0.76, 5))
    return targets
  