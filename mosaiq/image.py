# encoding: utf8

# A class for reading image data from the Mosaiq database.
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

class Image:
  
  # Returns a single image matching the given database id (IMG_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Image WHERE IMG_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all images belonging to the given field.
  @classmethod
  def for_field(cls, location):
    images = list()
    rows = Database.fetch_all("SELECT * FROM Image WHERE Fld_Set_ID = '{}'".format(location.id))
    for row in rows:
      images.append(cls(row))
    return images
  
  # Gives all images belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    images = list()
    rows = Database.fetch_all("SELECT * FROM Image WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      images.append(cls(row))
    return images
  
  # Gives all images belonging to the given prescription.
  @classmethod
  def for_prescription(cls, prescription):
    images = list()
    rows = Database.fetch_all("SELECT * FROM Image WHERE SIT_Set_id = '{}'".format(prescription.id))
    for row in rows:
      images.append(cls(row))
    return images
  
  # Creates a Image instance from a image database row.
  def __init__(self, row):
    # Database attributes:
    self.img_id = row['IMG_ID']
    self.field_id = row['Fld_Set_ID']
    self.patient_id = row['Pat_ID1']
    self.prescription_id = row['SIT_Set_id']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.approved_date = row['Att_App_DtTm']
    self.approved_by_id = row['Att_Apper_ID']
    self.field_reference_image = row['IMG_Status_TxDefinition_Enabled']
    self.number = row['Image_Num']
    self.image_class_id = row['Image_Class']
    self.title = row['Short_Name']
    self.storage_id = row['Storage_ID']
    self.dicom_series_id = row['DCMSeries_ID']
    self.name = row['Image_Name']
    self.machine_name = row['Machine_Name']
    self.location_id = row['Machine_ID_Staff_ID']
    self.institution_id = row['Inst_ID']
    self.comment = row['Comments']
    self.approval_status_id = row['Att_App']
    self.archived = row['Archived']
    self.offset_id = row['Off_Set_ID']
    self.imager = row['Imager_Name']
    self.isocenter = row['IsocenterPosition']
    self.image_type_id = row['Image_Type']
    self.treatment_associated = row['IMG_Status_Associated']
    # Convenience attributes:
    self.id = self.img_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_field = None
    self.instance_location = None
    self.instance_offset = None
    self.instance_patient = None
    self.instance_prescription = None
    
  # The approval status of the image.
  def approval_status(self):
    values = {
      0 : 'Staff review complete: Rejected',
      1 : 'Staff review complete: Approved',
      2 : 'Staff review required but NOT completed',
      3 : 'Staff review NOT required'
    }
    return values.get(self.approval_status_id, 'Unknown approval_status_id: {}'.format(self.approval_status_id))
  
  # The staff who approved the image.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # The staff who created the image.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the image.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # Gives the field which this image belongs to.
  def field(self):
    if not self.instance_field:
      self.instance_field = Field.find(self.field_id)
    return self.instance_field
  
  # The image_class description derived from the image_class_id.
  def image_class(self):
    values = {
      0 : 'Unknown',
      1 : 'Medical Image',
      2 : 'ID Photo',
      3 : 'Field Setup Photo',
      4 : 'Diagram',
      5 : 'Document',
      6 : 'CT',
      7 : 'MR',
      8 : 'Simulator',
      9 : 'Portal',
      10 : 'Radiograph',
      11 : 'DRR',
      12 : 'Isodose',
      13 : 'Setup Verification',
      14 : 'Ultrasound',
      15 : 'PET',
      16 : '3D CBCT',
      17 : '4D CBCT',
      18 : 'Motion View'
    }
    return values.get(self.image_class_id, 'Unknown image_class_id: {}'.format(self.image_class_id))
  
  # The image_type description derived from the image_type_id.
  def image_type(self):
    values = {
      0 : 'Unknown',
      1 : 'Medical Image',
      2 : 'ID Photo',
      3 : 'Field Setup Photo',
      4 : 'Diagram',
      5 : 'Document'
    }
    return values.get(self.image_type_id, 'Unknown image_type_id: {}'.format(self.image_type_id))
  
  # The location which this image is associated with.
  def location(self):
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location
  
  # Gives the offset (if any) which is related from this image.
  def offset(self):
    if not self.instance_offset:
      self.instance_offset = Offset.find(self.offset_id)
    return self.instance_offset
  
  # Gives the patient which this image belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  # Gives the prescription which this image belongs to.
  def prescription(self):
    if not self.instance_prescription:
      self.instance_prescription = Prescription.find(self.prescription_id)
    return self.instance_prescription
  
  