# encoding: utf8

# A class for reading patient data from the Mosaiq database.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

from .course import Course
from .database import Database
from .delivered_dose import DeliveredDose
from .diagnosis import Diagnosis
from .field import Field
from .prescription import Prescription
from .scheduled_field import ScheduledField
from .session import Session

class Patient:
  
  # Returns a single patient matching the given database id (Pat_ID1) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Patient WHERE Pat_ID1 = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Returns a single patient matching the given IDA (Fødselsnummer: ddmmyy xxxxx) (or None if no match).
  @classmethod
  def find_by_ida(cls, ida):
    patient = None
    pat_id1 = cls.pat_id1_from_ida(ida)
    if pat_id1:
      patient = cls.find(pat_id1)
    return patient
  
  # Extracts all patients matching the given name. Note that the match is exact.
  @classmethod
  def find_by_name(cls, last_name="", first_name=""):
    # Set the max number of patients allowed to be extracted by this query:
    max_patients = 30
    last_name = str(last_name)
    first_name = str(first_name)
    if len(last_name) == 0 and len(first_name) == 0:
      raise InputError("Too few characters used. Requires at least 1 character in order to define a meaningful db search.")
    if len(last_name) > 0:
      ln_part = "Last_Name LIKE '{}%'".format(last_name)
    else:
      ln_part = ""
    if len(first_name) > 0:
      fn_part = "First_Name LIKE '{}%'".format(first_name)
    else:
      fn_part = ""
    if len(last_name) > 0 and len(first_name) > 0:
      mid_part = " AND "
    else:
      mid_part = ""
    patients = list()
    rows = Database.fetch_all("SELECT TOP {} * FROM Patient WHERE {}{}{}".format(str(max_patients), ln_part, mid_part, fn_part))
    for row in rows:
      patients.append(cls(row))
    return patients
  
  # Returns a Pat_Id1 matching the given patient IDA (or None if no match).
  @classmethod
  def pat_id1_from_ida(cls, fnr):
    pat_id1 = None
    row = Database.fetch_one("SELECT * FROM Ident WHERE IDA = '{}'".format(str(fnr)))
    if row != None:
      pat_id1 = row['Pat_Id1'] # (typo probably in database table: lower case d)
    return pat_id1
  
  # Creates a Patient instance from a patient database row.
  def __init__(self, row):
    # Database attributes:
    self.pat_id1 = row['Pat_ID1']
    self.created_date = row['Create_DtTm']
    self.edited_date = row['Edit_DtTm']
    self.birth_date = row['Birth_DtTm']
    self.last_name = row['Last_Name']
    self.first_name = row['First_Name']
    self.middle_name = row['MIddle_Name']
    self.inactive = row['Inactive']
    # Convenience attributes:
    self.id = self.pat_id1
    # Cache attributes:
    self.instance_address = None
    self.instance_appointments = None
    self.instance_checklists = None
    self.instance_courses = None
    self.instance_delivered_doses = None
    self.instance_diagnoses = None
    self.instance_documents = None
    self.instance_fields = None
    self.instance_images = None
    self.instance_institution_id = None
    self.instance_is_in = None
    self.instance_location = None
    self.instance_notes = None
    self.instance_pat_ida = None
    self.instance_prescriptions = None
    self.instance_performed_site_setups = None
    self.instance_scheduled_fields = None

  # Patient's address (postal code).
  def address(self):
    if not self.instance_address:
      row = Database.fetch_one("SELECT * FROM Admin WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_address = row['Pat_Postal']
    return self.instance_address
  
  # The patient's appointments.
  def appointments(self):
    if not self.instance_appointments:
      self.instance_appointments = Appointment.for_patient(self)
    return self.instance_appointments
  
  # Gives the checklist items/tasks (if any) belonging to this patient.
  def checklists(self):
    if not self.instance_checklists:
      self.instance_checklists = Checklist.for_patient(self)
    return self.instance_checklists
  
  # Gives the radiation oncology courses (Care plans) (if any) belonging to this patient.
  def courses(self):
    if not self.instance_courses:
      self.instance_courses = Course.for_patient(self)
    return self.instance_courses
      
  # Gives the patient's delivered dose instances.
  def delivered_doses(self):
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_patient(self)
    return self.instance_delivered_doses
  
  # Gives the diagnoses (if any) belonging to this patient.
  def diagnoses(self):
    if not self.instance_diagnoses:
      self.instance_diagnoses = Diagnosis.for_patient(self)
    return self.instance_diagnoses
  
  # Gives the documents (if any) belonging to this patient.
  def documents(self):
    if not self.instance_documents:
      self.instance_documents = Document.for_patient(self)
    return self.instance_documents
  
  # Gives the fields (if any) belonging to this patient.
  def fields(self):
    if not self.instance_fields:
      self.instance_fields = Field.for_patient(self)
    return self.instance_fields
  
  # Gives the full name (formatted by last name, comma first name space middle name).
  def full_name(self):
    name = self.last_name.rstrip()
    if len(first_name > 0):
      name = "{}, {} {}".format(name, self.first_name, self.middle_name).rstrip()
    return name
  
  # Gives the images (if any) belonging to this patient.
  def images(self):
    if not self.instance_images:
      self.instance_images = Image.for_patient(self)
    return self.instance_images
  
  # Patient's institution id (e.g. 1 for Site 1, 2 for Site 2).
  def institution_id(self):
    if not self.instance_institution_id:
      row = Database.fetch_one("SELECT * FROM AdmDept WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_institution_id = row['Inst_ID']
    return self.instance_institution_id
  
  # Patient's nursing status (in hospital bed or not).
  def is_in(self):
    if not self.instance_is_in:
      row = Database.fetch_one("SELECT * FROM Admin WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_is_in = row['IsInPatient']
    return self.instance_is_in
  
  # Patient's location (nursing unit).
  def location(self):
    if not self.instance_location:
      row = Database.fetch_one("SELECT * FROM Admin WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_location = row['Nurse_Unit']
    return self.instance_location
  
  # Gives the next available field number for this patient.
  # Any fields containing 'XVI' in its label is not considered.
  # Fields imported from Visir (containing an @) is processed and included.
  # Examples:
  # If no fields exists, 1 is returned.
  # If field labels 1,2 and 3 exists, 4 is returned.
  # If field labels @1, @2, 3 and XVI4 exists, 4 is returned.
  # If field labels 1 and 3 exists, 4 is returned.
  def next_available_field_number(self):
    numbers = [0]
    for field in self.fields():
      # We are not intersted in fields that are XVI-related:
      if not 'XVI' in field.label:
        # Fields imported from Visir will contain an '@' before the field number. This must be washed out:
        digitized_label = ''.join(c for c in field.label if c.isdigit())
        # Add it to our list as long as we're not left with an empty string:
        if digitized_label != '':
          numbers.append(int(digitized_label))
    next_available_number = max(numbers) + 1
    return next_available_number
  
  # Gives the notes (if any) belonging to this patient.
  def notes(self):
    if not self.instance_notes:
      self.instance_notes = Note.for_patient(self)
    return self.instance_notes
  
  # Patients PAT_IDA (social security nr).
  def pat_ida(self):
    if not self.instance_pat_ida:
      row = Database.fetch_one("SELECT * FROM Ident WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_pat_ida = row['IDA']
    return self.instance_pat_ida
  
  # Gives the patient's performed_site_setup instances.
  def performed_site_setups(self):
    if not self.instance_performed_site_setups:
      self.instance_performed_site_setups = PerformedSiteSetup.for_patient(self)
    return self.instance_performed_site_setups
  
  # Gives the radiation prescriptions (Rad Rx) (if any) belonging to this patient.
  def prescriptions(self):
    if not self.instance_prescriptions:
      self.instance_prescriptions = Prescription.for_patient(self)
    return self.instance_prescriptions
  
  # Gives the scheduled_fields (if any) belonging to this patient.
  def scheduled_fields(self):
    if not self.instance_scheduled_fields:
      self.instance_scheduled_fields = ScheduledField.for_patient(self)
    return self.instance_scheduled_fields
  
  # Gives the sessions (if any) belonging to this patient.
  def sessions(self):
    if not self.instance_sessions:
      self.instance_sessions = Session.for_patient(self)
    return self.instance_sessions
  