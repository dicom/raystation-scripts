# encoding: utf8

# Import local files:
import margins as MARGINS

# ROI class - used for manually defined ROIs.
class ROI(object):

    def __init__(self, name, type, color, case=None, model=None):
      self.name = name
      self.type = type
      self.color = color
      self.case = case # e.g. 'Thorax'
      self.model = model # e.g. 'SpinalCord (Thorax)'
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
      self.name = name
      self.type = type
      self.color = color
      self.source = source
      self.outward_dist = outward_dist
      self.inward_dist = inward_dist
      self.source_level = 0
