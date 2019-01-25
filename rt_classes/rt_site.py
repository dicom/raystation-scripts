# encoding: utf8

# NOTE: This file is named rt_site.py instead of site.py because of a file name conflict with the IronPython library!

# Contains information about region codes, clinical goals and OAR optimization objectives used for a given treatment site.
class Site(object):

    def __init__(self, codes, oar_objectives, opt_objectives, oar_clinical_goals, target_clinical_goals):
      self.codes = codes
      self.oar_objectives = oar_objectives
      self.opt_objectives = opt_objectives
      self.oar_clinical_goals = oar_clinical_goals
      self.target_clinical_goals = target_clinical_goals
