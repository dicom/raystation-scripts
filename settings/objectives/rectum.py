# encoding: utf8

# A class with objective settings for Rectum.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import objective_functions as OF
import region_codes as RC
import rois as ROIS


class Rectum:

  # Creates a Rectum objectives instance.
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
    if prescription.total_dose == 50:
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 10*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 4*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 5*100, 2, 2, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 15*100, 2, 1, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 15*100, 2, 1, beam_set_index=i))
    else:
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 2*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 2.5*100, 2, 2, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 7.5*100, 2, 1, beam_set_index=i))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 7.5*100, 2, 1, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in oars if i is not None]


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription, i):
    others = []
    if prescription.total_dose == 50:
      # SIB treatment (47 & 50 Gy):
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30, beam_set_index=i))
      others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30, beam_set_index=i))
      others.append(OF.fall_off(ss, plan, ROIS.z_ptv_50_wall.name, 49*100, 45*100, 0.65, 5, adapt=True, beam_set_index=i))
      others.append(OF.fall_off(ss, plan, ROIS.z_ptv_47_50_wall.name, 50*100, 32*100, 1.0, 5, adapt=True, beam_set_index=i))
    else:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.8, 15, beam_set_index=i))
      others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 20, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in others if i is not None]
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription, i):
    targets = []
    if prescription.total_dose == 50:
      # SIB treatment (47 & 50 Gy):
      targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_50.name, prescription.total_dose*100, 35, beam_set_index=i))
      targets.append(OF.min_dose(ss, plan, ROIS.ptv_50.name, prescription.total_dose*100*0.95, 150, beam_set_index=i))
      targets.append(OF.max_dose(ss, plan, ROIS.ptv_50.name, prescription.total_dose*100*1.05, 50, beam_set_index=i))
      targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_47.name, 47*100, 35, beam_set_index=i))
      targets.append(OF.min_dose(ss, plan, ROIS.ptv_47.name, 47*100*0.95, 150, beam_set_index=i))
      targets.append(OF.max_dvh(ss, plan, ROIS.ptv_47.name, 47.5*100, 3, 125, beam_set_index=i))
    else:
      targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 35, beam_set_index=i))
      targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150, beam_set_index=i))
      targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.05, 50, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in targets if i is not None]
  