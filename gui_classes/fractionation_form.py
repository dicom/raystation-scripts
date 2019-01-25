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
class FractionationForm(Form):

    _selectedRegionCode = None
    _selectedFractionDose = None
    _selectedNumberFractions = None
    _selectedPlannerInitials = None

    @property
    def SelectedRegionCode( self ):
        return self._selectedRegionCode
    @property
    def SelectedFractionDose( self ):
        return self._selectedFractionDose
    @property
    def SelectedNumberOfFractions( self ):
        return self._selectedNumberFractions
    @property
    def SelectedPlannerInitials( self ):
        return self._selectedPlannerInitials


    def __init__(self):
        self.Text = "Fraksjonering"
        self.AutoSize = True
        #self.Heigth = 500

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False

        self.setupRegionCode()
        self.setupFractionDoseCode()
        self.setupNumberOfFractions()
        self.setupPlannerInitials()
        self.setupButtons()

        self.Controls.Add(self.regionCodePanel)
        self.Controls.Add(self.fractionDosePanel)
        self.Controls.Add(self.numberFractionsPanel)
        self.Controls.Add(self.plannerInitialsPanel)
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
        self.regionCodeLabel1.Text = "Regionkode:"
        self.regionCodeLabel1.Location = Point(25, 25)
        self.regionCodeLabel1.AutoSize = True

        self.regionCodeTextbox = TextBox()
        self.regionCodeTextbox.Text =""
        self.regionCodeTextbox.Location = Point(25, 50)
        self.regionCodeTextbox.Width = 100
        self.regionCodeTextbox.MaxLength = 4

        self.regionCodePanel.Controls.Add(self.regionCodeLabel1)
        self.regionCodePanel.Controls.Add(self.regionCodeTextbox)


    def setupFractionDoseCode( self):
        self.fractionDosePanel = self.newPanel(0, 25)

        self.fractionDoseLabel1 = Label()
        self.fractionDoseLabel1.Text = "Fraksjonsdose [Gy]:"
        self.fractionDoseLabel1.Location = Point(25, 75)
        self.fractionDoseLabel1.AutoSize = True

        self.fractionDoseTextbox = TextBox()
        self.fractionDoseTextbox.Text =""
        self.fractionDoseTextbox.Location = Point(25, 100)
        self.fractionDoseTextbox.Width = 100
        self.fractionDoseTextbox.MaxLength = 4

        self.fractionDosePanel.Controls.Add(self.fractionDoseLabel1)
        self.fractionDosePanel.Controls.Add(self.fractionDoseTextbox)


    def setupNumberOfFractions( self):
        self.numberFractionsPanel = self.newPanel(0, 75)

        self.numberFractionsLabel1 = Label()
        self.numberFractionsLabel1.Text = "Antall fraksjoner:"
        self.numberFractionsLabel1.Location = Point(25, 100)
        self.numberFractionsLabel1.AutoSize = True

        self.numberFractionsTextbox = TextBox()
        self.numberFractionsTextbox.Text =""
        self.numberFractionsTextbox.Location = Point(25, 125)
        self.numberFractionsTextbox.Width = 100
        self.numberFractionsTextbox.MaxLength = 3

        self.numberFractionsPanel.Controls.Add(self.numberFractionsLabel1)
        self.numberFractionsPanel.Controls.Add(self.numberFractionsTextbox)


    def setupPlannerInitials( self):
        self.plannerInitialsPanel = self.newPanel(0, 100)

        self.plannerInitialsLabel1 = Label()
        self.plannerInitialsLabel1.Text = "Doseplanleggers initialer:"
        self.plannerInitialsLabel1.Location = Point(25, 150)
        self.plannerInitialsLabel1.AutoSize = True

        self.plannerInitialsTextbox = TextBox()
        self.plannerInitialsTextbox.Text =""
        self.plannerInitialsTextbox.Location = Point(25, 175)
        self.plannerInitialsTextbox.Width = 100
        self.plannerInitialsTextbox.MaxLength = 4

        self.plannerInitialsPanel.Controls.Add(self.plannerInitialsLabel1)
        self.plannerInitialsPanel.Controls.Add(self.plannerInitialsTextbox)


    def okClicked(self, sender, args):
      if 0 < int(self.regionCodeTextbox.Text) < 595:
        self._selectedRegionCode = self.regionCodeTextbox.Text
      else:
        raise IOError("Ugyldig regionkode.")

      if 0 < float(self.fractionDoseTextbox.Text) < 26:
        self._selectedFractionDose = self.fractionDoseTextbox.Text
      else:
        raise IOError("Ugyldig fraksjondose.")

      if 0 < int(self.numberFractionsTextbox.Text) < 40:
        self._selectedNumberFractions = self.numberFractionsTextbox.Text
      else:
        raise IOError("Ugyldig antall fraksjoner.")

      if 1 < len(self.plannerInitialsTextbox.Text) < 4 :
        self._selectedPlannerInitials = self.plannerInitialsTextbox.Text
      else:
        raise IOError("Skriv initialer!.")
      self.DialogResult = DialogResult.OK
      self.Dispose


    def cancelClicked(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Dispose


    def setupButtons(self):
        self.buttonPanel = self.newPanel(0, 170)

        okButton = Button()
        okButton.Text = "OK"
        okButton.Location = Point(25, 170)
        self.AcceptButton = okButton
        okButton.Click += self.okClicked

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Location = Point(okButton.Left + okButton.Width + 10, okButton.Top)
        self.CancelButton = cancelButton
        cancelButton.Click += self.cancelClicked

        self.buttonPanel.Controls.Add(okButton)
        self.buttonPanel.Controls.Add(cancelButton)
