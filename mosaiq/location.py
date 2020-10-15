# encoding: utf8

# A class for reading location data (Staff/Machine) from the Mosaiq database.
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

class Location:
  
  # Returns a single location (Staff/Machine) matching the given database id (Staff_ID) (or nil if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Staff WHERE Staff_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Extracts all locations (Staff/Machine) matching the given name. Note that the match is exact.
  @classmethod
  def find_by_name(cls, last_name="", first_name=""):
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
  
  # Creates a Location instance (Staff/Machine) from a location database row.
  def __init__(self, row):
    # Database attributes:
    self.staff_id = row['Staff_ID']
    self.created_date = row['Create_DtTm']
    self.initials = row['Initials'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.user_name = row['User_Name'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.code = row['Code'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.type = row['Type'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.last_name = row['Last_Name'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.first_name = row['First_Name']
    self.middle_initial = row['Mdl_Initial'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.deleted = row['Deleted']
    self.inactive = row['Status_inactive']
    self.login = row['Status_Login']
    self.unapproved = row['Status_Unaprv']
    self.password = row['PasswordBytes'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    # Convenience attributes:
    self.id = self.staff_id
    # Cache attributes:
    self.instance_institution_id = None

  # Gives the institution_id of this location (Staff/Machine).
  def institution_id(self):
    if not self.instance_institution_id:
      row = Database.fetch_one("SELECT * FROM StfDept WHERE Staff_ID = '{}'".format(str(self.staff_id)))
      if row != None:
        self.instance_institution_id = row['Inst_ID']
    return self.instance_institution_id
    
  # Returns name formatted as "last_name, first_name middle_name"
  def full_name(self):
    name = self.last_name.rstrip()
    if len(first_name > 0):
      name = "{}, {} {}".format(name, self.first_name, self.middle_name).rstrip()
    return name
  