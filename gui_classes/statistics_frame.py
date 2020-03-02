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

class StatisticsFrame(Frame):
    def __init__(self,the_window, radio_button_object):
        Frame.__init__(self, the_window, bg='white')
        self.ok = False
        self.radio_button_object = radio_button_object
        self.create_widgets()
        # Parameters for h = height, w = width of window, as well as location on the screen: x and y 
        h = len(self.radio_button_object.elements)*15 + 350
        w = 350
        x = 1100
        y = 250
        the_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        the_window.title(self.radio_button_object.text)
        the_window.configure(bg = 'white')

                 
    def create_widgets(self):
        # Crate label
        self.l = Label(self, text = 'Velg periode du ønsker å hente ut statistikk fra:', font = ("TkDefaultFont",10), anchor = W, bg = 'white', width = 35, justify = LEFT)
        # Declear list to hold the checkbuttons 
        self.checkbuttons = []
        # Declear list to hold the checkbutton variables (whether they are checked or not)
        self.variables = []
        # Create the number of checkbuttons based on the length of the radiobutton elements (the number of OARs)
        # Set up labels and entries
        self.start_date = StringVar()
        self.start_date.set('01.01.2019')
        self.start_date_label = Label(self, text = "Startdato", width = 10, bg = 'white', font = ("TkDefaultFont",10))
        self.start_date_entry = Entry(self, textvariable = self.start_date, width = 10, bg = 'white',font = ("TkDefaultFont",10))

        
        self.stop_date = StringVar()
        self.stop_date.set('20.02.2019')
        self.stop_date_label = Label(self, text = "Sluttdato", width = 10, bg = 'white', font = ("TkDefaultFont",10))
        self.stop_date_entry = Entry(self, textvariable = self.stop_date, width = 10, bg = 'white',font = ("TkDefaultFont",10))
        self.stereotactic_label = Label(self, text = "Velg:", width = 10, bg = 'white', font = ("TkDefaultFont",10),anchor = W)
        self.s = IntVar()
        self.stereotactic = Checkbutton(self, text = 'Stereotaksi', variable = self.s, wraplength = 150, onvalue = 1, offvalue = 0, bg = 'white',font = ("TkDefaultFont",10))
        self.c = IntVar()
        self.conv = Checkbutton(self, text = 'Konvensjonell', variable = self.c, wraplength = 150, onvalue = 1, offvalue = 0, bg = 'white',font = ("TkDefaultFont",10))
        
        self.l1 = Label(self, text = 'Velg parametere:', font = ("TkDefaultFont",10), anchor = W, bg = 'white', width = 15)
        v1 = IntVar()
        self.button = Checkbutton(self, text = "Alle:", variable = v1, command=self.select_all, wraplength = 150, onvalue = 1, offvalue = 0, bg = 'white',font = ("TkDefaultFont",10))
        j = 6
        for i in range(len(self.radio_button_object.elements)):
            # Declear int variable to hold information on which checkbutton that is selected
            v = IntVar()
            # Create checkbuttons
            b = Checkbutton(self, text = self.radio_button_object.elements[i].name, variable = v, wraplength = 155, onvalue = 1, offvalue = 0, bg = 'white',font = ("TkDefaultFont",10),justify = LEFT)
            # Make two columns as the list of OARs is very long
            if i > (len(self.radio_button_object.elements)/2)-1:
                # Place checkbuttons
                b.grid(row = j+1 , column = 1, sticky = W, padx = 12)
                j+=1
            else:
                # Place checkbuttons
                b.grid(row = i+7 , column = 0, sticky = W, padx = 12)
            # Store checkbuttons and variables in list
            self.checkbuttons.append(b)
            self.variables.append(v)
        
        # Create OK and Cancel buttons    
        self.okButton = Button(self, text="OK",command=self.ok_clicked,font = ("TkDefaultFont",10),bg = 'white')
        self.quitButton = Button(self, text="Cancel", command=self.cancel_clicked,font = ("TkDefaultFont",10),bg = 'white')
        # Place label 
        self.l.grid(row=0,column=0,padx = 10, pady = 10, columnspan = 2,sticky = W)
        self.start_date_label.grid(row = 1, column = 0, padx = 10, pady = 10,sticky = W)
        self.start_date_entry.grid(row = 1, column = 1, padx = 10, pady = 10,sticky = W)

        self.stop_date_label.grid(row = 2, column = 0, padx = 10, pady = 10,sticky = W)
        self.stop_date_entry.grid(row = 2, column = 1, padx = 10, pady = 10,sticky = W)
        self.stereotactic_label.grid(row = 3, column =0,padx = 10, pady = 10,sticky = W)
        self.stereotactic.grid(row = 4, column =0,padx = 10, pady = 10,sticky = W)
        self.conv.grid(row = 4, column =1, padx = 10, pady = 10,sticky = W)
         
        self.l1.grid(row=5,column=0,padx = 10, pady = 10,sticky = W)
        self.button.grid(row = 6, column = 0, padx = 10, pady = 10,sticky = W)
        # Place OK and Cancel buttons
        self.okButton.grid(row = len(self.radio_button_object.elements)+5, column = 0, padx = 10, pady = 10, ipadx = 6)
        self.quitButton.grid(row = len(self.radio_button_object.elements)+5, column = 1, padx = 10, pady = 10)
        self.start_date_entry.focus()
    
    def select_all(self):
      for j in self.checkbuttons:
        j.select()

        
    # This function is called from a function in the script to get the results from the user input
    def get_results(self):
      s = str(self.start_date_entry.get())
      t= str(self.stop_date_entry.get())
      if 0 < int(s[0:2]) < 32 and 0 < int(s[3:5]) < 13 and 2014 < int(s[6:10]) < 2021 and 0 < int(t[0:2]) < 32 and 0 < int(t[3:5]) < 13 and 2014 < int(t[6:10]) < 2021:
        start_date = s
        stop_date = t
      else:
        messagebox.showinfo("Ugyldig verdi.","Ugyldig verdi." )
        sys.exit(0)
      conv = False
      stereotactic = False
      if self.s.get() == 1:      
        stereotactic = True
      if self.c.get() == 1:
        conv = True
        
      return (start_date,stop_date,stereotactic, conv)

    # Handles the event of a click on the Cancel-button, closes current window
    def cancel_clicked(self, event=None):
        self.quit()
    # Handles the event of a click on the OK-button, closes current window
    def ok_clicked(self, event=None):
        self.ok = True
        self.quit()
        return self.ok

                 





