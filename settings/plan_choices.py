# encoding: utf8

# Import local files:
import property as P
import structure_set_functions as SSF
from tkinter import messagebox

# Setup techniques:
conformal = P.Property('3D-CRT','Conformal')
vmat = P.Property('VMAT','VMAT', default = True)

'''
# Setup techniques:
conformal = P.Property('3D-CRT','Conformal', next_category = 'optimalisering')
vmat = P.Property('VMAT','VMAT', next_category = 'optimalisering', default = True)
# Optimization choices for vmat/conformal:
for tech in [conformal, vmat]:
  opt_without = P.Property('Uten optimalisering','without', parent = tech, default = True)
  opt_init = P.Property('Initiell optimalisering', 'init', parent = tech)
  opt_init_oar = P.Property('Initiell optimalisering med tilpasning til risikoorganer','oar', parent = tech)
'''
# List of choices:
techniques = [conformal, vmat]
#optimization = [opt_without, opt_init, opt_init_oar]
#optimization_simple = [opt_without, opt_init_oar]


def beam_set_choices(ss):
  nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
  
  sep_plan = P.Property('Separate planer','sep_plan', next_category = 'målvolum')
  sep_beamset_sep_iso = P.Property('Separate beam set - separate isosenter','sep_beamset_sep_iso')
  sep_beamset_iso = P.Property('Separate beam set - felles isosenter','sep_beamset_iso', default = True)
  beamset_iso = P.Property('Samme beam set - felles isosenter','beamset')

  for i in range(nr_targets):
    P.Property('CTV' + str(i+1),'CTV' + str(i+1), parent = sep_plan)
  return [sep_plan, sep_beamset_sep_iso, sep_beamset_iso, beamset_iso] 
