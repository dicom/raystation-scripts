# Processes ROIs to be used in the Brain Deep Learning project.
# This script is designed to be run after a patient has been imported in the research environment.
# It does the following:
# -Creates new ROIs which are not originally present
# -Renames ROIs which are present, but have a different name than the one decided for the project
# -Deletes ROIs which are not supposed to be included in the project


from connect import *


# Load local files:
sys.path.append("C:\\temp\\raystation-scripts\\functions")
sys.path.append("C:\\temp\\raystation-scripts\\rt_classes")
sys.path.append("C:\\temp\\raystation-scripts\\settings")
sys.path.append("C:\\temp\\raystation-scripts\\def_regions")
sys.path.append("C:\\temp\\raystation-scripts\\gui_classes")
import patient_model_functions as PMF
import structure_set_functions as SSF

# Load the patient case:
try:
  case = get_current('Case')
  examination = get_current('Examination')
except SystemError:
  raise IOError("No case loaded. Load patient and case.")

# The patient model:  
pm = case.PatientModel

# Load structure set:
ss = PMF.get_structure_set(pm, examination)

# Types of ROIs: External, Ptv, Ctv, Bolus, Organ, Marker, Cavity, Support, Fixation, Undefined

# Creates a ROI.
# If the ROI already exists, do not create a duplicate.
# If a ROI with name of known_variants exists, do not create a duplicate,
# but instead rename that variant according to the given name.
def create_roi(name, color, type, alternatives):
  try:
    roi = pm.RegionsOfInterest[name]
  except:
    roi = None
  if not roi:
    variant_roi = False
    for alternative in alternatives:
      try:
        variant_roi = pm.RegionsOfInterest[alternative]
      except:
        pass
    if not variant_roi:
      # Create the ROI:
      roi = pm.CreateRoi(Name = name, Color = color, Type = type)
    else:
      # Process the existing variant ROI:
      variant_roi.Name = name
      variant_roi.Color = color
      variant_roi.Type = type
      roi = variant_roi
  else:
    # The ROI exists with the given name. Make sure it is of correct color and type:
    roi.Color = color
    roi.Type = type
  return roi


# Create ROIs:
# External:
external = create_roi(name = 'External', color = '255, 173, 91', type = 'External', alternatives=[])
body = create_roi(name = 'Body', color = '255, 173, 91', type = 'Undefined', alternatives=[])

# Organs:
create_roi(name = 'Brain', color = 'DarkBlue', type = 'Organ', alternatives=[])
create_roi(name = 'Brainstem', color = 'Indigo', type = 'Organ', alternatives=[])
create_roi(name = 'Cochlea_L', color = 'Violet', type = 'Organ', alternatives=[])
create_roi(name = 'Cochlea_R', color = 'Violet', type = 'Organ', alternatives=[])
create_roi(name = 'Eye_L', color = 'DeepSkyBlue', type = 'Organ', alternatives=[])
create_roi(name = 'Eye_R', color = 'DeepSkyBlue', type = 'Organ', alternatives=[])
create_roi(name = 'Hippocampus_L', color = 'Sienna', type = 'Organ', alternatives=[])
create_roi(name = 'Hippocampus_R', color = 'Sienna', type = 'Organ', alternatives=[])
create_roi(name = 'LacrimalGland_L', color = 'DarkBlue', type = 'Organ', alternatives=[])
create_roi(name = 'LacrimalGland_R', color = 'DarkBlue', type = 'Organ', alternatives=[])
create_roi(name = 'Lens_L', color = 'DarkTurquoise', type = 'Organ', alternatives=[])
create_roi(name = 'Lens_R', color = 'DarkTurquoise', type = 'Organ', alternatives=[])
create_roi(name = 'OpticChiasm', color = 'MidnightBlue', type = 'Organ', alternatives=[])
create_roi(name = 'OpticNerve_L', color = 'SteelBlue', type = 'Organ', alternatives=[])
create_roi(name = 'OpticNerve_R', color = 'SteelBlue', type = 'Organ', alternatives=[])
create_roi(name = 'OralCavity', color = 'Olive', type = 'Organ', alternatives=[])
create_roi(name = 'Parotid_L', color = 'Orange', type = 'Organ', alternatives=[])
create_roi(name = 'Parotid_R', color = 'Orange', type = 'Organ', alternatives=[])
create_roi(name = 'Pituitary', color = 'Orange', type = 'Organ', alternatives=[])
create_roi(name = 'SpinalCanal', color = 'Blue', type = 'Organ', alternatives=[])
create_roi(name = 'SubmandGland_L', color = 'DarkOrange', type = 'Organ', alternatives=[])
create_roi(name = 'SubmandGland_R', color = 'DarkOrange', type = 'Organ', alternatives=[])


