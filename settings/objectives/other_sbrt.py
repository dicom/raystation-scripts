# Import local files:
import objective_functions as OF
import region_codes as RC
import rois as ROIS


class OtherSBRT:
  '''Handles the configuration of optimization objectives for miscellaneous SBRT cases.'''

  def __init__(self, ss, plan, prescription, beam_set_index=0):
    '''Initializes the optimization objective configuration instance for miscellaneous SBRT cases.

    Args:
      ss (PyScriptObject): A RayStation StructureSet instance.
      plan (PyScriptObject]): A RayStation TreatmentPlan instance.
      prescription (Prescription): A Prescription instance.
      beam_set_index (int): A specification of beam set index (for cases of multiple beam sets).
        Defaults to 0.
    '''
    self.ss = ss
    self.plan = plan
    self.prescription = prescription
    self.beam_set_index = beam_set_index
    self.targets = self.create_target_objectives(ss, plan, prescription, beam_set_index)
    self.others = self.create_other_objectives(ss, plan, prescription, beam_set_index)
    self.oars = self.create_oar_objectives(ss, plan, prescription, beam_set_index)

  def create_oar_objectives(self, ss, plan, prescription, i):
    '''Creates organ at risk optimization objectives.

    Args:
      ss (PyScriptObject): A RayStation StructureSet instance.
      plan (PyScriptObject]): A RayStation TreatmentPlan instance.
      prescription (Prescription): A Prescription instance.
      i (int): A specification of beam set index (for cases of multiple beam sets).

    Returns:
      list[PyScriptObject]: A list of optimization objectives (ConstituentFunction instances).
    '''
    oars = []
    if prescription.region_code in RC.palliative_head_codes or prescription.region_code in RC.palliative_neck_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.brain.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dose(ss, plan, ROIS.brainstem.name, 5*100, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.oral_cavity.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.parotid_l.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.parotid_r.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.parotids.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_cord.name, 5*100, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.submand_l.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.submand_r.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.submands.name, 5*100, 1, 2, beam_set_index=i))
    elif prescription.region_code in RC.palliative_thorax_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_l.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_r.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_cord.name, 5*100, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.trachea.name, 5*100, 1, 2, beam_set_index=i))
    elif prescription.region_code in RC.palliative_abdomen_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.esophagus.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.heart.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_l.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.kidney_r.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.kidneys.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.liver.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_l.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lung_r.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.lungs.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dose(ss, plan, ROIS.spinal_cord.name, 5*100, 2, beam_set_index=i))
    elif prescription.region_code in RC.palliative_pelvis_codes:
      oars.append(OF.max_eud(ss, plan, ROIS.bladder.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.bowel_small.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_dose(ss, plan, ROIS.cauda_equina.name, 5*100, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.colon.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 5*100, 1, 2, beam_set_index=i))
      oars.append(OF.max_eud(ss, plan, ROIS.skin.name, 5*100, 1, 2, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in oars if i is not None]

  def create_other_objectives(self, ss, plan, prescription, i):
    '''Creates other (e.g. External) optimization objectives.

    Args:
      ss (PyScriptObject): A RayStation StructureSet instance.
      plan (PyScriptObject]): A RayStation TreatmentPlan instance.
      prescription (Prescription): A Prescription instance.
      i (int): A specification of beam set index (for cases of multiple beam sets).

    Returns:
      list[PyScriptObject]: A list of optimization objectives (ConstituentFunction instances).
    '''
    others = []
    others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*106, 3*100, 3, 3, beam_set_index=i))
    others.append(OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, prescription.total_dose*100, 0.65*prescription.total_dose*100, 0.5, 10, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in others if i is not None]

  def create_target_objectives(self, ss, plan, prescription, i):
    '''Creates target optimization objectives.

    Args:
      ss (PyScriptObject): A RayStation StructureSet instance.
      plan (PyScriptObject]): A RayStation TreatmentPlan instance.
      prescription (Prescription): A Prescription instance.
      i (int): A specification of beam set index (for cases of multiple beam sets).

    Returns:
      list[PyScriptObject]: A list of optimization objectives (ConstituentFunction instances).
    '''
    targets = []
    targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100, 200, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in targets if i is not None]
