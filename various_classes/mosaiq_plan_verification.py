# encoding: utf8

# Peforms a verification of the current treatment plan (including its beam sets) in Mosaiq,
# testing whether the parameters of the plan has been successfully exported to the Mosaiq database.
#
# PROOF OF CONCEPT!
# At this time only one parameter is checked (beam MU). The goal of this project
# however is to be able to verify all plan/beam parameters!

# System configuration:
from connect import *
import sys
# GUI framework (debugging only):
from tkinter import *
from tkinter import messagebox

# Local script imports:
import beam_set_label as BSL
import region_list as REGIONS




class MosaiqPlanVerification(object):
  def __init__(self, patient, case, plan, mq_patient):
    self.patient = patient
    self.case = case
    self.plan = plan
    self.mq_patient = mq_patient
    # Load list of region codes and corresponding region names, and get the region name for our particular region code (raise error if a name is not retrieved):
    self.regions = REGIONS.RegionList("C:\\temp\\raystation-scripts\\settings\\regions.tsv")
    
    # Iterate beam sets:
    for beam_set in self.plan.BeamSets:
      # Beam set label:
      beam_set_label = beam_set.DicomPlanLabel
      label = BSL.BeamSetLabel(beam_set_label)
      mq_label = self.translate(label)
      # Pass or fail?
      match = True
      text = ""
      # Find the corresponding plan (Rad Rx) in Mosaiq:
      mq_beam_set = None
      for p in self.mq_patient.prescriptions():
        if p.site_name == mq_label:
          mq_beam_set = p
      # Proceed with beam set comparison if a match was found:
      if mq_beam_set:
        # Test if monitor units of first beam are equal:
        if round(beam_set.Beams[0].BeamMU, 1) == round(mq_beam_set.fields()[0].meterset, 1):
          match = True
          text = "Success!\n\nPlan: " + mq_label + "\n\nMU:\nExpected " + str(round(beam_set.Beams[0].BeamMU,1)) + " - Found " + str(round(mq_beam_set.fields()[0].meterset,1))
        else:
          match = False
          text = "Failed!\n\nPlan: " + mq_label + "\n\nMU:\nExpected " + str(round(beam_set.Beams[0].BeamMU,1)) + " - Found " + str(round(mq_beam_set.fields()[0].meterset,1))
      else:
        text = "No matching prescription found in Mosaiq for plan label: " + mq_label
      # Display the results of the test:      
      root = Tk()
      root.withdraw()
      title = "RayStation and Mosaiq plan comparison"
      #text = ""
      messagebox.showinfo(title, text)
      root.destroy()

  
  # Translates a RayStation (code format) beam set label to the Mosaiq (readable) version.
  def translate(self, bs_label):
    assert type(bs_label) is BSL.BeamSetLabel, "bs_label is not a BeamSetLabel: %r" % bs_label
    # Get the region text part of the label:
    region_text = self.regions.get_text(bs_label.region)
    assert region_text != None
    # Add the dose part of the label to complete it:
    mq_label = region_text + " " + str(round(bs_label.start_dose)) + "-" + str(round(bs_label.end_dose))
    return mq_label