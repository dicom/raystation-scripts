# encoding: utf8

# Import local files:
import property as P

# Regions:
brain = P.Property('Hjerne', 'brain', next_category='omfang', default = True)
lung = P.Property('Lunge', 'lung', next_category = 'intensjon')
breast = P.Property('Bryst', 'breast', next_category = 'omfang')
bladder = P.Property('Blære', 'bladder', next_category = 'intensjon')
prostate = P.Property('Prostata', 'prostate', next_category = 'omfang')
rectum = P.Property('Rektum', 'rectum', next_category = 'fraksjonering')
other = P.Property('Skjelett og øvrig bløtvev', 'other', next_category = '')


# Brain: Scope:
brain_whole = P.Property('Hele hjernen', 'whole', parent=brain, next_category ='involvering av hjernehinne', default = True)
brain_partial = P.Property('Del av hjerne', 'part', parent=brain)
brain_stereotactic = P.Property('Stereotaksi','stereotactic', parent = brain, next_category ='antall målvolum')

# Brain: Whole
brain_whole_default = P.Property('Standard total hjerne','no', parent = brain_whole, default = True)
brain_whole_with_margin = P.Property('Metastase i hjernehinne (ekstra margin)','yes', parent = brain_whole)

# Brain: Stereotactic
brain_stereo_nr1 = P.Property('1','1', parent = brain_stereotactic, default = True)
brain_stereo_nr2 = P.Property('2','2', parent = brain_stereotactic)
brain_stereo_nr3 = P.Property('3','3', parent = brain_stereotactic)
brain_stereo_nr4 = P.Property('4','4', parent = brain_stereotactic)


# Lung:
lung_curative = P.Property('Kurativ', 'curative', parent = lung, next_category = 'diagnose', default = True)
lung_palliative = P.Property('Palliativ','palliative', parent = lung, next_category = '')
lung_stereotactic = P.Property('Stereotaksi', 'stereotactic', parent = lung, next_category ='side')

# Lung curative:
lung_4d = P.Property('4DCT / DIBH','4dct', parent = lung_curative, default = True)
lung_free = P.Property('Fripust','freebreath', parent = lung_curative)
lung_postop =P.Property('Postoperativ', 'postop', parent = lung_curative)

# Lung stereotactic:
stereo_lung_right = P.Property('Høyre','right', parent = lung_stereotactic, next_category ='antall målvolum', default = True)
stereo_lung_left = P.Property('Venstre','left', parent = lung_stereotactic, next_category ='antall målvolum')

# Lung SBRT: Nr of targets:
for side in [stereo_lung_right, stereo_lung_left]:
  lung_stereo_nr1 = P.Property('1','1', parent = side, default = True)
  lung_stereo_nr2 = P.Property('2','2', parent = side)
  lung_stereo_nr3 = P.Property('3','3', parent = side)

# Lung palliative:
lung_with_4dct = P.Property('4DCT / DIBH', 'with', parent = lung_palliative, default = True)
lung_without_4dct = P.Property('Fripust', 'without', parent = lung_palliative)


# Breast:
breast_partial = P.Property('Del av bryst', 'partial', parent = breast, next_category = '')
breast_whole = P.Property('Bryst/brystvegg', 'whole', parent = breast, next_category = '', default = True)
breast_locoregional = P.Property('Bryst/brystvegg og regionale lymfeknuter', 'regional', parent = breast, next_category ='side')
breast_imn = P.Property('Bryst/brystvegg og regionale+parasternale lymfeknuter', 'regional_imn', parent = breast, next_category = 'side')
breast_bilateral = P.Property('Bilateral', 'bilateral', parent = breast, next_category = '')

# Whole breast: Side:
breast_right_whole = P.Property('Høyre','right', parent = breast_whole, next_category = '', default = True)
breast_left_whole = P.Property('Venstre','left', parent = breast_whole, next_category = '')

