# Import system libraries:
import csv
import codecs


class UserList(object):
  '''Handles import of user names and initials from a tab separated text file
  and allows to query initials for a given user name.
  '''

  def __init__(self, filename):
    '''Initializes the UserList instance with the relevant parameters.

    Args:
      filename (str): The path & filename of a users file to be loaded.
    '''
    self.filename = filename
    self.users = []
    self.initials = []
    self.groups = []
    self.read(filename)

  def read(self, filename):
    '''Reads attributes from a a tab separated file containing user information
    (user name, initials and occupational group).

    Args:
      filename (str): The path & filename of a users file to be loaded.
    '''
    with codecs.open(filename) as tsvfile:
      reader = csv.reader(tsvfile, delimiter='\t')
      for row in reader:
        self.users.append(row[0])
        self.initials.append(row[1])
        self.groups.append(row[2])

  def get_group(self, user):
    '''Gives the occupational group for a given user name.

    Args:
      user (str): A user name.

    Returns:
      str: The occupational group for the given user (or an empty string if there is no match).
    '''
    try:
      return self.groups[self.users.index(str(user))]
    except ValueError:
      return ""

  def get_initials(self, user):
    '''Gives the initials  corresponding to a given user name.

    Args:
      user (str): A user name.

    Returns:
      str: The initials for the given user (or an empty string if there is no match).
    '''
    try:
      return self.initials[self.users.index(str(user))]
    except ValueError:
      return ""
