# Import local files:
from .database import Database

class Activity:
  """A class for reading activity data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the CPT table corresponding to the given id.

    Args:
      id (str or int): The primary database id (PRS_ID) of the row to be extracted.

    Returns:
      Activity: A new instance of the Activity class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM CPT WHERE PRS_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def find_by_code(cls, hsp_code):
    """Finds the row in the CPT table matching the given code.

    Args:
      hsp_code (str or int): The activity code (Hsp_Code) of the row to be extracted.

    Returns:
      Activity: A new instance of the Activity class, or None if no match.
    """
    instance = None
    if len(hsp_code) > 0:
      row = Database.fetch_one("SELECT * FROM CPT WHERE Hsp_Code = '{}'".format(str(hsp_code)))
      if row != None:
        instance = cls(row)
    return instance

  def __init__(self, row):
    """Initializes an instance from a row extracted from the CPT table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.prs_id = row['PRS_ID']
    self.inactive = row['Status_Inactive']
    self.code_group = row['CGroup'].rstrip()
    self.code1 = row['Hsp_Code']
    self.code2 = row['Hsp_Code1']
    self.code3 = row['Hsp_Code2']
    self.code4 = row['Hsp_Code3']
    self.code5 = row['Hsp_Code4']
    self.code6 = row['Hsp_Code5']
    self.charge_code = row['CPT_Code'].rstrip()
    self.abbreviation = row['Tiny_Desc'].rstrip()
    self.title = row['Short_Desc']
    self.description = row['Description']
    self.deleted = row['Deleted']
    self.color = row['ScheduleColor']
    # Convenience attributes:
    self.id = self.prs_id
