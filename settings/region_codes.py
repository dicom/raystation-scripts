# encoding: utf8


# Region codes:

# Brain
brain_whole_codes = [401]
brain_partial_codes =  range(402, 415+1)
brain_codes = brain_whole_codes + brain_partial_codes

# Breast
breast_tang_l_codes = [239]
breast_tang_r_codes = [240]
breast_tang_codes = breast_tang_l_codes + breast_tang_r_codes
breast_reg_l_codes = [241, 243]
breast_reg_r_codes = [242, 244]
breast_reg_codes = breast_reg_l_codes + breast_reg_r_codes
breast_l_codes = [239, 241, 243]
breast_r_codes = [240, 242, 244]
breast_codes = breast_tang_l_codes + breast_tang_r_codes + breast_reg_l_codes + breast_reg_r_codes

# Lung
lung_codes = [245, 246, 247, 248, 249, 250]
lung_r_codes = [248, 250]
lung_l_codes = [247, 249]
lung_mediastinum_codes = [224, 225, 226, 228, 245, 246]
lung_and_mediastinum_codes = lung_codes + lung_mediastinum_codes

# Palliative
palliative_head_codes = range(1, 20+1) + range(100, 126+1)  + range(501, 506+1)
palliative_head_codes.extend((100, 101, 102, 110, 111, 112, 114, 116, 117, 118, 120, 121, 125, 126))
palliative_neck_codes = range(21, 29 +1) + range(140, 146+1)
palliative_neck_codes.extend((122, 123, 124, 128, 129, 130, 140, 148, 150, 151, 152, 154, 155, 156, 158, 160, 162, 164, 166, 170, 171, 172, 174, 175, 176, 178, 179, 180, 416, 517))
palliative_thorax_codes = range(30, 43+1) + range(200, 223+1) + range(231, 238+1) + range(251, 258+1) + range(417, 419+1) + range(518, 521+1) + range(530, 538+1)
palliative_thorax_codes.extend((549, 550, 553, 554))
palliative_thorax_and_abdomen_codes = [522]
palliative_abdomen_codes = range(62, 69+1) + range(300, 311+1)
palliative_abdomen_codes.extend((315, 316, 523, 351, 352, 259, 260))
palliative_pelvis_codes = range(70, 85+1) +range(342, 349+1) + range(353, 354+1) + range(512, 514+1) + range(524, 527+1) + range(541, 546+1)
palliative_pelvis_codes.extend((312, 313, 314, 318, 320, 321, 322, 324, 325, 326, 328, 330, 332, 333, 334, 335, 336, 338, 373, 374, 385, 386, 573, 574))
palliative_other_codes = range(44, 61 +1) + range(86, 91 +1) + range(261, 272 +1) + range(585, 594 +1) + range(561, 572 +1)
palliative_other_codes.extend((375, 376, 377, 378, 387, 388, 389, 390, 393, 394, 575, 576, 577, 578, 900, 400))
palliative_codes = palliative_head_codes + palliative_neck_codes + palliative_thorax_codes + palliative_thorax_and_abdomen_codes + palliative_abdomen_codes + palliative_pelvis_codes + palliative_other_codes
palliative_columna_codes = range(517, 526+1)
palliative_columna_codes.extend((512, 416, 417, 418, 419))

# Palliative: Stereotactic
stereotactic_pelvis_codes = [513, 514, 527, 573, 574, 575, 576, 577, 578, 585, 586]
stereotactic_spine_thorax_codes = [520, 521, 522]
stereotactic_spine_pelvis_codes = [523, 524, 525]
bone_stereotactic_codes = stereotactic_pelvis_codes + stereotactic_spine_thorax_codes + stereotactic_spine_pelvis_codes

# Bladder
bladder_codes = [341]

# Prostate
prostate_only_codes = [342]
prostate_vesicles_codes = [343]
prostate_bed_codes = [348]

prostate_codes = prostate_only_codes + prostate_vesicles_codes + prostate_bed_codes
prostate_codes = [342, 343, 348]
# Rectum
rectum_codes = [340]

whole_pelvis_codes = [512]

# Regions where conventional planning and vmat is both done:
conventional_and_vmat_site_codes = brain_whole_codes + breast_reg_codes

