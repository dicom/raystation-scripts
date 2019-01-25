# encoding: utf8

# Creates an Anal Canal ROI from a Rectum ROI by copying the caudal 4 cm of Rectum ROI.
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 6.0

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
import math

# Add necessary folders to the system path:
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\def_regions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\functions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\gui_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\rt_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\settings".decode('utf8'))


from connect import *

import patient_model_functions as PMF
import roi as ROI
import rois as ROIS

# Load case data:
try:
    case = get_current("Case")
except SystemError:
    raise IOError("No case loaded.")

# Load patient model, examination and structure set:
pm = case.PatientModel
examination = get_current("Examination")
ss = PMF.get_structure_set(pm, examination)

# Create the posterior half ROI:
PMF.create_bottom_part_x_cm(pm, examination, ss, ROIS.rectum, ROIS.anal_canal, 4)