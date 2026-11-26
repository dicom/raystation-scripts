'''Contains the Site class which holds parameters for configuring a plan optimization.

Note that this file was originally named rt_site.py instead of site.py because of
a file name conflict with the IronPython library.
'''


class Site(object):
  '''Contains relevant information for plan optimization.'''

  def __init__(self, codes, oar_objectives, opt_objectives, oar_clinical_goals, target_clinical_goals):
    '''Initializes the Site instance with the relevant parameters.

    Args:
      codes (list[int]): A list of region codes relevant for the site.
      oar_objectives (list[PyScriptObject]): A list of organ at risk objectives (ConstituentFunction instances).
      opt_objectives (list[PyScriptObject]): A list of target objectives (ConstituentFunction instances).
      oar_clinical_goals (list[ClinicalGoal]): A list of organ at risk clinical goals
        (which will eventually be turned into EvaluationFunction instances).
      target_clinical_goals (list[ClinicalGoal]): A list of target clinical goals
        (which will eventually be turned into EvaluationFunction instances).
    '''
    self.codes = codes
    self.oar_objectives = oar_objectives
    self.opt_objectives = opt_objectives
    self.oar_clinical_goals = oar_clinical_goals
    self.target_clinical_goals = target_clinical_goals
    self.optimizer = None

  def optimize(self):
    '''Performs plan optimization for this site.'''
    self.optimizer.optimize()
