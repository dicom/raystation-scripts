# Import system libraries:
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, CheckBox, TextBox)


# Class that sets up a generic radio button dialogue.
class CheckBoxForm(Form):

    _selectedBoxes = None

    @property
    def SelectedBoxes( self ):
        return self._selectedBoxes

    def __init__(self, radio_button_object):
        self.radio_button_object = radio_button_object
        #self.Height = len(self.radio_button_object.elements)*25 + 150
        self.Width = 400
        self.Text = self.radio_button_object.text
        self.AutoSize = True
        self.ok_button_location = 400
        self.textbox = []

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False

        self.setupcheckBoxes()
        self.setupButtons()

        self.Controls.Add(self.checkBoxPanel)
        self.Controls.Add(self.buttonPanel)

        self.ShowDialog()


    def newPanel(self, x, y):
        panel = Panel()
        panel.AutoSize = True
        panel.Location = Point(x, y)
        panel.BorderStyle = BorderStyle.None
        return panel


    def setupcheckBoxes(self):
        self.checkBoxPanel = self.newPanel(0, 0)
        self.checkBoxLabel1 = Label()
        self.checkBoxLabel1.Text = self.radio_button_object.label
        self.checkBoxLabel1.Location = Point(25, 25)
        self.checkBoxLabel1.AutoSize = True
        self.checkBoxPanel.Controls.Add(self.checkBoxLabel1)
        self.checkBoxes = []
        j = 0
        for i, t in enumerate(self.radio_button_object.elements):
          b = CheckBox()
          b.Text = t.name
          if i > len(self.radio_button_object.elements)/2:
            b.Location = Point(self.checkBoxLabel1.Location.X + 200, self.checkBoxLabel1.Location.Y + (j+1) * 25)
            j += 1
          else:
            b.Location = Point(self.checkBoxLabel1.Location.X, self.checkBoxLabel1.Location.Y + (i+1) * 25)
          b.AutoSize = True
          self.checkBoxPanel.Controls.Add(b)
          self.checkBoxes.append(b)


    def okClicked(self, sender, args):
      #match = False

      #self.checkBoxes.append(self.b.Checked)

      #for t in self.checkBoxes:
      #  self.textbox.extend([t.Text])
      #  match = True
      #else:
      #  raise IOError("Ingen bokser er valgt!")

      #if match:
      self._selectedBoxes = self.checkBoxes

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
