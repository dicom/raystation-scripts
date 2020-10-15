# encoding: utf8

# A class for reading activity data from the Mosaiq database.
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

class Activity:
  
  # Returns a single activity matching the given database id (PRS_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM CPT WHERE PRS_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Returns a single activity matching the given activity code (or nil if no match).
  @classmethod
  def find_by_code(cls, hsp_code):
    instance = None
    if len(hsp_code) > 0:
      row = Database.fetch_one("SELECT * FROM CPT WHERE Hsp_Code = '{}'".format(str(hsp_Code)))
      if row != None:
        instance = cls(row)
    return instance

  # Creates a Activity instance from a activity database row.
  def __init__(self, row):
    # Database attributes:
    self.prs_id = row['PRS_ID']
    self.inactive = row['Status_Inactive']
    self.code_group = row['CGroup'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.code1 = row['Hsp_Code']
    self.code2 = row['Hsp_Code1']
    self.code3 = row['Hsp_Code2']
    self.code4 = row['Hsp_Code3']
    self.code5 = row['Hsp_Code4']
    self.code6 = row['Hsp_Code5']
    self.charge_code = row['CPT_Code'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.abbreviation = row['Tiny_Desc'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.title = row['Short_Desc']
    self.description = row['Description']
    self.deleted = row['Deleted']
    self.color = row['ScheduleColor']
    # Convenience attributes:
    self.id = self.prs_id
