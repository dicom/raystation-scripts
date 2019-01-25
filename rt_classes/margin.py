# encoding: utf8


# Class for setting up margins for a ROI expansion.
class Expansion(object):

  def __init__(self, superior, inferior, anterior, posterior, right, left):
    self.superior = superior
    self.inferior = inferior
    self.anterior = anterior
    self.posterior = posterior
    self.right = right
    self.left = left


  # Gives a dictionary containing all the information needed to express this object with the ROI algebra function.
  def expression(self):
    return {'Type':"Expand", 'Superior':self.superior, 'Inferior':self.inferior,'Anterior':self.anterior,'Posterior':self.posterior,'Right':self.right,'Left':self.left}


# Class for setting up margins for a ROI contraction.
class Contraction(object):

  def __init__(self, superior, inferior, anterior, posterior, right, left):
    self.superior = superior
    self.inferior = inferior
    self.anterior = anterior
    self.posterior = posterior
    self.right = right
    self.left = left


  # Gives a dictionary containing all the information needed to express this object with the ROI algebra function.
  def expression(self):
    return {'Type':"Contract", 'Superior':self.superior, 'Inferior':self.inferior,'Anterior':self.anterior,'Posterior':self.posterior,'Right':self.right,'Left':self.left}
