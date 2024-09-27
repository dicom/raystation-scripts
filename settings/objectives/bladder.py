# encoding: utf8

# A class with objective settings for Bladder.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import objective_functions as OF
import region_codes as RC
import rois as ROIS


class Bladder:

  # Creates a Bladder objectives instance.
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
    oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 45*100, 2, 1, beam_set_index=i))
    oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 45*100, 2, 1, beam_set_index=i))
    oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 50*100, 1, 2, beam_set_index=i))
    oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 20*100, 1, 2, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in oars if i is not None]


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription, i):
    others = []
    others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30, beam_set_index=i))
    others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in others if i is not None]
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription, i):
    targets = []
    targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 30, beam_set_index=i))
    targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150, beam_set_index=i))
    targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.05, 80, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in targets if i is not None]
  