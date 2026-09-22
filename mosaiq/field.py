# Import local files:
from .control_point import ControlPoint
from .database import Database
from .scheduled_field import ScheduledField

class Field:
  """A class for reading field data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the TxField table corresponding to the given id.

    Args:
      id (str or int): The primary database id (FLD_ID) of the row to be extracted.

    Returns:
      Field: A new instance of the Field class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM TxField WHERE FLD_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def find_current(cls, id):
    """Finds the current field row in the TxField table, given the original row/instance database id.

    Note that non-current fields are excluded (Version != 0).

    Args:
      id (str or int): The primary database id (FLD_SET_ID) of the row to be extracted.

    Returns:
      Field: A new instance of the Field class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM TxField WHERE FLD_SET_ID = '{}' AND Version = '0'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    """Extracts all fields belonging to the given patient.

    Note that non-current fields are excluded (Version != 0).

    Args:
      patient (Patient): The patient instance for which to extract associated field rows.

    Returns:
      List[Field]: A list of fields belonging to the given patient.
    """
    fields = list()
    rows = Database.fetch_all("SELECT * FROM TxField WHERE Pat_ID1 = '{}' AND Version = '0'".format(patient.id))
    for row in rows:
      fields.append(cls(row))
    return fields

  @classmethod
  def for_prescription(cls, prescription):
    """Extracts all fields belonging to the given prescription.

    Note that non-current fields are excluded (Version != 0).

    Args:
      prescription (Prescription): The prescription instance for which to extract associated field rows.

    Returns:
      List[Field]: A list of fields belonging to the given prescription, sorted by created date (oldest fields first).
    """
    fields = list()
    rows = Database.fetch_all("SELECT * FROM TxField WHERE SIT_Set_ID = '{}' AND Version = '0'".format(prescription.id))
    for row in rows:
      fields.append(cls(row))
    fields.sort(key=lambda f: f.created_date, reverse=False)
    return fields

  # Creates a Field instance from a field database row.
  def __init__(self, row):
    """Initializes an instance from a row extracted from the TxField table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.fld_id = row['FLD_ID']
    self.original_field_id = row['FLD_SET_ID']
    self.version = row['Version']
    self.patient_id = row['Pat_ID1']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.prescription_id = row['SIT_Set_ID']
    self.label = row['Field_Label']
    self.name = row['Field_Name']
    self.location_id = row['Machine_ID_Staff_ID']
    self.machine_id = row['MachineCharID']
    self.first_treated_date = row['Start_DtTm']
    self.last_treated_date = row['Last_Tx_DtTm']
    self.nr_fractions_treated = row['Fractions_Tx']
    self.dose = float(row['Cgray'])
    self.epid = row['PIAcqDevice']
    self.tolerance_id = row['Tol_Tbl_ID']
    self.applicator = row['Wdg_Appl'].rstrip()
    self.fda = row['Comp_Fda'].rstrip()
    self.ssd = float(row['Ssd'])
    self.mlc = row['Mlc']
    self.image_id = row['IMG_ID']
    self.notes = row['Notes']
    self.is_hidden = row['IsHidden']
    self.delivered_dose_id = row['TxFromDHS_ID']
    self.beam_type_id = row['Beam_Type_Flag']
    self.type_id = row['Type_Enum']
    self.modality_id = row['Modality_Enum']
    self.nr_control_points = row['ControlPoints']
    self.original_plan_uid = row['OriginalPlanUID'].rstrip()
    self.meterset = float(row['Meterset'])
    self.is_fff = row['IsFFF']
    self.xvi_preset = row['XVI_Preset']
    self.xvi_preset_type_id = row['XVI_PresetType_Enum']
    # Convenience attributes:
    self.id = self.fld_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_control_points = None
    self.instance_current_field = None
    self.instance_created_by = None
    self.instance_delivered_doses = None
    self.instance_edited_by = None
    self.instance_images = None
    self.instance_patient = None
    self.instance_prescription = None
    self.instance_original_field = None
    self.instance_scheduled_fields = None

  def approved_by(self):
    """Gives the staff who approved the field.

    Returns:
      Location: The location (staff) who approved this field.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def beam_type(self):
    """The beam_type description derived from the beam_type_id.

    Returns:
      str: The beam type description (e.g. 'Dynamic').
    """
    values = {
      0 : 'Unspecified',
      1 : 'Static',
      2 : 'Dynamic'
    }
    return values.get(self.beam_type_id, 'Unknown beam_type_id: {}'.format(self.beam_type_id))

  def control_points(self):
    """Gives the control_points (if any) belonging to this field.

    Returns:
      List[ControlPoint]: The control_points belonging to this field, or an empty list.
    """
    if not self.instance_control_points:
      self.instance_control_points = ControlPoint.for_field(self)
    return self.instance_control_points

  def created_by(self):
    """Gives the staff who created the field.

    Returns:
      Location: The location (staff) who created this field.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def current_field(self):
    """Gives the current version of this field record.

    If changes has occured to the field at some time, then a current field record might exist which has
    deprecated this one. If no other (later) field record exists (version=0) for this field, self is returned.

    Returns:
      Field: The current version of this field.
    """
    if not self.instance_current_field:
      if self.version == 0:
        self.instance_current_field = self
      else:
        self.instance_current_field = Field.find_current(self.id)
    return self.instance_current_field

  def delivered_doses(self):
    """Gives the delivered_doses (if any) belonging to this field.

    Returns:
      List[DeliveredDose]: The delivered_doses belonging to this field, or an empty list.
    """
    if not self.instance_delivered_doses:
      self.instance_delivered_doses = DeliveredDose.for_field(self)
    return self.instance_delivered_doses

  def edited_by(self):
    """Gives the staff who last edited the field.

    Returns:
      Location: The location (staff) who edited this field.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def images(self):
    """Gives the images (if any) associated with this field.

    Returns:
      List[Image]: The images associated with this field, or an empty list.
    """
    if not self.instance_images:
      self.instance_images = Image.for_field(self)
    return self.instance_images

  def modality(self):
    """The modality description derived from the modality_id.

    Returns:
      str: The modality description (e.g. 'X-rays').
    """
    values = {
      0 : 'Unspecified',
      1 : 'X-rays',
      2 : 'Electrons',
      3 : 'Co-60',
      4 : 'Ortho',
      5 : 'E/HD',
      6 : 'Protons',
      7 : 'kV (orthovoltage)',
      8 : 'Ir-192',
      9 : 'Ion',
      20 : 'UserDefined'
    }
    return values.get(self.modality_id, 'Unknown modality_id: {}'.format(self.modality_id))

  def original_field(self):
    """Gives the original field.

    If changes has occured to the field at some time, then an original field record might exist which is
    different from this one. If no other original field exists, self is returned.

    Returns:
      Field: The original field.
    """
    if not self.instance_original_field:
      if self.original_field_id == self.id:
        self.instance_original_field = self
      else:
        self.instance_original_field = Field.find(self.original_field_id)
    return self.instance_original_field

  def patient(self):
    """Gives the patient which this field belongs to.

    Returns:
      Patient: The patient which this field belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def prescription(self):
    """Gives the prescription which this field belongs to.

    Returns:
      Prescription: The prescription which this field belongs to.
    """
    if not self.instance_prescription:
      self.instance_prescription = Prescription.find(self.prescription_id)
    return self.instance_prescription

  def scheduled_fields(self):
    """Gives the scheduled_fields (if any) associated with this field.

    Returns:
      List[ScheduledField]: The scheduled_fields associated with this field, or an empty list.
    """
    if not self.instance_scheduled_fields:
      self.instance_scheduled_fields = ScheduledField.for_field(self)
    return self.instance_scheduled_fields

  def type(self):
    """The type description derived from the type_id.

    Returns:
      str: The type description (e.g. 'VMAT').
    """
    values = {
      0 : 'Unspecified',
      1 : 'Static',
      2 : 'StepNShoot',
      3 : 'Setup',
      4 : 'kV Setup',
      5 : 'CT',
      6 : 'Port',
      7 : 'Fixed (legacy - hx only',
      8 : 'Dynamic (legacy)',
      9 : 'MV CT',
      11 : 'Arc',
      12 : 'Skip Arcs',
      13 : 'VMAT',
      14 : 'DMLC',
      15 : 'Helical',
      16 : 'Fixed Angle',
      17 : 'Path',
      18 : 'Shot',
      20 : 'User Defined',
      21 : 'PDR'
    }
    return values.get(self.type_id, 'Unknown type_id: {}'.format(self.type_id))

  def xvi_preset_type(self):
    """The xvi_preset_type description derived from the xvi_preset_type_id.

    Returns:
      str: The xvi_preset_type description (e.g. 'CT').
    """
    values = {
      0 : 'Unspecified',
      1 : 'CT',
      2 : 'kV Setup',
      3 : 'MotionView',
      4 : 'CT During',
      5 : 'kV During',
      6 : 'MotionView During'
    }
    return values.get(self.xvi_preset_type_id, 'Unknown xvi_preset_type_id: {}'.format(self.xvi_preset_type_id))
