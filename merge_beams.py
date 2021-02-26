# Merges beams with the same gantry, couch and collimator angle
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 10B
# Python 3.6

from connect import *
import math
import sys
# Python 3.6
from System.Windows import *

try:
    beam_set = get_current("BeamSet")
except SystemError:
    raise IOError("No beam set loaded.")
		
target_beams = []
potential_beams = ['LPO','Venstre','Forfra','RAO','Høyre','RPO','LAO','Bakfra']
for beam in beam_set.Beams:
	for i in range(len(potential_beams)):
		if beam.Name == potential_beams[i]:
			target_beams.append(beam_set.Beams[beam.Name])

for t in target_beams:
	beams_to_be_merged = []
	for beam in beam_set.Beams:
		if beam.Name != t.Name and beam.GantryAngle == t.GantryAngle and beam.InitialCollimatorAngle == t.InitialCollimatorAngle and beam.CouchRotationAngle == t.CouchRotationAngle and beam.BeamQualityId == t.BeamQualityId:
			beams_to_be_merged.append(beam.Name)
	if len(list(beams_to_be_merged)) > 0:
		beam_set.MergeBeamSegments(TargetBeamName = t.Name, MergeBeamNames = beams_to_be_merged)
