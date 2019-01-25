# encoding: utf8

# GUI framework (for debugging):
#from connect import *
#import sys
#clr.AddReference("PresentationFramework")
#from System.Windows import *
#MessageBox.Show(value, 'DEBUG', MessageBoxButton.OK, MessageBoxImage.Information)

# Formats a string for output.
def f(str):
  if str:
    #return str.decode('utf8', 'replace')
    return str.decode('iso-8859-1', 'replace')
  else:
    return ''

# The Test class contains properties and results for a given test.
# Instances of Test are usually connected to a Parameter instance.
#
# Note: If the 'expected' parameter is True, an expected/found pair will NOT be printed in the results printout!
class Test(object):
  def __init__(self, text, expected, parent):
    self.text = text
    self.expected = expected
    self.parent = parent
    if parent:
      parent.add_test(self)
    self.run = False
    self.failed = None
    self.found = None

  def fail(self, found=False):
    self.run = True
    self.failed = True
    self.found = found
    return False

  def level(self):
    if self.parent:
      return 1 + self.parent.level()
    else:
      return 0

  def prefix(self):
    return "  " * self.level()

  def result(self):
    if self.expected == True:
      # No meaningful expected/found pair to give:
      return self.prefix() + f(self.text) + "\n"
    else:
      # Give expected and found values:
      return self.prefix() + f(self.text) + " [Forventet " + f(str(self.expected)) + " -> Fant " + f(str(self.found)) + "]" + "\n"

  def succeed(self):
    self.run = True
    self.failed = False
    self.found = self.expected
    return True

# The Parameter class describes a RayStation property (e.g. Beam),
# and contains tests and sub-parameters.
class Parameter(object):
  def __init__(self, type, value, parent):
    if type:
      self.type = type
    else:
      self.type = ''
    if value:
      self.value = value
    else:
      self.value = ''
    self.parent = parent
    if parent:
      parent.add_parameter(self)
    self.tests = []
    self.parameters = []

  def add_test(self, test):
    self.tests.append(test)

  def add_parameter(self, parameter):
    self.parameters.append(parameter)

  def failure_summary(self):
    summary = ""
    if self.nr_failures() > 0:
      summary += self.prefix() + self.type + ": " + str(self.value) + "\n"
      for t in self.tests:
        if t.failed:
          summary += t.result()
      for p in self.parameters:
        summary += p.failure_summary()
    return summary

  def level(self):
    if self.parent:
      return 1 + self.parent.level()
    else:
      return 0

  def nr_failures(self):
    nr = 0
    for t in self.tests:
      if t.failed:
        nr += 1
    for p in self.parameters:
      nr += p.nr_failures()
    return nr

  def nr_passes(self):
    nr = 0
    for t in self.tests:
      if t.run and not t.failed:
        nr += 1
    for p in self.parameters:
      nr += p.nr_passes()
    return nr

  def nr_tests(self):
    nr = len(self.tests)
    for p in self.parameters:
      nr += p.nr_tests()
    return nr

  def nr_skips(self):
    nr = 0
    for t in self.tests:
      if not t.run:
        nr += 1
    for p in self.parameters:
      nr += p.nr_skips()
    return nr

  def prefix(self):
    return "  " * self.level()