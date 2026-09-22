# Import local files:
from .database import Database

class Session:
  """A class for reading session data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the PatCItem table corresponding to the given id.

    Args:
      id (str or int): The primary database id (PCI_ID) of the row to be extracted.

    Returns:
      Session: A new instance of the Session class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM PatCItem WHERE PCI_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_course(cls, course):
    """Extracts all sessions belonging to the given course.

    Args:
      course (Course): The patient instance for which to extract associated session rows.

    Returns:
      List[Session]: A list of sessions belonging to the given course, sorted by due_date.
    """
    sessions = list()
    rows = Database.fetch_all("SELECT * FROM PatCItem WHERE PCP_ID = '{}'".format(course.id))
    for row in rows:
      sessions.append(cls(row))
    sessions.sort(key=lambda s: s.due_date, reverse=False)
    return sessions

  @classmethod
  def for_patient(cls, patient):
    """Extracts all sessions belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated session rows.

    Returns:
      List[Session]: A list of sessions belonging to the given patient.
    """
    sessions = list()
    rows = Database.fetch_all("SELECT * FROM PatCItem WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      sessions.append(cls(row))
    return sessions

  def __init__(self, row):
    """Initializes an instance from a row extracted from the PatCItem table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def approved_by(self):
    """Gives the staff who approved the session.

    Returns:
      Location: The location (staff) who approved this session.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def course(self):
    """Gives the course which this session belongs to.

    Returns:
      Course: The course which this session belongs to.
    """
    if not self.instance_course:
      self.instance_course = Course.find(self.course_id)
    return self.instance_course

  def created_by(self):
    """Gives the staff who created the session.

    Returns:
      Location: The location (staff) who created this session.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the session.

    Returns:
      Location: The location (staff) who edited this session.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def note(self):
    """Gives the note (if any) associated with this session.

    Returns:
      Note: The note associated with this session, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def patient(self):
    """Gives the patient (if any) which is referenced by this session.

    Returns:
      Patient: The patient which is referenced by this session, or None.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def scheduled_fields(self):
    """Gives the scheduled_fields (if any) associated with this session.

    Returns:
      List[ScheduledField]: The scheduled_fields associated with this session, or an empty list.
    """
    if not self.instance_scheduled_fields:
      self.instance_scheduled_fields = ScheduledField.for_session(self)
    return self.instance_scheduled_fields

  def status(self):
    """The status description derived from the status_id.

    Returns:
      str: The status description (e.g. 'CLOSE').
    """
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
