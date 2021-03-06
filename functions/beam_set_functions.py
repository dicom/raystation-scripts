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


# Set presciption (default is median dose, with dose at volume for stereotactic plans).
def add_prescription(beam_set, nr_fractions, fraction_dose, target):
  total_dose = nr_fractions*fraction_dose
  if is_stereotactic(nr_fractions, fraction_dose):
    beam_set.AddDosePrescriptionToRoi(RoiName = target, PrescriptionType = 'DoseAtVolume', DoseValue = total_dose*100, DoseVolume = 99)
  else:
    beam_set.AddDosePrescriptionToRoi(RoiName = target, PrescriptionType = 'MedianDose', DoseValue = total_dose*100)


# Creates two arcs (VMAT).
def create_dual_arcs(beam_set, isocenter, energy='6', gantry_stop_angle1='181', gantry_stop_angle2='179', gantry_start_angle1='179', gantry_start_angle2='181', collimator_angle1='5', collimator_angle2='355', couch_angle1='0', couch_angle2='0', iso_index=1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angle1,
    ArcRotationDirection = BF.rotation_direction(gantry_start_angle1, gantry_stop_angle1),
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index),
    Description = '',
    GantryAngle = gantry_start_angle1 ,
    CollimatorAngle = collimator_angle1,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreateArcBeam(
    ArcStopGantryAngle = gantry_stop_angle2,
    ArcRotationDirection = BF.rotation_direction(gantry_start_angle2, gantry_stop_angle2),
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= 'Arc '+str(beam_index+1),
    Description = '',
    GantryAngle = gantry_start_angle2,
    CollimatorAngle = collimator_angle2,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle2
  )
  b2.Number = beam_index + 1


# Creates four beams (3D-CRT).
def create_four_beams(beam_set, isocenter, energy='6', name1='', name2='', name3='', name4='', gantry_angle1='181', gantry_angle2='179', gantry_angle3='181', gantry_angle4='179', collimator_angle1='0', collimator_angle2='0', collimator_angle3='0', collimator_angle4='0', couch_angle1='0', couch_angle2 = '0', couch_angle3 = '0', couch_angle4 = '0', iso_index = 1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name1,
    Description = '',
    GantryAngle = gantry_angle1 ,
    CollimatorAngle = collimator_angle1,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name2,
    Description = '',
    GantryAngle = gantry_angle2,
    CollimatorAngle = collimator_angle2,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle2
  )
  b2.Number = beam_index + 1
  b3 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name3,
    Description = '',
    GantryAngle = gantry_angle3 ,
    CollimatorAngle = collimator_angle3,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle3
  )
  b3.Number = beam_index + 2
  b4 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name4,
    Description = '',
    GantryAngle = gantry_angle4,
    CollimatorAngle = collimator_angle4,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle4
  )
  b4.Number = beam_index + 3


