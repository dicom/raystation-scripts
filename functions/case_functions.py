# encoding: utf8

# Import local files:
import isodose_color_tables as ISODOSES
import plan_functions as PF
import region_codes as RC
import structure_set_functions as SSF
import rois as ROIS

# Contains a collection of case functions.


# Set up plan, making sure the plan name does not already exist. If the plan name exists, (1), (2), (3) etc is added behind the name.
def create_plan(case, examination, region_text):
  name = region_text
  name_conflict = False
  for p in case.TreatmentPlans:
    if p.Name == region_text:
      name_conflict = True
  if name_conflict:
    i = 0
    while True:
      i += 1
      name = region_text + " (" + str(i) + ")"
      name_conflict = False
      for p in case.TreatmentPlans:
        if p.Name == name:
          name_conflict = True
      if name_conflict == False:
        break
  plan = case.AddNewPlan(PlanName = name, ExaminationName = examination.Name)
  return plan


# Loads a plan in the RayStation GUI. This is used when a new plan is created by script, in which case
# it is not automatically loaded in the GUI.
def load_plan(case, plan):
  current_plan = case.QueryPlanInfo(Filter = {'Name': plan.Name})
  case.LoadPlan(PlanInfo = current_plan[0])


# Set isodose lines:
def determine_isodoses(case, ss, region_code, nr_fractions, fraction_dose):
  case.CaseSettings.DoseColorMap.PresentationType = 'Relative'
  case.CaseSettings.DoseColorMap.ReferenceValue = nr_fractions*fraction_dose*100

  if region_code in RC.breast_codes and fraction_dose == 2 or region_code in RC.rectum_codes:
    ISODOSES.sib_47_50.apply_to(case)
  elif region_code in RC.prostate_codes:
    if fraction_dose in [2.0, 2.2]:
      if region_code in RC.prostate_bed_codes:
        if SSF.has_roi_with_shape(ss, ROIS.ctv_56.name):
          ISODOSES.prostate_bed_56_70.apply_to(case)
        else:
          ISODOSES.standard.apply_to(case)
      else:
        if SSF.has_roi_with_shape(ss, ROIS.ctv_56.name):
          ISODOSES.prostate_56_70_77.apply_to(case)
        else:
          ISODOSES.prostate_70_77.apply_to(case)
    elif fraction_dose == 3:
      ISODOSES.prostate_57_60.apply_to(case)
  elif PF.is_stereotactic(nr_fractions, fraction_dose):
    ISODOSES.stereotactic.apply_to(case)
  else:
    ISODOSES.standard.apply_to(case)

def determine_patient_position(examination):
  patient_position = "HeadFirstSupine"
  if examination.PatientPosition == 'FFS':
    patient_position = "FeetFirstSupine"
  return patient_position


def is_head_first_supine(examination):
  if determine_patient_position(examination) == 'HeadFirstSupine':
    return True
  else:
    return False