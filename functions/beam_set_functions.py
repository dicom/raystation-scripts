# encoding: utf8

# Import system libraries:
import math

# Import local files:
import beam_functions as BF
import general_functions as GF
import objective_functions as OBJF
import region_codes as RC
import roi_functions as ROIF
import structure_set_functions as SSF
import colors as COLORS
import rois as ROIS

# Contains a collection of beam set functions.


# Set the beam set presciption.
def add_prescription(beam_set, prescription):
  if prescription.is_stereotactic():
    # DoseAtVolume:
    beam_set.AddRoiPrescriptionDoseReference(RoiName = prescription.target, PrescriptionType = prescription.type, DoseValue = prescription.total_dose*100, DoseVolume = prescription.volume_percent)
  else:
    # MedianDose:
    beam_set.AddRoiPrescriptionDoseReference(RoiName = prescription.target, PrescriptionType = prescription.type, DoseValue = prescription.total_dose*100)


# Creates two arcs (VMAT).
def create_dual_arcs(beam_set, isocenter, energy='6', gantry_stop_angles=['181', '179'], gantry_start_angles=['179', '181'], collimator_angles=['5', '355'], couch_angles=['0', '0'], iso_index=1, beam_index=1, bolus=None):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angles[0],
    ArcRotationDirection = BF.rotation_direction(gantry_start_angles[0], gantry_stop_angles[0]),
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index),
    Description = '',
    GantryAngle = gantry_start_angles[0],
    CollimatorAngle = collimator_angles[0],
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angles[0]
  )
  b1.Number = beam_index
  b2 = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angles[1],
    ArcRotationDirection = BF.rotation_direction(gantry_start_angles[1], gantry_stop_angles[1]),
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index+1),
    Description = '',
    GantryAngle = gantry_start_angles[1],
    CollimatorAngle = collimator_angles[1],
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angles[1]
  )
  b2.Number = beam_index + 1
  if bolus:
    for b in [b1, b2]:
      b.SetBolus(BolusName = bolus.OfRoi.Name)
  return [b1, b2]


# Creates a single arc (VMAT).
def create_single_arc(beam_set, isocenter, energy='6', gantry_stop_angle='179', gantry_start_angle='181', collimator_angle='5', couch_angle='0', iso_index = 1, beam_index=1, bolus=None):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angle,
    ArcRotationDirection = BF.rotation_direction(gantry_start_angle, gantry_stop_angle),
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index),
    Description = '',
    GantryAngle = gantry_start_angle,
    CollimatorAngle = collimator_angle,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle
  )
  b.Number = beam_index
  if bolus:
    b.SetBolus(BolusName = bolus.OfRoi.Name)
  return b


# Creates two beams (3D-CRT).
def create_two_beams(beam_set, isocenter, energy='6', name1='', name2='', gantry_angle1='181', gantry_angle2='179', collimator_angle1='5', collimator_angle2='355', couch_angle1='0', couch_angle2='0', iso_index=1, beam_index=1, bolus=None):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name1,
    Description = '',
    GantryAngle = gantry_angle1,
    CouchRotationAngle = couch_angle1,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CollimatorAngle = collimator_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name2,
    Description = '',
    GantryAngle = gantry_angle2,
    CouchRotationAngle = couch_angle2,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CollimatorAngle = collimator_angle2
  )
  b2.Number = beam_index + 1
  if bolus:
    for b in [b1, b2]:
      b.SetBolus(BolusName = bolus.OfRoi.Name)


# Creates a label based on region code, presciption and technique (VMAT or 3D-CRT). The label is used as beam set name.
def label(presciption, technique, background_dose=0):
  if technique == 'Conformal': # 3D-CRT
    t = 'I:' + str(background_dose) + '-'
  else:
    if presciption.is_stereotactic():
      t = 'S:' + str(background_dose) + '-' #Stereotactic
    else:
      t = 'V:' + str(background_dose) + '-' #VMAT
  return str(presciption.region_code) + t + GF.dynamic_round(background_dose + presciption.total_dose) + ':' + str(presciption.nr_fractions)


# Creates the label based on region code, fraction dose, number of fractions and which technique (VMAT or 3D-CRT).
# Is used as beam set name for the additional beam sets for stereotactic brain with multiple targets
def label_s(region_code, fraction_dose, nr_fractions):
  t = 'S:0-'
  return str(region_code) + t + GF.dynamic_round(fraction_dose*nr_fractions) + ':' + str(nr_fractions)


# Sets the monitor units of the beams in a beam set based on a list of names and monitor units.
def set_MU(beam_set, names, mu):
  for i in range(len(names)):
    beam_set.Beams[names[i]].BeamMU = mu[i]


# Set the beam set dose grid (0.2x0.2x0.2 cm3 for stereotactic treatments/prostate/partial brain - 0.3x03x0.3 cm3 otherwise).
def set_dose_grid(beam_set, presciption):
  # Default grid size:
  size = 0.3
  if presciption.is_stereotactic() or presciption.region_code in RC.prostate_codes or presciption.region_code in RC.brain_codes:
    size = 0.2
  beam_set.SetDefaultDoseGrid(VoxelSize={'x':size, 'y':size, 'z':size})
