# Import local files:
from .appointment import Appointment
from .checklist import Checklist
from .course import Course
from .database import Database
from .delivered_dose import DeliveredDose
from .diagnosis import Diagnosis
from .document import Document
from .field import Field
from .image import Image
from .location import Location
from .note import Note
from .performed_site_setup import PerformedSiteSetup
from .prescription import Prescription
from .scheduled_field import ScheduledField
from .session import Session

class Patient:
  """A class for reading patient data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Patient table corresponding to the given id.

    Args:
      id (str or int): The primary database id (Pat_ID1) of the row to be extracted.

    Returns:
      Patient: A new instance of the Patient class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Patient WHERE Pat_ID1 = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def find_by_ida(cls, ida):
    """Finds a patient by IDA.

    Note that in our Norwegian demographics system, IDA points to what we call 'birth number',
    which is an 11 digit number containing birth date and a 5 digit personal number.

    Args:
      ida (str): The IDA parameter ("an 11 digit 'birth number' - DDMMYYxxxxx).

    Returns:
      Patient: A new instance of the Patient class, or None if no match.
    """
    patient = None
    pat_id1 = cls.pat_id1_from_ida(ida)
    if pat_id1:
      patient = cls.find(pat_id1)
    return patient

  @classmethod
  def find_by_name(cls, last_name="", first_name=""):
    """Finds all patients matching the given name.

    Note that the match is exact.
    A maximum of 30 matches will be returned.

    Args:
      last_name (str, optional): The last name of the patient. Defaults to an empty string.
      first_name (str, optional): The first name of the patient. Defaults to an empty string.

    Returns:
      List[Patient]: A list of patients matching the given name, or an empty list.
    """
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

  @classmethod
  def pat_id1_from_ida(cls, ida):
    """Finds a patient's ID1 from the IDA.

    Note that in our Norwegian demographics system, IDA points to what we call 'birth number',
    which is an 11 digit number containing birth date and a 5 digit personal number.

    Args:
      ida (str): The IDA parameter ("an 11 digit 'birth number' - DDMMYYxxxxx).

    Returns:
      str: The 'Pat_ID1' value, or None if no match.
    """
    pat_id1 = None
    row = Database.fetch_one("SELECT * FROM Ident WHERE IDA = '{}'".format(str(ida)))
    if row != None:
      pat_id1 = row['Pat_Id1'] # (typo probably in database table: lower case d)
    return pat_id1

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Patient table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def address(self):
    """Gives the patient's address (postal code).

    Returns:
      str: The patient's address ('Pat_Postal' value from the 'Admin' table).
    """
    if not self.instance_address:
      row = Database.fetch_one("SELECT * FROM Admin WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_address = row['Pat_Postal']
    return self.instance_address

  def appointments(self):
    """Gives the appointments (if any) belonging to this patient.

    Returns:
      List[Appointment]: The appointments belonging to this patient, or an empty list.
    """
    if not self.instance_appointments:
      self.instance_appointments = Appointment.for_patient(self)
    return self.instance_appointments

  def checklists(self):
    """Gives the checklist items/tasks (if any) belonging to this patient.

    Returns:
      List[Checklist]: The checklist items/tasks belonging to this patient, or an empty list.
    """
    if not self.instance_checklists:
      self.instance_checklists = Checklist.for_patient(self)
    return self.instance_checklists

  def courses(self):
    """Gives the courses (Care plans) (if any) belonging to this patient.

    Returns:
      List[Course]: courses belonging to this patient, or an empty list.
    """
    if not self.instance_courses:
      self.instance_courses = Course.for_patient(self)
    return self.instance_courses

  def delivered_doses(self):
    """Gives the delivered_doses (if any) belonging to this patient.

    Returns:
      List[DeliveredDose]: The delivered_doses belonging to this patient, or an empty list.
    """
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_patient(self)
    return self.instance_delivered_doses

  def diagnoses(self):
    """Gives the diagnoses (if any) belonging to this patient.

    Returns:
      List[Diagnosis]: The diagnoses belonging to this patient, or an empty list.
    """
    if not self.instance_diagnoses:
      self.instance_diagnoses = Diagnosis.for_patient(self)
    return self.instance_diagnoses

  def documents(self):
    """Gives the documents (if any) belonging to this patient.

    Returns:
      List[Document]: The documents belonging to this patient, or an empty list.
    """
    if not self.instance_documents:
      self.instance_documents = Document.for_patient(self)
    return self.instance_documents

  def fields(self):
    """Gives the fields (if any) belonging to this patient.

    Returns:
      List[Field]: The fields belonging to this patient, or an empty list.
    """
    if not self.instance_fields:
      self.instance_fields = Field.for_patient(self)
    return self.instance_fields

  # Gives the full name (formatted by last name, comma first name space middle name).
  def full_name(self):
    name = self.last_name.rstrip()
    if len(self.first_name) > 0:
      name = "{}, {} {}".format(name, self.first_name, self.middle_name).rstrip()
    return name

  def images(self):
    """Gives the images (if any) belonging to this patient.

    Returns:
      List[Image]: The images belonging to this patient, or an empty list.
    """
    if not self.instance_images:
      self.instance_images = Image.for_patient(self)
    return self.instance_images

  def institution_id(self):
    """Gives the patient's institution_id.

    Returns:
      int: The patient's institution_id ('Inst_ID' value from the 'AdmDept' table).
    """
    if not self.instance_institution_id:
      row = Database.fetch_one("SELECT * FROM AdmDept WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_institution_id = row['Inst_ID']
    return self.instance_institution_id

  def is_in(self):
    """Gives the patient's nursing status (in-patient or out-patient).

    Returns:
      str: The patient's nursing status (e.q. 'I' or 'O').
    """
    if not self.instance_is_in:
      row = Database.fetch_one("SELECT * FROM Admin WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_is_in = row['IsInPatient']
    return self.instance_is_in

  def location(self):
    """Gives the patient's nursing unit (if any).

    Returns:
      str: The patient's nursing unit.
    """
    if not self.instance_location:
      row = Database.fetch_one("SELECT * FROM Admin WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_location = row['Nurse_Unit']
    return self.instance_location

  def next_available_field_number(self):
    """Gives the next available radiation field number for this patient.

    Note:
    Any fields containing 'XVI' in its label is not considered.
    Fields imported from Visir (containing an @) is processed and included.
    Examples:
    If no fields exists, 1 is returned.
    If field labels 1,2 and 3 exists, 4 is returned.
    If field labels @1, @2, 3 and XVI4 exists, 4 is returned.
    If field labels 1 and 3 exists, 4 is returned.

    Returns:
      int: The next available field number.
    """
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

  def notes(self):
    """Gives the notes (if any) belonging to this patient.

    Returns:
      List[Note]: The notes belonging to this patient, or an empty list.
    """
    if not self.instance_notes:
      self.instance_notes = Note.for_patient(self)
    return self.instance_notes

  def pat_ida(self):
    """Gives the patient's IDA (social security nr).

    Returns:
      str: The patient's IDA.
    """
    if not self.instance_pat_ida:
      row = Database.fetch_one("SELECT * FROM Ident WHERE Pat_ID1 = '{}'".format(self.pat_id1))
      if row != None:
        self.instance_pat_ida = row['IDA']
    return self.instance_pat_ida

  def performed_site_setups(self):
    """Gives the performed_site_setups (if any) associated with this patient.

    Returns:
      List[PerformedSiteSetup]: The performed_site_setups associated with this patient, or an empty list.
    """
    if not self.instance_performed_site_setups:
      self.instance_performed_site_setups = PerformedSiteSetup.for_patient(self)
    return self.instance_performed_site_setups

  def prescriptions(self):
    """Gives the prescriptions (Rad Rx) (if any) associated with this patient.

    Returns:
      List[Prescription]: The prescriptions associated with this patient, or an empty list.
    """
    if not self.instance_prescriptions:
      self.instance_prescriptions = Prescription.for_patient(self)
    return self.instance_prescriptions

  def scheduled_fields(self):
    """Gives the scheduled_fields (if any) associated with this patient.

    Returns:
      List[ScheduledField]: The scheduled_fields associated with this patient, or an empty list.
    """
    if not self.instance_scheduled_fields:
      self.instance_scheduled_fields = ScheduledField.for_patient(self)
    return self.instance_scheduled_fields

  def sessions(self):
    """Gives the sessions (if any) associated with this patient.

    Returns:
      List[Session]: The sessions associated with this patient, or an empty list.
    """
    if not self.instance_sessions:
      self.instance_sessions = Session.for_patient(self)
    return self.instance_sessions
