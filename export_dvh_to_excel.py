# encoding: utf8

# Exports dose volume histograms from RayStation to Excel.
#
# Source:
# https://github.com/raysearchlabs/scripting
#
# Updated for RayStation 5.0: Christoffer Lervåg - 27.09.2016
# Tested for RayStation version: 6.0.

from connect import *
import clr, sys
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Microsoft.Office.Interop.Excel import *
from System.Drawing import (Color, ContentAlignment, Font, FontStyle, Point)
from System.Windows.Forms import (Application, BorderStyle, Button, CheckBox, DialogResult, Form, FormBorderStyle, Label, Panel, RadioButton)

# Class that sets up a simple dialogue
class DialogueForm(Form):

    _selectedDoseType = None
    _selectedDoseUnit = None
    _selectedVolumeUnit = None
    _selectedBeamSet = None
    _beamSetNames = None

    @property
    def ExcludeExternalRoi( self ):
        return self.excludeExternalRoiCheck1.Checked

    @property
    def SelectedVolumeUnit( self ):
        return self._selectedVolumeUnit

    @property
    def SelectedDoseUnit( self ):
        return self._selectedDoseUnit

    @property
    def SelectedDoseType( self ):
        return self._selectedDoseType

    @property
    def SelectedBeamSetName( self ):
        return self._selectedBeamSet


    def __init__(self, beamSetNames, supportedDoseTypes, supportedDoseUnits, supportedVolumeUnits):
        self.Text = "Plot DVH curve using MS Excel"
        self._beamSetNames = beamSetNames
        self.AutoSize = True

        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False

        self.setupDoseTypeRadioButtons( beamSetNames )
        self.setupDoseUnitRadioButtons( supportedDoseUnits )
        self.setupVolumeUnitRadioButtons( supportedVolumeUnits )
        self.setupExcludeExternalRoiCheckBox()
        self.setupButtons()

        self.Controls.Add(self.doseTypeRadioPanel)
        self.Controls.Add(self.doseUnitRadioPanel)
        self.Controls.Add(self.volumeUnitRadioPanel)
        self.Controls.Add(self.excludeExternalRoiCheckPanel)
        self.Controls.Add(self.buttonPanel)

        self.ShowDialog()

    def newPanel(self, x, y):
        panel = Panel()
        panel.AutoSize = True
        panel.Location = Point(x, y)
        panel.BorderStyle = BorderStyle.None
        return panel

    def setupDoseTypeRadioButtons(self, beamSetNames):
        self.doseTypeRadioPanel = self.newPanel(0, 0)

        self.doseTypeRadioLabel1 = Label()
        self.doseTypeRadioLabel1.Text = "Select dose:"
        self.doseTypeRadioLabel1.Location = Point(25, 25)
        self.doseTypeRadioLabel1.AutoSize = True

        multipleBeamSets = len(beamSetNames) > 1

        self.doseTypeRadio1 = RadioButton()
        self.doseTypeRadio1.Text = "Plan dose"
        self.doseTypeRadio1.Location = Point(self.doseTypeRadioLabel1.Location.X + 20, self.doseTypeRadioLabel1.Location.Y + 25)
        self.doseTypeRadio1.Checked = True
        self.doseTypeRadio1.Enabled = multipleBeamSets
        self.doseTypeRadio1.AutoSize = True

        self.doseTypeRadio2 = RadioButton()
        self.doseTypeRadio2.Text = 'Beam set dose: {0}'.format(beamSetNames[0])
        self.doseTypeRadio2.Location = Point(self.doseTypeRadio1.Location.X, self.doseTypeRadio1.Location.Y + 25)
        self.doseTypeRadio2.Enabled = multipleBeamSets
        self.doseTypeRadio2.AutoSize = True

        if multipleBeamSets:
            self.doseTypeRadio3 = RadioButton()
            self.doseTypeRadio3.Text = 'Beam set dose: {0}'.format(beamSetNames[1])
            self.doseTypeRadio3.Location = Point(self.doseTypeRadio2.Location.X, self.doseTypeRadio2.Location.Y + 25)
            self.doseTypeRadio3.AutoSize = True

        self.doseTypeRadioPanel.Controls.Add(self.doseTypeRadioLabel1)
        self.doseTypeRadioPanel.Controls.Add(self.doseTypeRadio1)
        self.doseTypeRadioPanel.Controls.Add(self.doseTypeRadio2)
        if multipleBeamSets:
            self.doseTypeRadioPanel.Controls.Add(self.doseTypeRadio3)

    def setupDoseUnitRadioButtons( self, doseUnits ):
        self.doseUnitRadioPanel = self.newPanel(0, 125)

        self.radioDoseUnitLabel1 = Label()
        self.radioDoseUnitLabel1.Text = "Select dose unit:"
        self.radioDoseUnitLabel1.Location = Point(25, 25)
        self.radioDoseUnitLabel1.AutoSize = True

        self.radioDoseUnit1 = RadioButton()
        self.radioDoseUnit1.Text = list(doseUnits)[0]
        self.radioDoseUnit1.Location = Point(self.radioDoseUnitLabel1.Location.X + 20, self.radioDoseUnitLabel1.Location.Y + 25)

        self.radioDoseUnit1.AutoSize = True

        self.radioDoseUnit2 = RadioButton()
        self.radioDoseUnit2.Text = list(doseUnits)[1]
        self.radioDoseUnit2.Location = Point(self.radioDoseUnit1.Location.X, self.radioDoseUnit1.Location.Y + 25)
        self.radioDoseUnit2.Checked = True
        self.radioDoseUnit2.AutoSize = True

        self.doseUnitRadioPanel.Controls.Add(self.radioDoseUnitLabel1)
        self.doseUnitRadioPanel.Controls.Add(self.radioDoseUnit1)
        self.doseUnitRadioPanel.Controls.Add(self.radioDoseUnit2)

    def setupVolumeUnitRadioButtons( self, volumeUnits ):
        self.volumeUnitRadioPanel = self.newPanel(0, 225)

        self.radioVolumeUnitLabel1 = Label()
        self.radioVolumeUnitLabel1.Text = "Select volume unit:"
        self.radioVolumeUnitLabel1.Location = Point(25, 25)
        self.radioVolumeUnitLabel1.AutoSize = True

        self.radioVolumeUnit1 = RadioButton()
        self.radioVolumeUnit1.Text = list(volumeUnits)[0]
        self.radioVolumeUnit1.Location = Point(self.radioVolumeUnitLabel1.Location.X + 20, self.radioVolumeUnitLabel1.Location.Y + 25)
        self.radioVolumeUnit1.Checked = True
        self.radioVolumeUnit1.AutoSize = True

        self.radioVolumeUnit2 = RadioButton()
        self.radioVolumeUnit2.Text = list(volumeUnits)[1]
        self.radioVolumeUnit2.Location = Point(self.radioVolumeUnit1.Location.X, self.radioVolumeUnit1.Location.Y + 25)

        self.radioVolumeUnit2.AutoSize = True

        self.volumeUnitRadioPanel.Controls.Add(self.radioVolumeUnitLabel1)
        self.volumeUnitRadioPanel.Controls.Add(self.radioVolumeUnit1)
        self.volumeUnitRadioPanel.Controls.Add(self.radioVolumeUnit2)

    def setupExcludeExternalRoiCheckBox(self):
        self.excludeExternalRoiCheckPanel = self.newPanel(0, 325)

        self.excludeExternalRoiCheck1 = CheckBox()
        self.excludeExternalRoiCheck1.Text = "Exclude external ROI:"
        self.excludeExternalRoiCheck1.Location = Point(45, 25)
        self.excludeExternalRoiCheck1.Width = 135
        self.excludeExternalRoiCheck1.TextAlign = ContentAlignment.MiddleLeft
        self.excludeExternalRoiCheck1.CheckAlign = ContentAlignment.MiddleRight
        self.excludeExternalRoiCheck1.Checked = False

        self.excludeExternalRoiCheckPanel.Controls.Add(self.excludeExternalRoiCheck1)

    def okClicked(self, sender, args):
        if self.doseTypeRadio1.Checked:
            self._selectedDoseType = self.doseTypeRadio1.Text
            self._selectedBeamSet = self.doseTypeRadio2.Text
        elif self.doseTypeRadio2.Checked:
            self._selectedDoseType = 'Beam set dose'
            self._selectedBeamSet = list(self._beamSetNames)[0]
        elif self.doseTypeRadio3.Checked:
            self._selectedDoseType = 'Beam set dose'
            self._selectedBeamSet = list(self._beamSetNames)[1]
        else:
            raise IOError("Dose type selection failed.")

        if self.radioDoseUnit1.Checked:
            self._selectedDoseUnit = self.radioDoseUnit1.Text
        elif self.radioDoseUnit2.Checked:
            self._selectedDoseUnit = self.radioDoseUnit2.Text
        else:
            raise IOError("Dose unit selection failed.")

        if self.radioVolumeUnit1.Checked:
            self._selectedVolumeUnit = self.radioVolumeUnit1.Text
        elif self.radioVolumeUnit2.Checked:
            self._selectedVolumeUnit = self.radioVolumeUnit2.Text
        else:
            raise IOError("Volume unit selection failed.")

        self.DialogResult = DialogResult.OK
        self.Dispose

    def cancelClicked(self, sender, args):
        self.DialogResult = DialogResult.Cancel
        self.Dispose

    def setupButtons(self):
        self.buttonPanel = self.newPanel(0, 375)

        okButton = Button()
        okButton.Text = "OK"
        okButton.Location = Point(25, 50)
        self.AcceptButton = okButton
        okButton.Click += self.okClicked

        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.Location = Point(okButton.Left + okButton.Width + 10, okButton.Top)
        self.CancelButton = cancelButton
        cancelButton.Click += self.cancelClicked

        self.buttonPanel.Controls.Add(okButton)
        self.buttonPanel.Controls.Add(cancelButton)

