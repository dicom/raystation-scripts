# Formats a string for output.
def f(str):
  '''Formats a string for output.

  Args:
      str (str, None): A string value (or None).

    Returns:
      str: The given string, or an empty string (if None was given).
  '''
  if str:
    return str
  else:
    return ''


class Test(object):
  '''The Test class contains properties and results for a given test.
  Instances of Test are usually connected to a Parameter instance.

  Note: If the 'expected' parameter is True, an expected/found pair will NOT be printed in the results printout!
  '''

  def __init__(self, text, expected, parent):
    '''Initializes the test.

    Args:
      text (str): The description of the test.
      expected (str, int, float, bool): The expected result of the test.
      parent (Parameter): The parameter which this test belongs to.
    '''
    self.text = text
    self.expected = expected
    self.parent = parent
    if parent:
      parent.add_test(self)
    self.run = False
    self.failed = None
    self.found = None

  def fail(self, found=False):
    '''Registers the value found and sets the test result as failed.

    Args:
      found (str, int, float, bool): The actual result.

    Returns:
      bool: False.
    '''
    self.run = True
    self.failed = True
    self.found = found
    return False

  def level(self):
    '''Gives the level of the test in the parameter hierarchy.

    Returns:
      int: The level of self in the hiearchy (an integer in the range 0 - n).
    '''
    if self.parent:
      return 1 + self.parent.level()
    else:
      return 0

  def prefix(self):
    '''Gives a prefix to be used before the output of a failed test result.

    Returns:
      str: A string containing and indentation of empty spaces.
    '''
    return "  " * self.level()

  def result(self):
    '''Gives the result of the test.

    Note that if the expected value is True, then no meaningful expected/found pair is given.

    Returns:
      str: A description of the test result (prefix, description, excepted value and found value).
    '''
    if self.expected == True:
      # No meaningful expected/found pair to give:
      return self.prefix() + f(self.text) + "\n"
    else:
      # Give expected and found values:
      return self.prefix() + f(self.text) + " [Forventet " + f(str(self.expected)) + " -> Fant " + f(str(self.found)) + "]" + "\n"

  def succeed(self):
    '''Sets the test result as a success.

    Returns:
      bool: True.
    '''
    self.run = True
    self.failed = False
    self.found = self.expected
    return True


class Parameter(object):
  '''The Parameter class describes a RayStation property (e.g. Beam),
  and contains tests and sub-parameters.
  '''

  def __init__(self, type, value, parent):
    '''Initializes the parameter.

    Args:
      type (str): The title/description of the paraneter.
      value (str, int, float, bool): The value (if any) of the parameter.
      parent (Parameter): The parameter which this parameter belongs to.
    '''
    if type is not None:
      self.type = type
    else:
      self.type = ''
    if value is not None:
      self.value = value
    else:
      self.value = ''
    self.parent = parent
    if parent:
      parent.add_parameter(self)
    self.tests = []
    self.parameters = []

  def add_test(self, test):
    '''Adds a test to this parameter.'''
    self.tests.append(test)

  def add_parameter(self, parameter):
    '''Adds a child parameter to this parameter.'''
    self.parameters.append(parameter)

  def failure_summary(self):
    '''Gives a summary of the failures of tests belonging to this parameter.

    Returns:
      str: A description of test failures (if any) belonging to this parameter.
    '''
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
    '''Gives the level of the parameter in the parameter hierarchy.

    Returns:
      int: The level of self in the hiearchy (an integer in the range 0 - n).
    '''
    if self.parent:
      return 1 + self.parent.level()
    else:
      return 0

  def nr_failures(self):
    '''Gives the number of test failures for this parameter.

    Returns:
      int: The number of failures (an integer in the range 0 - n).
    '''
    nr = 0
    for t in self.tests:
      if t.failed:
        nr += 1
    for p in self.parameters:
      nr += p.nr_failures()
    return nr

  def nr_passes(self):
    '''Gives the number of test successes for this parameter.

    Returns:
      int: The number of successes (an integer in the range 0 - n).
    '''
    nr = 0
    for t in self.tests:
      if t.run and not t.failed:
        nr += 1
    for p in self.parameters:
      nr += p.nr_passes()
    return nr

  def nr_tests(self):
    '''Gives the number of tests for this parameter.

    Returns:
      int: The number of tests (an integer in the range 0 - n).
    '''
    nr = len(self.tests)
    for p in self.parameters:
      nr += p.nr_tests()
    return nr

  def nr_skips(self):
    '''Gives the number of skipped tests for this parameter.

    Returns:
      int: The number of skipped tests (an integer in the range 0 - n).
    '''
    nr = 0
    for t in self.tests:
      if not t.run:
        nr += 1
    for p in self.parameters:
      nr += p.nr_skips()
    return nr

  def prefix(self):
    '''Gives a prefix to be used before the output of the parameter description.

    Returns:
      str: A string containing and indentation of empty spaces.
    '''
    return "  " * self.level()
