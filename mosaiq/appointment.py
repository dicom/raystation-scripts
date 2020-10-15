# encoding: utf8

# A class for reading appointment data from the Mosaiq database.
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

class Appointment:
  
  # Returns a single appointment matching the given database id (Sch_Id) (or None if no match).
  @classmethod
  def find(cls, id):
    instance = None
    row = Database.fetch_one("SELECT * FROM Schedule WHERE Sch_Id = '{}'".format(str(id)))
    if row != None:
      instance = cls(row)
    return instance
  
  # Gives all appointments belonging to the given patient.
  # Excludes deleted appointments (suppressed = true).
  # Excludes historic appointments (version != 0).
  # Returns appointments sorted by their start_date parameter.
  @classmethod
  def for_patient(cls, patient):
    appointments = list()
    rows = Database.fetch_all("SELECT * FROM Schedule WHERE Pat_ID1 = '{}' AND Suppressed != {} AND Version = 0".format(patient.id, True))
    for row in rows:
      appointments.append(cls(row))
    return appointments
  
  # Creates a Appointment instance from a appointment database row.
  def __init__(self, row):
    # Database attributes:
    self.sch_id = row['Sch_Id']
    self.sch_set_id = row['Sch_Set_Id']
    self.related_appointment_id = row['Sch_Set_Id']
    self.activity_code = row['Activity'].rstrip() # If this crashes sometimes, we have to test if the string exists.
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
    
  # Gives the status of the appointment, whether it is a boost start or not ("Old Start").
  def boost(self):
    if 'O' in self.status2:
      return True
    else:
      return False
  
  # The staff who created the appointment.
  def created_by(self):
    if not self.instance_created_by:
      self.instance_created_by = Location.find(self.created_by_id)
    return self.instance_created_by
  
  # The staff who last edited the appointment.
  def edited_by(self):
    if not self.instance_edited_by:
      self.instance_edited_by = Location.find(self.edited_by_id)
    return self.instance_edited_by
  
  # The location which the appointment is assigned to.
  def location(self):
    if not self.instance_location:
      self.instance_location = Location.find(self.location_id)
    return self.instance_location
  
  # Gives the note (if any) associated with this appointment.
  def note(self):
    if not self.instance_note:
      self.instance_note = Note.find(self.note_id)
    return self.instance_note
  
  # Gives the patient which this appointment belongs to.
  def patient(self):
    if not self.instance_patient:
      self.instance_patient = Patient.find(self.patient_id)
    return self.instance_patient
  
  # Gives the previous (historic) versions (if any) of this appointment.
    def previous_versions(self):
      if len(self.instance_previous_versions) == 0:
        rows = Database.fetch_all("SELECT * FROM Schedule WHERE Sch_Set_Id = '{}' AND Sch_Id != {}".format(self.sch_set_id, self.sch_id))
        for row in rows:
          self.instance_previous_versions.append(cls(row))
      return self.instance_previous_versions
  
  # The staff who is associated with the appointment.
  def staff(self):
    if not self.instance_staff:
      self.instance_staff = Location.find(self.staff_id)
    return self.instance_staff

  # Gives the status of the appointment, whether it is a tretment start or not ("New Start").
  def start(self):
    if 'S' in self.status2:
      return True
    else:
      return False
  
  # Gives the task item referenced by this appointment.
  def task(self):
    if not self.instance_task:
      self.instance_task = Task.find(self.task_id)
    return self.instance_task
  