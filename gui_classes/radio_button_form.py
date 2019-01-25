# Import system libraries:
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton, TextBox)


# Class that sets up a generic radio button dialogue.
class RadioButtonForm(Form):

    _selectedButton = None

    @property
    def SelectedButton( self ):
        return self._selectedButton

    def __init__(self, radio_button_object):
        self.radio_button_object = radio_button_object
        self.Height = len(self.radio_button_object.elements)*25 + 150
        self.Width = 400
        self.Text = self.radio_button_object.text
        self.AutoSize = False
        self.ok_button_location = len(self.radio_button_object.elements)*15 +25

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False

        self.setupRadioButtons()
        self.setupButtons()

        self.Controls.Add(self.radioButtonPanel)
        self.Controls.Add(self.buttonPanel)

        self.ShowDialog()


    def newPanel(self, x, y):
        panel = Panel()
        panel.AutoSize = True
        panel.Location = Point(x, y)
        panel.BorderStyle = BorderStyle.None
        return panel


    def setupRadioButtons(self):
        self.radioButtonPanel = self.newPanel(0, 0)
        self.radioButtonLabel1 = Label()
        self.radioButtonLabel1.Text = self.radio_button_object.label
        self.radioButtonLabel1.Location = Point(25, 25)
        self.radioButtonLabel1.AutoSize = True
        self.radioButtonPanel.Controls.Add(self.radioButtonLabel1)
        self.radioButtons = []
        for i, t in enumerate(self.radio_button_object.elements):
          b = RadioButton()
          b.Text =t.name
          b.Location = Point(self.radioButtonLabel1.Location.X, self.radioButtonLabel1.Location.Y + (i+1) * 25)
          #if self.radio_button_object.default == t:
          if t.default:
            b.Checked = True
          b.AutoSize = True
          self.radioButtonPanel.Controls.Add(b)
          self.radioButtons.append(b)


    def okClicked(self, sender, args):
      for i, t in enumerate(self.radio_button_object.elements):
        if self.radioButtons[i].Checked:
          self._selectedButton = self.radio_button_object.elements[i]
      if not self._selectedButton:
        raise IOError("Selection failed.")

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
