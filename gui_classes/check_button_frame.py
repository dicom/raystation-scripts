# Class that creates a check button GUI that gives a list of OARs in a GUI, and returns the selected check boxes
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6
from tkinter import *
from tkinter import messagebox

class CheckButtonFrame(Frame):
    def __init__(self,the_window, radio_button_object):
        Frame.__init__(self, the_window, bg='white')
        self.ok = False
        self.radio_button_object = radio_button_object
        self.create_widgets()
        # Parameters for h = height, w = width of window, as well as location on the screen: x and y 
        h = len(self.radio_button_object.elements)*13 + 80
        w = 290
        x = 1100
        y = 250
        the_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        the_window.title(self.radio_button_object.text)
        the_window.configure(bg = 'white')
                 
    def create_widgets(self):
        # Crate label
        self.l = Label(self, text = self.radio_button_object.label, font = ("TkDefaultFont",10), anchor = W, bg = 'white', width = 15)
        # Declear list to hold the checkbuttons 
        self.checkbuttons = []
        # Declear list to hold the checkbutton variables (whether they are checked or not)
        self.variables = []
        # Create the number of checkbuttons based on the length of the radiobutton elements (the number of OARs)
        j = 0
        for i in range(len(self.radio_button_object.elements)):
            # Declear int variable to hold information on which checkbutton that is selected
            v = IntVar()
            # Create checkbuttons
            b = Checkbutton(self, text = self.radio_button_object.elements[i].name, variable = v, wraplength = 100, onvalue = 1, offvalue = 0, bg = 'white')
            # Make two columns as the list of OARs is very long
            if i > len(self.radio_button_object.elements)/2:
                # Place checkbuttons
                b.grid(row = j+1 , column = 1, sticky = W, padx = 12)
                j+=1
            else:
                # Place checkbuttons
                b.grid(row = i+1 , column = 0, sticky = W, padx = 12)
            # Store checkbuttons and variables in list
            self.checkbuttons.append(b)
            self.variables.append(v)
        
        # Create OK and Cancel buttons    
        self.okButton = Button(self, text="OK",command=self.ok_clicked,font = ("TkDefaultFont",10),bg = 'white')
        self.quitButton = Button(self, text="Cancel", command=self.cancel_clicked,font = ("TkDefaultFont",10),bg = 'white')
        # Place label 
        self.l.grid(row=0,column=0,padx = 10, pady = 10)
        # Place OK and Cancel buttons
        self.okButton.grid(row = len(self.radio_button_object.elements), column = 0, padx = 10, pady = 10, ipadx = 6)
        self.quitButton.grid(row = len(self.radio_button_object.elements), column = 1, padx = 10, pady = 10)

    # Handles the event of a click on the Cancel-button, closes current window
    def cancel_clicked(self, event=None):
        self.quit()
    # Handles the event of a click on the OK-button, closes current window
    def ok_clicked(self, event=None):
        self.ok = True
        self.quit()
        return self.ok

  
    
