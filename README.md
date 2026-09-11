# RayStation Scripts

A collection of Python scripts developed at **Helse Møre og Romsdal HF** to
improve workflow within the radiotherapy treatment planning system
[RayStation](https://www.raysearchlabs.com/raystation/).

The scripts automate common treatment planning tasks, such as ROI definition,
treatment planning, quality control, and export/verification workflows. They are
run from RayStation's built-in scripting workspace.

## Features

- Interactive Tkinter-based GUIs for data entry
- Per-site treatment planning protocols for brain, breast, lung, bladder, prostate, rectum and palliative
- Clinical goal and optimization objective definitions per treatment site
- Quality control suite for treatment plans
- Integration with the Mosaiq oncology information system (OIS) database

## Requirements

- RayStation 2024B+
- Python 3.11 (bundled with RayStation)
- Tkinter (bundled with RayStation)
- [pymssql](https://pypi.org/project/pymssql/) for Mosaiq database access
- Microsoft SQL Server (Mosaiq) with valid credentials

## Installation

1. Create the deployment directory:

   ```bat
   mkdir C:\temp\raystation-scripts
   ```

2. Copy the contents of this repository into it:

   ```bat
   xcopy /E /I raystation-scripts\* C:\temp\raystation-scripts
   ```

   > **Note:** The scripts hardcode `C:\temp\raystation-scripts\` as the
   > deployment path. Relative paths will not work when these scripts are imported into
   > the RayStation database. The scripts will not run from any other location.

3. Configure the Mosaiq database credentials in the `mosaiq/` folder:
   - `database.txt` - SQL server address
   - `user.txt` - database user name
   - `password.txt` - database password

4. Copy the files to the RayStation scripting workspace, or import the scripts
   into the RayStation database so they appear in the scripting workspace GUI.

5. Ensure `pymssql` is available in the RayStation Python environment.

## Usage

All executable scripts are found in the root folder. From the RayStation
scripting workspace, open a patient and case, then run a script.

### Main workflows

| Script | Description |
| ------ | ----------- |
| `run_def.py` | ROI definition setup for a specified treatment site |
| `run_plan.py` | Main treatment planning workflow: sets up all parameters for planning of the current patient |
| `run_quality_control.py` | Runs the quality control suite on the current plan |
| `run_mosaiq_plan_verification.py` | Verifies export of the current plan against the Mosaiq database |

### ROI and structure utilities

| Script | Description |
| ------ | ----------- |
| `create_oars.py` | GUI for selecting and creating organs-at-risk |
| `create_wall.py` | Creates wall ROIs around PTVs |
| `update_derived_rois.py` | Updates derived ROIs |
| `delete_roi_geometries.py` | Deletes ROI geometries |

### Dose and QA utilities

| Script | Description |
| ------ | ----------- |
| `create_perturbed_dose.py` | Computes perturbed doses for robustness analysis |
| `create_and_export_qa_plan.py` | Creates and exports a QA plan |
| `calculate_edric.py` | Calculates the EDRIC metric |
| `calculate_paddick_index.py` | Calculates the Paddick conformity index |
| `clinical_goal_plan_association.py` | Associates clinical goals with plans |

### Export and diagnostics

| Script | Description |
| ------ | ----------- |
| `export_dicom_current_patient.py` | Exports DICOM data for the current patient |
| `export_statistics_to_excel.py` | Exports statistics to Excel |
| `run_console_and_statetree.py` | Console and state tree utilities |
| `copy_files.py` | File copy utility |

## Project structure

The root folder contains the executable scripts. Sub-folders contain the
libraries and resources they use:

| Folder | Contents |
| ------ | -------- |
| `functions/` | Utility function libraries (patient model, plan, beam set, ROI, GUI, etc.) |
| `ts_classes/` | Thin wrappers around the RayStation scripting API for test suite (`ts_*` prefix), plus Mosaiq verification wrappers (`mqv_*` prefix) |
| `rt_classes/` | Radiotherapy domain classes (sites, clinical goals, ROIs, margins, prescriptions, objectives) |
| `gui_classes/` | Reusable Tkinter GUI widget classes |
| `various_classes/` | High-level orchestration classes (plan, definition, quality control, Mosaiq verification) |
| `settings/` | Configuration and clinical protocol data (ROI definitions, beams, prescriptions, region codes, objectives, clinical goals) |
| `settings/clinical_goals/` | Per-site clinical goal definitions |
| `settings/objectives/` | Per-site optimization objective definitions |
| `def_regions/` | Per-site ROI definition scripts |
| `mosaiq/` | Mosaiq database integration layer (connection + domain model classes) |
| `single_use_scripts/` | One-off or site-specific batch scripts |
| `media/icons/` | GUI icons |

### Treatment sites

Supported treatment sites and their entry points:

| Site | ROI definition |
| ---- | -------------- |
| Bladder | `def_regions/def_bladder.py` |
| Brain | `def_regions/def_brain.py` |
| Breast | `def_regions/def_breast.py` |
| Lung | `def_regions/def_lung.py` |
| Palliative | `def_regions/def_palliative.py` |
| Prostate | `def_regions/def_prostate.py` |
| Rectum | `def_regions/def_rectum.py` |

The per-site planner logic is found in `various_classes/plan.py`
with settings and definitions found in `settings/objectives/`,
`settings/clinical_goals/`, and `rt_classes/optimizers/`.

## Development

This project has no test suite and no formal contribution guidelines yet. When
extending the scripts, follow the existing conventions:

- Executable scripts at the root: thin wrappers that load the current patient
  and case, then delegate to a class in `various_classes/`.
- Store site-specific clinical data in `settings/` rather than hardcoding it.

## License

This project is licensed under the GNU General Public License v3.0. See
[LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Authors

Developed and maintained by:

* Christoffer Lervåg (christoffer.lervag [@nospam.com] @helse-mr.no)
* Robert Hoggard
* Marit Funderud
* Helse Møre og Romsdal HF - Norway