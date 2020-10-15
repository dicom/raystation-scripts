# encoding: utf8

# A class for reading offset data from the Mosaiq database.
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

class Offset:
  
  # Returns a single offset matching the given database id (OFF_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Offset WHERE OFF_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives the offset instance belonging to the given location/staff.
  @classmethod
  def for_location(cls, location):
    offsets = list()
    rows = Database.fetch_all("SELECT * FROM Offset WHERE Create_ID = '{}'".format(location.id))
    for row in rows:
      offsets.append(cls(row))
    return offsets
  
  # Gives the offset instances belonging to the given site setup.
  @classmethod
  def for_site_setup(cls, site_setup):
    offsets = list()
    rows = Database.fetch_all("SELECT * FROM Offset WHERE Sit_Set_ID = '{}'".format(site_setup.id))
    for row in rows:
      offsets.append(cls(row))
    return offsets
  
  # Creates a Offset instance from a offset database row.
  def __init__(self, row):
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
    
  # The staff who created the offset.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the offset.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # The image_source description derived from the image_source_id.
  def image_source(self):
    values = {
      0 : 'Unknown',
      1 : '2D',
      2 : 'Orthogonal Pair',
      3 : '3D'
    }
    return values.get(self.image_source_id, 'Unknown image_source_id: {}'.format(self.image_source_id))
  
  # Gives the site_setup which this offset originates from.
  # FIXME: For some reason, in some cases we dont find a SiteSetup instance
  # from this record's @site_setup_id. It might be in cases where Site Setup has been modified?!
  # OR it might have to do with Version != 0 (look at Prescription class for this phenomena)
  def site_setup(self):
    if not self.instance_site_setup:
      self.instance_site_setup = SiteSetup.find(self.site_setup_id)
    return self.instance_site_setup
  
  # The state description derived from the state_id.
  def state(self):
    values = {
      0 : 'Reset',
      1 : 'Active',
      2 : 'Complete',
      3 : 'Excluded'
    }
    return values.get(self.state_id, 'Unknown state_id: {}'.format(self.state_id))
  
  # The type description derived from the type_id.
  def type(self):
    values = {
      0 : 'Unknown',
      1 : 'Prescribed Relative Offset',
      2 : 'Localization',
      3 : 'Session',
      4 : 'Third Party'
    }
    return values.get(self.type_id, 'Unknown type_id: {}'.format(self.type_id))
  