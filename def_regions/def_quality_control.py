# encoding: utf8

# Used for GUI:
from tkinter import *
from tkinter import messagebox

# Import local files:


# Quality control of examination slice thickness.
def test_slice_thickness(examination, expected_thickness, description):
  image_stack = examination.Series[0].ImageStack
  if len(image_stack.SlicePositions) > 1:
    actual_thickness = round(abs(image_stack.SlicePositions[1] - image_stack.SlicePositions[0]), 1)
    if actual_thickness != round(expected_thickness, 1):
      # Display warning of slice thickness mismatch:
      root = Tk()
      root.withdraw()
      title = "Test av snitt-tykkelse"
      text = "Case: " + description + "\n\n" + "Forventet snitt-tykkelse: " + str(expected_thickness) + " cm\n\n" + "I denne CT-serien er det benyttet " + str(actual_thickness) + " cm!"
      messagebox.showinfo(title, text)
      root.destroy()
