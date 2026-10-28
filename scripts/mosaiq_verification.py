'''Script for verifying the content of a treatment plan exported to Mosaiq against the original plan in RayStation.

Authors:
Christoffer Lervåg
Helse Møre og Romsdal HF
'''

# Import system libraries:
import datetime
import sys
from tkinter import *
from tkinter import messagebox


# Import RayStation packages:
sys.path.append("C:/Program Files/RaySearch Laboratories/RayStation 2024B/ScriptClient/")
from connect import *

# Add local folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\ts_classes")
sys.path.append(r'C:\temp\raystation-scripts')
# Relative paths would be better, but unfortunately doesnt seem to work when imported into the RayStation database, e.q.:
#sys.path.append(os.path.join(sys.path[0],'def_regions'))

# Import local packages:
import mosaiq

# Import local files:
import beam_set_label as BSL
import region_list as REGIONS
import test_p as TEST
import mqv_plan as MQV_P
import mqv_beam_set as MQV_BS
import mqv_beam as MQV_B
import mqv_segment as MQV_S


def perform_verification(patient, case, plan):
  """Performs the verification.

    Configures the test suite data struture (patient, case, plan, beam set, beam, segment, etc).
    Executes tests on each of these levels.
    Collects the results of the individual tests in a parameter object.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
      case (PyScriptObject): The RayStation Case instance.
      plan (PyScriptObject): The RayStation TreatmentPlan instance.

    Returns:
      test_p.Parameter: The results of the verification performed on the treatment plan.
    """
  # Load mosaiq patient:
  mq_patient = mosaiq.Patient.find_by_ida(patient.PatientID)

  # Load list of region codes and corresponding region names,
  # and get the region name for our particular region code (raise error if a name is not retrieved):
  regions = REGIONS.RegionList("C:\\temp\\raystation-scripts\\settings\\regions.tsv")

  # Initialize test suite classes:
  mqv_plan = MQV_P.MQVPlan(patient, case, plan, mq_patient)
  for beam_set in plan.BeamSets:
    mqv_beam_set = MQV_BS.MQVBeamSet(beam_set, mqv_plan=mqv_plan)
    for beam in beam_set.Beams:
      mqv_beam = MQV_B.MQVBeam(beam, mqv_beam_set=mqv_beam_set)
      for segment in beam.Segments:
        mqv_segment = MQV_S.MQVSegment(segment, mqv_beam=mqv_beam)

  if mq_patient:
    # Collect & assign the equivalent Mosaiq objects to the RayStation objects (beam sets, beams & segments):
    # Beam sets:
    beam_sets = {}
    # Collect beam sets:
    for bs in mq_patient.prescriptions():
      beam_sets[bs.site_name] = bs
    # Iterate beam sets:
    for mqv_beam_set in mqv_plan.mqv_beam_sets:
      # Assign beam set (if we have a matching label):
      if mqv_beam_set.expected_mosaiq_label in beam_sets:
        mqv_beam_set.mq_beam_set = beam_sets[mqv_beam_set.expected_mosaiq_label]
        # Beams:
        beams = {}
        # Collect beams:
        for b in mqv_beam_set.mq_beam_set.fields():
          beams[str(b.label)] = b
        # Iterate beams:
        for mqv_beam in mqv_beam_set.mqv_beams:
          # Assign beam (if we have a matching beam number):
          if str(mqv_beam.nr.value) in beams:
            mqv_beam.mq_beam = beams[str(mqv_beam.nr.value)]
            # Segments:
            segments = {}
            # Collect segments:
            for s in mqv_beam.mq_beam.control_points():
              segments[s.number] = s
            # Iterate segments:
            for mqv_segment in mqv_beam.mqv_segments:
              # Assign segments:
              mqv_segment.mq_segment = segments[mqv_segment.segment.SegmentNumber]
  return mqv_plan.param

  # Store the plan test results:
  result = mqv_plan.param

  # Run tests:
  mqv_plan.test_matching_patient()
  mqv_plan.test_other_unapproved_treatment_plans_in_case()
  # Beam set tests:
  for mqv_beam_set in mqv_plan.mqv_beam_sets:
    mqv_beam_set.test_matching_beam_set_name()
    mqv_beam_set.test_technique()
    mqv_beam_set.test_modality()
    mqv_beam_set.test_patient_orientation()
    mqv_beam_set.test_setup_offsets()
    # Beam tests:
    for mqv_beam in mqv_beam_set.mqv_beams:
      mqv_beam.test_matching_beam_number()
      mqv_beam.test_mu()
      mqv_beam.test_name()
      mqv_beam.test_energy()
      mqv_beam.test_fff()
      # Segment tests:
      for mqv_segment in mqv_beam.mqv_segments:
        mqv_segment.test_matching_segment_number()
        mqv_segment.test_collimator_angle()
        mqv_segment.test_jaw_positions()
        mqv_segment.test_gantry_angle()
        mqv_segment.test_relative_weight()
        mqv_segment.test_positions_leaf_bank1()
        mqv_segment.test_positions_leaf_bank2()


def main():
  '''Performs verification of the Mosaiq export of the RayStation treatment plan
  and displays the result in a dialogue window.
  '''
  # Log start time:
  time_start = datetime.datetime.now()

  # Load patient and case data:
  try:
    patient = get_current("Patient")
  except SystemError:
    raise IOError("No patient loaded.")
  try:
    case = get_current("Case")
  except SystemError:
    raise IOError("No case loaded.")
  try:
    plan = get_current("Plan")
  except SystemError:
    raise IOError("No plan loaded.")

  # Set up and execute the verification:
  result = perform_verification(patient, case, plan)

  # Create title and body strings:
  title = "Mosaiq Plan Verification"
  summary = result.failure_summary()
  if result.nr_failures() == 0:
    # Zero failures:
    text = "Ingen problemer ble funnet! :)\n\n"
  else:
    # 1 or more failures:
    text = str(result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary

  # Max text length of messagebox is 1024. Reduce failure summary if it is too long:
  limit = 4000
  if len(text) > limit:
    text = text[0:limit] + "\n\n... [Resten er klippet ut]"

  # Log finish time and format a time string:
  time_end = datetime.datetime.now()
  elapsed_time = time_end - time_start
  if elapsed_time.seconds > 3600:
    hours = elapsed_time.seconds // 3600 % 3600
    minutes = (elapsed_time.seconds - hours * 3600) // 60 % 60
    seconds = elapsed_time.seconds - hours * 3600 - minutes * 60
  else:
    hours = 0
    minutes = elapsed_time.seconds // 60 % 60
    seconds = elapsed_time.seconds - minutes * 60
  # Append time string to result:
  if hours > 0:
    text += "\n\n" + "Tidsbruk: " +str(hours) + " time(r) " + str(minutes) + " min " + str(seconds) + " sek"
  else:
    if minutes > 0:
      text += "\n\n" + "Tidsbruk: " + str(minutes) + " min " + str(seconds) + " sek"
    else:
      text += "\n\n" + "Tidsbruk: " + str(seconds) + " sek"

  # Display the messagebox GUI with a visible taskbar icon:
  # Create the root window:
  root = Tk()
  # Hide the root window:
  root.withdraw()
  # Set the taskbar icon:
  root.iconbitmap(r'C:\temp\raystation-scripts\media\icons\qc.ico')
  # Show the root window (so it has a taskbar presence):
  root.deiconify()
  # Set title:
  root.title("Plan Quality Control")
  # Show the message box:
  messagebox.showinfo(title, text)
  # Close the root window after the messagebox is dismissed:
  root.destroy()


# Execution:
if __name__ == "__main__":
  main()
