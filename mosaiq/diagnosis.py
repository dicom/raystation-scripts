# Import local files:
from .database import Database
from .course import Course

class Diagnosis:
  """A class for reading diagnosis data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Medical table corresponding to the given id.

    Args:
      id (str or int): The primary database id (MED_ID) of the row to be extracted.

    Returns:
      Diagnosis: A new instance of the Diagnosis class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Medical WHERE MED_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    """Extracts all diagnoses belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated diagnoses rows.

    Returns:
      List[Diagnosis]: A list of diagnoses belonging to the given patient.
    """
    diagnoses = list()
    rows = Database.fetch_all("SELECT * FROM Medical WHERE PAT_ID1 = '{}'".format(patient.id))
    for row in rows:
      diagnoses.append(cls(row))
    return diagnoses

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Medical table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def code(self):
    """The diagnosis code.

    Returns:
      str: The diagnosis code (e.g. 'C61').
    """
    if not self.instance_code:
      row = Database.fetch_one("SELECT * FROM Topog WHERE TPG_ID = '{}'".format(self.topography_id))
      if row != None:
        self.instance_code = row['Diag_Code']
        self.instance_description = row['Description']
    return self.instance_code

  def courses(self):
    """Gives the courses (Care plans) (if any) associated with this diagnosis.

    Returns:
      List[Course]: The courses associated with this diagnosis, or an empty list.
    """
    if not self.instance_courses:
      self.instance_courses = Course.for_diagnosis(self)
    return self.instance_courses

  def description(self):
    """The diagnosis description.

    Returns:
      str: The diagnosis description (e.g. 'Myelomatose').
    """
    if not self.instance_description:
      row = Database.fetch_one("SELECT * FROM Topog WHERE TPG_ID = '{}'".format(self.topography_id))
      if row != None:
        self.instance_code = row['Diag_Code']
        self.instance_description = row['Description']
    return self.instance_description

  def edited_by(self):
    """Gives the staff who last edited the diagnosis.

    Returns:
      Location: The location (staff) who edited this diagnosis.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def note(self):
    """Gives the note (if any) associated with this diagnosis.

    Returns:
      Note: The note associated with this diagnosis, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def patient(self):
    """Gives the patient which this diagnosis belongs to.

    Returns:
      Patient: The patient which this diagnosis belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
