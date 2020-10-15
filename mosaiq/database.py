# encoding: utf8

# A class for interacting with the Mosaiq database.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

# Used for GUI debugging:
#from tkinter import *
#from tkinter import messagebox

import pymssql

class Database:
  
  # The Mosaiq SQL server address:
  server = open(r'C:\temp\raystation-scripts\mosaiq\database.txt', "r").read()
  # The username to be used for access to the Mosaiq database:
  user = open(r'C:\temp\raystation-scripts\mosaiq\user.txt', "r").read()
  # The password to be used for access to the Mosaiq database:
  password = open(r'C:\temp\raystation-scripts\mosaiq\password.txt', "r").read()
  
  # Returns all rows matching the given query text (or an empty list if no match).
  @staticmethod
  def fetch_all(text):
    conn = pymssql.connect(server=Database.server, user=Database.user, password=Database.password)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(text)
    rows = list()
    for row in cursor:
      rows.append(row)
      #print(str(row))
    conn.close()
    return rows
  
  # Returns a single row matching the given query text (or None if no match).
  @staticmethod
  def fetch_one(text):
    conn = pymssql.connect(server=Database.server, user=Database.user, password=Database.password)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(text)
    row = cursor.fetchone()
    #print(str(row))
    conn.close()
    return row

#root = Tk()
#root.withdraw()
#title = ""
#text = ""
#messagebox.showinfo(title, text)
#root.destroy()