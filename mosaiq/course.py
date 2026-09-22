# Import local files:
from .database import Database
from .prescription import Prescription

class Course:
  """A class for reading course data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the PatCPlan table corresponding to the given id.

    Args:
      id (str or int): The primary database id (PCP_ID) of the row to be extracted.

    Returns:
      Course: A new instance of the Course class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM PatCPlan WHERE PCP_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_diagnosis(cls, diagnosis):
    """Extracts all courses belonging to the diagnosis.

    Args:
      diagnosis (Diagnosis): The diagnosis instance for which to extract associated course rows.

    Returns:
      List[Course]: A list of courses belonging to the given diagnosis, sorted by course number (low to high).
    """
    courses = list()
    rows = Database.fetch_all("SELECT * FROM PatCPlan WHERE MED_ID = '{}'".format(diagnosis.id))
    for row in rows:
      courses.append(cls(row))
    courses.sort(key=lambda c: c.number, reverse=False)
    return courses

  @classmethod
  def for_patient(cls, patient):
    """Extracts all courses belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated course rows.

    Returns:
      List[Course]: A list of courses belonging to the given patient, sorted by course number (low to high).
    """
    courses = list()
    rows = Database.fetch_all("SELECT * FROM PatCPlan WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      courses.append(cls(row))
    courses.sort(key=lambda c: c.number, reverse=False)
    return courses

  def __init__(self, row):
    """Initializes an instance from a row extracted from the PatCPlan table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.pcp_id = row['PCP_ID']
    self.number = row['Course']
    self.intention = row['Tx_Intent'].rstrip()
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

  def diagnosis(self):
    """Gives the diagnosis which this course belongs to.

    Returns:
      Diagnosis: The diagnosis which this course belongs to.
    """
    if not self.instance_diagnosis:
      self.instance_diagnosis = Diagnosis.find(self.diagnosis_id)
    return self.instance_diagnosis

  def edited_by(self):
    """Gives the staff who last edited the course.

    Returns:
      Location: The location (staff) who edited this course.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def note(self):
    """Gives the note (if any) associated with this course.

    Returns:
      Note: The note associated with this course, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def prescriptions(self):
    """Gives the prescriptions (Rad Rx) (if any) associated with this course.

    Returns:
      List[Prescription]: The prescriptions associated with this course, or an empty list.
    """
    if not self.instance_prescriptions:
      self.instance_prescriptions = Prescription.for_course(self)
    return self.instance_prescriptions

  def sessions(self):
    """Gives the treatment sessions (if any) associated with this course.

    Returns:
      List[Session]: The sessions associated with this course, or an empty list.
    """
    if not self.instance_sessions:
      self.instance_sessions = Session.for_course(self)
    return self.instance_sessions
