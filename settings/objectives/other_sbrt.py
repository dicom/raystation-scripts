# encoding: utf8

# A class with objective settings for OtherSBRT treatments.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import objective_functions as OF
import region_codes as RC
import rois as ROIS


class OtherSBRT:

  # Creates a OtherSBRT objectives instance.
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
    if prescription.region_code in RC.palliative_head_codes or prescription.region_code in RC.palliative_neck_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.brain.name, 5*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.brainstem.name, 5*100, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.oral_cavity.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.parotid_l.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.parotid_r.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.parotids.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_cord.name, 5*100, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.submand_l.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.submand_r.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.submands.name, 5*100, 1, 2))
    elif prescription.region_code in RC.palliative_thorax_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_l.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_r.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_cord.name, 5*100, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.trachea.name, 5*100, 1, 2))
    elif prescription.region_code in RC.palliative_abdomen_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_l.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_r.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_cord.name, 5*100, 2))
    elif prescription.region_code in RC.palliative_pelvis_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.small_bowel.name, 5*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.cauda_equina.name, 5*100, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.colon.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 5*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2))
    return oars


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription):
    others = []
    others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*106, 3*100, 3, 3))
    others.append(OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, prescription.total_dose*100, 0.65*prescription.total_dose*100, 0.5, 10))
    return others
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription):
    targets = []
    targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100, 200))
    return targets
  