# Breast/partial: Side:
breast_right_part = P.Property('Høyre','right', parent = breast_partial, default = True)
breast_left_part = P.Property('Venstre','left', parent = breast_partial)

# Breast youth boost:
for side in [breast_right_whole, breast_left_whole]:
  breast_with_boost_whole = P.Property('Med ungdomsboost','with', parent = side)
  breast_without_boost_whole = P.Property('Uten ungdomsboost', 'without', parent = side, default = True)

# Breast regional:
for b in [breast_locoregional, breast_imn]:
  breast_right = P.Property('Høyre','right', parent = b, next_category = '', default = True)
  breast_left = P.Property('Venstre','left', parent = b, next_category = '')
  for side in [breast_right, breast_left]:
    # Breast youth boost:
    breast_with_boost = P.Property('Med ungdomsboost','with', parent = side)
    breast_without_boost = P.Property('Uten ungdomsboost', 'without', parent = side, default = True)

# Bilateral breast left side:
breast_bilateral_left_whole = P.Property('Venstre side: Bryst/Brystvegg', 'bilateral_left_whole', parent = breast_bilateral, next_category = '', default = True)
breast_bilateral_left_regional = P.Property('Venstre side: Lokoregional', 'bilateral_left_regional', parent = breast_bilateral, next_category = '')

# Bilateral breast right side:
for t in [breast_bilateral_left_whole, breast_bilateral_left_regional]:
  breast_bilateral_right_whole = P.Property('Høyre side: Bryst/Brystvegg', 'bilateral_right_whole', parent = t, next_category = '', default = True)
  breast_bilateral_right_regional = P.Property('Høyre side: Lokoregional', 'bilateral_right_regional', parent = t, next_category = '')


# Bladder:
bladder_curative = P.Property('Kurativ', 'curative', parent = bladder, next_category = '', default = True)
bladder_palliative = P.Property('Palliativ','palliative', parent = bladder, next_category = '')


# Prostate:
prostate_normal = P.Property('Prostata', 'prostate', parent = prostate, next_category ='', default = True)
prostate_bed = P.Property('Prostataseng', 'bed', parent = prostate, next_category ='')

# Prostate: Fractionation:
prostate_normo = P.Property('Konvensjonell fraksjonering', 'normo', parent = prostate_normal, next_category ='')
prostate_bergen = P.Property('Hypofraksjonering (67.5 Gy / 25 fx)', 'hypo_bergen', parent = prostate_normal, next_category ='')
prostate_hypo = P.Property('Hypofraksjonering (60 Gy)', 'hypo_60', parent = prostate_normal, next_category ='', default = True)
prostate_lc = P.Property('Lokal kontroll (STAMPEDE: 55 Gy)', 'hypo_55', parent = prostate_normal, next_category ='')
prostate_palliative = P.Property('Palliativ behandling', 'palliative', parent = prostate_normal, next_category ='')

# Prostate: Local control: Seeds?
prostate_lc_seeds = P.Property('Gullmarkører', 'seeds', parent = prostate_lc, next_category ='', default = True)
prostate_lc_bone = P.Property('Bein-match', 'bone', parent = prostate_lc, next_category ='')

# Prostate/bed: Fractionation:
prostate_bed_normo = P.Property('Konvensjonell fraksjonering', 'normo', parent = prostate_bed, next_category ='', default = True)
prostate_bed_palliative = P.Property('Palliativ fraksjonering', 'palliative', parent = prostate_bed, next_category ='')

# Prosate/bed: Lymph nodes:
for p in [prostate_normo, prostate_bergen, prostate_bed_normo]:
  prostate_without_ln =  P.Property('Uten lymfeknuter', 'no',  parent = p, next_category ='', default = True)
  prostate_with_ln =  P.Property('Med lymfeknuter', 'with', parent = p, next_category ='')
  prostate_with_ln_boost =  P.Property('Med lymfeknuter og boost til positiv lymfeknute', 'with_node', parent = p, next_category ='')


