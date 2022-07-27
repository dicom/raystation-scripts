# encoding: utf8

# Contains tests for the patient object.
#
# Verified for RayStation 6.0.

# System configuration:
from connect import *
import sys

# GUI framework (debugging only):
#from tkinter import messagebox

# Local script imports:
import test_p as TEST
#import raystation_utilities as RSU

# This class contains tests for the RayStation Patient object:
# (Note that contrary to all other test objects, the patient does not have any
# parent test obects, as it is on the top of the chain)
class TSPatient(object):
  def __init__(self, patient):
    # RayStation object:
    self.patient = patient
    # Related test suite objects:
    self.ts_case = None
    # Parameters:
    self.param = TEST.Parameter('Pasient', patient.Name, None) # NB: Enkodingproblem: krasjer ikke, men gir ? istedenfor æ,ø,å
    self.id = TEST.Parameter('ID', '', self.param)

  # Tests the length of the patient's ID.
  def id_length_test(self):
    t = TEST.Test('Skal være eksakt 11 tegn (ddmmååxxxxx)', 11, self.id)
    if len(self.patient.PatientID) != 11:
      return t.fail(len(self.patient.PatientID))
    else:
      return t.succeed()

