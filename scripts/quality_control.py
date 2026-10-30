'''Script for performing quality control on a treatment plan.

Authors:
Christoffer Lervåg
Robert Hoggard
Helse Møre og Romsdal HF
'''

# Import system libraries:
import datetime
import sys
import os
import json
import base64
import hashlib
import hmac
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont


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


# Import local files:
import test_p as TEST
import raystation_utilities as RSU
import ts_patient as TS_P
import ts_case as TS_C
import ts_poi as TS_POI
import ts_roi as TS_ROI
import ts_structure_set as TS_SS
import ts_poi_geometry as TS_PG
import ts_roi_geometry as TS_RG
import ts_plan as TS_PLAN
import ts_beam_set as TS_BS
import ts_prescription as TS_PR
import ts_label as TS_L
import ts_beam as TS_B
import ts_segment as TS_S
import ts_optimization as TS_O


# Encryption constants:
ENCRYPTION_VERSION = 1
PBKDF2_ITERATIONS = 200000


def get_patient_modification_time_string(patient):
  """Gives the patient modification time.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.

    Returns:
      str: A string representation of the patient modification time.
    """
  try:
    if hasattr(patient, 'ModificationInfo') and patient.ModificationInfo is not None:
      modification_time = patient.ModificationInfo.ModificationTime
      if modification_time is None:
        return None
      if modification_time.Year < 1900:
        return None
      modification_time_py = datetime.datetime(
        modification_time.Year,
        modification_time.Month,
        modification_time.Day,
        modification_time.Hour,
        modification_time.Minute,
        modification_time.Second
      )
      return modification_time_py.strftime("%Y-%m-%d %H:%M:%S")
  except Exception:
    return None
  return None


def get_key_material(unique_plan_id, modification_time_str):
  """Creates key material.

    Args:
      unique_plan_id (int): A unique plan id.
      modification_time_str (str): A string representation of the patient modification time.

    Returns:
      str: A combined string.
    """
  return (str(unique_plan_id) + "|" + str(modification_time_str)).encode("utf-8")


def derive_key(unique_plan_id, modification_time_str, salt):
  """Derives an encryption key.

    Args:
      unique_plan_id (int): A unique plan id.
      modification_time_str (str): A string representation of the patient modification time.
      salt (str): A salt (random string) used in the encryption.

    Returns:
      str: A byte string.
    """
  return hashlib.pbkdf2_hmac(
    "sha256",
    get_key_material(unique_plan_id, modification_time_str),
    salt,
    PBKDF2_ITERATIONS,
    dklen=32
  )


def make_keystream(key, nonce, length):
  """Creates an encryption stream.

    Args:
      key (str): The key used in the encryption.
      nonce (str): A random string used in the encryption.
      length (int): The length of the byte string.

    Returns:
      str: A byte string.
    """
  stream = bytearray()
  counter = 0
  while len(stream) < length:
    counter_bytes = counter.to_bytes(8, byteorder="big")
    stream.extend(hmac.new(key, nonce + counter_bytes, hashlib.sha256).digest())
    counter += 1
  return bytes(stream[:length])


def xor_bytes(data, key_stream):
  """Applies an encryption stream to a plain text.

    Args:
      data (str): The plain text to be encrypted.
      key_stream (str): The key stream used to encrypt the plain text.

    Returns:
      str: An encrypted byte string.
    """
  return bytes([a ^ b for a, b in zip(data, key_stream)])


def encrypt_text(text, unique_plan_id, modification_time_str):
  """Encrypts plain text and dumps it to a json string along with relevant encryption parameters.

    Args:
      text (str): The plain text to be encrypted.
      unique_plan_id (int): A unique plan id.
      modification_time_str (str): A string representation of the patient modification time.

    Returns:
      str: A json string of a hash containing the encrypted text along with relevant encryption parameters.
    """
  salt = os.urandom(16)
  nonce = os.urandom(16)
  key = derive_key(unique_plan_id, modification_time_str, salt)
  plain_bytes = text.encode("utf-8")
  key_stream = make_keystream(key, nonce, len(plain_bytes))
  cipher_bytes = xor_bytes(plain_bytes, key_stream)
  tag = hmac.new(key, salt + nonce + cipher_bytes, hashlib.sha256).digest()
  payload = {
    "version": ENCRYPTION_VERSION,
    "salt": base64.b64encode(salt).decode("ascii"),
    "nonce": base64.b64encode(nonce).decode("ascii"),
    "ciphertext": base64.b64encode(cipher_bytes).decode("ascii"),
    "hmac": base64.b64encode(tag).decode("ascii")
  }
  return json.dumps(payload, sort_keys=True, indent=2)


