'''Contains classes for handling margins (Expansion and Contraction).'''


class Expansion(object):
  '''Handles setup for a derived ROI which is an expansion of an original ROI.'''

  def __init__(self, superior, inferior, anterior, posterior, right, left):
    '''Initializes the expansion with the relevant margins.

    Args:
      superior (float): Margin in the superior direction in cm (e.g. 0.5).
      inferior (float): Margin in the inferior direction in cm (e.g. 0.5).
      anterior (float): Margin in the anterior direction in cm (e.g. 0.5).
      posterior (float): Margin in the posterior direction in cm (e.g. 0.5).
      right (float): Margin in the right direction in cm (e.g. 0.5).
      left (float): Margin in the left direction in cm (e.g. 0.5).
    '''
    self.superior = superior
    self.inferior = inferior
    self.anterior = anterior
    self.posterior = posterior
    self.right = right
    self.left = left

  def expression(self):
    '''Gives a dictionary containing all the information needed to express this object with the ROI algebra function.

    Returns:
      dict: A Dictionary containing the settings for this ROI Algebra expansion.
    '''
    return {'Type':"Expand", 'Superior':self.superior, 'Inferior':self.inferior,'Anterior':self.anterior,'Posterior':self.posterior,'Right':self.right,'Left':self.left}


class Contraction(object):
  '''Handles setup for a derived ROI which is a contraction of an original ROI.'''

  def __init__(self, superior, inferior, anterior, posterior, right, left):
    '''Initializes the contraction with the relevant margins.

    Args:
      superior (float): Margin in the superior direction in cm (e.g. 0.5).
      inferior (float): Margin in the inferior direction in cm (e.g. 0.5).
      anterior (float): Margin in the anterior direction in cm (e.g. 0.5).
      posterior (float): Margin in the posterior direction in cm (e.g. 0.5).
      right (float): Margin in the right direction in cm (e.g. 0.5).
      left (float): Margin in the left direction in cm (e.g. 0.5).
    '''
    self.superior = superior
    self.inferior = inferior
    self.anterior = anterior
    self.posterior = posterior
    self.right = right
    self.left = left

  def expression(self):
    '''Gives a dictionary containing all the information needed to express this object with the ROI algebra function.

    Returns:
      dict: A Dictionary containing the settings for this ROI Algebra contraction.
    '''
    return {'Type':"Contract", 'Superior':self.superior, 'Inferior':self.inferior,'Anterior':self.anterior,'Posterior':self.posterior,'Right':self.right,'Left':self.left}
