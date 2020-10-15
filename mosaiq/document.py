# encoding: utf8

# A class for reading document data from the Mosaiq database.
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

class Document:
  
  # Returns a single document matching the given database id (OBJ_ID) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Object WHERE OBJ_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all documents belonging to the given patient.
  @classmethod
  def for_patient(cls, patient):
    documents = list()
    rows = Database.fetch_all("SELECT * FROM Object WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      documents.append(cls(row))
    return documents
  
  # Creates a Document instance from a document database row.
  def __init__(self, row):
    # Database attributes:
    self.obj_id = row['OBJ_ID']
    self.patient_id = row['Pat_ID1']
    self.file_number = row['Filenum']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.type_id = row['DocType']
    self.file_format_id = row['File_Format']
    self.note_id = row['Note_ID']
    self.status_id = row['Status_Enum']
    self.document_id = row['OBJ_SET_ID']
    self.version = row['Version']
    self.institution_id = row['Inst_ID']
    # Convenience attributes:
    self.id = self.obj_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_file_name = None
    self.instance_note = None
    self.instance_nr_pages = None
    self.instance_patient = None
    
  # The staff who approved the document.
  def approved_by(self):
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by
  
  # The staff who created the document.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the document.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  # The file_format description derived from the file_format_id.
  def file_format(self):
    values = {
      0 : 'Word_Perfect',
      2 : 'PhastNote',
      4 : 'ScanDoc',
      5 : 'Word_Doc',
      6 : 'Interface_Image',
      7 : 'Tx_Plan',
      8 : 'Interface_RTF',
      9 : 'Field_Document'
    }
    return values.get(self.file_format_id, 'Unknown file_format_id: {}'.format(self.file_format_id))
  
  # The file name of the document.
  def file_name(self):
    if not self.instance_file_name:
      row = Database.fetch_one("SELECT * FROM ObjFilenames WHERE OBJ_ID = '{}'".format(str(id)))
      if row != None:
        self.instance_file_name = row['eSCANFilename']
    return self.instance_file_name
  
  # Gives the note (if any) associated with this document.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # The number of pages of the document.
  def nr_pages(self):
    if not self.instance_nr_pages:
      row = Database.fetch_one("SELECT * FROM ObjFilenames WHERE OBJ_ID = '{}'".format(str(id)))
      if row != None:
        self.instance_nr_pages = row['PageNumber']
    return self.instance_nr_pages
  
  # Gives the patient which this document belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  # The status of the document.
  def status(self):
    values = {
      0 : 'Unknown',
      1 : 'Void',
      2 : 'Close',
      3 : 'Complete',
      4 : 'Hold',
      5 : 'Approved',
      6 : 'Process_Lock',
      7 : 'Pending',
      8 : 'Signed',
      9 : 'Cosigned_Approved',
      10 : 'Obj_Transcription_Req',
      11 : 'Obj_Dictation_Req',
      12 : 'Obj_Edit_Req',
      13 : 'Obj_Review_Req',
      14 : 'Obj_Signature_Req',
      16 : 'Unreviewed',
      17 : 'Reviewed',
      20 : 'Partial Approval'
    }
    return values.get(self.status_id, 'Unknown status_id: {}'.format(self.status_id))