def decrypt_text(encrypted_text, unique_plan_id, modification_time_str):
  """Decrypts an encrypted text loaded from a json payload containing relevant encryption parameters.

    Args:
      encrypted_text (str): The encryption payload.
      unique_plan_id (int): A unique plan id.
      modification_time_str (str): A string representation of the patient modification time.

    Returns:
      str: The decrypted plain text.
    """
  payload = json.loads(encrypted_text)
  if payload.get("version") != ENCRYPTION_VERSION:
    return None
  salt = base64.b64decode(payload["salt"])
  nonce = base64.b64decode(payload["nonce"])
  cipher_bytes = base64.b64decode(payload["ciphertext"])
  stored_tag = base64.b64decode(payload["hmac"])
  key = derive_key(unique_plan_id, modification_time_str, salt)
  calculated_tag = hmac.new(key, salt + nonce + cipher_bytes, hashlib.sha256).digest()
  if not hmac.compare_digest(stored_tag, calculated_tag):
    return None
  key_stream = make_keystream(key, nonce, len(cipher_bytes))
  plain_bytes = xor_bytes(cipher_bytes, key_stream)
  return plain_bytes.decode("utf-8")


def clean_old_files(output_dir, file_prefix, file_suffix, cache_max_age_days):
  """Cleans up the log file folder by deleting files older than a specific threshold.

    Args:
      output_dir (str): The folder where log files are stored.
      file_prefix (str): Log file prefix.
      file_suffix (str): Log file suffix.
      cache_max_age_days (int): Max lifetime of log files (in days) before they are deleted.
    """
  threshold = datetime.datetime.now() - datetime.timedelta(days=cache_max_age_days)
  try:
    if not os.path.exists(output_dir):
      return
    for filename in os.listdir(output_dir):
      if filename.startswith(file_prefix) and filename.endswith(file_suffix):
        full_path = os.path.join(output_dir, filename)
        file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
        if file_mtime < threshold:
          os.remove(full_path)
  except Exception as e:
    print("Could not clean old QC files: " + str(e))


def read_saved_result(file_path, unique_plan_id, modification_time_str):
  """Reads and decrypts an encrypted an encrypted log file.

    Args:
      file_path (str): The path to a log file.
      unique_plan_id (int): A unique plan id.
      modification_time_str (str): A string representation of the patient modification time.

    Returns:
      str: The decrypted plain text.
    """
  if modification_time_str is None:
    return None
  if not os.path.exists(file_path):
    return None
  try:
    with open(file_path, "r", encoding="utf-8") as file:
      encrypted_text = file.read()
    return decrypt_text(encrypted_text, unique_plan_id, modification_time_str)
  except Exception as e:
    print("Could not read QC file: " + str(e))
    return None


def write_saved_result(output_dir, file_path, unique_plan_id, modification_time_str, text):
  """Wites a given result to file.

    Args:
      output_dir (str): The directory of the log file folder.
      file_path (str): The full path (including file name) of the log file to be written.
      unique_plan_id (int): A unique plan id.
      modification_time_str (str): A string representation of the patient modification time.
      text (str): The text to be written to the file.
    """
  if modification_time_str is None:
    return
  try:
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    encrypted_text = encrypt_text(text, unique_plan_id, modification_time_str)
    with open(file_path, "w", encoding="utf-8", newline='\n') as file:
      file.write(encrypted_text)
  except Exception as e:
    messagebox.showerror("Feil", "Kunne ikke skrive til fil:\n" + file_path + "\n\nFeilmelding: " + str(e))


def insert_indented_text(text_box, text):
  """Insert text with preserved indentation for wrapped lines.

    Args:
      text_box (tkinter.Text): The GUI text box where the indented text will be displayed.
      text (str): The indented text to be tranferred to the text_box.
    """
  # Get the font used by the text box:
  font_obj = tkfont.Font(font=text_box.cget("font"))
  # Measure the width of one space character:
  space_width = font_obj.measure(" ")
  # Create a dictionary to track indentation tags already created:
  used_tags = {}
  # Loop through each line in the result text:
  for line in text.splitlines():
    # Replace tab characters with spaces:
    line = line.expandtabs(2)
    # Preserve empty lines:
    if line.strip() == "":
      text_box.insert(END, "\n")
      continue
    # Count the number of leading spaces:
    indent_chars = len(line) - len(line.lstrip(" "))
    # Remove leading spaces from the text content:
    content = line.lstrip(" ")
    # Create a tag name for this indentation level:
    tag_name = "indent_" + str(indent_chars)
    # Create a new indentation tag if it does not already exist:
    if tag_name not in used_tags:
      margin = indent_chars * space_width
      text_box.tag_configure(tag_name, lmargin1=margin, lmargin2=margin)
      used_tags[tag_name] = True
    # Insert the line using the correct indentation tag:
    text_box.insert(END, content + "\n", tag_name)


