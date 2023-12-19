# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import def_quality_control as DEFQC
import margins as MARGINS
import patient_model_functions as PMF
import roi as ROI
import rois as ROIS

# Definitions script for lung treatments (palliative, curative and stereotactiv).
class DefLung(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Add ROIs which are common for all cases:
    self.add_common_rois(pm, examination, site)
    # Choice 1: Intent (curative or palliative)
    intent = choices[1]
    if intent == 'curative':
      # Curative:
      # Choice 2: Diagnosis
      diagnosis = choices[2]
      if diagnosis == '4dct':
        # Curative (with 4DCT or DIBH):
        self.add_curative_4dct_dibh(pm, examination, site)
      elif diagnosis == 'freebreath':
        # Curative (free breath):
        self.add_curative_free_breath(pm, examination, site)
      elif diagnosis =='postop':
        # Curative post operative:
        self.add_curative_postop(pm, examination, site)
    elif intent == 'palliative':
      # Palliative:
      # Choice 2: 4DCT - with or without?
      with_4dct = choices[2]
      if with_4dct == 'with':
        # Palliative 4DCT:
        self.add_palliative_4dct(pm, examination, site)
      else:
        # Palliative free breathing:
        self.add_palliative_free_breath(pm, examination, site)
    elif intent == 'stereotactic':
      # Choice 2: Side - left or right?
      side = choices[2]
      # Choice 3: Number of target volumes?
      nr_targets = int(choices[3])
      # Stereotactic:
      self.add_stereotactic_lung(pm, examination, site, side, nr_targets)
    # Create all targets and OARs in RayStation:
    site.create_rois()


  # Adds rois that are common across all cases.
  def add_common_rois(self, pm, examination, site):
    # DL OARs:
    examination.RunOarSegmentation(ModelName="RSL Thorax-Abdomen CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["A_LAD", "Esophagus", "Heart", "Kidney_L", "Kidney_R", "Liver", "Pancreas", "SpinalCanal", "Spleen", "Sternum", "Stomach", "ThyroidGland", "Trachea"])
    # Use our own breast model for the lungs (because these seems to be sub optimal in the RSL Thorax model):
    examination.RunOarSegmentation(ModelName="St. Olavs-Alesund Breast CT", ExaminationsAndRegistrations={ examination.Name: None }, RoisToInclude=["Lung_L", "Lung_R"])
    # Non-DL OARs:
    site.add_oars([ROIS.lungs])
  
  
  # Adds curative 4DCT/DIBH ROIs to the site object.
  def add_curative_4dct_dibh(self, pm, examination, site):
    # Targets:
    igtv = ROI.ROIAlgebra(ROIS.igtv.name, ROIS.igtv.type, ROIS.gtv.color, sourcesA=[ROIS.igtv_p], sourcesB=[ROIS.igtv_n])
    ictv_p = ROI.ROIExpanded(ROIS.ictv_p.name, ROIS.ictv_p.type, COLORS.ctv_high, source = ROIS.igtv_p, margins = MARGINS.uniform_5mm_expansion)
    ictv_n = ROI.ROIExpanded(ROIS.ictv_n.name, ROIS.ictv_n.type, COLORS.ctv_high, source = ROIS.igtv_n, margins = MARGINS.uniform_5mm_expansion)
    ictv = ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color, sourcesA=[ictv_p, ictv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high, sourcesA = [ictv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.igtv_p, ROIS.igtv_n, igtv, ictv_p, ictv_n, ictv, ptv])
    # Other derived ROIs:
    lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [igtv], operator='Subtraction')
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[igtv], operator='Subtraction', operatorA = 'Intersection')
    site.add_oars([lungs_igtv, water])
    self.add_ptv_derived_rois(pm, examination, site, ptv)
  
  
  # Adds curative free breathing ROIs to the site object.
  def add_curative_free_breath(self, pm, examination, site):
    # Targets:
    gtv = ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[ROIS.gtv_p], sourcesB=[ROIS.gtv_n])
    ctv_p = ROI.ROIExpanded(ROIS.ctv_p.name, ROIS.ctv_p.type, COLORS.ctv_high, source = ROIS.gtv_p, margins = MARGINS.uniform_5mm_expansion)
    ctv_n = ROI.ROIExpanded(ROIS.ctv_n.name, ROIS.ctv_n.type, COLORS.ctv_high, source = ROIS.gtv_n, margins = MARGINS.uniform_5mm_expansion)
    ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ctv_p, ctv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high, sourcesA = [ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.gtv_p, ROIS.gtv_n, gtv, ctv_p, ctv_n, ctv, ptv])
    # Other derived ROIs:
    lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_gtv.name, ROIS.lungs_gtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [gtv], operator='Subtraction')
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[gtv], operator='Subtraction', operatorA = 'Intersection')
    site.add_oars([lungs_gtv, water])
    self.add_ptv_derived_rois(pm, examination, site, ptv)
  
  
  # Adds curative post-operative ROIs to the site object.
  def add_curative_postop(self, pm, examination, site):
    # Targets:
    ctv = ROI.ROI(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ctv, ptv])
    # Other derived ROIs:
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ctv], operator='Subtraction', operatorA = 'Intersection')
    site.add_oars([water])
    self.add_ptv_derived_rois(pm, examination, site, ptv)
  
  
  # Adds palliative 4DCT ROIs to the site object.
  def add_palliative_4dct(self, pm, examination, site):
    # Targets:
    ictv = ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color, sourcesA=[ROIS.igtv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ictv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.igtv, ictv, ptv])
    # Other derived ROIs:
    lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [ROIS.igtv], operator='Subtraction')
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ROIS.igtv], operator='Subtraction', operatorA = 'Intersection')
    site.add_oars([lungs_gtv, water])
    self.add_ptv_derived_rois(pm, examination, site, ptv)
  
  
  # Adds palliative free breathing ROIs to the site object.
  def add_palliative_free_breath(self, pm, examination, site):
    # Targets:
    ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ROIS.gtv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
    site.add_targets([ROIS.gtv, ctv, ptv])
    # Other derived ROIs:
    lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_gtv.name, ROIS.lungs_gtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [ROIS.gtv], operator='Subtraction')
    water = ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ROIS.gtv], operator='Subtraction', operatorA = 'Intersection')
    site.add_oars([lungs_gtv, water])
    self.add_ptv_derived_rois(pm, examination, site, ptv)
  
  
  # Adds ROIs derived by the PTV to the site object.
  def add_ptv_derived_rois(self, pm, examination, site, ptv):
    # Common for all palliative cases:
    heart_ptv = ROI.ROIAlgebra(ROIS.z_heart.name, ROIS.z_heart.type, COLORS.heart, sourcesA = [ROIS.heart], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    esophagus_ptv = ROI.ROIAlgebra(ROIS.z_esophagus.name, ROIS.z_esophagus.type, COLORS.esophagus, sourcesA = [ROIS.esophagus], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
    site.add_oars([heart_ptv, esophagus_ptv])
  
  
  # Adds stereotactic lung ROIs to the site object.
  def add_stereotactic_lung(self, pm, examination, site, side, nr_targets):
    # Slice thickness quality control:
    DEFQC.test_slice_thickness(examination, 0.2, "Lunge SBRT")
    # Add a POI for breath hold measurement:
    PMF.create_poi(pm, examination, 'Pust', 'Marker', 'Magenta')
    # Non-DL OARs:
    site.add_oars(DEF.lung_stereotactic_oars)
    # Side dependent OARs:
    if side == 'right':
      site.add_oars([ROIS.rib_x_r, ROIS.rib_y_r, ROIS.ribs_r])
    elif side == 'left':
      site.add_oars([ROIS.rib_x_l, ROIS.rib_y_l, ROIS.ribs_l])
    # Targets:
    if nr_targets == 1:
      # Single target:
      site.add_targets([ROIS.igtv, ROIS.iptv_gtv, ROIS.wall_ptv])
      site.add_oars([ROIS.lungs_igtv])
    else:
      # Multiple targets:
      igtvs = []
      ptvs = []
      walls = []
      for i in range(0, nr_targets):
        # Targets:
        igtvs.append(ROI.ROI('IGTV'+str(i+1), 'Gtv', ROIS.igtv.color))
        ptvs.append(ROI.ROIExpanded(ROIS.ptv.name+str(i+1), ROIS.ptv.type, COLORS.ptv, igtvs[-1], margins = MARGINS.uniform_5mm_expansion))
        # Other derived ROIs:
        walls.append(ROI.ROIWall("zPTV"+str(i+1)+"_Wall", ROIS.z_ptv_wall.type, COLORS.wall, ptvs[-1], 1, 0))
      # Union target volumes:
      igtv = ROI.ROIAlgebra(ROIS.igtv.name, ROIS.igtv.type, ROIS.igtv.color, sourcesA=[igtvs[0]], sourcesB=igtvs[1:])
      ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptvs[0]], sourcesB=ptvs[1:])
      igtvs.append(igtv)
      ptvs.append(ptv)
      # Targets:
      site.add_targets(igtvs + ptvs)
      # Other derived ROIs:
      lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, 'Organ', COLORS.lungs, sourcesA=[ROIS.lungs], sourcesB=[igtv], operator = 'Subtraction')
      site.add_oars([lungs_igtv] + walls)
    