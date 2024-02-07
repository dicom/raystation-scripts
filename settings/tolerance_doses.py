# encoding: utf8

# Import local files:
import tolerance as EQD


# Alpha/beta values:
ab_kidney = 2
ab_kidneys = 2
ab_lung = 3
ab_heart = 3
ab_heart_darby = 2
ab_bowel = 3
ab_spinalcord = 2
ab_spinalcord_dmcg = 0.87
ab_eye = 3
ab_lens = 1
ab_parotid = 3
ab_thyroid = 3
ab_brain = 2
ab_esophagus = 3
ab_lung = 3
ab_bladder = 2
ab_rectum = 3
ab_femoral = 3
ab_brainstem = 2
ab_optic_nerve = 2
ab_optic_chiasm = 2
ab_lacrimal = 3
ab_cochlea = 3
ab_hippocampus = 2
ab_pituitary = 2
ab_retina = 3
ab_scalp = 2
ab_humeral = 3
ab_trachea = 3
ab_chestwall = 3
ab_ribs = 3
ab_greatves = 3
ab_bronchus = 3
ab_liver = 2
ab_brachial = 2
ab_spleen = 3
ab_stomach = 3
ab_skin = 2
ab_kidney_hilum = 2
ab_cauda = 3
ab_colon = 3
ab_bowel = 3
ab_breast = 4
ab_lad = 2
ab_cornea = 3
ab_penile_bulb = 3
ab_blood = 3


# Reference number of fractions:
fractions_kidney = 25
fractions_lung = 33
fractions_heart = 33
fractions_bowelspace = 25
fractions_spinalcord = 25
fractions_parotid = 25
fractions_esophagus = 33
fractions_bladder = 41
fractions_bladder_hypo = 20
fractions_rectum = 39
fractions_rectum_hypo = 20
fractions_femoral = 21
fractions_bladder_at_rectum = 25
fractions_breast = 25
fractions_breast_15 = 15
fractions_eye = 33
fractions_sbrt_3 = 3
fractions_sbrt_5 = 5
fractions_sbrt_8 = 8
fractions_sbrt_1 = 1
# Til ny prosedyre, del av hjerne og total hjerne
fractions_brainstem_surface = 30
fractions_brainstem_core = 27
fractions_optic_nerve = 27.5
fractions_optic_chiasm = 27.5
fractions_cochlea = 22.5
fractions_cochlea_tinnitus = 16
fractions_hippocampus = 3.65
fractions_lens = 5
fractions_humeral = 25
fractions_pituitary = 22.5
fractions_pituitary_2 = 10
fractions_brain = 30
fractions_cornea = 25
fractions_lacrimal = 12.5
fractions_retina = 22.5
fractions_skin = 12.5

# Example:
# EQD.Tolerance(organ, endpoint, alphabeta, nr_fractions, dose, criteria, comment)

# Conventional RT:

# Head