# Check that needed data is available
try:
    patient = get_current("Patient")
except SystemError:
    raise IOError("No patient loaded. Load patient and plan.")

try:
    case = get_current('Case')
except SystemError:
    raise IOError("No case loaded. Load patient and case.")

try:
    plan = get_current("Plan")
except SystemError:
    raise IOError("No plan loaded. Load patient and plan.")

try:
    beamset = get_current("BeamSet")
except SystemError:
    raise IOError("No beam set loaded.")

# Plan or beam set dose
PLAN_DOSE = 'Plan dose'
BEAM_SET_DOSE = 'Beam set dose'
SUPPORTED_DOSE_TYPES = set([PLAN_DOSE, BEAM_SET_DOSE])

# Units
VOLUME_PERCENT = r'%'
VOLUME_CC = 'cc'
SUPPORTED_VOLUME_UNITS = set([VOLUME_PERCENT, VOLUME_CC])
CGY = 'cGy'
GY = 'Gy'
SUPPORTED_DOSE_UNITS = set([CGY, GY])

# Propmt user for input
form = DialogueForm([x.DicomPlanLabel for x in plan.BeamSets], SUPPORTED_DOSE_TYPES, SUPPORTED_DOSE_UNITS, SUPPORTED_VOLUME_UNITS)
form.DialogResult
# Apply user configure
if form.DialogResult == DialogResult.OK:
    dose_type = form.SelectedDoseType
    beam_set_name = form.SelectedBeamSetName
    selected_dose_unit = form.SelectedDoseUnit
    selected_volume_unit = form.SelectedVolumeUnit
    exclude_external = form.ExcludeExternalRoi