# Adjusts leaf positions on the first segment of each beam for 3DCRT breast plans.
# Leafs (on anterior-lateral leaf bank) are pulled 2.5 cm out from their initial position.
# For locoregional plans, this is only done in the part of the field covering the breast.
def create_margin_air_for_3dcrt_breast(ss, beam_set, region_code):
  roi_dict = SSF.create_roi_dict(ss)
  for beam in beam_set.Beams:
    segment = beam.Segments[0]
    leaf_positions = segment.LeafPositions
    jaw = segment.JawPositions
    y1 = jaw[2]
    if region_code in RC.breast_reg_codes:
      if SSF.has_named_roi_with_contours(ss, ROIS.ptv_pc.name) and SSF.has_named_roi_with_contours(ss, ROIS.ptv_nc.name) and beam.Name in ['RPO','LPO']:
        nodes = ss.RoiGeometries[ROIS.ptv_nc.name].GetBoundingBox()
        breast = ss.RoiGeometries[ROIS.ptv_pc.name].GetBoundingBox()
        y2 =  jaw[3] - (nodes[1].z - breast[1].z + 1)
      elif SSF.has_named_roi_with_contours(ss, ROIS.ptv_50c.name) and SSF.has_named_roi_with_contours(ss, ROIS.ptv_47c.name) and beam.Name in ['RPO','LPO']:
        nodes = ss.RoiGeometries[ROIS.ptv_47c.name].GetBoundingBox()
        breast = ss.RoiGeometries[ROIS.ptv_50c.name].GetBoundingBox()
        y2 =  jaw[3] - (nodes[1].z - breast[1].z + 1)
      else:
        y2 = jaw[3]
    else:
      y2 = jaw[3]
    # (Don't forget that MLC number 50 has index leafPositions[x][49])
    mlcY1 = int(math.floor((y1 + 20) * 2) + 1.0)
    mlcY2 = int(math.ceil ((y2 + 20) * 2))
    for leaf in range(mlcY1-1, mlcY2+1):
      if beam.Name == 'LAO' and region_code in RC.breast_r_codes:
        leaf_positions[0][leaf] = leaf_positions[0][leaf] - 2.5
      elif beam.Name == 'RAO' and region_code in RC.breast_l_codes:
        leaf_positions[1][leaf] = leaf_positions[1][leaf] + 2.5
      elif beam.Name in ['RPO', 'RPO 1']:
        leaf_positions[1][leaf] = leaf_positions[1][leaf] + 2.5
      elif beam.Name in ['LPO', 'LPO 1']:
        leaf_positions[0][leaf] = leaf_positions[0][leaf] - 2.5
    segment.LeafPositions = leaf_positions


# Creates a single arc (VMAT).
def create_single_arc(beam_set, isocenter, energy='6', gantry_stop_angle='179', gantry_start_angle='181', collimator_angle='5', couch_angle='0', iso_index = 1, beam_index=1):
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


# Creates three beams (3D-CRT).
def create_three_beams(beam_set, isocenter, energy='6', name1='', name2='', name3='', gantry_angle1='181', gantry_angle2='179', gantry_angle3='181', collimator_angle1='0', collimator_angle2='0', collimator_angle3='0', couch_angle1='0', couch_angle2 = '0', couch_angle3 = '0', iso_index = 1, beam_index=1):
  beam_set.ClearBeams(RemoveBeams = 'True')
  b1 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name1,
    Description = '',
    GantryAngle = gantry_angle1 ,
    CollimatorAngle = collimator_angle1,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle1
  )
  b1.Number = beam_index
  b2 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name2,
    Description = '',
    GantryAngle = gantry_angle2,
    CollimatorAngle = collimator_angle2,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle2
  )
  b2.Number = beam_index + 1
  b3 = beam_set.CreatePhotonBeam(
    BeamQualityId = energy,
    IsocenterData={ 'Position': { 'x': isocenter.x, 'y': isocenter.y, 'z': isocenter.z }, 'NameOfIsocenterToRef': "Iso"+str(iso_index), 'Name': "Iso"+str(iso_index), 'Color': COLORS.iso },
    Name= name3,
    Description = '',
    GantryAngle = gantry_angle3 ,
    CollimatorAngle = collimator_angle3,
    CouchPitchAngle = '0',
    CouchRollAngle = '0',
    CouchRotationAngle = couch_angle3
  )
  b3.Number = beam_index + 2


# Creates two beams (3D-CRT).
def create_two_beams(beam_set, isocenter, energy='6', name1='', name2='', gantry_angle1='181', gantry_angle2='179', collimator_angle1='5', collimator_angle2='355', couch_angle1='0', couch_angle2='0', iso_index=1, beam_index=1):
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


