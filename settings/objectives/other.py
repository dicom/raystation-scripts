# encoding: utf8

# A class with objective settings for Other (palliative) treatments.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import objective_functions as OF
import region_codes as RC
import rois as ROIS


class Other:

  # Creates a Other objectives instance.
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
    if prescription.region_code in RC.palliative_head_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.eye_l.name, 13*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.eye_r.name, 13*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 35.8*100, 2))
    elif prescription.region_code in RC.palliative_neck_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.parotids.name, 20*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 35.8*100, 2))
    elif prescription.region_code in RC.palliative_thorax_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 24.9*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 20.7*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 23.9*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 19.2*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 35.8*100, 2))
    elif prescription.region_code in RC.palliative_thorax_and_abdomen_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 33.8*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 24.9*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 20.7*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 12.1*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 23.9*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 19.2*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 35.8*100, 2))
    elif prescription.region_code in RC.palliative_abdomen_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 33.8*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 12.1*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 23.9*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 35.8*100, 2))
    elif prescription.region_code in RC.palliative_abdomen_and_pelvis_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 41.6*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 33.8*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 12.1*100, 1, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 33.6*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 35.8*100, 2))
    elif prescription.region_code in RC.palliative_pelvis_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 41.6*100, 1, 2))
      oars.append(OF.max_dose(ss, plan, ROIS.cauda_equina.name, 35.8*100, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 33.8*100, 1, 2))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_l.name, 33.2*100, 2, 2))
      oars.append(OF.max_dvh(ss, plan, ROIS.femur_head_neck_r.name, 33.2*100, 2, 2))
      oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 33.6*100, 1, 2))
    return oars


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription):
    others = []
    others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30))
    others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30))
    others.append(OF.fall_off(ss, plan, ROIS.wall_ptv.name, prescription.total_dose*100, prescription.total_dose*0.75*100, 1.0, 2))
    return others
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription):
    targets = []
    targets.append(OF.uniform_dose(ss, plan, prescription.target, prescription.total_dose*100, 30))
    targets.append(OF.min_dose(ss, plan, prescription.target.replace("C", "P"), prescription.total_dose*100*0.95, 150))
    targets.append(OF.max_dose(ss, plan, prescription.target.replace("C", "P"), prescription.total_dose*100*1.05, 80))
    return targets
  