

#   RayStation version: 9A


# Import system libraries:
from connect import *
import clr, sys, os
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from Microsoft.Office.Interop.Excel import *
from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton, TextBox)
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\gui_classes".decode('utf8'))
import text_box_perturbed_form as FORM

beam_set = get_current("BeamSet")
examination = get_current("Examination")
name = examination.Name


# Setup and run GUI:
form = FORM.TextBoxForm()
form.DialogResult


# Extract information from the users's selections in the GUI:
if form.DialogResult == DialogResult.OK:
  x = float(form.SelectedX)
  y = float(form.SelectedY)
  z = float(form.SelectedZ)
elif form.DialogResult == DialogResult.Cancel:
  print "Script execution cancelled by user..."
  sys.exit(0)
else:
  raise IOError("Unexpected error (selection).")



beam_set.ComputePerturbedDose(DensityPerturbation=0, PatientShift={ 'x': x, 'y': 0, 'z': 0 }, OnlyOneDosePerImageSet=False, AllowGridExpansion=False, ExaminationNames=[name], FractionNumbers=[0], ComputeBeamDoses=True)

beam_set.ComputePerturbedDose(DensityPerturbation=0, PatientShift={ 'x': -x, 'y': 0, 'z': 0 }, OnlyOneDosePerImageSet=False, AllowGridExpansion=False, ExaminationNames=[name], FractionNumbers=[0], ComputeBeamDoses=True)

beam_set.ComputePerturbedDose(DensityPerturbation=0, PatientShift={ 'x': 0, 'y': 0, 'z': y }, OnlyOneDosePerImageSet=False, AllowGridExpansion=False, ExaminationNames=[name], FractionNumbers=[0], ComputeBeamDoses=True)

beam_set.ComputePerturbedDose(DensityPerturbation=0, PatientShift={ 'x': 0, 'y': 0, 'z': -y }, OnlyOneDosePerImageSet=False, AllowGridExpansion=False, ExaminationNames=[name], FractionNumbers=[0], ComputeBeamDoses=True)

beam_set.ComputePerturbedDose(DensityPerturbation=0, PatientShift={ 'x': 0, 'y': -z, 'z': 0 }, OnlyOneDosePerImageSet=False, AllowGridExpansion=False, ExaminationNames=[name], FractionNumbers=[0], ComputeBeamDoses=True)

beam_set.ComputePerturbedDose(DensityPerturbation=0, PatientShift={ 'x': 0, 'y': z, 'z': 0 }, OnlyOneDosePerImageSet=False, AllowGridExpansion=False, ExaminationNames=[name], FractionNumbers=[0], ComputeBeamDoses=True)


