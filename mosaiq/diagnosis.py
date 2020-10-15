# encoding: utf8

# A class for reading diagnosis data from the Mosaiq database.
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
from .course import Course

class Diagnosis:
  
  # Returns a single diagnosis matching the given database id (MED_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Medical WHERE MED_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all diagnoses belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    diagnoses = list()
    rows = Database.fetch_all("SELECT * FROM Medical WHERE PAT_ID1 = '{}'".format(patient.id))
    for row in rows:
      diagnoses.append(cls(row))
    return diagnoses
  
  # Creates a Diagnosis instance from a diagnosis database row.
  def __init__(self, row):
    # Database attributes:
    self.med_id = row['MED_ID']
    self.patient_id = row['PAT_ID1']
    self.topography_id = row['TPG_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.note_id = row['Note_ID']
    # Convenience attributes:
    self.id = self.med_id
    # Cache attributes:
    self.instance_code = None
    self.instance_courses = None
    self.instance_description = None
    self.instance_edited_by = None
    self.instance_note = None
    self.instance_patient = None
  
  # The diagnosis code (e.g. 'C61').
  def code(self):
    if not self.instance_code:
      row = Database.fetch_one("SELECT * FROM Topog WHERE TPG_ID = '{}'".format(self.topography_id))
      if row != None:
        self.instance_code = row['Diag_Code']
        self.instance_description = row['Description']
    return self.instance_code
  
  # Gives the radiation oncology courses (Care plans) (if any) belonging to this diagnosis.
  def courses(self):
    if not self.instance_courses:
      self.instance_courses = Course.for_diagnosis(self)
    return self.instance_courses
  
  # The diagnosis description (e.g. 'Ondartet svulst i bronkie').
  def description(self):
    if not self.instance_description:
      row = Database.fetch_one("SELECT * FROM Topog WHERE TPG_ID = '{}'".format(self.topography_id))
      if row != None:
        self.instance_code = row['Diag_Code']
        self.instance_description = row['Description']
    return self.instance_description
  
  # The staff who last edited the diagnosis.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the note (if any) associated with this delivered_dose.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the patient which this diagnosis belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  