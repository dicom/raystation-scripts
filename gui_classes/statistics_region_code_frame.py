# Class that creates a text box GUI for the situation of multiple target volumes where the user needs to enter
# region codes for the targets beyond the first one. The entered region codes are returned.
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6
from tkinter import *
from tkinter import messagebox

# Import local files:
import structure_set_functions as SSF
import region_codes as RC

# This window contains 1-3 textboxes for entering a region code.
class RegionCodeFrame(Frame):
    def __init__(self,the_window):
        Frame.__init__(self, the_window,bg = 'white')
        self.ok = False
        self.create_widgets()
        self.nr_targets = 12
        # Parameters for h = height, w = width of window, as well as location on the screen: x and y 
        h = self.nr_targets*35 + 140
        #w = 240
        w = 300
        x = 1100
        y = 250
        # Set these parameters
        the_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # Title of window
        the_window.title("Regionkoder")
        # Set the background to white
        the_window.configure(bg = 'white')
                 
    def create_widgets(self):
        # Parameter for width of the label in characters 
        w = 13
        # Parameter that limit the number of characters in each line by setting this option to the desired number
        wl = 300
        # Create label
        self.l1 = Label(self, text = "Skriv inn regionkoder:", font = ("TkDefaultFont",10), anchor = W, width = 36,bg = 'white') 
        # Number of targets (PTVs)
        self.nr_targets = 12
        # Declear list to hold the input text
        self.textbox = []
        #codes = RC.lung_and_mediastinum_codes
        #codes = RC.brain_codes
        #codes = RC.palliative_all_codes
        codes = RC.breast_reg_codes
        #codes = RC.rectum_codes
        # Create the number of textboxes and labels based on number of PTVs
        #for i in range(self.nr_targets-1):
        for i in range(len(codes)):
            # Label
            #l2 = Label(self, text = "", font = ("TkDefaultFont",10), width = w, bg = 'white')
            # Textbox entry
            self.code = StringVar()
            self.code.set(str(codes[i]))
            entry = Entry(self, textvariable = self.code, width = 13, bg = 'white', font = ("TkDefaultFont",10))
            # Place label and entry
            #l2.grid(row = i+1 , column = 0, padx = 15, pady = 10)
            entry.grid(row = i+1 , column = 0, padx = 15, pady = 10, columnspan = 2)
            # Store entry in list
            self.textbox.append(entry)

        # Create OK and Cancel buttons 
        self.okButton = Button(self, text = "OK", command = self.ok_clicked, font = ("TkDefaultFont",10), bg = 'white')
        self.quitButton = Button(self, text = "Cancel", command = self.cancel_clicked, font = ("TkDefaultFont",10), bg = 'white')
        
        # Place label 
        self.l1.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)
        
        # Place OK and Cancel buttons
        self.okButton.grid(row = self.nr_targets, column = 0, padx = 20, pady = 15, ipadx = 10, sticky = E)
        self.quitButton.grid(row = self.nr_targets, column = 1, padx = 20, pady = 15, sticky = W)

    # This function is called from a function in the script to get the results from the user input
    def get_results(self):
        self.region_codes=[]
        for i in range(len(self.textbox)):
          self.region_codes.extend([int(self.textbox[i].get())])
          #messagebox.showinfo("", int(self.textbox[i].get()))
          
        
        return self.region_codes

    # Handles the event of a click on the Cancel-button, closes current window
    def cancel_clicked(self, event=None):
        self.quit()

    # Handles the event of a click on the OK-button, closes current window
    def ok_clicked(self, event=None):
        self.ok = True
        self.quit()
        return self.ok