def show_qc_result_window(title, text):
  """Insert text with preserved indentation for wrapped lines.

    Args:
      title (str): The title of the dialogue window.
      text (str): The text to be displayed in the GUI.
    """
  # Create the popup window:
  root = Tk()
  # Set the popup title:
  root.title(title)
  # Allow the popup to be resized:
  root.resizable(True, True)
  # Set the taskbar icon:
  try:
    root.iconbitmap(r'C:\temp\raystation-scripts\media\icons\qc.ico')
  except Exception:
    pass
  # Allow the popup contents to resize with the window:
  root.grid_rowconfigure(0, weight=1)
  root.grid_columnconfigure(0, weight=1)
  # Create the main frame:
  frame = Frame(root, padx=18, pady=14)
  frame.grid(row=0, column=0, sticky="nsew")
  # Allow the text box to resize with the frame:
  frame.grid_rowconfigure(0, weight=1)
  frame.grid_columnconfigure(0, weight=1)
  # Create the text box:
  text_box = Text(frame, width=95, height=22, wrap=WORD, font=("Segoe UI", 10))
  text_box.grid(row=0, column=0, sticky="nsew")
  # Add a vertical scrollbar:
  scrollbar = Scrollbar(frame, orient="vertical", command=text_box.yview)
  scrollbar.grid(row=0, column=1, sticky="ns")
  text_box.config(yscrollcommand=scrollbar.set)
  # Insert the result text with indentation-aware wrapping:
  insert_indented_text(text_box, text)
  # Make the text box read-only:
  text_box.config(state="disabled")
  # Create the OK button:
  ok_button = Button(frame, text="OK", width=10, command=root.destroy)
  ok_button.grid(row=1, column=0, columnspan=2, sticky="e", pady=(12, 0))
  # Close the popup with escape
  root.bind("<Escape>", lambda event: root.destroy())
  # Centre the popup on screen:
  root.update_idletasks()
  root.eval('tk::PlaceWindow . center')
  # Bring the popup to the front:
  root.lift()
  root.attributes("-topmost", True)
  root.after(250, lambda: root.attributes("-topmost", False))
  # Run the popup:
  root.mainloop()


