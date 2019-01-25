# encoding: utf8

# Import system libraries:
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton, TextBox)

# Import local files:
import structure_set_functions as SSF


# Class that sets up a fractionation dialogue.
# This window contains 1-3 textboxes for entering a region code.
class RegionCodeForm(Form):

    _selectedRegionCode = None

    @property
    def SelectedRegionCodes( self ):
        return self._selectedRegionCodes

    def __init__(self, ss):
        self.Text = "Regionkode"
        self.AutoSize = True
        self.ss = ss
        self.nr_targets = SSF.determine_nr_of_indexed_ptvs(self.ss)
        self.Height = (self.nr_targets)*30 + 150
        self.ok_button_location = (self.nr_targets)*22 +15
        self.textbox = []

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False

        self.setupRegionCode()
        self.setupButtons()

        self.Controls.Add(self.regionCodePanel)
        self.Controls.Add(self.buttonPanel)

        self.ShowDialog()


    def newPanel(self, x, y):
        panel = Panel()
        panel.AutoSize = True
        panel.Location = Point(x, y)
        panel.BorderStyle = BorderStyle.None
        return panel


    def setupRegionCode( self):
        self.regionCodePanel = self.newPanel(0, 0)
        self.regionCodeLabel1 = Label()
        self.regionCodeLabel1.Text = "Regionkode, flere målvolum (må være forskjellig!)"
        self.regionCodeLabel1.Location = Point(25, 25)
        self.regionCodeLabel1.AutoSize = True
        self.regionCodes = []
        self.regionCodePanel.Controls.Add(self.regionCodeLabel1)

        for i in range(0, self.nr_targets-1):
          regionCodeLabel2 = Label()
          regionCodeLabel2.Text = "PTV" + str(i + 2) + ":"
          regionCodeLabel2.Location = Point(self.regionCodeLabel1.Location.X, self.regionCodeLabel1.Location.Y + (i+1) * 35)
          regionCodeLabel2.AutoSize = True
          t = TextBox()
          t.Text =""
          t.Location = Point(self.regionCodeLabel1.Location.X+ 40, self.regionCodeLabel1.Location.Y + (i+1) * 35)
          t.Width = 100
          t.MaxLength = 4
          self.regionCodePanel.Controls.Add(regionCodeLabel2)
          self.regionCodePanel.Controls.Add(t)
          self.regionCodes.append(t)


    def okClicked(self, sender, args):
      match = False
      for t in self.regionCodes:
        if 0 < int(t.Text) < 595:
          self.textbox.extend([t.Text])
          match = True
        else:
          raise IOError("Ugyldig regionkode.")

      if match:
        self._selectedRegionCodes = self.textbox

      self.DialogResult = DialogResult.OK
      self.Dispose


    def cancelClicked(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Dispose


    def setupButtons(self):
        self.buttonPanel = self.newPanel(0, self.ok_button_location)

        okButton = Button()
        okButton.Text = "OK"
        okButton.Location = Point(25, self.ok_button_location)
        self.AcceptButton = okButton
        okButton.Click += self.okClicked

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Location = Point(okButton.Left + okButton.Width + 10, okButton.Top)
        self.CancelButton = cancelButton
        cancelButton.Click += self.cancelClicked

        self.buttonPanel.Controls.Add(okButton)
        self.buttonPanel.Controls.Add(cancelButton)
