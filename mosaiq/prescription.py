# encoding: utf8

# A class for reading prescription data from the Mosaiq database.
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
from .field import Field
from .site_setup import SiteSetup

class Prescription:
  
  # Returns a single prescription matching the given database id (SIT_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Site WHERE SIT_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all prescriptions belonging to the given course.
  # Excludes prescriptions with version != 0.
  # Returned prescriptions are sorted by display_sequence (low to high).
  @classmethod
  def for_course(cls, course):
    prescriptions = list()
    rows = Database.fetch_all("SELECT * FROM Site WHERE PCP_ID = '{}' AND Version = '0'".format(course.id))
    for row in rows:
      prescriptions.append(cls(row))
    prescriptions.sort(key=lambda p: p.display_sequence, reverse=False)
    return prescriptions
  
  # Gives all prescriptions belonging to the given patient.
  # Excludes prescriptions with version != 0.
  @classmethod
  def for_patient(cls, patient):
    prescriptions = list()
    rows = Database.fetch_all("SELECT * FROM Site WHERE Pat_ID1 = '{}' AND Version = '0'".format(patient.id))
    for row in rows:
      prescriptions.append(cls(row))
    return prescriptions
  
  # Creates a Prescription instance from a prescription database row.
  def __init__(self, row):
    # Database attributes:
    self.sit_id = row['SIT_ID']
    self.original_prescription_id = row['SIT_SET_ID']
    self.version = row['Version']
    self.patient_id = row['Pat_ID1']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_Id']
    self.note_id = row['Note_ID']
    self.site_name = row['Site_Name']
    self.technique = row['Technique'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.modality = row['Modality']
    self.target = row['Target'].rstrip() # If this crashes sometimes, we have to test if the string exists.
    self.prescription_depth = float(row['Rx_Depth'])
    self.target_units = row['Target_Units']
    self.fraction_dose = int(row['Dose_Tx'])
    self.total_dose = int(row['Dose_Ttl'])
    self.cumulative_dose = int(row['Dose_Ttl_Cum'])
    self.nr_fractions = row['Fractions']
    self.pattern = row['Frac_Pattern']
    self.comment = row['Notes']
    self.display_sequence = row['DisplaySequence']
    self.parent_prescription_id = row['Reference_SIT_Set_ID']
    self.reference_fraction = row['Reference_Fraction']
    self.reference_fraction_offset = row['Reference_Fx_Offset']
    self.course_id = row['PCP_ID']
    self.status_id = row['Status_Enum']
    # Convenience attributes:
    self.id = self.sit_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_child_prescription = None
    self.instance_course = None
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_delivered_doses = None
    self.instance_fields = None
    self.instance_images = None
    self.instance_note = None
    self.instance_parent_prescription = None
    self.instance_patient = None
    self.instance_performed_site_setups = None
    self.instance_original_prescription = None
    self.instance_site_setup = None
   
  # The staff who approved the prescription.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # Gives the prescription (if any) which is related to (e.g. is a boost of) this prescription.
  # If this prescription doesn't have a child prescription, and it has an original_prescription
  # reference, then it returns the child prescription for the original_prescription instead.
  def child_prescription(self):
    if not self.instance_child_prescription:
      row = Database.fetch_one("SELECT * FROM Site WHERE Reference_SIT_Set_ID = '{}'".format(self.id))
      if row != None:
        self.instance_child_prescription = cls(row)
      else:
        if self.original_prescription_id != None:
          self.instance_child_prescription = self.original_prescription().child_prescription()
    return self.instance_child_prescription
  
  # Gives the course which this prescription belongs to.
  def course(self):
    if not self.instance_course:
      self.instance_course = Course.find(self.course_id)
    return self.instance_course
  
  # The staff who created the prescription.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # Gives the delivered_doses (if any) belonging to this prescription.
  # If this prescription doesn't have any delivered_dose references, and it has an original_prescription
  # reference, then it returns delivered_doses for the original_prescription instead.
  def delivered_doses(self):
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_prescription(self)
      if len(self.instance_delivered_doses) == 0 and self.original_prescription_id:
        self.instance_delivered_doses = DeliveredDose.for_prescription(self.original_prescription())
    return self.instance_delivered_doses
  
  # The staff who last edited the prescription.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the fields (if any) belonging to this prescription.
  # If this prescription doesn't have any field references, and it has an original_prescription
  # reference, then it returns fields for the original_prescription instead.
  def fields(self):
    if not self.instance_fields:
      self.instance_fields = Field.for_prescription(self)
      if len(self.instance_fields) == 0 and self.original_prescription_id:
        self.instance_fields = Field.for_prescription(self.original_prescription())
    return self.instance_fields
  
  # Gives the images (if any) belonging to this prescription.
  def images(self):
    if not self.instance_images:
      self.instance_images = Image.for_patient(self)
    return self.instance_images
  
  # Gives the note (if any) associated with this prescription.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the original prescription. If changes has occured to the prescription at some time,
  # then an original prescription record might exist that is different from this one.
  # If no other original precription exists, self is returned.
  def original_prescription(self):
    if not self.instance_original_prescription:
      if self.original_prescription_id == self.id:
        self.instance_original_prescription = self
      else:
        self.instance_original_prescription = Prescription.find(self.original_prescription_id)
    return self.instance_original_prescription
  
  # Gives the prescription (if any) which this prescription is related to (e.g. is a boost of).
  def parent_prescription(self):
    if not self.instance_parent_prescription:
      self.instance_parent_prescription = Prescription.find(self.parent_prescription_id)
    return self.instance_parent_prescription
  
  # Gives the patient which this prescription belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # Gives the performed_site_setups (if any) belonging to this prescription.
  # If this prescription doesn't have any performed_site_setup references, and it has an original_prescription
  # reference, then it returns performed_site_setups for the original_prescription instead.
  def performed_site_setups(self):
    if not self.instance_performed_site_setups:
      self.instance_performed_site_setups = PerformedSiteSetup.for_patient(self)
      if len(self.instance_performed_site_setups) == 0 and self.original_prescription_id:
        self.instance_performed_site_setups = PerformedSiteSetup.for_prescription(self.original_prescription())
    return self.instance_performed_site_setups
  
  # Gives the site setup (if any) which belongs to this prescription.
  # If this prescription doesn't have any site_setup references, and it has an original_prescription
  # reference, then it returns site_setup for the original_prescription instead.
  def site_setup(self):
    if not self.instance_site_setup:
      self.instance_site_setup = SiteSetup.for_prescription(self)
      if not self.instance_site_setup and self.original_prescription_id:
        self.instance_site_setup = SiteSetup.for_prescription(self.original_prescription())
    return self.instance_site_setup

  # The status description derived from the status_id.
  def status(self):
    values = {
      0 : 'Unknown',
      1 : 'VOID',
      2 : 'CLOSE',
      3 : 'COMPLETE',
      4 : 'HOLD',
      5 : 'APPROVE',
      6 : 'PROCESS_LOCK',
      7 : 'PENDING'
    }
    return values.get(self.status_id, 'Unknown status_id: {}'.format(self.status_id))
