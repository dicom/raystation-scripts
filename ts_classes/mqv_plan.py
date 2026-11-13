# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import test_p as TEST


class MQVPlan(object):
  '''This class contains tests for the RayStation TreatmentPlan object.

  Note that contrary to all other test classes, the Plan class does not
  have any parent test classes, as it is on the top of the hierarchy.
  '''

  def __init__(self, patient, case, plan, mq_patient):
    '''Initializes the plan verification with the relevant RayStation instance.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
      case (PyScriptObject): The RayStation Case instance.
      plan (PyScriptObject): The RayStation TreatmentPlan instance.
      mq_patient (MQPatient): The Mosaiq Patient instance.
    '''
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

  def test_matching_patient(self):
    '''Checks that a matching patient has been found in Mosaiq.'''
    t = TEST.Test("Skal finnes matchende pasient i Mosaiq.", self.patient.value, self.patient)
    if self.mq_patient:
      return t.succeed()
    else:
      return t.fail()

  def test_other_unapproved_treatment_plans_in_case(self):
    '''Checks that this case doesnt contain any other unapproved treatment plans.

    At the time when this script is executed, only approved treatment plans should remain
    in the case, as unapproved plans should have been deleted (cleaned up).
    '''
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
