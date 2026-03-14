# encoding: utf8

# A class for reading patient payer data from the Mosaiq database.
#
# Authors:
# Ben George
#
# Python 3.6

from .database import Database

from pprint import pprint

class PatPay:
  
  # Returns a single task matching the given database id (Payer_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Pat_Pay WHERE PP_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  # Returns the payer for a given patient.
  @classmethod
  def for_patient(cls, patient):
    instance = None
    row = Database.fetch_one("SELECT * FROM Pat_Pay WHERE Pat_ID1 = '{}'".format(str(patient.id)))
    if row != None:
      instance = cls(row)
    return instance

  # Creates a Payer instance from a payer database row.
  def __init__(self, row):
    # Database attributes:
    self.pat_pay_id = row['PP_ID']
    self.payer_id = row['Payer_ID']