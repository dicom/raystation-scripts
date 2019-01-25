# encoding: utf8


# Site class for ROI definition.
class RadioButton(object):

  def __init__(self, text, label, elements, default=None, parent=None):
      self.text = text
      self.label = label
      self.elements = elements
      self.default = default
      self.children = []
      if parent:
        parent.children.append(self)
