# encoding: utf8

# Import local files:
import gui_functions as GUIF
import objective_adaptation as OA
import objective_functions as OF
import rois as ROIS
import roi_functions as ROIF
import plan_functions as PF
import structure_set_functions as SSF
import raystation_utilities as RSU
import region_codes as RC

# Contains a collection of objective functions.


# Adapts the optimization of a beam set, aiming to achieve a mild sparing of the organs at risk in general.
# (Typically used in situations where we have an unknown geometry - .i.e. palliative situations)
# NOTE: In RayStation 12A, ConstituentFunctions (objectives) apparently may have multiple dose distributions
# (before they had just a single one). We choose to extract the first dose distribution, but there may
# occurs cases where this is wrong!
#
def adapt_optimization_oar(ss, plan, oar_list, region_code):
  for i, beam_set in enumerate(plan.BeamSets):
    objective_adaptations = []
    objective_adaptations = setup_objectives(ss, plan, oar_list, i, region_code)
    # Get OAR average doses of first optimization, and set the initial OAR target average dose as half of that value:
    for oa in objective_adaptations:
      if oa.roi.name == ROIS.spinal_canal.name:
        v = oa.objective.OfDoseDistributions[0].GetDoseAtRelativeVolumes(RoiName = oa.roi.name, RelativeVolumes = [0.02])
        oa.set_dose_high(v[0])
        oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * v[0]
      else:
        avg = oa.objective.OfDoseDistributions[0].GetDoseStatistic(RoiName = oa.roi.name, DoseType = 'Average')
        oa.set_dose_high(avg)
        oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * avg
    adaptive_optimization(plan, objective_adaptations)


# NOT IN USE YET (UNDER DEVELOPMENT).
def objective_adaptations(plan):
  objective_adaptations = []
  #o.FunctionValue < 1*10**-10
  for o in plan.PlanOptimizations[0].Objective.ConstituentFunctions:
    if o.FunctionValue.FunctionValue < 1*10**-10 and o.ForRegionOfInterest.Type == 'Organ':
      objective_adaptations.append(OA.ObjectiveAdaptation(o.ForRegionOfInterest.Name, o))

  for oa in objective_adaptations:
    if oa.roi == ROIS.spinal_canal.name:
      v = oa.objective.OfDoseDistributions[0].GetDoseAtRelativeVolumes(RoiName = oa.roi, RelativeVolumes = [0.02])
      oa.set_dose_high(v[0])
      oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * v[0]
    else:
      avg = oa.objective.OfDoseDistributions[0].GetDoseStatistic(RoiName = oa.roi, DoseType = 'Average')
      oa.set_dose_high(avg)
      oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * avg

  return objective_adaptations


# Runs optimization iterations until satisfactory optimization function values have been reached.
def adaptive_optimization(plan, objective_adaptations):
  for beam_set in plan.BeamSets:
    completed = False
    while (completed == False):
      # Get the plan optimization corresponding to the current beam set:
      po = RSU.plan_optimization(plan, beam_set)
      # Run a new optimization with the updated average dose criterias:
      #plan.PlanOptimizations[0].RunOptimization()
      po.RunOptimization()
      # Assume the goals are reached until proven otherwise:
      completed = True
      # Check each objective:
      for oa in objective_adaptations:
        # Continue adapting if target has not been reached, and the achieved dose is above 1 cGy:
        if oa.on_target() == False and oa.objective.DoseFunctionParameters.DoseLevel > 1:
          completed = False
          # Function value is either too high or too low:
          if oa.objective.FunctionValue.FunctionValue < oa.function_value_low:
            # Function value is too low: It is possible to reduce dose further:
            oa.nr_dose_reductions += 1
            oa.nr_dose_increases = 0
            oa.set_dose_high(0.5 * (oa.dose_low + oa.dose_high))
            # After new high limit has been set, the target function value should be between low and high limit:
            oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * (oa.dose_low + oa.dose_high)
          elif oa.objective.FunctionValue.FunctionValue > oa.function_value_high:
            # Function value is too high: We were too aggressive, dose limit must be increased:
            oa.nr_dose_increases += 1
            oa.nr_dose_reductions = 0
            oa.set_dose_low(oa.objective.DoseFunctionParameters.DoseLevel)
            # After new low limit has been set, the target function value should be between low and high limit:
            oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * (oa.dose_low + oa.dose_high)


# NOT IN USE YET (UNDER DEVELOPMENT).
def adaptive_optimization_with_calculation(plan, beam_set, objective_adaptations):
  # Run optimization iterations until satisfactory optimization function values have been reached:
  completed = False
  while (completed == False):
    # Run a new optimization with the updated average dose criterias:
    plan.PlanOptimizations[0].RunOptimization()
    beam_set.ComputeDose(DoseAlgorithm = 'CCDose')
    # Assume the goals are reached until proven otherwise:
    completed = True
    # Check each objective:
    for oa in objective_adaptations:
      # Continue adapting if target has not been reached, and the achieved dose is above 1 cGy:
      if oa.on_target() == False and oa.objective.DoseFunctionParameters.DoseLevel > 1:
        completed = False
        # Function value is either too high or too low:
        if oa.objective.FunctionValue.FunctionValue < oa.function_value_low:
          # Function value is too low: It is possible to reduce dose further:
          oa.nr_dose_reductions += 1
          oa.set_dose_high(0.5 * (oa.dose_low + oa.dose_high))
          # After new high limit has been set, the target function value should be between low and high limit:
          oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * (oa.dose_low + oa.dose_high)
        elif oa.objective.FunctionValue.FunctionValue > oa.function_value_high:
          # Function value is too high: We were too aggressive, dose limit must be increased:
          oa.nr_dose_reductions = 0
          oa.set_dose_low(oa.objective.DoseFunctionParameters.DoseLevel)
          # After new low limit has been set, the target function value should be between low and high limit:
          oa.objective.DoseFunctionParameters.DoseLevel = 0.5 * (oa.dose_low + oa.dose_high)


