# encoding: utf8

# Import local files:
import beam_set_functions as BSF
import case_functions as CF
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF


# Set up beams or arcs, based on region code (i.e. treatment site).
def setup_beams(ss, examination, beam_set, isocenter, region_code, fraction_dose, technique_name, iso_index = 1, beam_index=1):
  if technique_name == '3D-CRT':
    #Two tangetial beams:
    if region_code in RC.breast_tang_l_codes:
      BSF.create_two_beams(beam_set, isocenter, name1 = 'LPO', name2 = 'RAO', gantry_angle1 = '130', gantry_angle2 = '310', collimator_angle1 = '343', collimator_angle2 = '17', iso_index=iso_index, beam_index=beam_index)
      BSF.set_MU(beam_set,['LPO','RAO'], [100, 100] )
    elif region_code in RC.breast_tang_r_codes:
      BSF.create_two_beams(beam_set, isocenter, name1 = 'RPO', name2 = 'LAO', gantry_angle1 = '230', gantry_angle2 = '50', collimator_angle1 = '9', collimator_angle2 = '352', iso_index=iso_index, beam_index=beam_index)
      BSF.set_MU(beam_set,['RPO','LAO'], [100, 100] )
    # Breast with regional lymph nodes:
    elif region_code in RC.breast_reg_l_codes: # Left
      BSF.create_four_beams(beam_set, isocenter, name1 = 'LPO', name2 = 'Venstre', name3 = 'Forfra', name4 = 'RAO', gantry_angle1 = '130', gantry_angle2 = '90', gantry_angle3 = '0', gantry_angle4 = '309', iso_index=iso_index, beam_index=beam_index)
      if fraction_dose == 2:
        BSF.set_MU(beam_set,['LPO','Venstre','Forfra','RAO'], [25, 15, 100, 90] )
      elif fraction_dose == 2.67:
        BSF.set_MU(beam_set,['LPO','Venstre','Forfra','RAO'], [40, 25, 115, 105] )
    elif region_code in RC.breast_reg_r_codes: # Right
      BSF.create_four_beams(beam_set, isocenter, name1 = 'RPO', name2 = 'Høyre', name3 = 'Forfra', name4 = 'LAO', gantry_angle1 = '235', gantry_angle2 = '270', gantry_angle3 = '0', gantry_angle4 = '55', iso_index=iso_index, beam_index=beam_index)
      if fraction_dose == 2:
        BSF.set_MU(beam_set,['RPO','Høyre','Forfra','LAO'], [25, 15, 100, 90] )
      elif fraction_dose == 2.67:
        BSF.set_MU(beam_set,['RPO','Høyre','Forfra','LAO'], [40, 25, 115, 105] )
    elif region_code in RC.brain_whole_codes:
      BSF.create_two_beams(beam_set, isocenter, energy = '10', name1 = 'Høyre', name2 = 'Venstre', gantry_angle1 = '270', gantry_angle2 = '90', collimator_angle1 = '295', collimator_angle2 = '63', iso_index=iso_index, beam_index=beam_index)
      BSF.set_MU(beam_set,['Høyre','Venstre'], [130, 130] )
  elif technique_name == 'VMAT':
    # Brain:
    if region_code in RC.brain_whole_codes: # Whole brain
      BSF.create_single_arc(beam_set, isocenter)
    elif region_code in RC.brain_partial_codes:
      if fraction_dose > 6: # Stereotactic brain
        BSF.create_single_arc(beam_set, isocenter, collimator_angle = '45', iso_index=iso_index, beam_index=beam_index)
      else: # Partial brain
        if SSF.partial_brain_conflict_oars(ss):
          BSF.create_single_arc(beam_set, isocenter, collimator_angle = '45', iso_index=iso_index, beam_index=beam_index)
        else:
          BSF.create_dual_arcs(beam_set, isocenter, iso_index=iso_index, beam_index=beam_index)
    # Breast with regional lymph nodes:
    elif region_code in RC.breast_reg_l_codes:
      BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '310', gantry_stop_angle2 = '179', gantry_start_angle1 = '179', gantry_start_angle2 = '310', iso_index=iso_index, beam_index=beam_index)
    elif region_code in RC.breast_reg_r_codes:
      BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '50', gantry_stop_angle2 = '181', gantry_start_angle1 = '181', gantry_start_angle2 = '50', iso_index=iso_index, beam_index=beam_index)
    # Lung:
    elif region_code in RC.lung_and_mediastinum_codes:
      if region_code in RC.lung_r_codes: # Right
        BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '30', gantry_stop_angle2 = '181', gantry_start_angle1 = '181', gantry_start_angle2 = '30', iso_index=iso_index, beam_index=beam_index)
      elif region_code in RC.lung_l_codes: # Left
        BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '330', gantry_stop_angle2 = '179', gantry_start_angle1 = '179', gantry_start_angle2 = '330', iso_index=iso_index, beam_index=beam_index)
      else: # Mediastinum or both lungs
        BSF.create_dual_arcs(beam_set, isocenter, iso_index=iso_index, beam_index=beam_index)
    # Bladder:
    elif region_code in RC.bladder_codes:
        BSF.create_single_arc(beam_set, isocenter, iso_index=iso_index, beam_index=beam_index)
    # Prostate:
    elif region_code in RC.prostate_codes:
      # Set up beams (arcs). Two arcs if there is a lymph node volume and one arc if not.
      if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name):
        BSF.create_dual_arcs(beam_set, isocenter, collimator_angle1 = '45', collimator_angle2 = '5', iso_index=iso_index, beam_index=beam_index)
      else:
        BSF.create_single_arc(beam_set, isocenter, iso_index=iso_index, beam_index=beam_index)
    # Rectum:
    elif region_code in RC.rectum_codes:
      BSF.create_dual_arcs(beam_set, isocenter, collimator_angle1 = '45', collimator_angle2 = '5', iso_index=iso_index, beam_index=beam_index)
    # Palliative:
    elif region_code in RC.palliative_codes:
      # Stereotactic palliative codes:
      if fraction_dose > 8:
        BSF.create_single_arc(beam_set, isocenter, collimator_angle = '45', iso_index=iso_index, beam_index=beam_index)
      else:
        if region_code in RC.whole_pelvis_codes:
          BSF.create_dual_arcs(beam_set, isocenter, collimator_angle1 = '45', collimator_angle2 = '5', iso_index=iso_index, beam_index=beam_index)
        else:
          if abs(isocenter.x) > 5:
            if isocenter.x > 5 and CF.is_head_first_supine(examination) or not CF.is_head_first_supine(examination) and isocenter.x < -5:
              BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '330', gantry_stop_angle2 = '179', gantry_start_angle1 = '179', gantry_start_angle2 = '330', iso_index=iso_index, beam_index=beam_index)
            else:
              BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '30', gantry_stop_angle2 = '181', gantry_start_angle1 = '181', gantry_start_angle2 = '30', iso_index=iso_index, beam_index=beam_index)
          elif abs(isocenter.y) +5 < abs(SSF.roi_center_y(ss, "External")):
            BSF.create_dual_arcs(beam_set, isocenter, gantry_stop_angle1 = '240', gantry_stop_angle2 = '110', gantry_start_angle1 = '110', gantry_start_angle2 = '240', iso_index=iso_index, beam_index=beam_index)
          else:
            BSF.create_single_arc(beam_set, isocenter, iso_index=iso_index, beam_index=beam_index)
  return len(list(beam_set.Beams))
