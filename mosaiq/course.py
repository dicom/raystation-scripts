# encoding: utf8

# A class for reading course data from the Mosaiq database.
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
from .prescription import Prescription

class Course:
  
  # Returns a single course matching the given database id (PCP_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM PatCPlan WHERE PCP_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all courses belonging to the given diagnosis.
  # Returned courses are sorted by course number: low to high.
  @classmethod
  def for_diagnosis(cls, diagnosis):
    courses = list()
    rows = Database.fetch_all("SELECT * FROM PatCPlan WHERE MED_ID = '{}'".format(diagnosis.id))
    for row in rows:
      courses.append(cls(row))
    courses.sort(key=lambda c: c.number, reverse=False)
    return courses
  
  # Gives all courses belonging to the given patient.
  # Returned courses are sorted by course number: low to high.
  @classmethod
  def for_patient(cls, patient):
    courses = list()
    rows = Database.fetch_all("SELECT * FROM PatCPlan WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      courses.append(cls(row))
    courses.sort(key=lambda c: c.number, reverse=False)
    return courses
  
  # Creates a Course instance from a course database row.
  def __init__(self, row):
    # Database attributes:
    self.pcp_id = row['PCP_ID']
    self.number = row['Course']
    self.intention = row['Tx_Intent'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.patient_id = row['Pat_ID1']
    self.diagnosis_id = row['MED_ID']
    self.comment = row['Notes']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.note_id = row['Note_ID']
    # Convenience attributes:
    self.id = self.pcp_id
    # Cache attributes:
    self.instance_diagnosis = None
    self.instance_edited_by = None
    self.instance_note = None
    self.instance_prescriptions = None
    self.instance_sessions = None

  # Gives the diagnosis which this course belongs to.
  def daignosis(self):
    if not self.instance_diagnosis:
      self.instance_diagnosis = Diagnosis.find(self.diagnosis_id)
    return self.instance_diagnosis
  
  # The staff who last edited the course.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the note (if any) associated with this course.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the radiation prescriptions (Rad Rx) (if any) belonging to this course.
  def prescriptions(self):
    if not self.instance_prescriptions:
      self.instance_prescriptions = Prescription.for_course(self)
    return self.instance_prescriptions
  
  # Gives the treatment sessions (if any) associated with this course.
  def sessions(self):
    if not self.instance_sessions:
      self.instance_sessions = Session.for_course(self)
    return self.instance_sessions
  