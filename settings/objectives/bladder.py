# Import local files:
import objective_functions as OF
import region_codes as RC
import rois as ROIS


class Bladder:
  '''Handles the configuration of optimization objectives for Bladder cases.'''

  # Creates a Bladder objectives instance.
  def __init__(self, ss, plan, prescription, beam_set_index=0):
    '''Initializes the Bladder optimization objective configuration instance with the relevant parameters.

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
    oars.append(OF.max_dvh(ss, plan, ROIS.femoral_head_l.name, 45*100, 2, 1, beam_set_index=i))
    oars.append(OF.max_dvh(ss, plan, ROIS.femoral_head_r.name, 45*100, 2, 1, beam_set_index=i))
    oars.append(OF.max_eud(ss, plan, ROIS.rectum.name, 50*100, 1, 2, beam_set_index=i))
    oars.append(OF.max_eud(ss, plan, ROIS.bowel_space.name, 20*100, 1, 2, beam_set_index=i))
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
    others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30, beam_set_index=i))
    others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30, beam_set_index=i))
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
    targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 30, beam_set_index=i))
    targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150, beam_set_index=i))
    targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.05, 80, beam_set_index=i))
    # Return objectives (filtered for possible None elements):
    return [i for i in targets if i is not None]
