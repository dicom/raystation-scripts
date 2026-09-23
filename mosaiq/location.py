# Import local files:
from .database import Database

class Location:
  """A class for reading location (staff/machine) data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Staff table corresponding to the given id.

    Note that the Staff table is also used to store machines/locations.

    Args:
      id (str or int): The primary database id (Staff_ID) of the row to be extracted.

    Returns:
      Location: A new instance of the Location class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Staff WHERE Staff_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def find_by_name(cls, last_name="", first_name=""):
    """Finds all locations (Staff/Machine) matching the given name.

    Note that the match is exact.
    A maximum of 30 matches will be returned.

    Args:
      last_name (str, optional): The last name of the staff. Defaults to an empty string.
      first_name (str, optional): The first name of the staff. Defaults to an empty string.

    Returns:
      List[Location]: A list of locations (staff) matching the given name, or an empty list.
    """
    # Set the max number of locations allowed to be extracted by this query:
    max_locations = 30
    last_name = str(last_name)
    first_name = str(first_name)
    if len(last_name) == 0 and len(first_name) == 0:
      raise InputError("Too few characters used. Requires at least 1 character in order to define a meaningful db search.")
    if len(last_name) > 0:
      ln_part = "Last_Name LIKE '{}%'".format(last_name)
    else:
      ln_part = ""
    if len(first_name) > 0:
      fn_part = "First_Name LIKE '{}%'".format(first_name)
    else:
      fn_part = ""
    if len(last_name) > 0 and len(first_name) > 0:
      mid_part = " AND "
    else:
      mid_part = ""
    locations = list()
    rows = Database.fetch_all("SELECT TOP {} * FROM Staff WHERE {}{}{}".format(str(max_locations), ln_part, mid_part, fn_part))
    for row in rows:
      locations.append(cls(row))
    return locations

  @classmethod
  def find_by_user_name(cls, user_name):
    """Finds a location (Staff/Machine) matching the given user name.

    Args:
      user_name (str): The user name of the staff.

    Returns:
      Location: A location (staff) matching the given user name, or None.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Staff WHERE User_Name = '{}'".format(str(user_name)))
    #pprint(row)
    if row != None:
      instance = cls(row)
    return instance

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Staff table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.staff_id = row['Staff_ID']
    self.created_date = row['Create_DtTm']
    self.initials = row['Initials'].rstrip()
    self.user_name = row['User_Name'].rstrip()
    self.code = row['Code'].rstrip()
    self.type = row['Type'].rstrip()
    self.last_name = row['Last_Name'].rstrip()
    self.first_name = row['First_Name']
    self.middle_initial = row['Mdl_Initial'].rstrip()
    self.deleted = row['Deleted']
    self.inactive = row['Status_inactive']
    self.login = row['Status_Login']
    self.unapproved = row['Status_Unaprv']
    self.password = row['PasswordBytes'].rstrip()
    # Convenience attributes:
    self.id = self.staff_id
    # Cache attributes:
    self.instance_institution_id = None

  def institution_id(self):
    """Gives the institution_id of this location (Staff/Machine)

    Returns:
      int: The nstitution_id of this location (Staff/Machine).
    """
    if not self.instance_institution_id:
      row = Database.fetch_one("SELECT * FROM StfDept WHERE Staff_ID = '{}'".format(str(self.staff_id)))
      if row != None:
        self.instance_institution_id = row['Inst_ID']
    return self.instance_institution_id

  def full_name(self):
    """Gives the full name, formatted as "last_name, first_name middle_name".

    Returns:
      str: The full name, formatted as "last_name, first_name middle_name".
    """
    name = self.last_name.rstrip()
    if len(self.first_name) > 0:
      name = "{}, {} {}".format(name, self.first_name, self.middle_initial).rstrip()
    return name
