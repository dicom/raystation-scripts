# encoding: utf8

from __future__ import division
import math


# Tolerance class.
# Contains information about organ at risk tolerance doses and computes equivalent
# tolerance doses for different fractionations.
class Tolerance(object):

    def __init__(self, organ, endpoint, alphabeta, nr_fractions, dose, criteria, comment):
      self.organ = organ
      self.endpoint = endpoint
      self.alphabeta = alphabeta
      self.nr_fractions = nr_fractions
      self.dose = dose
      self.criteria = criteria
      self.comment = comment


    # Calculates the EQD2 equivalent dose
    # Returned value is rounded to 1 decimal.
    def equivalent(self, alternative_nr_fractions):
      if alternative_nr_fractions == self.nr_fractions:
        return self.dose
      else:
        d = self.dose/self.nr_fractions
        par = 4*((self.nr_fractions*(d**2)+(self.nr_fractions*d*self.alphabeta))/alternative_nr_fractions)
        return round(alternative_nr_fractions*(((-self.alphabeta) + math.sqrt(self.alphabeta**2+ par ))/2), 1)
