# encoding: utf8

# A class for reading scheduled_field data from the Mosaiq database.
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

class ScheduledField:
  
  # Returns a single scheduled_field matching the given database id (PTC_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM PatTxCal WHERE PTC_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all scheduled field instances belonging to the given field.
  @classmethod
  def for_field(cls, field):
    scheduled_fields = list()
    rows = Database.fetch_all("SELECT * FROM PatTxCal WHERE FLD_Set_ID = '{}'".format(field.id))
    for row in rows:
      scheduled_fields.append(cls(row))
    return scheduled_fields
  
  # Gives all scheduled field instances belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    scheduled_fields = list()
    rows = Database.fetch_all("SELECT * FROM PatTxCal WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      scheduled_fields.append(cls(row))
    return scheduled_fields
  
  # Gives all scheduled field instances belonging to the given session.
  @classmethod
  def for_session(cls, session):
    scheduled_fields = list()
    rows = Database.fetch_all("SELECT * FROM PatTxCal WHERE PCI_ID = '{}'".format(session.id))
    for row in rows:
      scheduled_fields.append(cls(row))
    return scheduled_fields
  
  # Creates a ScheduledField instance from a scheduled_field database row.
  def __init__(self, row):
    # Database attributes:
    self.ptc_id = row['PTC_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.session_id = row['PCI_ID']
    self.status_id = row['Status_enum']
    self.patient_id = row['Pat_ID1']
    self.institution_id = row['Inst_ID']
    self.note_id = row['Note_ID']
    self.field_id = row['FLD_Set_ID']
    self.sequence = row['TxSequence']
    self.partial = row['IsPartial']
    self.mfs = row['MFS']
    self.mfs_begin = row['MFS_Begin']
    self.afs = row['AFS']
    self.afs_begin = row['AFS_Begin']
    self.port_only = row['PF_Only']
    self.port_during = row['PF_During']
    # Convenience attributes:
    self.id = self.ptc_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_delivered_doses = None
    self.instance_edited_by = None
    self.instance_field = None
    self.instance_note = None
    self.instance_patient = None
    self.instance_session = None
    
  # The staff who approved the scheduled_field.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # Gives the delivered_doses (if any) belonging to this scheduled_field.
  def delivered_doses(self):
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_scheduled_field(self)
    return self.instance_delivered_doses
  
  # The staff who last edited the scheduled_field.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the field which this scheduled_field references.
  def field(self):
    if not self.instance_field:
      self.instance_field = Field.find_current(self.field_id)
    return self.instance_field
  
  # Gives the note (if any) associated with this scheduled_field.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the patient which this scheduled_field belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # Gives the session which this scheduled_field belongs to.
  def session(self):
    if not self.instance_session:
      self.instance_session = Session.find(self.session_id)
    return self.instance_session
  
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