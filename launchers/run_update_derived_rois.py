'''Launches the update_derived_rois script.'''

# Import local files:
sys.path.append("C:\\temp\\raystation-scripts\\launchers")
import launcher

# Script to be executed:
target_script = "raystation-scripts/scripts/update_derived_rois.py"

# Execution:
if __name__ == "__main__":
  launcher.run_and_register(target_script)
