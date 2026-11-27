'''Contains the Optimization class, used for configuring an optimization in RayStation.

Also contains a collection of default optimization settings for various sites,
and a function for selecting an appropriate Optimization instance based on a
given prescription.
'''

# Import local files:
import region_codes as RC


# Optimization parameters class - for setting up an optimization in RayStation.
class Optimization(object):
  '''Handles the configuration of optimization parameters.'''

  def __init__(self,
    max_number_of_iterations=40,
    optimality_tolerance=0.000001,
    compute_final_dose=True,
    compute_intermediate_dose=False,
    iterations_in_preparations_phase=7,
    final_arc_gantry_spacing=4,
    max_arc_delivery_time=90,
    max_leaf_travel_distance_per_degree=0,
    use_max_leaf_travel_distance_per_degree=False,
    use_sliding_window_sequencing=False
  ):
    '''Initializes the Optimization instance.

    Args:
      max_number_of_iterations (int): The maximum number of optimization iterations.
        Defaults to 40.
      optimality_tolerance (float): The tolerance of optimality.
        Defaults to 0.000001.
      compute_final_dose (bool): Whether to compute final (accurate) dose (True).
        Defaults to True.
      compute_intermediate_dose (bool): Whether to compute intermediate (accurate) dose (True).
        Defaults to False.
      iterations_in_preparations_phase (int): Number of optimization iterations
        to perform before conversion to segments.
      final_arc_gantry_spacing (int): Gantry angle between neighbouring segments.
        Defaults to 4.
      max_arc_delivery_time (int): The maximum delivery time (in seconds) for an arc.
        Defaults to 90.
      max_leaf_travel_distance_per_degree (float): The maximum leaf travel distance per degree (cm/deg).
        Defaults to 0.
      use_max_leaf_travel_distance_per_degree (bool): Specifies whether to use
        maximum leaf travel distance per degree (True). Defaults to False.
      use_sliding_window_sequencing (bool): If True the VMAT arc is converted
        using sliding window leaf sequencing. Defaults to False.
    '''
    self.max_number_of_iterations = max_number_of_iterations
    self.optimality_tolerance = optimality_tolerance
    self.compute_final_dose = compute_final_dose
    self.compute_intermediate_dose = compute_intermediate_dose
    self.iterations_in_preparations_phase = iterations_in_preparations_phase
    self.final_arc_gantry_spacing = final_arc_gantry_spacing
    self.max_arc_delivery_time = max_arc_delivery_time
    self.max_leaf_travel_distance_per_degree = max_leaf_travel_distance_per_degree
    self.use_max_leaf_travel_distance_per_degree = use_max_leaf_travel_distance_per_degree
    self.use_sliding_window_sequencing = use_sliding_window_sequencing
    self.max_arc_mu = None

  def apply_to(self, plan_optimization):
    '''Applies the parameters of this Optimization instance to a RayStation PlanOptimization instance.

    Args:
      plan_optimization (PyScriptObject]): A RayStation PlanOptimization instance.
    '''
    assert hasattr(plan_optimization, 'OptimizationParameters'), 'plan_optimization lacks OptimizationParameters'
    assert len(plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].BeamSettings) > 0, "plan_optimization.OptimizationParameters.TreatmentSetupSettings[0] does not contain any BeamSettings"
    plan_optimization.OptimizationParameters.Algorithm.MaxNumberOfIterations = self.max_number_of_iterations
    plan_optimization.OptimizationParameters.Algorithm.OptimalityTolerance = self.optimality_tolerance
    plan_optimization.OptimizationParameters.DoseCalculation.ComputeFinalDose = self.compute_final_dose
    plan_optimization.OptimizationParameters.DoseCalculation.ComputeIntermediateDose = self.compute_intermediate_dose
    plan_optimization.OptimizationParameters.DoseCalculation.IterationsInPreparationsPhase = self.iterations_in_preparations_phase
    for beam in plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].BeamSettings:
      beam.ArcConversionPropertiesPerBeam.FinalArcGantrySpacing = self.final_arc_gantry_spacing
      beam.ArcConversionPropertiesPerBeam.MaxArcDeliveryTime = self.max_arc_delivery_time
      beam.ArcConversionPropertiesPerBeam.MaxArcMU = self.max_arc_mu
    plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties.MaxLeafTravelDistancePerDegree = self.max_leaf_travel_distance_per_degree
    plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties.UseMaxLeafTravelDistancePerDegree = self.use_max_leaf_travel_distance_per_degree
    plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].SegmentConversion.ArcConversionProperties.UseSlidingWindowSequencing = self.use_sliding_window_sequencing

  def set_max_arc_mu(self, mu):
    '''Sets the max arc mu parameter.

    Args:
      mu (float]): Maximum total MU for the arc.
    '''
    self.max_arc_mu = mu


# A collection of default optimization settings used for various treatment sites:
default = Optimization()
sliding_window = Optimization(final_arc_gantry_spacing=2, max_arc_delivery_time=120, use_sliding_window_sequencing=True)
sliding_window_quick = Optimization(final_arc_gantry_spacing=2, max_arc_delivery_time=70, use_sliding_window_sequencing=True)
sbrt = Optimization(final_arc_gantry_spacing=2, max_arc_delivery_time=150, use_sliding_window_sequencing=True)


def optimization_parameters(prescription):
  '''Sets up optimization parameters, based on region code (i.e. treatment site)
  and fraction dose (i.e. conventionally fractionated radiotherapy or SBRT).

  Args:
    prescription (Prescription]): A Prescription instance.

  Returns:
    Optimization: The Optimization instance chosen for the given prescription (case).
  '''
  # Set the default optimization settings:
  opt = default
  # Assign alternative optimization settings based on region code (and in some cases fraction dose):
  if prescription.region_code in RC.brain_partial_codes:
    # Partial brain:
    if prescription.is_stereotactic():
      # Stereotactic brain
      opt = sbrt
    else:
      # Partial brain (ordinary fractionation):
      opt = sliding_window_quick
  elif prescription.region_code in RC.brain_whole_codes:
    # Whole brain:
    opt = sliding_window_quick
  elif prescription.region_code in RC.breast_codes:
    if prescription.region_code in RC.breast_reg_codes:
      # Regional breast:
      opt = sliding_window
    else:
      # Non-regional breast:
      opt = sliding_window_quick
  elif prescription.region_code in RC.lung_and_mediastinum_codes:
    # Lung:
    if prescription.is_stereotactic():
      # Stereotactic lung:
      opt = sbrt
      opt.max_arc_delivery_time = max(prescription.fraction_dose * 12, 100)
    else:
      # Conventional lung:
      opt = sliding_window_quick
  elif prescription.region_code in RC.prostate_codes:
    # Prostate:
    if prescription.region_code not in RC.prostate_node_codes:
      # "Simple" prostate cases:
      opt = sliding_window_quick
    else:
      # "Complex" prostate/bed cases:
      opt = sliding_window
  elif prescription.region_code in RC.rectum_codes:
    # Rectum:
    opt = sliding_window
  elif prescription.region_code in RC.palliative_codes:
    # Palliative treatment:
    if prescription.is_stereotactic():
      # Stereotactic palliative:
      opt = sbrt
    else:
      # Conventional palliative:
      if prescription.region_code in RC.whole_pelvis_codes:
        opt = sliding_window_quick
  # Set max number of monitor units (for all non-sbrt optimizations):
  if opt != sbrt:
    opt.set_max_arc_mu(prescription.fraction_dose * 300)
  # Return the assigned optimization settings:
  return opt
