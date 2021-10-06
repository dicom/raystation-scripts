# encoding: utf8

# Import local files:
import tolerance as EQD


# Alpha/beta values:
ab_kidney = 2
ab_kidneys = 2
ab_lung = 3
ab_heart = 3
ab_bowel = 3
ab_spinalcord = 2
ab_eye = 3
ab_lens = 1
ab_parotid = 3
ab_thyroid = 3
ab_brain = 2
ab_esophagus = 3
ab_lung = 3
ab_bladder = 6
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
ab_stomach = 2
ab_skin = 2
ab_kidney_hilum = 2
ab_cauda = 3
ab_colon = 3
ab_bowel = 3
ab_breast = 3
ab_lad = 2
ab_cornea = 3


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
kidney_mean = EQD.Tolerance('Kidney', 'Some failure', ab_kidney, fractions_kidney, 15, 'Mean', 'Conventional RT')
kidney_v20_adx = EQD.Tolerance('Kidney', 'Some failure', ab_kidney, fractions_kidney, 28, 'Volume receiving tolerance dose being less than 20%', 'Conventional RT')
kidney_v30_adx = EQD.Tolerance('Kidney', 'Some failure', ab_kidney, fractions_kidney, 23, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
kidney_v32_adx = EQD.Tolerance('Kidney', 'Some failure', ab_kidney, fractions_kidney, 20, 'Volume receiving tolerance dose being less than 32%', 'Conventional RT')
kidney_v55_adx = EQD.Tolerance('Kidney', 'Some failure', ab_kidney, fractions_kidney, 12, 'Volume receiving tolerance dose being less than 12%', 'Conventional RT')
lung_mean = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_lung, 20, 'Mean', 'Conventional RT')
lung_v35_adx = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_lung, 20, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
lung_v65_adx = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_lung, 5, 'Volume receiving tolerance dose being less than 65%', 'Conventional RT')
heart_mean = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_heart, 20, 'Mean', 'Conventional RT')
heart_v25_adx = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_heart, 50, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
heart_v30_adx = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_heart, 60, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
heart_v60_adx = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_heart, 45, 'Volume receiving tolerance dose being less than 60%', 'Conventional RT')
heart_v80_adx = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_heart, 40, 'Volume receiving tolerance dose being less than 80%', 'Conventional RT')
spinalcord_v2_adx = EQD.Tolerance('SpinalCord', 'Some failure', ab_spinalcord, fractions_spinalcord, 50, 'Volume receiving tolerance dose being less than 2 cm3', 'Conventional RT')
spinalcanal_v2_adx = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_spinalcord, 50, 'Volume receiving tolerance dose being less than 2 cm3', 'Conventional RT')
spinalcanal_chemo_v2_adx = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_spinalcord, 45, 'Volume receiving tolerance dose being less than 2 cm3', 'Conventional RT')
esophagus_mean = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_esophagus, 34, 'Mean', 'Conventional RT')
esophagus_v15_adx = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_esophagus, 60, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')
esophagus_v17_adx = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_esophagus, 60, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')


# Breast
lung_v15_adx = EQD.Tolerance('Lung_L', 'Some failure', ab_lung, fractions_breast_15, 18, 'Volume receiving tolerance dose being less than 15%', 'Conventional RT')
heart_mean_breast = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_breast, 2, 'Mean', 'Conventional RT')
heart_mean_breast_15 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_breast_15, 2, 'Mean', 'Conventional RT')
humeral_v33_adx = EQD.Tolerance('Humeral', 'Some failure', ab_humeral, fractions_breast, 25, 'Volume receiving tolerance dose being less than 5 cm3', 'Conventional RT')
contralat_breast_mean = EQD.Tolerance('Breast', 'Some failure', ab_breast, fractions_breast, 3, 'Mean', 'Conventional RT')
lung_v35_adx_25 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_breast, 20, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
lung_v35_adx_15 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_breast_15, 18, 'Volume receiving tolerance dose being less than 35%', 'Conventional RT')
lung_v65_adx_25 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_breast, 5, 'Volume receiving tolerance dose being less than 65%', 'Conventional RT')
lad_v100_adx = EQD.Tolerance('LAD', 'Some failure', ab_lad, fractions_breast, 20, 'Volume receiving tolerance dose being less than 100%', 'Conventional RT')
lad_v100_adx_15 = EQD.Tolerance('LAD', 'Some failure', ab_lad, fractions_breast_15, 20, 'Volume receiving tolerance dose being less than 100%', 'Conventional RT')
ipsilateral_breast_v50_adx = EQD.Tolerance('Breast_L/R','Some failure', ab_heart, fractions_breast_15, 40,'Volume receiving tolerance dose being less than 50%', 'Conventional RT' )
esophagus_mean_brt = EQD.Tolerance('Esophagus', 'Esophagitis grade 2', ab_esophagus, 25, 11, 'Mean', 'Conventional RT')
esophagus_v30_adx_brt = EQD.Tolerance('Esophagus', 'Esophagitis grade 2', ab_esophagus, 25, 10, 'Volume receiving tolerance dose being less than 30%', 'Conventional RT')
esophagus_v15_adx_brt = EQD.Tolerance('Esophagus', 'Esophagitis grade 2', ab_esophagus, 25, 20, 'Volume receiving tolerance dose being less than 15%', 'Conventional RT')
thyroid_mean_brt = EQD.Tolerance('ThyroidGland', 'Hypothyroidism', ab_thyroid, 25, 11.8, 'Mean', 'Conventional RT')
thyroid_v8_5cc_adx_brt = EQD.Tolerance('ThyroidGland', 'Hypothyroidism', ab_thyroid, 25, 20, 'More than 8.5 cm^3 should receive less than the tolerance dose', 'Conventional RT')


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


