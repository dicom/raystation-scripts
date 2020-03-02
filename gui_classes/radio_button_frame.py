# Class that creates a radio button GUI and returns the selected radio button
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6
from tkinter import *
from tkinter import messagebox

class RadioButtonFrame(Frame):
    def __init__(self,the_window, radio_button_object):
        Frame.__init__(self, the_window, bg='white')
        self.ok = False
        self.radio_button_object = radio_button_object
        self.create_widgets()
        # Parameters for h = height, w = width of window, as well as location on the screen: x and y 
        h = len(self.radio_button_object.elements)*28 + 110
        w = 350
        x = 1100
        y = 500
        # Set these parameters
        the_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # Title of window
        the_window.title(self.radio_button_object.text)
        # Set the background to white
        the_window.configure(bg = 'white')

                 
    def create_widgets(self):
        # Parameter for width of the label in characters 
        w = 40
        # Parameter that limit the number of characters in each line by setting this option to the desired number
        wl = 300
        # Create dictionary from radio_button_objects for name and value
        values = {}
        for i in range(len(self.radio_button_object.elements)):
          values[self.radio_button_object.elements[i].name] = self.radio_button_object.elements[i].value
        # Label
        self.l = Label(self, text = self.radio_button_object.label, font = ("TkDefaultFont",10), anchor = W, bg = 'white',width = w)
        # Declear string variable to hold information on which radio button that is selected
        self.v = StringVar()

        j=0
        for (text,value) in values.items():
            b = Radiobutton(self, text = text, variable = self.v, value = value, wraplength = wl, bg = 'white', font = ("TkDefaultFont",10), justify = LEFT)
            b.grid(row = j+1, column = 0,sticky = W,padx = 12,columnspan=2)
            # Pre-select the button that is defined to be the default 
            if self.radio_button_object.elements[j].default:
                b.select()
            j+=1

        # Create OK and Cancel buttons       
        self.okButton = Button(self, text = "OK", command = self.ok_clicked, font = ("TkDefaultFont",10), bg = 'white')
        self.quitButton = Button(self, text = "Cancel", command = self.cancel_clicked, font = ("TkDefaultFont",10), bg = 'white')
        # Place label 
        self.l.grid(row = 0,column = 0, padx = 10, pady = 10,columnspan = 2)
        # Place OK and Cancel buttons
        self.okButton.grid(row = len(self.radio_button_object.elements)+1 , column = 0, padx = 20, pady = 15, ipadx = 10, sticky = E)
        self.quitButton.grid(row = len(self.radio_button_object.elements)+1, column = 1, padx = 20, pady = 15, sticky = W)
        
    # Handles the event of a click on the Cancel-button, closes current window
    def cancel_clicked(self, event = None):
        self.quit()

    # Handles the event of a click on the OK-button, closes current window
    def ok_clicked(self, event = None):
        self.ok = True
        self.quit()
        return self.ok

    # This function is called from other functions in the script to get the results from the user input
    def get_results(self):
        for i in range(len(self.radio_button_object.elements)):
            # The .get() method gets the information on which button that is selected
            if self.v.get() == self.radio_button_object.elements[i].value:
                # Return the radio button element and the radio button value that is selected
                return (self.radio_button_object.elements[i],self.radio_button_object.elements[i].value)
