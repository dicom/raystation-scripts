# Import system libraries:
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton, TextBox)


# Class that sets up a fractionation dialogue.
# This window contains three textboxes:
# -Region code
# -Fraction dose
# -Number of fractoions
class TextBoxForm(Form):

    _selectedX = None
    _selectedY = None
    _selectedZ = None


    @property
    def SelectedX( self ):
        return self._selectedX
    @property
    def SelectedY( self ):
        return self._selectedY
    @property
    def SelectedZ( self ):
        return self._selectedZ


    def __init__(self):
        self.Text = "Beregn perturberte doser"
        self.AutoSize = True
        self.Height = 90

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.ok_button_location = 65

        self.setupX()
        self.setupY()
        self.setupZ()
        self.setupButtons()

        self.Controls.Add(self.XPanel)
        self.Controls.Add(self.YPanel)
        self.Controls.Add(self.ZPanel)
        self.Controls.Add(self.buttonPanel)

        self.ShowDialog()


    def newPanel(self, x, y):
        panel = Panel()
        panel.AutoSize = True
        panel.Location = Point(x, y)
        panel.BorderStyle = BorderStyle.None
        return panel


    def setupX( self):
        self.XPanel = self.newPanel(0, 0)
        self.XPanel.Height = 25

        self.XLabel = Label()
        self.XLabel.Text = "+/- x [cm]:"
        self.XLabel.Location = Point(25, 25)
        self.XLabel.AutoSize = True

        self.XTextBox = TextBox()
        self.XTextBox.Text ="0.5"
        self.XTextBox.Location = Point(self.XLabel.Location.X + 75, self.XLabel.Location.Y)
        self.XTextBox.Width = 50
        self.XTextBox.MaxLength = 3

        self.XPanel.Controls.Add(self.XLabel)
        self.XPanel.Controls.Add(self.XTextBox)


    def setupY( self):
        self.YPanel = self.newPanel(0, 30)
        self.YPanel.Height = 25
        self.YLabel = Label()
        self.YLabel.Text = "+/- y [cm]:"
        self.YLabel.Location = Point(25, 30)
        self.YLabel.AutoSize = True

        self.YTextBox = TextBox()
        self.YTextBox.Text ="0.5"
        self.YTextBox.Location = Point(self.YLabel.Location.X+ 75, self.YLabel.Location.Y)
        self.YTextBox.Width = 50
        self.YTextBox.MaxLength = 3

        self.YPanel.Controls.Add(self.YLabel)
        self.YPanel.Controls.Add(self.YTextBox)


    def setupZ( self):
        self.ZPanel = self.newPanel(0, 60)
        self.ZPanel.Height = 25
        self.ZLabel = Label()
        self.ZLabel.Text = "+/- z [cm]:"
        self.ZLabel.Location = Point(25, 35)
        self.ZLabel.AutoSize = True

        self.ZTextBox = TextBox()
        self.ZTextBox.Text ="0.5"
        self.ZTextBox.Location = Point(self.ZLabel.Location.X + 75, self.ZLabel.Location.Y)
        self.ZTextBox.Width = 50
        self.ZTextBox.MaxLength = 3

        self.ZPanel.Controls.Add(self.ZLabel)
        self.ZPanel.Controls.Add(self.ZTextBox)


    def okClicked(self, sender, args):
      if 0 < float(self.XTextBox.Text) < 3:
        self._selectedX = self.XTextBox.Text
      else:
        raise IOError("Ugyldig verdi.")

      if 0 < float(self.YTextBox.Text) < 3:
        self._selectedY = self.YTextBox.Text
      else:
        raise IOError("Ugyldig verdi.")

      if 0 < float(self.ZTextBox.Text) < 3:
        self._selectedZ = self.ZTextBox.Text
      else:
        raise IOError("Ugyldig verdi.")

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