elif form.DialogResult == DialogResult.Cancel:
    print "Script execution cancelled by user..."
    sys.exit(0)
else:
    raise IOError("Selected dose type not supported.")

# Assert
assert dose_type in SUPPORTED_DOSE_TYPES
assert selected_dose_unit in SUPPORTED_DOSE_UNITS
assert selected_volume_unit in SUPPORTED_VOLUME_UNITS

# Converts cc unit if needed
def unit_to_string(unit):
    assert unit in SUPPORTED_VOLUME_UNITS.union(SUPPORTED_DOSE_UNITS)
    if unit == VOLUME_CC:
        return r'cc'
    else:
        return unit

# Utility function to create 2-dimensional array
def create_array(m, n):
  dims = System.Array.CreateInstance(System.Int32, 2)
  dims[0] = m
  dims[1] = n
  return System.Array.CreateInstance(System.Object, dims)

# Check that needed data is available
if dose_type == PLAN_DOSE:
    if (plan.TreatmentCourse == None or plan.TreatmentCourse.TotalDose == None or plan.TreatmentCourse.TotalDose.DoseValues == None):
        raise IOError('There is no plan dose.')
elif dose_type == BEAM_SET_DOSE:
    try:
        beamset = plan.BeamSets[beam_set_name]
    except SystemError:
        raise IOError('The beam set dose not exist.')

    if beamset.FractionDose == None or beamset.FractionDose.DoseValues == None:
        raise IOError('There is no beam set dose.')

    if beamset.FractionationPattern == None or beamset.FractionationPattern.NumberOfFractions == None:
        raise IOError('Unknown number of fractions')
else:
    raise IOError('Dose type not supported.')

# Define dose distribution
if dose_type == PLAN_DOSE:
    dose_distribution = plan.TreatmentCourse.TotalDose
else:
    beamset = plan.BeamSets[beam_set_name]
    nrOfFractions = beamset.FractionationPattern.NumberOfFractions
    dose_distribution = beamset.FractionDose

# Get rois
rois = []
IGNORED_ROI_TYPES = set(["Bolus", "Fixation", "Support"])
if exclude_external:
    IGNORED_ROI_TYPES.add("External")

for roi in case.PatientModel.RegionsOfInterest:
    if dose_distribution.GetDoseGridRoi(RoiName = roi.Name) != None and roi.Type not in IGNORED_ROI_TYPES:
        rois.append(roi)

