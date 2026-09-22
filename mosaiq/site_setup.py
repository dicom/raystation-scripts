# Import local files:
from .database import Database
from .location import Location
from .performed_site_setup import PerformedSiteSetup

class SiteSetup:
  """A class for reading site setup data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the SiteSetup table corresponding to the given id.

    Args:
      id (str or int): The primary database id (SIS_ID) of the row to be extracted.

    Returns:
      SiteSetup: A new instance of the SiteSetup class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM SiteSetup WHERE SIS_ID = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_prescription(cls, prescription):
    """Extracts the site setup belonging to the given prescription.

    Args:
      prescription (Prescription): The prescription instance for which to extract associated session rows.

    Returns:
      SiteSetup: A new instance of the SiteSetup class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM SiteSetup WHERE Sit_Set_ID = '{}'".format(prescription.id))
    if row != None:
      instance = cls(row)
    return instance

  def __init__(self, row):
    """Initializes an instance from a row extracted from the SiteSetup table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
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

  def approved_by(self):
    """Gives the staff who approved the site_setup.

    Returns:
      Location: The location (staff) who approved this site_setup.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def created_by(self):
    """Gives the staff who created the site_setup.

    Returns:
      Location: The location (staff) who created this site_setup.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the site_setup.

    Returns:
      Location: The location (staff) who edited this site_setup.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def location(self):
    """Gives the location which this site_setup is associated with.

    Returns:
      Note: The location which this site_setup is associated with.
    """
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location

  def performed_site_setups(self):
    """Gives the performed_site_setups (if any) associated with this site_setup

    Returns:
      List[PerformedSiteSetup]: The performed_site_setups associated with this site_setup, or an empty list.
    """
    if not self.instance_performed_site_setups:
      self.instance_performed_site_setups = PerformedSiteSetup.for_site_setup(self)
    return self.instance_performed_site_setups

  def prescription(self):
    """Gives the prescription which this site_setup belongs to.

    Returns:
      Prescription: The prescription which this site_setup belongs to.
    """
    if not self.instance_prescription:
      self.instance_prescription = Prescription.find(self.prescription_id)
    return self.instance_prescription

  def status(self):
    """The status description derived from the status_id.

    Returns:
      str: The status description (e.g. 'Approved').
    """
    values = {
      5 : 'Approved',
      7 : 'Pending'
    }
    return values.get(self.status_id, 'Unknown status_id: {}'.format(self.status_id))
