# encoding: utf8


# Import local files:
import rois as ROIS
import gui_functions as GUIF
import structure_set_functions as SSF
from tkinter import messagebox


# Clinical Goal class
class ClinicalGoal(object):

  def __init__(self, name, criteria, type, tolerance, value, priority):
    self.name = name
    self.criteria = criteria
    self.type = type
    self.tolerance = tolerance
    self.value = value
    self.priority = priority
  
  # Applies the clinical goal object to a given EvaluationSetup.
  # Parameters:
  # es - A RayStation EvaluationSetup instance, in which the clinical goal is to be created
  # normalized_tolerance - an alternative to the original tolerance (AcceptanceLevel), e.q. recalculated as a percentage value of the prescription dose.
  # normalized_value - an alternative to the original dose value (ParameterValue), e.q. recalculated as a percentage value of the prescription dose.
  def apply_to(self, es, normalized_tolerance = None, normalized_value = None):
    # Use preset values if normalized arguments are not given:
    if normalized_tolerance is None:
      normalized_tolerance = self.tolerance
    if normalized_value is None:
      normalized_value = self.value
    try:
      if self.type == 'AverageDose':
        # When clinical goal is of type AverageDose, we do not use the ParameterValue when invoking the RayStation AddClinicalGoal function:
        es.AddClinicalGoal(RoiName = self.name, GoalCriteria = self.criteria, GoalType = self.type, AcceptanceLevel = normalized_tolerance, Priority = self.priority)
      else:
        # Call AddClinicalGoal function with ParameterValue:
        es.AddClinicalGoal(RoiName = self.name, GoalCriteria = self.criteria, GoalType = self.type, AcceptanceLevel = normalized_tolerance, ParameterValue = normalized_value, Priority = self.priority)
    except Exception as e:
      GUIF.handle_error_on_clinical_goal_creation(self, normalized_tolerance, normalized_value, e)
  
  # Gives a text representation of the clinical goal object.
  def text(self):
   return f"Name: {self.name}\nCriteria: {self.criteria}\nType: {self.type}\nTolerance: {self.tolerance}\nValue: {self.value}\nPriority: {self.priority}"

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
# using the given prescription to determine target clinical goals as well as doing EQD2 conversion on OAR clinical goals.
def setup_clinical_goals(ss, es, site, prescription, target):
  for cg in site.target_clinical_goals:
    # Make sure corresponding ROI exists before trying to create clinical goal:
    if SSF.has_roi(ss, cg.name):
      if cg.name in [ROIS.external.name, ROIS.igtv.name, ROIS.gtv.name] and cg.criteria == 'AtMost' and cg.tolerance != 5000:
        cg.apply_to(es, normalized_tolerance = round(cg.tolerance*prescription.total_dose*100,0))
      elif cg.name in [ROIS.ctv_sb.name, ROIS.ptv_sbc.name] and target != ROIS.ctv_sb.name or cg.tolerance == 5000 or cg.type == homogeneity_index:
        cg.apply_to(es)
      elif cg.type == conformity_index:
        cg.apply_to(es, normalized_value = round(cg.value*prescription.total_dose*100,0))
      # Attempt fix of VolumeAtDose for targets (had to implement for Breast SIB CTVp-CTVsb):
      elif cg.type == volume_at_dose:
        cg.apply_to(es)
      else:
        cg.apply_to(es, normalized_tolerance = round(cg.tolerance*prescription.total_dose*100,0))
    else:
      # Missing ROI:
      GUIF.handle_missing_roi_for_clinical_goal(cg.name)
  for cg in site.oar_clinical_goals:
    # Make sure corresponding ROI exists before trying to create clinical goal:
    if SSF.has_roi(ss, cg.name):      
      if cg.type in [dose_at_volume, dose_at_abs_volume, average_dose]:
        cg.apply_to(es, normalized_tolerance = round(cg.tolerance.equivalent(prescription.nr_fractions)*100,0))
      else:
        cg.apply_to(es, normalized_value = round(cg.value.equivalent(prescription.nr_fractions)*100,0))
    else:
      # Missing ROI:
      GUIF.handle_missing_roi_for_clinical_goal(cg.name)
