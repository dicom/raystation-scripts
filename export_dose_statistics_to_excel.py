# encoding: utf8

# Example script that shows how to write dose statistics to an Excel file
# Set the parameter 'file_path' to the location where the generated Excel file should be saved,
# or set 'file_path' to None if the file should not be saved automatically
# Set the parameter 'close_excel' to True if the Excel application should be closed when the file is finished
# The Excel application will not be closed if the file is not saved, regardless of the value of 'close_excel'
#
# Source:
# https://github.com/raysearchlabs/scripting
#
# Updated for RayStation 5.0: Christoffer Lervåg - 27.09.2016
# Tested for RayStation version: 9A

import clr, sys
import System.Array
from connect import *

clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")

import Microsoft.Office.Interop.Excel as interop_excel

# Utility function to create 2-dimensional array
def create_array(m, n):
    dims = System.Array.CreateInstance(System.Int32, 2)
    dims[0] = m
    dims[1] = n
    return System.Array.CreateInstance(System.Object, dims)

# Select path where the Excel file should be saved
# Set file_path = None if the file should not be automatically saved
file_path = None

# Should the Excel file be closed after it is created?
# If no file path is selected, the Excel application will not be closed
close_excel = True

try:
    patient = get_current('Patient')
    case = get_current('Case')
    plan = get_current('Plan')
except:
    print 'Patient and plan has to be loaded. Exiting script.'
    sys.exit()

plan_dose = plan.TreatmentCourse.TotalDose

# Find all visible ROIs with defined geometry in the current plan
structure_set = plan.GetStructureSet()
hidden_names = case.CaseSettings.HiddenRegionsOfInterest.Keys
roi_names = [r.OfRoi.Name for r in structure_set.RoiGeometries if r.PrimaryShape != None
             and r.OfRoi.Name not in hidden_names]

# Create an Excel file
try:
    # Open Excel with new worksheet
    excel = interop_excel.ApplicationClass(Visible=True)
    workbook = excel.Workbooks.Add(interop_excel.XlWBATemplate.xlWBATWorksheet)
    worksheet = workbook.Worksheets[1]

    # Set up header row
    # Edit this if other dose statistics are desired
    header_row = create_array(1,9)
    header_row[0,0] = 'ROI'
    header_row[0,1] = 'Volume [cc]'
    header_row[0,2] = 'D99 [cGy]'
    header_row[0,3] = 'D98 [cGy]'
    header_row[0,4] = 'D95 [cGy]'
    header_row[0,5] = 'Average [cGy]'
    header_row[0,6] = 'D50 [cGy]'
    header_row[0,7] = 'D2 [cGy]'
    header_row[0,8] = 'D1 [cGy]'

    # Add header row to work sheet
    startcell = worksheet.Cells(1, 1)
    header_range = worksheet.Range(startcell, startcell.Cells(header_row.GetLength(0), header_row.GetLength(1)))
    header_range.Value2 = header_row

    # Create data array to hold ROI data
    data_array = create_array(len(roi_names),9)

    # Add data for each ROI
    for idx, roi in enumerate(roi_names):
        # Edit this if other dose statistics are desired
        volume = plan_dose.GetDoseGridRoi(RoiName=roi).RoiVolumeDistribution.TotalVolume
        d99, d98, d95, d50, d2, d1 = plan_dose.GetDoseAtRelativeVolumes(RoiName=roi, RelativeVolumes=[.99,.98,.95,.5,.02,.01])
        average = plan_dose.GetDoseStatistic(RoiName=roi, DoseType='Average')
        data_array[idx,0] = roi
        data_array[idx,1] = volume
        data_array[idx,2] = d99
        data_array[idx,3] = d98
        data_array[idx,4] = d95
        data_array[idx,5] = average
        data_array[idx,6] = d50
        data_array[idx,7] = d2
        data_array[idx,8] = d1

    # Add ROI data array to work sheet
    startcell = worksheet.Cells(2,1)
    data_range = worksheet.Range(startcell, startcell.Cells(data_array.GetLength(0), data_array.GetLength(1)))
    data_range.Value2 = data_array

    # Auto-fit the width of all columns
    worksheet.Columns.AutoFit()

    if file_path != None:
        # File name is PatientNamePlanNameDoseStatistics
        # Edit this if another file name is desired
        filename = r"{0}\{1}{2}DoseStatistics.xlsx".format(file_path, patient.PatientName, plan.Name)
        excel.DisplayAlerts = False
        workbook.SaveAs(filename)
finally:
    # The following is needed for the excel process to die when user closes worksheet
    if file_path != None and close_excel:
        excel.Quit()
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
