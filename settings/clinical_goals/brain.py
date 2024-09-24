# encoding: utf8

# A class with clinical goal settings for Brain.
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


class Brain:

  # Creates a Brain clinical goals instance.
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
    if prescription.region_code in RC.brain_whole_codes:
      # Whole brain:
      oars.append(CG.ClinicalGoal(ROIS.cochlea_l.name, CG.at_most, CG.average_dose, TOL.cochlea_mean_tinnitus, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.cochlea_r.name, CG.at_most, CG.average_dose, TOL.cochlea_mean_tinnitus, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.lens_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_v003_adx, 0.03, 3))
      oars.append(CG.ClinicalGoal(ROIS.lens_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_v003_adx, 0.03, 3))
      oars.append(CG.ClinicalGoal(ROIS.lacrimal_l.name, CG.at_most, CG.average_dose, TOL.lacrimal_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.lacrimal_r.name, CG.at_most, CG.average_dose, TOL.lacrimal_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_v003_adx, 0.03, 6))
    elif prescription.region_code in RC.brain_partial_codes:
      # Partial brain (SBRT & conventional):
      oars.append(CG.ClinicalGoal(ROIS.hippocampus_l.name, CG.at_most, CG.average_dose, TOL.hippocampus_v40, None, 5))
      oars.append(CG.ClinicalGoal(ROIS.hippocampus_r.name, CG.at_most, CG.average_dose, TOL.hippocampus_v40, None, 5))
      if prescription.nr_fractions == 1:
        # SRT (1 fraction):
        oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.abs_volume_at_dose, 15, TOL.brain_srt_1fx, 2))
        oars.append(CG.ClinicalGoal(ROIS.brainstem.name, CG.at_most, CG.dose_at_abs_volume, TOL.brainstem_srt_1fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_chiasm.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_chiasm_srt_1fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.brainstem.name, CG.at_most, CG.dose_at_abs_volume, TOL.brainstem_srt_1fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.optic_chiasm.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_chiasm_srt_1fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_1fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_l.name, CG.at_most, CG.average_dose, TOL.cochlea_srt_1fx, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_r.name, CG.at_most, CG.average_dose, TOL.cochlea_srt_1fx, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.eye_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.eye_srt_1fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.eye_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.eye_srt_1fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_srt_1fx_v10, 10, 4))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_srt_1fx_v0_1, 0.1, 4))
        oars.append(CG.ClinicalGoal(ROIS.lens_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_srt_1fx, 0.1, 4))
        oars.append(CG.ClinicalGoal(ROIS.lens_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_srt_1fx, 0.1, 4))
        oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.abs_volume_at_dose, 10, TOL.brain_srt_1fx, 4))
        oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.abs_volume_at_dose, 5, TOL.brain_srt_1fx, 6))
      elif prescription.nr_fractions == 3:
        # SRT (3 fractions):
        oars.append(CG.ClinicalGoal(ROIS.brainstem.name, CG.at_most, CG.dose_at_abs_volume, TOL.brainstem_srt_3fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_chiasm.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_chiasm_srt_3fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p1, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.abs_volume_at_dose, 30, TOL.brain_srt_3fx, 3))
        oars.append(CG.ClinicalGoal(ROIS.brainstem.name, CG.at_most, CG.dose_at_abs_volume, TOL.brainstem_srt_3fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.optic_chiasm.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_chiasm_srt_3fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_srt_3fx_p2, 0.035, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_l.name, CG.at_most, CG.average_dose, TOL.cochlea_srt_3fx, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_r.name, CG.at_most, CG.average_dose, TOL.cochlea_srt_3fx, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.eye_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.eye_srt_3fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.eye_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.eye_srt_3fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_srt_3fx_v0_1, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_srt_3fx_v10, 10, 3))
        oars.append(CG.ClinicalGoal(ROIS.lens_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_srt_3fx, 0.1, 4))
        oars.append(CG.ClinicalGoal(ROIS.lens_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_srt_3fx, 0.1, 4))
        oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.abs_volume_at_dose, 20, TOL.brain_srt_3fx, 4))
      else:
        # Partial brain:
        oars.append(CG.ClinicalGoal(ROIS.brainstem_surface.name, CG.at_most, CG.dose_at_abs_volume, TOL.brainstem_surface_v003_adx, 0.03, 2))
        oars.append(CG.ClinicalGoal(ROIS.brainstem_core.name, CG.at_most, CG.dose_at_abs_volume, TOL.brainstem_core_v003_adx, 0.03, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_chiasm.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_chiasm_v003_adx, 0.03, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_v003_adx, 0.03, 2))
        oars.append(CG.ClinicalGoal(ROIS.optic_nrv_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.optic_nrv_v003_adx, 0.03, 2))
        oars.append(CG.ClinicalGoal(ROIS.retina_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.retina_v003_adx, 0.03, 3))
        oars.append(CG.ClinicalGoal(ROIS.retina_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.retina_v003_adx, 0.03, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_l.name, CG.at_most, CG.average_dose, TOL.cochlea_mean, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_r.name, CG.at_most, CG.average_dose, TOL.cochlea_mean, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_l.name, CG.at_most, CG.average_dose, TOL.cochlea_mean_tinnitus, None, 4))
        oars.append(CG.ClinicalGoal(ROIS.cochlea_r.name, CG.at_most, CG.average_dose, TOL.cochlea_mean_tinnitus, None, 4))
        oars.append(CG.ClinicalGoal(ROIS.lacrimal_l.name, CG.at_most, CG.average_dose, TOL.lacrimal_mean, None, 4))
        oars.append(CG.ClinicalGoal(ROIS.lacrimal_r.name, CG.at_most, CG.average_dose, TOL.lacrimal_mean, None, 4))
        oars.append(CG.ClinicalGoal(ROIS.lens_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_v003_adx, 0.03, 4))
        oars.append(CG.ClinicalGoal(ROIS.lens_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.lens_v003_adx, 0.03, 4))
        oars.append(CG.ClinicalGoal(ROIS.pituitary.name, CG.at_most, CG.average_dose, TOL.pituitary_mean, None, 4))
        oars.append(CG.ClinicalGoal(ROIS.pituitary.name, CG.at_most, CG.average_dose, TOL.pituitary_2_mean, None, 4))
        oars.append(CG.ClinicalGoal(ROIS.cornea_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.cornea_v003_adx, 0.03, 4))
        oars.append(CG.ClinicalGoal(ROIS.cornea_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.cornea_v003_adx, 0.03, 4))
        oars.append(CG.ClinicalGoal(ROIS.brain.name, CG.at_most, CG.dose_at_abs_volume, TOL.brain_v003, 3.0, 5))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_v003_adx, 0.03, 6))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    if prescription.is_stereotactic():
      # SRT:
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.5, 2.0, 4))
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      if nr_targets == 1:
        # Single target:
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 1.0, 0.99, 1))
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_most, CG.dose_at_volume, 1.5, 0.02, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.9, 1.0, 5))
      else:
        # Multiple targets:
        for i in range(0, nr_targets):
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_least, CG.dose_at_volume, 1.0, 0.99, 1))
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_most, CG.dose_at_volume, 1.4, 0.02, 4))
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_least, CG.conformity_index, 0.9, 1.0, 5))
    else:
      # Whole brain or partial brain:
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 4))
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 4))
      targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.95, 0.95, 5))
    return targets
  