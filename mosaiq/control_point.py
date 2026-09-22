# Import local files:
from .database import Database

class ControlPoint:
  """A class for reading control point data from the Mosaiq database."""

  # Returns a single control_point matching the given database id (TFP_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    """Finds the row in the TxFieldPoint table corresponding to the given id.

    Args:
      id (str or int): The primary database id (TFP_ID) of the row to be extracted.

    Returns:
      ControlPoint: A new instance of the ControlPoint class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM TxFieldPoint WHERE TFP_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_field(cls, field):
    """Extracts all control points belonging to the given field.

    Args:
      field (Field): The field instance for which to extract associated control point rows.

    Returns:
      List[ControlPoint]: A list of control points belonging to the given field.
    """
    control_points = list()
    rows = Database.fetch_all("SELECT * FROM TxFieldPoint WHERE FLD_ID = '{}'".format(field.id))
    for row in rows:
      control_points.append(cls(row))
    return control_points

  def __init__(self, row):
    """Initializes an instance from a row extracted from the TxFieldPoint table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.tfp_id = row['TFP_ID']
    self.field_id = row['FLD_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.number = row['Point']
    self.index = row['Index']
    self.nr_leaves = row['MLC_Leaves']
    self.leaf_bank1 = row['A_Leaf_Set']
    self.leaf_bank2 = row['B_Leaf_Set']
    self.gantry_angle = row['Gantry_Ang']
    self.collimator_angle = row['Coll_Ang']
    self.field_size_x = row['Field_X']
    self.field_size_y = row['Field_Y']
    self.collimator_x1 = float(row['Coll_X1'])
    self.collimator_x2 = float(row['Coll_X2'])
    self.collimator_y1 = float(row['Coll_Y1'])
    self.collimator_y2 = float(row['Coll_Y2'])
    self.beam_intensity = row['Beam_Intensity']
    self.energy = row['Energy']
    self.energy_unit_id = row['Energy_Unit_Enum']
    self.meterset_rate = row['Meterset_Rate']
    self.gantry_rotation_id = row['Gantry_Dir_Enum']
    self.couch_pitch_angle = row['Couch_Pitch_Ang']
    #self.couch_roll_angle = row['Couch_Roll_Angle'] # for some reason this caused a crash
    self.couch_angle = row['Couch_Ang']
    self.couch_vertical = row['Couch_Vrt']
    self.couch_lateral = row['Couch_Lat']
    self.couch_longitudinal = row['Couch_Lng']
    self.isocenter_x = row['Isocenter_X']
    self.isocenter_y = row['Isocenter_Y']
    self.isocenter_z = row['Isocenter_Z']
    self.is_modified = row['IsModifiedAfterDataImport']
    # Convenience attributes:
    self.id = self.tfp_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_field = None

  def created_by(self):
    """Gives the staff who created the control point.

    Returns:
      Location: The location (staff) who created this control point.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the control point.

    Returns:
      Location: The location (staff) who edited this control point.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  # The energy_unit description derived from the energy_unit_id.
  def energy_unit(self):
    """The energy_unit description derived from the energy_unit_id.

    Returns:
      str: The energy unit description (e.g. 'MV').
    """
    values = {
      1 : 'KV',
      2 : 'MV',
      3 : 'MEV'
    }
    return values.get(self.energy_unit_id, 'Unknown energy_unit_id: {}'.format(self.energy_unit_id))

  def field(self):
    """Gives the field which this control point belongs to.

    Returns:
      Field: The field which this control point belongs to.
    """
    if not self.instance_field:
      self.instance_field = Field.find(self.field_id)
    return self.instance_field

  def gantry_rotation(self):
    """The gantry_rotation description derived from the gantry_rotation_id.

    Returns:
      str: The gantry rotation description (e.g. 'CW').
    """
    values = {
      0 : 'Unspecified',
      1 : 'CW',
      2 : 'CC',
      3 : 'NONE'
    }
    return values.get(self.gantry_rotation_id, 'Unknown gantry_rotation_id: {}'.format(self.gantry_rotation_id))
