# Import local files:
from .database import Database

class Episode:
  """A class for reading episode data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Episode table corresponding to the given id.

    Args:
      id (str or int): The primary database id (Epi_Id) of the row to be extracted.

    Returns:
      Episode: A new instance of the Episode class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Episode WHERE Epi_Id = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    """Extracts all episodes belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated episode rows.

    Returns:
      List[Episode]: A list of episodes belonging to the given patient.
    """
    instance = None
    query = "SELECT * FROM Episode WHERE Pat_ID1 = '{}'".format(patient.id)
    episodes = list()
    rows = Database.fetch_all(query)
    for row in rows:
      episodes.append(cls(row))
    return episodes

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Episode table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.epi_id = row['Epi_Id']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.patient_id = row['Pat_ID1']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_Id']
    self.comment = row['Comment']
    self.first_treatment_date = row['FirstTx_DtTm']
    self.active_date = row['Active_DtTm']
    self.inactive_date = row['Inactive_DtTm']
    # Convenience attributes:
    self.id = self.epi_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None

  def created_by(self):
    """Gives the staff who created the episode.

    Returns:
      Location: The location (staff) who created this episode.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the episode.

    Returns:
      Location: The location (staff) who edited this episode.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
