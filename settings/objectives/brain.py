# encoding: utf8

# A class with objective settings for Brain.
#
# Authors:
# Christoffer Lervåg
# Helse Møre og Romsdal HF
#
# Python 3.6

import gui_functions as GUIF
import margins as MARGINS
import objective_functions as OF
import patient_model_functions as PMF
import region_codes as RC
import roi as ROI
import roi_functions as ROIF
import rois as ROIS
import tolerance_doses as TOL
import structure_set_functions as SSF


class Brain:

  # Creates a Brain objectives instance.
  def __init__(self, ss, plan, prescription, pm, examination):
    # Database attributes:
    self.ss = ss
    self.plan = plan
    self.prescription = prescription
    self.pm = pm
    self.examination = examination
    self.targets = self.create_target_objectives(ss, plan, prescription, pm, examination)
    self.others = self.create_other_objectives(ss, plan, prescription)
    self.oars = self.create_oar_objectives(ss, plan, prescription, pm, examination)


  # Create OAR objectives.
  def create_oar_objectives(self, ss, plan, prescription, pm, examination):
    oars = []
    if prescription.is_stereotactic():
      # Stereotactic brain:
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      for i in range(0, nr_targets):
        oars.append(OF.max_eud(ss, plan, ROIS.brain_ptv.name, 0.08*prescription.total_dose*100, 1.3, 1, beam_set_index = i))
        oars.append(OF.max_eud(ss, plan, ROIS.brain_ptv.name, 0.06*prescription.total_dose*100, 1, 1, beam_set_index = i))
    else:
      # Conventional brain:
      if prescription.region_code in RC.brain_whole_codes:
        # Whole brain:
        oars.append(OF.max_eud(ss, plan, ROIS.lens_l.name, 8*100, 1, 2))
        oars.append(OF.max_eud(ss, plan, ROIS.lens_r.name, 8*100, 1, 2))
        oars.append(OF.max_eud(ss, plan, ROIS.nasal_cavity.name, 14*100, 1, 2))
      else:
        # Partial brain:
        if prescription.region_code not in RC.brain_whole_codes:  
          # Objectives for prioritized OARs:
          oars.append(OF.max_dose(ss, plan, ROIS.brainstem_surface.name, (TOL.brainstem_surface_v003_adx.equivalent(prescription.nr_fractions)*100)-50, 60))
          oars.append(OF.max_dose(ss, plan, ROIS.brainstem_core.name, (TOL.brainstem_core_v003_adx.equivalent(prescription.nr_fractions)*100)-50, 80))
          oars.append(OF.max_dose(ss, plan, ROIS.optic_chiasm.name, (TOL.optic_chiasm_v003_adx.equivalent(prescription.nr_fractions)*100)-50, 40))
          oars.append(OF.max_dose(ss, plan, ROIS.optic_nrv_l.name, (TOL.optic_nrv_v003_adx.equivalent(prescription.nr_fractions)*100)-50, 20))
          oars.append(OF.max_dose(ss, plan, ROIS.optic_nrv_r.name, (TOL.optic_nrv_v003_adx.equivalent(prescription.nr_fractions)*100)-50, 20))
          # Setup of objectives for less prioritized OARs:
          other_oars = [ROIS.cochlea_l, ROIS.cochlea_r, ROIS.hippocampus_l, ROIS.hippocampus_r, ROIS.lens_l, ROIS.lens_r, ROIS.lacrimal_l, ROIS.lacrimal_r, ROIS.retina_l, ROIS.retina_r, ROIS.cornea_r, ROIS.cornea_l, ROIS.pituitary]
          tolerances = [TOL.cochlea_mean_tinnitus, TOL.cochlea_mean_tinnitus, TOL.hippocampus_v40, TOL.hippocampus_v40, TOL.lens_v003_adx, TOL.lens_v003_adx, TOL.lacrimal_mean, TOL.lacrimal_mean, TOL.retina_v003_adx, TOL.retina_v003_adx, TOL.cornea_v003_adx, TOL.cornea_v003_adx, TOL.pituitary_mean]
          for i in range(len(other_oars)):
            if SSF.has_named_roi_with_contours(ss, other_oars[i].name):
              weight = None
              # Conflict with dose?
              if tolerances[i].equivalent(prescription.nr_fractions) < prescription.total_dose*0.95:
                # Conflict with dose:
                if not SSF.roi_overlap(pm, examination, ss, ROIS.ptv, other_oars[i], 2):
                  if ROIF.roi_vicinity_approximate(SSF.rg(ss, ROIS.ptv.name), SSF.rg(ss, other_oars[i].name), 2):
                    # OAR is close, but not overlapping:
                    weight = 2
                  else:
                    weight = 20
              else:
                # No conflict with dose:
                weight = 20
              # Create objective if indicated:
              if weight:
                if other_oars[i].name in  [ROIS.cochlea_r.name, ROIS.cochlea_l.name, ROIS.lacrimal_l.name, ROIS.lacrimal_r.name, ROIS.hippocampus_l.name, ROIS.hippocampus_r.name, ROIS.pituitary.name]:
                  oars.append(OF.max_eud(ss, plan, other_oars[i].name, tolerances[i].equivalent(prescription.nr_fractions)*100-50, 1, weight))
                else:
                  oars.append(OF.max_dose(ss, plan, other_oars[i].name, (tolerances[i].equivalent(prescription.nr_fractions)*100)-50, weight))
            else:
              GUIF.handle_missing_roi_for_objective(other_oars[i].name)
    return oars


  # Create other objectives (e.q. External).
  def create_other_objectives(self, ss, plan, prescription):
    others = []
    if prescription.is_stereotactic():
      # Stereotactic brain:
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      for i in range(0, nr_targets):
        others.append(OF.fall_off(ss, plan, ROIS.body.name, prescription.total_dose*100, prescription.total_dose*100/2, 0.8, 25, beam_set_index = i))
      if nr_targets == 1:
        # Single target:
        others.append(OF.fall_off(ss, plan, ROIS.z_ptv_wall.name, prescription.total_dose*100, 0.7*prescription.total_dose*100, 0.6, 25, beam_set_index = 0))
      else:
        # Multiple targets:
        for i in range(0, nr_targets):
          others.append(OF.fall_off(ss, plan, "zPTV"+str(i+1)+"_Wall", prescription.total_dose*100, 0.7*prescription.total_dose*100, 0.6, 25, beam_set_index = i))
    else:
      # Conventional brain:
      others.append(OF.fall_off(ss, plan, ROIS.external.name, prescription.total_dose*100, prescription.total_dose*100/2, 1.5, 30))
      others.append(OF.max_dose(ss, plan, ROIS.external.name, prescription.total_dose*100*1.05, 30))
    return others
  
  
  # Create target objectives.
  def create_target_objectives(self, ss, plan, prescription, pm, examination):
    targets = []
    if prescription.is_stereotactic():
      # Stereotactic brain:
      nr_targets = SSF.determine_nr_of_indexed_ptvs(ss)
      if nr_targets == 1:
        # Single target:
        targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100, 200, beam_set_index = 0))
      else:
        # Multiple targets:
        for i in range(0, nr_targets):
          targets.append(OF.min_dose(ss, plan, ROIS.ptv.name+str(i+1), prescription.total_dose*100, 200, beam_set_index = i))
    else:
      # Conventional brain:
      targets.append(OF.max_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*1.03, 80))
      if prescription.region_code in RC.brain_whole_codes:
        # Whole brain:
        targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 30))
        targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.97, 150))
      else:
        # Partial brain:
        prioritized_oars = [ROIS.brainstem_core, ROIS.brainstem_surface, ROIS.optic_chiasm, ROIS.optic_nrv_l, ROIS.optic_nrv_r]
        tolerances = [TOL.brainstem_core_v003_adx, TOL.brainstem_surface_v003_adx, TOL.optic_chiasm_v003_adx, TOL.optic_nrv_v003_adx, TOL.optic_nrv_v003_adx]
        conflict_oars = []
        for i in range(len(prioritized_oars)):
          if tolerances[i].equivalent(prescription.nr_fractions) < prescription.total_dose*0.95:
            conflict_oars.append(prioritized_oars[i])
        # Setup of min and uniform doses depends on presence of critical overlaps or not:
        if len(conflict_oars) > 0:
          # Create subtraction and intersect ROIs for planning of conflicting sites:
          ctv_oars = ROI.ROIAlgebra(ROIS.ctv_oars.name, ROIS.ctv_oars.type, ROIS.ctv.color, sourcesA = [ROIS.ctv], sourcesB = conflict_oars, operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_2mm_expansion)
          ptv_oars = ROI.ROIAlgebra(ROIS.ptv_oars.name, ROIS.ptv_oars.type, ROIS.ptv.color, sourcesA = [ROIS.ptv], sourcesB = conflict_oars, operator = 'Subtraction', marginsA = MARGINS.zero, marginsB = MARGINS.uniform_2mm_expansion)
          ptv_and_oars = ROI.ROIAlgebra(ROIS.ptv_and_oars.name, ROIS.ptv_and_oars.type, ROIS.other_ptv.color, sourcesA = [ROIS.ptv], sourcesB = conflict_oars, operator='Intersection')
          rois = [ctv_oars, ptv_oars, ptv_and_oars]
          PMF.delete_matching_rois(pm, rois)
          for i in range(len(rois)):
            PMF.create_algebra_roi(pm, examination, ss, rois[i])
            PMF.exclude_roi_from_export(pm, rois[i].name)
          # Create objectives for the subtraction/intersect ROIs:
          targets.append(OF.uniform_dose(ss, plan, ROIS.ptv_and_oars.name, (tolerances[0].equivalent(prescription.nr_fractions)*100-50), 5)) # (Note that this assumes our OARs have the same tolerance dose...)
          targets.append(OF.uniform_dose(ss, plan, ROIS.ctv_oars.name, prescription.total_dose*100, 30))
          targets.append(OF.min_dose(ss, plan, ROIS.ptv_oars.name, prescription.total_dose*100*0.95, 150))
        else:
          targets.append(OF.uniform_dose(ss, plan, ROIS.ctv.name, prescription.total_dose*100, 30))
          targets.append(OF.min_dose(ss, plan, ROIS.ptv.name, prescription.total_dose*100*0.95, 150))
    return targets
  