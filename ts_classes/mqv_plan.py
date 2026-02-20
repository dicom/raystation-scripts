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
    self.patient = TEST.Parameter('Patient', self.patient.Name, self.param)
    self.case_param = TEST.Parameter('Case', self.case.CaseName, self.param)
  
  
  # Checks that a matching patient has been found in Mosaiq.
  def test_matching_patient(self):
    t = TEST.Test("Skal finnes matchende pasient i Mosaiq.", self.patient.value, self.patient)
    if self.mq_patient:
      return t.succeed()
    else:
      return t.fail()
  
  # Checks that this case doesnt contain any other unapproved treatment plans.
  # At this stage, only approved treatment plans should be present in the case,
  # as unapproved plans should have been deleted.
  def test_other_unapproved_treatment_plans_in_case(self):
    t = TEST.Test("Skal ikke inneholde andre planer som er unapproved (disse bør være ryddet opp og slettet når planleggingen er ferdig).", None, self.case_param)
    other_unapproved_plans = []
    for plan in self.case.TreatmentPlans:
      if plan.Name != self.plan.Name:
        if not plan.Review:
          other_unapproved_plans.append(plan.Name)
    if len(other_unapproved_plans) == 0:
      return t.succeed()
    else:
      return t.fail(str(other_unapproved_plans))
