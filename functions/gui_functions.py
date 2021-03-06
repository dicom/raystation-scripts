# encoding: utf8

# Import system libraries:
from connect import *
import clr, sys
from tkinter import *
from tkinter import messagebox

# Import local files:
import beam_set_functions as BSF
import fractionation_frame as FRAC_FRAME
import plan_choices as PC
import radio_button as RB
import radio_button_frame as FRAME
import region_code_frame as REGION_FRAME
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF


# Checks if the given region code and region code list contain only unique codes.
# If a duplicate exists, an error is raised.
def check_region_codes(region_code, region_codes):
  codes = list(region_codes)
  codes.extend([str(region_code)])
  if len(list(set(codes))) != len(codes):
    title = "Ugyldig regionkode"
    text = "Ugyldig regionkode. Samme regionskode kan ikke brukes flere ganger!"
    messagebox.showinfo(title, text)
    sys.exit(0)


# Collects the selected choices from the user
def collect_choices(options, my_window, choices):
  # Set up GUI windows
  frame = FRAME.RadioButtonFrame(my_window, options)
  frame.grid(row = 0, column = 0)
  my_window.mainloop()
  # Extract information from the users's selections in the GUI:
  if frame.ok:
    (selection,value) = frame.get_results()
  elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
  else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)
  choices.append(value)
  if selection.children:  
    new_window = Toplevel()
    next_options = RB.RadioButton(selection.next_category.capitalize(), 'Velg ' + selection.next_category +':' , selection.children)
    selection = collect_choices(next_options, new_window,choices)
    choices.append(value)
  return choices


# Extract information from the users's input in the GUI,
def collect_delete_choice(options, my_window, choices):
  # Set up GUI windows
  frame = FRAME.RadioButtonFrame(my_window,options)
  frame.grid(row = 0, column = 0)
  my_window.mainloop()
  # Extract information from the users's selections in the GUI:
  if frame.ok:
    (selection,value) = frame.get_results()
  elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
  else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)
  choices.append(value) 
  return choices


def collect_fractionation_choices(my_window):
  # Set up GUI windows
  frame = FRAC_FRAME.FractionationFrame(my_window)
  frame.grid(row = 0, column = 0)
  my_window.mainloop()
  # Extract information from the users's selections in the GUI:
  if frame.ok:
    (region_code, fraction_dose, nr_fractions, initials) = frame.get_results()
    total_dose = nr_fractions * fraction_dose
  elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
  else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)
  return (region_code, fraction_dose, nr_fractions, initials, total_dose)
  

# Determines what list of technique possibilities will be given for different region codes:
def determine_choices(region_code, nr_fractions, fraction_dose, my_window, choices):
  # Default technique value, 'VMAT' 
  technique = 'VMAT'
  # Default technique name, 'VMAT' or '3D-CRT'
  technique_name = 'VMAT'
  # Default optimization value
  opt = ''
  if region_code in RC.breast_tang_codes or region_code in RC.breast_partial_codes:
    # Chosen technique value, 'VMAT' or 'Conformal'
    technique = 'Conformal'
    # Chosen technique name, 'VMAT' or '3D-CRT'
    technique_name = '3D-CRT'
    # Chosen optimization value
    opt = 'oar'
  elif region_code in RC.breast_reg_codes:
    # Determine which technique choices which will appear in the form
    techniques = RB.RadioButton('Planoppsett ', 'Velg planoppsett: ', PC.techniques)
    # Collects the selected choices from the user
    choices = collect_choices(techniques, my_window, [])
    # Chosen technique value, 'VMAT' or 'Conformal'
    technique = choices[0]
    # Chosen technique name, 'VMAT' or '3D-CRT'
    if technique == 'Conformal':
      technique_name = '3D-CRT'
    else:
      technique_name = 'VMAT'
    # Optimization value
    opt = 'oar'
  else:
    if region_code in RC.palliative_codes and nr_fractions*fraction_dose < 55 and not BSF.is_stereotactic(nr_fractions, fraction_dose) or region_code in RC.bladder_codes or region_code in RC.prostate_codes and nr_fractions*fraction_dose < 40 or region_code in RC.brain_whole_codes:
      opt = 'oar'
  results = [technique, technique_name, opt]
  return results


# Displays a warning for a prescription which have been considered invalid for a given region code.
# Halts the script execution after the warning has been displayed.
def handle_invalid_prescription(prescription, region_code):
  title = "Advarsel"
  text = "Ukjent fraksjonering angitt!\n\nFraksjoneringen (" + prescription.description() + ") er ikke gjenkjent for følgende regionkode:\n" + str(region_code) + "\n\nVennligst undersøk om du kan ha skrevet feil i fraksjonering eller regionkode, eller om dette eventuelt er en uvanlig fraksjonering som ikke står i prosedyren."
  messagebox.showinfo(title, text)
  sys.exit(0)


# Handles the situation of a missing target.
def handle_missing_ptv():
  title = "Manglende ROI"
  text = "PTV er ikke definert."
  messagebox.showinfo(title, text)
  sys.exit(0)


# Handles the situation of a missing target.
def handle_missing_ctv_or_ptv():
  title = "Manglende ROI"
  text = "Verken CTV eller PTV er definert."
  message_box(title, text)
  sys.exit(0)


