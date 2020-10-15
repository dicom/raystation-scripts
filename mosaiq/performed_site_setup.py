# encoding: utf8

# A class for reading performed_site_setup data from the Mosaiq database.
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

class PerformedSiteSetup:
  
  # Returns a single performed_site_setup matching the given database id (SHS_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM SiteSetup_Hst WHERE SHS_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all performed site setups belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    performed_site_setups = list()
    rows = Database.fetch_all("SELECT * FROM SiteSetup_Hst WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      performed_site_setups.append(cls(row))
    return performed_site_setups
  
  # Gives the performed site setup instance belonging to the given prescription.
  @classmethod
  def for_prescription(cls, prescription):
    performed_site_setups = list()
    rows = Database.fetch_all("SELECT * FROM SiteSetup_Hst WHERE SIT_ID = '{}'".format(prescription.id))
    for row in rows:
      performed_site_setups.append(cls(row))
    return performed_site_setups
  
  # Gives the performed site setup instances belonging to the given site setup.
  @classmethod
  def for_site_setup(cls, site_setup):
    performed_site_setups = list()
    rows = Database.fetch_all("SELECT * FROM SiteSetup_Hst WHERE SIS_ID = '{}'".format(site_setup.id))
    for row in rows:
      performed_site_setups.append(cls(row))
    return performed_site_setups
  
  # Creates a PerformedSiteSetup instance from a performed_site_setup database row.
  def __init__(self, row):
    # Database attributes:
    self.shs_id = row['SHS_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.performed_date = row['SHS_DtTm']
    self.performed_by_id = row['Staff_ID']
    self.institution_id = row['Inst_ID']
    self.site_setup_id = row['SIS_ID']
    self.prescription_id = row['SIT_ID']
    self.offset_id = row['OFF_ID']
    self.location_id = row['Machine_ID_Staff_ID']
    self.machine_id = row['MAC_ID']
    self.is_in_patient = row['IsInPatient']
    self.was_qa_mode = row['WasQAMode']
    self.was_verified = row['WasVerified']
    self.was_overridden = row['WasOverridden']
    self.overrides = row['Overrides1']
    self.patient_id = row['Pat_ID1']
    self.patient_verification_status_id = row['PatientVxStatus']
    self.notes = row['Notes']
    # Convenience attributes:
    self.id = self.shs_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_location = None
    self.instance_patient = None
    self.instance_performed_by = None
    self.instance_prescription = None
    self.instance_site_setup = None
    
  # The staff who created the performed_site_setup.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the performed_site_setup.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # The location which this performed_site_setup is associated with.
  def location(self):
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location
  
  # Gives the patient (if any) which is referenced by this performed_site_setup.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # The patient_verification_status description derived from the patient_verification_status_id.
  def patient_verification_status(self):
    values = {
      0 : 'Unknown',
      1 : 'Not Verified',
      2 : 'Barcode Verified',
      3 : 'Manually Verified',
      4 : 'Partially Manually Verified',
      5 : 'Incorrect Patient'
    }
    return values.get(self.patient_verification_status_id, 'Unknown patient_verification_status_id: {}'.format(self.patient_verification_status_id))
  
  # The staff who performed the performed_site_setup.
  def performed_by(self):
    if not self.instance_performed_by:
      self.instance_performed_by = Location.find(self.performed_by_id)
    return self.instance_performed_by
  
  # Gives the prescription which this performed_site_setup belongs to.
  def prescription(self):
    if not self.instance_prescription:
      self.instance_prescription = Prescription.find(self.prescription_id)
    return self.instance_prescription
  
  # Gives the site_setup which this performed_site_setup originates from.
  def site_setup(self):
    if not self.instance_site_setup:
      self.instance_site_setup = SiteSetup.find(self.site_setup_id)
    return self.instance_site_setup
