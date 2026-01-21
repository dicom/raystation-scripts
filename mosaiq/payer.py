# encoding: utf8

# A class for reading Episode of Care data from the Mosaiq database.
#
# Authors:
# Ben George
#
# Python 3.6

from .database import Database

from pprint import pprint

class Payer:
  
  # Returns a single task matching the given database id (Payer_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Payer WHERE Payer_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  @classmethod
  def find_all(cls):
    instance = None
    rows = Database.fetch_all("SELECT * FROM Payer")
    payers = list()
    for row in rows:
      payers.append(cls(row))
    payers.sort(key=lambda p: p.payer_id, reverse=False)
    return payers

  # Creates a Payer instance from a payer database row.
  def __init__(self, row):
    # Database attributes:
    self.payer_id = row['Payer_ID']
    self.payer_name = row['Payer_Name']