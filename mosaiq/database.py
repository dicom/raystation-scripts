# Import system libraries:
import pymssql

class Database:
  """A class for interacting with the Mosaiq database."""

  # The Mosaiq SQL server address:
  server = open(r'C:\temp\raystation-scripts\mosaiq\server.txt', "r").read()
  # The username to be used for access to the Mosaiq database:
  user = open(r'C:\temp\raystation-scripts\mosaiq\user.txt', "r").read()
  # The password to be used for access to the Mosaiq database:
  password = open(r'C:\temp\raystation-scripts\mosaiq\password.txt', "r").read()
  # The name of the database to access:
  database = open(r'C:\temp\raystation-scripts\mosaiq\database.txt', "r").read()

  @staticmethod
  def fetch_all(text):
    """Gives all rows matching the given query text (or an empty list if no match).

    Args:
      text (str): A database query (SQL statement).

    Returns:
      List[dict]: A list of database rows.
    """
    conn = pymssql.connect(server=Database.server, user=Database.user, password=Database.password, database=Database.database)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(text)
    rows = list()
    for row in cursor:
      rows.append(row)
    conn.close()
    return rows

  @staticmethod
  def fetch_one(text):
    """Gives one row matching the given query text (or None if no match).

    Args:
      text (str): A database query (SQL statement).

    Returns:
      dict: A dict containing information from the matched row (or None if no match).
    """
    conn = pymssql.connect(server=Database.server, user=Database.user, password=Database.password, database=Database.database)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(text)
    row = cursor.fetchone()
    conn.close()
    return row