# SBRT:


# Lung SBRT 3 fractions
spinal_canal_sbrt_3fx_v1_2 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_3, 12.3, 'Volume receiving tolerance dose being less than 1.2 cm3', 'SBRT')
spinal_canal_sbrt_3fx_v0 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_3, 22, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
esophagus_sbrt_3fx_v5 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_3, 17.7, 'Volume receiving tolerance dose being less than 5 cm3', 'SBRT')
esophagus_sbrt_3fx_v0 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_3, 25.2, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
greatves_sbrt_3fx_v10 = EQD.Tolerance('GreatVes', 'Some failure', ab_greatves, fractions_sbrt_3, 39, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
greatves_sbrt_3fx_v0 = EQD.Tolerance('GreatVes', 'Some failure', ab_greatves, fractions_sbrt_3, 45, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
main_bronchus_sbrt_3fx_v0 = EQD.Tolerance('Main Bronchus', 'Some failure', ab_bronchus, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
main_bronchus_sbrt_3fx_v4 = EQD.Tolerance('Main Bronchus', 'Some failure', ab_bronchus, fractions_sbrt_3, 15, 'Volume receiving tolerance dose being less than 4 cm3', 'SBRT')
heart_sbrt_3fx_v15 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_3, 24, 'Volume receiving tolerance dose being less than 15 cm3', 'SBRT')
heart_sbrt_3fx_v0 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
liver_sbrt_3fx_mean = EQD.Tolerance('Liver', 'Some failure', ab_liver, fractions_sbrt_3, 15, 'Mean', 'SBRT')
liver_sbrt_3fx_v700 = EQD.Tolerance('Liver', 'Some failure', ab_liver, fractions_sbrt_3, 17, 'Volume receiving tolerance dose being less than 700 cm3', 'SBRT')
lung_contra_sbrt_3fx_mean = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_3, 3.6, 'Mean', 'SBRT')
lung_sbrt_3fx_v10 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_3, 20, 'Volume receiving tolerance dose being less than 10%', 'SBRT')
lung_sbrt_3fx_v1500 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_3, 11.6, 'Volume receiving tolerance dose being less than 1500cm3', 'SBRT')
lung_sbrt_3fx_v1000 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_3, 12.4, 'Volume receiving tolerance dose being less than 1000cm3', 'SBRT')
lung_sbrt_3fx_v37 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_3, 4.5, 'Volume receiving tolerance dose being less than 37%', 'SBRT')
lung_sbrt_3fx_v40 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_3, 10, 'Volume receiving tolerance dose being less than 40%', 'SBRT')
trachea_sbrt_3fx_v4 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_3, 15, 'Volume receiving tolerance dose being less than 4cm3', 'SBRT')
trachea_sbrt_3fx_v0 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
chestwall_sbrt_3fx_v30 = EQD.Tolerance('Chestwall', 'Some failure', ab_chestwall, fractions_sbrt_3, 30, 'Volume receiving tolerance dose being less than 30cm3', 'SBRT')
ribs_sbrt_3fx_v2 = EQD.Tolerance('Ribs', 'Some failure', ab_ribs, fractions_sbrt_3, 27, 'Volume receiving tolerance dose being less than 2cm3', 'SBRT')
ribs_sbrt_3fx_v0 = EQD.Tolerance('Ribs', 'Some failure', ab_ribs, fractions_sbrt_3, 53.76, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
skin_sbrt_3fx_v10 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_3, 22.5, 'Volume receiving tolerance dose being less than 10cm3', 'SBRT')
skin_sbrt_3fx_v0 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_3, 24, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')


