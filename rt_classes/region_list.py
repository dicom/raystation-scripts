# encoding: utf8

# Import system libraries:
import csv
import codecs

# Imports region codes and descriptions from a tab separated text file and allows
# to retrieve a region text from a given region code.
class RegionList(object):

    def __init__(self, filename):
      self.filename = filename
      self.codes = []
      self.labels = []
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
          self.codes.append(row[0])
          self.labels.append(row[4])


    # Get a text corresponding to a given region code.
    def get_text(self, code):
      try:
        return self.labels[self.codes.index(str(code))]
      except ValueError:
        return None
