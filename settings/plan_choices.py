# encoding: utf8

# Import local files:
import property as P
import structure_set_functions as SSF
from tkinter import messagebox

# Breast robustness (ptosis):
ptosis = P.Property('Ptose', 'ptosis')
std = P.Property('Standard', 'standard', default = True)

# Setup techniques:
conformal = P.Property('3D-CRT','Conformal')
vmat = P.Property('VMAT','VMAT', default = True)

# List of choices:
techniques = [conformal, vmat]
breast_robustness = [ptosis, std]


def beam_set_choices(ss):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  
  sep_plan = P.Property('Separate planer','sep_plan', next_category = 'målvolum')
  sep_beamset_sep_iso = P.Property('Separate beam set - separate isosenter','sep_beamset_sep_iso')
  sep_beamset_iso = P.Property('Separate beam set - felles isosenter','sep_beamset_iso', default = True)
  beamset_iso = P.Property('Samme beam set - felles isosenter','beamset')

  for i in range(nr_targets):
    P.Property('CTV' + str(i+1),'CTV' + str(i+1), parent = sep_plan)
  return [sep_plan, sep_beamset_sep_iso, sep_beamset_iso, beamset_iso] 
