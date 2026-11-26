# Import system libraries:
import csv
import codecs


class RegionList(object):
  '''Imports region codes and their titles/descriptions from a tab separated text file
  and facilitates query of region text for a given region code.
  '''

  def __init__(self, filename):
    '''Initializes the RegionList class with a given file name.

    Args:
      filename (str): The path & filename of a region code file to be loaded.
    '''
    self.filename = filename
    self.codes = []
    self.labels = []
    self.read(filename)

  def read(self, filename):
    '''Read and import a tab separated file containing region codes and labels.

    Args:
      filename (str): The path & filename of a region code file to be loaded.
    '''
    with codecs.open(filename) as tsvfile:
      reader = csv.reader(tsvfile, delimiter='\t')
      for row in reader:
        self.codes.append(row[0])
        self.labels.append(row[4])

  def get_text(self, code):
    '''Get a text label corresponding to a given region code.

    Args:
      code (int, str): A region code (e.g. 343).
    '''
    try:
      return self.labels[self.codes.index(str(code))]
    except ValueError:
      return None
