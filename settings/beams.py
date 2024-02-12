# encoding: utf8

# Import local files:
import beam_set_functions as BSF
import case_functions as CF
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF


# Set up beams or arcs, based on region code (i.e. treatment site).
def setup_beams(ss, examination, beam_set, isocenter, region_code, fraction_dose, technique_name, energy_name, iso_index = 1, beam_index=1):
  bolus = SSF.bolus(ss)
  if technique_name == '3D-CRT':
    # 3D-CRT:
    if region_code in RC.extremity_codes:
      # Extremities:
      BSF.create_two_beams(beam_set, isocenter, energy = '6', name1 = 'Forfra', name2 = 'Bakfra', gantry_angle1 = '0', gantry_angle2 = '180', collimator_angle1 = '0', collimator_angle2 = '0', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      BSF.set_MU(beam_set,['Forfra','Bakfra'], [130, 130] )
    elif region_code in RC.brain_whole_codes:
      # Whole brain:
      BSF.create_two_beams(beam_set, isocenter, energy = '6', name1 = 'Høyre', name2 = 'Venstre', gantry_angle1 = '270', gantry_angle2 = '90', collimator_angle1 = '295', collimator_angle2 = '63', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      BSF.set_MU(beam_set,['Høyre','Venstre'], [130, 130] )
  elif technique_name == 'VMAT':
    # VMAT:
    # Brain:
    if region_code in RC.brain_whole_codes:
      # Whole brain:
      BSF.create_single_arc(beam_set, isocenter)
    elif region_code in RC.brain_partial_codes:
      # Partial brain:
      if fraction_dose > 15:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      elif fraction_dose > 6: # Stereotactic brain
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      else:
        # Partial brain (ordinary fractionation):
        if SSF.partial_brain_conflict_oars(ss):
          BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '45', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
        else:
          BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    # Breast partial/whole/regional:
    elif region_code in RC.breast_partial_l_codes:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '300', gantry_start_angle = '179', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.breast_partial_r_codes:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '60', gantry_start_angle = '181', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.breast_l_codes:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '285', gantry_start_angle = '179', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.breast_r_codes:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '75', gantry_start_angle = '181', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.breast_bilateral_codes:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    # Lung:
    elif region_code in RC.lung_and_mediastinum_codes:
      if region_code in RC.lung_r_codes:
        # Right:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '30', gantry_start_angle = '181', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      elif region_code in RC.lung_l_codes:
        # Left:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '330', gantry_start_angle = '179', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      else:
        # Mediastinum or both lungs:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.bladder_codes:
      # Bladder:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.prostate_codes:
      # Prostate:
      if SSF.has_roi_with_shape(ss, ROIS.ptv_56.name) or SSF.has_roi_with_shape(ss, ROIS.ptv__50.name):
        # With lymph nodes:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      else:
        # Without lymph nodes:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.rectum_codes:
      # Rectum:
      BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
    elif region_code in RC.palliative_codes:
      # Palliative treatment:
      if fraction_dose > 8:
        # Stereotactic fractionation:
        BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
      else:
        # 'Normal' fractionation:
        if region_code in RC.whole_pelvis_codes:
          BSF.create_single_arc(beam_set, isocenter, energy = energy_name, collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
        else:
          if abs(isocenter.x) > 5:
            # Lateral treatment volume:
            if isocenter.x > 5 and CF.is_head_first_supine(examination) or not CF.is_head_first_supine(examination) and isocenter.x < -5:
              BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '330', gantry_start_angle = '179', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
            else:
              BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '30', gantry_start_angle = '181', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
          elif abs(isocenter.y) + 5 < abs(SSF.roi_center_y(ss, "External")):
            # Anterior treatment volume:
            BSF.create_single_arc(beam_set, isocenter, energy = energy_name, gantry_stop_angle = '250', gantry_start_angle = '110', collimator_angle = '5', iso_index=iso_index, beam_index=beam_index, bolus=bolus)
          else:
            BSF.create_single_arc(beam_set, isocenter, energy = energy_name, iso_index=iso_index, beam_index=beam_index, bolus=bolus)
  # Return the number of beams created:
  return len(list(beam_set.Beams))
