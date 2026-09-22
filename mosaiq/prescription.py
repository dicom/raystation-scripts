# Import local files:
from .database import Database
from .field import Field
from .site_setup import SiteSetup
from .offset import Offset

class Prescription:
  """A class for reading prescription data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Site table corresponding to the given id.

    Args:
      id (str or int): The primary database id (SIT_ID) of the row to be extracted.

    Returns:
      Prescription: A new instance of the Prescription class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Site WHERE SIT_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_course(cls, course):
    """Extracts all prescriptions belonging to the given course.

    Note that non-current prescriptions are excluded (Version != 0).

    Args:
      course (Course): The course instance for which to extract associated prescription rows.

    Returns:
      List[Prescription]: A list of prescriptions belonging to the given course,
        sorted by display_sequence (low to high).
    """
    prescriptions = list()
    rows = Database.fetch_all("SELECT * FROM Site WHERE PCP_ID = '{}' AND Version = '0'".format(course.id))
    for row in rows:
      prescriptions.append(cls(row))
    prescriptions.sort(key=lambda p: p.display_sequence, reverse=False)
    return prescriptions

  @classmethod
  def for_patient(cls, patient):
    """Extracts all prescriptions belonging to the given patient.

    Note that non-current prescriptions are excluded (Version != 0).

    Args:
      patient (Patient): The patient instance for which to extract associated prescription rows.

    Returns:
      List[Prescription]: A list of prescriptions belonging to the given patient.
    """
    prescriptions = list()
    rows = Database.fetch_all("SELECT * FROM Site WHERE Pat_ID1 = '{}' AND Version = '0'".format(patient.id))
    for row in rows:
      prescriptions.append(cls(row))
    return prescriptions

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Site table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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
    self.technique = row['Technique'].rstrip()
    self.modality = row['Modality']
    self.target = row['Target'].rstrip()
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
    self.instance_prescribed_offset = None
    self.instance_original_prescription = None
    self.instance_site_setup = None
    self.instance_third_party_offsets = None

  def approved_by(self):
    """Gives the staff who approved the prescription.

    Returns:
      Location: The location (staff) who approved this prescription.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def child_prescription(self):
    """Gives the prescription (if any) which is related to (e.g. is a boost of) this prescription.

    Note that if this prescription doesn't have a child prescription, and it has an original_prescription
    reference, then it returns the child prescription for the original_prescription instead.

    Returns:
      Prescription: The prescription (if any) which is related to this prescription.
    """
    if not self.instance_child_prescription:
      row = Database.fetch_one("SELECT * FROM Site WHERE Reference_SIT_Set_ID = '{}'".format(self.id))
      if row != None:
        self.instance_child_prescription = cls(row)
      else:
        if self.original_prescription_id != None:
          self.instance_child_prescription = self.original_prescription().child_prescription()
    return self.instance_child_prescription

  def course(self):
    """Gives the course which this prescription belongs to.

    Returns:
      Course: The course which this prescription belongs to.
    """
    if not self.instance_course:
      self.instance_course = Course.find(self.course_id)
    return self.instance_course

  def created_by(self):
    """Gives the staff who created the prescription.

    Returns:
      Location: The location (staff) who created this prescription.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def delivered_doses(self):
    """Gives the delivered_doses (if any) associated with this prescription.

    Note that if this prescription doesn't have any delivered dose references, and it has an original_prescription
    reference, then it returns delivered_doses for the original_prescription instead.

    Returns:
      List[DeliveredDose]: The delivered_doses associated with this prescription, or an empty list.
    """
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_prescription(self)
      if len(self.instance_delivered_doses) == 0 and self.original_prescription_id:
        self.instance_delivered_doses = DeliveredDose.for_prescription(self.original_prescription())
    return self.instance_delivered_doses

  def edited_by(self):
    """Gives the staff who last edited the prescription.

    Returns:
      Location: The location (staff) who edited this prescription.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def fields(self):
    """Gives the fields (if any) associated with this prescription.

    Note that if this prescription doesn't have any field references, and it has an original_prescription
    reference, then it returns fields for the original_prescription instead.

    Returns:
      List[Field]: The fields associated with this prescription, or an empty list.
    """
    if not self.instance_fields:
      self.instance_fields = Field.for_prescription(self)
      if len(self.instance_fields) == 0 and self.original_prescription_id:
        self.instance_fields = Field.for_prescription(self.original_prescription())
    return self.instance_fields

  def images(self):
    """Gives the images (if any) associated with this prescription.

    Returns:
      List[Image]: The images associated with this prescription, or an empty list.
    """
    if not self.instance_images:
      self.instance_images = Image.for_patient(self)
    return self.instance_images

  def note(self):
    """Gives the note (if any) associated with this prescription.

    Returns:
      Note: The note associated with this prescription, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def original_prescription(self):
    """Gives the original prescription.

    If changes has occured to the prescription at some time, then an original prescription record
    might exist that is different from this one. If no other original precription exists, self is returned.

    Returns:
      Prescription: The prescription which this prescription is related to.
    """
    if not self.instance_original_prescription:
      if self.original_prescription_id == self.id:
        self.instance_original_prescription = self
      else:
        self.instance_original_prescription = Prescription.find(self.original_prescription_id)
    return self.instance_original_prescription

  def parent_prescription(self):
    """Gives the prescription (if any) which this prescription is related to (e.g. is a boost of).

    Returns:
      Prescription: The prescription which this prescription is related to.
    """
    if not self.instance_parent_prescription:
      self.instance_parent_prescription = Prescription.find(self.parent_prescription_id)
    return self.instance_parent_prescription

  def patient(self):
    """Gives the patient which this prescription belongs to.

    Returns:
      Patient: The patient which this prescription belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def performed_site_setups(self):
    """Gives the performed site setups (if any) which belongs to this prescription.

    Note that if this prescription doesn't have any performed_site_setup references, and it has an original_prescription
    reference, then it returns performed_site_setups for the original_prescription instead.

    Returns:
      List[PerformedSiteSetup]: A list of performed site setups belonging to this prescription, or an empty list.
    """
    if not self.instance_performed_site_setups:
      self.instance_performed_site_setups = PerformedSiteSetup.for_prescription(self)
      if len(self.instance_performed_site_setups) == 0 and self.original_prescription_id:
        self.instance_performed_site_setups = PerformedSiteSetup.for_prescription(self.original_prescription())
    return self.instance_performed_site_setups

  def prescribed_offset(self):
    """Gives the prescribed offset for this prescription.

    Returns:
      Offset: The offset for this prescription.
    """
    if not self.instance_prescribed_offset:
      offsets = Offset.for_prescription(self, type=1)
      if len(offsets) > 0:
        self.instance_prescribed_offset = offsets[0]
      if len(offsets) == 0 and self.original_prescription_id:
        offsets = Offset.for_prescription(self.original_prescription(), type=1)
        if len(offsets) > 0:
          self.instance_prescribed_offset = offsets[0]
    return self.instance_prescribed_offset

  def site_setup(self):
    """Gives the site_setup (if any) which belongs to this prescription.

    Note that if this prescription doesn't have any site_setup references, and it has an
    original_prescription reference, then it returns site_setup for the original_prescription instead.

    Returns:
      SiteSetup: The site_setup belonging to this prescription.
    """
    if not self.instance_site_setup:
      self.instance_site_setup = SiteSetup.for_prescription(self)
      if not self.instance_site_setup and self.original_prescription_id:
        self.instance_site_setup = SiteSetup.for_prescription(self.original_prescription())
    return self.instance_site_setup

  def status(self):
    """The status description derived from the status_id.

    Returns:
      str: The status description (e.g. 'PENDING').
    """
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

  def third_party_offsets(self):
    """Gives the third party offsets (e.g. CBCT offsets) (if any) for this prescription.

    Returns:
      List[Offset]: The offsets associated with this prescription, or an empty list.
    """
    if not self.instance_third_party_offsets:
      self.instance_third_party_offsets = Offset.for_prescription(self, type=4)
      if len(self.instance_third_party_offsets) == 0 and self.original_prescription_id:
        self.instance_third_party_offsets = Offset.for_prescription(self.original_prescription(), type=4)
    return self.instance_third_party_offsets
