# encoding: utf8


# Choices for usage with RadioButton.
class Property(object):

  def __init__(self, name, value, parent=None, next_category=None, default = False):
      self.children = []
      self.name = name
      self.value = value
      self.next_category=next_category
      self.default = default
      if parent:
        parent.children.append(self)
