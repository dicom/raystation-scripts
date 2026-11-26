'''Contains both the ClinicalGoal class as well as a couple of functions for setting up clinical goals.'''

# Import local files:
import gui_functions as GUIF
import rois as ROIS
import structure_set_functions as SSF


class ClinicalGoal(object):
  '''Class for creating a Clinical Goal in RayStation based on given input parameters.'''

  def __init__(self, name, criteria, type, tolerance, value, priority):
    '''Initializes the clinical goal with the relevant parameters.

    Args:
      name (str): Name of ROI (e.g. "Prostate").
      criteria (str): Planning goal criteria (e.g. "AtMost").
      type (str): goal type (e.g. "DoseAtVolume").
      tolerance (Tolerance, float): Primary acceptance level - the level at which a clinical goal is considered fulfilled (e.g. 6.5).
      value (Tolerance, float): The parameter value (goal type specific parameter) (e.g. 3.5).
      priority (int): The priority of the clinical goal (1-n).
    '''
    self.name = name
    self.criteria = criteria
    self.type = type
    self.tolerance = tolerance
    self.value = value
    self.priority = priority

  def apply_to(self, es, normalized_tolerance = None, normalized_value = None, ignore_identical = False):
    '''Applies the clinical goal instance to a given EvaluationSetup.

    Args:
      es (PyScriptObject): The RayStation EvaluationSetup instance (in which the clinical goal is to be created).
      normalized_tolerance (float): An alternative to the original tolerance (PrimaryAcceptanceLevel),
        e.q. recalculated as a percentage value of the prescription dose. Defaults to None.
      normalized_value (float): An alternative to the original dose value (ParameterValue),
        e.q. recalculated as a percentage value of the prescription dose. Defaults to None.
      ignore_identical (bool): If True, the function will not display a warning if an
        identical clinical goal already exists. Defaults to False.
    '''
    # Use preset values if normalized arguments are not given:
    if normalized_tolerance is None:
      normalized_tolerance = self.tolerance
    if normalized_value is None:
      normalized_value = self.value
    try:
      if self.type == 'AverageDose':
        # When clinical goal is of type AverageDose, we do not use the ParameterValue when invoking the RayStation AddClinicalGoal function:
        es.AddClinicalGoal(RoiName = self.name, GoalCriteria = self.criteria, GoalType = self.type, PrimaryAcceptanceLevel = normalized_tolerance, Priority = self.priority, AssociateToPlan = True)
      else:
        # Call AddClinicalGoal function with ParameterValue:
        es.AddClinicalGoal(RoiName = self.name, GoalCriteria = self.criteria, GoalType = self.type, PrimaryAcceptanceLevel = normalized_tolerance, ParameterValue = normalized_value, Priority = self.priority, AssociateToPlan = True)
    except Exception as e:
      # If ignore_identical keyword is set, and exception is "An identical clinical goal already exists", do not display error.
      # Otherwise error will be shown.
      if not ignore_identical or 'identical' not in str(e.args[0]):
        GUIF.handle_error_on_clinical_goal_creation(self, normalized_tolerance, normalized_value, e)

  def text(self):
    '''Gives a text representation of the clinical goal instance.

    Returns:
      str: A text representation of the clinical goal instance.
    '''
    return f"Name: {self.name}\nCriteria: {self.criteria}\nType: {self.type}\nTolerance: {self.tolerance}\nValue: {self.value}\nPriority: {self.priority}"

# Limits:
at_most = 'AtMost'
at_least = 'AtLeast'

# Types:
volume_at_dose = 'VolumeAtDose'
abs_volume_at_dose = 'AbsoluteVolumeAtDose'
dose_at_abs_volume = 'DoseAtAbsoluteVolume'
dose_at_volume = 'DoseAtVolume'
average_dose = 'AverageDose'
homogeneity_index = 'HomogeneityIndex'
conformity_index = 'ConformityIndex'


def setup_clinical_goals(ss, es, site, prescription, target, ignore_identical = False):
  '''Creates clinical goals in RayStation based on clinical goal objects from the given Site, using the given
  prescription to determine target clinical goals as well as doing EQD2 conversion on OAR clinical goals.

  Args:
    es (PyScriptObject): The RayStation EvaluationSetup instance (in which the clinical goal is to be created).
    site (Site): The Site instance containing lists of clinical goals to set up.
    prescription (Prescription): The Prescription instance for this beam set.
    target (ROI): The target ROI for this beam set.
    ignore_identical (bool): If True, the function will not display a warning if an
      identical clinical goal already exists. Defaults to False.
  '''
  for cg in site.target_clinical_goals:
    setup_target(ss, es, prescription, cg)
  for cg in site.oar_clinical_goals:
    # Make sure corresponding ROI exists before trying to create clinical goal:
    if SSF.has_roi(ss, cg.name):
      if cg.type in [dose_at_volume, dose_at_abs_volume, average_dose]:
        cg.apply_to(es, normalized_tolerance = round(cg.tolerance.equivalent(prescription.nr_fractions)*100,0), ignore_identical=ignore_identical)
      else:
        cg.apply_to(es, normalized_value = round(cg.value.equivalent(prescription.nr_fractions)*100,0), ignore_identical=ignore_identical)
    else:
      # Missing ROI:
      GUIF.handle_missing_roi_for_clinical_goal(cg.name)


def setup_target(ss, es, prescription, cg):
  '''Sets up a target clinical goal before it is applied to an EvaluationSetup instance.

  Args:
    es (PyScriptObject): The RayStation EvaluationSetup instance (in which the clinical goal is to be created).
    prescription (Prescription): The Prescription instance for this beam set.
    cg (ClinicalGoal): The target clinical goal to be set up.
  '''
  # Make sure corresponding ROI exists before trying to create clinical goal:
  if SSF.has_roi(ss, cg.name):
    if cg.name in [ROIS.external.name, ROIS.igtv.name, ROIS.gtv.name] and cg.criteria == 'AtMost' and cg.tolerance != 5000:
      cg.apply_to(es, normalized_tolerance = round(cg.tolerance*prescription.total_dose*100,0))
    elif cg.name in [ROIS.ctv_sb.name, ROIS.ptv_sbc.name] and prescription.target != ROIS.ctv_sb.name or cg.tolerance == 5000 or cg.type == homogeneity_index:
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
