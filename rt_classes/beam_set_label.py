# Handling the Aalesund beam set label format:
class BeamSetLabel(object):
  def __init__(self, label):
    self.valid = True
    self.label = label
    self.technique = None
    self.region = None
    self.nr_fractions = None
    self.process_sections()
    if self.valid:
      self.process_fx()
      self.process_technique()
      self.process_region()
      self.process_middle_part()

  # Label should have 3 sections (separated by colon):
  def process_sections(self):
    self.parts = self.label.split(':')
    if len(self.parts) != 3:
      self.valid = False

  # Last section should be a positive integer:
  def process_fx(self):
    if self.parts[-1].isdigit():
      self.nr_fractions = self.parts[-1]
    else:
      self.valid = False

  # Last character of first section should be a letter:
  def process_technique(self):
    if not self.parts[0][-1].isalpha():
      self.valid = False
    else:
      self.technique = self.parts[0][-1]

  # First characters of first section should be integer(s):
  def process_region(self):
    if not self.parts[0][0:-1].isdigit():
      self.valid = False
    else:
      self.region = int(self.parts[0][0:-1])

  # Middle section should have 2 parts (separated by -):
  def process_middle_part(self):
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