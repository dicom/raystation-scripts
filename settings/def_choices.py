# encoding: utf8

# Import local files:
import property as P

# Regions:
brain = P.Property('Hjerne', 'brain', next_category='omfang', default = True)
lung = P.Property('Lunge', 'lung', next_category = 'intensjon')
breast = P.Property('Bryst', 'breast', next_category = 'omfang')
bladder = P.Property('Blære', 'bladder')
prostate = P.Property('Prostata', 'prostate', next_category = 'omfang')
rectum = P.Property('Rektum', 'rectum', next_category = 'fraksjonering')
other = P.Property('Palliativ (skjelett og øvrig bløtvev)', 'other', next_category = '')


# Brain: Scope:
brain_whole = P.Property('Hele hjernen', 'whole', parent=brain, default = True)
brain_partial = P.Property('Del av hjerne', 'part', parent=brain)
brain_stereotactic = P.Property('Stereotaksi','stereotactic', parent = brain, next_category ='antall målvolum')

# Brain: Partial: Diagnosis:
#brain_partial_diag1 = P.Property('Glioblastom WHO grad IV', 'glio', parent=brain_partial, default = True)
#brain_partial_diag2 = P.Property('Anaplastisk astrocytom WHO grad III', 'astro', parent=brain_partial)
#brain_partial_diag3 = P.Property('Atypisk og anaplastisk meningeom', 'meningeom', parent=brain_partial)

# Brain: Stereotactic
brain_stereo_nr1 = P.Property('1','one', parent = brain_stereotactic, default = True)
brain_stereo_nr2 = P.Property('2','two', parent = brain_stereotactic)
brain_stereo_nr3 = P.Property('3','three', parent = brain_stereotactic)
brain_stereo_nr4 = P.Property('4','four', parent = brain_stereotactic)


# Lung
lung_curative = P.Property('Kurativ', 'curative', parent = lung, next_category = 'diagnose', default = True)
lung_palliative = P.Property('Palliativ','palliative', parent = lung, next_category = '')
lung_stereotactic = P.Property('Stereotaksi', 'stereotactic', parent = lung, next_category ='side')

# Lung curative:
lung_nsclc = P.Property('Ikke-småcellet lungekreft/ Småcellet lungekreft (med 4DCT)','4dct', parent = lung_curative, default = True)
lung_sclc = P.Property('Småcellet lungekreft (uten 4DCT)','sclc', parent = lung_curative)
lung_pancoast =P.Property('Pancoast', 'pancoast', parent = lung_curative)
lung_postop =P.Property('Postoperativ', 'postop', parent = lung_curative)

# Lung stereotactic:
stereo_lung_right = P.Property('Høyre','right', parent = lung_stereotactic, next_category ='antall målvolum', default = True)
stereo_lung_left = P.Property('Venstre','left', parent = lung_stereotactic, next_category ='antall målvolum')

for side in [stereo_lung_right, stereo_lung_left]:
  lung_stereo_nr1 = P.Property('1','one', parent = side, default = True)
  lung_stereo_nr2 = P.Property('2','two', parent = side)
  lung_stereo_nr3 = P.Property('3','three', parent = side)


# Lung palliative:
lung_with_4dct = P.Property('Med 4DCT', 'with', parent = lung_palliative, default = True)
lung_without_4dct = P.Property('Uten 4DCT', 'without', parent = lung_palliative)


#Breast:
breast_partial = P.Property('Del av bryst', 'part', parent = breast, next_category = '')
breast_tangential = P.Property('Bryst/brystvegg', 'tang', parent = breast, next_category = '', default = True)
breast_locoregional = P.Property('Bryst/brystvegg og regionale lymfeknuter', 'reg', parent = breast, next_category ='side')
breast_imn = P.Property('Bryst/brystvegg, regionale lymfeknuter og parasternale glandler', 'imn', parent = breast, next_category = 'side')


# Breast tangential: Side:
breast_right_tang = P.Property('Høyre','right', parent = breast_tangential, next_category = '', default = True)
breast_left_tang = P.Property('Venstre','left', parent = breast_tangential, next_category = '')


breast_right_part = P.Property('Høyre','right', parent = breast_partial, default = True)
breast_left_part = P.Property('Venstre','left', parent = breast_partial)


# Breast youth boost:
for side in [breast_right_tang, breast_left_tang]:
  breast_with_boost_tang = P.Property('Med ungdomsboost','with', parent = side)
  breast_without_boost_tang = P.Property('Uten ungdomsboost', 'without', parent = side, default = True)


# Breast regional:
for b in [breast_locoregional, breast_imn]:
  breast_right = P.Property('Høyre','right', parent = b, next_category = '', default = True)
  breast_left = P.Property('Venstre','left', parent = b, next_category = '')
  for side in [breast_right, breast_left]:
    # Breast: Fractionation:
    breast_hypo = P.Property('Hypofraksjonering', 'hypo', parent = side, next_category ='', default = True)
    breast_normo = P.Property('Konvensjonell fraksjonering', 'normo', parent = side, next_category ='')
    # Breast youth boost:
    for frac in [breast_hypo, breast_normo]:
      breast_with_boost = P.Property('Med ungdomsboost','with', parent = frac)
      breast_without_boost = P.Property('Uten ungdomsboost', 'without', parent = frac, default = True)


