# encoding: utf8

# A class for reading checklist data from the Mosaiq database.
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

class Checklist:
  
  # Returns a single checklist matching the given database id (Chk_id) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Chklist WHERE Chk_id = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all checklists belonging to the given patient.
  # Optionally the query may be restricted to a given task type (specified by id).
  @classmethod
  def for_patient(cls, patient, task_id=None):
    query = "SELECT * FROM Chklist WHERE Pat_ID1 = '{}'".format(patient.id)
    if task_id:
      query += " AND TSK_ID = '{}'".format(task_id)
    checklists = list()
    rows = Database.fetch_all(query)
    for row in rows:
      checklists.append(cls(row))
    return checklists
  
  # Creates a Checklist instance from a checklist database row.
  def __init__(self, row):
    # Database attributes:
    self.chk_id = row['Chk_id']
    self.set_id = row['Chk_set_id']
    self.complete = row['Complete']
    self.suppressed = row['Suppressed']
    self.item_sequence = row['Item_Seq']
    self.qcl_type = row['Qcl_Type']
    self.activity = row['Activity']
    self.comment = row['Notes']
    self.instructions = row['Instructions']
    self.due_date = row['Due_DtTm']
    self.completed_id = row['Com_Staff_ID']
    self.completed_date = row['Act_DtTm']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.note_id = row['Note_ID']
    self.patient_id = row['Pat_ID1']
    self.institution_id = row['Inst_ID']
    self.taskset_id = row['Chklist_ID']
    self.task_id = row['TSK_ID']
    self.requesting_id = row['Req_Staff_ID']
    self.responsible_id = row['Rsp_Staff_ID']
    # Convenience attributes:
    self.id = self.chk_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_completed_by = None
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_note = None
    self.instance_patient = None
    self.instance_requesting = None
    self.instance_responsible = None
    self.instance_task = None
    
  # The staff who approved the checklist.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # The staff who completed the checklist.
  def completed_by(self):
    if not self.instance_completed_by:
      self.instance_completed_by = Location.find(self.completed_by_id)
    return self.instance_completed_by
  
  # The staff who created the checklist.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the checklist.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the note (if any) associated with this checklist.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the patient which this checklist belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # The staff/location/group requesting the checklist.
  def requesting(self):
    if not self.instance_requesting:
      self.instance_requesting = Location.find(self.requesting_id)
    return self.instance_requesting
  
  # The staff/location/group responsible for the checklist.
  def responsible(self):
    if not self.instance_responsible:
      self.instance_responsible = Location.find(self.responsible_id)
    return self.instance_responsible
  
  # Gives the task item referenced by this checklist.
  def task(self):
    if not self.instance_task:
      self.instance_task = Task.find(self.task_id)
    return self.instance_task
  