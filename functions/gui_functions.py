# encoding: utf8

# Import system libraries:
from connect import *
import clr, sys
from tkinter import *
from tkinter import messagebox

# Import local files:
import beam_set_functions as BSF
import def_choices as DC
import fractionation_frame as FRAC_FRAME
import patient_model_functions as PMF
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
  

# Returns multiple region codes in cases where this needs to be collected.
# This means, for SBRT brain or lung, if there are multiple targets, an extra form
# is displayed where the user can specify the region code(s) of the other target(s).
def collect_target_strategy_and_region_codes(ss, nr_targets, region_code, prescription):
  region_codes = []
  target = None
  palliative_choices = None
  if nr_targets > 1:
    if region_code in RC.brain_codes + RC.lung_codes:
      if prescription.is_stereotactic():
        region_codes = multiple_beamset_form(ss, Toplevel())
        check_region_codes(region_code, region_codes)
    elif region_code in RC.palliative_codes:
      # For palliative cases with multiple targets:
      palliative_choices = palliative_beamset_form(ss, Toplevel())
      if palliative_choices[0] in ['sep_beamset_iso', 'sep_beamset_sep_iso']:
        region_codes = multiple_beamset_form(ss, Toplevel())
        check_region_codes(region_code, region_codes)
        if SSF.has_roi_with_shape(ss, ROIS.ctv1.name):
          target = ROIS.ctv1.name
        elif SSF.has_roi_with_shape(ss, ROIS.ctv2.name):
          target = ROIS.ctv2.name
        elif SSF.has_roi_with_shape(ss, ROIS.ctv3.name):
          target = ROIS.ctv3.name
        elif SSF.has_roi_with_shape(ss, ROIS.ctv4.name):
          target = ROIS.ctv4.name
      elif palliative_choices[0] == 'sep_plan':
        target = palliative_choices[1]
  return target, palliative_choices, region_codes


# Determines what list of technique possibilities will be given for different region codes:
def determine_choices(region_code, prescription, my_window, choices):
  # Default technique value, 'VMAT' 
  technique = 'VMAT'
  # Default technique name, 'VMAT' or '3D-CRT'
  technique_name = 'VMAT'
  # Default optimization value
  opt = ''
  if region_code in RC.extremity_codes:
    # For extremities it may be practical to use 3D-CRT in some cases:
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
  elif region_code in RC.palliative_codes and not prescription.is_stereotactic():
    # Palliative (non-SBRT):
    opt = 'oar'
  elif region_code in RC.bladder_codes:
    # Bladder:
    opt = 'oar'
  elif region_code in RC.prostate_codes and prescription.total_dose < 40:
    # Palliative prostate:
    opt = 'oar'
  elif region_code in RC.brain_whole_codes:
    # Whole brain:
    opt = 'oar'
  elif region_code in RC.bone_codes and prescription.is_stereotactic():
    # Bone SBRT:
    opt = 'oar'
  results = [technique, technique_name, opt]
  return results


# Handles the situation when the attempt to delete a ROI results in a crash.
def handle_delete_roi_error(roi_name):
  title = "Feilet å slette ROI"
  text = "Mislyktes å slette følgende ROI:" + "\n" + roi_name + "\n\n" + "Årsaken kan være at struktursettet er låst (signert)."
  messagebox.showinfo(title, text)


# Handles the sitsuation of a missing ROI when trying to create a clinical goal.
def handle_error_on_clinical_goal_creation(cg, normalized_tolerance, normalized_value, error):
  title = "Feilmelding!"
  text = "Det skjedde en feil ved opprettelse av følgende Clinical Goal:\n\n" + cg.text() + "\nNormalized tolerance: " + str(normalized_tolerance) + "\nNormalized value: " + str(normalized_value) + "\n\nFeilmelding:\n" + str(error.args[0]) + "\n\nTa kontakt med skript-ansvarlig for feilsøking!" # {An identical clinical goal already exists.}
  messagebox.showinfo(title, text)


# Checks if any ROIs exist, and if they have a contour in the current structure set.
# If so, ask the user if ROIs are to be deleted.
# Returns the Tk window object.
def handle_existing_rois(pm, ss):  
  if SSF.has_roi_with_contours(ss):
    delete = RB.RadioButton('Eksisterende ROIs oppdaget', 'Velg:', DC.delete)
    my_window = Tk()
    choice_d=[]
    delete_choice = collect_delete_choice(delete, my_window, choice_d)
    for i in range(len(delete_choice)):
      if delete_choice[i] == 'yes':
        # All ROIs are to be deleted:
        PMF.delete_all_rois(pm)
      elif delete_choice[i] == 'some':
        # Only non-delineated ROIs are to be deleted:
        PMF.delete_rois_except_manually_contoured(pm, ss)
    my_window = Toplevel()
  else:
    my_window = Tk()
  return my_window


# Displays a warning for a prescription which is unknown for a given region code.
# The user is then given the choice to continue script execution or to stop.
def handle_invalid_prescription(prescription, region_code, region_text):
  title = "Advarsel!"
  text = "Ukjent fraksjonering angitt!\n\nFraksjoneringen (" + prescription.description() + ") er ikke gjenkjent for følgende regionkode:\n" + str(region_code) + " (" + region_text + ")\n\nVennligst undersøk om du kan ha skrevet feil i fraksjonering eller regionkode, eller om dette eventuelt er en uvanlig fraksjonering som ikke står i prosedyren.\n\nØnsker du å fortsette?"
  result = messagebox.askquestion(title, text)
  # Stop script execution if the user clicks 'no' (on the question to continue):
  if result != 'yes':
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
  text = "Legg merke til at det har blitt opprettet en ny roi: " + roi_name + "\n\n" "Dette er fordi en tilsvarende roi finnes i et allerede godkjent struktursett." + "\n\n"  + "Hvis denne skal benyttes bør man oppdatere 'Clinical Goals' og evt 'Objectives'"
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
def handle_missing_target(expected, present):
  title = "Manglende målvolum"
  text = "Mislyktes i å gjenkjenne målvolum for denne casen." + "\n\n" + "Årsaken er sannsynligvis at navngivingen på målvolumene avviker fra forventet nomenklatur.\n\n" + "Forventede målvolumskandidater:\n" + str(expected) + "\n\n" + "ROIer tilstede:\n" + str(present)
  messagebox.showinfo(title, text)
  sys.exit(0)


# Handles an error occuring when doing beam set optimization.
def handle_optimization_error(po, error):
  title = "Feilmelding!"
  msg = error.args[0]
  msg_intro = msg.partition('--- End of inner exception stack trace')[0]
  text = "Det skjedde en feil ved optimalisering av følgende beam set:\n" + po.OptimizedBeamSets[0].DicomPlanLabel + "\n\nFeilmelding:\n" + msg_intro + "\n\nEn vanlig årsak kan være manglende GPU til å gjøre beregninger på datamaskinen.\n\nHvis det ser ut til å være en annen feil, kan du vurdere å ta kontakt med skript-ansvarlig for feilsøking!"
  messagebox.showinfo(title, text)


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
