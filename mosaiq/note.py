# Import local files:
from .database import Database

class Note:
  """A class for reading note data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Notes table corresponding to the given id.

    Args:
      id (str or int): The primary database id (Note_ID) of the row to be extracted.

    Returns:
      Note: A new instance of the Note class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Notes WHERE Note_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    """Extracts all notes belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated note rows.

    Returns:
      List[Note]: A list of notes belonging to the given patient.
    """
    notes = list()
    rows = Database.fetch_all("SELECT * FROM Notes WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      notes.append(cls(row))
    return notes

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Notes table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def approved_by(self):
    """Gives the staff who approved the note.

    Returns:
      Location: The location (staff) who approved this note.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def created_by(self):
    """Gives the staff who created the note.

    Returns:
      Location: The location (staff) who created this note.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the note.

    Returns:
      Location: The location (staff) who edited this note.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def patient(self):
    """Gives the patient which this note belongs to.

    Returns:
      Patient: The patient which this note belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def type(self):
    """Gives the type assigned to this note.

    Returns:
      str: The type assigned to this note.
    """
    if not self.instance_type:
      row = Database.fetch_one("SELECT * FROM Prompt WHERE PGroup = '#NT1' AND Enum = '{}'".format(self.type_id))
      if row != None:
        self.instance_type = row['Text']
    return self.instance_type
