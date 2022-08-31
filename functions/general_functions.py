# encoding: utf8

# Import local files:


# Dynamically rounds a float to position of the last non-zero decimal.
# Returns the rounded value as a string.
def dynamic_round(value):
  return str(int(float(value)) if int(float(value)) == float(value) else float(value))
