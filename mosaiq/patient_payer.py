# Import local files:
from .database import Database

class PatientPayer:
  """A class for reading patient payer data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Pat_Pay table corresponding to the given id.

    Args:
      id (str or int): The primary database id (PP_ID) of the row to be extracted.

    Returns:
      PatientPayer: A new instance of the PatientPayer class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Pat_Pay WHERE PP_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    """Extracts the patient payer for the given patient.

    Args:
      patient (Patient): The patient instance for which to extract the patient payer.

    Returns:
      PatientPayer: The PatientPayer for the given patient.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Pat_Pay WHERE Pat_ID1 = '{}'".format(str(patient.id)))
    if row != None:
      instance = cls(row)
    return instance

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Pat_Pay table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.pp_id = row['PP_ID']
    self.payer_id = row['Payer_ID']
    # Convenience attributes:
    self.id = self.pp_id
