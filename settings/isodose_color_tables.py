# encoding: utf8

# Import the System.Drawing namespace:
import clr
clr.AddReference('System.Drawing')
import System.Drawing

# Import local files:
import colors as COLORS


# Defines an isodose object (which contains a percentage value and a visualization color).
class Isodose(object):

    def __init__(self, percent, color):
      self.percent = percent
      self.color = color


# Defines a color table object (which contains a list of isodoses).
class ColorTable(object):

    def __init__(self, isodoses):
      self.isodoses = isodoses
    
    # Applies this color table object to the given case.
    def apply_to(self, case):
      # Extract the color table:
      dct = case.CaseSettings.DoseColorMap.ColorTable
      # Remove all existing dose lines:
      dct.Clear()
      # Set the dose lines of this color table object:
      for isodose in self.isodoses:
      	dct.Add(isodose.percent, isodose.color)
      # Set the color table:
      case.CaseSettings.DoseColorMap.ColorTable = dct


# Colors used for isodose lines:
grey = System.Drawing.Color.FromArgb(255,64,128,128)
sea_green = System.Drawing.Color.FromArgb(255,64,128,128)
white = System.Drawing.Color.FromArgb(255,255,255,255)
blue =  System.Drawing.Color.FromArgb(255,0,0,160)
green = System.Drawing.Color.FromArgb(255,0,255,0)
yellow = System.Drawing.Color.FromArgb(255,255,255,0)
orange = System.Drawing.Color.FromArgb(255,255,128,0)
red = System.Drawing.Color.FromArgb(255,160,0,0)
blue_mid =  System.Drawing.Color.FromArgb(255,0,128,255)
green_low = System.Drawing.Color.FromArgb(255,128,255,128)
yellow_low = System.Drawing.Color.FromArgb(255,255,255,128)
green_mid = System.Drawing.Color.FromArgb(255,0,255,128)
purple = System.Drawing.Color.FromArgb(255,128,0,255)
pink = System.Drawing.Color.FromArgb(255,192,0,192)
purple_low = System.Drawing.Color.FromArgb(255,128,128,255)


# The standard isodose setup:
standard_isodoses = []
standard_isodoses.append(Isodose(30, sea_green))
standard_isodoses.append(Isodose(50, white))
standard_isodoses.append(Isodose(90, blue))
standard_isodoses.append(Isodose(95, green))
standard_isodoses.append(Isodose(100, yellow))
standard_isodoses.append(Isodose(105, orange))
standard_isodoses.append(Isodose(110, red))


# Prostate SIB 56/70/77 isodose setup:
prostate_56_70_77_isodoses = []
prostate_56_70_77_isodoses.append(Isodose(30, sea_green))
prostate_56_70_77_isodoses.append(Isodose(50, white))
prostate_56_70_77_isodoses.append(Isodose(65, blue))
prostate_56_70_77_isodoses.append(Isodose(69, green_low))
prostate_56_70_77_isodoses.append(Isodose(72.72, yellow_low))
prostate_56_70_77_isodoses.append(Isodose(86.36, green_mid))
prostate_56_70_77_isodoses.append(Isodose(90.09, yellow_low))
prostate_56_70_77_isodoses.append(Isodose(95, green))
prostate_56_70_77_isodoses.append(Isodose(100, yellow))
prostate_56_70_77_isodoses.append(Isodose(105, orange))


# Prostate SIB 70/77 isodose setup:
prostate_70_77_isodoses = []
prostate_70_77_isodoses.append(Isodose(45.45, sea_green))
prostate_70_77_isodoses.append(Isodose(63.63, grey))
prostate_70_77_isodoses.append(Isodose(77.92, white))
prostate_70_77_isodoses.append(Isodose(81.81, blue_mid))
prostate_70_77_isodoses.append(Isodose(86.36, green_mid))
prostate_70_77_isodoses.append(Isodose(90.09, yellow_low))
prostate_70_77_isodoses.append(Isodose(95, green))
prostate_70_77_isodoses.append(Isodose(100, yellow))
prostate_70_77_isodoses.append(Isodose(105, orange))


# Prostate SIB 57/60 isodose setup:
prostate_57_60_isodoses = []
prostate_57_60_isodoses.append(Isodose(30, sea_green))
prostate_57_60_isodoses.append(Isodose(70, grey))
prostate_57_60_isodoses.append(Isodose(85, white))
prostate_57_60_isodoses.append(Isodose(90.25, green_mid))
prostate_57_60_isodoses.append(Isodose(95, green))
prostate_57_60_isodoses.append(Isodose(100, yellow))
prostate_57_60_isodoses.append(Isodose(105, orange))


# Prostate bed SIB 56/70 isodose setup:
prostate_bed_56_70_isodoses = []
prostate_bed_56_70_isodoses.append(Isodose(30, sea_green))
prostate_bed_56_70_isodoses.append(Isodose(50, white))
prostate_bed_56_70_isodoses.append(Isodose(72, blue))
prostate_bed_56_70_isodoses.append(Isodose(76, green_mid))
prostate_bed_56_70_isodoses.append(Isodose(80, yellow_low))
prostate_bed_56_70_isodoses.append(Isodose(85.7142, grey))
prostate_bed_56_70_isodoses.append(Isodose(95, green))
prostate_bed_56_70_isodoses.append(Isodose(100, yellow))
prostate_bed_56_70_isodoses.append(Isodose(104.935, orange))


# SIB 47/50 isodose setup:
sib_47_50_isodoses = []
sib_47_50_isodoses.append(Isodose(30, sea_green))
sib_47_50_isodoses.append(Isodose(50, white))
sib_47_50_isodoses.append(Isodose(84.6, blue))
sib_47_50_isodoses.append(Isodose(89, green_mid))
sib_47_50_isodoses.append(Isodose(95, green))
sib_47_50_isodoses.append(Isodose(100, yellow))
sib_47_50_isodoses.append(Isodose(105, orange))
sib_47_50_isodoses.append(Isodose(110, red))


# SBRT isodose setup:
stereotactic_isodoses = []
stereotactic_isodoses.append(Isodose(30, sea_green))
stereotactic_isodoses.append(Isodose(50, white))
stereotactic_isodoses.append(Isodose(90, blue))
stereotactic_isodoses.append(Isodose(95, green))
stereotactic_isodoses.append(Isodose(100, yellow))
stereotactic_isodoses.append(Isodose(105, orange))
stereotactic_isodoses.append(Isodose(120, pink))
stereotactic_isodoses.append(Isodose(130, purple_low))
stereotactic_isodoses.append(Isodose(150, red))
stereotactic_isodoses.append(Isodose(170, purple))


# Set up the color tables to be used:
standard = ColorTable(standard_isodoses)
prostate_56_70_77 = ColorTable(prostate_56_70_77_isodoses)
prostate_70_77 = ColorTable(prostate_70_77_isodoses)
prostate_57_60 = ColorTable(prostate_57_60_isodoses)
sib_47_50 = ColorTable(sib_47_50_isodoses)
prostate_bed_56_70 = ColorTable(prostate_bed_56_70_isodoses)
stereotactic = ColorTable(stereotactic_isodoses)
