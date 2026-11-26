'''Contains classes for handling ROI objects.'''

# Import local files:
import margins as MARGINS


class ROI(object):
  '''Handles setup of a manually segmented or model based ROIs.'''

  def __init__(self, name, type, color, case=None, model=None):
    '''Initializes the ROI instance with the relevant parameters.

    Args:
      name (str): Name of the ROI (e.g. 'Rectum').
      type (str): Type of the ROI (e.g. 'Organ').
      color (str): Color of the ROI (e.g. 'Brown').
      case (PyScriptObject): Case in which to create ROI.
      model (str): The RayStation MBS model name.
    '''
    self.name = name
    self.type = type
    self.color = color
    self.case = case # e.g. 'Thorax'
    self.source_level = 999
    # Model based segmentation model:
    self.model = model # e.g. 'SpinalCord (Thorax)'


class ROIDLS(object):
  '''Handles setup of deep learning segmentation ROIs.'''

  def __init__(self, name, type, color, model, lib_name=None):
    '''Initializes the ROIDLS instance with the relevant parameters.

    Args:
      name (str): Name of the ROI (e.g. 'Prostate').
      type (str): Type of the ROI (e.g. 'Organ').
      color (str): Color of the ROI (e.g. 'Pink').
      model (str): The RayStation DLS model name (e.g. 'RSL Thorax-Abdomen CT').
      lib_name (str): The name used for the ROI in the RayStation script library (e.g. 'Prostate_minus_VenousPlexus').
        In most cases lib_name equals name, but in some cases they differ. Defaults to None.
    '''
    self.name = name
    self.type = type
    self.color = color
    self.source_level = 999
    # Deep learning segmentation model:
    self.model = model
    # The lib_name parameter equals name unless it has been specified:
    if lib_name:
      self.lib_name = lib_name
    else:
      # Default to name if not specified:
      self.lib_name = name


class ROIExpanded(object):
  '''Handles setup of expanded ROIs (simple derived ROIs having only one set of sources).'''

  def __init__(self, name, type, color, source, margins=MARGINS.zero):
    '''Initializes the ROIExpanded instance with the relevant parameters.

    Args:
      name (str): Name of the ROI (e.g. 'PTV').
      type (str): Type of the ROI (e.g. 'Ptv').
      color (str): Color of the ROI (e.g. 'Blue').
      source (ROI, ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): The ROI instance which is the source for the expansion.
      margins (Expansion, Contraction): An Expansion or a Contraction instance to be used for margin setup.
    '''
    self.name = name
    self.type = type
    self.color = color
    self.source = source
    self.margins = margins
    self.margin_settings = margins.expression()
    self.source_level = 0


