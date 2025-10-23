# encoding: utf8

# A class with objective settings for Prostate.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import objective_functions as OF
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF


class Prostate:

  # Creates a Prostate objectives instance.
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
    if prescription.region_code in RC.prostate_bed_codes:
      # Prostate bed:
      if prescription.region_code in RC.prostate_node_codes:
        # With elective nodes:
        oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 15*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 25*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anal_canal.name, 40*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 60*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 45*100, 2, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 13*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 13*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bone.name, 25*100, 1, 1, beam_set_index=i))
      else:
        # Prostate bed only:
        oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 25*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anal_canal.name, 20*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 60*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 10*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 10*100, 1, 1, beam_set_index=i))
    else:
      # Prostate:
      if prescription.total_dose == 67.5 and prescription.region_code in RC.prostate_node_codes:
        # High risk prostate with elective nodes:
        oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 15*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 25*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anal_canal.name, 15*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 16*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 20*100, 2, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 8*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 8*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bone.name, 25*100, 1, 1, beam_set_index=i))
      elif prescription.total_dose == 67.5:
        # High risk prostate only:
        oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 25*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anal_canal.name, 7*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 16*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 8*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 8*100, 1, 1, beam_set_index=i))
      elif prescription.total_dose == 60:
        # Intermediate (or high risk) prostate only:
        oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 23*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anal_canal.name, 6*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 14*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 7*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 7*100, 1, 1, beam_set_index=i))
      elif prescription.total_dose == 36.25:
        # Favorable intermediate prostate (SBRT):
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 7*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 3*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 3*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anorectum.name, 10*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_dvh(ss, plan, ROIS.anorectum.name, 35*100, 0.1, 50, beam_set_index=i))
        oars.append(OF.max_dvh(ss, plan, ROIS.urethra.name, 41.5*100, 40, 10, beam_set_index=i))
      else:
        # STAMPEDE or palliative:
        oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 23*100, 1, 4, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.anal_canal.name, 6*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 14*100, 1, 2, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_l.name, 7*100, 1, 1, beam_set_index=i))
        oars.append(OF.max_eud(ss, plan, ROIS.femoral_r.name, 7*100, 1, 1, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in oars if i is not None]


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription, i):
    others = []
    if prescription.total_dose == 36.25:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 2.8, 20, adapt=True, beam_set_index=i))
      others.append(OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, 34.44*100, 29.5*100, 1, 2, adapt=True, beam_set_index=i))
    else:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 2, 20, adapt=True, beam_set_index=i))
    if prescription.region_code in RC.prostate_bed_codes:
      # Prostate bed:
      others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 25, beam_set_index=i))   
      if prescription.region_code in RC.prostate_node_codes:
        # With elective nodes:
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_70_wall.name, prescription.total_dose*100, 56*100, 1, 1, adapt=True, beam_set_index=i))
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_56_wall.name, 70*100, 42*100, 1, 1, adapt=True, beam_set_index=i))
      else:
        # Prostate bed only:
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_70_wall.name, prescription.total_dose*100, 56*100, 1, 1, beam_set_index=i))
    else:
      # Prostate:
      if not prescription.total_dose == 36.25:
        # For non-SBRT prostate:
        others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.038, 25, beam_set_index=i))
      if prescription.total_dose == 67.5 and prescription.region_code in RC.prostate_node_codes:
        # High risk prostate with elective nodes:
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_67_5_wall.name, prescription.total_dose*100, 62*100, 0.3, 1, adapt=True, beam_set_index=i))
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_62_5_67_5_wall.name, prescription.total_dose*100, 47*100, 0.8, 12, adapt=True, beam_set_index=i))
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_50_62_5_67_5_wall.name, 67.5*100, 40*100, 1.0, 10, adapt=True, beam_set_index=i))
      elif prescription.total_dose == 67.5:
        # High risk prostate only:
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_67_5_wall.name, prescription.total_dose*100, 62*100, 0.3, 10, adapt=True, beam_set_index=i))
      elif prescription.total_dose == 60:
        # Intermediate (or high risk) prostate only:
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_60_wall.name, prescription.total_dose*100, 57*100, 0.3, 1, adapt=True, beam_set_index=i))
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_57_60_wall.name, prescription.total_dose*100, 42*100, 0.8, 12, adapt=True, beam_set_index=i))
      else:
        if not prescription.total_dose == 36.25:
          # STAMPEDE or palliative:
          others.append(OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, prescription.total_dose*100, 0.8*prescription.total_dose*100, 1, 1, adapt=True, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in others if i is not None]
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription, i):
    targets = []
    if prescription.region_code in RC.prostate_bed_codes:
      # Prostate bed:
      if prescription.region_code in RC.prostate_node_codes:
        # With elective nodes:
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_70.name, prescription.total_dose*100, 20, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_56.name, 56*100, 20, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_70.name, 67*100, 150, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_56.name, 54*100, 150, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv_70.name, prescription.total_dose*100*1.045, 70, beam_set_index=i))
        targets.append(OF.max_dvh(ss, plan, ROIS.ptv_56.name, 58.24*100, 5, 5, beam_set_index=i))
        # Plan includes positive nodes to be treated with 66 Gy?
        if SSF.has_roi(ss, ROIS.ptv_66.name):
          targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_66.name, 66*100, 25, beam_set_index=i))
          targets.append(OF.min_dose(ss, plan, ROIS.ptv_66.name, 62.7*100, 100, beam_set_index=i))
          targets.append(OF.max_dvh(ss, plan, ROIS.ptv_66.name, 66*1.025*100, 5, 50, beam_set_index=i))
      else:
        # Prostate bed only:
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_70.name, prescription.total_dose*100, 25, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_70.name, prescription.total_dose*100*0.96, 100, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv_70.name, prescription.total_dose*100*1.03, 50, beam_set_index=i))
    else:
      # Prostate:
      if prescription.total_dose == 67.5 and prescription.region_code in RC.prostate_node_codes:
        # High risk prostate with elective nodes:
        targets.append(OF.uniform_dose(ss, plan, 'CTV!_50', 50*100, 15, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, 'CTV!_62.5', 62.5*100, 25, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, 'CTV_67.5', 67.5*100, 20, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, 'PTV!_50', 48*100, 100, beam_set_index=i))
        targets.append(OF.max_dvh(ss, plan, 'PTV!_50', 52*100, 5, 5, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, 'PTV!_62.5', prescription.total_dose*100*0.88, 100, beam_set_index=i))
        targets.append(OF.max_dvh(ss, plan, 'PTV!_62.5', prescription.total_dose*0.95*100, 5, 50, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, 'PTV_67.5', prescription.total_dose*100*0.98, 100, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, 'PTV_67.5', prescription.total_dose*100*1.02, 70, beam_set_index=i))
        # Plan includes positive nodes to be treated with 60 Gy?
        if SSF.has_roi(ss, ROIS.ptv__60.name):
          targets.append(OF.uniform_dose(ss, plan, ROIS.ctv__60.name, 60*100, 25, beam_set_index=i))
          targets.append(OF.min_dose(ss, plan, ROIS.ptv__60.name, 57*100, 100, beam_set_index=i))
          targets.append(OF.max_dvh(ss, plan, ROIS.ptv__60.name, 60*1.025*100, 5, 50, beam_set_index=i))
      elif prescription.total_dose == 67.5:
        # High risk prostate only:
        targets.append(OF.uniform_dose(ss, plan, 'CTV!_62.5', 62.5*100, 25, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, 'CTV_67.5', 67.5*100, 20, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, 'PTV!_62.5', prescription.total_dose*100*0.88, 100, beam_set_index=i))
        targets.append(OF.max_dvh(ss, plan, 'PTV!_62.5', prescription.total_dose*0.95*100, 5, 50, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, 'PTV_67.5', prescription.total_dose*100*0.98, 100, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, 'PTV_67.5', prescription.total_dose*100*1.02, 70, beam_set_index=i))
      elif prescription.total_dose == 60:
        # Intermediate (or high risk) prostate only:
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_60.name, prescription.total_dose*100, 40, beam_set_index=i))
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_57.name, prescription.total_dose*0.95*100, 40, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_60.name, 57.1*100, 150, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_57.name, prescription.total_dose*100*0.91, 170, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ctv_57.name, prescription.total_dose*100*0.93, 35, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv_60.name, prescription.total_dose*100*1.02, 60, beam_set_index=i))
        targets.append(OF.max_dvh(ss, plan, ROIS.ptv_57.name, prescription.total_dose*0.978*100, 1, 50, beam_set_index=i))
      elif prescription.total_dose == 36.25:
        # Favorable intermediate prostate (SBRT):
        targets.append(OF.min_dvh(ss, plan, ROIS.ctv_40.name, 40*100, 95, 200, beam_set_index=i))
        #targets.append(OF.min_dvh(ss, plan, ROIS.ptv_36_25.name, 36.25*100, 95, 100, beam_set_index=i))
        #targets.append(OF.min_dose(ss, plan, ROIS.ptv_36_25.name, 34.4*100, 50, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv_36_25.name, 36.25*100, 80, beam_set_index=i))
        #targets.append(OF.max_dose(ss, plan, ROIS.ptv_36_25.name, 43*100, 25, beam_set_index=i))
        targets.append(OF.max_dvh(ss, plan, ROIS.ptv_36_25.name, 42.4*100, 1.7, 50, beam_set_index=i))
      else:
        # STAMPEDE or palliative:
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 40, beam_set_index=i))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150, beam_set_index=i))
        targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.02, 60, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in targets if i is not None]
  