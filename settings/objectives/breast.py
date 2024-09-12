# encoding: utf8

# A class with objective settings for Breast.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import objective_functions as OF
import region_codes as RC
import rois as ROIS


class Breast:

  # Creates a Breast objectives instance.
  def __init__(self, ss, plan, prescription):
    # Database attributes:
    self.ss = ss
    self.plan = plan
    self.prescription = prescription
    self.targets = self.create_target_objectives(ss, plan, prescription)
    self.others = self.create_other_objectives(ss, plan, prescription)
    self.oars = self.create_oar_objectives(ss, plan, prescription)


  # Create OAR objectives.
  def create_oar_objectives(self, ss, plan, prescription):
    oars = []
    # Independent objectives:
    oars.append(OF.max_dvh(ss, plan, ROIS.a_lad.name, prescription.total_dose*0.5*100, 2, 2))
    oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 2*100, 1, 3))
    # Regional objectives (common for both sides):
    if prescription.region_code in RC.breast_reg_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.thyroid.name, 8.7*100, 1, 1))
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 8.2*100, 1, 1))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 20*100, 1))
    # Side-dependent objectives:
    if prescription.region_code in RC.breast_l_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 16*100, 1, 2))
      oars.append(OF.max_dvh(ss, plan, ROIS.lung_l.name, prescription.total_dose*0.4*100, 15, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 1*100, 1, 1))
      oars.append(OF.max_eud(ss, plan, ROIS.breast_r.name, 3*100, 1, 1))
    elif prescription.region_code in RC.breast_r_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 16*100, 1, 2))
      oars.append(OF.max_dvh(ss, plan, ROIS.lung_r.name, prescription.total_dose*0.4*100, 15, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 1*100, 1, 1))
      oars.append(OF.max_eud(ss, plan, ROIS.breast_l.name, 3*100, 1, 1))
      if not prescription.region_code in RC.breast_partial_codes:
        # Add liver for right sided whole breast:
        oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 2*100, 1, 1))
    elif prescription.region_code in RC.breast_bilateral_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 16*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 16*100, 1, 2))
    return oars


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription):
    others = []
    others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30))
    if prescription.region_code in RC.breast_partial_codes:
      # Partial breast:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30))
    else:
      # Whole or regional breast:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 5.0, 30))
    return others
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription):
    targets = []
    if prescription.total_dose == 48:
      # SIB treatment (40.05 & 48 Gy):
      lower_dose = 40.05
      # Tumor bed:
      # CTVsb:
      targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_sb.name, prescription.total_dose*100, 30))
      targets.append(OF.min_dose(ss, plan, ROIS.ctv_sb.name, prescription.total_dose*100*0.95, 150))
      # PTVsbc:
      targets.append(OF.min_dose(ss, plan, ROIS.ptv_sbc.name, prescription.total_dose*100*0.95, 75))
      targets.append(OF.max_dose(ss, plan, ROIS.ptv_sbc.name, prescription.total_dose*100*1.05, 80))
      # Whole breast:
      # CTV:
      targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_ptv_sbc.name, lower_dose*100, 30))
      targets.append(OF.min_dose(ss, plan, prescription.target, lower_dose*100*0.95, 150))
      # PTVc:
      targets.append(OF.min_dose(ss, plan, prescription.target.replace("C", "P")+"c", lower_dose*100*0.95, 100))
      targets.append(OF.max_dose(ss, plan, ROIS.ptv_c_ptv_sbc.name, lower_dose*100*1.05, 80))
      # Added objectives for regional or bilateral cases:
      if prescription.region_code in RC.breast_reg_codes:
        # PTVpc:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_pc.name, lower_dose*100*0.95, 100))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv_pc_ptv_sbc.name, lower_dose*100*1.05, 80))
      if prescription.region_code in RC.breast_bilateral_codes:
        # Sided targets:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_R', lower_dose*100*0.95, 100))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_L', lower_dose*100*0.95, 100))
    else:
      # Non-boost treatment:
      # CTV:
      targets.append(OF.uniform_dose(ss, plan, prescription.target, prescription.total_dose*100, 30))
      targets.append(OF.min_dose(ss, plan, prescription.target, prescription.total_dose*100*0.95, 150))
      # PTVc:
      targets.append(OF.min_dose(ss, plan, prescription.target.replace("C", "P")+"c", prescription.total_dose*100*0.95, 100))
      targets.append(OF.max_dose(ss, plan, prescription.target.replace("C", "P")+"c", prescription.total_dose*100*1.05, 80))
      # Added objectives for regional or bilateral cases:
      if prescription.region_code in RC.breast_reg_codes:
        # PTVpc:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_pc.name, prescription.total_dose*100*0.95, 100))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv_pc.name, prescription.total_dose*100*1.05, 80))
      if prescription.region_code in RC.breast_bilateral_codes:
        # Sided targets:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_R', prescription.total_dose*100*0.95, 100))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_L', prescription.total_dose*100*0.95, 100))
    return targets
  