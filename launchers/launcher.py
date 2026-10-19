'''This wrapper handles the execution of a target script, captures its exit status or errors,
calculates the total duration, and sends a summary payload as a POST request to a web server
which stores it in a database for analysis.
'''

# Import system libraries:
import sys
import os
import subprocess
import time

# Import packages:
import requests

# Import local files:
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
import user_list as USERS

# Configuration:
WEB_SERVER_URL = open(r'C:\temp\raystation-scripts\launchers\web_server_url.txt', "r").read()

def run_and_register(target_script):
  """Executes a target script and registers information about the execution with a web server.

    Args:
      target_script (str): Relative path and file name of script to be executed.
    """
  # Construct the execution command using the same interpreter:
  command = [sys.executable, target_script]
  # Extract file name from full path:
  path, file_name = os.path.split(target_script)
  
  start_time = time.time()
  status = "success"
  exit_code = 0
  error_message = ""
  
  # Get user information:
  user_name = os.getlogin() if hasattr(os, 'getlogin') else "unknown"
  users = USERS.UserList("C:\\temp\\raystation-scripts\\settings\\users.tsv")
  group = users.get_group(user_name)

  print(f"[Launcher] Starting script: {target_script}...")
    
  env = os.environ.copy()
  launcher_dir = os.path.dirname(os.path.abspath(__file__))
  env["PYTHONPATH"] = (
    f"{launcher_dir};{env.get('PYTHONPATH', '')}"
    if os.name == "nt"
    else f"{launcher_dir}:{env.get('PYTHONPATH', '')}"
  )
    
  try:
    # Executes the script while streaming its output straight to the console
    result = subprocess.run(command, check=True, cwd="c:/temp", env=env)
    exit_code = result.returncode
  except subprocess.CalledProcessError as e:
    status = "failed"
    exit_code = e.returncode
    error_message = f"Script exited with error code {e.returncode}"
    print(f"[Launcher] Error encountered: {error_message}")
  except Exception as e:
    status = "error"
    exit_code = -1
    error_message = str(e)
    print(f"[Launcher] Failed to launch script: {error_message}")
        
  end_time = time.time()
  duration = round(end_time - start_time, 3)
    
  # Build metadata payload:
  payload = {
    "name": file_name,
    "status": status,
    "exit_code": exit_code,
    "duration": duration,
    "error": error_message,
    "group": group,
    "user": user_name
  }
    
  # Post telemetry data to the web server:
  print(f"[Launcher] Registering execution details with web server...")
  headers = {
    "Content-Type": "application/json"
  }
    
  try:
    response = requests.post(WEB_SERVER_URL, json=payload, headers=headers, timeout=10)
    if response.status_code in [200, 201]:
      print("[Launcher] Execution data successfully registered!")
    else:
      print(f"[Launcher] Server warning: Received status code {response.status_code}")
  except requests.exceptions.RequestException as req_err:
    print(f"[Launcher] Critical Error: Failed to contact the web server. Details: {req_err}")
