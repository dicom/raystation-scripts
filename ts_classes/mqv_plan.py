# encoding: utf8

# Contains tests for the treatment plan object.
#

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST


# This class contains tests for the RayStation TreatmentPlan object:
# (Note that contrary to all other test objects, the plan does not have any
# parent test obects, as it is on the top of the chain)
class MQVPlan(object):
  def __init__(self, patient, case, plan, mq_patient):
    # RayStation object:
    self.patient = patient
    self.case = case
    self.plan = plan
    self.mq_patient = mq_patient
    # Related test suite objects:
    self.mqv_beam_sets = []
    # Parameters:
    self.param = TEST.Parameter('Plan', plan.Name, None)
  