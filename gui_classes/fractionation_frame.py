# Class that creates a text box GUI to get information on region code, fraction dose, number of fractions and initials
#
# Authors:
# Marit Funderud / Christoffer Lervåg
# Helse Møre og Romsdal HF


# Import system libraries:
from tkinter import *
from tkinter import messagebox
import os

# Import local files:
import user_list as USERS

# The FractionationFrame contains 4 text fields: Region code, fraction dose, number of fractions, and initials.
class FractionationFrame(Frame):

  # Creates the instance.
  def __init__(self, the_window):
    Frame.__init__(self, the_window,bg = 'white')
    self.ok = False
    self.create_widgets()
    h = 270
    w = 350
    x = 1100
    y = 500
    the_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    the_window.title("Fraksjonering")
    the_window.configure(bg = 'white')


  # Quits if the cancel button is clicked.
  def cancel_clicked(self, event=None):
    self.quit()


  # Set up the GUI elements.
  def create_widgets(self):
    w = 13
    wl = 127
    # Empty label (just to make the window look nice):
    self.l = Label(self, text = "", width = 40, anchor = W,bg = 'white')
    # Set up labels:
    # Region code:
    self.region_code = StringVar(None)
    self.region_code_label = Label(self, text = "Regionkode:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W, bg = 'white')
    self.region_code_entry = Entry(self, textvariable = self.region_code, width = w, bg = 'white', font = ("TkDefaultFont",10))
    # Fraction dose:
    self.fraction_dose = StringVar(None)
    self.fraction_dose_label = Label(self, text = "Fraksjondose [Gy]:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W,bg = 'white')
    self.fraction_dose_entry = Entry(self, textvariable = self.fraction_dose, width = w, bg = 'white', font = ("TkDefaultFont",10))
    # Number of fractions:
    self.number_of_fractions = StringVar(None)
    self.number_of_fractions_label = Label(self, text = "Antall fraksjoner:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W, bg = 'white')
    self.number_of_fractions_entry = Entry(self, textvariable = self.number_of_fractions, width = w, bg = 'white', font = ("TkDefaultFont",10))
    # Initials:
    self.initials = StringVar()
    self.initials_label = Label(self, text = "Doseplanleggers initialer:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W, justify = LEFT, bg = 'white')
    self.initials_entry = Entry(self, textvariable = self.initials, width = w, bg = 'white', font = ("TkDefaultFont",10))
    # Fill out initials from windows user name:
    self.initials_entry.insert(0, self.user_initials()) 
    # Create OK and Cancel buttons:
    self.okButton = Button(self, text = "OK", command = self.ok_clicked, font = ("TkDefaultFont",10), bg = 'white')
    self.quitButton = Button(self, text = "Cancel", command = self.cancel_clicked, font = ("TkDefaultFont",10), bg = 'white')
    # Place the labels and entries:
    self.l.grid(row = 0, column = 0, padx = 15, columnspan = 2)
    self.region_code_label.grid(row = 1, column = 0, padx = 15, pady = 10)
    self.region_code_entry.grid(row = 1, column = 1, padx = 15, pady = 10)
    self.fraction_dose_label.grid(row = 2, column = 0, padx = 15, pady = 10)
    self.fraction_dose_entry.grid(row = 2, column = 1, padx = 15, pady = 10)
    self.number_of_fractions_label.grid(row = 3, column = 0, padx = 15, pady = 10)
    self.number_of_fractions_entry.grid(row = 3, column = 1, padx = 15, pady = 10)
    self.initials_label.grid(row = 4, column = 0, padx = 15, pady = 10)
    self.initials_entry.grid(row = 4, column = 1, padx = 15, pady = 10)
    # Place OK and Cancel buttons:
    self.okButton.grid(row = 5, column = 0, padx = 20, pady = 15, ipadx = 10, sticky = E)
    self.quitButton.grid(row = 5, column = 1, padx = 20, pady = 15, sticky = W)
    # Sets focus to this text box:
    self.region_code_entry.focus()


  # This function the results from the user input (returned in 4 separate parameters).
  def get_results(self):
    # Collect region code:
    if 0 < int(self.region_code_entry.get()) < 595:
      region_code = int(self.region_code_entry.get())
    else:
      messagebox.showinfo("Ugyldig regionkode.","Ugyldig regionkode." )
      sys.exit(0)
    # Collect fraction dose:
    # (Floats expect . so for more flexibility we will replace , with . as , is commonly used in Norway for floats)
    fraction_dose = float(self.fraction_dose_entry.get().replace(',', '.'))
    if not 0 < fraction_dose < 26: 
      messagebox.showinfo("Ugyldig fraksjonsdose.","Ugyldig fraksjonsdose." )
      sys.exit(0)
    # Collect number of fractions:
    if 0 < int(self.number_of_fractions_entry.get()) <= 40:
      number_of_fractions = int(self.number_of_fractions_entry.get())
    else:
      messagebox.showinfo("Ugyldig antall fraksjoner.","Ugyldig antall fraksjoner." )
      sys.exit(0)
    # Collect initials:
    if 0 < len(self.initials_entry.get()) < 4:
      initials = self.initials_entry.get()
    else:
      messagebox.showinfo("Ugyldige initialer.","Ugyldige initialer." )
      sys.exit(0)
    # Return the collected parameters:
    return (region_code,fraction_dose,number_of_fractions,initials)


  # Handles the shut down of the UI when the OK button is clicked.
  def ok_clicked(self, event=None):
    self.ok = True
    self.quit()
    return self.ok


  # Returns initials derived from the windows user name.
  def user_initials(self):
    user_name = os.getlogin()
    users = USERS.UserList("C:\\temp\\raystation-scripts\\settings\\users.tsv")
    initials = users.get_initials(user_name)
    return initials
