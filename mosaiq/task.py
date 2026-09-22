# Import local files:
from .database import Database

class Task:
  """A class for reading site task data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the QCLTask table corresponding to the given id.

    Args:
      id (str or int): The primary database id (TSK_ID) of the row to be extracted.

    Returns:
      Task: A new instance of the Task class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM QCLTask WHERE TSK_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  def __init__(self, row):
    """Initializes an instance from a row extracted from the QCLTask table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.tsk_id = row['TSK_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.description = row['Description'].rstrip()
    self.inactive = row['Inactive']
    self.due_date = row['Due_DtTm']
    self.responsible_id = row['Responsible_Staff_ID']
    self.estimated_duration = row['Est_Dur']
    self.elapsed_action = row['Elpsd_Action']
    # Convenience attributes:
    self.id = self.tsk_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None

  def created_by(self):
    """Gives the staff who created the task.

    Returns:
      Location: The location (staff) who created this task.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the task.

    Returns:
      Location: The location (staff) who edited this task.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
