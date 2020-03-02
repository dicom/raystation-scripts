# encoding: utf8

# Import system libraries:
from connect import *
import clr, sys
from tkinter import *
from tkinter import messagebox

# Import local files:
import plan_choices as PC
import plan_functions as PF
import radio_button as RB
import radio_button_frame as FRAME
import fractionation_frame as FRAC_FRAME
import region_code_frame as REGION_FRAME
import region_codes as RC
import structure_set_functions as SSF
import rois as ROIS


# Lists of which number of fractions and fraction dose are allowed for a given region code, i.e treatment site. If the given values does not match the values in the list, an error is raised.
# FIXME: This function has an inherent weakness (or the error() fuction actually), that it does not
# check the pair of fraction dose and nr of fractions, it only checks the values separately.
# Furthermore, it probably shouldnt stop execution on an uknown fractionation scheme, it should just warn
# and allow the user to continue.
def check_input(ss, region_code, nr_fractions, fraction_dose):
  if region_code in RC.brain_codes:
    if region_code in RC.brain_whole_codes:
      error(nr_fractions, fraction_dose, [5, 10], [2.5, 3, 4])
    else:
      if fraction_dose > 6:
        error(nr_fractions, fraction_dose, [1, 3], [7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
  elif region_code in RC.lung_codes:
    if nr_fractions in [3, 8] or nr_fractions == 5 and fraction_dose == 11:
      error(nr_fractions, fraction_dose, [3, 5, 8], [15, 11, 7])
    else:
      error(nr_fractions, fraction_dose, [2, 5, 10, 11, 12, 13, 15, 16, 17, 25, 30, 33, 35], [1.5, 1.8, 2, 2.8, 3, 4, 8.5])
  elif region_code in RC.breast_codes:
    if SSF.has_roi_with_shape(ss, ROIS.ctv_p.name):
      error(nr_fractions, fraction_dose, [15], [2.67])
    else:
      error(nr_fractions, fraction_dose, [25, 15], [2, 2.67])
  elif region_code in RC.bladder_codes:
    error(nr_fractions, fraction_dose, [3, 5, 6, 7, 10, 11, 12, 13, 25, 32], [2, 3, 3.5, 4, 7])
  elif region_code in RC.prostate_codes:
    if region_code in RC.prostate_bed_codes and SSF.has_roi_with_shape(ss, ROIS.ptv_70.name):
      error(nr_fractions, fraction_dose, [35], [2])
    elif SSF.has_roi_with_shape(ss, ROIS.ptv_77.name):
      error(nr_fractions, fraction_dose, [35], [2.2])
    elif SSF.has_roi_with_shape(ss, ROIS.ptv_60.name):
      error(nr_fractions, fraction_dose, [20], [3])
  elif region_code in RC.rectum_codes:
    if SSF.has_roi_with_shape(ss, ROIS.ctv_50.name):
      error(nr_fractions, fraction_dose, [25], [2])
    else:
      error(nr_fractions, fraction_dose, [30, 5], [1.5, 5]) # Added 1.5 Gy*30, which was used in a rectum case.
  elif region_code in RC.palliative_codes:
    if fraction_dose > 8:
      error(nr_fractions, fraction_dose, [1, 3], [9, 16])



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
    if region_code in RC.palliative_codes and nr_fractions*fraction_dose < 55 and not PF.is_stereotactic(nr_fractions, fraction_dose) or region_code in RC.bladder_codes or region_code in RC.prostate_codes and nr_fractions*fraction_dose < 40 or region_code in RC.brain_whole_codes:
      opt = 'oar'

  results = [technique, technique_name, opt]
  return results


# Gives an error if the given number of fractions and fraction dose is not in the given list of possible values
def error(nr_fractions, fraction_dose, nr_fractions_list, fraction_dose_list):
  if nr_fractions not in nr_fractions_list:
    title = ""
    text = "Ugyldig antall fraksjoner."
    messagebox.showinfo(title, text)
    sys.exit(0)
  if fraction_dose not in fraction_dose_list:
    title = ""
    text = "Ugyldig fraksjondose."
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

