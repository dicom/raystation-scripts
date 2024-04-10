# encoding: utf8

# Import local files:
import region_codes as RC
import rois as ROIS
import structure_set_functions as SSF

# Prescription class - holds information on total dose, nr of fractions and fraction dose.
class Prescription(object):

  def __init__(self, total_dose, nr_fractions, type, volume_percent=None, roi_name=None):
    # Verify input:
    assert 1 <= total_dose <= 100, "total_dose is not in a valid range (1-100): %r" % total_dose
    assert 1 <= nr_fractions <= 40, "nr_fractions is not in a valid range (1-40): %r" % nr_fractions
    assert isinstance(type, str), "type is not a string: %r" % type
    assert type in ['MedianDose', 'DoseAtVolume'] # (more than than these two exists, but lets stick to these two for now)
    if roi_name is not None:
      assert isinstance(roi_name, str), "roi_name is not a string (or None): %r" % roi_name
    # Assign parameters:
    self.total_dose = round(float(total_dose), 2)
    self.nr_fractions = int(nr_fractions)
    self.fraction_dose = self.total_dose / self.nr_fractions
    self.roi_name = roi_name
    self.type = type
    # If DVH prescription type is used, we need to set the volume percent:
    if type == 'DoseAtVolume':
      # Verify that we have a valid DVH value (range 0-100):
      assert 0 <= volume_percent <= 100, "volume_percent is not in a valid range (0-100) (which it must be when DoseAtVolume type prescription is used) %r" % volume_percent 
      self.volume_percent = volume_percent
    else:
      # MedianDose:
      self.volume_percent = 50
        
  # Override the default implementation of equality.
  def __eq__(self, other):
    if isinstance(other, Prescription):
      return [self.total_dose, self.nr_fractions, self.type, self.volume_percent, self.roi_name] == [other.total_dose, other.nr_fractions, other.type, other.volume_percent, other.roi_name]
    return NotImplemented
  
  # Overrides the default implementation of hash.
  def __hash__(self):
    return hash(tuple(sorted(self.__dict__.items())))
  
  # Gives a description (string) of this Prescription object.
  def description(self):
    return str(self.total_dose) + " Gy / " + str(self.nr_fractions) + " fx @ D" + str(self.volume_percent)
  
  # Gives True if the prescription is stereotactic and False if not.
  def is_stereotactic(self):
    result = False
    if self.type == 'DoseAtVolume' and self.volume_percent >= 98:
      result = True
    return result


