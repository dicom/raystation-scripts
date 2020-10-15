# encoding: utf8

# A class for reading note data from the Mosaiq database.
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

class Note:
  
  # Returns a single note matching the given database id (Note_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Notes WHERE Note_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all notes belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    notes = list()
    rows = Database.fetch_all("SELECT * FROM Notes WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      notes.append(cls(row))
    return notes
  
  # Creates a Note instance from a note database row.
  def __init__(self, row):
    # Database attributes:
    self.note_id = row['Note_ID']
    self.type_id = row['Note_Type']
    self.subject = row['Subject']
    self.patient_id = row['Pat_ID1']
    self.text = row['notes']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    # Convenience attributes:
    self.id = self.note_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_patient = None
    self.instance_type = None
    
  # The staff who approved the note.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # The staff who created the note.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the note.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the patient which this note belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # Gives the type assigned to this note.
  def type(self):
    if not self.instance_type:
      row = Database.fetch_one("SELECT * FROM Prompt WHERE PGroup = '#NT1' AND Enum = '{}'".format(self.type_id))
      if row != None:
        self.instance_type = row['Text']
    return self.instance_type
