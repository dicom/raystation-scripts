# Import local files:
from .database import Database

class ScheduledField:
  """A class for reading scheduled field data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the PatTxCal table corresponding to the given id.

    Args:
      id (str or int): The primary database id (PTC_ID) of the row to be extracted.

    Returns:
      ScheduledField: A new instance of the ScheduledField class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM PatTxCal WHERE PTC_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_field(cls, field):
    """Extracts all scheduled fields belonging to the given field.

    Args:
      field (Field): The field instance for which to extract associated scheduled field rows.

    Returns:
      List[ScheduledField]: A list of scheduled fields belonging to the given field.
    """
    scheduled_fields = list()
    rows = Database.fetch_all("SELECT * FROM PatTxCal WHERE FLD_Set_ID = '{}'".format(field.id))
    for row in rows:
      scheduled_fields.append(cls(row))
    return scheduled_fields

  @classmethod
  def for_patient(cls, patient):
    """Extracts all scheduled fields belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated scheduled field rows.

    Returns:
      List[ScheduledField]: A list of scheduled fields belonging to the given patient.
    """
    scheduled_fields = list()
    rows = Database.fetch_all("SELECT * FROM PatTxCal WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      scheduled_fields.append(cls(row))
    return scheduled_fields

  @classmethod
  def for_session(cls, session):
    """Extracts all scheduled fields belonging to the given session.

    Args:
      session (Session): The session instance for which to extract associated scheduled field rows.

    Returns:
      List[ScheduledField]: A list of scheduled fields belonging to the given session.
    """
    scheduled_fields = list()
    rows = Database.fetch_all("SELECT * FROM PatTxCal WHERE PCI_ID = '{}'".format(session.id))
    for row in rows:
      scheduled_fields.append(cls(row))
    return scheduled_fields

  def __init__(self, row):
    """Initializes an instance from a row extracted from the PatTxCal table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def approved_by(self):
    """Gives the staff who approved the scheduled_field.

    Returns:
      Location: The location (staff) who approved this scheduled_field.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def delivered_doses(self):
    """Gives the delivered_doses (if any) belonging to this scheduled_field.

    Returns:
      List[DeliveredDose]: The delivered_doses belonging to this scheduled_field, or an empty list.
    """
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_scheduled_field(self)
    return self.instance_delivered_doses

  def edited_by(self):
    """Gives the staff who last edited the scheduled_field.

    Returns:
      Location: The location (staff) who edited this scheduled_field.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def field(self):
    """Gives the field which this scheduled_field references.

    Returns:
      Note: The field which this scheduled_field references.
    """
    if not self.instance_field:
      self.instance_field = Field.find_current(self.field_id)
    return self.instance_field

  def note(self):
    """Gives the note (if any) associated with this scheduled_field.

    Returns:
      Note: The note associated with this scheduled_field, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def patient(self):
    """Gives the patient which this scheduled_field belongs to.

    Returns:
      Note: The patient which this scheduled_field belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def session(self):
    """Gives the session which this scheduled_field belongs to.

    Returns:
      Note: The session which this scheduled_field belongs to.
    """
    if not self.instance_session:
      self.instance_session = Session.find(self.session_id)
    return self.instance_session

  def status(self):
    """The status description derived from the status_id.

    Returns:
      str: The status description (e.g. 'COMPLETE').
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
