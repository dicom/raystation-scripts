# encoding: utf8

# Executes the QualityControl class which runs a suite of tests on the current patient,
# case and treatment plan (including ROIs, beam sets, beams, objectives, etc).
#
# Authors:
# Christoffer Lervåg & Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 6.0

# System configuration:
from connect import *
import sys
# Add necessary folders to the system path:
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\def_regions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\functions".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\gui_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\rt_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\settings".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\ts_classes".decode('utf8'))
sys.path.append("I:\\HSM - Kreftavdelingen - gammelt fellesområde\\Program\\Skript\\raystation-scripts\\various_classes".decode('utf8'))

# GUI framework:
clr.AddReference("PresentationFramework")
from System.Windows import *

# Local script imports:
import quality_control as QC

# "Global" variables:
patient = get_current('Patient')
case = get_current('Case')
plan = get_current('Plan')
#machine_db = get_current('MachineDB')

# Set up and execute the quality control:
qc = QC.QualityControl(patient, case, plan)

# Display the results of the quality control:
title = "Plan Quality Control"
summary = qc.result.failure_summary()
text = str(qc.result.nr_failures()) + " mulige problemer ble funnet:\n\n" + summary
MessageBox.Show(text, title, MessageBoxButton.OK, MessageBoxImage.Information)
