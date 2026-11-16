
class BeamSetLabel(object):
  '''Handles the Aalesund beam set label format.'''

  def __init__(self, label):
    '''Initializes the brain optimizer with the relevant treatment planning instances.

    Args:
      label (str): A beam set label, formatted in a specific format (e.g. "343V:0-60:20").
    '''
    # Set some default parameters:
    self.valid = True
    self.label = label
    self.technique = None
    self.region = None
    self.nr_fractions = None
    # Start processing the label:
    self.process_sections()
    if self.valid:
      self.process_fx()
      self.process_technique()
      self.process_region()
      self.process_middle_part()

  def process_sections(self):
    '''Label should have 3 sections (each separated by a colon).'''
    self.parts = self.label.split(':')
    if len(self.parts) != 3:
      self.valid = False

  def process_fx(self):
    '''Last section should be a positive integer.'''
    if self.parts[-1].isdigit():
      self.nr_fractions = self.parts[-1]
    else:
      self.valid = False

  def process_technique(self):
    '''Last character of first section should be a letter.'''
    if not self.parts[0][-1].isalpha():
      self.valid = False
    else:
      self.technique = self.parts[0][-1]

  def process_region(self):
    '''First characters of first section should be integer(s).'''
    if not self.parts[0][0:-1].isdigit():
      self.valid = False
    else:
      self.region = int(self.parts[0][0:-1])

  def process_middle_part(self):
    '''Middle section should have 2 parts (numbers) separated by "-".'''
    self.middle_parts = self.parts[1].split('-')
    if len(self.middle_parts) != 2:
      self.valid = False
    else:
      # Each part of the middle string should be positive integers or floats:
      try:
        self.start_dose_str = self.middle_parts[0]
        self.end_dose_str = self.middle_parts[-1]
        self.dose = float(self.middle_parts[-1]) - float(self.middle_parts[0])
        self.start_dose = float(self.middle_parts[0])
        self.end_dose = float(self.middle_parts[-1])
      except ValueError:
        self.valid = False