class ROIAlgebra(object):
  '''Handles setup of algebra ROIs (complex derived ROIs depending on two sets of sources).'''

  # operator: 'Union', 'Intersection', 'Subtraction'
  # operatorA: 'Union', 'Intersection'
  # operatorB: 'Union', 'Intersection'
  def __init__(self, name, type, color, sourcesA=[], sourcesB=[], operator='Union', operatorA='Union', operatorB='Union', marginsA=MARGINS.zero, marginsB=MARGINS.zero, result_margins=MARGINS.zero):
    '''Initializes the ROIExpanded instance with the relevant parameters.

    Args:
      name (str): Name of the ROI (e.g. 'PTV1').
      type (str): Type of the ROI (e.g. 'Ptv').
      color (str): Color of the ROI (e.g. 'Blue').
      sourcesA (list[ROI, ROIDLS, ROIAlgebra, ROIExpanded, ROIWall]): A list of ROI instances making up source A.
        Defaults to an empty list.
      sourcesB (list[ROI, ROIDLS, ROIAlgebra, ROIExpanded, ROIWall]): A list of ROI instances making up source B.
        Defaults to an empty list.
      operator (str): The operator to be used for the overall expression ('Union', 'Intersection' or 'Subtraction').
        Defaults to 'Union'.
      operatorA (str): The operator to be used on set A ('Union' or 'Intersection').
        Defaults to 'Union'.
      operatorB (str): The operator to be used on set B ('Union' or 'Intersection').
        Defaults to 'Union'.
      marginsA (Expansion, Contraction): An Expansion or a Contraction instance to be used for source A margins.
        Defaults to zero margins.
      marginsB (Expansion, Contraction): An Expansion or a Contraction instance to be used for source B margins.
        Defaults to zero margins.
      result_margins (Expansion, Contraction): An Expansion or a Contraction instance to be used for the result margins.
        Defaults to zero margins.
    '''
    # Verify input:
    assert isinstance(name, str), "name is not a string: %r" % name
    assert isinstance(type, str), "type is not a string: %r" % type
    assert isinstance(color, str), "color is not a string: %r" % color
    assert isinstance(sourcesA, list), "sourcesA is not a list: %r" % sourcesA
    assert isinstance(sourcesB, list), "sourcesB is not a list: %r" % sourcesB
    for sourceA in sourcesA:
      assert sourceA.__class__.__name__ in ['ROI', 'ROIDLS', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "sourceA is not a ROI (or ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): %r" % sourceA
    for sourceB in sourcesB:
      assert sourceB.__class__.__name__ in ['ROI', 'ROIDLS', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "sourceB is not a ROI (or ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): %r" % sourceB
    assert operator in ['Union', 'Intersection', 'Subtraction'], "operator is not a valid value (Union, Intersection, Subtraction): %r" % operator
    assert operatorA in ['Union', 'Intersection'], "operatorA is not a valid value (Union, Intersection): %r" % operatorA
    assert operatorB in ['Union', 'Intersection'], "operatorB is not a valid value (Union, Intersection): %r" % operatorB
    assert marginsA.__class__.__name__ in ['Expansion', 'Contraction'], "marginsA is not a valid margin class (Expansion or Contraction): %r" % marginsA
    assert marginsB.__class__.__name__ in ['Expansion', 'Contraction'], "marginsB is not a valid margin class (Expansion or Contraction): %r" % marginsB
    assert result_margins.__class__.__name__ in ['Expansion', 'Contraction'], "result_margins is not a valid margin class (Expansion or Contraction): %r" % result_margins
    # Assign parameters:
    self.name = name
    self.type = type
    self.color = color
    self.sourcesA = sourcesA
    self.sourcesB = sourcesB
    self.operator = operator
    self.operatorA = operatorA
    self.operatorB = operatorB
    self.marginsA = marginsA
    self.marginsB = marginsB
    self.result_margins = result_margins
    self.source_level = 0

  def expressionA(self):
    '''Gives a dictionary containing all the information needed to express source A of the ROI algebra.

    Returns:
      dict: A Dictionary containing the settings for source A.
    '''
    names = []
    for source in self.sourcesA:
      names.append(source.name)
    return {'Operation': self.operatorA, 'SourceRoiNames': names, 'MarginSettings': self.margin_settingsA()}

  def expressionB(self):
    '''Gives a dictionary containing all the information needed to express source B of the ROI algebra.

    Returns:
      dict: A Dictionary containing the settings for source B.
    '''
    names = []
    for source in self.sourcesB:
      names.append(source.name)
    return {'Operation': self.operatorB, 'SourceRoiNames': names, 'MarginSettings': self.margin_settingsB()}

  def margin_settingsA(self):
    '''Gives a dictionary containing all the information needed to express the margins for source A of the ROI algebra.

    Returns:
      dict: A Dictionary containing the margin settings for source A.
    '''
    return self.marginsA.expression()

  def margin_settingsB(self):
    '''Gives a dictionary containing all the information needed to express the margins for source B of the ROI algebra.

    Returns:
      dict: A Dictionary containing the margin settings for source B.
    '''
    return self.marginsB.expression()

  # Gives a dictionary containing all the information needed to express the result margins of this object with the ROI algebra function.
  def result_margin_settings(self):
    '''Gives a dictionary containing all the information needed to express the margins
    for the result of the ROI algebra.

    Returns:
      dict: A Dictionary containing the margin settings for the result.
    '''
    return self.result_margins.expression()


class ROIWall(object):
  '''Handles setup of wall ROIs.'''

  def __init__(self, name, type, color, source, outward_dist, inward_dist):
    '''Initializes the ROIWall instance with the relevant parameters.

    Args:
      name (str): Name of the ROI (e.g. 'PTV_Wall').
      type (str): Type of the ROI (e.g. 'Undefined').
      color (str): Color of the ROI (e.g. 'Gray').
      source (ROI, ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): The ROI instance which is the source for the wall.
      outward_dist (float, int): The distance outwards, in cm (e.g. '1.0').
      inward_dist (float, int): The distance inwards, in cm (e.g. '0.5').
    '''
    # Verify input:
    assert isinstance(name, str), "name is not a string: %r" % name
    assert isinstance(type, str), "type is not a string: %r" % type
    assert isinstance(color, str), "color is not a string: %r" % color
    assert source.__class__.__name__ in ['ROI', 'ROIDLS', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "source is not a ROI (or ROIDLS, ROIAlgebra, ROIExpanded, ROIWall): %r" % source
    assert isinstance(outward_dist, (float, int)), "outward_dist is not a float or integer: %r" % outward_dist
    assert isinstance(inward_dist, (float, int)), "inward_dist is not a float or integer: %r" % inward_dist
    # Assign parameters:
    self.name = name
    self.type = type
    self.color = color
    self.source = source
    self.outward_dist = outward_dist
    self.inward_dist = inward_dist
    self.source_level = 0