# Creates a label based on region code, fraction dose, number of fractions and technique (VMAT or 3D-CRT). The label is used as beam set name.
def label(region_code, fraction_dose, nr_fractions, technique, background_dose=0):
  if technique == 'Conformal': # 3D-CRT
    t = 'I:' + str(background_dose) + '-'
  else:
    if is_stereotactic(nr_fractions, fraction_dose):
      t = 'S:' + str(background_dose) + '-' #Stereotactic
    else:
      t = 'V:' + str(background_dose) + '-' #VMAT
  return str(region_code) + t + GF.dynamic_round(background_dose + fraction_dose*nr_fractions) + ':' + str(nr_fractions)


# Creates the label based on region code, fraction dose, number of fractions and which technique (VMAT or 3D-CRT).
# Is used as beam set name for the additional beam sets for stereotactic brain with multiple targets
def label_s(region_code, fraction_dose, nr_fractions):
  t = 'S:0-'
  return str(region_code) + t + GF.dynamic_round(fraction_dose*nr_fractions) + ':' + str(nr_fractions)


# Sets the monitor units of the beams in a beam set based on a list of names and monitor units.
def set_MU(beam_set, names, mu):
  for i in range(len(names)):
    beam_set.Beams[names[i]].BeamMU = mu[i]


def set_up_treat_and_protect_for_stereotactic_lung(beam_set, protect_roi, margin):
    beam_set.SelectToUseROIasTreatOrProtectForAllBeams(RoiName = protect_roi)
    for beam in beam_set.Beams:
        beam.SetTreatAndProtectMarginsForBeam(TopMargin = margin, BottomMargin = margin, LeftMargin = margin, RightMargin = margin, Roi = protect_roi)


def set_up_beams_and_optimization_for_tangential_breast(plan, beam_set, plan_optimization, protect_roi):
	beam_set.SetTreatmentTechnique(Technique = 'Conformal')
	beam_set.SelectToUseROIasTreatOrProtectForAllBeams(RoiName = protect_roi)
	for beam in beam_set.Beams:
		beam.SetTreatAndProtectMarginsForBeam(TopMargin = 0.5, BottomMargin = 0.5, LeftMargin = 0.5, RightMargin = 0.5, Roi = protect_roi)
	beam_set.TreatAndProtect(ShowProgress=True)
	beam_set.CopyBeamsFromBeamSet(BeamSetToCopyFrom = beam_set)
	beam_set.SetTreatmentTechnique(Technique = 'SMLC')
	po = plan_optimization
	tss = po.OptimizationParameters.TreatmentSetupSettings[0]
	tss.SegmentConversion.UseConformalSequencing = False
	for bs in tss.BeamSettings:
		if bs.ForBeam.Name in ['RPO','LPO','LAO','RAO']:
			bs.EditBeamOptimizationSettings(OptimizationTypes=["None"], SelectCollimatorAngle=False, AllowBeamSplit=False, JawMotion="Automatic")
	po.ResetOptimization()
	po.AutoScaleToPrescription = False
	tss.SegmentConversion.UseConformalSequencing = False
	opt_param = po.OptimizationParameters.DoseCalculation.IterationsInPreparationsPhase = 7
	po.OptimizationParameters.DoseCalculation.ComputeFinalDose = True
	tss.SegmentConversion.MaxNumberOfSegments = 10
	tss.SegmentConversion.MinSegmentArea = 4
	tss.SegmentConversion.MinSegmentMUPerFraction = 4


