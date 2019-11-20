# encoding: utf8

# Executes the Definition class, which sets up all ROIs and POIs needed for treatment planning in RayStation.
#
# Authors:
# Christoffer Lervåg & Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9A

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


# Add necessary folders to the system path:
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\def_regions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\functions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\gui_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\quality_control".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\rt_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\settings".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\ts_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\various_classes".decode('utf8'))
# Relative paths would be better, but unfortunately doesnt seem to work when imported into the RayStation database:
#sys.path.append(os.path.join(sys.path[0],'def_regions'))
#sys.path.append(os.path.join(sys.path[0],'functions'))
#sys.path.append(os.path.join(sys.path[0],'gui_classes'))
#sys.path.append(os.path.join(sys.path[0],'rt_classes'))
#sys.path.append(os.path.join(sys.path[0],'settings'))



# Import local files:
import definition as DEF


# Load patient and case data:
try:
  patient = get_current("Patient")
except SystemError:
  raise IOError("No patient loaded.")
try:
  case = get_current("Case")
except SystemError:
  raise IOError("No case loaded.")
try:
  patient_db = get_current('PatientDB')
except SystemError:
  raise IOError("No case loaded.")

# Set up and execute the def script:
d = DEF.Definition(patient_db, patient, case)
