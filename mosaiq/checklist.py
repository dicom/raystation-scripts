# Import local files:
from .database import Database

class Checklist:
  """A class for reading checklist data from the Mosaiq database."""

  @classmethod
  def find(cls, id):
    """Finds the row in the Chklist table corresponding to the given id.

    Args:
      id (str or int): The primary database id (Chk_id) of the row to be extracted.

    Returns:
      Checklist: A new instance of the Checklist class, or None if no match.
    """
    instance = None
    row = Database.fetch_one("SELECT * FROM Chklist WHERE Chk_id = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance

  @classmethod
  def for_patient(cls, patient, task_id=None):
    """Extracts all checklist items belonging to the given patient.

    Note that if a task_id is given, only checklists of that type is extracted.

    Args:
      patient (Patient): The patient instance for which to extract associated checklist rows.
      task_id (int, optional): A specific task type for which to restrict the query. Defaults to None,

    Returns:
      List[Checklist]: A list of checklist items belonging to the given patient.
    """
    query = "SELECT * FROM Chklist WHERE Pat_ID1 = '{}'".format(patient.id)
    if task_id:
      query += " AND TSK_ID = '{}'".format(task_id)
    checklists = list()
    rows = Database.fetch_all(query)
    for row in rows:
      checklists.append(cls(row))
    return checklists

  def __init__(self, row):
    """Initializes an instance from a row extracted from the Chklist table.

    Args:
      row (dict): The row extracted from the database from which to create this instance.
    """
    # Database attributes:
    self.chk_id = row['Chk_id']
    self.set_id = row['Chk_set_id']
    self.complete = row['Complete']
    self.suppressed = row['Suppressed']
    self.item_sequence = row['Item_Seq']
    self.qcl_type = row['Qcl_Type']
    self.activity = row['Activity']
    self.comment = row['Notes']
    self.instructions = row['Instructions']
    self.due_date = row['Due_DtTm']
    self.completed_id = row['Com_Staff_ID']
    self.completed_date = row['Act_DtTm']
    self.edited_date = row['Edit_DtTm']
    self.edited_by_id = row['Edit_ID']
    self.created_date = row['Create_DtTm']
    self.created_by_id = row['Create_ID']
    self.approved_date = row['Sanct_DtTm']
    self.approved_by_id = row['Sanct_ID']
    self.note_id = row['Note_ID']
    self.patient_id = row['Pat_ID1']
    self.institution_id = row['Inst_ID']
    self.taskset_id = row['Chklist_ID']
    self.task_id = row['TSK_ID']
    self.requesting_id = row['Req_Staff_ID']
    self.responsible_id = row['Rsp_Staff_ID']
    # Convenience attributes:
    self.id = self.chk_id
    # Cache attributes:
    self.instance_approved_by = None
    self.instance_completed_by = None
    self.instance_created_by = None
    self.instance_edited_by = None
    self.instance_note = None
    self.instance_patient = None
    self.instance_requesting = None
    self.instance_responsible = None
    self.instance_task = None

  def approved_by(self):
    """Gives the staff who approved the checklist.

    Returns:
      Location: The location (staff) who approved this checklist.
    """
    if not self.instance_approved_by:
      self.instance_approved_by = Location.find(self.approved_by_id)
    return self.instance_approved_by

  def completed_by(self):
    """Gives the staff who completed the checklist.

    Returns:
      Location: The location (staff) who completed this checklist.
    """
    if not self.instance_completed_by:
      self.instance_completed_by = Location.find(self.completed_by_id)
    return self.instance_completed_by

  def created_by(self):
    """Gives the staff who created the checklist.

    Returns:
      Location: The location (staff) who created this checklist.
    """
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by

  def edited_by(self):
    """Gives the staff who last edited the checklist.

    Returns:
      Location: The location (staff) who edited this checklist.
    """
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by

  def note(self):
    """Gives the note (if any) associated with this checklist.

    Returns:
      Note: The note associated with this checklist, or None.
    """
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note

  def patient(self):
    """Gives the patient which this checklist belongs to.

    Returns:
      Patient: The patient which this checklist belongs to.
    """
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient

  def requesting(self):
    """Gives the staff/location/group who requested the checklist.

    Returns:
      Location: The staff/location/group who requested this checklist.
    """
    if not self.instance_requesting:
      self.instance_requesting = Location.find(self.requesting_id)
    return self.instance_requesting

  def responsible(self):
    """Gives the staff/location/group who is responsible for this checklist.

    Returns:
      Location: The staff/location/group who is responsible for this checklist.
    """
    if not self.instance_responsible:
      self.instance_responsible = Location.find(self.responsible_id)
    return self.instance_responsible

  def task(self):
    """Gives the task item referenced by this checklist.

    Returns:
      Task: The task item referenced by this checklist.
    """
    if not self.instance_task:
      self.instance_task = Task.find(self.task_id)
    return self.instance_task
