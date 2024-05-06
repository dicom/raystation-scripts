# encoding: utf8

# A class for reading site_setup data from the Mosaiq database.
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
from .location import Location
from .offset import Offset
from .performed_site_setup import PerformedSiteSetup

class SiteSetup:
  
  # Returns a single site_setup matching the given database id (SIS_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM SiteSetup WHERE SIS_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives the site setup instance belonging to the given prescription.
  @classmethod
  def for_prescription(cls, prescription):
    instance = None
    row = Database.fetch_one("SELECT * FROM SiteSetup WHERE Sit_Set_ID = '{}'".format(prescription.id))
    if row != None:
      instance = cls(row)
    return instance
  
  # Creates a SiteSetup instance from a site_setup database row.
  def __init__(self, row):
    # Database attributes:
    self.sis_id = row['SIS_ID']
    self.site_setup_id = row['SIS_Set_ID']
    self.version = row['Version']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.prescription_id = row['Sit_Set_ID']
    self.patient_orientation_id = row['Patient_Orient']
    self.prescribed_offset_id = row['Off_Set_ID']
    self.description = row['Setup_Technique_Description']
    self.iso_x = float(row['Isocenter_Position_X'])
    self.iso_y = float(row['Isocenter_Position_Y'])
    self.iso_z = float(row['Isocenter_Position_Z'])
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.status_id = row['Status_Enum']
    self.note = row['Setup_Note']
    self.tolerance_id = row['TOL_ID']
    self.name = row['Setup_Name']
    self.couch_vertical = float(row['Couch_Vrt'])
    self.couch_lateral = float(row['Couch_Lat'])
    self.couch_longitudinal = float(row['Couch_Lng'])
    self.location_id = row['Machine_ID_Staff_ID']
    self.frame_of_reference_uid = row['Frame_Of_Reference_UID']
    self.structure_set_uid = row['Structure_Set_UID']
    self.couch_max_tolerance_id = row['MAX_TOL_ID']
    self.couch_threshold_tolerance_id = row['THR_TOL_ID']
    self.machine_id = row['MAC_ID']
    self.is_excluded_from_treatment = row['IsExcludedFromTreatment']
    # Convenience attributes:
    self.id = self.sis_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_created_by_by = None
    self.instance_edited_by = None
    self.instance_location = None
    self.instance_offsets = None
    self.instance_performed_site_setups = None
    self.instance_prescribed_offset = None
    self.instance_prescription = None

  # The staff who approved the site_setup.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
   
  # The staff who created the site_setup.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the site_setup.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # The location which this site_setup is associated with.
  def location(self):
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location
  
  # Gives the offsets (if any) associated with this site_setup.
  def offsets(self):
    if not self.instance_offsets:
      self.instance_offsets = Offset.for_site_setup(self)
    return self.instance_offsets
  
  # Gives the performed_site_setups (if any) associated with this site_setup.
  def performed_site_setups(self):
    if not self.instance_performed_site_setups:
      self.instance_performed_site_setups = PerformedSiteSetup.for_site_setup(self)
    return self.instance_performed_site_setups
  
  # Gives the prescribed offset for this site setup.
  def prescribed_offset(self):
    if not self.instance_prescribed_offset:
      self.instance_prescribed_offset = Offset.find(self.prescribed_offset_id)
    return self.instance_prescribed_offset
  
  # Gives the prescription which this site_setup belongs to.
  def prescription(self):
    if not self.instance_prescription:
      self.instance_prescription = Prescription.find(self.prescription_id)
    return self.instance_prescription
  
  # The status description derived from the status_id.
  def status(self):
    values = {
      5 : 'Approved',
      7 : 'Pending'
    }
    return values.get(self.status_id, 'Unknown status_id: {}'.format(self.status_id))
    