# Define lists of "known" prescriptions for various sites:
brain_whole = [
  Prescription(20, 5, 'MedianDose'),
  Prescription(25, 10, 'MedianDose'),
  Prescription(30, 10, 'MedianDose')
]
brain_partial = [
  # Conventional:
  Prescription(25, 5, 'MedianDose'),
  Prescription(34, 10, 'MedianDose'),
  Prescription(39, 13, 'MedianDose'),
  Prescription(40.05, 15, 'MedianDose'),
  Prescription(50, 20, 'MedianDose'),
  Prescription(54, 27, 'MedianDose'),
  Prescription(50.4, 28, 'MedianDose'),
  Prescription(54, 30, 'MedianDose'),
  Prescription(57, 30, 'MedianDose'),
  Prescription(60, 30, 'MedianDose'),
  Prescription(55.8, 31, 'MedianDose'),
  Prescription(59.4, 33, 'MedianDose'),
  # Stereotactic:
  Prescription(15, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(16, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(17, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(18, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(19, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(20, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(21, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(22, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(23, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(24, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(25, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(21, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(22.5, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(24, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(25.5, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(27, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(28.5, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(30, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(25, 5, 'DoseAtVolume', volume_percent=99),
  Prescription(30, 5, 'DoseAtVolume', volume_percent=99),
  Prescription(35, 5, 'DoseAtVolume', volume_percent=99)
]
als = [
  Prescription(7.5, 1, 'MedianDose')
]
breast = [
  Prescription(16, 8, 'MedianDose'),
  Prescription(26, 5, 'MedianDose'),
  Prescription(40.05, 15, 'MedianDose'),
  Prescription(48, 15, 'MedianDose'), # SIB with 40.05 Gy to the whole breast
  Prescription(50, 25, 'MedianDose')
]
lung = [
  # Conventional:
  Prescription(17, 2, 'MedianDose'),
  Prescription(30, 10, 'MedianDose'),
  Prescription(39, 13, 'MedianDose'),
  Prescription(42, 15, 'MedianDose'),
  Prescription(48, 16, 'MedianDose'),
  Prescription(51, 17, 'MedianDose'),
  Prescription(55, 20, 'MedianDose'),
  Prescription(50, 25, 'MedianDose'),
  Prescription(54, 27, 'MedianDose'),
  Prescription(45, 30, 'MedianDose'), # Bi-daily
  Prescription(60, 30, 'MedianDose'),
  Prescription(66, 33, 'MedianDose'),
  Prescription(70, 35, 'MedianDose'),
  Prescription(60, 40, 'MedianDose'), # Bi-daily
  # Stereotactic:
  Prescription(54, 3, 'DoseAtVolume', volume_percent=98),
  Prescription(55, 5, 'DoseAtVolume', volume_percent=98),
  Prescription(56, 8, 'DoseAtVolume', volume_percent=98),
  Prescription(60, 8, 'DoseAtVolume', volume_percent=98)
]
bladder = [
  Prescription(21, 3, 'MedianDose'),
  Prescription(20, 5, 'MedianDose'),
  Prescription(28, 7, 'MedianDose'),
  Prescription(30, 10, 'MedianDose'),
  Prescription(35, 10, 'MedianDose'),
  Prescription(39, 13, 'MedianDose'),
  Prescription(64, 32, 'MedianDose')
]
prostate = [
  Prescription(36, 6, 'MedianDose'),
  Prescription(39, 13, 'MedianDose'),
  Prescription(55, 20, 'MedianDose'),
  Prescription(60, 20, 'MedianDose'),
  Prescription(67.5, 25, 'MedianDose'),
  Prescription(77, 35, 'MedianDose')
]
prostate_bed = [
  Prescription(70, 35, 'MedianDose')
]
rectum = [
  Prescription(8, 1, 'MedianDose'),
  Prescription(25, 5, 'MedianDose'),
  Prescription(30, 10, 'MedianDose'),
  Prescription(39, 13, 'MedianDose'),
  Prescription(50, 25, 'MedianDose')
]
palliative = [
  # Conventional:
  Prescription(8, 1, 'MedianDose'),
  Prescription(10, 1, 'MedianDose'),
  Prescription(20, 5, 'MedianDose'),
  Prescription(30, 10, 'MedianDose'),
  Prescription(36, 12, 'MedianDose'),
  Prescription(39, 13, 'MedianDose'),
  Prescription(50, 25, 'MedianDose'),
  # Stereotactic:
  Prescription(16, 1, 'DoseAtVolume', volume_percent=99),
  Prescription(27, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(24, 3, 'DoseAtVolume', volume_percent=99),
  Prescription(30, 3, 'DoseAtVolume', volume_percent=99), # Bony-M trial (GTV dose)
  Prescription(37.5, 3, 'DoseAtVolume', volume_percent=99), # Bony-M trial (GTV dose)
  Prescription(30, 5, 'DoseAtVolume', volume_percent=99),
  Prescription(35, 5, 'DoseAtVolume', volume_percent=99)
]


# Creates a Prescription from the given dose and nr of fractions,
# automatically assigning the prescription type based on it.
# This method is used because we don't have a selection of Conformal/Stereotactic
# in our PLAN script (i.e. it has to be inferred).
def create_prescription(total_dose, nr_fractions, region_code, ss):
  # Verify input:
  assert 1 <= total_dose <= 100, "total_dose is not in a valid range (1-100): %r" % total_dose
  assert 1 <= nr_fractions <= 40, "nr_fractions is not in a valid range (1-40): %r" % nr_fractions
  assert -1 <= region_code <= 999, "region_code is not in a valid range (-1-999): %r" % region_code
  # Determine if the given information indicates a stereotactic prescription:
  stereotactic = False
  if region_code in RC.brain_partial_codes:
    if (nr_fractions == 1 and total_dose >= 15) or (nr_fractions == 3 and total_dose >= 21) or (nr_fractions == 5 and total_dose >= 25 and not SSF.has_roi_with_shape(ss, ROIS.ctv.name)):
      stereotactic = True
  elif region_code in RC.lung_and_mediastinum_codes:
    if (nr_fractions == 3 and total_dose >= 45) or (nr_fractions == 5 and total_dose >= 55) or (nr_fractions == 8 and total_dose >= 56):
      stereotactic = True
  elif region_code in RC.bone_codes:
    if (nr_fractions == 1 and total_dose >= 16) or (nr_fractions == 3 and total_dose >= 24) or (nr_fractions == 5 and total_dose >= 30):
      stereotactic = True
  if stereotactic:
    if region_code in RC.lung_and_mediastinum_codes:
      p = Prescription(total_dose, nr_fractions, 'DoseAtVolume', volume_percent=98)
    else:
      p = Prescription(total_dose, nr_fractions, 'DoseAtVolume', volume_percent=99)
  else:
    p = Prescription(total_dose, nr_fractions, 'MedianDose')
  return p


# Validates the prescription which has been selected against the known prescriptions for each treatment region.
# If the prescription is recognized, returns True, and if not returns False.
def validate_prescription(prescription, region_code):
  # Verify input:
  assert type(prescription) is Prescription, "prescription is not a Prescription: %r" % prescription
  assert -1 <= region_code <= 999, "region_code is not in a valid range (-1-999): %r" % region_code
  # The return parameter:
  valid = False
  # Test for each region code category and set valid True if there is a match:
  if region_code in RC.brain_whole_codes:
    if prescription in brain_whole:
      valid = True
  elif region_code in RC.brain_partial_codes:
    if prescription in brain_partial:
      valid = True
  elif region_code in RC.als_codes:
    if prescription in als:
      valid = True
  elif region_code in RC.breast_codes:
    if prescription in breast:
      valid = True
  elif region_code in RC.lung_and_mediastinum_codes:
    if prescription in lung:
      valid = True
  elif region_code in RC.bladder_codes:
    if prescription in bladder:
      valid = True
  elif region_code in RC.prostate_intact_codes:
    if prescription in prostate:
      valid = True
  elif region_code in RC.prostate_bed_codes:
    if prescription in prostate_bed:
      valid = True
  elif region_code in RC.rectum_codes:
    if prescription in rectum:
      valid = True
  elif region_code in RC.palliative_codes:
    if prescription in palliative:
      valid = True
  return valid
