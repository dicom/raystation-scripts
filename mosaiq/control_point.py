# encoding: utf8

# A class for reading control_point data from the Mosaiq database.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

# Used for GUI debugging:
#from tkinter import *
#from tkinter import messagebox

from .database import Database

class ControlPoint:
  
  # Returns a single control_point matching the given database id (TFP_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM TxFieldPoint WHERE TFP_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  

  # Gives all control_point instances belonging to the given field.
  @classmethod
  def for_field(cls, field):
    control_points = list()
    rows = Database.fetch_all("SELECT * FROM TxFieldPoint WHERE FLD_ID = '{}'".format(field.id))
    for row in rows:
      control_points.append(cls(row))
    return control_points
  
  # Creates a ControlPoint instance from a control_point database row.
  def __init__(self, row):
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

  # The staff who created the appointment.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the appointment.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # The energy_unit description derived from the energy_unit_id.
  def energy_unit(self):
    values = {
      1 : 'KV',
      2 : 'MV',
      3 : 'MEV'
    }
    return values.get(self.energy_unit_id, 'Unknown energy_unit_id: {}'.format(self.energy_unit_id))
  
  # Gives the field which this checklist belongs to.
  def field(self):
    if not self.instance_field:
      self.instance_field = Field.find(self.field_id)
    return self.instance_field
  
  # The gantry_rotation description derived from the gantry_rotation_id.
  def gantry_rotation(self):
    values = {
      0 : 'Unspecified',
      1 : 'CW',
      2 : 'CC',
      3 : 'NONE'
    }
    return values.get(self.gantry_rotation_id, 'Unknown gantry_rotation_id: {}'.format(self.gantry_rotation_id))
  