# Create optimization objects, minimum dvh, with robustness
def fall_off(ss, plan, roi_name, high_dose_level, low_dose_level, distance, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="DoseFallOff", RoiName = roi_name)
    o.DoseFunctionParameters.HighDoseLevel = high_dose_level
    o.DoseFunctionParameters.LowDoseLevel = low_dose_level
    o.DoseFunctionParameters.LowDoseDistance = distance
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, maximum dose
def max_dose(ss, plan, roi_name, dose_level, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MaxDose", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, maximum dvh
def max_dvh(ss, plan, roi_name, dose_level, percent_volume, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MaxDvh", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.PercentVolume = percent_volume
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, maximum eud
def max_eud(ss, plan, roi_name, dose_level, eud_parameter, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MaxEud", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.EudParameterA =  eud_parameter
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, minimum dose
def min_dose(ss, plan, roi_name, dose_level, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MinDose", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, minimum dvh
def min_dvh(ss, plan, roi_name, dose_level, percent_volume, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MinDvh", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.PercentVolume = percent_volume
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, minimum dvh, with robustness
def min_dvh_robust(ss, plan, roi_name, dose_level, percent_volume, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MinDvh", RoiName = roi_name, IsRobust = True)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.PercentVolume = percent_volume
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Create optimization objects, minimum eud
def min_eud(ss, plan, roi_name, dose_level, eud_parameter, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="MinEud", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.EudParameterA = eud_parameter
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# FIXME: Bør vurdere å gi denn et generelt navn for å sette robustness verdier,
# og flytte innstillingsbiten av koden til en separat fil i "settings" mappen.
# Sets robustness parameters for vmat breast plans.
def set_robustness_breast(plan, region_code):
  if region_code in [240, 242, 244]:
    plan.PlanOptimizations[0].OptimizationParameters.SaveRobustnessParameters(
      PositionUncertaintyAnterior=1,
      PositionUncertaintyPosterior=0,
      PositionUncertaintySuperior=0,
      PositionUncertaintyInferior=0,
      PositionUncertaintyLeft=0,
      PositionUncertaintyRight=1,
      DensityUncertainty=0,
      PositionUncertaintySetting='Universal',
      IndependentLeftRight = True,
      IndependentAnteriorPosterior = True,
      IndependentSuperiorInferior = True,
      ComputeExactScenarioDoses=False,
      NamesOfNonPlanningExaminations=[]
    )
  elif region_code in [239, 241, 243]:
    plan.PlanOptimizations[0].OptimizationParameters.SaveRobustnessParameters(
      PositionUncertaintyAnterior=1,
      PositionUncertaintyPosterior=0,
      PositionUncertaintySuperior=0,
      PositionUncertaintyInferior=0,
      PositionUncertaintyLeft=1,
      PositionUncertaintyRight=0,
      DensityUncertainty=0,
      PositionUncertaintySetting='Universal',
      IndependentLeftRight = True,
      IndependentAnteriorPosterior = True,
      IndependentSuperiorInferior = True,
      ComputeExactScenarioDoses=False,
      NamesOfNonPlanningExaminations=[]
    )


# Create optimization object: uniform dose
def uniform_dose(ss, plan, roi_name, dose_level, weigth, beam_set_index=0):
  if SSF.has_named_roi_with_contours(ss, roi_name):
    po = plan.PlanOptimizations[beam_set_index]
    o = po.AddOptimizationFunction(FunctionType="UniformDose", RoiName = roi_name)
    o.DoseFunctionParameters.DoseLevel = dose_level
    o.DoseFunctionParameters.Weight = weigth
    return o
  else:
    GUIF.handle_missing_roi_for_objective(roi_name)


# Creates optimization objectives and objective adapation objects.
def setup_objectives(ss, plan, rois, beam_set_index, region_code):
  dose = 10000
  weight = 2
  eud = 1
  percent_volume = 2
  adaptations = []
  objective = None
  for roi in rois:
    if roi.name == ROIS.spinal_canal.name and region_code not in RC.palliative_columna_codes:
      objective = max_dvh(ss, plan, roi.name, dose, percent_volume, weight, beam_set_index=beam_set_index)
    elif roi.name != ROIS.spinal_canal.name:
      objective = max_eud(ss, plan, roi.name, dose, eud, weight, beam_set_index=beam_set_index)

    if objective:
      adaptations.append(OA.ObjectiveAdaptation(roi, objective))
  return adaptations

