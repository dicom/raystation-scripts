# encoding: utf8


# Import local files:
import structure_set_functions as SSF


# A class which tries to determine a prescription from a given structure set.
class PrescriptionInterpreter(object):

  def __init__(self, ss):
    self.ss = ss
    self.region_code = ''
    self.fraction_dose = ''
    self.nr_fractions = ''
    if SSF.has_roi(ss, 'Breast_L'):
      self.interpret_breast(ss)
    elif SSF.has_roi(ss, 'Prostate'):
      self.interpret_prostate(ss)
    elif SSF.has_roi(ss, 'CTVsb') and SSF.has_roi(ss, 'CTV_70'):
      self.interpret_prostate_bed(ss)
    elif SSF.has_roi(ss, 'GTVp') and SSF.has_roi(ss, 'Bladder') and not SSF.has_roi(ss, 'Rectum'):
      self.interpret_rectum(ss)
    elif SSF.has_roi(ss, 'GTVp') and self.is_expansion_of('CTVe', 'Bladder'):
      self.interpret_bladder(ss)

  
  # Tries to determine prescription values for a structure set which indicates that we have a bladder case.
  def interpret_bladder(self, ss):
    # For now we just have one default prescription for bladder:    
    self.region_code = 341
    self.fraction_dose = 2
    self.nr_fractions = 32
  
  
  # Tries to determine prescription values for a structure set which indicates that we have a breast case.
  def interpret_breast(self, ss):
    sib = False
    # Determine category of breast treatment:
    if SSF.has_roi(ss, 'CTVp_L') or SSF.has_roi(ss, 'CTVp_R'):
      # Bilateral locoregional:
      self.region_code = 276
    elif SSF.has_roi(ss, 'CTV_L') and SSF.has_roi(ss, 'CTV_R'):
      # Bilateral whole breast:
      self.region_code = 275
    elif SSF.has_roi(ss, 'CTVp'):
      # Locoregional:
      if self.has_roi_in_expression_a('CTVp', 'Breast_L_Draft'):
        if SSF.has_roi(ss, 'BreastString_L'):
          # (Presence of breast string is an indicator of cheastwall)
          self.region_code = 241
        else:
          self.region_code = 243
      elif self.has_roi_in_expression_a('CTVp', 'Breast_R_Draft'):
        if SSF.has_roi(ss, 'BreastString_R'):
          # (Presence of breast string is an indicator of cheastwall)
          self.region_code = 242
        else:
          self.region_code = 244
      # SIB?
      if SSF.has_roi(ss, 'CTVsb'):
        sib = True
    elif SSF.has_roi(ss, 'CTVsb') and not SSF.has_roi(ss, 'CTV'):
      # Partial breast:
      if self.has_roi_in_expression_a('CTVsb', 'SurgicalBed_L'):
        self.region_code = 273
      elif self.has_roi_in_expression_a('CTVsb', 'SurgicalBed_R'):
        self.region_code = 274
    elif SSF.has_roi(ss, 'CTV'):
      # Whole breast:
      if self.has_roi_in_expression_a('CTV', 'Breast_L_Draft'):
        self.region_code = 239
      elif self.has_roi_in_expression_a('CTV', 'Breast_R_Draft'):
        self.region_code = 240
      # SIB?
      if SSF.has_roi(ss, 'CTVsb'):
        sib = True
    # Since all breast default prescriptions have the same nr of fractions, we can deduce
    # that if region code has been determined, the nr of fractions should be set also.
    # As for dose, it depends on whether we have a SIB or not:
    if self.region_code != '':
      self.nr_fractions = 15
      if sib:
        self.fraction_dose = 3.2
      else:
        self.fraction_dose = 2.67


  # Tries to determine prescription values for a structure set which indicates that we have a prostate case.
  def interpret_prostate(self, ss):
    # Determine category of prostate treatment:
    if SSF.has_roi(ss, 'CTV_60'):
      # Prostate and vesicles:
      self.region_code = 343
      self.fraction_dose = 3
      self.nr_fractions = 20
    elif SSF.has_roi(ss, 'CTV_67.5'):
      if SSF.has_roi(ss, 'CTV!_50'):
        # Prostate and lymph nodes:
        self.region_code = 355
        self.fraction_dose = 2.7
        self.nr_fractions = 25
      else:
        # Prostate and vesicles:
        self.region_code = 343
        self.fraction_dose = 2.7
        self.nr_fractions = 25
    elif SSF.has_roi(ss, 'CTV'):
      # Presumably prostate STAMPEDE:
      self.region_code = 342
      self.fraction_dose = 2.7
      self.nr_fractions = 20
  
  
  # Tries to determine prescription values for a structure set which indicates that we have a prostate bed case.
  def interpret_prostate_bed(self, ss):
    # Determine category of prostate bed treatment:
    if SSF.has_roi(ss, 'CTV!_56'):
      # Prostate bed and lymph nodes:
      self.region_code = 356
      self.fraction_dose = 2
      self.nr_fractions = 35
    else:
      # Prostate bed only:
      self.region_code = 348
      self.fraction_dose = 2
      self.nr_fractions = 35
  
  
  # Tries to determine prescription values for a structure set which indicates that we have a rectum case.
  def interpret_rectum(self, ss):
    # Determine category of rectum treatment:
    if SSF.has_roi(ss, 'CTV_50'):
      # Conventional fx:
      self.region_code = 340
      self.fraction_dose = 2
      self.nr_fractions = 25
    else:
      # Short course RT:
      self.region_code = 340
      self.fraction_dose = 5
      self.nr_fractions = 5
  
  
  # Checks if a derived ROI has a given child ROI in its Expression A.
  def has_roi_in_expression_a(self, parent_name, child_name):
    match = False
    parent_rg = self.ss.RoiGeometries[parent_name]
    if parent_rg and parent_rg.PrimaryShape.DerivedRoiStatus:
      expression_a = parent_rg.OfRoi.DerivedRoiExpression.Children[0].Children[0]
      if expression_a:
        match = self.has_roi_in_expression(expression_a, child_name)
    return match


  # Checks if a derived ROI has a given child ROI in its Expression B.
  def has_roi_in_expression_b(self, parent_name, child_name):
    match = False
    parent_rg = self.ss.RoiGeometries[parent_name]
    if parent_rg and parent_rg.PrimaryShape.DerivedRoiStatus:
      expression_b = parent_rg.OfRoi.DerivedRoiExpression.Children[0].Children[1]
      if expression_b:
        match = self.has_roi_in_expression(expression_b, child_name)
    return match


  # Checks if a given child ROI exists in the given expression.
  def has_roi_in_expression(self, expression, child_name):
    match = False
    for child in expression.Children[0].Children:
      if child.RegionOfInterest.Name == child_name:
        match = True
        break
    return match
  
  
  # Checks if the given parent roi is an expanded/contracted ROI of the given child roi.
  def is_expansion_of(self, parent_name, child_name):
    match = False
    parent_rg = self.ss.RoiGeometries[parent_name]
    if parent_rg:
      if len(parent_rg.OfRoi.DerivedRoiExpression.Children[0].Children) == 0:
        if parent_rg.OfRoi.DerivedRoiExpression.Children[0].RegionOfInterest.Name == child_name:
          match = True
    return match
