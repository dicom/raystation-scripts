# encoding: utf8


# Import local files:
import rois as ROIS
import gui_functions as GUIF
import structure_set_functions as SSF


# Clinical Goal class
class ClinicalGoal(object):

  def __init__(self, name, criteria, type, tolerance, value, priority):
    self.name = name
    self.criteria = criteria
    self.type = type
    self.tolerance = tolerance
    self.value = value
    self.priority = priority


# Types:
volume_at_dose = 'VolumeAtDose'
abs_volume_at_dose = 'AbsoluteVolumeAtDose'
dose_at_abs_volume = 'DoseAtAbsoluteVolume'
dose_at_volume = 'DoseAtVolume'
average_dose = 'AverageDose'
homogeneity_index = 'HomogeneityIndex'
conformity_index = 'ConformityIndex'


# Sets up clinical goals.
# Creates clinical goals in RayStation from clinical goal objects from the given Site,
# using the given fractionation to determine target clinical goals as well as doing EQD2 conversion on OAR clinical goals.
def setup_clinical_goals(ss, es, site, total_dose, nr_fractions, target):
  for cg in site.target_clinical_goals:
    # Make sure corresponding ROI exists before trying to create clinical goal:
    if SSF.has_roi(ss, cg.name):
      if cg.name in [ROIS.external.name, ROIS.igtv.name, ROIS.gtv.name] and cg.criteria == 'AtMost' and cg.tolerance != 5000:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance*total_dose*100, ParameterValue = cg.value, Priority = cg.priority)
      elif cg.name in [ROIS.ctv_sb.name, ROIS.ptv_sbc.name] and target != ROIS.ctv_sb.name or cg.tolerance == 5000 or cg.type == homogeneity_index:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance, ParameterValue = cg.value, Priority = cg.priority)
      elif cg.type == conformity_index:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance, ParameterValue = cg.value*total_dose*100, Priority = cg.priority)
      else:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance*total_dose*100, ParameterValue = cg.value, Priority = cg.priority)

    else:
      # Missing ROI:
      GUIF.handle_missing_roi_for_clinical_goal(cg.name)

  for cg in site.oar_clinical_goals:
    # Make sure corresponding ROI exists before trying to create clinical goal:
    if SSF.has_roi(ss, cg.name):
      if cg.type != average_dose:
        if cg.type in [dose_at_volume, dose_at_abs_volume]:
          c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance.equivalent(nr_fractions)*100, ParameterValue = cg.value, Priority = cg.priority)
        else:
          c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance, ParameterValue = cg.value.equivalent(nr_fractions)*100, Priority = cg.priority)
      else:
        c = es.AddClinicalGoal(RoiName = cg.name, GoalCriteria = cg.criteria, GoalType = cg.type, AcceptanceLevel = cg.tolerance.equivalent(nr_fractions)*100, Priority = cg.priority)
    else:
      # Missing ROI:
      GUIF.handle_missing_roi_for_clinical_goal(cg.name)




