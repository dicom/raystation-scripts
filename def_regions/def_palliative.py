# encoding: utf8

# Import local files:
import colors as COLORS
import def_oars as DEF
import margins as MARGINS
import roi as ROI
import rois as ROIS

# Definitions script for palliative treatments (prostate/prostate bed, with or without lymph nodes, normo/hypofractionated).
class DefPalliative(object):

  # Adds target and OAR ROIs to the given site and creates them in RayStation.
  def __init__(self, pm, examination, ss, choices, site):
    # Choice 1: Stereotactic or not?
    stereotactic = choices[1]
    # Choice 2: Region
    region = choices[2]
    if stereotactic == 'yes':
      # Stereotactic:
      if region in ['col thorax', 'col pelvis']:
        # Targets:
        ctv = ROI.ROIExpanded(ROIS.ctv.name, ROIS.ctv.type, COLORS.ctv_med, ROIS.gtv, margins = MARGINS.uniform_3mm_expansion)
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ctv], sourcesB=[ROIS.vb])
        ptv_gtv = ROI.ROIAlgebra(ROIS.ptv_gtv.name, ROIS.ptv_gtv.type, COLORS.ptv_med, sourcesA = [ptv], sourcesB = [ROIS.gtv], operator='Subtraction')
        ptv_spinal = ROI.ROIAlgebra(ROIS.ptv_spinal.name, ROIS.ptv_spinal.type, COLORS.ptv_med, sourcesA = [ptv], sourcesB = [ROIS.spinal_cord_prv], operator='Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_1mm_expansion)
        site.add_targets([ROIS.gtv, ROIS.vb, ptv_gtv, ptv_spinal, ctv, ptv])
        # OARs:
        if region == 'col thorax':
          site.add_oars(DEF.palliative_stereotactic_thorax_oars)
        elif region == 'col pelvis':
          site.add_oars(DEF.palliative_stereotactic_spine_pelvis_oars)
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        site.add_oars([ROIS.spinal_cord_prv, wall_ptv])
      else:
        # Non-columna SBRT (assumed pelvis):
        # Targets:
        ptv = ROI.ROIExpanded(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, ROIS.gtv, margins = MARGINS.uniform_3mm_expansion)
        site.add_targets([ROIS.gtv, ptv])
        # OARs:
        wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
        site.add_oars(DEF.palliative_stereotactic_pelvis_oars + [wall_ptv])   
    else:
      # Non-stereotactic:
      wall_ptv = ROI.ROIWall(ROIS.wall_ptv.name, ROIS.wall_ptv.type, COLORS.wall, ptv, 1, 0)
      # Region:
      if region == 'head':
        site.add_oars(DEF.palliative_head_oars, wall_ptv)
      elif region == 'neck':
        site.add_oars(DEF.palliative_neck_oars, wall_ptv)
      elif region == 'thorax':
        site.add_oars(DEF.palliative_thorax_oars, wall_ptv)
      elif region == 'costa':
        site.add_oars(DEF.palliative_thorax_abdomen_oars, wall_ptv)
      elif region == 'thorax_abdomen':
        site.add_oars(DEF.palliative_thorax_abdomen_oars, wall_ptv)
      elif region == 'abdomen':
        site.add_oars(DEF.palliative_abdomen_oars, wall_ptv)
      elif region == 'abdomen_pelvis':
        site.add_oars(DEF.palliative_abdomen_pelvis_oars, wall_ptv)
      elif region == 'pelvis':
        site.add_oars(DEF.palliative_pelvis_oars, wall_ptv)
      # Choice 3: Number of targets:
      nr_targets = int(choices[3])
      # Choice 4: GTV included?
      with_gtv = choices[4]
      # Determine PTV margins:
      if with_gtv == 'with':
        # Soft tissue target:
        if region in ['head']:
          # Head: 3 mm
          ptv_margin = MARGINS.uniform_3mm_expansion
        elif region in ['neck']:
          # Neck: 3 mm (mask) or 5 mm (no mask)
          # Choice 5: Mask?
          mask = choices[5]
          if mask == 'mask':
            ptv_margin = MARGINS.uniform_3mm_expansion
          else:
            ptv_margin = MARGINS.uniform_5mm_expansion
        elif region in ['thorax_abdomen']:
          # Near lung (affected by breathing motion):
          ptv_margin = MARGINS.abdomen_near_lung_soft_tissue_expansion
        else:
          # All others: 7 mm
          ptv_margin = MARGINS.uniform_7mm_expansion
      else:
        # Bone target:
        if region in ['head']:
          # Head: 3 mm
          ptv_margin = MARGINS.uniform_3mm_expansion
        elif region in ['neck']:
          # Neck: 3 mm (mask) or 5 mm (no mask)
          # Choice 5: Mask?
          mask = choices[5]
          if mask == 'mask':
            ptv_margin = MARGINS.uniform_3mm_expansion
          else:
            ptv_margin = MARGINS.uniform_5mm_expansion
        elif region in ['costa', 'other']:
          # Costa/Extremities: 7 mm
          ptv_margin = MARGINS.uniform_7mm_expansion
        else:
          # Other torso: 5 mm
          ptv_margin = MARGINS.uniform_5mm_expansion
      # Set up target volumes:
      if nr_targets == 1:
        # A single target:
        if with_gtv == 'with':
          site.add_targets([ROIS.gtv, ROIS.ctv_ext])
        else:
          site.add_targets([ROIS.ctv_underived])
        site.add_targets([ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ROIS.ctv], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction)])
      else:
        # Multiple targets (2 or 3):
        gtvs = []
        ctvs = []
        ptvs = []
        if with_gtv=='with':
          # With GTV:
          for i in range(0, nr_targets):
            gtvs.append(ROI.ROI('GTV'+str(i+1), 'Gtv', COLORS.gtv))
            ctvs.append(ROI.ROIAlgebra(ROIS.ctv.name+str(i+1), ROIS.ctv1.type, ROIS.ctv.color, sourcesA = [gtvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction))
            ptvs.append(ROI.ROIAlgebra(ROIS.ptv.name+str(i+1), ROIS.ptv1.type, ROIS.ptv.color, sourcesA = [ctvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction))
          # GTV union target volume:
          gtvs.append(ROI.ROIAlgebra(ROIS.gtv.name, ROIS.gtv.type, ROIS.gtv.color, sourcesA=[gtvs[0]], sourcesB=gtvs[1:]))
          site.add_targets(gtvs)
        else:
          # Without GTV:
          for i in range(0, nr_targets):
            ctvs.append(ROI.ROI('CTV'+str(i+1), 'Ctv', COLORS.ctv))
            ptvs.append(ROI.ROIAlgebra(ROIS.ptv.name+str(i+1), ROIS.ptv.type, ROIS.ptv.color, sourcesA = [ctvs[-1]], sourcesB = [ROIS.external], operator = 'Intersection', marginsA = ptv_margin, marginsB = MARGINS.uniform_5mm_contraction))
        # Union target volumes:
        ctv = ROI.ROIAlgebra(ROIS.ctv.name, ROIS.ctv.type, ROIS.ctv.color, sourcesA=[ctvs[0]], sourcesB=ctvs[1:])
        ptv = ROI.ROIAlgebra(ROIS.ptv.name, ROIS.ptv.type, ROIS.ptv.color, sourcesA=[ptvs[0]], sourcesB=ptvs[1:])
        ctvs.append(ctv)
        ptvs.append(ptv)
        site.add_targets(ctvs + ptvs)
    # Create all targets and OARs in RayStation:
    site.create_rois()