# Prostate:
prostate_normal = P.Property('Prostata', 'prostate', parent = prostate, next_category ='', default = True)
prostate_bed = P.Property('Prostataseng', 'bed', parent = prostate, next_category ='')

# Prostate: Fractionation:
prostate_hypo = P.Property('Hypofraksjonering (60 Gy)', 'hypo_60', parent = prostate_normal, next_category ='', default = True)
prostate_hypo_55 = P.Property('Hypofraksjonering, med gull (55 Gy)', 'hypo_55', parent = prostate_normal, next_category ='')
prostate_normo = P.Property('Konvensjonell fraksjonering', 'normo', parent = prostate_normal, next_category ='')
prostate_palliative = P.Property('Palliativ fraksjonering, uten gull', 'palliative', parent = prostate_normal, next_category ='')

prostate_bed_normo = P.Property('Konvensjonell fraksjonering', 'normo', parent = prostate_bed, next_category ='', default = True)
prostate_bed_palliative = P.Property('Palliativ fraksjonering', 'palliative', parent = prostate_bed, next_category ='')

# Prosate/bed: Lymph nodes:
for p in [prostate_normo, prostate_bed_normo]:
  prostate_without_ln =  P.Property('Uten lymfeknuter', 'without',  parent = p, next_category ='', default = True)
  prostate_with_ln =  P.Property('Med lymfeknuter', 'with', parent = p, next_category ='')
  prostate_with_ln_boost =  P.Property('Med lymfeknuter og boost til positiv lymfeknute', 'with_node', parent = p, next_category ='')


# Rectum:
rectum_hypo = P.Property('Hypofraksjonering', 'hypo', parent = rectum, next_category ='')
rectum_normo = P.Property('Konvensjonell fraksjonering med SIB', 'normo', parent = rectum, next_category ='omfang', default = True)

# Rectum normo: Nodes:
rectum_with_nodes = P.Property('Med patologisk forstørrede lymfeglandler i lyskene', 'with', parent = rectum_normo)
rectum_without_nodes = P.Property('Uten patologisk forstørrede lymfeglandler i lyskene', 'without', parent = rectum_normo, default = True)


# Other (palliative): SBRT:
other_stereotactic = P.Property('Stereotaksi', 'yes', parent =other, next_category = 'region')
other_non_stereotactic = P.Property('Ikke stereotaksi', 'no', parent = other, next_category = 'region', default = True)

# Other non-SBRT: Region:
other_head = P.Property('Hode', 'head', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_neck = P.Property('Hals', 'neck', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_thorax = P.Property('Thorax', 'thorax', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_thorax_and_abdomen = P.Property('Thorax/Abdomen', 'thorax_abdomen', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_abdomen = P.Property('Abdomen', 'abdomen', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_abdomen_and_pelvis = P.Property('Abdomen/Bekken', 'abdomen_pelvis', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_pelvis = P.Property('Bekken', 'pelvis', parent=other_non_stereotactic, next_category = 'antall målvolum', default = True)
other_other = P.Property('Ekstremiteter/Annet', 'other', parent=other_non_stereotactic, next_category = 'antall målvolum')

# Other SBRT: Region:
other_stereotactic_col_thorax =  P.Property('Columna - thorax', 'col thorax', parent=other_stereotactic)
other_stereotactic_col_pelvis =  P.Property('Columna - bekken', 'col pelvis', parent=other_stereotactic)
other_stereotactic_pelvis  = P.Property('Bekken', 'pelvis', parent=other_stereotactic, default = True)

# Other non-SBRT: Number of target volumes:
for region in [other_head, other_neck, other_thorax, other_thorax_and_abdomen, other_abdomen, other_abdomen_and_pelvis, other_pelvis, other_other]:
  other_target_volume_one = P.Property('1','1', parent = region, next_category = '', default = True)
  other_target_volume_two = P.Property('2','2', parent = region, next_category = '')
  # With or without soft tissue component:
  for tv in [other_target_volume_one, other_target_volume_two]:
    other_with_gtv = P.Property('Bløtvevskomponent (med GTV)', 'with', parent = tv)
    other_without_gtv = P.Property('Skjelett (uten GTV)', 'without', parent = tv, default = True)


# Lists to be used with radiobutton objects:
regions = [brain, lung, breast, bladder, prostate, rectum, other]


# Radiobutton choices for deleting/keeping pre-existing ROIs:
p_delete = P.Property('Slett eksisterende ROIs', 'yes')
p_delete_derived = P.Property('Slett alle bortsett fra inntegnede ROIs','some')
p_not_delete = P.Property('Ikke slett eksisterende ROIs','no', default = True)
delete = [p_delete, p_delete_derived, p_not_delete]
