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
    site.add_oars(DEF.lung_oars)
    # Choice 1: Intent (curative or palliative)
    intent = choices[1]
    # Curative:
    if intent == 'curative':
      # Choice 2: Diagnosis
      diagnosis = choices[2]
      # Non small cell lung cancer (with 4DCT) or small cell lung cancer (with 4DCT):
      if diagnosis == '4dct':
        igtv =  ROI.ROIAlgebra(ROIS.igtv.name, ROIS.igtv.type, ROIS.gtv.color, sourcesA=[ROIS.igtv_p], sourcesB=[ROIS.igtv_n])
        ictv_p = ROI.ROIExpanded(ROIS.ictv_p.name, ROIS.ictv_p.type, COLORS.ctv_high, source = ROIS.igtv_p, margins = MARGINS.uniform_10mm_expansion)
        ictv_n = ROI.ROIExpanded(ROIS.ictv_n.name, ROIS.ictv_n.type, COLORS.ctv_high, source = ROIS.igtv_n, margins = MARGINS.uniform_5mm_expansion)
        ictv =  ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color, sourcesA=[ictv_p, ictv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, COLORS.ptv_high, sourcesA = [ictv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [igtv], operator='Subtraction')
        water =  ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[igtv], operator='Subtraction', operatorA = 'Intersection')
        site.add_targets([ROIS.igtv_p, ROIS.igtv_n, igtv, ictv_p, ictv_n, ictv, ptv])
        site.add_oars([lungs_igtv, water])
      # Small cell lung cancer (without 4DCT):
      elif diagnosis == 'sclc':
        ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ROIS.ctv_p, ROIS.ctv_n], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_5mm_contraction)
        ptv_p =  ROI.ROIAlgebra(ROIS.ptv_p.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ROIS.ctv_p], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.lung_sclc_without_4dct, marginsB = MARGINS.uniform_5mm_contraction)
        ptv_n =  ROI.ROIAlgebra(ROIS.ptv_n.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ROIS.ctv_n], sourcesB=[ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv =  ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptv_p], sourcesB=[ptv_n])
        water =  ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ctv], operator='Subtraction', operatorA = 'Intersection')
        site.add_oars([water])
        site.add_targets([ROIS.ctv_p, ROIS.ctv_n, ctv, ptv_p, ptv_n, ptv])
      # Pancoast tumor (with 4DCT):
      elif diagnosis =='pancoast':
        igtv = ROI.ROI(ROIS.igtv.name, ROIS.igtv.type, COLORS.gtv)
        ictv =  ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color, sourcesA=[igtv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv =  ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ictv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [igtv], operator='Subtraction')
        water =  ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[igtv], operator='Subtraction', operatorA = 'Intersection')
        site.add_oars([lungs_igtv, water])
        site.add_targets([igtv, ictv, ptv])
      # Post operative treatment:
      elif diagnosis =='postop':
        ctv = ROI.ROI(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv)
        ptv =  ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        water =  ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ctv], operator='Subtraction', operatorA = 'Intersection')
        site.add_oars([water])
        site.add_targets([ctv, ptv])
      # Common for all curative cases:
      heart_ptv =  ROI.ROIAlgebra(ROIS.z_heart.name, ROIS.z_heart.type, COLORS.heart, sourcesA = [ROIS.heart], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      esophagus_ptv =  ROI.ROIAlgebra(ROIS.z_esophagus.name, ROIS.z_esophagus.type, COLORS.esophagus, sourcesA = [ROIS.esophagus], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      site.add_oars([heart_ptv, esophagus_ptv])
    # Palliative:
    elif intent == 'palliative':
      # Choice 2: 4DCT - with or without?
      # With 4DCT:
      if choices[2]:
        ictv =  ROI.ROIAlgebra(ROIS.ictv.name, ROIS.ictv.type, ROIS.ctv.color, sourcesA=[ROIS.igtv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv =  ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ictv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, ROIS.lungs_igtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [ROIS.igtv], operator='Subtraction')
        water =  ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ROIS.igtv], operator='Subtraction', operatorA = 'Intersection')
        site.add_oars([lungs_gtv, water])
        site.add_targets([ROIS.igtv, ictv, ptv])
      # Without 4DCT:
      else:
        ctv =  ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ROIS.gtv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_5mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        ptv =  ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = MARGINS.uniform_10mm_expansion, marginsB = MARGINS.uniform_5mm_contraction)
        lungs_gtv = ROI.ROIAlgebra(ROIS.lungs_gtv.name, ROIS.lungs_gtv.type, COLORS.lungs, sourcesA = [ROIS.lungs], sourcesB = [ROIS.gtv], operator='Subtraction')
        water =  ROI.ROIAlgebra(ROIS.z_water.name, ROIS.z_water.type, COLORS.other_ptv, sourcesA=[ROIS.lungs, ptv], sourcesB=[ROIS.gtv], operator='Subtraction', operatorA = 'Intersection')
        site.add_oars([lungs_gtv, water])
        site.add_targets([ROIS.gtv, ctv, ptv])
      # Common for all palliative cases:
      heart_ptv =  ROI.ROIAlgebra(ROIS.z_heart.name, ROIS.z_heart.type, COLORS.heart, sourcesA = [ROIS.heart], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      esophagus_ptv =  ROI.ROIAlgebra(ROIS.z_esophagus.name, ROIS.z_esophagus.type, COLORS.esophagus, sourcesA = [ROIS.esophagus], sourcesB = [ptv], operator='Subtraction', marginsB = MARGINS.uniform_3mm_expansion)
      site.add_oars([heart_ptv, esophagus_ptv])
    # Stereotactic treatment:
    elif intent == 'stereotactic':
      # Slice thickness quality control:
      DEFQC.test_slice_thickness(examination, 0.2, "Lunge SBRT")
      # Add a POI for breath hold measurement:
      PMF.create_poi(pm, examination, 'Pust', 'Marker', 'Magenta')
      # Choice 2: Side - left or right?
      side = choices[2]
      if side == 'right':
        site.add_oars([ROIS.rib_x_r, ROIS.rib_y_r, ROIS.ribs_r])
      elif side == 'left':
        site.add_oars([ROIS.rib_x_l, ROIS.rib_y_l, ROIS.ribs_l])
      nr_targets = choices[3]
      # Choice 3: Number of target volumes?
      if nr_targets == 'one':
        site.add_targets([ROIS.igtv, ROIS.ictv, ROIS.iptv, ROIS.wall_ptv])
        site.add_oars([ROIS.lungs_igtv])
      elif nr_targets in ['two', 'three']:
        igtv =  ROI.ROIAlgebra(ROIS.igtv.name, ROIS.igtv.type, ROIS.gtv.color, sourcesA=[ROIS.igtv1], sourcesB=[ROIS.igtv2])
        site.add_targets([ROIS.igtv1, ROIS.igtv2, igtv, ROIS.ictv1, ROIS.ictv2, ROIS.iptv1, ROIS.iptv2, ROIS.wall_ptv1, ROIS.wall_ptv2])
        if nr_targets == 'three':
          igtv.sourcesB.extend([ROIS.igtv3])
          site.add_targets([ROIS.igtv3, ROIS.ictv3, ROIS.iptv3, ROIS.wall_ptv3])
        lungs_igtv = ROI.ROIAlgebra(ROIS.lungs_igtv.name, 'Organ', COLORS.lungs, sourcesA=[ROIS.lungs], sourcesB=[igtv], operator = 'Subtraction')
        site.add_oars([lungs_igtv])
      site.add_oars(DEF.lung_stereotactic_oars)

    # Create all targets and OARs in RayStation:
    site.create_rois()
