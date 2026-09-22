# Import local files:
from .database import Database
from .location import Location
from .note import Note
from .task import Task

class Appointment:
  """A class for reading appointment data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Schedule table corresponding to the given id.

    Args:
      id (str or int): The primary database id (Sch_Id) of the row to be extracted.

    Returns:
      Appointment: A new instance of the Appointment class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Schedule WHERE Sch_Id = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient):
    """Extracts all appointments belonging to the given patient.

    Note that both deleted appointments (Suppressed = 1) and historic appointments (Version != 0) are excluded.

    Args:
      patient (Patient): The patient instance for which to extract associated appointment rows.

    Returns:
      List[Appointment]: A list of all appointments belonging to the given patient, sorted by their start_date parameter.
    """
    appointments = list()
    rows = Database.fetch_all("SELECT * FROM Schedule WHERE Pat_ID1 = '{}' AND Suppressed != {} AND Version = 0".format(patient.id, 1))
    for row in rows:
      appointments.append(cls(row))
    return appointments

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Schedule table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.sch_id = row['Sch_Id']
    self.sch_set_id = row['Sch_Set_Id']
    self.related_appointment_id = row['Sch_Set_Id']
    self.activity_code = row['Activity'].rstrip()
    self.start_date = row['App_DtTm']
    self.location_id = row['Location']
    self.staff_id = row['Staff_ID']
    self.institution_id = row['Inst_ID']
    self.alert = row['Alert']
    self.comment = row['Notes']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.note_id = row['Note_ID']
    self.deleted = row['Suppressed']
    self.duration_raw = row['Duration_time']
    self.status1 = row['SchStatus_Hist_UD']
    self.status2 = row['SchStatus_Hist_SD']
    self.patient_id = row['Pat_ID1']
    # Convenience attributes:
    self.id = self.sch_id
    self.duration = self.duration_raw / 6000
    # Cache attributes:
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_location = None
    self.instance_note = None
    self.instance_patient = None
    self.instance_previous_versions = list()
    self.instance_staff = None
    self.instance_task = None

  def boost(self):
    """Interprets the status2 parameter, whether it is a boost ("Old Start") or not.

    Returns:
      bool: True if status2 contains 'O', False if not.
    """
    if 'O' in self.status2:
      return True
    else:
      return False

  def created_by(self):
    """Gives the staff who created the appointment.

    Returns:
      Location: The location (staff) who created this appointment.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the appointment.

    Returns:
      Location: The location (staff) who edited this appointment.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def location(self):
    """Gives the location which the appointment is assigned to.

    Returns:
      Location: The location which the appointment is assigned to.
    """
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location

  def note(self):
    """Gives the note (if any) associated with this appointment.

    Returns:
      Note: The note associated with this appointment, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def patient(self):
    """Gives the patient which this appointment belongs to.

    Returns:
      Patient: The patient which this appointment belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def previous_versions(self):
    """Gives the previous (historic) versions (if any) of this appointment.

    Returns:
      List[Appointment]: The note associated with this appointment, or an empty list.
    """
    if len(self.instance_previous_versions) == 0:
      rows = Database.fetch_all("SELECT * FROM Schedule WHERE Sch_Set_Id = '{}' AND Sch_Id != {}".format(self.sch_set_id, self.sch_id))
      for row in rows:
        self.instance_previous_versions.append(cls(row))
    return self.instance_previous_versions

  def staff(self):
    """Gives the staff who is associated with the appointment.

    Returns:
      Location: The location (staff) who is associated with the appointment.
    """
    if not self.instance_staff:
      self.instance_staff = Location.find(self.staff_id)
    return self.instance_staff

  def start(self):
    """Interprets the status2 parameter, whether it is a treatment start ("New Start") or not.

    Returns:
      bool: True if status2 contains 'S', False if not.
    """
    if 'S' in self.status2:
      return True
    else:
      return False

  def task(self):
    """Gives the task item referenced by this appointment.

    Returns:
      Task: The task item referenced by this appointment.
    """
    if not self.instance_task:
      self.instance_task = Task.find(self.task_id)
    return self.instance_task
