# encoding: utf8

# Import local files:
import margin as MARGIN

# Examples:
# MARGIN.Expansion(superior, inferior, anterior, posterior, right, left)
# MARGIN.Contraction(superior, inferior, anterior, posterior, right, left)


# Commonly used margins:
zero = MARGIN.Expansion(0, 0, 0, 0, 0, 0)


# Expansion margins:
uniform_20mm_expansion = MARGIN.Expansion(2, 2, 2, 2, 2, 2) # (Brain tumor CTV)
bladder_expansion = MARGIN.Expansion(2, 1.5, 1.5, 1.5, 1.5, 1.5)
uniform_1mm_expansion = MARGIN.Expansion(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
uniform_2mm_expansion = MARGIN.Expansion(0.2, 0.2, 0.2, 0.2, 0.2, 0.2) # (SRT, Cranial PRVs)
uniform_3mm_expansion = MARGIN.Expansion(0.3, 0.3, 0.3, 0.3, 0.3, 0.3) # (Brain, Head & Neck PTV)
uniform_5mm_expansion = MARGIN.Expansion(0.5, 0.5, 0.5, 0.5, 0.5, 0.5) # (Standard extra cranial daily online bone match IGRT)
uniform_7mm_expansion = MARGIN.Expansion(0.7, 0.7, 0.7, 0.7, 0.7, 0.7)
uniform_10mm_expansion = MARGIN.Expansion(1.0, 1.0, 1.0, 1.0, 1.0, 1.0) # (Seminal vesicles, cases of poor fixation)
uniform_15mm_expansion = MARGIN.Expansion(1.5, 1.5, 1.5, 1.5, 1.5, 1.5)
lung_sclc_without_4dct = MARGIN.Expansion(1.5, 1.5, 1.3, 1.3, 1.3, 1.3)
prostate_seed_expansion = MARGIN.Expansion(0.7, 0.7, 0.7, 0.7, 0.5, 0.5)
prostate_lymph_nodes_seed_expansion = MARGIN.Expansion(1.0, 1.0, 1.0, 1.0, 0.7, 0.7)
prostate_bone_match_expansion = MARGIN.Expansion(1.2, 1.2, 1, 1, 0.8, 0.8)
rectum_ctv_primary_risk_expansion = MARGIN.Expansion(0.5, 0.5, 0.8, 0.5, 0.5, 0.5)
rectum_ptv_50_expansion = MARGIN.Expansion(0.7, 0.7, 1, 0.7, 0.7, 0.7)


# Contraction margins:
uniform_5mm_contraction = MARGIN.Contraction(0.5, 0.5, 0.5, 0.5, 0.5, 0.5) # (typically used with external)
