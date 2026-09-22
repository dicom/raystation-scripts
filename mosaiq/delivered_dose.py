# Import local files:
from .database import Database

class DeliveredDose:
  """A class for reading delivered dose data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Dose_Hst table corresponding to the given id.

    Args:
      id (str or int): The primary database id (DHS_ID) of the row to be extracted.

    Returns:
      DeliveredDose: A new instance of the DeliveredDose class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Dose_Hst WHERE DHS_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_field(cls, field):
    """Extracts all delivered doses belonging to the field.

    Args:
      field (Field): The field instance for which to extract associated delivered dose rows.

    Returns:
      List[DeliveredDose]: A list of delivered doses belonging to the given field.
    """
    delivered_doses = list()
    rows = Database.fetch_all("SELECT * FROM Dose_Hst WHERE FLD_ID = '{}'".format(field.id))
    for row in rows:
      delivered_doses.append(cls(row))
    return delivered_doses

  @classmethod
  def for_patient(cls, patient):
    """Extracts all delivered doses belonging to the patient.

    Args:
      patient (Patient): The patient instance for which to extract associated delivered dose rows.

    Returns:
      List[DeliveredDose]: A list of delivered doses belonging to the given patient.
    """
    delivered_doses = list()
    rows = Database.fetch_all("SELECT * FROM Dose_Hst WHERE Pat_ID1 = '{}'".format(patient.id))
    for row in rows:
      delivered_doses.append(cls(row))
    return delivered_doses

  @classmethod
  def for_prescription(cls, prescription):
    """Extracts all delivered doses belonging to the prescription.

    Args:
      prescription (Prescription): The prescription instance for which to extract associated delivered dose rows.

    Returns:
      List[DeliveredDose]: A list of delivered doses belonging to the given prescription.
    """
    delivered_doses = list()
    rows = Database.fetch_all("SELECT * FROM Dose_Hst WHERE SIT_ID = '{}'".format(field.id))
    for row in rows:
      delivered_doses.append(cls(row))
    return delivered_doses

  @classmethod
  def for_scheduled_field(cls, scheduled_field):
    """Extracts all delivered doses belonging to the scheduled field.

    Args:
      scheduled_field (ScheduledField): The scheduled field instance for which to extract associated delivered dose rows.

    Returns:
      List[DeliveredDose]: A list of delivered doses belonging to the given scheduled field.
    """
    delivered_doses = list()
    rows = Database.fetch_all("SELECT * FROM Dose_Hst WHERE PTC_ID = '{}'".format(field.id))
    for row in rows:
      delivered_doses.append(cls(row))
    return delivered_doses

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Dose_Hst table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.dhs_id = row['DHS_ID']
    self.patient_id = row['Pat_ID1']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.institution_id = row['Inst_ID']
    self.note_id = row['Note_ID']
    self.field_id = row['FLD_ID']
    self.prescription_id = row['SIT_ID']
    self.treated_date = row['Tx_DtTm']
    self.fraction = row['Fractions_Tx']
    self.energy = row['Energy']
    self.epid = row['PIAcqDevice']
    self.dose = row['Dose_Tx_Act']
    self.treated_by_id = row['Staff_Id']
    self.location_id = row['Machine_ID_Staff_ID']
    self.termination_code = row['TerminationCode']
    self.is_in_patient = row['IsInPatient']
    self.overridden_by_id = row['OverrideID']
    self.overrides = row['Overrides1']
    self.comment = row['Notes'].rstrip
    self.scheduled_field_id = row['PTC_ID']
    self.is_open_port = row['IsOpenPort']
    self.was_overridden = row['WasOverridden']
    self.first_treatment = row['NewFieldDef']
    self.was_qa_mode = row['WasQAMode']
    self.partially_treated = row['PartiallyTreated']
    self.machine_id = row['MAC_ID']
    self.site_setup_id = row['SIS_ID']
    self.modality_id = row['Modality_Enum']
    self.type_id = row['Type_Enum']
    self.meterset = float(row['Meterset'])
    self.xvi_preset = row['XVI_Preset']
    # Convenience attributes:
    self.id = self.dhs_id
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_field = None
    self.instance_location = None
    self.instance_note = None
    self.instance_overridden_by = None
    self.instance_patient = None
    self.instance_prescription = None
    self.instance_scheduled_field = None
    self.instance_treated_by = None

  def created_by(self):
    """Gives the staff who created the delivered_dose.

    Returns:
      Location: The location (staff) who created this delivered_dose.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the delivered_dose.

    Returns:
      Location: The location (staff) who edited this delivered_dose.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def field(self):
    """Gives the field which this delivered_dose belongs to.

    Returns:
      Field: The field which this delivered_dose belongs to.
    """
    if not self.instance_field:
      self.instance_field = Field.find(self.field_id)
    return self.instance_field

  # The location which this delivered_dose is associated with.
  def location(self):
    """Gives the location which this delivered_dose is associated with.

    Returns:
      Location: The location which this delivered_dose is associated with.
    """
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location

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

  def note(self):
    """Gives the note (if any) associated with this delivered_dose.

    Returns:
      Note: The note associated with this delivered_dose, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def overridden_by(self):
    """Gives the staff who overrode the delivered_dose.

    Returns:
      Location: The location (staff) who overrode this delivered_dose.
    """
    if not self.instance_overridden_by:
      self.instance_overridden_by = Location.find(self.overridden_by_id)
    return self.instance_overridden_by

  def patient(self):
    """Gives the patient (if any) which this delivered_dose belongs to.

    Returns:
      Patient: The patient which this delivered_dose belongs to, or None.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def prescription(self):
    """Gives the prescription which this delivered_dose belongs to.

    Returns:
      Prescription: The prescription which this delivered_dose belongs to.
    """
    if not self.instance_prescription:
      self.instance_prescription = Prescription.find(self.prescription_id)
    return self.instance_prescription

  def scheduled_field(self):
    """Gives the scheduled_field (if any) which is referenced by this delivered_dose.

    Returns:
      ScheduledField: The scheduled_field which is referenced by this delivered_dose, or None.
    """
    if not self.instance_scheduled_field:
      self.instance_scheduled_field = ScheduledField.find(self.scheduled_field_id)
    return self.instance_scheduled_field

  def treated_by(self):
    """Gives the staff who treated (delivered) the dose.

    Returns:
      Location: The location (staff) who treated (delivered) this dose.
    """
    if not self.instance_treated_by:
      self.instance_treated_by = Location.find(self.treated_by_id)
    return self.instance_treated_by

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
