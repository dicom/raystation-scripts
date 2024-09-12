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
    if prescription.total_dose == 50:
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 15*100, 2, 1))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 15*100, 2, 1))
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 10*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 4*100, 1, 2))
      oars.append(OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 5*100, 2, 2))
    else:
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 7.5*100, 2, 1))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 7.5*100, 2, 1))
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 2*100, 1, 2))
      oars.append(OF.max_dvh(ss, plan, ROIS.cauda_equina.name, 2.5*100, 2, 2))
    return oars


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription):
    others = []
    others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.8, 15))
    others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 20))
    return others
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription):
    targets = []
    targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 35))
    targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150))
    targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.05, 50))
    return targets
  