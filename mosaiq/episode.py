# encoding: utf8

# A class for reading Episode of Care data from the Mosaiq database.
#
# Authors:
# Ben George
#
# Python 3.6

from .database import Database

#from pprint import pprint

class Episode:
  
  # Returns a single task matching the given database id (TSK_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Episode WHERE Epi_Id = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    instance = None
    query = "SELECT * FROM Episode WHERE Pat_ID1 = '{}'".format(patient.id)
    episodes = list()
    rows = Database.fetch_all(query)
    for row in rows:
      episodes.append(cls(row))
    return episodes

  # Creates a Task instance from a task database row.
  def __init__(self, row):
    # Database attributes:
    self.epi_id = row['Epi_Id']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.patient_id = row['Pat_ID1']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_Id']
    self.comment = row['Comment']#.rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.first_treatment_date = row['FirstTx_DtTm']
    self.active_date = row['Active_DtTm']
    self.inactive_date = row['Inactive_DtTm']
    # Convenience attributes:
    self.id = self.epi_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None
    
  # The staff who created the task.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the task.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  