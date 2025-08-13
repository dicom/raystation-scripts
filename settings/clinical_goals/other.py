# encoding: utf8

# A class with clinical goal settings for Other (palliative) treatments.
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


class Other:

  # Creates a Other clinical goals instance.
  def __init__(self, ss, plan, prescription, target_nr = None):
    # Database attributes:
    self.ss = ss
    self.plan = plan
    self.prescription = prescription
    self.target_nr = target_nr
    self.targets = self.create_target_clinical_goals(ss, plan, prescription, target_nr)
    self.oars = self.create_oar_clinical_goals(ss, plan, prescription)


  # Create OAR clinical goals.
  def create_oar_clinical_goals(self, ss, plan, prescription):
    oars = []
    if prescription.region_code in RC.palliative_head_codes:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.dose_at_abs_volume, TOL.brain_v003, 0, 3))
      oars.append(CG.ClinicalGoal(ROIS.lens_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_v003_adx, 0, 4))
      oars.append(CG.ClinicalGoal(ROIS.lens_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_v003_adx, 0, 4))
    elif prescription.region_code in RC.palliative_neck_codes:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.parotids.name, CG.at_most, CG.average_dose, TOL.parotids_mean, None, 3))
    elif prescription.region_code in RC.palliative_thorax_codes:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.average_dose, TOL.heart_mean_quantec, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.46, TOL.heart_v46_quantec, 3))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.average_dose, TOL.esophagus_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.liver.name, CG.at_most, CG.average_dose, TOL.liver_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.average_dose, TOL.lung_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.volume_at_dose, 0.35, TOL.lung_v35_adx, 3))
    elif prescription.region_code in RC.palliative_thorax_and_abdomen_codes:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.average_dose, TOL.heart_mean_quantec, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.46, TOL.heart_v46_quantec, 3))
      oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.average_dose, TOL.lung_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.lungs.name, CG.at_most, CG.volume_at_dose, 0.35, TOL.lung_v35_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.average_dose, TOL.kidney_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.55, TOL.kidney_v55_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.32, TOL.kidney_v32_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.3, TOL.kidney_v30_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.2, TOL.kidney_v20_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.liver.name, CG.at_most, CG.average_dose, TOL.liver_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195.0, TOL.bowel_bag_v195cc, 3))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.average_dose, TOL.spleen_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.stomach.name, CG.at_most, CG.abs_volume_at_dose, 0, TOL.stomach_min, 3))
    elif prescription.region_code in RC.palliative_abdomen_codes:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.average_dose, TOL.kidney_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.55, TOL.kidney_v55_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.32, TOL.kidney_v32_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.3, TOL.kidney_v30_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.2, TOL.kidney_v20_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.liver.name, CG.at_most, CG.average_dose, TOL.liver_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195.0, TOL.bowel_bag_v195cc, 3))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.average_dose, TOL.spleen_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.stomach.name, CG.at_most, CG.abs_volume_at_dose, 0, TOL.stomach_min, 3))
    elif prescription.region_code in RC.palliative_abdomen_and_pelvis_codes:
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.average_dose, TOL.kidney_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.55, TOL.kidney_v55_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.32, TOL.kidney_v32_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.3, TOL.kidney_v30_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.kidneys.name, CG.at_most, CG.volume_at_dose, 0.2, TOL.kidney_v20_adx, 3))
      oars.append(CG.ClinicalGoal(ROIS.liver.name, CG.at_most, CG.average_dose, TOL.liver_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195.0, TOL.bowel_bag_v195cc, 3))
      oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.51, TOL.rectum_v51pc,  3))
      oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.5, TOL.bladder_v50_quantec, 4))
    elif prescription.region_code in RC.palliative_pelvis_codes:
      oars.append(CG.ClinicalGoal(ROIS.cauda_equina.name, CG.at_most, CG.dose_at_volume, TOL.spinalcord_v2_adx, 0.02, 2))
      oars.append(CG.ClinicalGoal(ROIS.bowel_space.name, CG.at_most, CG.abs_volume_at_dose, 195.0, TOL.bowel_bag_v195cc, 3))
      oars.append(CG.ClinicalGoal(ROIS.rectum.name, CG.at_most, CG.volume_at_dose, 0.51, TOL.rectum_v51pc,  3))
      oars.append(CG.ClinicalGoal(ROIS.bladder.name, CG.at_most, CG.volume_at_dose, 0.5, TOL.bladder_v50_quantec, 4))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription, target_nr):
    targets = []
    nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
    if target_nr:
      targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(target_nr), CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(target_nr), CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(target_nr), CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(target_nr), CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(target_nr), CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(target_nr), CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
    else:
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
      if nr_targets > 1 and len(list(plan.BeamSets)) > 1:
        for i in range(0, nr_targets):
          targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(i+1), CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
          targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(i+1), CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
          targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(i+1), CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
          targets.append(CG.ClinicalGoal(ROIS.ctv.name+str(i+1), CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
      else:
        ptv = self.ptv(ss, prescription.target)
        targets.append(CG.ClinicalGoal(prescription.target, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
        targets.append(CG.ClinicalGoal(prescription.target, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
        targets.append(CG.ClinicalGoal(prescription.target, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
        targets.append(CG.ClinicalGoal(ptv, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
        targets.append(CG.ClinicalGoal(prescription.target, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ptv, CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
    return targets
  
  
  # Determine the ptv name, based on the prescription target.
  def ptv(self, ss, target):
    ptv = target.replace("C", "P")
    if not SSF.has_roi(ss, ptv):
      # Assume cropped volume (PTVc):
      ptv = ptv + "c"
    return ptv