# Partial brain
lens_v003_adx = EQD.Tolerance('Lens_L','Some failure', ab_lens, fractions_lens, 10, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
brain_v003 = EQD.Tolerance('Brain','Some failure', ab_brain, fractions_brain, 60, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
brainstem_surface_v003_adx = EQD.Tolerance('BrainstemSurface', 'Some failure', ab_brainstem, fractions_brainstem_surface, 60, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
brainstem_core_v003_adx = EQD.Tolerance('BrainstemCore', 'Some failure', ab_brainstem, fractions_brainstem_core, 54, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
optic_nrv_v003_adx = EQD.Tolerance('OpticNrv','Some failure', ab_optic_nerve, fractions_optic_nerve, 55,  'Maximum dose at less than 0.03cc volume', 'Conventional RT')
optic_chiasm_v003_adx = EQD.Tolerance('OpticChiasm', 'Some failure', ab_optic_chiasm, fractions_optic_chiasm, 55, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
lacrimal_mean = EQD.Tolerance('Glnd_Lacrimal', 'Some failure', ab_lacrimal, fractions_lacrimal, 25,  'Mean', 'Conventional RT')
cochlea_mean = EQD.Tolerance('Cochlea_L', 'Some failure', ab_cochlea, fractions_cochlea, 45, 'Mean', 'Conventional RT')
cochlea_mean_tinnitus = EQD.Tolerance('Cochlea_R', 'Some failure', ab_cochlea, fractions_cochlea_tinnitus, 32, 'Mean', 'Conventional RT')
pituitary_mean = EQD.Tolerance('Pituitary', 'Some failure', ab_pituitary, fractions_pituitary, 45, 'Mean', 'Conventional RT')
pituitary_2_mean = EQD.Tolerance('Pituitary', 'Some failure', ab_pituitary, fractions_pituitary_2, 20, 'Mean', 'Conventional RT')
retina_v003_adx = EQD.Tolerance('Retina_R', 'Some failure', ab_retina, fractions_retina, 45, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
cornea_v003_adx = EQD.Tolerance('Cornea', 'Some failure', ab_cornea, fractions_cornea, 50, 'Maximum dose at less than 0.03cc volume', 'Conventional RT')
skin_v003_adx = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_skin, 25,'Maximum dose at less than 0.03cc volume', 'Conventional RT')
hippocampus_v40 = EQD.Tolerance('Hippocampus_L', 'Some failure', ab_hippocampus, fractions_hippocampus, 7.3, 'Volume receiving tolerance dose being less than 40%', 'Conventional RT')


# Neck
parotids_mean = EQD.Tolerance('Parotid', 'Some failure', ab_parotid, fractions_parotid, 25, 'Mean', 'Conventional RT')
parotid_mean = EQD.Tolerance('Parotid', 'Some failure', ab_parotid, fractions_parotid, 20, 'Mean', 'Conventional RT')


# Thorax
esophagus_mean = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', ab_esophagus, fractions_esophagus, 34, 'Mean', 'Conventional RT')
esophagus_v17_adx = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', ab_esophagus, fractions_esophagus, 60, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')
heart_mean = EQD.Tolerance('Heart', 'Heart toxicity < 15 %', ab_heart, fractions_heart, 20, 'Mean', 'Conventional RT')
heart_v25_adx = EQD.Tolerance('Heart', 'Heart toxicity < 15 %', ab_heart, fractions_heart, 50, 'Volume receiving tolerance dose being less than 25 %', 'Conventional RT')
heart_v30_adx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, fractions_heart, 60, 'Volume receiving tolerance dose being less than 30 %', 'Conventional RT')
heart_v60_adx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, fractions_heart, 45, 'Volume receiving tolerance dose being less than 60 %', 'Conventional RT')
heart_v80_adx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, fractions_heart, 40, 'Volume receiving tolerance dose being less than 80 %', 'Conventional RT')
heart_v10 = EQD.Tolerance('Heart', 'Heart toxicity < 1 % @ 15 years', ab_heart, 10, 20, 'Volume receiving tolerance dose being less than 10 %', 'Conventional RT')
heart_v355 = EQD.Tolerance('Heart', 'Post operative OS', ab_heart, 2.655, 5.31, 'Volume receiving tolerance dose being less than 35.5 %', 'Conventional RT')
heart_lymphopenia_mean = EQD.Tolerance('Heart', 'Grade 3 lymphopenia', 10, 2.21, 4.42, 'Mean', 'Conventional RT')
heart_lymphopenia_v38 = EQD.Tolerance('Heart', 'Grade 3 lymphopenia', 10, 2.125, 4.25, 'Volume receiving tolerance dose being less than 38 %', 'Conventional RT')
heart_lymphopenia_v25 = EQD.Tolerance('Heart', 'Grade 3 lymphopenia', 10, 4.305, 8.61, 'Volume receiving tolerance dose being less than 25 %', 'Conventional RT')
kidney_mean = EQD.Tolerance('Kidney', 'Acute kidney failure', ab_kidney, fractions_kidney, 15, 'Mean', 'Conventional RT')
kidney_v20_adx = EQD.Tolerance('Kidney', 'Acute kidney failure', ab_kidney, fractions_kidney, 28, 'Volume receiving tolerance dose being less than 20%', 'Conventional RT')
kidney_v30_adx = EQD.Tolerance('Kidney', 'Acute kidney failure', ab_kidney, fractions_kidney, 23, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
kidney_v32_adx = EQD.Tolerance('Kidney', 'Acute kidney failure', ab_kidney, fractions_kidney, 20, 'Volume receiving tolerance dose being less than 32%', 'Conventional RT')
kidney_v55_adx = EQD.Tolerance('Kidney', 'Acute kidney failure', ab_kidney, fractions_kidney, 12, 'Volume receiving tolerance dose being less than 12%', 'Conventional RT')
lad_v10 = EQD.Tolerance('A_LAD', '20 % risk of death within 2 years', 3, 33, 15, 'Volume receiving tolerance dose being less than 10 %', 'Conventional RT')
lad_v01 = EQD.Tolerance('A_LAD', 'Increased risk of heart toxicity for patients with previous heart disesase', 3, 33, 15, 'Volume receiving tolerance dose being less than 1 %', 'Conventional RT')
lung_mean = EQD.Tolerance('Lung', 'Radiation induced pneumonitis < 20 %', ab_lung, fractions_lung, 20, 'Mean', 'Conventional RT')
lung_v35_adx = EQD.Tolerance('Lung', 'Radiation induced pneumonitis < 20 %', ab_lung, fractions_lung, 20, 'Volume receiving tolerance dose being less than 35 %', 'Conventional RT')
lung_lymphopenia_mean = EQD.Tolerance('Lung', 'Grade 3 lymphopenia', 10, 6, 12, 'Mean', 'Conventional RT')
lung_lymphopenia_v30 = EQD.Tolerance('Lung', 'Radiation induced lymphopenia', 10, 30, 10, 'Volume receiving tolerance dose being less than 30 %', 'Conventional RT')
lung_lymphopenia_v45 = EQD.Tolerance('Lung', 'Radiation induced lymphopenia', 10, 30, 5, 'Volume receiving tolerance dose being less than 45 %', 'Conventional RT')
spinalcord_v2_adx = EQD.Tolerance('SpinalCord', 'Myelopathy', ab_spinalcord, fractions_spinalcord, 50, 'Volume receiving tolerance dose being less than 2 cm3', 'Conventional RT')
spinalcanal_v2_adx = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord, fractions_spinalcord, 50, 'Volume receiving tolerance dose being less than 2 cm3', 'Conventional RT')
spinalcanal_chemo_v2_adx = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord, fractions_spinalcord, 45, 'Volume receiving tolerance dose being less than 2 cm3', 'Conventional RT')
spleen_lymphopenia_mean = EQD.Tolerance('Spleen', 'Lymphopenia OS 1 year after RT', 10, 0.955, 1.91, 'Mean', 'Conventional RT')
spleen_lymphopenia_v17 = EQD.Tolerance('Spleen', 'Grade 3 lymphopenia', 10, 2.12, 4.24, 'Volume receiving tolerance dose being less than 17 %', 'Conventional RT')
spleen_lymphopenia_v16 = EQD.Tolerance('Spleen', 'Grade 3 lymphopenia', 10, 4.315, 8.63, 'Volume receiving tolerance dose being less than 16 %', 'Conventional RT')
spleen_lymphopenia_v09 = EQD.Tolerance('Spleen', 'Grade 3 lymphopenia', 10, 6.585, 13.17, 'Volume receiving tolerance dose being less than 9 %', 'Conventional RT')
spleen_lymphopenia_v05 = EQD.Tolerance('Spleen', 'Grade 3 lymphopenia', 10, 8.93, 17.86, 'Volume receiving tolerance dose being less than 5 %', 'Conventional RT')


