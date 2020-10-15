# encoding: utf8

# A class for reading session data from the Mosaiq database.
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

class Session:
  
  # Returns a single session matching the given database id (PCI_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM PatCItem WHERE PCI_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all session instances belonging to the given course.
  # The sessions are sorted by due_date.
  @classmethod
  def for_course(cls, course):
    sessions = list()
    rows = Database.fetch_all("SELECT * FROM PatCItem WHERE PCP_ID = '{}'".format(course.id))
    for row in rows:
      sessions.append(cls(row))
    sessions.sort(key=lambda s: s.due_date, reverse=False)
    return sessions
  
  # Gives all session instances belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    sessions = list()
    rows = Database.fetch_all("SELECT * FROM PatCItem WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      sessions.append(cls(row))
    return sessions
  
  # Creates a Session instance from a session database row.
  def __init__(self, row):
    # Database attributes:
    self.pci_id = row['PCI_ID']
    self.patient_id = row['Pat_ID1']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.institution_id = row['Inst_ID']
    self.note_id = row['Note_ID']
    self.course_id = row['PCP_ID']
    self.due_date = row['Due_DtTm']
    self.actual_date = row['Act_DtTm']
    self.elapsed_days = row['Elpsd_Action']
    self.activity = row['Activity']
    self.is_pre_treat = row['IsPreTreat']
    self.status_id = row['Status_Enum']
    self.sequence = row['Seq']
    # Convenience attributes:
    self.id = self.pci_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_course = None
    self.instance_created_by_by = None
    self.instance_edited_by = None
    self.instance_note = None
    self.instance_patient = None
    self.instance_scheduled_fields = None

  # The staff who approved the session.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # Gives the course which this session belongs to.
  def course(self):
    if not self.instance_course:
      self.instance_course = Course.find(self.course_id)
    return self.instance_course
    
  # The staff who created the session.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the session.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the note (if any) associated with this session.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the patient (if any) which is referenced by this session.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # Gives the scheduled_fields (if any) associated with this session.
  def scheduled_fields(self):
    if not self.instance_scheduled_fields:
      self.instance_scheduled_fields = ScheduledField.for_session(self)
    return self.instance_scheduled_fields
  
  # The status description derived from the status_id.
  def status(self):
    values = {
      0 : 'Unknown',
      1 : 'VOID',
      2 : 'CLOSE',
      3 : 'COMPLETE',
      4 : 'HOLD',
      5 : 'APPROVE',
      6 : 'PROCESS_LOCK',
      7 : 'PENDING'
    }
    return values.get(self.status_id, 'Unknown status_id: {}'.format(self.status_id))
  