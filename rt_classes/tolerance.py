# Import system libraries:
from __future__ import division
import math


class Tolerance(object):
  '''Contains information about organ at risk tolerance doses
  and computes equivalent tolerance doses for alternative fractionations.
  '''

  def __init__(self, organ, endpoint, alphabeta, nr_fractions, dose, criteria, comment):
    '''Initializes the Tolerance instance with the relevant parameters.

    Args:
      organ (str): The name of the organ (e.g. 'Parotid').
      endpoint (str]): A description of the end point (e.g. 'Xerostomia').
      alphabeta (int, float): The alpha/beta ratio of the tissue (e.g. 3).
      nr_fractions (int, float]): The number of fractions for the given tolerance.
      dose (int, float): The dose limit.
      criteria (str): A description of the dose volume type of the tolerance.
      comment (str): A description of scope for the tolerance (e.g. conventional RT or SBRT).
    '''
    self.organ = organ
    self.endpoint = endpoint
    self.alphabeta = alphabeta
    self.nr_fractions = nr_fractions
    self.dose = dose
    self.criteria = criteria
    self.comment = comment

  def equivalent(self, alternative_nr_fractions):
    '''Calculates the EQD2 equivalent dose.

    Args:
      alternative_nr_fractions (int): A number of fractions for which to calculate an equivalent dose.

    Returns:
      float: An equivalent dose calculated for the alternative number of fractions.
        The returned value is rounded to 1 decimal.
    '''
    if alternative_nr_fractions == self.nr_fractions:
      return self.dose
    else:
      d = self.dose/self.nr_fractions
      par = 4*((self.nr_fractions*(d**2)+(self.nr_fractions*d*self.alphabeta))/alternative_nr_fractions)
      return round(alternative_nr_fractions*(((-self.alphabeta) + math.sqrt(self.alphabeta**2+ par ))/2), 1)