# Handles the situation of a missing target.
def handle_missing_external():
  title = "Manglende ROI"
  text = "Finner ingen 'External' eller 'Body'."
  messagebox.showinfo(title, text)
  sys.exit(0)


# Handles the situation of a crashed attempt to perform model based segmentation.
def handle_failed_model_based_segmentation(roi_name):
  title = "Feilet modell-basert segmentering"
  text = "Mislyktes i å gjøre modell-basert segmentering for følgende ROI:" + "\n" + roi_name + "\n\n" + "Årsaken er at CT-bildene ikke inneholder ROIen eller at programmet ikke fant den."
  messagebox.showinfo(title, text)


# Handles the situation of a crashed attempt to move a roi that takes part of a structure set which has already been approved
def handle_failed_translation_of_roi(roi_name):
  title = "Feilet flytting av: " + roi_name
  text = "Mislyktes i flytte " + roi_name + "\n\n" + "Årsaken er at en struktur med samme navn er godkjent i en tidligere plan." + "\n\n" + "Sjekk at plassering av " + roi_name + " er fornuftig!"
  messagebox.showinfo(title, text)


# Handles the situation of a crashed attempt to move a roi that takes part of a structure set which has already been approved
def handle_failed_creation_of_roi(roi_name):
  title = "Feilet opprettelse av: " + roi_name
  text = "Mislyktes i å opprette " + roi_name + "\n\n" + "Årsaken er at en struktur med samme navn er godkjent i en tidligere plan." + "\n\n"
  messagebox.showinfo(title, text)


# Handles the situation of a crashed attempt to move a roi that takes part of a structure set which has already been approved
def handle_creation_of_new_roi_because_of_approved_structure_set(roi_name):
  title = "Opprettet roi: " + roi_name
  text = "Legg merke til at det har blitt opprettet en roi: " + roi_name + "\n\n" "Dette er fordi en tilsvarende roi finnes i et allerede godkjent struktursett." + "\n\n"  + "Hvis denne skal benyttes bør man oppdatere 'Clinical Goals' og evt 'Objectives'"
  messagebox.showinfo(title, text)


# Handles the sitsuation of a missing ROI when trying to create a clinical goal.
def handle_missing_roi_for_clinical_goal(roi_name):
  title = "Manglende ROI"
  text = "Mislyktes i å opprettte 'Clinical Goal' for følgende ROI:" + "\n" + roi_name + "\n\n" + "Årsaken er at ROIen mangler (eller at navnet er endret)"
  messagebox.showinfo(title, text)


# Handles the situation of a missing ROI when trying to create a derived ROI.
def handle_missing_roi_for_derived_rois(target_name, source_names):
  title = "Manglende ROI"
  text = "Mislyktes i å opprette følgende derived ROI:" + "\n" + target_name + "\n\n" + "Årsaken er at følgende source ROI mangler (eller har endret navn):" + "\n" + str(source_names)
  message_box(title, text)


# Handles the situation of a missing (or empty) ROI when trying to create an optimization objective.
def handle_missing_roi_for_objective(roi_name):
  title = "Manglende ROI"
  text = "Mislyktes i å opprettte 'Objective' for følgende ROI:" + "\n" + roi_name + "\n\n" + "Årsaken er at ROIen mangler, navnet er endret eller at den ikke har definert et volum."
  message_box(title, text)


# Handles the situation of a missing target.
def handle_missing_target():
  title = "Manglende målvolum"
  text = "Mislyktes i gjenkjenne målvolum for denne casen." + "\n\n" + "Årsaken er sannsynligvis at navngivingen på målvolumene avviker fra forventet nomenklatur."
  messagebox.showinfo(title, text)
  sys.exit(0)


# Handles the situation where the CT selected as primary is not the most recent CT in the case.
def handle_primary_is_not_most_recent_ct():
  title = "Primary image set"
  text = "CT-serien som er valgt som primary er ikke den siste CT-serien i denne casen." + "\n\n" + "Sjekk at inntegning ikke gjøres på feil CT-serie."
  message_box(title, text)


def message_box(title, text):
  root = Tk()
  root.withdraw()
  messagebox.showinfo(title, text)
  root.destroy()


# Extract information from the users's input in the GUI, in this case, the region code of additional stereotactic or palliative targets:
def multiple_beamset_form(ss, my_window):
  # Set up GUI windows
  frame = REGION_FRAME.RegionCodeFrame(my_window, ss)
  frame.grid(row = 0, column = 0)
  my_window.mainloop()

  # Extract information from the users's selections in the GUI
  if frame.ok:
    region_codes = frame.get_results()
  elif not frame.ok:
    print ("Script execution cancelled by user...")
    sys.exit(0)
  else:
    messagebox.showinfo("Error.","Unexpected error.")
    sys.exit(0)
  return region_codes


# Extract information from the users's input in the GUI, in this case, the set up of plans/beam sets:
def palliative_beamset_form(ss, my_window):
  beam_set_options = RB.RadioButton('Multiple målvolum oppdaget', 'Velg ønsket oppsett for plan/beam set: ', PC.beam_set_choices(ss))
  choices = collect_choices(beam_set_options, my_window, [])
  return choices
