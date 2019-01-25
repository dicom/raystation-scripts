# encoding: utf8

# Class used for setting up an adaptive, dynamic optimization.
class ObjectiveAdaptation(object):

  def __init__(self, roi, objective):
    self.roi = roi
    self.objective = objective # ConstituentFunction
    self.dose_high = None
    self.dose_low = 0
    self.nr_dose_increases = 0 # (number of consequtive dose increases)
    self.nr_dose_reductions = 0 # (number of consequtive dose reductions)
    self.function_value_high = 5 * 10**-5
    self.function_value_low = 10**-5


  # Indicates whether the adaptation is on target.
  # Returns true if the objective function value is between the defined low and high limits,
  # or if the maximum number of consequtive dose reductions have been reached.
  # (This is done to avoid iterating infinitely for OARs which are located far from the target)
  def on_target(self):
    if self.objective.FunctionValue:
      if self.function_value_low <= self.objective.FunctionValue.FunctionValue <= self.function_value_high or self.nr_dose_reductions >= 5 or self.nr_dose_increases >= 5:
        return True
      else:
        return False


  # Sets the high dose limit.
  def set_dose_high(self, value):
    self.dose_high = value


  # Sets the low dose limit.
  def set_dose_low(self, value):
    self.dose_low = value
