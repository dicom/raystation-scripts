# Import system files:
import datetime

# Import local files:
import gui_functions as GUIF
import objective_functions as OBJF
import optimization as OPT


class Bladder(object):
  '''An optimizer class for bladder cases.'''

  def __init__(self, ss, plan, site, prescription):
    '''Initializes the bladder optimizer with the relevant treatment planning instances.

    Args:
      ss (PyScriptObject): The RayStation StructureSet instance.
      plan (PyScriptObject): The RayStation TreatmentPlan instance.
      site (Site): A Site instance containing region codes, objectives and clinical goals.
      prescription (Prescription): A prescription instance containing dose information.
    '''
    # Assign parameters:
    self.ss = ss
    self.plan = plan
    self.site = site
    self.prescription = prescription

  def configure_optimization(self, po):
    '''Configures the optimization setings.

    Args:
      po (PyScriptObject): The RayStation PlanOptimization instance.
    '''
    # Optimization parameters:
    optimization_parameters = OPT.optimization_parameters(self.prescription)
    optimization_parameters.apply_to(po)

  def optimize(self):
    '''Performs plan optimization.'''
    # Iterate plan optimization(s):
    for po in self.plan.PlanOptimizations:
      self.optimize_beam_set(po)

  def log_information(self, po, time_start):
    '''Logs execution information.

    Args:
      po (PyScriptObject): The RayStation PlanOptimization instance.
      time_start (datetime): The time when we started the optimization.
    '''
    time_end = datetime.datetime.now()
    elapsed_time = time_end - time_start
    if elapsed_time.seconds > 3600:
      hours = elapsed_time.seconds // 3600 % 3600
      minutes = (elapsed_time.seconds - hours * 3600) // 60 % 60
      seconds = elapsed_time.seconds - hours * 3600 - minutes * 60
    else:
      hours = 0
      minutes = elapsed_time.seconds // 60 % 60
      seconds = elapsed_time.seconds - minutes * 60
    if hours > 0:
      optimization_comment = "Tidsbruk: " +str(hours) + " time(r) " + str(minutes) + " min " + str(seconds) + " sek"
    else:
      optimization_comment = "Tidsbruk: " + str(minutes) + " min " + str(seconds) + " sek"
    po.OptimizedBeamSets[0].Comment = optimization_comment

  def optimize_beam_set(self, po):
    '''Performs beam set optimization.
    
    Args:
      po (PyScriptObject): The RayStation PlanOptimization instance.
    '''
    # Log start time:
    time_start = datetime.datetime.now()
    # Configure optimization settings:
    self.configure_optimization(po)
    # Perform a single optimization:
    self.run_first_optimization(po)
    # Adaptive OAR optimization:
    OBJF.adapt_optimization_oar(self.ss, self.plan, self.site.oar_objectives, self.prescription.region_code)
    # Log execution information:
    self.log_information(po, time_start)

  def run_first_optimization(self, po):
    '''Performs initial optimization (first optimization phase).

    Note that optimization may crash if e.g. GPU for computation is not available,
    or if max arc delivery time is too low for this target volume.
    
    Args:
      po (PyScriptObject): The RayStation PlanOptimization instance.
    '''
    # Assume we may have a beam delivery time error:
    possible_beam_delivery_time_error = True
    while possible_beam_delivery_time_error:
      try:
        po.RunOptimization()
        # Optimization succeeded, thus there is no time error:
        possible_beam_delivery_time_error = False
      except Exception as e:
        if "is shorter than the minimum feasible time" in e.args[0] or "The selected maximum beam delivery time of" in e.args[0]:
          # We need to increase the beam delivery time (and try the optimization again). Increase by 10 seconds:
          for beam in po.OptimizationParameters.TreatmentSetupSettings[0].BeamSettings:
            beam.ArcConversionPropertiesPerBeam.MaxArcDeliveryTime += 10
        else:
          # Although it did crash, it wasnt because of the time error:
          possible_beam_delivery_time_error = False
          GUIF.handle_optimization_error(po, e)