if rois.Count < 1:
  raise IOError('There are no ROIs with dose grid representation.')

# Define relative volumes
n = 100
relVolumes = [max(0.0,(x+0.5)) / n for x in range(-1, n)]
relVolumes.append(1.0)

# Get doses at relative volumes
m = relVolumes.Count + 2
n = rois.Count + 1
arr = System.Array.CreateInstance(System.Array, rois.Count)

for j, roi in enumerate(rois):
    arr[j] = create_array(m,2)
    # dose
    doseAtRelVol = dose_distribution.GetDoseAtRelativeVolumes(RoiName = roi.Name, RelativeVolumes = relVolumes)
    arr[j][0, 1] = "{0}: Dose [{1}]".format(roi.Name, unit_to_string(selected_dose_unit))
    arr[j][m-1, 1] = 0.0
    for i, dose in enumerate(doseAtRelVol):
        if dose_type == BEAM_SET_DOSE:
            dose *= nrOfFractions
        if selected_dose_unit == GY:
            dose /= 100.0
        arr[j][i+1, 1] = dose
    # volumes
    arr[j][0, 0] = '{0}: Vol. [{1}]'.format(roi.Name, unit_to_string(selected_volume_unit))

    volume_scaler = 100.0
    if selected_volume_unit == VOLUME_CC:
        volume_scaler = dose_distribution.GetDoseGridRoi(RoiName = roi.Name).RoiVolumeDistribution.TotalVolume
    arr[j][m-1, 0] = volume_scaler
    for i, value in enumerate(relVolumes):
        arr[j][i + 1, 0] = volume_scaler * value

try:
    # Open Excel with new worksheet
    excel = ApplicationClass(Visible=True)
    workbook = excel.Workbooks.Add(XlWBATemplate.xlWBATWorksheet)
    worksheet = workbook.Worksheets[1]

    # Populate worksheet
    x0 = 2
    y0 = 2
    nROIs = rois.Count
    for j, roi in enumerate(rois):
        startcell = worksheet.Cells(y0, x0 + j * 3 )
        tablerange = worksheet.Range(startcell, startcell.Cells(m, 2))
        tablerange.Value2 = arr[j]

    # Create a graph object
    chart = worksheet.ChartObjects().Add(10.0, 100.0, 800.0, 500.0).Chart

    # set x- and y-values
    seriesCollection = chart.seriesCollection()
    for j, roi in enumerate(rois):
      s = seriesCollection.NewSeries()
      s.Name = roi.Name
      cell = worksheet.Cells(y0 + 1, 4 + j)
      yValues = worksheet.Range(worksheet.Cells(y0 + 1, x0 + j * 3), worksheet.Cells(y0 + 1 + m, x0 + j * 3))
      xValues = worksheet.Range(worksheet.Cells(y0 + 1, x0 + j * 3 + 1), worksheet.Cells(y0 + 1 + m, x0 + j * 3 + 1))
      s.XValues = xValues
      s.Values = yValues

    # plot
    chart.ChartType = XlChartType.xlXYScatterLinesNoMarkers
    title = "DVH"

    valueTitle = "Volume [{0}]".format(unit_to_string(selected_volume_unit))
    patient_info = " \n \n  Patient name: {0}, Date of birth: {1}, ID: {2}".format(patient.PatientName, patient.DateOfBirth, patient.PatientID)
    if dose_type == PLAN_DOSE:
        categoryTitle = "Plan dose: {0} [{1}] {2}".format(plan.Name, unit_to_string(selected_dose_unit), patient_info)
    elif dose_type == BEAM_SET_DOSE:
        categoryTitle = "Beam set dose: {0} ({1}) [{2}] {3}".format(beam_set_name, plan.Name, unit_to_string(selected_dose_unit), patient_info)
    chart.ChartWizard(Title = title, ValueTitle = valueTitle, CategoryTitle = categoryTitle)

finally:
    # The following is needed for the excel process to die when user closes worksheet
    System.Runtime.InteropServices.Marshal.FinalReleaseComObject(seriesCollection)
    System.Runtime.InteropServices.Marshal.FinalReleaseComObject(chart)
    System.Runtime.InteropServices.Marshal.FinalReleaseComObject(worksheet)
    System.Runtime.InteropServices.Marshal.FinalReleaseComObject(workbook)
    System.Runtime.InteropServices.Marshal.FinalReleaseComObject(excel)
    seriesCollection = None
    chart = None
    worksheet = None
    workbook = None
    excel = None
    System.GC.WaitForPendingFinalizers()
    System.GC.Collect()







