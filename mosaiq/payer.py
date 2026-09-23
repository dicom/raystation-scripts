# Import local files:
from .database import Database

class Payer:
  """A class for reading payer data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Payer table corresponding to the given id.

    Args:
      id (str or int): The primary database id (Payer_ID) of the row to be extracted.

    Returns:
      Payer: A new instance of the Payer class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Payer WHERE Payer_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def find_all(cls):
    """Extracts all payers from the database.

    Returns:
      List[Payer]: A list of all payers from the database, sorted by payer_id.
    """
    instance = None
    rows = Database.fetch_all("SELECT * FROM Payer")
    payers = list()
    for row in rows:
      payers.append(cls(row))
    payers.sort(key=lambda p: p.payer_id, reverse=False)
    return payers

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Payer table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.payer_id = row['Payer_ID']
    self.payer_name = row['Payer_Name']
    # Convenience attributes:
    self.id = self.payer_id