def perform_quality_control(patient, case, plan):
  """Performs the quality control.

    Configures the test suite data struture (patient, case, plan, beam set, beam, segment, etc).
    Executes tests on each of these levels.
    Collects the results of the individual tests in a parameter object.

    Args:
      patient (PyScriptObject): The RayStation Patient instance.
      case (PyScriptObject): The RayStation Case instance.
      plan (PyScriptObject): The RayStation TreatmentPlan instance.

    Returns:
      test_p.Parameter: The results of the quality control performed on the treatment plan.
    """
  # Initialize test suite:
  ts_patient = TS_P.TSPatient(patient)
  ts_case = TS_C.TSCase(case, ts_patient=ts_patient)
  for poi in case.PatientModel.PointsOfInterest:
    ts_poi = TS_POI.TSPOI(poi, ts_case=ts_case)
  for roi in case.PatientModel.RegionsOfInterest:
    ts_roi = TS_ROI.TSROI(roi, ts_case=ts_case)
  for structure_set in case.PatientModel.StructureSets:
    ts_structure_set = TS_SS.TSStructureSet(structure_set, ts_case=ts_case)
    for poi_geometry in structure_set.PoiGeometries:
      ts_poi_geometry = TS_PG.TSPOIGeometry(poi_geometry, ts_structure_set=ts_structure_set)
    for roi_geometry in structure_set.RoiGeometries:
      ts_roi_geometry = TS_RG.TSROIGeometry(roi_geometry, ts_structure_set=ts_structure_set)
  ts_plan = TS_PLAN.TSPlan(plan, ts_case=ts_case)

  for beam_set in plan.BeamSets:
    ts_beam_set = TS_BS.TSBeamSet(beam_set, ts_plan=ts_plan)
    ts_label = TS_L.TSLabel(beam_set.DicomPlanLabel, ts_beam_set=ts_beam_set)
    if beam_set.Prescription.PrimaryPrescriptionDoseReference:
      ts_prescription = TS_PR.TSPrescription(beam_set.Prescription, ts_beam_set=ts_beam_set)
    po = RSU.plan_optimization(plan, beam_set)
    if po:
      ts_optimization = TS_O.TSOptimization(po, ts_beam_set=ts_beam_set)
    for beam in beam_set.Beams:
      ts_beam = TS_B.TSBeam(beam, ts_beam_set=ts_beam_set)
      for segment in beam.Segments:
        ts_segment = TS_S.TSSegment(segment, ts_beam=ts_beam)

  # Store the patient test results:
  result = ts_patient.param

  # Run tests:
  # Patient tests:
  ts_patient.id_length_test()
  # Case tests:
  ts_case.last_examination_used_test()
  ts_case.localization_points_for_gating_test()
  ts_case.breath_measurement_point_for_lung_sbrt_test()
  ts_case.breath_measurement_point_not_in_gantry_shadow_for_lung_sbrt_test()
  ts_case.dibh_control_examinations_present_on_dibh_case_test()
  ts_case.ctv_not_contracted_from_external_for_breast_case_with_virtual_bolus_test()
  ts_case.virtual_bolus_without_density_override_test()
  #ts_case.case_has_prosthesis_roi_if_metal_is_present_in_examination_test()

  # ROI tests:
  for ts_roi in ts_case.ts_rois:
    ts_roi.exclude_from_export_test()

  # Structure set tests:
  plan_ss_examination_name = ts_case.ts_plan.plan.BeamSets[0].GetStructureSet().OnExamination.Name
  for ts_structure_set in ts_case.ts_structure_sets:
    if ts_structure_set.structure_set.OnExamination.Name == plan_ss_examination_name:
      ts_structure_set.localization_point_test()
      ts_structure_set.external_test()
      ts_structure_set.dose_region_test()
      ts_structure_set.ptv_derived_test()
      ts_structure_set.prosthesis_titanium_test()
      ts_structure_set.external_ptv_bounding_test()
      ts_structure_set.couch_test()
      ts_structure_set.couch_close_to_patient_test()
      ts_structure_set.couch_joint_close_to_ptv_test()
      ts_structure_set.breast_seeds_test()
      ts_structure_set.no_empty_slice_between_rectum_and_analcanal_test()
      ts_structure_set.no_geometries_outside_external_test()

      # POI geometry tests:
      for ts_poi_geometry in ts_structure_set.ts_poi_geometries:
        ts_poi_geometry.is_defined_test()
        ts_poi_geometry.is_not_zero_test()
      # ROI geometry tests:
      for ts_roi_geometry in ts_structure_set.ts_roi_geometries:
        ts_roi_geometry.derived_roi_geometry_is_updated_test()
        ts_roi_geometry.gaps_in_definition_test()
        ts_roi_geometry.max_nr_of_islands_in_slice_test()

  # Plan tests:
  ts_plan.planned_by_test()
  ts_plan.unique_beam_numbers_test()
  ts_plan.localization_point_not_in_first_or_last_slice_test()

  # Beam set tests:
  for ts_beam_set in ts_plan.ts_beam_sets:
    ts_beam_set.unmerged_beams_test()
    ts_beam_set.technique_test()
    ts_beam_set.machine_test()
    ts_beam_set.setup_beams_test()
    ts_beam_set.dose_test()
    ts_beam_set.dose_is_clinical_test()
    ts_beam_set.dose_algorithm_test()
    ts_beam_set.electron_mc_uncertainty_test()
    ts_beam_set.beam_energy_equality_test()
    ts_beam_set.photon_energy_for_curative_fractionations_test()
    ts_beam_set.vmat_full_arc_rotation_of_last_beam_test()
    ts_beam_set.vmat_arc_sequence_test()
    ts_beam_set.reasonable_collimator_angles_test()
    ts_beam_set.defined_prescription_test()
    ts_beam_set.nr_fractions_test()
    ts_beam_set.label_vmat_test()
    ts_beam_set.label_target_volume_test()
    ts_beam_set.guard_leaf_test()
    ts_beam_set.name_of_beam_iso_test()
    ts_beam_set.isocenter_centered_long_test()
    ts_beam_set.prescription_mu_test()
    ts_beam_set.asymmetric_jaw_opening_long_test()
    ts_beam_set.isocenter_centered_test()
    ts_beam_set.vmat_mu_test()
    ts_beam_set.beam_number_test()
    ts_beam_set.target_volume_normalisation_for_sib_test()
    ts_beam_set.existing_plan_in_mosaiq_with_this_beam_set_label_test()


    # Label tests:
    ts_label = ts_beam_set.ts_label
    ts_label.nr_parts_test()
    ts_label.nr_fractions_test()
    ts_label.technique_test()
    ts_label.region_test()
    ts_label.middle_part_separator_test()
    ts_label.middle_part_doses_test()
    # Prescription tests:
    ts_prescription = ts_beam_set.ts_prescription
    if ts_prescription:
      ts_prescription.ctv_prescription_test()
      ts_prescription.prescription_type_test()
      ts_prescription.prescription_dose_test()
      ts_prescription.prescription_real_dose_test()
      ts_prescription.clinical_max_test()
      ts_prescription.stereotactic_prescription_technique_test()

    # Objectives/constraints tests:
    ts_optimization = ts_beam_set.ts_optimization
    if ts_optimization:
      ts_optimization.constraints_test()
      ts_optimization.objectives_background_dose_test()
      ts_optimization.objective_for_prescription_roi_test()
      ts_optimization.dose_grid_test()

    # Beam tests:
    for ts_beam in ts_beam_set.ts_beams:
      ts_beam.name_test()
      ts_beam.name_capitalization_test()
      ts_beam.name_of_arc_test()
      ts_beam.mu_beam_vmat_test()
      ts_beam.mu_1000_test()
      ts_beam.gantry_angle_test()
      ts_beam.logical_gantry_angle_breast_test()
      ts_beam.energy_of_arc_test()
      ts_beam.collimator_angle_of_arc_test()
      ts_beam.number_of_segments_of_static_beam_test()
      ts_beam.wide_jaw_opening_which_can_hit_vmat_qa_detector_electronics_test()
      ts_beam.arc_gantry_spacing_test()
      ts_beam.wide_jaw_opening_for_filter_free_energies()
      ts_beam.mu_segment_3dcrt_test()
      ts_beam.segment_test()
      ts_beam.bolus_set_test()
      ts_beam.couch_rotation_angle_test()
      ts_beam.cutout_name_and_cutout_contour_seems_to_correlate_for_electrons_test()
      #ts_beam.narrow_jaw_opening_for_filter_energies()
      # Segment tests (at the moment we have no segment tests):
      #for ts_segment in ts_beam.ts_segments:
  return result

