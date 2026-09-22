# Import local files:
from .database import Database

class Offset:
  """A class for reading offset data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Offset table corresponding to the given id.

    Args:
      id (str or int): The primary database id (OFF_ID) of the row to be extracted.

    Returns:
      Offset: A new instance of the Offset class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Offset WHERE OFF_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_location(cls, location):
    """Extracts all offsets belonging to the given location (staff).

    Args:
      location (Location): The location instance for which to extract associated offset rows.

    Returns:
      List[Offset]: A list of offsets belonging to the given location.
    """
    offsets = list()
    rows = Database.fetch_all("SELECT * FROM Offset WHERE Create_ID = '{}' AND Version = '0'".format(location.id))
    for row in rows:
      offsets.append(cls(row))
    return offsets

  @classmethod
  def for_prescription(cls, prescription, type=None):
    """Extracts all offsets belonging to the given prescription.

    Args:
      prescription (Prescription): The prescription instance for which to extract associated offset rows.
      type (str, optional): The Offset_Type parameter to filter for. Defaults to None.

    Returns:
      List[Offset]: A list of offsets belonging to the given prescription.
    """
    type_part = ""
    if type != None:
      type_part = " AND Offset_Type = '{}'".format(type)
    offsets = list()
    rows = Database.fetch_all("SELECT * FROM Offset WHERE Sit_Set_ID = '{}' AND Version = '0'{}".format(prescription.id, type_part))
    for row in rows:
      offsets.append(cls(row))
    return offsets

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Offset table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.off_id = row['OFF_ID']
    self.offset_id = row['OFF_Set_ID']
    self.site_setup_id = row['Sit_Set_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.study_date = row['Study_DtTm']
    self.version = row['Version']
    self.state_id = row['Offset_State']
    self.type_id = row['Offset_Type']
    self.image_source_id = row['Source_View']
    self.source_name = row['Source_Name']
    self.historic = row['Historic']
    self.superior = row['Superior_Offset']
    self.anterior = row['Anterior_Offset']
    self.lateral = row['Lateral_Offset']
    self.angle = row['Angle_Offset']
    self.pitch = row['Pitch_Offset']
    self.roll = row['Roll_Offset']
    # Convenience attributes:
    self.id = self.off_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_site_setup = None

  def created_by(self):
    """Gives the staff who created the offset.

    Returns:
      Location: The location (staff) who created this offset.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the offset.

    Returns:
      Location: The location (staff) who edited this offset.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def image_source(self):
    """The image_source description derived from the image_source_id.

    Returns:
      str: The image_source description (e.g. '3D').
    """
    values = {
      0 : 'Unknown',
      1 : '2D',
      2 : 'Orthogonal Pair',
      3 : '3D'
    }
    return values.get(self.image_source_id, 'Unknown image_source_id: {}'.format(self.image_source_id))

  # FIXME:
  # For some reason, in some cases we dont find a SiteSetup instance
  # from this record's @site_setup_id. It might be in cases where Site Setup has been modified?!
  # OR it might have to do with Version != 0 (look at Prescription class for this phenomena).
  def site_setup(self):
    """Gives the site_setup which this offset originates from.

    Returns:
      SiteSetup: The site_setup which this offset originates from.
    """
    if not self.instance_site_setup:
      self.instance_site_setup = SiteSetup.find(self.site_setup_id)
    return self.instance_site_setup

  def state(self):
    """The state description derived from the state_id.

    Returns:
      str: The state description (e.g. 'Complete').
    """
    values = {
      0 : 'Reset',
      1 : 'Active',
      2 : 'Complete',
      3 : 'Excluded'
    }
    return values.get(self.state_id, 'Unknown state_id: {}'.format(self.state_id))

  def type(self):
    """The type description derived from the type_id.

    Returns:
      str: The type description (e.g. 'Localization').
    """
    values = {
      0 : 'Unknown',
      1 : 'Prescribed Relative Offset',
      2 : 'Localization',
      3 : 'Session',
      4 : 'Third Party'
    }
    return values.get(self.type_id, 'Unknown type_id: {}'.format(self.type_id))