def set_up_beams_and_optimization_for_regional_breast(plan, beam_set, protect_roi, region_code):
	if region_code in [242,244]:
		beam_set.CopyBeam(BeamName = 'RPO')
		if beam_set.FractionationPattern.NumberOfFractions == 15:
			set_MU(beam_set,['RPO 1'], [60] )
		elif beam_set.FractionationPattern.NumberOfFractions == 25:
			set_MU(beam_set,['RPO 1'], [50] )
	elif region_code in [241, 243]:
		beam_set.CopyBeam(BeamName = 'LPO')
		if beam_set.FractionationPattern.NumberOfFractions == 15:
			set_MU(beam_set,['LPO 1'], [60] )
		elif beam_set.FractionationPattern.NumberOfFractions == 25:
			set_MU(beam_set,['LPO 1'], [50] )
	if beam_set.FractionationPattern.NumberOfFractions == 15:
		beam_set.SelectToUseROIasTreatOrProtectForAllBeams(RoiName = protect_roi)
		for beam in beam_set.Beams:
			beam.SetTreatAndProtectMarginsForBeam(TopMargin = 0.5, BottomMargin = 0.5, LeftMargin = 0.5, RightMargin = 0.5, Roi = protect_roi)
		beam_set.TreatAndProtect(ShowProgress=True)
	elif beam_set.FractionationPattern.NumberOfFractions == 25:
		beam_set.SelectToUseROIasTreatOrProtectForAllBeams(RoiName = ROIS.ptv_50c.name)
		beam_set.SelectToUseROIasTreatOrProtectForAllBeams(RoiName = ROIS.ptv_47c.name)
		for beam in beam_set.Beams:
			beam.SetTreatAndProtectMarginsForBeam(TopMargin = 0.5, BottomMargin = 0.5, LeftMargin = 0.5, RightMargin = 0.5, Roi = ROIS.ptv_50c.name)
			beam.SetTreatAndProtectMarginsForBeam(TopMargin = 0.5, BottomMargin = 0.5, LeftMargin = 0.5, RightMargin = 0.5, Roi = ROIS.ptv_47c.name)
		beam_set.TreatAndProtect(ShowProgress=True)
	for beam in beam_set.Beams:
		segments = beam.Segments[0]
		jaw = segments.JawPositions
		if beam.Name in ['RPO 1','LAO','LPO 1','RAO']: 
			jaw[3] = 0
		elif beam.Name in ['Høyre','Forfra','Venstre']:
			jaw[2] = 0
		segments.JawPositions = jaw
	if region_code in [242,244]:
		beam_set.CopyBeam(BeamName = 'RPO 1')
		beam_set.CopyBeam(BeamName = 'Høyre')
		beam_set.CopyBeam(BeamName = 'Forfra')
		beam_set.CopyBeam(BeamName = 'LAO')
	elif region_code in [241, 243]:
		beam_set.CopyBeam(BeamName = 'LPO 1')
		beam_set.CopyBeam(BeamName = 'Venstre')
		beam_set.CopyBeam(BeamName = 'Forfra')
		beam_set.CopyBeam(BeamName = 'RAO')
	beam_set.SetTreatmentTechnique(Technique = 'SMLC')
	po = plan.PlanOptimizations[0]
	tss = po.OptimizationParameters.TreatmentSetupSettings[0]
	for bs in tss.BeamSettings:
		if bs.ForBeam.Name in ['RPO','LPO','LAO','RAO','Høyre','Venstre','Forfra','RPO 1','LPO 1']:
			bs.EditBeamOptimizationSettings(OptimizationTypes=["None"], SelectCollimatorAngle=False, AllowBeamSplit=False, JawMotion="Automatic")
		elif bs.ForBeam.Name in ['RPO 2','LPO 2']:
			bs.EditBeamOptimizationSettings(OptimizationTypes=["SegmentOpt","SegmentMU"], SelectCollimatorAngle=False, AllowBeamSplit=False, JawMotion="Automatic")
		elif bs.ForBeam.Name in ['Høyre 1','Venstre 1','Forfra 1']:
			bs.EditBeamOptimizationSettings(OptimizationTypes=["SegmentOpt","SegmentMU"], SelectCollimatorAngle=False, AllowBeamSplit=False, JawMotion="Use limits as max", TopJaw = 0)
		elif bs.ForBeam.Name in ['LAO 1','RAO 1']:
			bs.EditBeamOptimizationSettings(OptimizationTypes=["SegmentOpt","SegmentMU"], SelectCollimatorAngle=False, AllowBeamSplit=False, JawMotion="Use limits as max", BottomJaw = 0)
	po.ResetOptimization()
	po.AutoScaleToPrescription = False
	tss.SegmentConversion.UseConformalSequencing = False
	opt_param = po.OptimizationParameters.DoseCalculation.IterationsInPreparationsPhase = 7
	po.OptimizationParameters.DoseCalculation.ComputeFinalDose = True
	tss.SegmentConversion.MaxNumberOfSegments = 15
	tss.SegmentConversion.MinSegmentArea = 4
	tss.SegmentConversion.MinSegmentMUPerFraction = 4


