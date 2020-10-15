# encoding: utf8

# A class for reading task data from the Mosaiq database.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

# Used for GUI debugging:
#from tkinter import *
#from tkinter import messagebox

from .database import Database

class Task:
  
  # Returns a single task matching the given database id (TSK_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM QCLTask WHERE TSK_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Creates a Task instance from a task database row.
  def __init__(self, row):
    # Database attributes:
    self.tsk_id = row['TSK_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.description = row['Description'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.inactive = row['Inactive']
    self.due_date = row['Due_DtTm']
    self.responsible_id = row['Responsible_Staff_ID']
    self.estimated_duration = row['Est_Dur']
    self.elapsed_action = row['Elpsd_Action']
    # Convenience attributes:
    self.id = self.tsk_id
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
  