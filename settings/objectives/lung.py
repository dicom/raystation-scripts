# encoding: utf8

# A class with objective settings for Lung.
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


class Lung:

  # Creates a Lung objectives instance.
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
    if prescription.is_stereotactic():
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      for i in range(0, nr_targets):
        oars.append(OF.max_dose(ss, plan, ROIS.skin.name, 30*100, 10, beam_set_index = i))
        oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 13*100, 5, beam_set_index = i))
        oars.append(OF.max_dvh(ss, plan, ROIS.chestwall.name, 30*100, 2, 100, beam_set_index = i))
        oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 4.5*100, 1, 1, beam_set_index = i))
        if prescription.region_code in RC.lung_r_codes:
          oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 6.5*100, 1, 3, beam_set_index = i))
          oars.append(OF.max_dose(ss, plan, ROIS.ribs_r.name, prescription.total_dose*120, 10, beam_set_index = i))
        else:
          oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 6.5*100, 1, 3, beam_set_index = i))
          oars.append(OF.max_dose(ss, plan, ROIS.ribs_l.name, prescription.total_dose*120, 10, beam_set_index = i))
    else:
      if prescription.total_dose > 40:
        # Curative fractionation:
        oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 0.51*prescription.total_dose*100, 1, 1)) # (~34 Gy for 66 Gy total dose)
        oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 0.53*prescription.total_dose*100, 1, 10)) # (~35 Gy for 66 Gy total dose)
        oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 0.757*prescription.total_dose*100, 10)) # (~50 Gy for 66 Gy total dose)
        # Determine which ROI to use for lung optimization:
        match = False
        if SSF.has_roi_with_shape(ss, ROIS.lungs_gtv.name):
          l = ROIS.lungs_gtv.name
        elif SSF.has_roi_with_shape(ss, ROIS.lungs_igtv.name):
          l = ROIS.lungs_igtv.name
        else:
          l = ROIS.lungs.name
        oars.append(OF.max_eud(ss, plan, l, 0.29*prescription.total_dose*100, 1, 15)) # (~19 Gy for 66 Gy total dose)
        oars.append(OF.max_dvh(ss, plan, l, prescription.total_dose*0.07575*100, 55, 70)) # (~5 Gy for 66 Gy total dose)
        oars.append(OF.max_dvh(ss, plan, l, prescription.total_dose*0.3030*100, 30, 80)) # (~5 Gy for 66 Gy total dose)
      elif prescription.total_dose < 40:
        # Palliative fractionation:
        oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 0.29*prescription.total_dose*100, 1, 10))
        oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 0.23*prescription.total_dose*100, 1, 15))
        oars.append(OF.max_dose(ss, plan, ROIS.spinal_canal.name, 0.95*prescription.total_dose*100, 5))
    return oars


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription):
    others = []
    if prescription.is_stereotactic():
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      for i in range(0, nr_targets):
        others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 3, 5, beam_set_index = i))
        others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*130, 15, beam_set_index = i))
      if nr_targets == 1:
        others.append(OF.fall_off(ss, plan, ROIS.wall_ptv.name, prescription.total_dose*100, 0.7*prescription.total_dose*100, 0.8, 5))
      else:
        for i in range(0, nr_targets):
          others.append(OF.fall_off(ss, plan, "zPTV"+str(i+1)+"_Wall", prescription.total_dose*100, 0.7*prescription.total_dose*100, 0.8, 5, beam_set_index = i))
    else:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 3, 2))
    return others
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription):
    targets = []
    if prescription.is_stereotactic():
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      if nr_targets == 1:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100, 250))
      else:
        for i in range(0, nr_targets):
          targets.append(OF.min_dose(ss, plan, ROIS.ptv.name+str(i+1), prescription.total_dose*100, 250, beam_set_index = i))
    else:
      targets.append(OF.uniform_dose(ss, plan, prescription.target, prescription.total_dose*100, 25))
      targets.append(OF.min_dvh(ss, plan, prescription.target, prescription.total_dose*0.95*100, 98, 100))
      targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.05, 120))
      targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150))
    return targets
  