def close_leaves_behind_jaw_for_regional_breast(beam_set):
	for beam in beam_set.Beams:
		if beam.Name in ['Høyre','Venstre','LPO 1','RAO','Forfra','RPO 1','LAO']:
			segments = beam.Segments[0]
			leaf_positions = segments.LeafPositions
			jaw = segments.JawPositions
			y1 = jaw[2]
			y2 = jaw[3]
			first_x1 = leaf_positions[0][1]
			last_x1 = leaf_positions[0][79]
			first_x2 = leaf_positions[1][1]
			last_x2 = leaf_positions[1][79]
			# Get the last corresponding MLC that is in the field:
			mlcY1 = math.floor((y1 + 20) * 2) + 1.0
			mlcY2 = math.ceil ((y2 + 20) * 2)
			# (Don't forget that MLC number 50 has the index leafPositions[0][49])
			for i in range(0, int(mlcY1 -2)):
				leaf_positions[0][i] = first_x1
				leaf_positions[1][i] = first_x2
			for j in range(int(mlcY2 +1), 80):
				leaf_positions[0][j] = last_x1
				leaf_positions[1][j] = last_x2
			if beam.Name in ['LAO','LPO 1']:
				if abs(leaf_positions[1][int(mlcY2)-1]-leaf_positions[1][int(mlcY2)-2]) > 1:
					leaf_positions[1][int(mlcY2)-1] = leaf_positions[1][int(mlcY2)-2]
					leaf_positions[1][int(mlcY2)] = leaf_positions[1][int(mlcY2)-2]
				elif abs(leaf_positions[1][int(mlcY2)-1]-leaf_positions[1][int(mlcY2)])>1:
					leaf_positions[1][int(mlcY2)] = leaf_positions[1][int(mlcY2)-1]
			elif beam.Name in ['RPO 1','RAO']:
				if abs(leaf_positions[0][int(mlcY2)-1]-leaf_positions[0][int(mlcY2)-2]) > 1:
					leaf_positions[0][int(mlcY2)-1] = leaf_positions[0][int(mlcY2)-2]
					leaf_positions[0][int(mlcY2)] = leaf_positions[0][int(mlcY2)-2]
				elif abs(leaf_positions[0][int(mlcY2)-1]-leaf_positions[0][int(mlcY2)])>1:
					leaf_positions[0][int(mlcY2)] = leaf_positions[0][int(mlcY2)-1]
			segments.LeafPositions = leaf_positions

# Returns True if the combination of nr_fractions and fraction_dose given appears to be stereotactic.
def is_stereotactic(nr_fractions, fraction_dose):
  if nr_fractions in [3, 5, 8] and fraction_dose in [15, 11, 7, 8, 9] or nr_fractions == 1 and fraction_dose > 14:
    return True
  else:
    return False

# Set the beam set dose grid (0.2x0.2x0.2 cm3 for stereotactic treatments/prostate/partial brain - 0.3x03x0.3 cm3 otherwise).
def set_dose_grid(beam_set, region_code, nr_fractions, fraction_dose):
  # Default grid size:
  size = 0.3
  if is_stereotactic(nr_fractions, fraction_dose) or region_code in RC.prostate_codes or region_code in RC.brain_codes:
    size = 0.2
  beam_set.SetDefaultDoseGrid(VoxelSize={'x':size, 'y':size, 'z':size})
