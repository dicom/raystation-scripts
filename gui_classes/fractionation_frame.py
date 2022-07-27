# Class that creates a text box GUI to get information on region code, fraction dose, number of fractions and initials
#
# Authors:
# Marit Funderud
# Helse Møre og Romsdal HF
#
# Made for RayStation version: 9.A
# Python 3.6
from tkinter import *
from tkinter import messagebox
class FractionationFrame(Frame):
    def __init__(self,the_window):
        Frame.__init__(self, the_window,bg = 'white')
        self.ok = False
        self.create_widgets()
        h = 270
        w = 350
        x = 1100
        y = 500
        the_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #the_window.geometry("270x260+1100+500")
        the_window.title("Fraksjonering")
        the_window.configure(bg = 'white')
                 
    def create_widgets(self):
        w = 13
        wl = 127
        # Empty label (just to make the window look nice)
        self.l = Label(self, text = "", width = 40, anchor = W,bg = 'white')
        
        # Set up labels and entries
        self.region_code = StringVar(None)
        self.region_code_label = Label(self, text = "Regionkode:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W, bg = 'white')
        self.region_code_entry = Entry(self, textvariable = self.region_code, width = w, bg = 'white', font = ("TkDefaultFont",10))

        self.fraction_dose = StringVar(None)
        self.fraction_dose_label = Label(self, text = "Fraksjondose [Gy]:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W,bg = 'white')
        self.fraction_dose_entry = Entry(self, textvariable = self.fraction_dose, width = w, bg = 'white', font = ("TkDefaultFont",10))

        self.number_of_fractions = StringVar(None)
        self.number_of_fractions_label = Label(self, text = "Antall fraksjoner:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W, bg = 'white')
        self.number_of_fractions_entry = Entry(self, textvariable = self.number_of_fractions, width = w, bg = 'white', font = ("TkDefaultFont",10))

        self.initials = StringVar()
        self.initials_label = Label(self, text = "Doseplanleggers initialer:", font = ("TkDefaultFont",10), width = w, wraplength = wl, anchor = W, justify = LEFT, bg = 'white')
        self.initials_entry = Entry(self, textvariable = self.initials, width = w, bg = 'white', font = ("TkDefaultFont",10))

        # Create OK and Cancel buttons 
        self.okButton = Button(self, text = "OK", command = self.ok_clicked, font = ("TkDefaultFont",10), bg = 'white')
        self.quitButton = Button(self, text = "Cancel", command = self.cancel_clicked, font = ("TkDefaultFont",10), bg = 'white')

        # Place the labels and entries
        self.l.grid(row = 0, column = 0, padx = 15, columnspan = 2)
        
        self.region_code_label.grid(row = 1, column = 0, padx = 15, pady = 10)
        self.region_code_entry.grid(row = 1, column = 1, padx = 15, pady = 10)
        
        self.fraction_dose_label.grid(row = 2, column = 0, padx = 15, pady = 10)
        self.fraction_dose_entry.grid(row = 2, column = 1, padx = 15, pady = 10)
        
        self.number_of_fractions_label.grid(row = 3, column = 0, padx = 15, pady = 10)
        self.number_of_fractions_entry.grid(row = 3, column = 1, padx = 15, pady = 10)

        self.initials_label.grid(row = 4, column = 0, padx = 15, pady = 10)
        self.initials_entry.grid(row = 4, column = 1, padx = 15, pady = 10)

        # Place OK and Cancel buttons
        self.okButton.grid(row = 5, column = 0, padx = 20, pady = 15, ipadx = 10, sticky = E)
        self.quitButton.grid(row = 5, column = 1, padx = 20, pady = 15, sticky = W)
        
        # Sets focus to this text box
        self.region_code_entry.focus()

    # This function is called from a function in the script to get the results from the user input
    def get_results(self):
        if 0 < int(self.region_code_entry.get()) < 595:
            region_code = int(self.region_code_entry.get())
        else:
            messagebox.showinfo("Ugyldig regionkode.","Ugyldig regionkode." )
            sys.exit(0)
    
        # Floats expect . (for more flexibility we will replace , with . as , is commonly used in Norway for floats)
        fraction_dose = float(self.fraction_dose_entry.get().replace(',', '.'))
        if not 0 < fraction_dose < 26: 
            messagebox.showinfo("Ugyldig fraksjonsdose.","Ugyldig fraksjonsdose." )
            sys.exit(0)
            
        if 0 < int(self.number_of_fractions_entry.get()) <= 40:
            number_of_fractions = int(self.number_of_fractions_entry.get())
        else:
            messagebox.showinfo("Ugyldig antall fraksjoner.","Ugyldig antall fraksjoner." )
            sys.exit(0)

        if 0 < len(self.initials_entry.get()) < 4:
            initials = self.initials_entry.get()
        else:
            messagebox.showinfo("Ugyldige initialer.","Ugyldige initialer." )
            sys.exit(0)
        
        return (region_code,fraction_dose,number_of_fractions,initials)
    
    def cancel_clicked(self, event=None):
        self.quit()

    def ok_clicked(self, event=None):
        self.ok = True
        self.quit()
        return self.ok
