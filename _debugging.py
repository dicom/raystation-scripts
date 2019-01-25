# Used for GUI debugging:

from connect import *
import clr, sys
import System.Array
clr.AddReference("Office")
clr.AddReference("Microsoft.Office.Interop.Excel")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("PresentationFramework")
from System.Windows import *

text = ""
MessageBox.Show(text, "DEBUG", MessageBoxButton.OK, MessageBoxImage.Information)