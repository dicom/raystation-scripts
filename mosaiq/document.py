# Import system libraries:
import os

# Import local files:
from .database import Database

class Document:
  """A class for reading document data from the Mosaiq database."""

  # The Mosaiq document file share path:
  path = open(r'C:\temp\raystation-scripts\mosaiq\document_path.txt', "r").read()

  @classmethod
  def find(cls, id):
    """Finds the row in the Object table corresponding to the given id.

    Args:
      id (str or int): The primary database id (OBJ_ID) of the row to be extracted.

    Returns:
      Document: A new instance of the Document class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Object WHERE OBJ_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient, type_id=None):
    """Extracts all documents belonging to the given patient.

    Args:
      patient (Patient): The patient instance for which to extract associated document rows.
      type_id (int, optional): A specific document type for which to restrict the query. Defaults to None.

    Returns:
      List[Document]: A list of documents belonging to the given patient.
    """
    query = "SELECT * FROM Object WHERE Pat_ID1 = '{}'".format(patient.id)
    if type_id is not None:
      query += " AND DocType = '{}'".format(type_id)
    documents = list()
    rows = Database.fetch_all(query)
    for row in rows:
      documents.append(cls(row))
    return documents

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Object table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def approved_by(self):
    """Gives the staff who approved the document.

    Returns:
      Location: The location (staff) who approved this document.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def created_by(self):
    """Gives the staff who created the document.

    Returns:
      Location: The location (staff) who created this document.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the document.

    Returns:
      Location: The location (staff) who edited this document.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def file_format(self):
    """The file_format description as derived from the file_format_id.

    Returns:
      str: The file_format description (e.g. 'ScanDoc').
    """
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

  def file_name(self):
    """Gives the file name of the document.

    Returns:
      str: The file name of the document.
    """
    if not self.instance_file_name:
      row = Database.fetch_one("SELECT * FROM ObjFilenames WHERE OBJ_ID = '{}'".format(str(self.id)))
      if row != None:
        self.instance_file_name = row['eSCANFilename']
    return self.instance_file_name

  def file_path(self):
    """Gives the full file path of the document.

    Note that the full file path is constructed from 3 components:
    The first part is the root path, as defined in document_path.txt and given by the Document.path parameter.
    The middle part is based on processing parts of the patient's ID and file number.
    The third part is the file name, as given by the file_name() function.
    The full path may look something like this:
    \\FILESHARE\MOSAIQ_DATA\DB\ESCRIBE\19\0000AD0B.003\20260942326297_221.pdf

    Returns:
      str: The full file path of the document.
    """
    # Extract the components used for the middle part:
    last_digit = str(self.patient().id)[-1]
    next_last_digit = str(self.patient().id)[-2]
    binary = str(int(next_last_digit) % 2)
    id_hex = f"{self.patient().id:X}"
    id_prefix = "0" * (8 - len(id_hex))
    file_nr_padding = "0" * (3 - len(str(self.file_number)))
    # Build the middle part:
    mid1 = binary + last_digit
    mid2 = id_prefix + id_hex + "." + file_nr_padding + str(self.file_number)
    # Build the full path:
    path = os.path.join(Document.path, mid1, mid2, self.file_name())
    return path

  def note(self):
    """Gives the note (if any) associated with this document.

    Returns:
      Note: The note associated with this document, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def nr_pages(self):
    """Gives the number of pages of the document.

    Returns:
      int: The number of pages of the document.
    """
    if not self.instance_nr_pages:
      row = Database.fetch_one("SELECT * FROM ObjFilenames WHERE OBJ_ID = '{}'".format(str(self.id)))
      if row != None:
        self.instance_nr_pages = row['PageNumber']
    return self.instance_nr_pages

  def patient(self):
    """Gives the patient which this document belongs to.

    Returns:
      Patient: The patient which this document belongs to.
    """
    from .patient import Patient
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def status(self):
    """The status of the document as derived from the status_id.

    Returns:
      str: The document status (e.g. 'Approved').
    """
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
