# Class that creates a text box GUI used to compute perturbated doses, the user has to type a number for the x, y and z directions
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6
from tkinter import *
from tkinter import messagebox
class TextBoxFrame(Frame):
    def __init__(self, the_window):
        Frame.__init__(self, the_window, bg = 'white')
        self.ok = False
        self.create_widgets()
        the_window.geometry("195x220+1100+500")
        the_window.title("Perturberte doser")
        the_window.configure(background = 'white')
                 
    def create_widgets(self):
        # Create label
        self.l = Label(self, text = "Beregn perturberte doser:", font = ("TkDefaultFont",10), bg = 'white')
        # Set up labels and entries
        self.x = DoubleVar()
        self.x.set(0.5)
        self.x_label = Label(self, text = "+/- x [cm]", width = 10, bg = 'white')
        self.x_entry = Entry(self, textvariable = self.x, width = 10, bg = 'white')

        self.y = DoubleVar()
        self.y.set(0.5)
        self.y_label = Label(self, text = "+/- y [cm]", width = 10, bg = 'white')
        self.y_entry = Entry(self, textvariable = self.y, width = 10, bg = 'white')

        self.z = DoubleVar()
        self.z.set(0.5)
        self.z_label = Label(self, text = "+/- z [cm]", width = 10, bg = 'white')
        self.z_entry = Entry(self, textvariable = self.z, width = 10, bg = 'white')
        
        self.okButton = Button(self, text = "OK", command = self.ok_clicked, font = ("TkDefaultFont",10), bg = 'white')
        self.quitButton = Button(self, text = "Cancel", command = self.cancel_clicked, font = ("TkDefaultFont",10), bg = 'white')
        
        # Place the labels and entries
        self.l.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)
        self.x_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = E)
        self.x_entry.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        self.y_label.grid(row = 2, column = 0, padx = 10, pady = 10)
        self.y_entry.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        self.z_label.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.z_entry.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        self.okButton.grid(row = 4, column = 0, padx = 10, pady = 10, ipadx = 10)
        self.quitButton.grid(row = 4, column = 1,padx = 10, pady = 10)
        
        # Sets focus to this text box
        self.x_entry.focus()

    # This function is called from a function in the script to get the results from the user input
    def get_results(self):
        if 0 < float(self.x_entry.get()) < 5 and 0 < float(self.y_entry.get()) < 5 and 0 < float(self.z_entry.get()) < 5:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            z = float(self.z_entry.get())
        else:
            messagebox.showinfo("Ugyldig verdi.","Ugyldig verdi." )
            sys.exit(0)
        
        return (x,y,z)

    # Handles the event of a click on the Cancel-button, closes current window
    def cancel_clicked(self, event=None):
        self.quit()

    # Handles the event of a click on the OK-button, closes current window
    def ok_clicked(self, event=None):
        self.ok = True
        self.quit()
        return self.ok

