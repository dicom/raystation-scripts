# encoding: utf8

# A class with clinical goal settings for Lung.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import clinical_goal as CG
import rois as ROIS
import tolerance as EQD
import tolerance_doses as TOL
import structure_set_functions as SSF


class Lung:

  # Creates a Lung clinical goals instance.
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
    if prescription.is_stereotactic():
      # SBRT:
      if prescription.nr_fractions == 3:
        # 3 fractions:
        oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_3fx, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_3fx, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.bronchial_tree.name, CG.at_most, CG.dose_at_abs_volume, TOL.main_bronchus_sbrt_3fx, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_3fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.greatves.name, CG.at_most, CG.dose_at_abs_volume, TOL.greatves_sbrt_3fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_3fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.a_pulmonary.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_3fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_mean, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_sbrt_v_15pc, 3))
        oars.append(CG.ClinicalGoal(ROIS.stomach.name, CG.at_most, CG.abs_volume_at_dose, 0.1, TOL.stomach_sbrt_3fx_cc01, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_3fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.a_pulmonary.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_3fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.chestwall.name, CG.at_most, CG.dose_at_abs_volume, TOL.chestwall_sbrt_3fx_v01, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.chestwall.name, CG.at_most, CG.abs_volume_at_dose, 30, TOL.chestwall_sbrt_3fx_v30, 6))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_3fx_cc01, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_3fx_cc10, 10, 6))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.volume_at_dose, 0.1, TOL.lung_sbrt_v_10pc, 6))
        if prescription.region_code in [248, 250]:
          # Right:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_3fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_contralat_mean, None, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_3fx, 0, 6))
        elif prescription.region_code in [247, 249]:
          # Left:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_3fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_contralat_mean, None, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_3fx, 0, 6))
        else:
          # Include OARs for both sides:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_3fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_3fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.ribs_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_3fx, 0, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_3fx, 0, 6))
      elif prescription.nr_fractions == 5:
        # 5 fractions:
        oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_5fx, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_5fx, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.bronchial_tree.name, CG.at_most, CG.dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_5fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.greatves.name, CG.at_most, CG.dose_at_abs_volume, TOL.greatves_sbrt_5fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_5fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.a_pulmonary.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_5fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_mean, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_sbrt_v_15pc, 3))
        oars.append(CG.ClinicalGoal(ROIS.stomach.name, CG.at_most, CG.abs_volume_at_dose, 0.1, TOL.stomach_sbrt_5fx_cc01, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_5fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.a_pulmonary.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_5fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.chestwall.name, CG.at_most, CG.dose_at_abs_volume, TOL.chestwall_sbrt_5fx_v01, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.chestwall.name, CG.at_most, CG.abs_volume_at_dose, 30, TOL.chestwall_sbrt_5fx_v30, 6))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_5fx_cc01, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_5fx_cc10, 10, 6))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.volume_at_dose, 0.1, TOL.lung_sbrt_v_10pc, 6))
        oars.append(CG.ClinicalGoal(ROIS.stomach.name, CG.at_most, CG.abs_volume_at_dose, 0.1, TOL.stomach_sbrt_5fx_cc01_secondary, 6))
        oars.append(CG.ClinicalGoal(ROIS.bronchial_tree.name, CG.at_most, CG.dose_at_abs_volume, TOL.main_bronchus_sbrt_5fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_5fx_secondary, 0.1, 6))
        if prescription.region_code in [248, 250]:
          # Right:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_contralat_mean, None, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_5fx, 0, 6))
        elif prescription.region_code in [247, 249]:
          # Left:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_contralat_mean, None, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_5fx, 0, 6))
        else:
          # Include OARs for both sides:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_5fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_5fx, 0, 6))
          Coars.append(G.ClinicalGoal(ROIS.ribs_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_5fx, 0, 6))
      elif prescription.nr_fractions == 8:
        # 8 fractions:
        oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_abs_volume, TOL.spinal_canal_sbrt_8fx, 0.035, 2))
        oars.append(CG.ClinicalGoal(ROIS.trachea.name, CG.at_most, CG.dose_at_abs_volume, TOL.trachea_sbrt_8fx, 0.1, 2))
        oars.append(CG.ClinicalGoal(ROIS.bronchial_tree.name, CG.at_most, CG.dose_at_abs_volume, TOL.main_bronchus_sbrt_8fx, 0.01, 2))
        oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_sbrt_8fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.greatves.name, CG.at_most, CG.dose_at_abs_volume, TOL.greatves_sbrt_8fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_8fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.a_pulmonary.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_8fx, 0.1, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_mean, None, 3))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.volume_at_dose, 0.15, TOL.lung_sbrt_v_15pc, 3))
        oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_8fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.a_pulmonary.name, CG.at_most, CG.dose_at_abs_volume, TOL.heart_sbrt_8fx_secondary, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.chestwall.name, CG.at_most, CG.dose_at_abs_volume, TOL.chestwall_sbrt_8fx_v01, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.chestwall.name, CG.at_most, CG.abs_volume_at_dose, 30, TOL.chestwall_sbrt_8fx_v30, 6))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_8fx_cc01, 0.1, 6))
        oars.append(CG.ClinicalGoal(ROIS.skin.name, CG.at_most, CG.dose_at_abs_volume, TOL.skin_sbrt_8fx_cc10, 10, 6))
        oars.append(CG.ClinicalGoal(ROIS.lungs_igtv.name, CG.at_most, CG.volume_at_dose, 0.1, TOL.lung_sbrt_v_10pc, 6))
        oars.append(CG.ClinicalGoal(ROIS.stomach.name, CG.at_most, CG.abs_volume_at_dose, 0.1, TOL.stomach_sbrt_8fx_cc01, 6))
        if prescription.region_code in [248, 250]:
          # Right:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx, 0.1, 3))          
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.lung_l.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_contralat_mean, None, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_8fx, 0, 6))
        elif prescription.region_code in [247, 249]:
          # Left:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.lung_r.name, CG.at_most, CG.average_dose, TOL.lung_sbrt_contralat_mean, None, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_8fx, 0, 6))
        else:
          # Include OARs for both sides:
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx, 0.1, 3))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx, 0.1, 3))          
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.brachial_plexus_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.brachial_sbrt_8fx_secondary, 0.1, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_r.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_8fx, 0, 6))
          oars.append(CG.ClinicalGoal(ROIS.ribs_l.name, CG.at_most, CG.dose_at_abs_volume, TOL.ribs_sbrt_8fx, 0, 6))
    else:
      # Conventional:
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
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_abs_volume, tol_spinalcanal, 0.03, 2))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.average_dose, tol_heart_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.25, tol_heart_v25, 3))
      oars.append(CG.ClinicalGoal(ROIS.a_lad.name, CG.at_most, CG.volume_at_dose, 0.10, TOL.lad_v10, 3))
      oars.append(CG.ClinicalGoal(lungs, CG.at_most, CG.average_dose, tol_lung_mean, None, 3))
      oars.append(CG.ClinicalGoal(lungs, CG.at_most, CG.volume_at_dose, 0.35, tol_lung_v35, 3))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.average_dose, tol_esophagus_mean, None, 3))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.volume_at_dose, 0.17, tol_esophagus_v17, 3))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.1, TOL.heart_v10, 4))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.355, TOL.heart_v355, 4))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.average_dose, TOL.heart_lymphopenia_mean, None, 6))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.38, TOL.heart_lymphopenia_v38, 6))
      oars.append(CG.ClinicalGoal(ROIS.heart.name, CG.at_most, CG.volume_at_dose, 0.25, TOL.heart_lymphopenia_v25, 6))
      oars.append(CG.ClinicalGoal(ROIS.a_lad.name, CG.at_most, CG.volume_at_dose, 0.01, TOL.lad_v01, 6))
      oars.append(CG.ClinicalGoal(lungs, CG.at_most, CG.average_dose, TOL.lung_lymphopenia_mean, None, 6))
      oars.append(CG.ClinicalGoal(lungs, CG.at_most, CG.volume_at_dose, 0.30, TOL.lung_lymphopenia_v30, 6))
      oars.append(CG.ClinicalGoal(lungs, CG.at_most, CG.volume_at_dose, 0.45, TOL.lung_lymphopenia_v45, 6))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, prescription_dose, 0.03, 6))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_grade3plus_max, 2.0, 6))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.average_dose, TOL.esophagus_grade3plus_mean, None, 6))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.average_dose, TOL.spleen_lymphopenia_mean, None, 6))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.volume_at_dose, 0.17, TOL.spleen_lymphopenia_v17, 6))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.volume_at_dose, 0.16, TOL.spleen_lymphopenia_v16, 6))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.volume_at_dose, 0.09, TOL.spleen_lymphopenia_v09, 6))
      oars.append(CG.ClinicalGoal(ROIS.spleen.name, CG.at_most, CG.volume_at_dose, 0.05, TOL.spleen_lymphopenia_v05, 6))
      oars.append(CG.ClinicalGoal(ROIS.spinal_canal.name, CG.at_most, CG.dose_at_abs_volume, tol_spinalcanal_chemo, 0.03, 6))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.dose_at_abs_volume, TOL.esophagus_grade2plus_max, 2.0, 7))
      oars.append(CG.ClinicalGoal(ROIS.esophagus.name, CG.at_most, CG.average_dose, TOL.esophagus_grade2plus_mean, None, 7))
    return oars


  # Create target (and External) clinical goals.
  def create_target_clinical_goals(self, ss, plan, prescription):
    targets = []
    if prescription.is_stereotactic():
      # SBRT:
      if prescription.nr_fractions == 8:
        max_factor = 1.3
      else:
        max_factor = 1.4
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, max_factor, 2.0, 4))
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      if nr_targets == 1:
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 1.0, 0.98, 1))
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_most, CG.dose_at_volume, max_factor, 0.02, 4))
        targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.88, 1.0, 5))
      else:
        for i in range(0, nr_targets):
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_least, CG.dose_at_volume, 1.0, 0.98, 1))
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_most, CG.dose_at_volume, max_factor, 0.02, 4))
          targets.append(CG.ClinicalGoal(ROIS.ptv.name+str(i+1), CG.at_least, CG.conformity_index, 0.88, 1.0, 5))
    else:
      # Conventional:
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 0.9, 0.98, 2))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.dose_at_volume, 0.93, 0.98, 5))
      targets.append(CG.ClinicalGoal(ROIS.ptv.name, CG.at_least, CG.conformity_index, 0.9, 0.95, 5))
      targets.append(CG.ClinicalGoal(ROIS.external.name, CG.at_most, CG.dose_at_abs_volume, 1.05, 2.0, 5))
      # Some variation in clinical goals whether GTV, CTV or IGTV is defined:
      if SSF.has_roi_with_shape(ss, ROIS.igtv.name):
        targets.append(CG.ClinicalGoal(ROIS.ictv.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ictv.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.igtv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ictv.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ictv.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ictv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 5))
      elif SSF.has_roi_with_shape(ss, ROIS.ctv.name):
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.995, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_most, CG.dose_at_volume, 1.005, 0.5, 1))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.95, 0.98, 2))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.homogeneity_index, 0.95, 0.98, 5))
        targets.append(CG.ClinicalGoal(ROIS.ctv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 5))
        if SSF.has_roi_with_shape(ss, ROIS.gtv.name):
          targets.append(CG.ClinicalGoal(ROIS.gtv.name, CG.at_least, CG.dose_at_volume, 0.98, 0.98, 2))
    return targets
  