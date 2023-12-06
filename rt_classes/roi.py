# encoding: utf8

# Import local files:
import margins as MARGINS

# ROI class - used for manually defined ROIs.
class ROI(object):

    def __init__(self, name, type, color, case=None, model=None, dlsm=None):
      self.name = name
      self.type = type
      self.color = color
      self.case = case # e.g. 'Thorax'
      # Model based segmentation model:
      self.model = model # e.g. 'SpinalCord (Thorax)'
      # Deep learning segmentation model:
      self.dlsm = dlsm # e.g. 'RSL Thorax-Abdomen CT'
      self.source_level = 999


# ROIExpanded class - used for simple derived ROIs (having only one dependence).
class ROIExpanded(object):

    def __init__(self, name, type, color, source, margins=MARGINS.zero):
      self.name = name
      self.type = type
      self.color = color
      self.source = source
      self.margins = margins
      self.margin_settings = margins.expression()
      self.source_level = 0



# ROIAlgebra class - used for complex derived ROIs (depending on two sets of sources).
class ROIAlgebra(object):

    # operator: 'Union', 'Intersection', 'Subtraction'
    # operatorA: 'Union', 'Intersection'
    # operatorB: 'Union', 'Intersection'
    def __init__(self, name, type, color, sourcesA=[], sourcesB=[], operator='Union', operatorA='Union', operatorB='Union', marginsA=MARGINS.zero, marginsB=MARGINS.zero, result_margins=MARGINS.zero):
      # Verify input:
      assert isinstance(name, str), "name is not a string: %r" % name
      assert isinstance(type, str), "type is not a string: %r" % type
      assert isinstance(color, str), "color is not a string: %r" % color
      assert isinstance(sourcesA, list), "sourcesA is not a list: %r" % sourcesA
      assert isinstance(sourcesB, list), "sourcesB is not a list: %r" % sourcesB
      for sourceA in sourcesA:
        assert sourceA.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "sourceA is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % sourceA
      for sourceB in sourcesB:
        assert sourceB.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "sourceB is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % sourceB
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

    # Gives a dictionary containing all the information needed to express the A side of this object with the ROI algebra function.
    def expressionA(self):
      names = []
      for source in self.sourcesA:
        names.append(source.name)
      return {'Operation': self.operatorA, 'SourceRoiNames': names, 'MarginSettings': self.margin_settingsA()}


    # Gives a dictionary containing all the information needed to express the B side of this object with the ROI algebra function.
    def expressionB(self):
      names = []
      for source in self.sourcesB:
        names.append(source.name)
      return {'Operation': self.operatorB, 'SourceRoiNames': names, 'MarginSettings': self.margin_settingsB()}


    # Gives a dictionary containing all the information needed to express the margins of the A side of this object with the ROI algebra function.
    def margin_settingsA(self):
      return self.marginsA.expression()


    # Gives a dictionary containing all the information needed to express the margins of the B side of this object with the ROI algebra function.
    def margin_settingsB(self):
      return self.marginsB.expression()


    # Gives a dictionary containing all the information needed to express the result margins of this object with the ROI algebra function.
    def result_margin_settings(self):
      return self.result_margins.expression()


# ROIWall class - used for derived ROIs which are walls around a single dependence.
class ROIWall(object):
    def __init__(self, name, type, color, source, outward_dist, inward_dist):
      # Verify input:
      assert isinstance(name, str), "name is not a string: %r" % name
      assert isinstance(type, str), "type is not a string: %r" % type
      assert isinstance(color, str), "color is not a string: %r" % color
      assert source.__class__.__name__ in ['ROI', 'ROIAlgebra', 'ROIExpanded', 'ROIWall'], "source is not a ROI (or ROIAlgebra, ROIExpanded, ROIWall): %r" % source
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
