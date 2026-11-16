# Import system files:
import datetime

# Import local files:
import gui_functions as GUIF
import objective_functions as OBJF
import optimization as OPT
import region_codes as RC


class General(object):
  '''Optimizer class for general cases (e.g. it can handle a variety of palliative sites).'''

  def __init__(self, ss, plan, site, prescription, adaptive_optimization=False):
    '''Initializes the general optimizer with the relevant treatment planning instances.

    Args:
      ss (PyScriptObject): The RayStation StructureSet instance.
      plan (PyScriptObject): The RayStation TreatmentPlan instance.
      site (Site): A Site instance containing region codes, objectives and clinical goals.
      prescription (Prescription): A prescription instance containing dose information.
      adaptive_optimization (bool): If true performs adaptive optimization
        (automatically adjust objectives towards a specific function value).
    '''
    # Assign parameters:
    self.ss = ss
    self.plan = plan
    self.site = site
    self.prescription = prescription
    self.adaptive_optimization = adaptive_optimization

  def optimize(self):
    '''Performs plan optimization.'''
    # Run first optimization on each beam set:
    for plan_optimization in self.plan.PlanOptimizations:
      plan_optimization.OptimizationParameters.DoseCalculation.ComputeFinalDose = True
      # Configure optimization parameters for VMAT only:
      if "Arc" in plan_optimization.OptimizedBeamSets[0].DeliveryTechnique:
        optimization_parameters = OPT.optimization_parameters(self.prescription)
        optimization_parameters.apply_to(plan_optimization)
      # Run the optimization:
      # Some typical causes of optimization exceptions:
      # (Optimization may crash if e.g. GPU for computation is not available, or if max arc delivery time is too low for this target volume)
      # On exceptions, assume we may have a beam delivery time error:
      possible_beam_delivery_time_error = True
      while possible_beam_delivery_time_error:
        try:
          plan_optimization.RunOptimization()
          # Optimization succeeded, thus there is no time error:
          possible_beam_delivery_time_error = False
        except Exception as e:
          if "is shorter than the minimum feasible time" in e.args[0] or "The selected maximum beam delivery time of" in e.args[0]:
            # We need to increase the beam delivery time (and try the optimization again). Increase by 10 seconds:
            for beam in plan_optimization.OptimizationParameters.TreatmentSetupSettings[0].BeamSettings:
              beam.ArcConversionPropertiesPerBeam.MaxArcDeliveryTime += 10
          else:
            # Although it did crash, it wasn't because of the delivery time error:
            possible_beam_delivery_time_error = False
            GUIF.handle_optimization_error(plan_optimization, e)
    # Start adaptive optimization if indicated:
    if self.adaptive_optimization:
      try:
        OBJF.adapt_optimization_oar(self.ss, self.plan, self.site.oar_objectives, self.prescription.region_code)
      except Exception as e:
        GUIF.handle_optimization_error(plan_optimization, e)