# Rectum:
rectum_hypo = P.Property('Hypofraksjonering', 'hypo', parent = rectum, next_category ='', default = True)
rectum_normo = P.Property('Konvensjonell fraksjonering (med SIB)', 'normo', parent = rectum, next_category ='omfang')

# Rectum normo: Nodes:
rectum_with_nodes = P.Property('Med patologisk forstørrede lymfeknuter i lyskene', 'with', parent = rectum_normo)
rectum_without_nodes = P.Property('Uten patologisk forstørrede lymfeknuter i lyskene', 'without', parent = rectum_normo, default = True)


# Other (palliative): SBRT:
other_stereotactic = P.Property('Stereotaksi', 'yes', parent =other, next_category = 'region')
other_non_stereotactic = P.Property('Ikke stereotaksi', 'no', parent = other, next_category = 'region', default = True)

# Other non-SBRT: Region:
other_head = P.Property('Hode', 'head', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_neck = P.Property('Hals', 'neck', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_costa = P.Property('Costa', 'costa', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_thorax = P.Property('Thorax', 'thorax', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_thorax_and_abdomen = P.Property('Thorax/Abdomen', 'thorax_abdomen', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_abdomen = P.Property('Abdomen', 'abdomen', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_abdomen_and_pelvis = P.Property('Abdomen/Bekken', 'abdomen_pelvis', parent=other_non_stereotactic, next_category = 'antall målvolum')
other_pelvis = P.Property('Bekken', 'pelvis', parent=other_non_stereotactic, next_category = 'antall målvolum', default = True)
other_other = P.Property('Ekstremiteter', 'other', parent=other_non_stereotactic, next_category = 'antall målvolum')

# Other SBRT: Region:
other_stereotactic_col_cervical =  P.Property('Columna - cervical', 'col cervical', parent=other_stereotactic)
other_stereotactic_col_thorax =  P.Property('Columna - thorax', 'col thorax', parent=other_stereotactic)
other_stereotactic_col_pelvis =  P.Property('Columna - bekken', 'col pelvis', parent=other_stereotactic)
other_stereotactic_pelvis  = P.Property('Bekken', 'pelvis', parent=other_stereotactic, default = True)

# Other non-SBRT: Number of target volumes:
for region in [other_head, other_neck, other_costa, other_thorax, other_thorax_and_abdomen, other_abdomen, other_abdomen_and_pelvis, other_pelvis, other_other]:
  other_target_volume_one = P.Property('1','1', parent = region, next_category = '', default = True)
  other_target_volume_two = P.Property('2','2', parent = region, next_category = '')
  # With or without soft tissue component:
  for tv in [other_target_volume_one, other_target_volume_two]:
    if region == other_neck:
      # For neck only, selection for whether a mask was used:
      other_with_gtv = P.Property('Bløtvevskomponent (med GTV)', 'with', parent = tv, next_category = '')
      other_without_gtv = P.Property('Skjelett (uten GTV)', 'without', parent = tv, next_category = '', default = True)
      for gtv in [other_with_gtv, other_without_gtv]:
        mask = P.Property('Fiksering med maske','mask', parent = gtv, next_category = '', default = True)
        without_mask = P.Property('Løs fiksering (ingen maske)','none', parent = gtv, next_category = '')
    else:
      # No mask selection to be made:
      other_with_gtv = P.Property('Bløtvevskomponent (med GTV)', 'with', parent = tv)
      other_without_gtv = P.Property('Skjelett (uten GTV)', 'without', parent = tv, default = True)


# Lists to be used with radiobutton objects:
regions = [brain, lung, breast, bladder, prostate, rectum, other]


# Radiobutton choices for deleting/keeping pre-existing ROIs:
p_delete = P.Property('Slett eksisterende ROIs', 'yes')
p_delete_derived = P.Property('Slett alle bortsett fra inntegnede ROIs','some')
p_not_delete = P.Property('Ikke slett eksisterende ROIs','no', default = True)
delete = [p_delete, p_delete_derived, p_not_delete]
