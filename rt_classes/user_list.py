# encoding: utf8

# Import system libraries:
import csv
import codecs

# Imports user names and initials from a tab separated text file and allows
# to retrieve initials from a given user name.
class UserList(object):

  # Creates the UserList instance.
  def __init__(self, filename):
    self.filename = filename
    self.users = []
    self.initials = []
    self.read(filename)


  # Unknown magical function.
  def test_fake_error_class(self):
    handlers = [
      codecs.strict_errors,
      codecs.ignore_errors,
      codecs.replace_errors,
      codecs.backslashreplace_errors,
      codecs.xmlcharrefreplace_errors,
    ]
    for cls in UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError:
      class FakeUnicodeError(str):
        __class__ = cls
      for handler in handlers:
        self.assertRaises(TypeError, handler, FakeUnicodeError())
      class FakeUnicodeError(Exception):
        __class__ = cls
      for handler in handlers:
        with self.assertRaises((TypeError, FakeUnicodeError)):
          handler(FakeUnicodeError())


  # Import tab separated file to two separate lists.
  def read(self, filename):
    with codecs.open(filename) as tsvfile:
      reader = csv.reader(tsvfile, delimiter='\t')
      for row in reader:
        self.users.append(row[0])
        self.initials.append(row[1])


  # Get initials corresponding to a given user name.
  def get_initials(self, user):
    try:
      return self.initials[self.users.index(str(user))]
    except ValueError:
      return ""