def main():
  '''Performs quality control of the treatment plan and displays the result in a dialogue window.

    Note that if a quality control of the exact same treatment plan have already been executed
    (recognized by plan UID and time stamp), then the results are retrieved from an
    encrypted log file instead of re-running the quality control, to save execution time.
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

  # Settings:
  # Log file path:
  output_dir = open(r'C:\temp\raystation-scripts\config\qc_log.txt', "r", encoding='utf-8').read()
  # Apply log file workflow?
  run_log = 1
  # File prefix and suffix:
  file_prefix = "qc_results_"
  file_suffix = ".txt"
  # Log file lifetime:
  cache_max_age_days = 30

  # Handle results:
  Log_file_used = 0
  if run_log == 1:
    # Set up the log file:
    try:
      unique_plan_id = plan.GetPlanUuid()
    except Exception:
      unique_plan_id = str(plan.Name)
    file_path = os.path.join(output_dir, file_prefix + str(unique_plan_id) + file_suffix)
    modification_time_str = get_patient_modification_time_string(patient)
    clean_old_files(output_dir, file_prefix, file_suffix, cache_max_age_days)

    # Read saved result from file:
    text = read_saved_result(file_path, unique_plan_id, modification_time_str)

    if text is None:
      # Set up and execute the quality control:
      result = perform_quality_control(patient, case, plan)

      # Create title and body strings:
      title = "Plan Quality Control"
      summary = result.failure_summary()
      if result.nr_failures() == 0:
        # Zero failures:
        text = "Ingen problemer ble funnet! :)\n\n"
      else:
        # One or more failures:
        text = str(result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary

      # Write result to file:
      write_saved_result(output_dir, file_path, unique_plan_id, modification_time_str, text)
    else:
      # Create title string:
      title = "Plan Quality Control"
      Log_file_used = 1
  else:
    # Set up and execute the quality control:
    result = perform_quality_control()

    # Create title and body strings:
    title = "Plan Quality Control"
    summary = result.failure_summary()
    if result.nr_failures() == 0:
      # Zero failures:
      text = "Ingen problemer ble funnet! :)\n\n"
    else:
      # One or more failures:
      text = str(result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary

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

  if Log_file_used == 1:
    text += "\n\n" "QC Results read from log file"

  # Display the QC results:
  show_qc_result_window(title, text)


# Execution:
if __name__ == "__main__":
  main()
