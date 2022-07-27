# encoding: utf8

# Import local files:
import margin as MARGIN

# Examples:
# MARGIN.Expansion(superior, inferior, anterior, posterior, right, left)
# MARGIN.Contraction(superior, inferior, anterior, posterior, right, left)


# Commonly used margins:
zero = MARGIN.Expansion(0, 0, 0, 0, 0, 0)


# Expansion margins:
# Uniform:
uniform_1mm_expansion = MARGIN.Expansion(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
uniform_2mm_expansion = MARGIN.Expansion(0.2, 0.2, 0.2, 0.2, 0.2, 0.2) # (SRT, Cranial PRVs)
uniform_3mm_expansion = MARGIN.Expansion(0.3, 0.3, 0.3, 0.3, 0.3, 0.3) # (Brain, Head & Neck PTV)
uniform_5mm_expansion = MARGIN.Expansion(0.5, 0.5, 0.5, 0.5, 0.5, 0.5) # (Standard extra cranial daily online bone match IGRT)
uniform_7mm_expansion = MARGIN.Expansion(0.7, 0.7, 0.7, 0.7, 0.7, 0.7)
uniform_8mm_expansion = MARGIN.Expansion(0.8, 0.8, 0.8, 0.8, 0.8, 0.8)
uniform_10mm_expansion = MARGIN.Expansion(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
uniform_15mm_expansion = MARGIN.Expansion(1.5, 1.5, 1.5, 1.5, 1.5, 1.5)
uniform_20mm_expansion = MARGIN.Expansion(2, 2, 2, 2, 2, 2) # (Brain tumor CTV)
# Custom expansion margins:
abdomen_near_lung_soft_tissue_expansion = MARGIN.Expansion(1.0, 1.0, 0.7, 0.7, 0.7, 0.7)
bladder_expansion = MARGIN.Expansion(2, 1.5, 1.5, 1.5, 1.5, 1.5)
breast_left_robustness = MARGIN.Expansion(0, 0, 1.5, 0, 0, 1.5) # (0.5 + 1.0 cm)
breast_right_robustness = MARGIN.Expansion(0, 0, 1.5, 0, 1.5, 0) # (0.5 + 1.0 cm)
lung_sclc_without_4dct = MARGIN.Expansion(1.5, 1.5, 1.3, 1.3, 1.3, 1.3)
prostate_ctv = MARGIN.Expansion(0.0, 0.3, 0.3, 0.3, 0.3, 0.3)
prostate_bone_match_expansion = MARGIN.Expansion(1.0, 1.0, 1.0, 1.0, 0.5, 0.5)
prostate_lymph_nodes_seed_expansion = MARGIN.Expansion(1.0, 1.0, 1.0, 1.0, 0.5, 0.5)
prostate_seed_expansion = MARGIN.Expansion(0.7, 0.7, 0.7, 0.7, 0.5, 0.5)
rectum_ctv_primary_risk_expansion = MARGIN.Expansion(0.5, 0.5, 0.8, 0.5, 0.5, 0.5)
rectum_ptv_50_expansion = MARGIN.Expansion(0.7, 0.7, 1, 0.7, 0.7, 0.7)


# Contraction margins:
uniform_5mm_contraction = MARGIN.Contraction(0.5, 0.5, 0.5, 0.5, 0.5, 0.5) # (typically used with external)
uniform_2mm_contraction = MARGIN.Contraction(0.2, 0.2, 0.2, 0.2, 0.2, 0.2) 