# Lung SBRT 5 fractions
spinal_canal_sbrt_5fx_v1_2 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_5, 14.5, 'Volume receiving tolerance dose being less than 1.2 cm3', 'SBRT')
spinal_canal_sbrt_5fx_v0 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_5, 30, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
esophagus_sbrt_5fx_v5 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_5, 19.5, 'Volume receiving tolerance dose being less than 5 cm3', 'SBRT')
esophagus_sbrt_5fx_v0 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_5, 35, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
greatves_sbrt_5fx_v10 = EQD.Tolerance('GreatVes', 'Some failure', ab_greatves, fractions_sbrt_5, 47, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
greatves_sbrt_5fx_v0 = EQD.Tolerance('GreatVes', 'Some failure', ab_greatves, fractions_sbrt_5, 53, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
main_bronchus_sbrt_5fx_v0 = EQD.Tolerance('Main Bronchus', 'Some failure', ab_bronchus, fractions_sbrt_5, 38, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
main_bronchus_sbrt_5fx_v4 = EQD.Tolerance('Main Bronchus', 'Some failure', ab_bronchus, fractions_sbrt_5, 18, 'Volume receiving tolerance dose being less than 4 cm3', 'SBRT')
heart_sbrt_5fx_v15 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_5, 32, 'Volume receiving tolerance dose being less than 15 cm3', 'SBRT')
heart_sbrt_5fx_v0 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_5, 38, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
liver_sbrt_5fx_v700 = EQD.Tolerance('Liver', 'Some failure', ab_liver, fractions_sbrt_5, 21, 'Volume receiving tolerance dose being less than 700 cm3', 'SBRT')
lung_contra_sbrt_5fx_mean = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_5, 3.6, 'Mean', 'SBRT')
lung_contra_sbrt_5fx_v26 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_5, 5, 'Volume receiving tolerance dose being less than 26%', 'SBRT')
lung_sbrt_5fx_v1500 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_5, 12.5, 'Volume receiving tolerance dose being less than 1500cm3', 'SBRT')
lung_sbrt_5fx_v1000 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_5, 13.5, 'Volume receiving tolerance dose being less than 1000cm3', 'SBRT')
lung_sbrt_5fx_v37 = EQD.Tolerance('Lung', 'Some failure', ab_lung, fractions_sbrt_5, 5, 'Volume receiving tolerance dose being less than 37%', 'SBRT')
trachea_sbrt_5fx_v4 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_5, 18, 'Volume receiving tolerance dose being less than 4cm3', 'SBRT')
trachea_sbrt_5fx_v0 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_5, 38, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
chestwall_sbrt_5fx_v30 = EQD.Tolerance('Chestwall', 'Some failure', ab_chestwall, fractions_sbrt_5, 30, 'Volume receiving tolerance dose being less than 30cm3', 'SBRT')
ribs_sbrt_5fx_v1 = EQD.Tolerance('Ribs', 'Some failure', ab_ribs, fractions_sbrt_5, 35, 'Volume receiving tolerance dose being less than 2cm3', 'SBRT')
skin_sbrt_5fx_v10 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_5, 32, 'Volume receiving tolerance dose being less than 10cm3', 'SBRT')
skin_sbrt_5fx_v0 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_5, 30, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')


