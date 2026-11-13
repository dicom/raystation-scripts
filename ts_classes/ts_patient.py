# Import system libraries:
import sys

# Import RayStation packages:
from connect import *

# Import local files:
import test_p as TEST


class TSPatient(object):
  '''This class contains tests for the RayStation Patient object.

  Note that contrary to all other test objects, the patient does not have any
  parent test objects, as it is on the top of the hierarchy.
  '''

  def __init__(self, patient):
    '''Initializes the patient test suite with the relevant RayStation instance.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
    '''
    # RayStation object:
    self.patient = patient
    # Related test suite objects:
    self.ts_case = None
    # Parameters:
    self.param = TEST.Parameter('Pasient', patient.Name, None) # NB: Enkodingproblem: krasjer ikke, men gir ? istedenfor æ,ø,å
    self.id = TEST.Parameter('ID', '', self.param)

  def id_length_test(self):
    '''Tests the length of the patient's ID.'''
    t = TEST.Test('Skal være eksakt 11 tegn (ddmmååxxxxx)', 11, self.id)
    if len(self.patient.PatientID) != 11:
      return t.fail(len(self.patient.PatientID))
    else:
      return t.succeed()
