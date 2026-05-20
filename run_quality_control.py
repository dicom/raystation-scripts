# Executes the QualityControl class which runs a suite of tests on the current patient,
# case and treatment plan (including ROIs, beam sets, beams, objectives, etc).
#
# Authors:
# Christoffer Lervåg, Marit Funderud, Robert Hoggard
# Helse Møre og Romsdal HF
#

# System configuration:
from connect import *
import datetime
import sys
from tkinter import *
from tkinter import messagebox
import os
import json
import base64
import hashlib
import hmac
import tkinter.font as tkfont

# Log start time:
time_start = datetime.datetime.now()

# Add necessary folders to the system path:
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\ts_classes")
sys.path.append("C:\\temp\\raystation-scripts\\various_classes")
sys.path.append(r'C:\temp\raystation-scripts')

# Local script imports:
import quality_control as QC

# "Global" variables:
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

# Apply log file workflow?
run_log = 1

# Log file configuration:
output_dir = r"I:\HMR - Begrenset\Klinikk for kreftbehandling og rehabilitering - Stråleterapi-kontor - Doseplanlegging\Skript\Misc Scripts\QA logs"
file_prefix = "qc_results_"
file_suffix = ".txt"
cache_max_age_days = 30

# Encryption configuration:
encryption_version = 1
pbkdf2_iterations = 200000

# Get patient modification time:
def get_patient_modification_time_string(patient):
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


# Create key material:
def get_key_material(unique_plan_id, modification_time_str):
  return (str(unique_plan_id) + "|" + str(modification_time_str)).encode("utf-8")


# Derive encryption key:
def derive_key(unique_plan_id, modification_time_str, salt):
  return hashlib.pbkdf2_hmac(
    "sha256",
    get_key_material(unique_plan_id, modification_time_str),
    salt,
    pbkdf2_iterations,
    dklen=32
  )


# Create encryption stream:
def make_keystream(key, nonce, length):
  stream = bytearray()
  counter = 0
  while len(stream) < length:
    counter_bytes = counter.to_bytes(8, byteorder="big")
    stream.extend(hmac.new(key, nonce + counter_bytes, hashlib.sha256).digest())
    counter += 1
  return bytes(stream[:length])


# Apply encryption stream:
def xor_bytes(data, key_stream):
  return bytes([a ^ b for a, b in zip(data, key_stream)])


# Encrypt text:
def encrypt_text(text, unique_plan_id, modification_time_str):
  salt = os.urandom(16)
  nonce = os.urandom(16)
  key = derive_key(unique_plan_id, modification_time_str, salt)
  plain_bytes = text.encode("utf-8")
  key_stream = make_keystream(key, nonce, len(plain_bytes))
  cipher_bytes = xor_bytes(plain_bytes, key_stream)
  tag = hmac.new(key, salt + nonce + cipher_bytes, hashlib.sha256).digest()
  payload = {
    "version": encryption_version,
    "salt": base64.b64encode(salt).decode("ascii"),
    "nonce": base64.b64encode(nonce).decode("ascii"),
    "ciphertext": base64.b64encode(cipher_bytes).decode("ascii"),
    "hmac": base64.b64encode(tag).decode("ascii")
  }
  return json.dumps(payload, sort_keys=True, indent=2)


# Decrypt text:
def decrypt_text(encrypted_text, unique_plan_id, modification_time_str):
  payload = json.loads(encrypted_text)
  if payload.get("version") != encryption_version:
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


# Clean old log files:
def clean_old_files(output_dir):
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


# Read result from file:
def read_saved_result(file_path, unique_plan_id, modification_time_str):
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


# Write result to file:
def write_saved_result(file_path, unique_plan_id, modification_time_str, text):
  if modification_time_str is None:
    return
  try:
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    encrypted_text = encrypt_text(text, unique_plan_id, modification_time_str)
    with open(file_path, "w", encoding="utf-8", newline='\n') as file:
      file.write(encrypted_text)
  except Exception as e:
    messagebox.showerror("Feil", "Kunne ikkje skrive til fil:\n" + file_path + "\n\nFeilmelding: " + str(e))


# Insert text with preserved indentation for wrapped lines:
def insert_indented_text(text_box, text):
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


# Display QC results in a custom popup:
def show_qc_result_window(title, text):
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


# Run Quality Control
Log_file_used = 0
if run_log == 1:
  # Set up the log file:
  try:
    unique_plan_id = plan.GetPlanUuid()
  except Exception:
    unique_plan_id = str(plan.Name)
  file_path = os.path.join(output_dir, file_prefix + str(unique_plan_id) + file_suffix)
  modification_time_str = get_patient_modification_time_string(patient)
  clean_old_files(output_dir)

  # Read saved result from file:
  text = read_saved_result(file_path, unique_plan_id, modification_time_str)

  if text is None:
    # Set up and execute the quality control class:
    qc = QC.QualityControl(patient, case, plan)

    # Create title and body strings:
    title = "Plan Quality Control"
    summary = qc.result.failure_summary()
    if qc.result.nr_failures() == 0:
      # Zero failures:
      text = "Ingen problemer ble funnet! :)\n\n"
    else:
      # One or more failures:
      text = str(qc.result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary

    # Write result to file:
    write_saved_result(file_path, unique_plan_id, modification_time_str, text)
  else:
    # Create title string:
    title = "Plan Quality Control"
    Log_file_used = 1
else:
  # Set up and execute the quality control class:
  qc = QC.QualityControl(patient, case, plan)

  # Create title and body strings:
  title = "Plan Quality Control"
  summary = qc.result.failure_summary()
  if qc.result.nr_failures() == 0:
    # Zero failures:
    text = "Ingen problemer ble funnet! :)\n\n"
  else:
    # One or more failures:
    text = str(qc.result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary 

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
