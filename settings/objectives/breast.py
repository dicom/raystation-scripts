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
  def __init__(self, ss, plan, prescription, beam_set_index=0):
    # Database attributes:
    self.ss = ss
    self.plan = plan
    self.prescription = prescription
    self.beam_set_index = beam_set_index
    self.targets = self.create_target_objectives(ss, plan, prescription, beam_set_index)
    self.others = self.create_other_objectives(ss, plan, prescription, beam_set_index)
    self.oars = self.create_oar_objectives(ss, plan, prescription, beam_set_index)


  # Create OAR objectives.
  def create_oar_objectives(self, ss, plan, prescription, i):
    oars = []
    # Independent objectives:
    oars.append(OF.max_dvh(ss, plan, ROIS.a_lad.name, prescription.total_dose*0.5*100, 2, 2, beam_set_index=i))
    oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 2*100, 1, 3, beam_set_index=i))
    # Regional objectives (common for both sides):
    if prescription.region_code in RC.breast_reg_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.thyroid.name, 8.7*100, 1, 1, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 8.2*100, 1, 1, beam_set_index=i))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 20*100, 1, beam_set_index=i))
    # Side-dependent objectives:
    if prescription.region_code in RC.breast_l_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 16*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.lung_l.name, prescription.total_dose*0.4*100, 15, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 1*100, 1, 1, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.breast_r.name, 3*100, 1, 1, beam_set_index=i))
    elif prescription.region_code in RC.breast_r_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 16*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.lung_r.name, prescription.total_dose*0.4*100, 15, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 1*100, 1, 1, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.breast_l.name, 3*100, 1, 1, beam_set_index=i))
      if not prescription.region_code in RC.breast_partial_codes:
        # Add liver for right sided whole breast:
        oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 2*100, 1, 1, beam_set_index=i))
    elif prescription.region_code in RC.breast_bilateral_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 16*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 16*100, 1, 2, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in oars if i is not None]


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription, i):
    others = []
    others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30, beam_set_index=i))
    if prescription.region_code in RC.breast_partial_codes:
      # Partial breast:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30, beam_set_index=i))
    else:
      # Whole or regional breast:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 5.0, 30, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in others if i is not None]
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription, i):
    targets = []
    if prescription.region_code in RC.breast_r_codes:
      wall_name = 'zCTV_R_Wall'
    elif prescription.region_code in RC.breast_l_codes:
      wall_name = 'zCTV_L_Wall'
    if prescription.total_dose == 48:
      # SIB treatment (40.05 & 48 Gy):
      lower_dose = 40.05
      ptv_min_dose_target = ROIS.ptv_c.name
      # Tumor bed:
      # CTVsb:
      targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_sb.name, prescription.total_dose*100, 30, beam_set_index=i))
      targets.append(OF.min_dose(ss, plan, ROIS.ctv_sb.name, prescription.total_dose*100*0.95, 150, beam_set_index=i))
      # PTVsbc:
      targets.append(OF.min_dose(ss, plan, ROIS.ptv_sbc.name, prescription.total_dose*100*0.95, 75, beam_set_index=i))
      targets.append(OF.max_dose(ss, plan, ROIS.ptv_sbc.name, prescription.total_dose*100*1.05, 80, beam_set_index=i))
      # Whole breast:
      # PTVc:
      targets.append(OF.min_dose(ss, plan, ptv_min_dose_target, lower_dose*100*0.95, 100, beam_set_index=i))
      if prescription.region_code in RC.breast_reg_codes:
        # Regional breast:
        # PTVpc:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_pc.name, lower_dose*100*0.95, 100, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, 'z'+ROIS.ctv_p_ptv_sbc.name, lower_dose*100, 30, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, 'z'+ROIS.ptv_pc_ptv_sbc.name, lower_dose*100*1.05, 80, beam_set_index=i))
      else:
        # Whole breast:
        targets.append(OF.min_dose(ss, plan, 'z'+ROIS.ctv_ptv_sbc.name, lower_dose*100*0.95, 150, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, 'z'+ROIS.ctv_ptv_sbc.name, lower_dose*100, 30, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, 'z'+ROIS.ptv_c_ptv_sbc.name, lower_dose*100*1.05, 80, beam_set_index=i))
      if prescription.region_code in RC.breast_bilateral_codes:
        # Bilateral: Sided targets:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_R', lower_dose*100*0.95, 100, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_L', lower_dose*100*0.95, 100, beam_set_index=i))
      # Wall:
      targets.append(OF.max_dose(ss, plan, wall_name, lower_dose*100*1.05, 200, beam_set_index=i))
    else:
      # Non-boost treatment:
      # CTV:
      targets.append(OF.uniform_dose(ss, plan, prescription.target, prescription.total_dose*100, 30, beam_set_index=i))
      targets.append(OF.min_dose(ss, plan, prescription.target, prescription.total_dose*100*0.95, 150, beam_set_index=i))
      # PTVc:
      targets.append(OF.min_dose(ss, plan, prescription.target.replace("C", "P")+"c", prescription.total_dose*100*0.95, 100, beam_set_index=i))
      targets.append(OF.max_dose(ss, plan, prescription.target.replace("C", "P")+"c", prescription.total_dose*100*1.05, 80, beam_set_index=i))
      # Added objectives for regional or bilateral cases:
      if prescription.region_code in RC.breast_reg_codes:
        # PTVpc:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_pc.name, prescription.total_dose*100*0.95, 100, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv_pc.name, prescription.total_dose*100*1.05, 80, beam_set_index=i))
      if prescription.region_code in RC.breast_bilateral_codes:
        # Sided targets:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_R', prescription.total_dose*100*0.95, 100, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_c.name+'_L', prescription.total_dose*100*0.95, 100, beam_set_index=i))
        # Wall:
        targets.append(OF.max_dose(ss, plan, 'zCTV_R_Wall', prescription.total_dose*100*1.05, 200, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, 'zCTV_L_Wall', prescription.total_dose*100*1.05, 200, beam_set_index=i))
      elif prescription.region_code not in RC.breast_partial_codes:
        # Wall:
        targets.append(OF.max_dose(ss, plan, wall_name, prescription.total_dose*100*1.05, 200, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in targets if i is not None]
  