# Bi-daily (30fx*1.5 Gy):
heart_mean_bid_30fx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, 30, 18.7, 'Mean', 'Conventional RT')
heart_v25_bid_30fx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, 30, 44.6, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
lung_mean_bid_30fx = EQD.Tolerance('Lung', 'Radiation pneumonitis', ab_lung, 30, 18.7, 'Mean', 'Conventional RT')
lung_v35_bid_30fx = EQD.Tolerance('Lung', 'Radiation pneumonitis', ab_lung, 30, 18.7, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
esophagus_mean_bid_30fx = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', ab_esophagus, 30, 31.7, 'Mean', 'Conventional RT')
esophagus_v17_bid_30fx = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', ab_esophagus, 30, 54.7, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')
spinalcanal_bid_30fx = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord, 30, 47.1, 'Volume receiving tolerance dose being less than 0.03 cm^3', 'Conventional RT')
spinalcanal_chemo_bid_30fx = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord, 30, 43.9, 'Volume receiving tolerance dose being less than 0.03 cm^3', 'Conventional RT')
# Bi-daily (40fx*1.5 Gy):
heart_mean_bid_40fx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, 40, 19.6, 'Mean', 'Conventional RT')
heart_v25_bid_40fx = EQD.Tolerance('Heart', 'Heart toxicity', ab_heart, 40, 48.3, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
lung_mean_bid_40fx = EQD.Tolerance('Lung', 'Radiation pneumonitis', ab_lung, 40, 19.6, 'Mean', 'Conventional RT')
lung_v35_bid_40fx = EQD.Tolerance('Lung', 'Radiation pneumonitis', ab_lung, 40, 19.6, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
esophagus_mean_bid_40fx = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', ab_esophagus, 40, 33.8, 'Mean', 'Conventional RT')
esophagus_v17_bid_40fx = EQD.Tolerance('Esophagus', 'Esophagitis grade 3', ab_esophagus, 40, 59.4, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')
spinalcanal_bid_40fx = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord, 40, 51.8, 'Volume receiving tolerance dose being less than 0.03 cm^3', 'Conventional RT')
spinalcanal_chemo_bid_40fx = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord, 40, 48.2, 'Volume receiving tolerance dose being less than 0.03 cm^3', 'Conventional RT')


# Breast
lung_v15_adx = EQD.Tolerance('Lung_L', 'Some failure', ab_lung, fractions_breast_15, 18, 'Volume receiving tolerance dose being less than 15%', 'Conventional RT')
lung_v8_fastforward = EQD.Tolerance('Lung_L', 'Some failure', ab_lung, 5, 8, 'Volume receiving tolerance dose being less than 15%', 'Conventional RT')
heart_mean_breast = EQD.Tolerance('Heart', 'Ischemic heart disease', ab_heart_darby, 1, 2, 'Mean', 'Conventional RT')
heart_mean_breast_low_priority = EQD.Tolerance('Heart', 'Any cardiac event/Major cardiac event (AH Zureick et al, 2022)', ab_heart_darby, 0.4, 0.8, 'Mean', 'Conventional RT')
heart_v7_fastforward = EQD.Tolerance('Heart', 'Some failure', ab_heart, 5, 7, 'Volume receiving tolerance dose being less than 5%', 'Conventional RT')
heart_v1_5_fastforward = EQD.Tolerance('Heart', 'Some failure', ab_heart, 5, 1.5, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
heart_v13gy_import_high = EQD.Tolerance('Heart', 'Import HIGH protocol', ab_heart, 15, 13, 'Volume receiving tolerance dose being less than 10%', 'Conventional RT')
lad_max = EQD.Tolerance('A_LAD', 'Any cardiac event/Major cardiac event (AH Zureick et al, 2022)', ab_lad, 3.35, 6.7, 'Max', 'Conventional RT')
lad_mean = EQD.Tolerance('A_LAD', 'Any cardiac event/Major cardiac event (AH Zureick et al, 2022)', ab_lad, 1.4, 2.8, 'Mean', 'Conventional RT')
humeral_v33_adx = EQD.Tolerance('Humeral', 'Some failure', ab_humeral, fractions_breast, 25, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')
contralat_breast_mean = EQD.Tolerance('Breast', 'Some failure', ab_breast, fractions_breast, 4, 'Mean', 'Conventional RT')
contralat_breast_mean_young_patients = EQD.Tolerance('Breast', 'Some failure', ab_breast, fractions_breast, 1, 'Mean', 'Conventional RT')
lung_v35_adx_25 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_breast, 20, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
lung_v35_adx_15 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_breast_15, 18, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
lung_v30 = EQD.Tolerance('Lung', 'Radiation induced lymphopenia', 10, 4.305, 8.61, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
lung_v45 = EQD.Tolerance('Lung', 'Radiation induced lymphopenia', 10, 2.12, 4.24, 'Volume receiving tolerance dose being less than 45%', 'Conventional RT')
lung_mean_import_high = EQD.Tolerance('Lung_L/R', 'Import HIGH protocol', ab_lung, 15, 6, 'Mean', 'Conventional RT')
lung_v2_5gy_import_high = EQD.Tolerance('Lung', 'Import HIGH protocol', ab_heart, 15, 2.5, 'Volume receiving tolerance dose being less than 15%', 'Conventional RT')
esophagus_mean_brt = EQD.Tolerance('Esophagus', 'Esophagitis grade 2', ab_esophagus, 25, 11, 'Mean', 'Conventional RT')
esophagus_v30_adx_brt = EQD.Tolerance('Esophagus', 'Esophagitis grade 2', ab_esophagus, 25, 10, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
esophagus_v15_adx_brt = EQD.Tolerance('Esophagus', 'Esophagitis grade 2', ab_esophagus, 25, 20, 'Volume receiving tolerance dose being less than 15%', 'Conventional RT')
spinalcanal_breast = EQD.Tolerance('SpinalCanal', 'Myelopathy', ab_spinalcord_dmcg, 22.5, 45, 'Volume receiving tolerance dose being less than 0.03 cm^3', 'Conventional RT')
thyroid_mean = EQD.Tolerance('ThyroidGland', 'Hypothyroidism', ab_thyroid, 15, 21, 'Mean', 'Conventional RT')
thyroid_mean_brt = EQD.Tolerance('ThyroidGland', 'Hypothyroidism', ab_thyroid, 25, 11.8, 'Mean', 'Conventional RT')
thyroid_v8_5cc_adx_brt = EQD.Tolerance('ThyroidGland', 'Hypothyroidism', ab_thyroid, 25, 20, 'More than 8.5 cm^3 should receive less than the tolerance dose', 'Conventional RT')
contralateral_lung_mean = EQD.Tolerance('Contralateral Lung', 'Secondary cancer risk', ab_lung, 25, 2, 'Mean', 'Conventional RT')
# Induration (for partial breast irradiation):
ipsilateral_breast_177cc = EQD.Tolerance('Breast_L/R','5 % risk of induration', 3.6, 15, 40,'Volume receiving tolerance dose being less than 177 cc', 'Conventional RT' )
ipsilateral_breast_426cc = EQD.Tolerance('Breast_L/R','10 % risk of induration', 3.6, 15, 40,'Volume receiving tolerance dose being less than 426 cc', 'Conventional RT' )


# Prostate
# Bowel bag:
bowel_bag_v195cc = EQD.Tolerance('BowelBag', 'Acute GI toxicity (QUANTEC, Roeske)', ab_bowel, 21.5, 43, 'Volume receiving tolerance dose being less than 195 cm^3', 'Conventional RT')
# Rectum (high risk):
rectum_v22pc = EQD.Tolerance('Rectum', 'High risk of rectal toxicity (Olsson)', ab_rectum, 36, 72, 'Volume receiving tolerance dose being less than 22 %', 'Conventional RT')
rectum_v38pc = EQD.Tolerance('Rectum', 'High risk of rectal toxicity (Olsson)', ab_rectum, 30, 60, 'Volume receiving tolerance dose being less than 38 %', 'Conventional RT')
rectum_v51pc = EQD.Tolerance('Rectum', 'High risk of rectal toxicity (Olsson)', ab_rectum, 25, 50, 'Volume receiving tolerance dose being less than 51 %', 'Conventional RT')
rectum_v64pc = EQD.Tolerance('Rectum', 'High risk of rectal toxicity (Olsson)', ab_rectum, 20, 40, 'Volume receiving tolerance dose being less than 64 %', 'Conventional RT')
rectum_v80pc = EQD.Tolerance('Rectum', 'High risk of rectal toxicity (Olsson)', ab_rectum, 13, 26, 'Volume receiving tolerance dose being less than 80 %', 'Conventional RT')
# Rectum (low risk):
rectum_v01pc = EQD.Tolerance('Rectum', 'Low risk of rectal toxicity (Olsson)', ab_rectum, 36, 72, 'Volume receiving tolerance dose being less than 1 %', 'Conventional RT')
rectum_v18pc = EQD.Tolerance('Rectum', 'Low risk of rectal toxicity (Olsson)', ab_rectum, 30, 60, 'Volume receiving tolerance dose being less than 18 %', 'Conventional RT')
rectum_v31pc = EQD.Tolerance('Rectum', 'Low risk of rectal toxicity (Olsson)', ab_rectum, 25, 50, 'Volume receiving tolerance dose being less than 31 %', 'Conventional RT')
rectum_v44pc = EQD.Tolerance('Rectum', 'Low risk of rectal toxicity (Olsson)', ab_rectum, 20, 40, 'Volume receiving tolerance dose being less than 44 %', 'Conventional RT')
rectum_v60pc = EQD.Tolerance('Rectum', 'Low risk of rectal toxicity (Olsson)', ab_rectum, 13, 26, 'Volume receiving tolerance dose being less than 60 %', 'Conventional RT')
# Anal canal:
anal_canal_mean = EQD.Tolerance('AnalCanal', 'Incontinence (Jadon)', ab_rectum, 20, 40, 'Mean', 'Conventional RT')
# Bladder:
bladder_v01pc = EQD.Tolerance('Bladder', 'Obstruction (Olsson)', ab_bladder, 40.5, 81, 'Volume receiving tolerance dose being less than 1 %', 'Conventional RT')
bladder_v20pc = EQD.Tolerance('Bladder', 'Obstruction (Olsson)', ab_bladder, 33, 66, 'Volume receiving tolerance dose being less than 20 %', 'Conventional RT')
bladder_v05pc = EQD.Tolerance('Bladder', 'Gross hematuria (Olsson)', ab_bladder, 37, 74, 'Volume receiving tolerance dose being less than 5 %', 'Conventional RT')
bladder_v41pc = EQD.Tolerance('Bladder', 'Microscopic hematuria (Olsson)', ab_bladder, 31.5, 63, 'Volume receiving tolerance dose being less than 41 %', 'Conventional RT')
bladder_v19pc = EQD.Tolerance('Bladder', 'Dysuria (Olsson)', ab_bladder, 32, 64, 'Volume receiving tolerance dose being less than 19 %', 'Conventional RT')
bladder_v02pc = EQD.Tolerance('Bladder', 'Urinary urgency (Olsson)', ab_bladder, 41.5, 83, 'Volume receiving tolerance dose being less than 2 %', 'Conventional RT')
bladder_v41pc_freq = EQD.Tolerance('Bladder', 'Urinary frequency (Olsson)', ab_bladder, 19.5, 39, 'Volume receiving tolerance dose being less than 41 %', 'Conventional RT')
# Femoral heads:
femoral_head_mean = EQD.Tolerance('FemoralHead_L/R', 'Femoral neck fracture (Grigsby)', ab_femoral, 21, 42, 'Mean', 'Conventional RT')
femoral_d02pc = EQD.Tolerance('FemoralHead_L/R', 'Hip osteoarthritis (Rasmusson)', ab_femoral, 20, 40, 'Near maximum dose (2 % volume) being less than the tolerance', 'Conventional RT')
# Penile bulb:
penile_bulb_mean = EQD.Tolerance('PenileBulb', 'Erectile dysfunction (Rasmusson)', ab_penile_bulb, 10, 20, 'Mean', 'Conventional RT')
penile_bulb_d02pc = EQD.Tolerance('PenileBulb', 'Erectile dysfunction (Rasmusson)', ab_penile_bulb, 25, 50, 'Near maximum dose (2 % volume) being less than the tolerance', 'Conventional RT')
# Bone:
bone_v1000cc = EQD.Tolerance('Bone', 'Reduced hemoglobin levels', ab_blood, 7.5, 15, 'Volume receiving tolerance dose being less than 1000 cm^3', 'Conventional RT')


# General / Palliative:
bladder_v50_quantec = EQD.Tolerance('Bladder','Grade >= 3 late RTOG', ab_bladder, 41, 65, 'Volume receiving tolerance dose being less than 50 %', 'Conventional RT')
heart_mean_quantec = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, 25, 26, 'Mean', 'Conventional RT')
heart_v46_quantec = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, 25, 30, 'Volume receiving tolerance dose being less than 46 %', 'Conventional RT')
liver_mean = EQD.Tolerance('Liver', 'Classic RILD (QUANTEC)', ab_liver, 15, 30, 'Mean', 'Conventional RT')
spleen_mean = EQD.Tolerance('Spleen', 'Lymphopenia', ab_spleen, 25, 10, 'Mean', 'Conventional RT')
stomach_min = EQD.Tolerance('Stomach', 'Ulceration', ab_stomach, 25, 45, 'Volume receiving tolerance dose being no more than 0 cm^3', 'Conventional RT')




# SBRT:


# Lung SBRT 3 fractions
spinal_canal_sbrt_3fx = EQD.Tolerance('SpinalCanal', 'Myelitis 1-5 %', ab_spinalcord, fractions_sbrt_3, 20.3, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
esophagus_sbrt_3fx = EQD.Tolerance('Esophagus', 'Stenosis/Fistula', ab_esophagus, fractions_sbrt_3, 25.2, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
greatves_sbrt_3fx = EQD.Tolerance('GreatVes', 'Aneurism', ab_greatves, fractions_sbrt_3, 45, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
main_bronchus_sbrt_3fx = EQD.Tolerance('Main Bronchus', 'Stenosis/Fistula', ab_bronchus, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
heart_sbrt_3fx = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
heart_sbrt_3fx_secondary = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, fractions_sbrt_3, 26, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
trachea_sbrt_3fx = EQD.Tolerance('Trachea', 'Stenosis/Fistula', ab_trachea, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
chestwall_sbrt_3fx_v01 = EQD.Tolerance('Chestwall', 'Grade 3 pain/fracture', ab_chestwall, fractions_sbrt_3, 36.9, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
chestwall_sbrt_3fx_v30 = EQD.Tolerance('Chestwall', 'Grade 3 pain/fracture', ab_chestwall, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 30 cm3', 'SBRT')
ribs_sbrt_3fx = EQD.Tolerance('Ribs', 'Fracture risk 5 %', ab_ribs, fractions_sbrt_3, 53.8, 'Maximum dose being less than the tolerance dose', 'SBRT')
skin_sbrt_3fx_cc01 = EQD.Tolerance('Skin', 'Grade 3 ulceration', ab_skin, fractions_sbrt_3, 33, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
skin_sbrt_3fx_cc10 = EQD.Tolerance('Skin', 'Grade 3 ulceration', ab_skin, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
stomach_sbrt_3fx_cc01 = EQD.Tolerance('Stomach', 'Grade 3 ulceration/fistula', ab_stomach, fractions_sbrt_3, 22.2, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')


# Lung SBRT 5 fractions
spinal_canal_sbrt_5fx = EQD.Tolerance('SpinalCanal', 'Myelitis 1-5 %', ab_spinalcord, fractions_sbrt_5, 25.3, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
esophagus_sbrt_5fx = EQD.Tolerance('Esophagus', 'Stenosis/Fistula', ab_esophagus, fractions_sbrt_5, 35, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
greatves_sbrt_5fx = EQD.Tolerance('GreatVes', 'Aneurism', ab_greatves, fractions_sbrt_5, 53, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
main_bronchus_sbrt_5fx = EQD.Tolerance('Main Bronchus', 'Stenosis/Fistula', ab_bronchus, fractions_sbrt_5, 38, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
heart_sbrt_5fx = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, fractions_sbrt_5, 38, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
heart_sbrt_5fx_secondary = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, fractions_sbrt_5, 29, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
lung_sbrt_mean = EQD.Tolerance('Lung', 'Pneumonitis', ab_lung, fractions_sbrt_5, 8, 'Mean dose', 'SBRT')
lung_sbrt_contralat_mean = EQD.Tolerance('Lung', 'Pneumonitis', ab_lung, fractions_sbrt_5, 3.6, 'Mean dose', 'SBRT')
lung_sbrt_v_10pc = EQD.Tolerance('Lung', 'Pneumonitis', ab_lung, fractions_sbrt_5, 20, 'Volume receiving tolerance dose being less than 10 %', 'SBRT')
lung_sbrt_v_15pc = EQD.Tolerance('Lung', 'Pneumonitis', ab_lung, fractions_sbrt_5, 20, 'Volume receiving tolerance dose being less than 15 %', 'SBRT')
trachea_sbrt_5fx = EQD.Tolerance('Trachea', 'Stenosis/Fistula', ab_trachea, fractions_sbrt_5, 38, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
chestwall_sbrt_5fx_v01 = EQD.Tolerance('Chestwall', 'Grade 3 pain/fracture', ab_chestwall, fractions_sbrt_5, 43, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
chestwall_sbrt_5fx_v30 = EQD.Tolerance('Chestwall', 'Grade 3 pain/fracture', ab_chestwall, fractions_sbrt_5, 32, 'Volume receiving tolerance dose being less than 30 cm3', 'SBRT')
ribs_sbrt_5fx = EQD.Tolerance('Ribs', 'Fracture risk 5 %', ab_ribs, fractions_sbrt_5, 67.9, 'Maximum dose being less than the tolerance dose', 'SBRT')
skin_sbrt_5fx_cc01 = EQD.Tolerance('Skin', 'Grade 3 ulceration', ab_skin, fractions_sbrt_5, 39.5, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
skin_sbrt_5fx_cc10 = EQD.Tolerance('Skin', 'Grade 3 ulceration', ab_skin, fractions_sbrt_5, 36.5, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
stomach_sbrt_5fx_cc01 = EQD.Tolerance('Stomach', 'Grade 3 ulceration/fistula', ab_stomach, fractions_sbrt_5, 35, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')


# Lung SBRT 8 fractions
spinal_canal_sbrt_8fx = EQD.Tolerance('SpinalCanal', 'Myelitis 1-5 %', ab_spinalcord, fractions_sbrt_8, 32.0, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
esophagus_sbrt_8fx = EQD.Tolerance('Esophagus', 'Stenosis/Fistula', ab_esophagus, fractions_sbrt_8, 40, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
greatves_sbrt_8fx = EQD.Tolerance('GreatVes', 'Aneurism', ab_greatves, fractions_sbrt_8, 65, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
main_bronchus_sbrt_8fx = EQD.Tolerance('Main Bronchus', 'Stenosis/Fistula', ab_bronchus, fractions_sbrt_8, 40, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
heart_sbrt_8fx = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, fractions_sbrt_8, 46, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
heart_sbrt_8fx_secondary = EQD.Tolerance('Heart', 'Pericarditis', ab_heart, fractions_sbrt_8, 40, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
trachea_sbrt_8fx = EQD.Tolerance('Trachea', 'Stenosis/Fistula', ab_trachea, fractions_sbrt_8, 40, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
chestwall_sbrt_8fx_v01 = EQD.Tolerance('Chestwall', 'Grade 3 pain/fracture', ab_chestwall, fractions_sbrt_8, 52.3, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
chestwall_sbrt_8fx_v30 = EQD.Tolerance('Chestwall', 'Grade 3 pain/fracture', ab_chestwall, fractions_sbrt_8, 35, 'Volume receiving tolerance dose being less than 30 cm3', 'SBRT')
ribs_sbrt_8fx = EQD.Tolerance('Ribs', 'Fracture risk 5 %', ab_ribs, fractions_sbrt_8, 83.6, 'Maximum dose being less than the tolerance dose', 'SBRT')
skin_sbrt_8fx_cc01 = EQD.Tolerance('Skin', 'Grade 3 ulceration', ab_skin, fractions_sbrt_8, 48, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
skin_sbrt_8fx_cc10 = EQD.Tolerance('Skin', 'Grade 3 ulceration', ab_skin, fractions_sbrt_8, 44, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
stomach_sbrt_8fx_cc01 = EQD.Tolerance('Stomach', 'Grade 3 ulceration/fistula', ab_stomach, fractions_sbrt_8, 40, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')


# Brain SRT 1 fraction
cochlea_srt_1fx = EQD.Tolerance('Cochlea_L', 'Hearing loss', ab_cochlea, fractions_sbrt_1, 4, 'Mean dose being less than', 'SBRT')
optic_nrv_srt_1fx_p1 = EQD.Tolerance('OpticNrv_L','Optic neuropathy', ab_optic_nerve, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
optic_nrv_srt_1fx_p2 = EQD.Tolerance('OpticNrv_L','Optic neuropathy', ab_optic_nerve, fractions_sbrt_1, 8, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
optic_chiasm_srt_1fx_p1 = EQD.Tolerance('OpticChiasm', 'Optic neuropathy', ab_optic_chiasm, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
optic_chiasm_srt_1fx_p2 = EQD.Tolerance('OpticChiasm', 'Optic neuropathy', ab_optic_chiasm, fractions_sbrt_1, 8, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
eye_srt_1fx = EQD.Tolerance('Eye_R','Retinopathy', ab_eye, fractions_sbrt_1, 8, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
lens_srt_1fx = EQD.Tolerance('Lens_L','Cataracts', ab_lens, fractions_sbrt_1, 1.5, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
brainstem_srt_1fx_p1 = EQD.Tolerance('Brainstem', 'Necrosis', ab_brainstem, fractions_sbrt_1, 15, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
brainstem_srt_1fx_p2 = EQD.Tolerance('Brainstem', 'Necrosis', ab_brainstem, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
brain_srt_1fx = EQD.Tolerance('Brain', 'Necrosis', ab_brain, fractions_sbrt_1, 12, 'Volume receiving tolerance dose being less than 5/10/15 cm3', 'SBRT')
skin_srt_1fx_v0_1 = EQD.Tolerance('Skin', 'Ulceration', ab_skin, fractions_sbrt_1, 26, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
skin_srt_1fx_v10 = EQD.Tolerance('Skin', 'Ulceration', ab_skin, fractions_sbrt_1, 23, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
spinal_cord_srt_1fx_p1 = EQD.Tolerance('SpinalCord', 'Myelopathy', ab_spinalcord, fractions_sbrt_1, 14, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
spinal_cord_srt_1fx_p2 = EQD.Tolerance('SpinalCord', 'Myelopathy', ab_spinalcord, fractions_sbrt_1, 12.4, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')


# Brain SRT 3 fractions
cochlea_srt_3fx = EQD.Tolerance('Cochlea_L', 'Hearing loss', ab_cochlea, fractions_sbrt_3, 17.1, 'Mean dose being less than', 'SBRT')
optic_nrv_srt_3fx_p1 = EQD.Tolerance('OpticNrv_L','Optic neuropathy', ab_optic_nerve, fractions_sbrt_3, 20, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
optic_nrv_srt_3fx_p2 = EQD.Tolerance('OpticNrv_R','Optic neuropathy', ab_optic_nerve, fractions_sbrt_3, 15, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
optic_chiasm_srt_3fx_p1 = EQD.Tolerance('OpticChiasm', 'Optic neuropathy', ab_optic_chiasm, fractions_sbrt_3, 20, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
optic_chiasm_srt_3fx_p2 = EQD.Tolerance('OpticChiasm', 'Optic neuropathy', ab_optic_chiasm, fractions_sbrt_3, 15, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
eye_srt_3fx = EQD.Tolerance('Eye_L','Retinopathy', ab_eye, fractions_sbrt_3, 12.4, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
lens_srt_3fx = EQD.Tolerance('Lens_R','Cataracts', ab_lens, fractions_sbrt_3, 2.2, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
brainstem_srt_3fx_p1 = EQD.Tolerance('Brainstem', 'Necrosis', ab_brainstem, fractions_sbrt_3, 23.1, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
brainstem_srt_3fx_p2 = EQD.Tolerance('Brainstem', 'Necrosis', ab_brainstem, fractions_sbrt_3, 18, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')
brain_srt_3fx = EQD.Tolerance('Brain', 'Necrosis', ab_brain, fractions_sbrt_3, 20, 'Volume receiving tolerance dose being less than 20/30 cm3', 'SBRT')
skin_srt_3fx_v0_1 = EQD.Tolerance('Skin', 'Ulceration', ab_skin, fractions_sbrt_3, 33, 'Volume receiving tolerance dose being less than 0.1 cm3', 'SBRT')
skin_srt_3fx_v10 = EQD.Tolerance('Skin', 'Ulceration', ab_skin, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
spinal_cord_srt_3fx = EQD.Tolerance('SpinalCord', 'Myelopathy', ab_spinalcord, fractions_sbrt_3, 20.3, 'Volume receiving tolerance dose being less than 0.035 cm3', 'SBRT')


# Bone/Spine SBRT 1 fraction
esophagus_sbrt_1fx_v5 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_1, 11.9, 'Volume receiving tolerance dose being less than 5 cm3', 'SBRT')
esophagus_sbrt_1fx_v0 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_1, 16, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_canal_sbrt_1fx_v0 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_1, 14, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_canal_sbrt_1fx_v0_35 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0.35 cm3', 'SBRT')
spinal_canal_3mm_sbrt_1fx_v0 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_1, 16, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_canal_3mm_sbrt_1fx_v0_1 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_1, 15, 'Volume receiving tolerance dose being less than 0.35 cm3', 'SBRT')
trachea_sbrt_1fx_v4 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_1, 10.5, 'Volume receiving tolerance dose being less than 4cm3', 'SBRT')
trachea_sbrt_1fx_v0 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_1, 20.2, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
heart_sbrt_1fx_v15 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_1, 16, 'Volume receiving tolerance dose being less than 15 cm3', 'SBRT')
heart_sbrt_1fx_v0 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_1, 22, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
skin_sbrt_1fx_v10 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_1, 23, 'Volume receiving tolerance dose being less than 10cm3', 'SBRT')
skin_sbrt_1fx_v0 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_1, 26, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
lungs_sbrt_1fx_v1000 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_1, 7.4, 'Volume receiving tolerance dose being less than 1000cm3', 'SBRT')
brachial_sbrt_1fx_v0 = EQD.Tolerance('BrachialPlexus', 'Some failure', ab_brachial, fractions_sbrt_1, 17.5, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
brachial_sbrt_1fx_v3 = EQD.Tolerance('BrachialPlexus', 'Some failure', ab_brachial, fractions_sbrt_1, 14, 'Volume receiving tolerance dose being less than 3cm3', 'SBRT')
cauda_equina_sbrt_1fx_v0 = EQD.Tolerance('CaudaEquina', 'Some failure', ab_cauda, fractions_sbrt_1, 16, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
cauda_equina_sbrt_1fx_v5 = EQD.Tolerance('BrachialPlexus', 'Some failure', ab_cauda, fractions_sbrt_1, 14, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
small_bowel_sbrt_1fx_v0 = EQD.Tolerance('SmallBowel', 'Some failure', ab_bowel, fractions_sbrt_1, 15.4, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
small_bowel_sbrt_1fx_v5 = EQD.Tolerance('SmallBowel', 'Some failure', ab_bowel, fractions_sbrt_1, 11.9, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
rectum_sbrt_1fx_v0 = EQD.Tolerance('Rectum', 'Some failure', ab_rectum, fractions_sbrt_1, 18.4, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
rectum_sbrt_1fx_v20 = EQD.Tolerance('Rectum', 'Some failure', ab_rectum, fractions_sbrt_1, 14.3, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
colon_sbrt_1fx_v0 = EQD.Tolerance('Colon', 'Some failure', ab_colon, fractions_sbrt_1, 18.4, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
colon_sbrt_1fx_v20 = EQD.Tolerance('Rectum', 'Some failure', ab_colon, fractions_sbrt_1, 14.3, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
kidney_hilum_1fx_v66 = EQD.Tolerance('Kidney_Hilum', 'Some failure', ab_kidney_hilum, fractions_sbrt_1, 10.6, 'Volume receiving tolerance dose being less than 2/3 volume', 'SBRT')
kidney_sbrt_1fx_v0 = EQD.Tolerance('Kidney', 'Some failure', ab_kidney, fractions_sbrt_1, 18.6, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
kidneys_col_1fx_v200 = EQD.Tolerance('Kidneys', 'Some failure', ab_kidneys, fractions_sbrt_1, 8.4, 'Volume receiving tolerance dose being less than 200cm3', 'SBRT')
bladder_1fx_v003 = EQD.Tolerance('Bladder', 'Fistula', ab_bladder, fractions_sbrt_1, 18.4, 'Volume receiving tolerance dose being less than 0.03 cm3', 'SBRT')
bladder_1fx_v15 = EQD.Tolerance('Bladder', 'Fistula', ab_bladder, fractions_sbrt_1, 11.4, 'Volume receiving tolerance dose being less than 15 cm3', 'SBRT')


# Bone/Spine SBRT 3 fractions
spinal_canal_sbrt_3fx_v0 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_3, 21.9, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_canal_sbrt_3fx_v0_35 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_3, 18, 'Volume receiving tolerance dose being less than 0.35 cm3', 'SBRT')
cauda_equina_sbrt_3fx_v0 = EQD.Tolerance('CaudaEquina', 'Some failure', ab_cauda, fractions_sbrt_3, 24, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
cauda_equina_sbrt_3fx_v5 = EQD.Tolerance('BrachialPlexus', 'Some failure', ab_cauda, fractions_sbrt_3, 21.9, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
small_bowel_sbrt_3fx_v0 = EQD.Tolerance('SmallBowel', 'Some failure', ab_bowel, fractions_sbrt_3, 25.2, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
small_bowel_sbrt_3fx_v5 = EQD.Tolerance('SmallBowel', 'Some failure', ab_bowel, fractions_sbrt_3, 17.7, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
skin_col_sbrt_3fx_v10 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 10cm3', 'SBRT')
skin_col_sbrt_3fx_v0 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_3, 33, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
rectum_sbrt_3fx_v0 = EQD.Tolerance('Rectum', 'Some failure', ab_rectum, fractions_sbrt_3, 28.8, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
rectum_sbrt_3fx_v20 = EQD.Tolerance('Rectum', 'Some failure', ab_rectum, fractions_sbrt_3, 24, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
colon_sbrt_3fx_v0 = EQD.Tolerance('Colon', 'Some failure', ab_colon,  fractions_sbrt_3, 28.8, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
colon_sbrt_3fx_v20 = EQD.Tolerance('Colon', 'Some failure', ab_colon,  fractions_sbrt_3, 24, 'Volume receiving tolerance dose being less than 5cm3', 'SBRT')
kidney_3fx_v10 = EQD.Tolerance('Kidney_Hilum', 'Some failure', ab_kidney_hilum, fractions_sbrt_3, 10, 'Volume receiving tolerance dose being less than 1/10 volume', 'SBRT')
kidneys_col_3fx_v200 = EQD.Tolerance('Kidneys', 'Some failure', ab_kidneys, fractions_sbrt_3, 16, 'Volume receiving tolerance dose being less than 200cm3', 'SBRT')
bladder_3fx_v003 = EQD.Tolerance('Bladder', 'Fistula', ab_bladder, fractions_sbrt_3, 28.2, 'Volume receiving tolerance dose being less than 0.03 cm3', 'SBRT')
bladder_3fx_v15 = EQD.Tolerance('Bladder', 'Fistula', ab_bladder, fractions_sbrt_3, 16.8, 'Volume receiving tolerance dose being less than 15 cm3', 'SBRT')
