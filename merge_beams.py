from connect import *
import math
import sys
clr.AddReference("PresentationFramework")
from System.Windows import *

try:
    beam_set = get_current("BeamSet")
except SystemError:
    raise IOError("No beam set loaded.")
		
target_beams = []
potential_beams = ['LPO','Venstre','Forfra','RAO','Høyre'.decode('utf8', 'replace'),'RPO','LAO','Bakfra']
for beam in beam_set.Beams:
	for i in range(len(potential_beams)):
		if beam.Name == potential_beams[i]:
			target_beams.append(beam_set.Beams[beam.Name])

for t in target_beams:
	beams_to_be_merged = []
	for beam in beam_set.Beams:
		if beam.Name != t.Name and beam.GantryAngle == t.GantryAngle and beam.InitialCollimatorAngle == t.InitialCollimatorAngle and beam.CouchAngle == t.CouchAngle and beam.BeamQualityId == t.BeamQualityId:
			beams_to_be_merged.append(beam.Name)
	if len(list(beams_to_be_merged)) > 0:
		beam_set.MergeBeamSegments(TargetBeamName = t.Name, MergeBeamNames = beams_to_be_merged)
