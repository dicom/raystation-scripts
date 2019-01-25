# encoding: utf8

# Import system libraries:
import math

# Import local files:
import beam_functions as BF
import general_functions as GF
import plan_functions as PF
import region_codes as RC
import roi_functions as ROIF
import structure_set_functions as SSF
import colors as COLORS

# Contains a collection of beam set functions.


# Set presciption (default is median dose, with dose at volume for stereotactic plans)
def add_prescription(beam_set, nr_fractions, fraction_dose, target):
  total_dose = nr_fractions*fraction_dose
  if PF.is_stereotactic(nr_fractions, fraction_dose):
    beam_set.AddDosePrescriptionToRoi(RoiName = target, PrescriptionType = 'DoseAtVolume', DoseValue = total_dose*100, DoseVolume = 99)
  else:
    beam_set.AddDosePrescriptionToRoi(RoiName = target, PrescriptionType = 'MedianDose', DoseValue = total_dose*100)


# Creates two arcs, VMAT
def create_dual_arcs(beam_set, isocenter, gantry_stop_angle1='181', gantry_stop_angle2='179', energy='6', gantry_start_angle1='179', gantry_start_angle2='181', collimator_angle1='5', collimator_angle2='355', couch_angle1='0', couch_angle2='0', iso_index=1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angle1,
    ArcRotationDirection = BF.rotation_direction(gantry_start_angle1, gantry_stop_angle1),
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index),
    Description = '',
    GantryAngle = gantry_start_angle1 ,
    CollimatorAngle = collimator_angle1,
    CouchAngle = couch_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angle2,
    ArcRotationDirection = BF.rotation_direction(gantry_start_angle2, gantry_stop_angle2),
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index+1),
    Description = '',
    GantryAngle = gantry_start_angle2,
    CollimatorAngle = collimator_angle2,
    CouchAngle = couch_angle2
  )
  b2.Number = beam_index + 1


# Creates four beams, 3D-CRT
def create_four_beams(beam_set, isocenter, energy='6', name1='', name2='', name3='', name4='', gantry_angle1='181', gantry_angle2='179', gantry_angle3='181', gantry_angle4='179', collimator_angle1='0', collimator_angle2='0', collimator_angle3='0', collimator_angle4='0', couch_angle1='0', couch_angle2 = '0', couch_angle3 = '0', couch_angle4 = '0', iso_index = 1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreatePhotonBeam(
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name1,
    Description = '',
    GantryAngle = gantry_angle1 ,
    CollimatorAngle = collimator_angle1,
    CouchAngle = couch_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreatePhotonBeam(
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name2,
    Description = '',
    GantryAngle = gantry_angle2,
    CollimatorAngle = collimator_angle2,
    CouchAngle = couch_angle2
  )
  b2.Number = beam_index + 1
  b3 = beam_set.CreatePhotonBeam(
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name3,
    Description = '',
    GantryAngle = gantry_angle3 ,
    CollimatorAngle = collimator_angle3,
    CouchAngle = couch_angle3
  )
  b3.Number = beam_index + 2
  b4 = beam_set.CreatePhotonBeam(
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name4,
    Description = '',
    GantryAngle = gantry_angle4,
    CollimatorAngle = collimator_angle4,
    CouchAngle = couch_angle4
  )
  b4.Number = beam_index + 3


# Adjusts leaf positions on the first segment of each beam for 3DCRT breast plans.
# Leafs (on anterior-lateral leaf bank) are pulled 2.5 cm out from their initial position.
# For locoregional plans, this is only done in the part of the field covering the breast.
def create_margin_air_for_3dcrt_breast(ss, beam_set, region_code, breast_name, nodes_name):

  for beam in beam_set.Beams:
    segment = beam.Segments[0]
    leaf_positions = segment.LeafPositions
    jaw = segment.JawPositions
    y1 = jaw[2]

    if region_code in RC.breast_reg_codes:
      if SSF.has_named_roi_with_contours(ss, nodes_name) and SSF.has_named_roi_with_contours(ss, breast_name):
        nodes = ss.RoiGeometries[nodes_name].GetBoundingBox()
        breast = ss.RoiGeometries[breast_name].GetBoundingBox()
        y2 =  jaw[3] - (nodes[1].z - breast[1].z + 1)
      else:
        y2 = jaw[3]
    else:
      y2 = jaw[3]

    # don't forget that mlc 50 is index leafPositions[x][49]
    mlcY1 = int(math.floor((y1 + 20) * 2) + 1.0)
    mlcY2 = int(math.ceil ((y2 + 20) * 2))

    for leaf in range(mlcY1-1, mlcY2+1):
      if beam.Name in ['LAO', 'LPO']:
        leaf_positions[0][leaf] = leaf_positions[0][leaf] - 2.5
      elif beam.Name in ['RAO','RPO']:
        leaf_positions[1][leaf] = leaf_positions[1][leaf] +2.5

    segment.LeafPositions = leaf_positions


# Creates a single arc, VMAT
def create_single_arc(beam_set, isocenter, gantry_stop_angle='179', energy='6', gantry_start_angle='181', collimator_angle='5', couch_angle='0', iso_index = 1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angle,
    ArcRotationDirection = 'Clockwise',
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index),
    Description = '',
    GantryAngle = gantry_start_angle,
    CollimatorAngle = collimator_angle,
    CouchAngle = couch_angle
  )
  b.Number = beam_index


# Creates two beams, 3D-CRT
def create_two_beams(beam_set, isocenter, energy='6', name1='', name2='', gantry_angle1='181', gantry_angle2='179', collimator_angle1='5', collimator_angle2='355', couch_angle1='0', couch_angle2='0', iso_index=1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreatePhotonBeam(
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name1,
    Description = '',
    GantryAngle = gantry_angle1 ,
    CollimatorAngle = collimator_angle1,
    CouchAngle = couch_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreatePhotonBeam(
    Energy = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name2,
    Description = '',
    GantryAngle = gantry_angle2,
    CollimatorAngle = collimator_angle2,
    CouchAngle = couch_angle2
  )
  b2.Number = beam_index + 1


# Creates the label from region code, fraction dose, number of fractions and which technique (VMAT or 3D-CRT). Is used as beam set name.
def label(region_code, fraction_dose, nr_fractions, technique, background_dose=0):
  if technique == 'Conformal': # 3D-CRT
    t = 'I:' + str(background_dose) + '-'
  else:
    if PF.is_stereotactic(nr_fractions, fraction_dose):
      t = 'S:' + str(background_dose) + '-' #Stereotactic
    else:
      t = 'V:' + str(background_dose) + '-' #VMAT
  return str(region_code) + t + GF.dynamic_round(background_dose + fraction_dose*nr_fractions) + ':' + str(nr_fractions)


# Creates the label from region code, fraction dose, number of fractions and which technique (VMAT or 3D-CRT).
# Is used as beam set name for the addition beam sets for stereotactic brain with multiple targets
def label_s(region_code, fraction_dose, nr_fractions):
  t = 'S:0-'
  return str(region_code) + t + GF.dynamic_round(fraction_dose*nr_fractions) + ':' + str(nr_fractions)


# Sets the monitor units of the beams in a beam set based on a list of names and monitor units.
def set_MU(beam_set, names, mu):
  for i in range(len(names)):
    beam_set.Beams[names[i]].BeamMU = mu[i]