# Delete ROI geometries:
for ss in pm.StructureSets:
  for rg in ss.RoiGeometries:
    if rg.OfRoi.Name in ['Hippocampus_L', 'Hippocampus_R']:
      rg.DeleteRoiGeometry()


# Delete ROIs:
# Delete known ROIs which we know we do not want:
delete = [
  '95',
  '105',
  'Artifacts',
  'box',
  'Brain (1)',
  'Brain-GTV',
  'Brain-PTV',
  'Brainstem_maxdose',
  'BrainstemCore',
  'BrainstemSurface',
  'Cranium',
  'CTV',
  'CTV1cm',
  'External-PTV',
  'Fylling Jeksel',
  'Glottis',
  'GTV1+2',
  'GTV1-3',
  'GTV1+3',
  'GTV2+3+4+5',
  'GTV2+4',
  'GTV3+4',
  'GTV4+5',
  'Hippocamous_L',
  'Joint_TM_L',
  'Joint_TM_R',
  'Lips',
  'Mask_PTV',
  'Mask_PTV1',
  'Mask_PTV1+2',
  'Mask_PTV1+3',
  'Mask_PTV2',
  'Mask_PTV2+3',
  'Mask_PTV2+3+4+5',
  'Mask_PTV2+4',
  'Mask_PTV3',
  'Mask_PTV3+4',
  'Mask_PTV4',
  'Mask_PTV5',
  'Mask_PTV6',
  'Mask_PTV7',
  'Mask_PTV15',
  'Mask_PTV16',
  'NeseCavity',
  'NasalCavity',
  'Nasal cavity',
  'Nasolacrimal_Duct_L',
  'Nasolacrimal_Duct_R',
  'opt',
  'Prosthesis',
  'PTV',
  'PTV-Brainstem',
  'PTV cerebellum',
  'PTV1',
  'PTV1-3',
  'PTV1-3-Brainstem',
  'PTV1+2',
  'PTV1+3',
  'PTV2',
  'PTV 2+3',
  'PTV2+3+4+5',
  'PTV2+4',
  'PTV3',
  'PTV3+4',
  'PTV4',
  'PTV4+5',
  'PTV5',
  'PTV6',
  'PTV7',
  'PTV15',
  'PTV16',
  'Skin',
  'Tongue_Base',
  'zPTV_Wall',
  'zPTV_Wall1',
  'zPTV_Wall2',
  'zPTV1_Wall',
  'zPTV1+3_Wall',
  'zPTV1-3_Wall',
  'zPTV2_Wall',
  'zPTV2+4_Wall',
  'zPTV3_Wall',
  'zPTV4_Wall',
  'zPTV3+4_Wall',
  'zPTV4+5_Wall',
  'zPTV2+3+4+5_Wall',
  'zPTV5_Wall',
  'zPTV6_Wall',
  'zPTV7_Wall',
  'zPTV15_Wall',
  'zPTV16_Wall',
]

for name in delete:
  try:
    roi = pm.RegionsOfInterest[name]
    roi.DeleteRoi()
  except:
    pass