# Lung SBRT 8 fractions
esophagus_sbrt_8fx_v0 = EQD.Tolerance('Esophagus', 'Some failure', ab_esophagus, fractions_sbrt_8, 41.6, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
heart_sbrt_8fx_v0 = EQD.Tolerance('Heart', 'Some failure', ab_heart, fractions_sbrt_8, 41.6, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_canal_sbrt_8fx_v0 = EQD.Tolerance('SpinalCanal', 'Some failure', ab_spinalcord, fractions_sbrt_8, 33.6, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
trachea_sbrt_8fx_v0 = EQD.Tolerance('Trachea', 'Some failure', ab_trachea, fractions_sbrt_8, 56, 'Volume receiving tolerance dose being less than 0cm3', 'SBRT')
main_bronchus_sbrt_8fx_v0 = EQD.Tolerance('Main Bronchus', 'Some failure', ab_bronchus, fractions_sbrt_8, 56, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
main_bronchus_contra_sbrt_8fx_v0 = EQD.Tolerance('Main Bronchus', 'Some failure', ab_bronchus, fractions_sbrt_8, 48.8, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')


# Brain SRT 1 fraction
cochlea_srt_1fx_v0 = EQD.Tolerance('Cochlea_L', 'Some failure', ab_cochlea, fractions_sbrt_1, 9, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
optic_nrv_srt_1fx_v0 = EQD.Tolerance('OpticNrv_L','Some failure', ab_optic_nerve, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
optic_nrv_srt_1fx_v0_2 = EQD.Tolerance('OpticNrv_L','Some failure', ab_optic_nerve, fractions_sbrt_1, 8, 'Volume receiving tolerance dose being less than 0.2 cm3', 'SBRT')
optic_chiasm_srt_1fx_v0 = EQD.Tolerance('OpticChiasm', 'Some failure', ab_optic_chiasm, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
optic_chiasm_srt_1fx_v0_2 = EQD.Tolerance('OpticChiasm', 'Some failure', ab_optic_chiasm, fractions_sbrt_1, 8, 'Volume receiving tolerance dose being less than 0.2 cm3', 'SBRT')
eye_srt_1fx_v0 = EQD.Tolerance('Eye_R','Some failure', ab_eye, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
lens_srt_1fx_v0 = EQD.Tolerance('Lens_L','Some failure', ab_lens, fractions_sbrt_1, 3, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
brainstem_srt_1fx_v0 = EQD.Tolerance('Brainstem', 'Some failure', ab_brainstem, fractions_sbrt_1, 12.5, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
brainstem_srt_1fx_v0_5 = EQD.Tolerance('Brainstem', 'Some failure', ab_brainstem, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0.5 cm3', 'SBRT')
brain_srt_1fx_v10 = EQD.Tolerance('Brain', 'Some failure', ab_brain, fractions_sbrt_1, 12, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
skin_srt_1fx_v10 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_1, 14.4, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
spinal_cord_srt_1fx_v0 = EQD.Tolerance('SpinalCord', 'Some failure', ab_spinalcord, fractions_sbrt_1, 12.5, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_cord_srt_1fx_v0_25 = EQD.Tolerance('SpinalCord', 'Some failure', ab_spinalcord, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 0.25 cm3', 'SBRT')


# Brain SRT 3 fractions
cochlea_srt_3fx_v0 = EQD.Tolerance('Cochlea_L', 'Some failure', ab_cochlea, fractions_sbrt_3, 17, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
optic_nrv_srt_3fx_v0 = EQD.Tolerance('OpticNrv_L','Some failure', ab_optic_nerve, fractions_sbrt_3, 19.5, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
optic_nrv_srt_3fx_v0_2 = EQD.Tolerance('OpticNrv_R','Some failure', ab_optic_nerve, fractions_sbrt_3, 15, 'Volume receiving tolerance dose being less than 0.2 cm3', 'SBRT')
optic_chiasm_srt_3fx_v0 = EQD.Tolerance('OpticChiasm', 'Some failure', ab_optic_chiasm, fractions_sbrt_3, 19.5, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
optic_chiasm_srt_3fx_v0_2 = EQD.Tolerance('OpticChiasm', 'Some failure', ab_optic_chiasm, fractions_sbrt_3, 15, 'Volume receiving tolerance dose being less than 0.2 cm3', 'SBRT')
eye_srt_3fx_v0 = EQD.Tolerance('Eye_L','Some failure', ab_eye, fractions_sbrt_3, 18, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
lens_srt_3fx_v0 = EQD.Tolerance('Lens_R','Some failure', ab_lens, fractions_sbrt_3, 7, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
brainstem_srt_3fx_v0 = EQD.Tolerance('Brainstem', 'Some failure', ab_brainstem, fractions_sbrt_3, 23, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
brainstem_srt_3fx_v0_5 = EQD.Tolerance('Brainstem', 'Some failure', ab_brainstem, fractions_sbrt_3, 18, 'Volume receiving tolerance dose being less than 0.5 cm3', 'SBRT')
brain_srt_3fx_v10 = EQD.Tolerance('Brain', 'Some failure', ab_brain, fractions_sbrt_3, 20, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
skin_srt_3fx_v10 = EQD.Tolerance('Skin', 'Some failure', ab_skin, fractions_sbrt_3, 22.5, 'Volume receiving tolerance dose being less than 10 cm3', 'SBRT')
spinal_cord_srt_3fx_v0 = EQD.Tolerance('SpinalCord', 'Some failure', ab_spinalcord, fractions_sbrt_3, 20, 'Volume receiving tolerance dose being less than 0 cm3', 'SBRT')
spinal_cord_srt_3fx_v0_25 = EQD.Tolerance('SpinalCord', 'Some failure', ab_spinalcord, fractions_sbrt_3, 18, 'Volume receiving tolerance dose being less than 0.25 cm3', 'SBRT')


# Bone/Spine SBRT 1 fractions
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
kidney_3fx_v10 = EQD.Tolerance('Kidney_Hilum', 'Some failure', ab_kidney_hilum, fractions_sbrt_1, 10, 'Volume receiving tolerance dose being less than 1/10 volume', 'SBRT')
kidneys_col_3fx_v200 = EQD.Tolerance('Kidneys', 'Some failure', ab_kidneys, fractions_sbrt_3, 16, 'Volume receiving tolerance dose being less than 200cm3', 'SBRT')
