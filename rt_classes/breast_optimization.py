# encoding: utf8

# Import local files:
import gui_functions as GUIF
import optimization as OPT
import region_codes as RC

# Import system files:
import datetime


# Optimization class for Breast optimization.
class BreastOptimization(object):

  # Creates a BreastOptimization object.
  # Sets up objects associated with the Optimization:
  # -Structure set
  # -Plan
  # -Site
  # -Region code
  def __init__(self, ss, plan, site, region_code):
    # Verify input:
    #assert isinstance(choices, list), "choices is not a list: %r" % choices
    # Assign parameters:
    self.ss = ss
    self.plan = plan
    self.site = site
    self.region_code = region_code
  

  # Executes the optimization.
  def optimize(self):
    # Iterate plan optimization(s):
    for po in self.plan.PlanOptimizations:
      # Log start time:
      time_start = datetime.datetime.now()
      nr_reduction_iterations = 0
      nr_target_iterations = 0
      # Extract objectives in 3 categories:
      external_objectives = []
      organ_objectives = []
      target_objectives = []
      for objective in po.Objective.ConstituentFunctions:
        if objective.ForRegionOfInterest.Type in ['External']:
          external_objectives.append(objective)
        elif objective.ForRegionOfInterest.Type in ['Organ']:
          organ_objectives.append(objective)
        elif objective.ForRegionOfInterest.Type in ['Gtv', 'Ctv', 'Ptv']:
          target_objectives.append(objective)   
      # Configure optimization settings:
      optimization_parameters = OPT.sliding_window
      optimization_parameters.apply_to(po)
      # Perform first optimization phase (initial optimization):
      # (Optimization may crash if e.g. GPU for computation is not available)
      try:
        po.RunOptimization()
      except Exception as e:
        GUIF.handle_optimization_error(po, e)
      # Perform second optimization phase: Reduction of OAR doses until target_objectives are compromised:
      if self.has_objective_with_positive_dose_and_further_dose_reduction_potential(organ_objectives):
        nr_reduction_iterations = self.reduce_organ_doses(po, organ_objectives, target_objectives, counter=1)
      # Preparation for third phase:
      # Set robustness (except for boost plans):
      # (since apparently the PlanOptimization script objects cannot be compared directly, we compare their related beam set numbers instead to establish equality)
      if po.OptimizedBeamSets[0].Number == self.plan.PlanOptimizations[0].OptimizedBeamSets[0].Number:
        # Set robustness settings:
        if self.region_code in RC.breast_r_codes:
          # Right:
          po.OptimizationParameters.SaveRobustnessParameters(PositionUncertaintyAnterior=1, PositionUncertaintyPosterior=0, PositionUncertaintySuperior=0, PositionUncertaintyInferior=0, PositionUncertaintyLeft=0, PositionUncertaintyRight=1, DensityUncertainty=0, PositionUncertaintySetting="Universal", IndependentLeftRight=True, IndependentAnteriorPosterior=True, IndependentSuperiorInferior=True, ComputeExactScenarioDoses=False, NamesOfNonPlanningExaminations=[], PatientGeometryUncertaintyType="PerTreatmentCourse", PositionUncertaintyType="PerTreatmentCourse", TreatmentCourseScenariosFactor=1000)
        elif self.region_code in RC.breast_l_codes:
          # Left:
          po.OptimizationParameters.SaveRobustnessParameters(PositionUncertaintyAnterior=1, PositionUncertaintyPosterior=0, PositionUncertaintySuperior=0, PositionUncertaintyInferior=0, PositionUncertaintyLeft=1, PositionUncertaintyRight=0, DensityUncertainty=0, PositionUncertaintySetting="Universal", IndependentLeftRight=True, IndependentAnteriorPosterior=True, IndependentSuperiorInferior=True, ComputeExactScenarioDoses=False, NamesOfNonPlanningExaminations=[], PatientGeometryUncertaintyType="PerTreatmentCourse", PositionUncertaintyType="PerTreatmentCourse", TreatmentCourseScenariosFactor=1000)
        # Set robustness for PTV min & max dose:
        for obj in target_objectives:
          if self.region_code in RC.breast_whole_codes:
            if obj.ForRegionOfInterest.Type == 'Ptv':
              obj.UseRobustness = True
          elif self.region_code in RC.breast_reg_codes:
            if obj.ForRegionOfInterest.Name == 'PTVpc':
              obj.UseRobustness = True
      # Proceed to third opimization phase: Increase weights for targets to fullfil target clincal goals.
      if self.has_target_with_unfulfilled_coverage(po.OptimizedBeamSets[0], target_objectives):
        nr_target_iterations = self.improve_target_doses(po, target_objectives, external_objectives, counter=1)
      # Log nr of iterations:
      optimization_comment = "OAR-iterasjoner: " + str(nr_reduction_iterations) + "\n"
      optimization_comment += "MV-iterasjoner: " + str(nr_target_iterations) + "\n"
      # Log finish time:
      time_end = datetime.datetime.now()
      elapsed_time = time_end - time_start
      minutes = elapsed_time.seconds // 60 % 60
      seconds = elapsed_time.seconds - minutes * 60
      optimization_comment += "Tidsbruk: " + str(minutes) + " min " + str(seconds) + " sek"
      po.OptimizedBeamSets[0].Comment = optimization_comment

  # Calculates the coverage of the objective, and determines if the coverage is fulfilled or not (based on criteria for CTV/PTV).
  # Returns True if coverage is fulfilled, False if not.
  # Note that for objectives which are not evaluated (e.q. Dose fall-off), True is returned.
  def fulfilled_coverage(self, beam_set, objective, high_ptv_coverage):
    prescription = beam_set.Prescription.PrimaryDosePrescription.DoseValue
    result = False
    # Criteria:
    # CTV min dose: 98% > 38.05 (95%)
    # PTV min dose: 98% > 36.04 (90%)
    # PTV max dose: 2% < 42.05 (105%)
    # CTV uniform dose: 39.85 < 50% < 40.25 (49.5% & 50.5 %)
    # PTV low pri: 98% > 38.05 (95%) - not considered at the moment!
    # Note that Dose fall-off objectives doesnt have the "FunctionType" parameter defined.
    # Dose fall-off will anyway not be evaluated for fulfilled status.
    # Test for the presence of this attribute:
    if hasattr(objective.DoseFunctionParameters, 'FunctionType'):
      if objective.DoseFunctionParameters.FunctionType == 'UniformDose':
        d50 = beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = objective.ForRegionOfInterest.Name, RelativeVolumes = [0.50])[0] * beam_set.FractionationPattern.NumberOfFractions
        if prescription * 0.995 <= d50 <= prescription * 1.005:
          result = True
      elif objective.DoseFunctionParameters.FunctionType == 'MinDose':
        d98 = beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = objective.ForRegionOfInterest.Name, RelativeVolumes = [0.98])[0] * beam_set.FractionationPattern.NumberOfFractions
        if objective.ForRegionOfInterest.Type == 'Ctv':
          if d98 > prescription * 0.95:
            result = True
        elif objective.ForRegionOfInterest.Type == 'Ptv':
          if high_ptv_coverage:
            if d98 > prescription * 0.95:
              result = True
          else:
            if d98 > prescription * 0.90:
              result = True
      elif objective.DoseFunctionParameters.FunctionType == 'MaxDose':
        d2 = beam_set.FractionDose.GetDoseAtRelativeVolumes(RoiName = objective.ForRegionOfInterest.Name, RelativeVolumes = [0.02])[0] * beam_set.FractionationPattern.NumberOfFractions
        if d2 < prescription * 1.05:
          result = True
    else:
      # Objective not evaluated (e.g. Dose Fall-off). Set result as True for this scenario.
      result = True
    return result
  
  # Checks if there is at least one target with a unfulfilled target coverage.
  # Returns True if at least one is unfulfilled, False if all are fulfilled.
  def has_target_with_unfulfilled_coverage(self, beam_set, objectives):
    result = False
    for obj in objectives:
      if not self.fulfilled_coverage(beam_set, obj, high_ptv_coverage=True):
        result = True
    return result
  
  # Checks if the given list of objectives contains at least one objective
  # with function value which is less than the predefined threshold of "resistance".
  # Returns True if so, False if not.
  def has_objective_with_positive_dose_and_further_dose_reduction_potential(self, objectives):
    threshold = 0.0001
    result = False
    for obj in objectives:
      if hasattr(obj.DoseFunctionParameters, 'DoseLevel'):
        # Is set dose greater or equal to 0.01 Gy (1 cGy)?
        if obj.DoseFunctionParameters.DoseLevel >= 1:
          if obj.FunctionValue.FunctionValue < threshold:
            result = True
    return result
  
  # Checks if the given list of objectives contains at least one objective with a zero function value.
  # Note that objectives are only evaluated if they contain a meaningful positive set dose (i.e. >= 0.01 Gy).
  # Returns True if so, False if all are positive.
  def has_objective_with_positive_dose_and_zero_function_value(self, objectives):
    result = False
    for obj in objectives:
      if hasattr(obj.DoseFunctionParameters, 'DoseLevel'):
        # Is set dose greater or equal to 0.01 Gy (1 cGy)?
        if obj.DoseFunctionParameters.DoseLevel >= 1:
          if obj.FunctionValue.FunctionValue == 0:
            result = True
    return result
  
  # Improves target doses (min, max and uniform dose) by increasing target objective weights.
  # Runs recursively until all target dose clinical goals are fullfilled.
  def improve_target_doses(self, po, target_objectives, external_objectives, counter):
    # Adjustment settings:
    weight_factors = []
    weight_factor = 1.7
    min_weight_factor = 1.5
    max_weight_factor = 40
    # Determine the gap in min dose between desired and achieved dose:
    dose_gap = 0
    for obj in target_objectives:
      # Get PTV D98 (min) dose:
      if obj.DoseFunctionParameters.FunctionType == 'MinDose' and obj.ForRegionOfInterest.Type == 'Ptv':
        achieved_d98 = po.OptimizedBeamSets[0].FractionDose.GetDoseAtRelativeVolumes(RoiName = obj.ForRegionOfInterest.Name, RelativeVolumes = [0.98])[0] * po.OptimizedBeamSets[0].FractionationPattern.NumberOfFractions
        desired_d98 = po.OptimizedBeamSets[0].Prescription.PrimaryDosePrescription.DoseValue * 0.95
        dose_gap = desired_d98 - achieved_d98 # (cGy)
        # Determine a weight factor dynamically based on the observed dose gap:
        computed_weight_factor = dose_gap * 0.01 * 30
        # Make sure the weight factor is within our set min and max limits (to avoid extreme values):
        weight_factors.append(sorted([min_weight_factor, computed_weight_factor, max_weight_factor])[1])
    weight_factor = max(weight_factors)
    # Iterate target and external objectives:
    for obj in target_objectives + external_objectives:
      # Increase all target & external objective weights:
      obj.DoseFunctionParameters.Weight = round(obj.DoseFunctionParameters.Weight * weight_factor)
    # Keep an extra eye on the Lung DVH requirement, and adjust weight of ipsilateral lung objective if necessary:
    lung_dose_level = 1800 / 15
    if po.OptimizedBeamSets[0].Prescription.PrimaryDosePrescription == 2600:
      lung_dose_level = 800 / 5
    # For whole breast or regional breast we use an extra lung DVH objective:
    if self.region_code in RC.breast_whole_codes or self.region_code in RC.breast_reg_codes:
      ipsilateral_lung = 'Lung_L'
      if self.region_code in RC.breast_r_codes:
        ipsilateral_lung = 'Lung_R'
      # Threshold depends on if we have a whole breast or regional breast case:
      if self.region_code in RC.breast_whole_codes:
        lung_threshold = 0.146
      elif self.region_code in RC.breast_reg_codes:
        lung_threshold = 0.34
      ipsilateral_lung_relative_volume = po.OptimizedBeamSets[0].FractionDose.GetRelativeVolumeAtDoseValues(RoiName = ipsilateral_lung, DoseValues = [lung_dose_level])[0]
      # Do we need extra weight on the lung objective?
      if ipsilateral_lung_relative_volume > lung_threshold:
        # Increase weight of lung objective to avoid the lung dose going above tolerance:
        for obj in po.Objective.ConstituentFunctions:
          if hasattr(obj.DoseFunctionParameters, 'FunctionType'):
            if obj.ForRegionOfInterest.Name == ipsilateral_lung and obj.DoseFunctionParameters.FunctionType == 'MaxDvh':
              obj.DoseFunctionParameters.Weight = round(obj.DoseFunctionParameters.Weight * weight_factor * 2)
    # Adjustments have been made. Proceed with new optimization:
    po.RunOptimization()
    # If counter is below threshold, and some target objectives are still unfulfilled, repeat target dose escalation:
    if counter < 15 and self.has_target_with_unfulfilled_coverage(po.OptimizedBeamSets[0], target_objectives):
      counter += 1
      counter = self.improve_target_doses(po, target_objectives, external_objectives, counter)
    return counter

  # Reduces organ doses by making OAR objectives more strict.
  # Runs recursively until all target min dose clinical goals are violated.
  #def reduce_organ_doses(self, po, organ_objectives, target_min_clinical_goals):
  def reduce_organ_doses(self, po, organ_objectives, target_objectives, counter):
    # Adjustment settings:
    set_dose_factor_for_zero_f_value = 0.6
    set_dose_factor_for_positive_f_value = 0.7
    threshold = 0.0001
    # Is any of the function values zero?
    if self.has_objective_with_positive_dose_and_zero_function_value(organ_objectives):
      # Iterate objectives:
      for obj in organ_objectives:
        # Reduce target dose for the objectives with zero function value:
        if obj.FunctionValue.FunctionValue == 0:
          # New set dose values:
          obj.DoseFunctionParameters.DoseLevel = obj.DoseFunctionParameters.DoseLevel * set_dose_factor_for_zero_f_value
    else:
      # Iterate objectives:
      for obj in organ_objectives:
        # Reduce target dose for the objectives with function value less than threshold:
        if obj.FunctionValue.FunctionValue < threshold:
          # New set dose values:
          obj.DoseFunctionParameters.DoseLevel = obj.DoseFunctionParameters.DoseLevel * set_dose_factor_for_positive_f_value
    # Adjustments have been made. Proceed with new optimization:
    po.RunOptimization()
    # If some target min dose objectives are still fulfilled, repeat organ dose reduction:
    if self.has_objective_with_positive_dose_and_further_dose_reduction_potential(organ_objectives):
      counter += 1
      counter = self.reduce_organ_doses(po, organ_objectives, target_objectives, counter)
    return counter
 