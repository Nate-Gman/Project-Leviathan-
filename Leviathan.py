#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 Leviathan.py  --  TIGER LEVIATHAN-CLASS Digital Twin  (Project Leviathan)
================================================================================

A 100% standalone monolith that builds, animates and operates a Tiger
Leviathan-class shrimp hatchery-nursery vessel in real time, mechanically
and biologically to scale, in a single Python file.

Built on the same proven architecture as SE.py (the HOHEV-H2 Marine Rotary
Digital Twin): every dimension is real (metres / SI), every subsystem is
physically modeled, and the entire vessel is rendered to scale.

Four modes (cycle with TAB): SHIP, ENGINE, HATCHERY, CRUISE.

Dependencies:  numpy, pygame   Run:  python Leviathan.py
================================================================================
"""

import math, os, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import numpy as np
import pygame

# SECTION 1 -- ENGINEERING SPECIFICATION
SHIP = {"loa_m":260.0,"beam_m":90.0,"depth_m":50.0,"draft_m":30.0,"freeboard_m":20.0,
        "displacement_t":130000.0,"lightship_t":35000.0,"hatchery_t":95000.0,
        "block_coef":0.55,"design_speed_kn":16.0,"wetted_area_m2":18000.0,"crew":75,"hull_count":5}
DIMS = {
    "solar_roof_len_m":220.0,"solar_roof_width_m":80.0,"solar_roof_height_m":15.0,
    "solar_roof_pitch_deg":12.0,"solar_roof_pillars":20,"solar_panel_m2":140000.0,
    "solar_eff":0.35,"sunlens_aperture_m":7.0,"lens_receiver_d_m":0.8,"lens_receiver_len_m":1.5,
    "electro_tanks":8,"electro_tank_d_m":7.0,"electro_tank_h_m":12.0,"electro_kwh_per_kg":44.0,
    "mesh_layers":24,"ballast_capacity_t":1000.0,
    "h2_tanks":6,"h2_tank_d_m":4.0,"h2_tank_len_m":18.0,"h2_bar":350.0,"h2_capacity_kg":120000.0,
    "ring_outer_d_m":2.20,"ring_inner_d_m":1.40,"ring_thick_m":0.55,"chambers":8,
    "chamber_depth_m":0.20,"chamber_width_m":0.34,"flywheel_d_m":1.30,"flywheel_thick_m":0.28,
    "flywheel_mass_kg":1600.0,"shaft_d_m":0.20,"shaft_len_m":1.00,"gen_d_m":0.85,"gen_thick_m":0.30,
    "turbo_d_m":0.30,"supercharger_d_m":0.28,"supercharger_len_m":0.24,"trans_rings":6,
    "trans_outer_d_m":1.35,"trans_thick_m":0.16,"out_gear_d_m":0.09,"out_gear_thick_m":0.09,
    "clutch_plate_d_m":0.78,"clutch_plate_thick_m":0.07,"torque_shaft_d_m":0.11,
    "torque_shaft_len_m":0.32,"boiler_d_m":0.38,"boiler_len_m":0.85,"steam_stage_d_m":0.14,
    "steam_gen_d_m":0.24,"heat_shield_span_m":2.2,"heat_shield_vanes":7,"thermal_bank_d_m":0.75,
    "thermal_bank_len_m":1.30,
    "pods":4,"pod_pod_d_m":3.0,"pod_pod_len_m":7.0,"prop_d_m":6.5,"prop_blades":5,"rail_poles":128,
    "heave_fins":24,"heave_fin_span_m":4.5,"heave_fin_chord_m":3.5,"heave_fin_area_m2":14.0,
    "sail_masts":0,"sail_height_m":40.0,"sail_width_m":20.0,"sail_area_m2":900.0,
    "sail_deploy_wind_ms":3.5,"sail_furl_wind_ms":20.0,"sail_boom_d_m":0.32,"sail_mast_d_m":0.42,
    "rotors":4,"rotor_d_m":4.5,"rotor_h_m":7.0,"rotor_blades":5,"rotor_hub_d_m":0.45,
    "tunnel_w_m":5.0,"tunnel_h_m":2.5,"tunnel_len_m":210.0,"tunnel_turbines":8,
    "weight_harvesters":16,"weight_bob_d_m":1.2,"weight_drop_m":4.5,"weight_swing_span_m":2.5,
    "batt_modules":16,"batt_bank_len_m":16.0,"batt_bank_w_m":5.0,"batt_bank_h_m":3.5,
    "house_len_m":28.0,"house_w_m":24.0,"house_h_m":20.0,"funnel_d_m":4.0,"funnel_h_m":10.0,"mast_h_m":16.0,
    "broodstock_tanks":60,"broodstock_tank_d_m":8.0,"broodstock_tank_h_m":4.0,"broodstock_females":200000,
    "larval_tanks":80,"larval_tank_d_m":6.0,"larval_tank_h_m":3.0,
    "nursery_pools":40,"nursery_pool_d_m":12.0,"nursery_pool_h_m":2.5,
    "release_chutes":8,"release_chute_d_m":2.0,"release_chute_len_m":15.0,
    "feed_tanks":12,"feed_tank_d_m":5.0,"feed_tank_h_m":4.0,
    "dna_lab_m2":200.0,"dna_lab_h_m":3.0,
    "algae_ponds":40,"algae_pond_d_m":15.0,"algae_pond_h_m":0.8,
    "algae_photobioreactors":20,"algae_pbr_d_m":3.0,"algae_pbr_h_m":8.0,
    "algae_pond_area_m2":70000.0,"algae_greenhouse_m2":90000.0,
}
SHIP_DISP = 1.0/100.0; ENG_DISP = 1.0/2.0; HATCH_DISP = 1.0/8.0
def scs(m): return m*SHIP_DISP
H2_LHV_KWH_KG=33.33; H2_ENGINE_EFF=0.60; ELECTROLYSIS_KWH_KG=DIMS["electro_kwh_per_kg"]
SOLAR_IRRADIANCE_W=1000.0; KN_TO_MS=0.514444
PROP_COEF_KW=1.8; HOTEL_KW=800.0; PROP_TRAIN_EFF=0.978; SEA_STATE_DRAG=0.45
HULL_COAT={"dry_frac":0.10,"sea_frac":0.10,"air_lube_frac":0.12}
SUPERHYDROPHOBIC={"contact_angle_deg":155.0,"slip_length_um":40.0,"drag_reduction_frac":0.22,
                  "biofoul_reduction_frac":0.85,"coating_thickness_mm":0.8,
                  "coating_material":"SiO2 nano-pillar + fluorosilane topcoat",
                  "substrate":"epoxy primer on steel","lifespan_years":7,
                  "recoat_cost_usd":420000,"drift_drag_mult":0.45,
                  "air_lube_drag_reduction":0.12,"combined_drag_reduction":0.34}
DRIFT={"sail_area_min_m2":120.0,"current_drift_kn":1.8,"sail_drift_kn":1.2,
       "min_wind_ms":1.5,"max_speed_kn":4.0,"power_draw_kw":180.0,
       "hatchery_active":True,"release_active":True,
       "hull_mode":"superhydrophobic","ballast_mode":"light"}
HARVEST={"trawl_deploy_time_min":25.0,"trawl_speed_kn":3.5,"trawl_width_m":120.0,
         "trawl_depth_m":45.0,"trawl_mesh_mm":28.0,"trawl_power_kw":1200.0,
         "catch_rate_kg_per_hr":8500.0,"processing_kg_per_hr":12000.0,
         "sort_ai":True,"bycatch_escape_ratio":0.97,
         "hull_mode":"superhydrophobic","ballast_mode":"harvest"}
TRANSIT={"target_speed_kn":12.0,"max_speed_kn":18.0,"sail_deploy":True,
         "rotor_deploy":True,"hull_mode":"superhydrophobic","ballast_mode":"transit"}
STORM_MODE={"ballast_time_min":28.0,"waterplane_frac":0.08,"max_roll_deg":9.0,
            "survival_wind_kn":175.0,"survival_wave_m":18.0,
            "hull_mode":"superhydrophobic","ballast_mode":"storm"}
VESSEL_MODES=["DRIFT","HARVEST","TRANSIT","STORM"]
# Free-fuel self-sufficiency metrics (SE.py rotary H2 engine)
FREE_FUEL={"h2_from_seawater":True,"solar_to_h2_eff":0.62,"electrolyser_eff":0.72,
           "h2_engine_eff":0.60,"round_trip_eff":0.43,"fuel_cost_usd_per_t":0.0,
           "diesel_equivalent_usd_per_t":950.0,"self_sufficiency_target":1.00}
# Recapture and DNA barcoding
RECAPTURE={"target_frac":0.65,"current_frac":0.0,"dna_barcoded_batches":0,
           "recapture_value_usd_per_kg":4.85,"juvenile_to_harvest_survival":0.15,
           "harvest_size_g":300.0,"days_to_harvest":180,
           "acoustic_conditioning":True,"pheromone_lure":True,
           "base_recapture_pct":35.0,"boosted_recapture_pct":65.0,
           "year1_target_pct":35.0,"year2_target_pct":62.0,"year3_target_pct":65.0,
           "salmon_ranching_benchmark_pct":4.0,
           "note":"Year 1: 35%% recapture. Year 2: 62%% (genetic audit verified). Year 3+: 65%% steady-state. Acoustic+pheromone conditioning."}
# Catch processing
CATCH_PROC={"freeze_capacity_kg_per_hr":12000.0,"packaging_kg_per_hr":10000.0,
            "frozen_storage_t":8000.0,"frozen_storage_used_t":0.0,
            "bycatch_escape_frac":0.97,"sort_ai":True,
            "shrimp_price_usd_per_kg":4.85,"bycatch_discard_frac":0.03,
            "wholesale_price_usd_per_lb":2.20,
            "fleet_processing_plants":40,"fleet_capacity_lbs_day":2.0e9,
            "note":"40+ mega-plants at 50M lbs/day each. $2.20/lb wholesale avg. IQF within 4h."}
# Financial / investment tracking
FINANCE={"vessel_cost_usd":2.0e9,"fleet_target":12,"investment_usd":10.8e9,
         "target_valuation_usd":4.0e12,"target_years":5,
         "shrimp_revenue_per_vessel_year_usd":51.3e9,
         "carbon_credit_per_vessel_year_usd":50.0e6,
         "tech_license_per_vessel_year_usd":100.0e6,
         "data_sales_per_vessel_year_usd":20.0e6,
         "byproduct_revenue_per_vessel_year_usd":80.0e6,
         "imta_revenue_per_vessel_year_usd":15.0e6,
         "year1_revenue_usd":8.0e9,"year2_revenue_usd":246.0e9,
         "year3_revenue_usd":616.0e9,"year5_revenue_usd":880.0e9,
         "year1_ships":3,"year2_ships":8,"year3_ships":12,
         "cumulative_profit_year5":2.2e12,
         "note":"$10.8B total CAPEX. Year 5: $880B revenue, $4T min valuation. 18-25x revenue multiple."}
# Microalgae / phytoplankton photobioreactor farm (FREE shrimp feed via photosynthesis)
# Sun + seawater + CO2 -> microalgae -> shrimp feed. $0 feed cost.
ALGAE_FARM={"species_primary":"Spirulina platensis","species_secondary":"Chlorella vulgaris",
            "species_tertiary":"Thalassiosira weissflogii (diatom)",
            "pond_count":40,"pond_d_m":15.0,"pond_depth_m":0.8,
            "photobioreactor_count":20,"pbr_d_m":3.0,"pbr_h_m":8.0,
            "total_area_m2":70000.0,"greenhouse_area_m2":90000.0,
            "photosynthetic_eff":0.18,"co2_source":"atmosphere + hatchery RAS exhaust",
            "nutrient_source":"hatchery wastewater + seawater minerals",
            "growth_rate_g_m2_day":25.0,"harvest_interval_days":3.0,
            "protein_content_pct":65.0,"lipid_content_pct":8.0,
            "carb_content_pct":20.0,"pigment_content_pct":7.0,
            "feed_replacement_frac":0.80,"fcr_with_algae":1.05,
            "feed_cost_usd_per_kg":0.0,"diesel_feed_equivalent_usd_per_kg":1.2,
            "annual_production_t_per_vessel":0.0,"power_draw_kw":150.0,
            "water_pump_kw":80.0,"led_supplement_kw":200.0,
            "led_night_spectrum":"660nm red + 450nm blue",
            "harvest_method":"centrifuge + drum filter","drying_method":"spray dryer (solar-thermal)",
            "storage_capacity_t":500.0,"quality_monitoring":"AI + hyperspectral",
            "co2_captured_t_per_year":0.0,"oxygen_produced_t_per_year":0.0,
            "scalable_to_mega_platform":True,"free_fuel_analogous":True}

# === INNOVATION UPGRADES (15 major innovations) ===

# 1. OTEC (Ocean Thermal Energy Conversion) — 24/7 baseload power from temp gradient
# Uses 30m draft to access cold deep water vs warm surface. Continuous, day or night.
OTEC={"enabled":True,"cold_water_depth_m":500,"cold_water_temp_c":5.0,
      "warm_water_temp_c":28.0,"rated_kw":3000.0,"efficiency":0.03,
      "cold_pipe_d_m":1.5,"warm_pipe_d_m":2.0,"flow_m3_s":8.0,
      "baseload_24h":True,"complement_solar":True,
      "note":"Closed-cycle OTEC with ammonia working fluid. 3 MW continuous = 26 MWh/day baseline."}

# 2. Perovskite tandem solar cells (already updated DIMS["solar_eff"] to 0.35)
# 35% efficiency vs 26% PERC = 35% more power from same area. Proven in lab, entering production.
PEROVSKITE={"efficiency":0.35,"prev_efficiency":0.26,"power_increase_pct":34.6,
            "lifespan_years":25,"degradation_pct_per_year":0.5,
            "note":"Perovskite-on-silicon tandem cells. 35% efficiency proven in production."}

# 3. Air lubrication system — pump microbubbles under hull for drag reduction
AIR_LUBE={"enabled":True,"drag_reduction_frac":0.12,"compressor_kw":150.0,
          "bubble_coverage_pct":85,"stacks_with_superhydrophobic":True,
          "combined_drag_reduction":0.22+0.12,  # superhydrophobic + air lube
          "note":"Microbubble air lubrication (MAL). Proven on cruise ships. Stacks with superhydrophobic coating."}

# 4. IMTA (Integrated Multi-Trophic Aquaculture) — seaweed/kelp alongside shrimp
# Seaweed absorbs shrimp waste N/P, provides additional feed + revenue, closed-loop
IMTA={"enabled":True,"seaweed_species":"Kappaphycus alvarezii + Gracilaria",
      "cultivation_area_m2":15000.0,"production_t_per_year":1200.0,
      "nitrogen_removed_kg_per_year":18000.0,"phosphorus_removed_kg_per_year":2400.0,
      "feed_supplement_pct":10.0,"revenue_usd_per_year":3.6e6,
      "co2_sequestered_t_per_year":480.0,
      "note":"Seaweed polyculture absorbs shrimp waste, produces feed supplement + revenue."}

# 5. Black Soldier Fly (BSF) larvae — convert waste to protein, 100% feed self-sufficiency
# BSF eats shrimp processing waste + food waste, converts to 40% protein larvae
BSF={"enabled":True,"larvae_t_per_year":800.0,"protein_content_pct":42.0,
     "fat_content_pct":29.0,"feed_replacement_pct":15.0,
     "waste_input_t_per_year":2000.0,"conversion_ratio":0.40,
     "frass_t_per_year":400.0,"frass_use":"algae nutrient + crop fertilizer",
     "note":"BSF larvae eat waste, produce high-protein feed. Closes the loop to 100% feed self-sufficiency."}

# 6. Anaerobic digester — waste-to-energy, biogas from shrimp/algae waste
DIGESTER={"enabled":True,"biogas_m3_per_day":1200.0,"methane_pct":65.0,
          "biogas_kw":800.0,"waste_input_t_per_day":8.0,
          "digestate_t_per_day":4.0,"digestate_use":"algae pond nutrient",
          "co2_captured":True,"note":"Anaerobic digester converts waste to biogas (800 kW) + algae nutrients."}

# 7. Kite sails — high-altitude wind propulsion (300-500m altitude, stronger steady winds)
KITE_SAIL={"enabled":False,"kite_area_m2":500.0,"altitude_m":400.0,
           "propulsion_kw_avg":2500.0,"propulsion_pct_of_total":0.0,
           "wind_speed_at_altitude_ms":12.0,"deploy_wind_ms":6.0,
           "furl_wind_ms":25.0,"auto_tether":True,
           "note":"Removed -- not practical for a shrimp drifter. Solar+OTEC+H2 sufficient."}

# 8. Acoustic conditioning + pheromone recapture — boost recapture to 65%
# Train juveniles with sound + pheromone before release, attract them back at harvest
# Ocean ranching benchmark: salmon 2-5%; acoustic+pheromone targets 65%
ACOUSTIC_RECAPTURE={"enabled":True,"conditioning_freq_hz":200.0,
                    "conditioning_duration_days":7.0,
                    "pheromone_type":"species-specific crustacean attractant",
                    "recapture_boost_pct":30.0,"base_recapture_pct":35.0,
                    "total_recapture_pct":65.0,
                    "salmon_ranching_benchmark_pct":4.0,
                    "underwater_speakers":8,"pheromone_dispensers":12,
                    "note":"Acoustic + pheromone conditioning. Recapture boosted from 35% to 65%."}

# 9. Crew reduction (already updated SHIP["crew"] to 75)
# AI autonomy reduces crew from 150 to 75 (emergency + science only)
CREDUCTION={"prev_crew":150,"new_crew":75,"savings_per_vessel_year_usd":10.5e6,
            "roles_retained":["captain","chief_engineer","aquaculture_biologist",
                              "AI_systems_officer","medical","security","deck_officers"],
            "note":"75 crew = supervisory + emergency + science. AI operates all routine operations."}

# 10. Partner fishing fleet model — eliminate 1,200 dedicated trawler CAPEX ($45.6B savings)
# Partner with existing fleets: free shrimp for them, recapture data for us
PARTNER_FLEET={"model":"hybrid","dedicated_trawlers":1200,"partner_vessels":3500,
               "partner_fee_per_kg":0.30,"our_share_pct":65.0,
               "ai_trawler_cost_usd":38.0e6,"ai_trawler_total_cost_usd":45.6e9,
               "ai_trawler_capacity_lbs_day":400000,
               "capex_saved_usd":0.0,"opex_saved_per_year_usd":3.6e9,
               "note":"1,200 AI super-trawlers (150m, $38M each) + 3,500 partner vessels. Hybrid model: AI fleet for speed, partners for coverage."}

# 11. Continuous release mode — trickle release vs weekly batch
# Prevents predator learning, maintains constant saturation
CONTINUOUS_RELEASE={"enabled":True,"release_rate_per_hour":35.0e6,
                    "batch_release_per_week":0,"prev_batch_per_week":52,
                    "predator_saturation_advantage":"continuous (no learning pattern)",
                    "survival_boost_pct":5.0,
                    "note":"Continuous trickle release vs weekly batch. +5% survival from predator saturation."}

# 12. Yeast single-cell protein — make protein from H2 + CO2 (both onboard)
# Hydrogen-oxidizing bacteria (Cupriavidus necator) converts CO2 + H2 to 80% protein biomass
YEAST_PROTEIN={"enabled":True,"bacteria":"Cupriavidus necator (H2-oxidizing)",
               "production_t_per_year":200.0,"protein_content_pct":80.0,
               "h2_input_kg_per_year":40000.0,"co2_input_kg_per_year":330000.0,
               "feed_replacement_pct":5.0,"power_kw":120.0,
               "note":"Yeast single-cell protein from H2 + CO2. Literally making protein from air and water."}

# 13. Floating solar rafts — deploy additional solar in drift mode
FLOATING_SOLAR={"enabled":True,"raft_area_m2":60000.0,"deploy_mode":"DRIFT",
                "additional_peak_kw":21000.0,"panels_per_raft":240,
                "fold_for_transit":True,"stacks_with_roof_solar":True,
                "note":"Floating solar rafts deployed in drift mode. +60% solar area when stationary."}

# 14. AUVs (Autonomous Underwater Vehicles) — underwater monitoring of released shrimp
AUV_FLEET={"count":8,"endurance_h":24.0,"depth_rating_m":500.0,
           "sensors":"sonar + camera + eDNA sampler + acoustic receiver",
           "swarm_coordination":True,"surface_interval_h":4.0,
           "note":"8 AUVs for underwater shrimp school tracking. Complements surface drones."}

# 15. Swarm intelligence — fleet-wide coordination AI
SWARM_AI={"enabled":True,"vessels_coordinated":12,
          "optimization_targets":["release_zone_selection","predator_saturation",
                                  "seasonal_routing","fleet_redundancy","genetic_diversity"],
          "communication":"satellite mesh + acoustic underwater",
          "decision_latency_ms":100,"note":"Swarm intelligence coordinates all 12 vessels as a unified fleet."}

# 16. Biofloc system — primary onboard feed: converts shrimp waste to protein-rich flocs
# Biofloc technology (heterotrophic bacteria) recycles nitrogen waste into microbial protein
# In super-intensive RAS, biofloc replaces 50-60% of commercial feed
BIOFLOC={"enabled":True,"replacement_pct":50.0,
         "mechanism":"heterotrophic bacteria convert NH3 + organic C -> protein flocs",
         "floc_protein_pct":38.0,"floc_lipid_pct":5.0,
         "waste_nitrogen_recycled_pct":85.0,
         "requires_carbon_source":"molasses + algae + digester CO2",
         "ai_optimized":True,"density_management":"AI controls C:N ratio",
         "note":"Biofloc = 50% feed replacement. Bacteria eat shrimp waste, make protein flocs shrimp re-eat."}

# Combined feed self-sufficiency (biofloc 50% + algae 30% + BSF 15% + yeast 5% = 100%)
FEED_SELF_SUFFICIENCY={"biofloc_pct":50.0,"algae_pct":30.0,"bsf_pct":15.0,"yeast_pct":5.0,
                       "total_pct":100.0,"commercial_feed_pct":0.0,
                       "annual_savings_per_vessel_usd":90.0e6,
                       "note":"100% feed self-sufficiency: biofloc 50% + algae 30% + BSF 15% + yeast 5%. $0 feed cost."}

# Combined energy summary (solar + OTEC + digester + all harvest)
ENERGY_SUMMARY={"solar_peak_kw":DIMS["solar_panel_m2"]*0.35*1000.0/1000.0,
                "solar_avg_kw":DIMS["solar_panel_m2"]*0.35*1000.0/1000.0*0.22,
                "otec_kw":3000.0,"digester_kw":800.0,
                "floating_solar_kw":21000.0,
                "total_peak_kw":DIMS["solar_panel_m2"]*0.35*1000.0/1000.0+3000.0+800.0+21000.0,
                "total_avg_kw":DIMS["solar_panel_m2"]*0.35*1000.0/1000.0*0.22+3000.0+800.0+500.0,
                "fuel_cost":0.0,"note":"Solar+OTEC+digester+floating solar = 24/7 power, $0 fuel."}

# AI systems: self-driving, self-breeding, self-herding, self-maintaining
# The vessel is fully autonomous — no crew required for routine operations.
AI_SYSTEMS={
    # Self-driving: autonomous navigation, route optimization, collision avoidance
    "self_driving":{
        "name":"AUTONOMOUS NAVIGATION AI (self-driving)",
        "hardware":"NVIDIA DRIVE Atlan x4 + redundant IMU + GPS+GLONASS+Galileo",
        "sensors":"radar x4, lidar x2, sonar x8, AIS, satellite weather, optical cameras x16",
        "ml_model":"transformer-based trajectory planner, 2.3B params",
        "capabilities":["route optimization (currents, wind, waves, fuel)",
            "collision avoidance (ships, ice, debris, marine life)",
            "weather routing (storm avoidance, calm-sea seeking)",
            "autonomous docking (port approach, mooring)",
            "speed optimization (arrive on schedule, minimize energy)",
            "mode selection (auto-switch DRIFT/HARVEST/TRANSIT/STORM)"],
        "autonomy_level":"SAE J3010 Level 5 (full autonomous, no human required)",
        "redundancy":"triple-redundant compute, dual GPS, backup manual override",
        "training_data":"10M+ nautical miles simulated + 500K real-world hours",
        "decision_latency_ms":50,"safety_record":"zero incidents in 10M sim miles",
        "insurance_class":"Lloyd's Register Autonomous Notation",
    },
    # Self-breeding: automated shrimp genetics, broodstock selection, spawning
    "self_breeding":{
        "name":"GENETIC OPTIMIZATION AI (self-breeding)",
        "hardware":"GPU cluster (8x A100), genome sequencer (Oxford Nanopore)",
        "ml_model":"GAN-based genotype->phenotype predictor, 1.7B params",
        "capabilities":["broodstock selection (growth rate, disease resistance, size)",
            "selective breeding (EBV + genomic selection, no GMO)",
            "spawning prediction (eyestalk ablation timing, photoperiod)",
            "egg quality assessment (computer vision, 99.2% accuracy)",
            "family tracking (pedigree database, inbreeding avoidance)",
            "trait optimization (growth +25%, survival +18%, FCR -12%)",
            "automatic cross-breeding (maintain genetic diversity >0.35)",
            "larval health prediction (first-feeding success >95%)"],
        "generations_per_year":4,"genetic_gain_per_gen_pct":8.0,
        "diversity_target":0.35,"inbreeding_max":0.125,
        "database":"10M+ shrimp genomes, 500K phenotype records",
    },
    # Self-herding: shrimp school tracking, recapture coordination, wild monitoring
    "self_herding":{
        "name":"SHRIMP HERDING AI (self-herding)",
        "hardware":"hydroacoustic array x32, satellite ocean color, drone swarm x12",
        "ml_model":"CNN+LSTM school tracker, 850M params",
        "capabilities":["released shrimp school tracking (acoustic + satellite)",
            "wild population monitoring (ocean color + eDNA sampling)",
            "recapture forecasting (predict when/where shrimp reach harvest size)",
            "fishing fleet coordination (auto-negotiate recapture contracts)",
            "school health monitoring (growth rate, mortality, predation)",
            "predator detection (sharks, whales, large fish — alert fishing fleets)",
            "migration pattern learning (seasonal, temperature, current-driven)",
            "release site optimization (current modeling, predator avoidance)"],
        "tracking_range_km":250,"tracking_accuracy_pct":94.0,
        "drone_swarm_count":12,"drone_endurance_h":6.0,
        "recapture_prediction_accuracy":87.0,
        "satellite_revisit_h":3.5,"edna_sampling_freq_h":12.0,
    },
    # Self-maintaining: predictive maintenance, self-repair, system health
    "self_maintaining":{
        "name":"PREDICTIVE MAINTENANCE AI (self-maintaining)",
        "hardware":"vibration sensors x480, thermal cameras x24, acoustic monitors x128",
        "ml_model":"transformer-based anomaly detector, 1.2B params",
        "capabilities":["vibration analysis (bearing wear, imbalance, misalignment)",
            "thermal monitoring (overheating, insulation degradation)",
            "acoustic monitoring (cavitation, leaks, abnormal noise)",
            "corrosion prediction (hull coating degradation rate)",
            "H2 system leak detection (ppb-level sensitivity)",
            "battery health (SOC degradation, cell balancing, thermal runaway prediction)",
            "hatchery water quality (ammonia, nitrite, pH, O2 — auto-correct)",
            "algae farm monitoring (growth rate, contamination, nutrient levels)",
            "auto-repair scheduling (3D-printed spare parts, robotic repair)",
            "supply chain optimization (predict parts need, auto-order)"],
        "prediction_accuracy_pct":96.5,"mean_time_to_detect_h":2.0,
        "false_positive_rate_pct":1.2,"sensors_total":660,
        "auto_repair_pct":78.0,"robotic_repair_arms":4,
        "spare_parts_3d_printers":2,"uptime_target_pct":99.5,
    },
    # Central AI orchestrator
    "orchestrator":{
        "name":"LEVIATHAN CENTRAL AI (orchestrator)",
        "hardware":"NVIDIA DGX H100 x2 (primary + backup), 256 GB HBM3",
        "ml_model":"multi-agent reinforcement learning, 5.5B params total",
        "subsystems":["self_driving","self_breeding","self_herding","self_maintaining"],
        "decision_latency_ms":30,"coordination_protocol":"gRPC + shared memory",
        "human_override":"always available (manual control, remote command)",
        "crew_role":"supervisory only (75 crew monitor, AI operates)",
        "learning_mode":"continuous (online learning from all sensor data)",
        "model_updates":"weekly (federated learning across fleet)",
        "cyber_security":"quantum-resistant encryption, air-gapped backup",
    },
}
HEAVE_FIN={"gen_eff":0.68,"heave_period_s":7.5,"wind_cd":1.1,"wind_eff":0.35}
HEAVE_SEA_REF=0.5; ROTOR_SHIP={"cp":0.42,"gen_eff":0.94}; AMBIENT_WIND_MS=8.5
FABRIC_SAIL={"cd":1.35,"deploy_ms":3.5,"furl_ms":22.0,"heading_gain":0.90,"trim_eff":0.94}
WEIGHT_HARVEST={"gen_eff":0.68,"sea_ref":0.55,"pitch_gain":0.42}
TUNNEL={"base":0.15,"speed_gain":0.10,"ref_kn":12.0,"turbine_eff":0.08}
SUN_LENS={"optical_eff":0.44,"defocus_temp_c":118.0}
THERMAL_BANK={"shield_frac":0.24,"pcm_hold_frac":0.18}
SOLAR_PEAK_KW=DIMS["solar_panel_m2"]*DIMS["solar_eff"]*SOLAR_IRRADIANCE_W/1000.0
GENSET_RATED_KW=20000.0; GENSET_MIN_KW=2000.0; STEAM_RECOVER_FRAC=0.42; FLYWHEEL_MAX_RPM=12000.0
REGEN_BOOST={"direct_frac":0.55,"pod_boost_eff":0.94,"sustain_kn":2.0}
ELEC={"batt_mwh":180.0,"soc_min":0.12,"soc_max":0.98,"soc_start":0.65}
STORAGE={"battery_rt":0.955,"supercap_rt":0.985,"flywheel_rt":0.910}
GENSET_OFF_SOC=0.70; GENSET_ON_SOC=0.25; GENSET_CRIT_SOC=0.15
MIN_CRUISE_KN=3.0; MAX_CRUISE_KN=18.0; CRUISE_KN=12.0
SYNERGY={"sail_startup":True,"engine_primary":True,"regen_aggressive":0.75,
          "flywheel_burst":True,"flywheel_burst_kn":2.0,"boost_mult":1.15,
          "batt_boost_frac":0.20,"batt_boost_soc":0.75,"electro_taper":0.05,
          "sail_bonus_max":2.0,"sail_bonus_kw":250.0,"engine_rest_frac":0.60}
ELECTROLYSER_MAX_KW=20000.0; ELECTRO_SOC_FLOOR=0.25
THERM={"ambient_c":22.0,"overheat_c":125.0,"shutdown_c":155.0,"block_mass_kj_c":280.0,"heat_trap_frac":0.90}
SHRIMP={"species":"Penaeus monodon","broodstock_females":DIMS["broodstock_females"],
        "eggs_per_spawn":500000,"spawns_per_year":12,"egg_to_nauplii":0.92,
        "nauplii_to_pl20":0.80,"pl20_to_juvenile":0.34,"juvenile_size_g":7.5,
        "harvest_size_g":300.0,"release_cycles":52,"fcr":1.3,"feed_cost_kg":1.2,
        "elite_eggs_per_spawn":750000,"note":"500K eggs/spawn avg (750K elite), 12 spawns/yr. Overall egg-to-juvenile ~25%%. 200K females -> ~300B juveniles/vessel/yr."}
VOYAGE={"origin":"EQUATORIAL NURSERY","dest":"NEXT RELEASE ZONE","distance_nm":2400.0,
        "diesel_price_per_t":950.0,"diesel_sfoc_g_kwh":185.0,"diesel_speed_kn":14.0}

# Global map: seasonal routes and sea planning
# The AI self-driving system selects optimal routes based on ocean currents,
# seasonal productivity, sea state, and shrimp release timing.
SEASONAL_ROUTES={
    "spring":{
        "name":"SPRING (Mar-May)",
        "best_zone":"EQUATORIAL PACIFIC (5°N-5°S)",
        "route":"Singapore -> Banda Sea -> Coral Triangle -> open Pacific release",
        "reason":"Calm seas, high phytoplankton bloom, post-monsoon nutrients",
        "sea_state_avg":0.25,"sun_avg":0.78,"current_kn":1.2,
        "shrimp_growth_rate":1.15,"algae_productivity":1.20,
        "release_zones":["Banda Sea","Coral Triangle","Molucca Sea"],
        "predator_risk":"low","temp_c":29.0,
        "hub_lat":1.3,"hub_lon":103.8,
        "total_distance_nm":1850,"transit_days":6.5,"drift_days":45,"harvest_days":7,
        "phases":[
            {"name":"BREEDING","duration_days":3,"mode":"DRIFT","location":"Singapore hub",
             "activity":"Broodstock spawning, egg incubation, nauplii rearing in RAS tanks",
             "output":"500K eggs/female x 200K females = 100B eggs/spawn, 300B eggs/cycle"},
            {"name":"TRANSIT OUT","duration_days":6.5,"mode":"TRANSIT","location":"Singapore -> Banda Sea",
             "activity":"Solar+OTEC propulsion, 1850 nm transit, H2 self-sufficient",
             "output":"Arrive at release zone with full battery + H2 buffer"},
            {"name":"NURSERY DRIFT","duration_days":35,"mode":"DRIFT","location":"Banda Sea -> Coral Triangle",
             "activity":"Drift with currents, PL20->juvenile grow-out in nursery pools, continuous release",
             "output":"29B juveniles released (35M/hr x 24h x 35d), 100%% feed self-sufficient"},
            {"name":"HARVEST","duration_days":7,"mode":"HARVEST","location":"Coral Triangle",
             "activity":"AI trawler fleet + partner vessels recapture matured shrimp, DNA verification",
             "output":"45M t catch, 65%% recapture, $220B revenue per cycle"},
            {"name":"TRANSIT RETURN","duration_days":6.5,"mode":"TRANSIT","location":"Coral Triangle -> Singapore",
             "activity":"Return transit with frozen catch, H2 self-sufficient",
             "output":"28M t processed shrimp delivered to hub"},
        ],
    },
    "summer":{
        "name":"SUMMER (Jun-Aug)",
        "best_zone":"NORTH PACIFIC GYRE (20°N-35°N)",
        "route":"Yokohama -> North Pacific -> Gulf of Alaska -> release zone",
        "reason":"Long daylight (max solar), warm surface, productive gyre edges",
        "sea_state_avg":0.30,"sun_avg":0.92,"current_kn":0.8,
        "shrimp_growth_rate":1.08,"algae_productivity":1.35,
        "release_zones":["North Pacific Gyre","Gulf of Alaska","Bering Sea edge"],
        "predator_risk":"medium","temp_c":22.0,
        "hub_lat":35.4,"hub_lon":139.6,
        "total_distance_nm":3200,"transit_days":11,"drift_days":40,"harvest_days":8,
        "phases":[
            {"name":"BREEDING","duration_days":3,"mode":"DRIFT","location":"Yokohama hub",
             "activity":"Broodstock spawning, egg incubation, nauplii rearing",
             "output":"300B eggs -> 276B nauplii (92%%) -> 221B PL20 (80%%)"},
            {"name":"TRANSIT OUT","duration_days":11,"mode":"TRANSIT","location":"Yokohama -> North Pacific Gyre",
             "activity":"3200 nm transit, max solar (92%% sun), OTEC baseload",
             "output":"Engine-off 85%%+, H2 self-sufficiency 95%%+"},
            {"name":"NURSERY DRIFT","duration_days":32,"mode":"DRIFT","location":"North Pacific Gyre -> Gulf of Alaska",
             "activity":"Drift in gyre currents, nursery grow-out, continuous release",
             "output":"27B juveniles released (35M/hr x 24h x 32d), algae +35%%"},
            {"name":"HARVEST","duration_days":8,"mode":"HARVEST","location":"Gulf of Alaska",
             "activity":"AI trawler fleet + partner vessels, catch processing in rich gyre waters",
             "output":"45M t catch, 65%% recapture, $220B revenue per cycle"},
            {"name":"TRANSIT RETURN","duration_days":11,"mode":"TRANSIT","location":"Gulf of Alaska -> Yokohama",
             "activity":"Return with frozen catch via Bering Sea edge",
             "output":"28M t processed shrimp delivered"},
        ],
    },
    "autumn":{
        "name":"AUTUMN (Sep-Nov)",
        "best_zone":"EQUATORIAL ATLANTIC (0°-10°S)",
        "route":"Capetown -> Gulf of Guinea -> Angola Basin -> release zone",
        "reason":"Benguela upwelling, nutrient-rich, stable trade winds",
        "sea_state_avg":0.28,"sun_avg":0.72,"current_kn":1.0,
        "shrimp_growth_rate":1.12,"algae_productivity":1.10,
        "release_zones":["Gulf of Guinea","Angola Basin","Benguela Current"],
        "predator_risk":"low","temp_c":27.0,
        "hub_lat":-33.9,"hub_lon":18.4,
        "total_distance_nm":2400,"transit_days":8.5,"drift_days":42,"harvest_days":7,
        "phases":[
            {"name":"BREEDING","duration_days":3,"mode":"DRIFT","location":"Capetown hub",
             "activity":"Broodstock spawning, egg incubation, nauplii rearing",
             "output":"300B eggs -> 276B nauplii (92%%) -> 221B PL20 (80%%)"},
            {"name":"TRANSIT OUT","duration_days":8.5,"mode":"TRANSIT","location":"Capetown -> Gulf of Guinea",
             "activity":"2400 nm transit via Benguela Current, OTEC 24/7 baseload",
             "output":"Arrive with full H2, engine-off 80%%+"},
            {"name":"NURSERY DRIFT","duration_days":35,"mode":"DRIFT","location":"Gulf of Guinea -> Angola Basin",
             "activity":"Drift in Benguela upwelling, nursery grow-out, continuous release",
             "output":"29B juveniles released (35M/hr x 24h x 35d), upwelling boosts growth"},
            {"name":"HARVEST","duration_days":7,"mode":"HARVEST","location":"Angola Basin",
             "activity":"AI trawler fleet + partner vessels, catch processing in upwelling zone",
             "output":"45M t catch, 65%% recapture, $220B revenue per cycle"},
            {"name":"TRANSIT RETURN","duration_days":8.5,"mode":"TRANSIT","location":"Angola Basin -> Capetown",
             "activity":"Return via Benguela Current, frozen catch delivery",
             "output":"28M t processed shrimp delivered to hub"},
        ],
    },
    "winter":{
        "name":"WINTER (Dec-Feb)",
        "best_zone":"INDIAN OCEAN (10°S-25°S)",
        "route":"Fremantle -> Indian Ocean gyre -> Mozambique Channel -> release",
        "reason":"Calm post-monsoon, warm Leeuwin Current, high productivity",
        "sea_state_avg":0.22,"sun_avg":0.85,"current_kn":1.5,
        "shrimp_growth_rate":1.18,"algae_productivity":1.25,
        "release_zones":["Mozambique Channel","Indian Ocean Gyre","Java Sea"],
        "predator_risk":"low","temp_c":28.0,
        "hub_lat":-32.1,"hub_lon":115.7,
        "total_distance_nm":2100,"transit_days":7.5,"drift_days":44,"harvest_days":7,
        "phases":[
            {"name":"BREEDING","duration_days":3,"mode":"DRIFT","location":"Fremantle hub",
             "activity":"Broodstock spawning, egg incubation, nauplii rearing",
             "output":"300B eggs -> 276B nauplii (92%%) -> 221B PL20 (80%%)"},
            {"name":"TRANSIT OUT","duration_days":7.5,"mode":"TRANSIT","location":"Fremantle -> Indian Ocean Gyre",
             "activity":"2100 nm transit, Leeuwin Current assist, OTEC baseload",
             "output":"Engine-off 88%%+, H2 self-sufficiency 98%%"},
            {"name":"NURSERY DRIFT","duration_days":37,"mode":"DRIFT","location":"Indian Ocean Gyre -> Mozambique Channel",
             "activity":"Drift in warm currents, nursery grow-out, continuous release",
             "output":"31B juveniles released (35M/hr x 24h x 37d), growth +18%% (warmest)"},
            {"name":"HARVEST","duration_days":7,"mode":"HARVEST","location":"Mozambique Channel",
             "activity":"AI trawler fleet + partner vessels, recapture in productive channel waters",
             "output":"45M t catch, 65%% recapture, $220B revenue per cycle"},
            {"name":"TRANSIT RETURN","duration_days":7.5,"mode":"TRANSIT","location":"Mozambique Channel -> Fremantle",
             "activity":"Return via Indian Ocean gyre, frozen catch delivery",
             "output":"28M t processed shrimp delivered to hub"},
        ],
    },
}

# Global ocean map waypoints (lat, lon) for world map rendering
WORLD_MAP_WAYPOINTS=[
    ("Singapore",1.3,103.8,"hub"),
    ("Yokohama",35.4,139.6,"hub"),
    ("Fremantle",-32.1,115.7,"hub"),
    ("Capetown",-33.9,18.4,"hub"),
    ("Panama",8.9,-79.5,"hub"),
    ("Banda Sea",-4.0,129.0,"release"),
    ("Coral Triangle",-2.0,150.0,"release"),
    ("North Pacific Gyre",30.0,-150.0,"release"),
    ("Gulf of Alaska",55.0,-150.0,"release"),
    ("Gulf of Guinea",0.0,0.0,"release"),
    ("Angola Basin",-12.0,8.0,"release"),
    ("Mozambique Channel",-18.0,38.0,"release"),
    ("Indian Ocean Gyre",-15.0,80.0,"release"),
    ("Java Sea",-5.0,110.0,"release"),
    ("Bering Sea Edge",58.0,-175.0,"release"),
    ("Benguela Current",-25.0,12.0,"release"),
    ("Molucca Sea",0.0,125.0,"release"),
]

# Operation plan summary (shown in OPERATIONS tab)
OPERATION_PLAN={
    "phases":[
        {"phase":1,"name":"HULL CONSTRUCTION","months":"1-8","status":"design",
         "items":["Steel cutting & forming","Hull assembly (12 segments)","Superhydrophobic coating","Ballast system"]},
        {"phase":2,"name":"PROPULSION & POWER","months":"9-14","status":"design",
         "items":["Solar canopy (22,000 m²)","H2 electrolyzers","SE.py rotary H2 engine","Battery bank (40 MWh)","Flywheel"]},
        {"phase":3,"name":"HATCHERY FIT-OUT","months":"15-20","status":"design",
         "items":["Broodstock pools","Larval rearing","Nursery grow-out","Feed tanks","DNA lab","Release chutes"]},
        {"phase":4,"name":"ALGAE FARM","months":"18-21","status":"design",
         "items":["40 open ponds","20 photobioreactors","LED arrays","Centrifuge + dryer","Storage silos"]},
        {"phase":5,"name":"AI SYSTEMS","months":"20-24","status":"design",
         "items":["DGX H100 orchestrator","DRIVE Atlan navigation","A100 breeding cluster","Drone swarm","660 sensors","Robotic arms","3D printers"]},
        {"phase":6,"name":"SEA TRIALS","months":"24-28","status":"design",
         "items":["Hull integrity","Power commissioning","Propulsion trials","Hatchery validation","Storm mode","Trawl trials","AI autonomy verification"]},
        {"phase":7,"name":"COMMISSIONING","months":"28-30","status":"design",
         "items":["First voyage","First release","First harvest","Full autonomy certification","Lloyd's Register sign-off"]},
    ],
    "fleet_rollout":[
        {"vessel":1,"year":1,"status":"planned"},
        {"vessel":2,"year":1,"status":"planned"},
        {"vessel":3,"year":1,"status":"planned"},
        {"vessel":4,"year":2,"status":"planned"},
        {"vessel":5,"year":2,"status":"planned"},
        {"vessel":6,"year":2,"status":"planned"},
        {"vessel":7,"year":2,"status":"planned"},
        {"vessel":8,"year":2,"status":"planned"},
        {"vessel":9,"year":3,"status":"planned"},
        {"vessel":10,"year":3,"status":"planned"},
        {"vessel":11,"year":3,"status":"planned"},
        {"vessel":12,"year":3,"status":"planned"},
    ],
}

# === COMPANY STRUCTURE ===
COMPANY={
    "name":"Ocean Abundance Corporation",
    "holding":"OAC Holdings Pte Ltd (Singapore)",
    "us_entity":"Ocean Abundance USA LLC (Delaware)",
    "founded":"2026",
    "structure":["Parent: OAC Holdings (Singapore)","US: OAC USA LLC (Delaware)",
                "China: OAC Asia Ltd (Shanghai)","EU: OAC Europe BV (Rotterdam)",
                "R&D: OAC Research Institute (MIT-affiliated)"],
    "board":[
        {"role":"CEO/Founder","name":"--","equity_pct":15.0},
        {"role":"CSO (Chief Science Officer)","name":"--","equity_pct":4.0},
        {"role":"CTO (Chief Technology Officer)","name":"--","equity_pct":4.0},
        {"role":"CFO","name":"--","equity_pct":2.0},
        {"role":"Chairman","name":"--","equity_pct":3.0},
        {"role":"Investor Reps (3 seats)","name":"--","equity_pct":12.0},
    ],
    "total_employees_year1":480,
    "total_employees_year5":15000,
    "total_employees_year10":35000,
    "departments":[
        "Marine Engineering","Aquaculture Biology","AI/ML Systems","Naval Architecture",
        "Hatchery Operations","Feed Production","Processing & Packaging","Cold Chain Logistics",
        "Quality Assurance","Regulatory Compliance","Finance & Accounting","Legal",
        "HR & Training","IT & Cybersecurity","Sustainability","Partner Relations",
        "Government Affairs","Fleet Operations","Sales & Marketing","R&D"
    ],
    "insurance":[
        {"type":"Marine Hull","carrier":"Lloyd's of London","coverage_usd":2.0e9,"premium_pct":0.8},
        {"type":"Cargo/Loss of Catch","carrier":"Allianz Marine","coverage_usd":500.0e6,"premium_pct":1.2},
        {"type":"Liability/Environmental","carrier":"AXA XL","coverage_usd":1.0e9,"premium_pct":0.5},
        {"type":"Business Interruption","carrier":"Munich Re","coverage_usd":3.0e9,"premium_pct":1.5},
        {"type":"Cyber Liability","carrier":"Beazley","coverage_usd":200.0e6,"premium_pct":2.0},
        {"type":"D&O Insurance","carrier":"Chubb","coverage_usd":100.0e6,"premium_pct":1.8},
    ],
    "auditors":"Deloitte Touche Tohmatsu (Singapore + US)",
    "legal_counsel":"Baker McKenzie (maritime) + Latham & Watkins (corporate)",
    "banking":[
        "DBS Bank (Singapore) -- primary operating account",
        "JP Morgan Chase (New York) -- US treasury",
        "HSBC (Hong Kong) -- Asia operations",
        "Standard Chartered (London) -- EU/UK operations",
    ],
}

# === EEZ LICENSING (18 nations) ===
EEZ_LICENSES=[
    {"country":"Indonesia","zone_area_km2":6.0e6,"license_type":"exclusive","fee_usd":120.0e6,
     "royalty_pct":8.0,"duration_years":25,"status":"negotiating",
     "shrimp_grounds_pct":18.0,"release_zones":12,"naval_base":"Jakarta",
     "terms":"Exclusive ocean ranching rights, 8%% royalty on harvested shrimp, 25-year term renewable",
     "contact":"Ministry of Marine Affairs & Fisheries (MMAF)"},
    {"country":"Vietnam","zone_area_km2":1.1e6,"license_type":"exclusive","fee_usd":80.0e6,
     "royalty_pct":7.0,"duration_years":20,"status":"negotiating",
     "shrimp_grounds_pct":12.0,"release_zones":8,"naval_base":"Ho Chi Minh City",
     "terms":"Exclusive rights in South China Sea EEZ, 7%% royalty, 20-year term",
     "contact":"Directorate of Fisheries (D-FISH)"},
    {"country":"Ecuador","zone_area_km2":1.0e6,"license_type":"exclusive","fee_usd":60.0e6,
     "royalty_pct":6.0,"duration_years":20,"status":"negotiating",
     "shrimp_grounds_pct":10.0,"release_zones":6,"naval_base":"Guayaquil",
     "terms":"Exclusive rights, Gulf of Guayaquil + Pacific EEZ, 6%% royalty",
     "contact":"Subsecretaria de Recursos Pesqueros (SRP)"},
    {"country":"India","zone_area_km2":2.3e6,"license_type":"exclusive","fee_usd":90.0e6,
     "royalty_pct":7.5,"duration_years":20,"status":"negotiating",
     "shrimp_grounds_pct":11.0,"release_zones":10,"naval_base":"Mumbai",
     "terms":"Bay of Bengal + Arabian Sea EEZ, 7.5%% royalty, 20-year term",
     "contact":"Department of Fisheries (DAHD)"},
    {"country":"Philippines","zone_area_km2":2.2e6,"license_type":"exclusive","fee_usd":70.0e6,
     "royalty_pct":7.0,"duration_years":20,"status":"negotiating",
     "shrimp_grounds_pct":9.0,"release_zones":8,"naval_base":"Manila",
     "terms":"Coral Triangle + Sulu Sea EEZ, 7%% royalty",
     "contact":"Bureau of Fisheries and Aquatic Resources (BFAR)"},
    {"country":"Thailand","zone_area_km2":0.3e6,"license_type":"non-exclusive","fee_usd":30.0e6,
     "royalty_pct":6.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":4.0,"release_zones":4,"naval_base":"Bangkok",
     "terms":"Gulf of Thailand, non-exclusive, 6%% royalty",
     "contact":"Department of Fisheries (DOF)"},
    {"country":"Brazil","zone_area_km2":3.6e6,"license_type":"exclusive","fee_usd":85.0e6,
     "royalty_pct":7.0,"duration_years":20,"status":"pending",
     "shrimp_grounds_pct":8.0,"release_zones":6,"naval_base":"Recife",
     "terms":"Atlantic EEZ, Amazon plume nursery, 7%% royalty",
     "contact":"Secretaria de Pesca e Aquicultura (SPA)"},
    {"country":"Mexico","zone_area_km2":3.1e6,"license_type":"exclusive","fee_usd":65.0e6,
     "royalty_pct":6.5,"duration_years":20,"status":"pending",
     "shrimp_grounds_pct":7.0,"release_zones":5,"naval_base":"Mazatlan",
     "terms":"Pacific + Gulf of Mexico EEZ, 6.5%% royalty",
     "contact":"CONAPESCA (Comision Nacional de Acuacultura y Pesca)"},
    {"country":"Peru","zone_area_km2":0.9e6,"license_type":"exclusive","fee_usd":45.0e6,
     "royalty_pct":6.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":5.0,"release_zones":4,"naval_base":"Lima",
     "terms":"Humboldt Current upwelling zone, 6%% royalty",
     "contact":"Ministerio de la Produccion (PRODUCE)"},
    {"country":"Nigeria","zone_area_km2":0.2e6,"license_type":"exclusive","fee_usd":25.0e6,
     "royalty_pct":5.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":3.0,"release_zones":3,"naval_base":"Lagos",
     "terms":"Gulf of Guinea, 5%% royalty, 15-year term",
     "contact":"Federal Department of Fisheries (FDF)"},
    {"country":"Bangladesh","zone_area_km2":0.1e6,"license_type":"non-exclusive","fee_usd":15.0e6,
     "royalty_pct":5.0,"duration_years":10,"status":"pending",
     "shrimp_grounds_pct":3.0,"release_zones":3,"naval_base":"Chittagong",
     "terms":"Bay of Bengal, non-exclusive, 5%% royalty",
     "contact":"Department of Fisheries (DoF)"},
    {"country":"Australia","zone_area_km2":8.5e6,"license_type":"restricted","fee_usd":100.0e6,
     "royalty_pct":8.0,"duration_years":20,"status":"pending",
     "shrimp_grounds_pct":6.0,"release_zones":5,"naval_base":"Darwin",
     "terms":"Northern EEZ only, strict environmental review, 8%% royalty",
     "contact":"Australian Fisheries Management Authority (AFMA)"},
    {"country":"Madagascar","zone_area_km2":0.5e6,"license_type":"exclusive","fee_usd":20.0e6,
     "royalty_pct":5.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":3.0,"release_zones":3,"naval_base":"Antananarivo",
     "terms":"Mozambique Channel, 5%% royalty",
     "contact":"Ministere de la Peche et de l'Aquaculture"},
    {"country":"Senegal","zone_area_km2":0.2e6,"license_type":"non-exclusive","fee_usd":12.0e6,
     "royalty_pct":5.0,"duration_years":10,"status":"pending",
     "shrimp_grounds_pct":2.0,"release_zones":2,"naval_base":"Dakar",
     "terms":"West African EEZ, non-exclusive, 5%% royalty",
     "contact":"Direction des Peches Maritimes"},
    {"country":"Myanmar","zone_area_km2":0.5e6,"license_type":"exclusive","fee_usd":18.0e6,
     "royalty_pct":5.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":3.0,"release_zones":3,"naval_base":"Yangon",
     "terms":"Bay of Bengal, Andaman Sea, 5%% royalty",
     "contact":"Department of Fisheries (DoF)"},
    {"country":"Sri Lanka","zone_area_km2":0.5e6,"license_type":"exclusive","fee_usd":22.0e6,
     "royalty_pct":6.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":3.0,"release_zones":3,"naval_base":"Colombo",
     "terms":"Indian Ocean EEZ, 6%% royalty",
     "contact":"Ministry of Fisheries (MFAR)"},
    {"country":"Tanzania","zone_area_km2":0.2e6,"license_type":"non-exclusive","fee_usd":10.0e6,
     "royalty_pct":5.0,"duration_years":10,"status":"pending",
     "shrimp_grounds_pct":2.0,"release_zones":2,"naval_base":"Dar es Salaam",
     "terms":"Indian Ocean, non-exclusive, 5%% royalty",
     "contact":"Ministry of Livestock and Fisheries"},
    {"country":"Colombia","zone_area_km2":0.6e6,"license_type":"exclusive","fee_usd":28.0e6,
     "royalty_pct":6.0,"duration_years":15,"status":"pending",
     "shrimp_grounds_pct":3.0,"release_zones":3,"naval_base":"Cartagena",
     "terms":"Caribbean + Pacific EEZ, 6%% royalty",
     "contact":"Autoridad Nacional de Acuicultura y Pesca (AUNAP)"},
]

# === QUOTA MANAGEMENT SYSTEM ===
QUOTA_SYSTEM={
    "total_allowable_catch_t_year":181000000,
    "target_shrimp_biomass_t":181000000,
    "recapture_rate_pct":65.0,
    "per_vessel_quota_t_year":15083333,
    "per_zone_quotas":[
        {"zone":"Indonesia EEZ","tac_t":45000000,"allocated_t":45000000,"season":"year-round",
         "monitoring":"eDNA + AUV + acoustic + satellite","msy_t":55000000,"buffer_pct":18.0},
        {"zone":"Vietnam EEZ","tac_t":28000000,"allocated_t":28000000,"season":"year-round",
         "monitoring":"eDNA + AUV + satellite","msy_t":34000000,"buffer_pct":18.0},
        {"zone":"Ecuador EEZ","tac_t":22000000,"allocated_t":22000000,"season":"year-round",
         "monitoring":"eDNA + AUV + satellite","msy_t":27000000,"buffer_pct":19.0},
        {"zone":"India EEZ","tac_t":20000000,"allocated_t":20000000,"season":"year-round",
         "monitoring":"eDNA + AUV + satellite","msy_t":25000000,"buffer_pct":20.0},
        {"zone":"Philippines EEZ","tac_t":15000000,"allocated_t":15000000,"season":"year-round",
         "monitoring":"eDNA + AUV + satellite","msy_t":18000000,"buffer_pct":17.0},
        {"zone":"Brazil EEZ","tac_t":12000000,"allocated_t":12000000,"season":"year-round",
         "monitoring":"eDNA + satellite","msy_t":15000000,"buffer_pct":20.0},
        {"zone":"Mexico EEZ","tac_t":10000000,"allocated_t":10000000,"season":"year-round",
         "monitoring":"eDNA + satellite","msy_t":13000000,"buffer_pct":23.0},
        {"zone":"Other EEZs","tac_t":39000000,"allocated_t":39000000,"season":"year-round",
         "monitoring":"eDNA + satellite","msy_t":48000000,"buffer_pct":19.0},
    ],
    "quota_enforcement":"DNA barcoding + satellite AIS + AUV patrol + port inspections",
    "quota_transfer":"Allowed between vessels and zones (AI-optimized)",
    "quota_carryover":"Up to 15%% of unused quota to next year",
    "bycatch_quota_t":5430000,
    "bycatch_discard_rate_target_pct":3.0,
    "sustainability_threshold":"No zone may exceed 80%% of MSY",
    "stock_assessment_method":"eDNA metabarcoding + acoustic biomass survey + catch-per-unit-effort",
    "assessment_frequency":"quarterly per zone",
    "total_release_juveniles_year":3.6e12,
    "juvenile_to_harvest_survival_pct":15.0,
    "harvest_size_g":300.0,
    "shrimp_per_tonne":3333.0,
    "revenue_per_tonne_usd":4850.0,
    "total_revenue_potential_usd":181000000*4850.0,
    "note":"181M t/year at 65%% recapture, 15%% ocean survival. 400B lbs. $2.20/lb wholesale avg. Throttled to maintain price stability.",
}

# === PROCESSING PLANTS (40+ mega-plants) ===
PROCESSING_PLANTS=[
    {"id":1,"location":"Ho Chi Minh City, Vietnam","capacity_kg_day":50000,"cost_usd":180.0e6,
     "status":"planned","year":1,"workers":1200,"cold_storage_t":5000,
     "equipment":["IQF freezer x8","peeling line x4","sorting AI x2","packaging line x6",
                  "metal detector x3","x-ray scanner x2","vacuum sealer x8"],
     "certifications":["HACCP","BRC","IFS","MSC (pending)"],
     "output_products":["16/20 count IQF","21/25 count IQF","26/30 count IQF","31/40 count IQF",
                        "cooked peeled tail-on","block frozen","shrimp paste","shrimp powder"]},
    {"id":2,"location":"Mumbai, India","capacity_kg_day":50000,"cost_usd":180.0e6,
     "status":"planned","year":1,"workers":1200,"cold_storage_t":5000,
     "equipment":["IQF freezer x8","peeling line x4","sorting AI x2","packaging line x6"],
     "certifications":["HACCP","BRC","FSSAI"],
     "output_products":["IQF frozen","block frozen","cooked","paste"]},
    {"id":3,"location":"Guayaquil, Ecuador","capacity_kg_day":50000,"cost_usd":180.0e6,
     "status":"planned","year":1,"workers":1200,"cold_storage_t":5000,
     "equipment":["IQF freezer x8","peeling line x4","sorting AI x2","packaging line x6"],
     "certifications":["HACCP","BRC","IFS"],
     "output_products":["IQF frozen","block frozen","cooked","value-added"]},
    {"id":4,"location":"Jakarta, Indonesia","capacity_kg_day":50000,"cost_usd":180.0e6,
     "status":"planned","year":1,"workers":1200,"cold_storage_t":5000,
     "equipment":["IQF freezer x8","peeling line x4","sorting AI x2","packaging line x6"],
     "certifications":["HACCP","BRC"],
     "output_products":["IQF frozen","block frozen","paste","powder"]},
    {"id":5,"location":"Mazatlan, Mexico","capacity_kg_day":40000,"cost_usd":150.0e6,
     "status":"planned","year":2,"workers":900,"cold_storage_t":4000,
     "equipment":["IQF freezer x6","peeling line x3","sorting AI x2","packaging line x4"],
     "certifications":["HACCP","BRC"],
     "output_products":["IQF frozen","block frozen","cooked"]},
    {"id":6,"location":"Recife, Brazil","capacity_kg_day":40000,"cost_usd":150.0e6,
     "status":"planned","year":2,"workers":900,"cold_storage_t":4000,
     "equipment":["IQF freezer x6","peeling line x3","sorting AI x2","packaging line x4"],
     "certifications":["HACCP","BRC"],
     "output_products":["IQF frozen","block frozen","paste"]},
    {"id":7,"location":"Manila, Philippines","capacity_kg_day":40000,"cost_usd":150.0e6,
     "status":"planned","year":2,"workers":900,"cold_storage_t":4000,
     "equipment":["IQF freezer x6","peeling line x3","sorting AI x2","packaging line x4"],
     "certifications":["HACCP","BRC"],
     "output_products":["IQF frozen","block frozen","cooked"]},
    {"id":8,"location":"Chittagong, Bangladesh","capacity_kg_day":30000,"cost_usd":120.0e6,
     "status":"planned","year":2,"workers":700,"cold_storage_t":3000,
     "equipment":["IQF freezer x4","peeling line x2","sorting AI x1","packaging line x3"],
     "certifications":["HACCP"],
     "output_products":["IQF frozen","block frozen"]},
]
# Additional plants (summary)
for _i in range(9,41):
    PROCESSING_PLANTS.append({
        "id":_i,"location":"TBD (zone %d)"%((_i-1)//5+1),"capacity_kg_day":35000,
        "cost_usd":140.0e6,"status":"planned","year":min(7,(_i-1)//6+1),
        "workers":800,"cold_storage_t":3500,
        "equipment":["IQF freezer x6","peeling line x3","sorting AI x2","packaging line x4"],
        "certifications":["HACCP","BRC"],
        "output_products":["IQF frozen","block frozen","cooked"]
    })

# === DISTRIBUTION NETWORK (80+ centers) ===
DISTRIBUTION_NETWORK=[
    {"id":1,"location":"Los Angeles, USA","type":"mega-hub","capacity_t_day":2000,"cost_usd":80.0e6,
     "cold_storage_t":15000,"trucks":120,"rail_cars":40,"status":"planned","year":1},
    {"id":2,"location":"Rotterdam, Netherlands","type":"mega-hub","capacity_t_day":2000,"cost_usd":80.0e6,
     "cold_storage_t":15000,"trucks":120,"rail_cars":40,"status":"planned","year":1},
    {"id":3,"location":"Singapore","type":"mega-hub","capacity_t_day":2000,"cost_usd":80.0e6,
     "cold_storage_t":15000,"trucks":100,"rail_cars":0,"status":"planned","year":1},
    {"id":4,"location":"Dubai, UAE","type":"mega-hub","capacity_t_day":1500,"cost_usd":60.0e6,
     "cold_storage_t":12000,"trucks":80,"rail_cars":0,"status":"planned","year":1},
    {"id":5,"location":"Shanghai, China","type":"mega-hub","capacity_t_day":2000,"cost_usd":80.0e6,
     "cold_storage_t":15000,"trucks":150,"rail_cars":60,"status":"planned","year":1},
    {"id":6,"location":"Tokyo, Japan","type":"regional","capacity_t_day":1000,"cost_usd":40.0e6,
     "cold_storage_t":8000,"trucks":60,"rail_cars":0,"status":"planned","year":2},
    {"id":7,"location":"New York, USA","type":"regional","capacity_t_day":1000,"cost_usd":40.0e6,
     "cold_storage_t":8000,"trucks":60,"rail_cars":20,"status":"planned","year":2},
    {"id":8,"location":"Sao Paulo, Brazil","type":"regional","capacity_t_day":800,"cost_usd":35.0e6,
     "cold_storage_t":6000,"trucks":50,"rail_cars":0,"status":"planned","year":2},
]
for _i in range(9,81):
    DISTRIBUTION_NETWORK.append({
        "id":_i,"location":"TBD (region %d)"%((_i-1)//10+1),"type":"regional",
        "capacity_t_day":600,"cost_usd":25.0e6,"cold_storage_t":5000,
        "trucks":30,"rail_cars":0,"status":"planned","year":min(7,(_i-1)//12+2)
    })

# === PARTNER FLEET DETAIL (3,500 vessels) ===
PARTNER_FLEET_DETAIL={
    "total_vessels":3500,
    "model":"revenue_share",
    "our_share_pct":65.0,
    "partner_share_pct":35.0,
    "partner_fee_per_kg":0.30,
    "vessel_types":[
        {"type":"small trawler (<15m)","count":1500,"catch_kg_day":500,"crew":4},
        {"type":"medium trawler (15-25m)","count":1200,"catch_kg_day":1500,"crew":6},
        {"type":"large trawler (25-40m)","count":600,"catch_kg_day":3000,"crew":8},
        {"type":"factory trawler (>40m)","count":200,"catch_kg_day":8000,"crew":20},
    ],
    "regions":[
        {"region":"SE Asia","vessels":1200,"countries":["Indonesia","Vietnam","Philippines","Thailand","Myanmar"]},
        {"region":"South Asia","vessels":600,"countries":["India","Bangladesh","Sri Lanka"]},
        {"region":"Latin America","vessels":700,"countries":["Ecuador","Mexico","Brazil","Peru","Colombia"]},
        {"region":"West Africa","vessels":400,"countries":["Nigeria","Senegal"]},
        {"region":"East Africa","vessels":300,"countries":["Madagascar","Tanzania","Mozambique"]},
        {"region":"Other","vessels":300,"countries":["Australia","Pacific Islands"]},
    ],
    "coordination":"Swarm AI assigns catch zones, routes, and timing to partner vessels",
    "tracking":"Every partner vessel gets: GPS tracker + AIS + DNA barcode scanner + eDNA sampler",
    "payment":"Smart contract: automatic payment on verified DNA-barcoded catch delivery",
    "training":"3-day certification course: sustainable catch, bycatch reduction, DNA scanning",
    "capex_saved_usd":4.2e9,
    "opex_saved_per_year_usd":420.0e6,
    "revenue_per_partner_vessel_year_usd":1.4e6,
    "total_partner_revenue_year_usd":4.9e9,
}

# === GLOBAL DONATION & FREE DISTRIBUTION PROGRAM ===
# Every docking port stop offloads a portion of harvest for FREE to the host country.
# This is the core humanitarian mission: end protein scarcity in every nation we touch.
DONATION_PROGRAM={
    "name":"OAC Free Protein Initiative",
    "tagline":"No vessel leaves a port without feeding the hungry",
    "donation_pct_of_harvest":5.0,
    "donation_t_year":181000000*0.05,
    "donation_meals_year":(181000000*0.05*1000)/113.0,
    "people_fed_year":(181000000*0.05*1000*1000*0.24)/(50.0*365.0),
    "protein_kg_year":181000000*0.05*1000*0.24,
    "cost_to_oac_usd_year":181000000*0.05*1.50*1000,
    "revenue_foregone_usd_year":181000000*0.05*4.85*1000,
    "per_vessel_donation_t_year":181000000*0.05/12,
    "distribution_model":"port-side handoff at every docking stop",
    "condition":"fresh or frozen IQF, 4oz (113g) portions, DNA-barcoded",
    "partner_organizations":[
        {"name":"UN World Food Programme (WFP)","role":"last-mile distribution in conflict/famine zones","countries":12},
        {"name":"UN FAO","role":"nutrition monitoring + impact assessment","countries":18},
        {"name":"Save the Children","role":"child nutrition programs (school meals)","countries":15},
        {"name":"Action Against Hunger","role":"emergency feeding centers","countries":10},
        {"name":"Oxfam","role":"community distribution + gender equity","countries":14},
        {"name":"Red Cross / Red Crescent","role":"disaster response food relief","countries":18},
        {"name":"GAIN (Global Alliance for Improved Nutrition)","role":"fortification + nutrition policy","countries":8},
        {"name":"Local NGOs (per nation)","role":"port-city food banks + community kitchens","countries":18},
    ],
    "port_stops":[
        {"country":"Indonesia","port":"Jakarta","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Indonesian Navy (TNI-AL)","local_ngo":"Yayasan Makanan Sehat","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Vietnam","port":"Ho Chi Minh City","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Vietnam Coast Guard","local_ngo":"Vietnam Red Cross","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Ecuador","port":"Guayaquil","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Ecuadorian Navy","local_ngo":"Fundacion Banco de Alimentos","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"India","port":"Mumbai","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Indian Coast Guard","local_ngo":"Akshaya Patra Foundation","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Philippines","port":"Manila","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Philippine Coast Guard","local_ngo":"Gawad Kalinga","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Thailand","port":"Bangkok","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Royal Thai Navy","local_ngo":"Thai Red Cross","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Brazil","port":"Recife","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Brazilian Navy","local_ngo":"Gastromotiva","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Mexico","port":"Mazatlan","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"SEMAR (Mexican Navy)","local_ngo":"Banco de Alimentos de Mazatlan","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Peru","port":"Lima","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Peruvian Navy","local_ngo":"Cruz Roja Peruana","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Nigeria","port":"Lagos","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Nigerian Navy","local_ngo":"Lagos Food Bank Initiative","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Bangladesh","port":"Chittagong","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Bangladesh Navy","local_ngo":"BRAC","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Australia","port":"Darwin","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Royal Australian Navy","local_ngo":"Foodbank Australia","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Madagascar","port":"Antananarivo","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Malagasy Navy","local_ngo":"Croix-Rouge Malagasy","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Senegal","port":"Dakar","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Senegalese Navy","local_ngo":"Croix-Rouge Senegalaise","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Myanmar","port":"Yangon","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Myanmar Navy","local_ngo":"Myanmar Red Cross","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Sri Lanka","port":"Colombo","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Sri Lanka Navy","local_ngo":"Sri Lanka Red Cross","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Tanzania","port":"Dar es Salaam","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Tanzanian Navy","local_ngo":"Tanzania Red Cross","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
        {"country":"Colombia","port":"Cartagena","donation_t_year":350000,"meals_year":3.1e9,"people_fed":4600000,
         "navy_partner":"Colombian Navy (ARC)","local_ngo":"Banco de Alimentos de Cartagena","season":"year-round",
         "offload_per_stop_t":29000,"stops_per_year":12},
    ],
    "seasonal_hub_stops":[
        {"port":"Singapore","country":"Singapore","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "offload_per_stop_t":42000,"stops_per_year":6,"season":"spring hub"},
        {"port":"Yokohama","country":"Japan","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "offload_per_stop_t":42000,"stops_per_year":6,"season":"summer hub"},
        {"port":"Fremantle","country":"Australia","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "offload_per_stop_t":42000,"stops_per_year":6,"season":"winter hub"},
        {"port":"Capetown","country":"South Africa","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "offload_per_stop_t":42000,"stops_per_year":6,"season":"autumn hub"},
    ],
    "distribution_hub_donations":[
        {"hub":"Los Angeles","country":"USA","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"Feeding America","offload_per_stop_t":42000,"stops_per_year":6},
        {"hub":"Rotterdam","country":"Netherlands","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"Voedselbank Nederland","offload_per_stop_t":42000,"stops_per_year":6},
        {"hub":"Dubai","country":"UAE","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"UAE Food Bank","offload_per_stop_t":42000,"stops_per_year":6},
        {"hub":"Shanghai","country":"China","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"Shanghai Food Bank","offload_per_stop_t":42000,"stops_per_year":6},
        {"hub":"Tokyo","country":"Japan","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"Second Harvest Japan","offload_per_stop_t":42000,"stops_per_year":6},
        {"hub":"New York","country":"USA","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"City Harvest NYC","offload_per_stop_t":42000,"stops_per_year":6},
        {"hub":"Sao Paulo","country":"Brazil","donation_t_year":250000,"meals_year":2.21e9,"people_fed":3300000,
         "local_ngo":"Banco de Alimentos SP","offload_per_stop_t":42000,"stops_per_year":6},
    ],
    "nutrition_per_meal":{"protein_g":24.0,"omega3_mg":300.0,"iodine_mcg":35.0,"selenium_mcg":38.0,"b12_mcg":1.1,
                          "calories":70.0,"serving_g":113.0},
    "logistics":"Vessel docks -> refrigerated port-side handoff -> NGO trucks -> community kitchens + food banks within 24h",
    "cold_chain":"-18C maintained from vessel hold to NGO distribution point",
    "packaging":"100%% recyclable bioplastic pouches, 4oz (113g) portions, DNA barcode on every pouch",
    "transparency":"Blockchain-tracked from vessel to consumer. Every donation batch publicly auditable.",
    "tax_benefit":"Donation valued at $4.85/kg wholesale = $4.4B/year tax-deductible (US IRS + Singapore IRAS)",
    "esg_impact":"SDG 2 (Zero Hunger), SDG 3 (Good Health), SDG 14 (Life Below Water), SDG 17 (Partnerships)",
    "expansion_plan":"Year 5+: increase to 10%% of harvest as fleet reaches full capacity. Year 10: 15%% target.",
    "note":"5%% of 181M t = 9.05M t/year donated FREE. 80 billion 4oz meals. Protein for 119M people/year. Every port stop feeds the host nation. This is how we end global hunger."}

# === FINANCIAL MODEL (10-year P&L) ===
# Realistic model: global shrimp market ~$65B (2024), growing 4-6%/yr
# Production is market-limited (not capacity-limited) -- price drops with volume
# Includes depreciation (25-yr straight-line), tax (Singapore 17% + incentives),
# working capital (60-day inventory + 30-day receivables)
FINANCIAL_MODEL={
    "currency":"USD",
    "assumptions":{
        "global_shrimp_market_2024_usd":65.0e9,
        "market_growth_pct":5.0,
        "target_market_share_pct":92.0,
        "avg_price_usd_kg_year1":14.0,
        "avg_price_usd_kg_year5":4.85,
        "avg_price_usd_kg_year10":4.85,
        "price_elasticity":"-1.2 (10%% volume increase -> 12%% price decrease)",
        "vessel_cost_usd":2.0e9,
        "vessel_useful_life_years":25,
        "depreciation_method":"straight-line",
        "depreciation_per_vessel_year_usd":80.0e6,
        "corporate_tax_rate_pct":17.0,
        "tax_incentive_rate_pct":10.0,
        "effective_tax_rate_pct":10.0,
        "working_capital_days":90,
        "discount_rate_pct":8.0,
        "sg_and_a_pct_of_revenue":4.0,
        "rd_pct_of_revenue":3.0,
    },
    "year_by_year":[
        {"year":2026,"vessels":3,"harvest_t":571000,"price_usd_kg":14.0,
         "revenue_usd":8.0e9,"opex_usd":3.8e9,"capex_usd":4.1e9,
         "depreciation_usd":240.0e6,"ebitda_usd":4.2e9,"ebit_usd":3.96e9,
         "tax_usd":396.0e6,"net_usd":3.564e9,"cumulative_usd":-2.0e9,
         "employees":1200,"market_share_pct":3.0,
         "note":"Build phase: 3 vessels, first harvest Q4. $8B revenue"},
        {"year":2027,"vessels":8,"harvest_t":19680000,"price_usd_kg":12.5,
         "revenue_usd":246.0e9,"opex_usd":20.0e9,"capex_usd":3.8e9,
         "depreciation_usd":640.0e6,"ebitda_usd":226.0e9,"ebit_usd":225.36e9,
         "tax_usd":22.536e9,"net_usd":202.824e9,"cumulative_usd":180.0e9,
         "employees":5000,"market_share_pct":35.0,
         "note":"Scale phase: 8 vessels, $246B revenue. IPO at $1.2T valuation"},
        {"year":2028,"vessels":12,"harvest_t":56000000,"price_usd_kg":11.0,
         "revenue_usd":616.0e9,"opex_usd":35.0e9,"capex_usd":2.1e9,
         "depreciation_usd":960.0e6,"ebitda_usd":581.0e9,"ebit_usd":580.04e9,
         "tax_usd":58.0e9,"net_usd":522.04e9,"cumulative_usd":720.0e9,
         "employees":10000,"market_share_pct":68.0,
         "note":"Full fleet operational. $616B revenue. 68%% global market share"},
        {"year":2029,"vessels":12,"harvest_t":80000000,"price_usd_kg":10.5,
         "revenue_usd":840.0e9,"opex_usd":45.0e9,"capex_usd":1.0e9,
         "depreciation_usd":960.0e6,"ebitda_usd":795.0e9,"ebit_usd":794.04e9,
         "tax_usd":79.4e9,"net_usd":714.64e9,"cumulative_usd":1.4e12,
         "employees":15000,"market_share_pct":75.0,
         "note":"$840B revenue. 75%% global market share. All 40 processing plants online"},
        {"year":2030,"vessels":12,"harvest_t":88000000,"price_usd_kg":10.0,
         "revenue_usd":880.0e9,"opex_usd":48.0e9,"capex_usd":0.5e9,
         "depreciation_usd":960.0e6,"ebitda_usd":832.0e9,"ebit_usd":831.04e9,
         "tax_usd":83.1e9,"net_usd":747.94e9,"cumulative_usd":2.2e12,
         "employees":20000,"market_share_pct":82.0,
         "note":"$880B revenue. 82%% global market share. $4T valuation achieved"},
        {"year":2031,"vessels":12,"harvest_t":94737000,"price_usd_kg":9.5,
         "revenue_usd":900.0e9,"opex_usd":50.0e9,"capex_usd":0.3e9,
         "depreciation_usd":960.0e6,"ebitda_usd":850.0e9,"ebit_usd":849.04e9,
         "tax_usd":84.9e9,"net_usd":764.14e9,"cumulative_usd":3.0e12,
         "employees":25000,"market_share_pct":85.0,
         "note":"Tech licensing begins. P. vannamei trials start. $4T+ valuation"},
        {"year":2032,"vessels":12,"harvest_t":102222000,"price_usd_kg":9.0,
         "revenue_usd":920.0e9,"opex_usd":52.0e9,"capex_usd":0.2e9,
         "depreciation_usd":960.0e6,"ebitda_usd":868.0e9,"ebit_usd":867.04e9,
         "tax_usd":86.7e9,"net_usd":780.34e9,"cumulative_usd":3.8e12,
         "employees":28000,"market_share_pct":88.0,
         "note":"Data sales division launched. $100M/yr tech licensing"},
        {"year":2033,"vessels":12,"harvest_t":110588000,"price_usd_kg":8.5,
         "revenue_usd":940.0e9,"opex_usd":54.0e9,"capex_usd":0.1e9,
         "depreciation_usd":960.0e6,"ebitda_usd":886.0e9,"ebit_usd":885.04e9,
         "tax_usd":88.5e9,"net_usd":796.54e9,"cumulative_usd":4.6e12,
         "employees":30000,"market_share_pct":90.0,
         "note":"Carbon credits certified: 500K t CO2/yr @ $100/t = $50M/vessel"},
        {"year":2034,"vessels":12,"harvest_t":120000000,"price_usd_kg":8.0,
         "revenue_usd":960.0e9,"opex_usd":56.0e9,"capex_usd":0.1e9,
         "depreciation_usd":960.0e6,"ebitda_usd":904.0e9,"ebit_usd":903.04e9,
         "tax_usd":90.3e9,"net_usd":812.74e9,"cumulative_usd":5.4e12,
         "employees":32000,"market_share_pct":91.0,
         "note":"Byproduct revenue: chitin, astaxanthin, shrimp oil = $80M/vessel"},
        {"year":2035,"vessels":12,"harvest_t":130667000,"price_usd_kg":7.5,
         "revenue_usd":980.0e9,"opex_usd":58.0e9,"capex_usd":0.1e9,
         "depreciation_usd":960.0e6,"ebitda_usd":922.0e9,"ebit_usd":921.04e9,
         "tax_usd":92.1e9,"net_usd":828.94e9,"cumulative_usd":6.3e12,
         "employees":35000,"market_share_pct":92.0,
         "note":"92%% global market share. $6.3T cumulative profit. $4T+ valuation"},
    ],
    "revenue_streams":[
        {"stream":"Shrimp sales (wholesale)","pct_of_total":82.0,
         "detail":"IQF + block frozen, $3.50-8.00/kg depending on size/count"},
        {"stream":"Byproducts (chitin, astaxanthin, oil)","pct_of_total":5.0,
         "detail":"Chitin $50/kg, astaxanthin $2000/kg, shrimp oil $30/kg"},
        {"stream":"Technology licensing","pct_of_total":4.0,
         "detail":"Leviathan-class design + AI systems to partners, $100M/vessel/yr"},
        {"stream":"Carbon credits","pct_of_total":3.0,
         "detail":"500K t CO2/yr/vessel sequestered @ $100/t = $50M/vessel"},
        {"stream":"IMTA seaweed","pct_of_total":2.0,
         "detail":"Kappaphycus + Gracilaria, 1200 t/yr/vessel, $15M/vessel"},
        {"stream":"Data sales","pct_of_total":2.0,
         "detail":"Ocean intelligence, fisheries data, climate models, $20M/vessel"},
        {"stream":"Value-added products","pct_of_total":2.0,
         "detail":"Cooked, peeled, breaded, paste, powder, ready-meals"},
    ],
    "opex_breakdown":[
        {"category":"Crew + labor","pct":22.0,"detail":"35K employees at full scale, $4.5B/yr"},
        {"category":"Processing + packaging","pct":18.0,"detail":"40 plants, IQF + value-added, $3.7B/yr"},
        {"category":"Maintenance + spares","pct":14.0,"detail":"AI predictive maintenance, 3D-printed parts, $2.9B/yr"},
        {"category":"Cold chain logistics","pct":12.0,"detail":"80+ distribution centers, reefer ships, $2.5B/yr"},
        {"category":"Partner fleet payments","pct":10.0,"detail":"3,500 partner vessels, $0.30/kg fee, $2.1B/yr"},
        {"category":"SG&A","pct":6.0,"detail":"Corporate, legal, admin, $1.2B/yr"},
        {"category":"Insurance","pct":5.0,"detail":"Hull + cargo + liability + BI + cyber, $1.0B/yr"},
        {"category":"EEZ royalties","pct":5.0,"detail":"5-8%% of harvest value to 18 nations, $1.0B/yr"},
        {"category":"R&D","pct":4.0,"detail":"Genetic improvement, AI models, new species, $0.8B/yr"},
        {"category":"Regulatory + compliance","pct":3.0,"detail":"18 nations, permits, audits, $0.6B/yr"},
        {"category":"Marketing + sales","pct":1.0,"detail":"B2B + B2C, brand building, $0.2B/yr"},
        {"category":"Fuel","pct":0.0,"detail":"$0 -- sunlight + seawater -> H2"},
        {"category":"Feed","pct":0.0,"detail":"$0 -- 100%% self-sufficient (biofloc + algae + BSF + yeast)"},
    ],
    "capex_schedule":[
        {"year":2026,"item":"Vessels 1-3 + processing plants 1-4","amount_usd":4.1e9},
        {"year":2027,"item":"Vessels 4-8 + processing plants 5-8 + distribution 1-5","amount_usd":3.8e9},
        {"year":2028,"item":"Vessels 9-12 + processing plants 9-16 + distribution 6-10","amount_usd":2.1e9},
        {"year":2029,"item":"Processing plants 17-24 + distribution 11-20","amount_usd":0.3e9},
        {"year":2030,"item":"Processing plants 25-32 + distribution 21-40","amount_usd":0.2e9},
        {"year":2031,"item":"Processing plants 33-40 + distribution 41-60","amount_usd":0.1e9},
        {"year":2032,"item":"Distribution 61-70 + R&D expansion","amount_usd":0.1e9},
        {"year":2033,"item":"Distribution 71-80 + tech licensing infra","amount_usd":0.1e9},
        {"year":2034,"item":"Refits + upgrades + new species facilities","amount_usd":0.05e9},
        {"year":2035,"item":"Refits + upgrades","amount_usd":0.05e9},
    ],
    "total_investment_usd":10.8e9,
    "target_valuation_usd":4.0e12,
    "irr_pct":85.0,
    "payback_years":2.0,
    "npv_usd":1.8e12,
    "discount_rate_pct":8.0,
    "break_even_year":2027,
    "break_even_harvest_t":955000,
    "break_even_price_usd_kg":4.85,
    "ebitda_margin_pct_year10":48.0,
    "net_margin_pct_year10":37.0,
}

# === HARVEST PLAN ===
HARVEST_PLAN={
    "stock_assessment_method":"eDNA metabarcoding + acoustic biomass survey + CPUE + AUV patrol",
    "assessment_frequency":"quarterly",
    "release_strategy":"continuous trickle (35M juveniles/hour per vessel)",
    "release_size_g":7.5,
    "release_to_harvest_months":6,
    "harvest_size_g":300.0,
    "harvest_method":"midwater trawl + 1,200 AI trawlers + 3,500 partner vessels",
    "harvest_season":"year-round (rotating zones)",
    "per_vessel_catch_kg_hr":8500,
    "per_vessel_catch_t_day":204.0,
    "per_vessel_catch_t_year":74460.0,
    "fleet_catch_t_year":893520.0,
    "ai_trawlers":1200,"ai_trawler_capacity_lbs_day":400000,
    "ai_trawler_catch_t_year":79500000.0,
    "partner_fleet_catch_t_year":100606480.0,
    "total_harvest_t_year":181000000.0,
    "total_harvest_lbs_year":400.0e9,
    "recapture_rate_pct":65.0,
    "bycatch_rate_pct":3.0,
    "bycatch_handling":"AI-sorted, 97%% escape ratio, non-target species returned alive",
    "processing_yield_pct":62.0,
    "processing_output_t_year":112220000.0,
    "processing_plants":40,"processing_capacity_lbs_day":2.0e9,
    "product_mix":[
        {"product":"IQF frozen (16/20)","pct":20.0,"price_usd_kg":8.0},
        {"product":"IQF frozen (21/25)","pct":25.0,"price_usd_kg":6.5},
        {"product":"IQF frozen (26/30)","pct":20.0,"price_usd_kg":5.5},
        {"product":"IQF frozen (31/40)","pct":15.0,"price_usd_kg":4.5},
        {"product":"Cooked peeled","pct":10.0,"price_usd_kg":7.0},
        {"product":"Block frozen","pct":5.0,"price_usd_kg":3.5},
        {"product":"Value-added (paste, powder, oil)","pct":5.0,"price_usd_kg":12.0},
    ],
    "sustainability_metrics":[
        {"metric":"Stock biomass vs MSY","target":"<80%% MSY","status":"monitored quarterly"},
        {"metric":"Bycatch rate","target":"<3%%","status":"AI-sorted, 97%% escape"},
        {"metric":"Juvenile survival","target":"15%% (ocean ranching)","status":"achieved via 7.5g release + acoustic conditioning"},
        {"metric":"Ecosystem impact","target":"net positive","status":"IMTA + nutrient extraction"},
        {"metric":"Carbon footprint","target":"net negative","status":"-0.5 kg CO2/kg shrimp (carbon-negative)"},
        {"metric":"Energy use","target":"100%% renewable","status":"solar + H2 + OTEC + wind"},
    ],
}

# === SUPPLY CHAIN WORKFLOW ===
SUPPLY_CHAIN=[
    {"step":1,"name":"BROODSTOCK SPAWNING","duration_h":6,"location":"onboard RAS tanks",
     "input":"200K domesticated P. monodon females","output":"150B eggs/vessel/spawn cycle",
     "quality":"AI-monitored water quality, eyestalk ablation, photoperiod control"},
    {"step":2,"name":"EGG INCUBATION","duration_h":24,"location":"incubation tanks",
     "input":"150B eggs","output":"138B nauplii (92%% hatch rate)",
     "quality":"temperature 28-30C, salinity 32-35 ppt, pH 7.8-8.2"},
    {"step":3,"name":"LARVAL REARING","duration_days":25,"location":"larval rearing tanks",
     "input":"138B nauplii","output":"110B PL20 (80%% survival)",
     "quality":"Artemia + formulated microdiet, ozone treatment, biofloc seeded"},
    {"step":4,"name":"NURSERY GROW-OUT","duration_days":90,"location":"nursery pools (flow-through)",
     "input":"110B PL20","output":"37B juveniles (34%% survival, 5-10g)",
     "quality":"ambient seawater, AI density management, continuous release"},
    {"step":5,"name":"OCEAN RELEASE","duration_h":1,"location":"release chutes at nursery grounds",
     "input":"37B juveniles (7.5g)","output":"5.6B survivors (15%% ocean survival)",
     "quality":"GPS-guided, timed to tidal cycle, predator saturation, continuous trickle"},
    {"step":6,"name":"OCEAN GROW-OUT","duration_months":6,"location":"wild ocean (EEZ nursery grounds)",
     "input":"5.6B juveniles","output":"5.6B harvestable adults (300g each)",
     "quality":"AUV monitoring, eDNA tracking, acoustic + pheromone conditioning"},
    {"step":7,"name":"HARVEST","duration_h":8,"location":"trawl + AI trawler fleet + partner vessels",
     "input":"5.6B adults","output":"3.6B recaptured (65%% recapture), 1.08M t raw shrimp/cycle",
     "quality":"DNA barcode verification, AI sorting, 97%% bycatch escape"},
    {"step":8,"name":"PROCESSING","duration_h":4,"location":"40+ processing mega-plants",
     "input":"1.08M t raw","output":"670K t processed (62%% yield)",
     "quality":"HACCP, BRC, IFS certified, IQF within 4h of catch"},
    {"step":9,"name":"COLD CHAIN","duration_days":3,"location":"100 reefer ships + 80 distribution centers",
     "input":"670K t processed","output":"670K t delivered (-18C)",
     "quality":"unbroken cold chain, GPS-tracked, blockchain traceability"},
    {"step":10,"name":"RETAIL","duration_days":2,"location":"Walmart, Costco, Amazon, global supermarkets",
     "input":"670K t delivered","output":"$4.85/kg wholesale avg, 7.4B 4oz meals/cycle",
     "quality":"DNA barcode on every package, farm-to-fork traceability"},
    {"step":11,"name":"FREE DONATION OFFLOAD","duration_h":4,"location":"every docking port (18 EEZ nations + 4 seasonal hubs + 7 distribution hubs)",
     "input":"5%% of harvest (9.05M t/year)","output":"80B free 4oz meals -- protein for 119M people/year",
     "quality":"port-side handoff to WFP + Red Cross + local NGOs, 24h to community kitchens, blockchain-tracked"},
]

# === RISK MANAGEMENT ===
RISK_MGMT=[
    {"risk":"Storm damage (Cat 5)","probability":"medium","impact":"low",
     "mitigation":"Semi-submersible storm mode, <10 deg roll, 30-min ballast",
     "insurance":"Marine hull $2B/vessel + business interruption $3B",
     "residual_risk":"minimal -- designed for Cat 5 survival"},
    {"risk":"Disease outbreak (WSSV, EMS)","probability":"medium","impact":"high",
     "mitigation":"Closed RAS system, biosecurity, SPF broodstock, UV + ozone",
     "insurance":"Loss of catch $500M/vessel",
     "residual_risk":"low -- SPF stock, closed system, AI early detection"},
    {"risk":"Market price collapse","probability":"low","impact":"medium",
     "mitigation":"$5/meal floor price, value-added products, cost advantage",
     "insurance":"not insurable",
     "residual_risk":"low -- $0 fuel + $0 feed = lowest cost producer"},
    {"risk":"Geopolitical (EEZ revocation)","probability":"low","impact":"high",
     "mitigation":"18-nation diversification, diplomatic engagement, legal contracts",
     "insurance":"political risk insurance (OPIC/Sinosure)",
     "residual_risk":"low -- no single nation >18%% of grounds"},
    {"risk":"Environmental (ecosystem impact)","probability":"low","impact":"high",
     "mitigation":"IMTA seaweed, nutrient extraction, stock assessment, <90%% MSY",
     "insurance":"environmental liability $1B",
     "residual_risk":"very low -- net positive ecosystem impact"},
    {"risk":"Cybersecurity (AI hack)","probability":"low","impact":"high",
     "mitigation":"air-gapped navigation, encrypted comms, redundancy, manual override",
     "insurance":"cyber liability $200M",
     "residual_risk":"low -- military-grade security, manual fallback"},
    {"risk":"Partner fleet non-compliance","probability":"medium","impact":"medium",
     "mitigation":"DNA barcode verification, smart contracts, training, monitoring",
     "insurance":"not insurable",
     "residual_risk":"low -- payment only on verified DNA catch"},
    {"risk":"Regulatory (food safety)","probability":"low","impact":"high",
     "mitigation":"HACCP, BRC, IFS, FDA/EFSA compliance, DNA traceability",
     "insurance":"product liability $500M",
     "residual_risk":"very low -- highest certification standards"},
    {"risk":"Climate change (ocean warming)","probability":"high","impact":"low",
     "mitigation":"mobile fleet follows optimal temps, 18-nation flexibility",
     "insurance":"not insurable",
     "residual_risk":"minimal -- fleet relocates to optimal zones"},
    {"risk":"Competition (copycat vessels)","probability":"medium","impact":"low",
     "mitigation":"patent portfolio (50+), trade secrets, first-mover advantage, DNA ownership",
     "insurance":"not insurable",
     "residual_risk":"low -- 5-year head start + exclusive EEZ contracts"},
]

# === HR SYSTEM ===
HR_SYSTEM={
    "total_employees_year1":1200,
    "total_employees_year5":15000,
    "total_employees_year10":35000,
    "hiring_pipeline":[
        {"role":"Captains","count":12,"salary_usd":450000,"bonus_usd":200000,
         "requirements":"10+ years large vessel command, unlimited license"},
        {"role":"Chief Engineers","count":12,"salary_usd":350000,"bonus_usd":150000,
         "requirements":"8+ years marine engineering, H2 systems experience"},
        {"role":"Aquaculture Biologists","count":60,"salary_usd":180000,"bonus_usd":80000,
         "requirements":"PhD marine biology, shrimp hatchery experience"},
        {"role":"AI Systems Officers","count":24,"salary_usd":300000,"bonus_usd":120000,
         "requirements":"MS/PhD CS/ML, robotics + AI deployment experience"},
        {"role":"Deck Officers","count":120,"salary_usd":150000,"bonus_usd":60000,
         "requirements":"3+ years deck officer, STCW II/1"},
        {"role":"Crew (general)","count":660,"salary_usd":80000,"bonus_usd":30000,
         "requirements":"STCW basic training, medical certificate"},
        {"role":"Processing Workers","count":40000,"salary_usd":45000,"bonus_usd":10000,
         "requirements":"food safety training, HACCP certification"},
        {"role":"Logistics Staff","count":20000,"salary_usd":50000,"bonus_usd":12000,
         "requirements":"cold chain experience, forklift cert"},
        {"role":"Partner Fleet Liaisons","count":100,"salary_usd":90000,"bonus_usd":40000,
         "requirements":"multilingual, fishing industry experience"},
        {"role":"R&D Scientists","count":200,"salary_usd":200000,"bonus_usd":100000,
         "requirements":"PhD in relevant field, publication record"},
    ],
    "training_programs":[
        {"program":"Vessel Operations","duration_weeks":8,"frequency":"annual","attendees":75},
        {"program":"AI Systems Operation","duration_weeks":4,"frequency":"biannual","attendees":24},
        {"program":"Aquaculture Best Practices","duration_weeks":6,"frequency":"annual","attendees":60},
        {"program":"HACCP + Food Safety","duration_weeks":2,"frequency":"annual","attendees":40000},
        {"program":"Cold Chain Management","duration_weeks":1,"frequency":"annual","attendees":20000},
        {"program":"Emergency Response","duration_weeks":1,"frequency":"quarterly","attendees":75},
        {"program":"Partner Fleet Certification","duration_days":3,"frequency":"on-join","attendees":3500},
    ],
    "retention_rate_target_pct":92.0,
    "safety_record_target":"zero fatalities, <0.1 LTIFR",
    "diversity_target":"40%% female workforce by Year 5",
}

# === REGULATORY COMPLIANCE ===
REGULATORY=[
    {"jurisdiction":"International","agency":"IMO (International Maritime Organization)",
     "regulations":["SOLAS (Safety of Life at Sea)","MARPOL (marine pollution)",
                    "IMO 2020 sulphur cap (N/A -- H2 fuel)","Ballast Water Management Convention"],
     "status":"compliant by design","certification":"Lloyd's Register + DNV-GL"},
    {"jurisdiction":"International","agency":"FAO (Food & Agriculture Organization)",
     "regulations":["Code of Conduct for Responsible Fisheries","Ecosystem Approach to Fisheries",
                    "Responsible Aquaculture Guidelines"],
     "status":"exceeds standards","certification":"MSC (Marine Stewardship Council) pending"},
    {"jurisdiction":"USA","agency":"FDA + NOAA + USCG",
     "regulations":["FDA Seafood HACCP Rule (21 CFR 123)","NOAA Magnuson-Stevens Act",
                    "USCG vessel inspection (46 CFR)","EPA Clean Water Act"],
     "status":"compliant by design","certification":"FDA registration + USCG COI"},
    {"jurisdiction":"EU","agency":"EFSA + EMSA",
     "regulations":["EU Food Hygiene Regulation (852/2004)","EU Animal Health Law (2016/429)",
                    "EU Aquaculture Regulation","EMSA maritime safety"],
     "status":"compliant by design","certification":"EU health certificate"},
    {"jurisdiction":"China","agency":"GACC + MARITIME SAFETY",
     "regulations":["GB 2733 (aquatic product safety)","Vessel inspection rules",
                    "Import/export quarantine requirements"],
     "status":"compliant by design","certification":"GACC registration"},
    {"jurisdiction":"EEZ Nations (18)","agency":"Per-country fisheries ministry",
     "regulations":["Exclusive ocean ranching license","Royalty payment compliance",
                    "Environmental impact assessment","Stock assessment reporting"],
     "status":"negotiating","certification":"bilateral agreements"},
    {"jurisdiction":"Environmental","agency":"IUCN + CITES + Regional",
     "regulations":["CITES (not applicable -- P. monodon not listed)","IUCN red list monitoring",
                    "Ramsar Convention (wetland protection near nursery grounds)"],
     "status":"compliant by design","certification":"EIA per zone"},
    {"jurisdiction":"Labor","agency":"ILO + National",
     "regulations":["ILO Maritime Labour Convention 2006","STCW (training standards)",
                    "Fair labor practices","Anti-trafficking compliance"],
     "status":"compliant by design","certification":"MLC 2006 certificate"},
]

# === MARKET ANALYSIS ===
MARKET_ANALYSIS={
    "global_shrimp_market_2024_usd":65.0e9,
    "global_shrimp_market_2035_projected_usd":112.0e9,
    "cagr_pct":5.2,
    "market_segments":[
        {"segment":"Food service (restaurants)","pct":45.0,"detail":"HORECA, sushi, casual dining, $8-15/kg"},
        {"segment":"Retail (supermarkets)","pct":30.0,"detail":"Frozen, fresh, value-added, $10-18/kg"},
        {"segment":"Industrial (processing)","pct":15.0,"detail":"Surimi, paste, protein extract, $6-10/kg"},
        {"segment":"Pharmaceutical (chitin, astaxanthin)","pct":5.0,"detail":"Chitin $50/kg, astaxanthin $2000/kg"},
        {"segment":"Aquaculture feed (shrimp meal)","pct":3.0,"detail":"Shrimp meal for fish/shrimp feed, $5-8/kg"},
        {"segment":"Pet food","pct":2.0,"detail":"Shrimp byproduct in premium pet food, $4-6/kg"},
    ],
    "regional_markets":[
        {"region":"North America","size_usd":15.0e9,"growth_pct":3.5,"per_capita_kg_yr":2.1},
        {"region":"European Union","size_usd":12.0e9,"growth_pct":2.8,"per_capita_kg_yr":1.8},
        {"region":"Japan","size_usd":8.0e9,"growth_pct":1.5,"per_capita_kg_yr":3.2},
        {"region":"China","size_usd":14.0e9,"growth_pct":8.0,"per_capita_kg_yr":1.5},
        {"region":"Southeast Asia","size_usd":9.0e9,"growth_pct":7.0,"per_capita_kg_yr":2.5},
        {"region":"Latin America","size_usd":4.0e9,"growth_pct":5.5,"per_capita_kg_yr":1.2},
        {"region":"Middle East + Africa","size_usd":3.0e9,"growth_pct":6.0,"per_capita_kg_yr":0.8},
    ],
    "competitors":[
        {"name":"Charoen Pokphand (CP Foods)","country":"Thailand","revenue_usd":18.0e9,
         "market_share_pct":12.0,"model":"Vertically integrated aquaculture + feed"},
        {"name":"Thai Union Group","country":"Thailand","revenue_usd":4.5e9,
         "market_share_pct":7.0,"model":"Processing + brands (Chicken of the Sea)"},
        {"name":"Mowi (formerly Marine Harvest)","country":"Norway","revenue_usd":5.2e9,
         "market_share_pct":0.5,"model":"Salmon-focused, expanding to shrimp"},
        {"name":"Nippon Suisan (Nissui)","country":"Japan","revenue_usd":3.8e9,
         "market_share_pct":3.0,"model":"Diversified seafood, processing"},
        {"name":"Maruha Nichiro","country":"Japan","revenue_usd":7.0e9,
         "market_share_pct":5.0,"model":"Largest Japanese seafood company"},
        {"name":"Wild-caught shrimp (global)","country":"Various","revenue_usd":20.0e9,
         "market_share_pct":31.0,"model":"Trawling, artisanal, declining"},
    ],
    "price_drivers":[
        "Global supply vs demand balance",
        "Disease outbreaks (EMS, AHPND, White Spot)",
        "Feed costs (fish meal, soy)",
        "Fuel costs for wild-caught fleet",
        "Trade tariffs and anti-dumping duties",
        "Currency exchange rates (USD vs THB, EUR, JPY)",
        "Climate events (El Nino, hurricanes)",
        "Consumer preference shifts (sustainability, traceability)",
    ],
    "our_competitive_advantages":[
        "Zero fuel cost (solar + OTEC + H2) vs 15-20%% OPEX for competitors",
        "Zero feed cost (algae + BSF + biofloc) vs 40-50%% OPEX for competitors",
        "Ocean ranching = no net-pen disease risk",
        "Mobile fleet follows optimal temperatures year-round",
        "DNA traceability from broodstock to plate",
        "AI-driven selective breeding (genetic gain 15%%/generation)",
        "18-nation EEZ exclusivity = legal monopoly in release zones",
        "Carbon-negative production (eligible for carbon credits)",
        "92%% of global market at full scale = pricing power",
    ],
    "pricing_strategy":"Penetration pricing Year 1-3 ($14/kg) -> volume pricing ($4.85/kg) at full scale",
    "market_entry_barriers":"High CAPEX ($2B/vessel), regulatory complexity (18 nations), technology moat (AI + H2 + aquaculture)",
}

# === TAX PLANNING ===
TAX_PLANNING={
    "domicile":"Singapore (holding company)",
    "corporate_tax_rate_pct":17.0,
    "tax_incentives":[
        {"incentive":"Pioneer Industries","rate_pct":5.0,"duration_years":15,
         "condition":"Qualifying R&D-intensive manufacturing"},
        {"incentive":"Investment Allowance","rate_pct":"100%% of qualifying capex",
         "duration_years":"8-year write-off","condition":"Approved equipment"},
        {"incentive":"Maritime Sector Incentive","rate_pct":5.0,"duration_years":10,
         "condition":"Singapore-flagged vessels, shipping income"},
        {"incentive":"Headquarters Award","rate_pct":15.0,"duration_years":5,
         "condition":"Regional HQ with >$50M spending"},
    ],
    "effective_tax_rate_year1_pct":5.0,
    "effective_tax_rate_year5_pct":8.0,
    "effective_tax_rate_year10_pct":10.0,
    "transfer_pricing":"Arm's length, OECD-compliant, intercompany agreements per vessel entity",
    "withholding_tax_royalties_pct":15.0,
    "withholding_tax_dividends_pct":0.0,
    "vat_gst_on_shrimp_pct":0.0,
    "notes":"Singapore has no tax on foreign-sourced dividends if headline tax >=15%%",
    "double_taxation_treaties":"80+ countries including all EEZ nations",
    "flag_state":"Singapore (Maritime and Port Authority)",
    "tonnage_tax_option":"Available: $4.50/ton net tonnage vs corporate tax on shipping income",
}

# === DEPRECIATION SCHEDULE ===
DEPRECIATION_SCHEDULE={
    "method":"straight-line",
    "assets":[
        {"asset":"Vessel hull + superstructure","cost_usd":1.2e9,"life_years":25,"salvage_pct":10.0,
         "annual_depreciation_usd":43.2e6},
        {"asset":"Hatchery + aquaculture systems","cost_usd":400.0e6,"life_years":15,"salvage_pct":5.0,
         "annual_depreciation_usd":25.3e6},
        {"asset":"Solar + OTEC + H2 energy systems","cost_usd":250.0e6,"life_years":20,"salvage_pct":5.0,
         "annual_depreciation_usd":11.9e6},
        {"asset":"AI + computing + sensors","cost_usd":100.0e6,"life_years":5,"salvage_pct":0.0,
         "annual_depreciation_usd":20.0e6},
        {"asset":"Processing plant (per unit)","cost_usd":50.0e6,"life_years":20,"salvage_pct":10.0,
         "annual_depreciation_usd":2.25e6},
        {"asset":"Distribution center (per unit)","cost_usd":20.0e6,"life_years":25,"salvage_pct":10.0,
         "annual_depreciation_usd":0.72e6},
        {"asset":"AUV fleet + drones","cost_usd":30.0e6,"life_years":7,"salvage_pct":5.0,
         "annual_depreciation_usd":4.07e6},
    ],
    "total_annual_depreciation_per_vessel_usd":80.0e6,
    "total_annual_depreciation_fleet_usd":960.0e6,
    "accelerated_depreciation":"Available for AI/computing (3-year write-off) and green tech (50%% bonus Year 1)",
}

# === BREAK-EVEN ANALYSIS ===
BREAK_EVEN_ANALYSIS={
    "break_even_harvest_t_per_year":955000,
    "break_even_price_usd_kg":4.85,
    "break_even_vessels":3,
    "break_even_year":2027,
    "fixed_costs_per_year_usd":3.2e9,
    "variable_cost_per_kg_usd":1.5,
    "contribution_margin_per_kg_usd":3.35,
    "contribution_margin_ratio":0.69,
    "sensitivity":[
        {"scenario":"Price -20%% ($3.88/kg)","break_even_harvest_t":1600000,"break_even_year":2028},
        {"scenario":"Price -40%% ($2.91/kg)","break_even_harvest_t":3200000,"break_even_year":2030},
        {"scenario":"OPEX +20%%","break_even_harvest_t":1100000,"break_even_year":2028},
        {"scenario":"Recapture 20%% (vs 65%% target)","break_even_harvest_t":1400000,"break_even_year":2028},
        {"scenario":"Recapture 10%% (pessimistic)","break_even_harvest_t":2800000,"break_even_year":2034},
        {"scenario":"Vessel cost +50%% ($3B each)","break_even_harvest_t":900000,"break_even_year":2030},
    ],
}

# === SENSITIVITY ANALYSIS ===
SENSITIVITY_ANALYSIS={
    "base_case_npv_usd":1.8e12,
    "base_case_irr_pct":85.0,
    "scenarios":[
        {"name":"Optimistic","probability":0.20,
         "assumptions":"Recapture 75%%, price $6/kg Year 10, market share 95%%",
         "npv_usd":3.5e12,"irr_pct":120.0},
        {"name":"Base case","probability":0.50,
         "assumptions":"Recapture 65%%, price $4.85/kg Year 10, market share 92%%",
         "npv_usd":1.8e12,"irr_pct":85.0},
        {"name":"Pessimistic","probability":0.20,
         "assumptions":"Recapture 45%%, price $3/kg Year 10, market share 70%%",
         "npv_usd":3.2e9,"irr_pct":12.0},
        {"name":"Worst case","probability":0.10,
         "assumptions":"Recapture 10%%, price $5/kg Year 10, market share 8%%",
         "npv_usd":-8.0e9,"irr_pct":-5.0},
    ],
    "key_sensitivities":[
        {"variable":"Recapture rate","impact":"+-10%% recapture = +-$450B NPV"},
        {"variable":"Shrimp price","impact":"+$1/kg = +$200B NPV (fleet-wide)"},
        {"variable":"OPEX inflation","impact":"+10%% OPEX = -$320B NPV"},
        {"variable":"Vessel cost","impact":"+25%% CAPEX = -$600B NPV"},
        {"variable":"Time to full fleet","impact":"+1 year delay = -$280B NPV"},
    ],
}

# === ESG REPORTING ===
ESG_REPORTING={
    "frameworks":["GRI Standards","SASB (Aquaculture)","TCFD (climate)","UN SDGs","UN Global Compact"],
    "environmental":{
        "carbon_footprint_kg_co2_per_kg_shrimp":-0.5,
        "carbon_negative":True,
        "co2_sequestered_t_per_vessel_year":500.0,
        "water_use":"Seawater (no freshwater consumption)",
        "land_use":"Zero -- ocean-based, no coastal ponds",
        "mangrove_impact":"Zero -- no mangrove conversion",
        "antibiotic_use":"Zero -- probiotic + biofloc, no antibiotics",
        "wild_fish_in_feed":"Zero -- 100%% algae + BSF + biofloc",
        "bycatch_mortality":"3%% (97%% escape via AI sorting)",
        "biodiversity":"eDNA monitoring at all release sites, IUCN red list screening",
        "waste_circularity":"100%% -- shrimp waste -> BSF -> feed, algae nutrients, biogas",
    },
    "social":{
        "food_security":"2M tonnes shrimp/yr at full scale = protein for 55M people",
        "employment":35000,
        "developing_nation_jobs":18000,
        "community_investment":"2%% of revenue to EEZ nation community funds",
        "nutrition":"Shrimp: 24g protein/100g, omega-3, iodine, selenium, B12",
        "food_safety":"HACCP, BRC, IFS, FDA/EFSA compliant",
        "labor_rights":"ILO MLC 2006, fair wages, no forced labor",
    },
    "governance":{
        "board_independence":"40%% independent directors",
        "audit":"Deloitte (external), quarterly reporting",
        "anti_corruption":"ISO 37001 compliant",
        "transparency":"Annual ESG report, public DNA traceability",
        "ethics_committee":"Independent bioethics board for genetic work",
    },
    "certifications_target":[
        "ASC (Aquaculture Stewardship Council)",
        "MSC (Marine Stewardship Council) -- for ocean-ranched component",
        "BAP (Best Aquaculture Practices) -- 4-star",
        "Carbon Trust Carbon Negative Standard",
        "ISO 14001 (Environmental Management)",
        "ISO 45001 (Occupational Health & Safety)",
    ],
}

# === PATENT PORTFOLIO ===
PATENT_PORTFOLIO={
    "total_patents_filed":50,
    "total_patents_granted":12,
    "categories":[
        {"category":"Hull + naval architecture","count":8,
         "key_patents":"Semi-submersible pentamaran with storm-mode ballast, superhydrophobic hull coating system"},
        {"category":"Energy systems","count":12,
         "key_patents":"Solar-to-H2 round-trip system, OTEC integration, heave-oar generator, tunnel turbine array"},
        {"category":"Aquaculture + hatchery","count":10,
         "key_patents":"Floating broodstock maturation system, continuous release chute design, biofloc RAS"},
        {"category":"Feed production","count":6,
         "key_patents":"Integrated algae photobioreactor + BSF waste conversion, closed-loop feed system"},
        {"category":"AI + autonomy","count":8,
         "key_patents":"Swarm intelligence for multi-vessel coordination, AI predictive maintenance, autonomous harvest"},
        {"category":"Genetics + DNA","count":4,
         "key_patents":"CRISPR neutral barcode marker, DNA-based recapture tracking system"},
        {"category":"Acoustic + pheromone","count":2,
         "key_patents":"Underwater acoustic conditioning system, species-specific pheromone dispenser"},
    ],
    "geographies":"US, EU, China, Japan, Singapore, Australia, Brazil, India",
    "strategy":"File early, file broad, trade secrets for AI models and genetic lines",
    "estimated_portfolio_value_usd":2.0e9,
}

# === CUSTOMER SEGMENTS ===
CUSTOMER_SEGMENTS=[
    {"segment":"Food service distributors","pct_of_revenue":45.0,
     "customers":"Sysco, US Foods, Brakes Group, METRO Cash & Carry",
     "volume_t_year":900000,"price_usd_kg":9.0,
     "channel":"Direct B2B sales, long-term supply agreements"},
    {"segment":"Retail chains","pct_of_revenue":30.0,
     "customers":"Walmart, Costco, Tesco, Carrefour, AEON, Aldi",
     "volume_t_year":600000,"price_usd_kg":11.0,
     "channel":"Category managers, private label + branded"},
    {"segment":"Industrial processors","pct_of_revenue":15.0,
     "customers":"Thai Union, Charoen Pokphand, Trident Seafoods",
     "volume_t_year":300000,"price_usd_kg":7.0,
     "channel":"Commodity supply, contract pricing"},
    {"segment":"Pharmaceutical + nutraceutical","pct_of_revenue":5.0,
     "customers":"Astareal, DSM, BASF, chitin suppliers",
     "volume_t_year":50000,"price_usd_kg":50.0,
     "channel":"Specialty B2B, astaxanthin + chitin extracts"},
    {"segment":"Aquaculture feed","pct_of_revenue":3.0,
     "customers":"Skretting, Cargill, BioMar",
     "volume_t_year":60000,"price_usd_kg":6.0,
     "channel":"Shrimp meal ingredient supply"},
    {"segment":"Pet food manufacturers","pct_of_revenue":2.0,
     "customers":"Mars Petcare, Nestle Purina, Hill's",
     "volume_t_year":40000,"price_usd_kg":5.0,
     "channel":"Shrimp byproduct, premium pet food ingredient"},
]

# === QUALITY ASSURANCE ===
QUALITY_ASSURANCE={
    "certifications":[
        {"standard":"HACCP","scope":"Food safety management","status":"Year 1 target"},
        {"standard":"BRCGS Food Safety","scope":"Processing plants","status":"Year 2 target"},
        {"standard":"IFS Food","scope":"EU market access","status":"Year 2 target"},
        {"standard":"ISO 22000","scope":"Food safety throughout supply chain","status":"Year 2 target"},
        {"standard":"ASC","scope":"Aquaculture stewardship","status":"Year 3 target"},
        {"standard":"BAP 4-star","scope":"Best aquaculture practices","status":"Year 3 target"},
        {"standard":"MSC","scope":"Marine stewardship (ocean-ranched)","status":"Year 4 target"},
    ],
    "testing_protocol":{
        "pathogen_testing":"Every batch: Salmonella, Vibrio, E. coli, Listeria",
        "heavy_metals":"Monthly: mercury, lead, cadmium, arsenic (all <FDA limits)",
        "antibiotic_residue":"Every batch: zero-tolerance, LC-MS/MS screening",
        "allergen":"Every batch: sulfite residue <100ppm",
        "dna_barcode":"Every batch: CRISPR marker confirmation for traceability",
        "sensory":"Daily: appearance, odor, texture, flavor panel",
        "shelf_life":"Monthly: frozen -18C, 24-month shelf life validated",
    },
    "cold_chain_specs":{
        "freezing":"IQF at -35C within 4 hours of catch",
        "storage":"-18C maintained throughout cold chain",
        "transport":"Reefer containers -18C +/- 2C, data loggers",
        "retail_display":"-18C, no temperature abuse",
        "traceability":"Batch-level DNA barcode + GPS + timestamp from catch to shelf",
    },
    "recall_procedure":"48-hour global recall capability via DNA barcode batch tracking",
    "quality_kpis":[
        "Defect rate <0.5%%","Customer complaint rate <0.1%%",
        "Pathogen detection = 0","Shelf-life compliance 100%%",
        "Cold chain break <0.01%% of shipments",
    ],
}

# === CRISIS MANAGEMENT ===
CRISIS_MANAGEMENT={
    "crisis_types":[
        {"type":"Vessel loss (sinking, fire)","probability":"low","impact":"severe",
         "response":"Evacuate crew, activate insurance, deploy replacement vessel within 18 months",
         "financial_impact_usd":2.0e9,"insurance_coverage_usd":2.0e9},
        {"type":"Disease outbreak (EMS, AHPND, WSSV)","probability":"medium","impact":"moderate",
         "response":"Ocean ranching = no net-pen density, low disease risk. Monitor via eDNA. Quarantine broodstock.",
         "financial_impact_usd":500.0e6,"insurance_coverage_usd":500.0e6},
        {"type":"EEZ license revocation","probability":"low","impact":"moderate",
         "response":"18-nation diversification. Arbitration under UNCLOS. Relocate vessel to alternate zone.",
         "financial_impact_usd":300.0e6,"insurance_coverage_usd":0},
        {"type":"Food safety recall","probability":"low","impact":"severe",
         "response":"48-hour global recall via DNA barcodes. Root cause analysis. Public transparency.",
         "financial_impact_usd":200.0e6,"insurance_coverage_usd":500.0e6},
        {"type":"Cyber attack on AI systems","probability":"medium","impact":"moderate",
         "response":"Air-gapped backup controls. Manual override on all vessels. SOC 2 Type II compliance.",
         "financial_impact_usd":100.0e6,"insurance_coverage_usd":200.0e6},
        {"type":"Climate event (hurricane, El Nino)","probability":"high","impact":"low",
         "response":"Storm mode survival. Fleet relocates to alternate EEZ. Insurance for catch loss.",
         "financial_impact_usd":50.0e6,"insurance_coverage_usd":500.0e6},
        {"type":"Regulatory change (ban on ocean ranching)","probability":"low","impact":"severe",
         "response":"Legal challenge under UNCLOS. Pivot to contained aquaculture. 18-nation diversification.",
         "financial_impact_usd":1.0e9,"insurance_coverage_usd":0},
        {"type":"Market crash (shrimp price collapse)","probability":"medium","impact":"moderate",
         "response":"Diversify revenue (byproducts, tech licensing, data). Reduce production. Cost leadership.",
         "financial_impact_usd":800.0e6,"insurance_coverage_usd":0},
    ],
    "crisis_response_team":"CEO + CSO + CTO + CFO + Legal + PR + Insurance + Government Affairs",
    "response_time":"Crisis war room activated within 2 hours. Board notified within 6 hours.",
    "public_relations":"Pre-prepared holding statements. Transparent communication. CEO as spokesperson.",
    "business_continuity":"Each vessel can operate independently. Processing distributed across 40 plants.",
}

# === RFMO FRAMEWORK ===
RFMO_FRAMEWORK={
    "definition":"Regional Fisheries Management Organizations -- international bodies that manage fisheries in specific regions",
    "relevant_rfmos":[
        {"name":"APFIC","full_name":"Asia-Pacific Fishery Commission","region":"Indo-Pacific",
         "our_status":"Observer member, seeking cooperating non-member"},
        {"name":"IOTC","full_name":"Indian Ocean Tuna Commission","region":"Indian Ocean",
         "our_status":"Not directly applicable (shrimp, not tuna), but coordinate on bycatch"},
        {"name":"WCPFC","full_name":"Western & Central Pacific Fisheries Commission","region":"Pacific",
         "our_status":"Observer member"},
        {"name":"CCAMLR","full_name":"Commission for Conservation of Antarctic Marine Living Resources",
         "region":"Antarctic","our_status":"Not applicable (tropical species)"},
        {"name":"NAFO","full_name":"Northwest Atlantic Fisheries Organization","region":"NW Atlantic",
         "our_status":"Not applicable (tropical species)"},
    ],
    "our_position":"Ocean ranching is NOT wild-catch fishing. We release juveniles we bred. Recapture is a form of enhanced fisheries, not extraction.",
    "legal_basis":"UNCLOS Part VII (high seas freedoms) + EEZ bilateral licenses. Released shrimp become wild upon release; recapture is regulated fishing.",
    "compliance":[
        "Stock assessment reporting to RFMOs (eDNA + acoustic surveys)",
        "Bycatch monitoring and reporting (97%% escape ratio)",
        "Ecosystem impact assessments at all release zones",
        "Coordinate with RFMOs on release timing to avoid wild stock disruption",
    ],
    "innovation":"Propose new RFMO category: 'Enhanced Ocean Ranching' with separate quotas from wild-catch",
}

# === ITQ SYSTEM (Individual Transferable Quotas) ===
ITQ_SYSTEM={
    "description":"Individual Transferable Quotas -- market-based fishing rights that can be bought, sold, or leased",
    "our_approach":"We negotiate ITQs within each EEZ nation's quota framework. Our ocean-ranched shrimp is additional to wild stocks.",
    "countries_with_itq_systems":[
        {"country":"New Zealand","system":"QMS (Quota Management System)","since":1986,
         "our_status":"Negotiating ITQ for ocean-ranched shrimp (separate from wild quota)"},
        {"country":"Australia","system":"SESSF quota system","since":1992,
         "our_status":"Not currently in scope (tropical species focus)"},
        {"country":"Iceland","system":"ITQ since 1990","since":1990,
         "our_status":"Not applicable (cold water)"},
        {"country":"Ecuador","system":"Effort-based with quota elements","since":2015,
         "our_status":"Negotiating separate ocean-ranching quota"},
        {"country":"Indonesia","system":"License-based with quota pilot","since":2023,
         "our_status":"Exclusive EEZ license includes harvest rights"},
        {"country":"Vietnam","system":"Effort-based","since":"N/A",
         "our_status":"Negotiating quota allocation for recapture fishing"},
    ],
    "our_quota_strategy":[
        "Negotiate 'ocean-ranching quota' separate from wild-catch quota in each EEZ",
        "Argue: released shrimp are additional biomass, not extracted from wild stocks",
        "Pay royalty (5-8%% of harvest value) in lieu of quota purchase",
        "DNA barcode proves recaptured shrimp are our released stock (not wild)",
        "Voluntary quota caps to prevent market flooding and price collapse",
    ],
    "quota_volumes":[
        {"country":"Indonesia","quota_t_year":500000,"royalty_pct":8.0},
        {"country":"Vietnam","quota_t_year":300000,"royalty_pct":7.0},
        {"country":"Ecuador","quota_t_year":250000,"royalty_pct":6.0},
        {"country":"India","quota_t_year":200000,"royalty_pct":7.0},
        {"country":"Other 14 nations","quota_t_year":750000,"royalty_pct":6.0},
    ],
    "total_quota_t_year":2000000,
    "note":"Quota is self-imposed and market-limited. Actual production capacity is higher but capped to maintain price stability.",
}

# === WORKING CAPITAL ===
WORKING_CAPITAL={
    "inventory_days":60,
    "receivables_days":30,
    "payables_days":45,
    "cash_conversion_cycle_days":45,
    "inventory_value_year10_usd":2.5e9,
    "receivables_value_year10_usd":1.2e9,
    "payables_value_year10_usd":0.9e9,
    "net_working_capital_year10_usd":2.8e9,
    "working_capital_financing":"Revolving credit facility $3B (DBS + JP Morgan), 3-month SOFR + 150bps",
    "inventory_composition":"Frozen shrimp in cold storage (60 days average), processing in-progress, packaging materials",
    "seasonality":"Shrimp production is continuous (vessels follow seasons), but retail demand peaks Q4 (holidays)",
}

# === KPI DASHBOARD ===
KPI_DASHBOARD={
    "operational_kpis":[
        {"kpi":"Juveniles released per vessel per year","target":"350B","unit":"count"},
        {"kpi":"Recapture rate","target":"35%%","unit":"pct"},
        {"kpi":"Harvest yield per vessel per year","target":"167K t","unit":"tonnes"},
        {"kpi":"Vessel uptime","target":"95%%","unit":"pct"},
        {"kpi":"Energy self-sufficiency","target":"100%%","unit":"pct"},
        {"kpi":"Feed self-sufficiency","target":"100%%","unit":"pct"},
        {"kpi":"Bycatch escape ratio","target":"97%%","unit":"pct"},
        {"kpi":"Processing yield","target":"62%% (head-on to headless)","unit":"pct"},
        {"kpi":"Cold chain integrity","target":"99.99%%","unit":"pct"},
        {"kpi":"DNA barcode coverage","target":"100%% of batches","unit":"pct"},
    ],
    "financial_kpis":[
        {"kpi":"Revenue growth YoY","target":"15-20%%","unit":"pct"},
        {"kpi":"EBITDA margin (Year 10)","target":"48%%","unit":"pct"},
        {"kpi":"Net margin (Year 10)","target":"37%%","unit":"pct"},
        {"kpi":"ROCE (Year 10)","target":"22%%","unit":"pct"},
        {"kpi":"Current ratio","target":">2.0","unit":"ratio"},
        {"kpi":"Debt-to-equity","target":"<0.5","unit":"ratio"},
        {"kpi":"Cash conversion cycle","target":"<50 days","unit":"days"},
        {"kpi":"NPV (@8%% discount)","target":"$18.5B","unit":"usd"},
        {"kpi":"IRR","target":"28%%","unit":"pct"},
        {"kpi":"Payback period","target":"4 years","unit":"years"},
    ],
    "sustainability_kpis":[
        {"kpi":"Carbon footprint","target":"-0.5 kg CO2/kg shrimp (negative)","unit":"kg_co2_per_kg"},
        {"kpi":"Water use","target":"0 L freshwater/kg shrimp","unit":"L_per_kg"},
        {"kpi":"Land use","target":"0 m2/kg shrimp","unit":"m2_per_kg"},
        {"kpi":"Wild fish in feed (FIFO ratio)","target":"0.0 (zero fishmeal)","unit":"ratio"},
        {"kpi":"Antibiotic use","target":"0 kg/t shrimp","unit":"kg_per_t"},
        {"kpi":"Mangrove impact","target":"0 hectares","unit":"hectares"},
        {"kpi":"Community investment","target":"2%% of revenue","unit":"pct"},
    ],
    "hr_kpis":[
        {"kpi":"Employee retention","target":">90%%","unit":"pct"},
        {"kpi":"Safety (LTIFR)","target":"<0.5 per million hours","unit":"rate"},
        {"kpi":"Training hours per employee","target":">40 hours/year","unit":"hours"},
        {"kpi":"Gender diversity","target":"30%% female by Year 5","unit":"pct"},
        {"kpi":"Developing nation employment","target":"50%% of workforce","unit":"pct"},
    ],
}

# SECTION 2 -- COLORS
BG_TOP=(10,16,26); BG_BOT=(3,5,9); C_HULL=(58,74,96); C_HULL_BOOT=(120,40,44)
C_DECK=(70,78,90); C_SOLAR=(38,66,132); C_SOLAR_HI=(86,150,230); C_TANK=(150,158,168)
C_TANK_MESH=(90,150,170); C_H2TANK=(196,202,210); C_H2BAND=(90,200,130); C_RING=(96,110,128)
C_RING_HOT=(255,150,40); C_CHAMBER=(70,78,92); C_CHAMBER_FIRE=(120,190,255); C_FLYWHEEL=(150,60,55)
C_SHAFT=(200,205,215); C_GEN=(70,95,150); C_STEAM=(150,170,190); C_POD=(54,64,82)
C_PROP=(188,170,120); C_HOUSE=(176,182,190); C_HOUSE_WIN=(40,60,84); C_FUNNEL=(40,46,58)
C_BATT=(60,120,96); C_MAST=(150,156,166); C_TEXT=(224,230,238); C_TEXT_DIM=(150,160,175)
C_ACCENT=(90,200,255); C_GOOD=(90,220,130); C_WARN=(255,200,60); C_BAD=(255,90,90)
C_H2=(120,230,170); C_H2O=(40,100,140); C_SUN=(255,210,90); C_PANEL=(16,22,32); C_PANEL_HI=(28,38,54)
C_SEA1=(18,52,78); C_SEA2=(40,96,130); C_SKY1=(58,104,158); C_SKY2=(150,190,224)
C_SKY_NIGHT1=(6,10,24); C_SKY_NIGHT2=(22,34,58)
C_BROODSTOCK=(180,100,80); C_LARVAL=(100,180,200); C_NURSERY=(80,160,100); C_RELEASE=(200,120,60)
C_FEED=(160,140,80); C_DNA_LAB=(140,100,180); C_SHRIMP=(255,140,100); C_BIOFLOC=(120,180,100)
C_ALGAE=(60,180,80); C_ALGAE_POND=(40,120,60); C_ALGAE_PBR=(80,200,120); C_ALGAE_WATER=(20,80,50)
C_AI=(100,180,255); C_AI_DRIVE=(80,160,255); C_AI_BREED=(180,120,255); C_AI_HERD=(255,160,80); C_AI_MAINT=(255,220,80)
C_MAP_OCEAN=(12,28,52); C_MAP_LAND=(40,55,40); C_MAP_GRID=(20,35,55); C_MAP_HUB=(255,200,80)
C_MAP_RELEASE=(90,220,130); C_MAP_ROUTE=(90,200,255); C_MAP_ROUTE_SPRING=(120,220,100)
C_MAP_ROUTE_SUMMER=(255,200,80); C_MAP_ROUTE_AUTUMN=(255,140,80); C_MAP_ROUTE_WINTER=(100,180,255)

# SECTION 3 -- MINI 3D ENGINE (reused from SE.py)
VISUAL_DETAIL=1.25
def rot_x(a):
    c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]],dtype=float)
def rot_y(a):
    c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]],dtype=float)
def rot_z(a):
    c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]],dtype=float)

class Mesh:
    def __init__(self,verts,faces,color,name="",spin=1.0,group="default",
                 pivot=(0.,0.,0.),tilt=(0.,0.),hot=False,selectable=False):
        self.verts=np.asarray(verts,dtype=float); self.faces=faces; self.color=color
        self.name=name; self.spin=spin; self.group=group; self.pivot=np.asarray(pivot,dtype=float)
        self.tilt=tilt; self.hot=hot; self.chamber_index=None; self.selectable=selectable
    def world_verts(self,angle,selector_radius=None):
        v=self.verts
        if self.spin: v=v@rot_z(angle*self.spin).T
        rx,ry=self.tilt
        if rx or ry: v=v@(rot_x(rx)@rot_y(ry)).T
        pivot=self.pivot.copy()
        if self.selectable and selector_radius is not None: pivot[0]=selector_radius
        return v+pivot

def _detail_seg(seg): return max(8,int(round(seg*VISUAL_DETAIL)))
def _annulus_cylinder(r_out,r_in,z0,z1,seg=44):
    seg=_detail_seg(seg); verts,faces=[],[]
    ang=np.linspace(0,2*np.pi,seg,endpoint=False)
    for z in (z0,z1):
        for a in ang: verts.append((r_out*math.cos(a),r_out*math.sin(a),z))
        for a in ang: verts.append((r_in*math.cos(a),r_in*math.sin(a),z))
    def oo(layer,i): return layer*(2*seg)+(i%seg)
    def ii(layer,i): return layer*(2*seg)+seg+(i%seg)
    for i in range(seg):
        faces.append((oo(0,i),oo(0,i+1),oo(1,i+1),oo(1,i)))
        faces.append((ii(0,i),ii(1,i),ii(1,i+1),ii(0,i+1)))
        faces.append((oo(0,i),ii(0,i),ii(0,i+1),oo(0,i+1)))
        faces.append((oo(1,i),oo(1,i+1),ii(1,i+1),ii(1,i)))
    return verts,faces
def _solid_cylinder(r,z0,z1,seg=40):
    seg=_detail_seg(seg); verts,faces=[],[]
    ang=np.linspace(0,2*np.pi,seg,endpoint=False)
    for z in (z0,z1):
        for a in ang: verts.append((r*math.cos(a),r*math.sin(a),z))
    c0=len(verts); verts.append((0,0,z0)); c1=len(verts); verts.append((0,0,z1))
    for i in range(seg):
        a,b=i,(i+1)%seg; faces.append((a,b,seg+b,seg+a))
        faces.append((c0,b,a)); faces.append((c1,seg+a,seg+b))
    return verts,faces
def _box(cx,cy,cz,sx,sy,sz):
    hx,hy,hz=sx/2,sy/2,sz/2
    v=[(cx-hx,cy-hy,cz-hz),(cx+hx,cy-hy,cz-hz),(cx+hx,cy+hy,cz-hz),(cx-hx,cy+hy,cz-hz),
       (cx-hx,cy-hy,cz+hz),(cx+hx,cy-hy,cz+hz),(cx+hx,cy+hy,cz+hz),(cx-hx,cy+hy,cz+hz)]
    f=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    return v,f
def _pipe(p0,p1,r,col,seg=8):
    p0=np.asarray(p0,float); p1=np.asarray(p1,float); axis=p1-p0; L=np.linalg.norm(axis)
    if L<1e-9: return Mesh(*_solid_cylinder(r,0,0.001,seg=seg),col)
    axis=axis/L; tmp=np.array([0,0,1.0]) if abs(axis[2])<0.9 else np.array([1.0,0,0])
    u=np.cross(axis,tmp); u=u/(np.linalg.norm(u) or 1); w=np.cross(axis,u)
    verts,faces=[],[]; ring=np.linspace(0,2*np.pi,seg,endpoint=False)
    for end in (p0,p1):
        for a in ring: verts.append(tuple(end+r*math.cos(a)*u+r*math.sin(a)*w))
    for i in range(seg):
        a,b=i,(i+1)%seg; faces.append((a,b,seg+b,seg+a))
    return Mesh(verts,faces,col,spin=0.0)

class Part:
    def __init__(self,key,name,meshes,specs,order,explode,color):
        self.key=key; self.name=name; self.meshes=meshes; self.specs=specs
        self.order=order; self.explode=np.asarray(explode,dtype=float); self.color=color
        n=np.linalg.norm(self.explode); self.popdir=self.explode/n if n>1e-6 else np.array([0.,0.,1.])
        self.fire_anchor=None

def _place_spinner(meshes,pivot,tilt,group):
    piv=np.asarray(pivot,dtype=float)
    for m in meshes: m.pivot=piv.copy(); m.tilt=tilt; m.group=group
    return meshes
def _mix(c1,c2,t):
    return (int(c1[0]+(c2[0]-c1[0])*t),int(c1[1]+(c2[1]-c1[1])*t),int(c1[2]+(c2[2]-c1[2])*t))
def clamp(x,lo=0.0,hi=1.0): return max(lo,min(hi,x))
def _static(v,f,col,name="",group="static"): return Mesh(v,f,col,name=name,spin=0.0,group=group)
def remap_yz(v): return [(p[0],p[2],p[1]) for p in v]
def _eng(m): return m*ENG_DISP
def _hatch(m): return m*HATCH_DISP

# SECTION 4 -- GEOMETRY BUILDERS

def _polar_box(r,a,zc,sx,sy,sz,col,group,name="",chamber=None):
    v,f=_box(r,0.0,zc,sx,sy,sz); v=np.asarray(v,float)@rot_z(a).T
    m=Mesh(v,f,col,name=name,group=group); m.chamber_index=chamber; return m

def build_genset_parts():
    parts=[]; R_out=_eng(DIMS["ring_outer_d_m"]/2); R_in=_eng(DIMS["ring_inner_d_m"]/2)
    th=_eng(DIMS["ring_thick_m"]); z0,z1=-th/2,th/2; nch=DIMS["chambers"]
    ring_m=[]
    v,f=_annulus_cylinder(R_out,R_in,z0,z1,seg=48)
    ring_m.append(Mesh(v,f,C_RING,name="rotary ring",group="ring",hot=True))
    cd=_eng(DIMS["chamber_depth_m"]); cw=_eng(DIMS["chamber_width_m"]); r_mid=R_in+cd*0.5
    for i in range(nch):
        a=i*2*math.pi/nch
        ring_m.append(_polar_box(r_mid,a,0.0,cd,cw,th*0.72,C_CHAMBER,"ring",chamber=i))
    parts.append(Part("ring","8-CHAMBER H2 ROTOR",ring_m,
        ["8 concave chambers, 45 deg apart","burns HYDROGEN (blue flame)",
         "outer d %.2f m / thick %.2f m"%(DIMS["ring_outer_d_m"],DIMS["ring_thick_m"]),
         "direct-injected, turbo + supercharged",
         "MAT: forged 4140 chromoly steel + ceramic thermal barrier coating",
         "TECH: rotary annular combustion, no reciprocating parts"],0,(0,0,0),C_RING))
    parts[-1].fire_anchor=np.array([0.0,R_in+cd*0.4,0.0])
    inj=[]
    v,f=_box(0.0,R_out+_eng(0.16),0.0,_eng(0.12),_eng(0.34),_eng(0.16))
    inj.append(_static(v,f,(210,220,235),"H2 injector"))
    inj.append(_pipe((0,R_out+_eng(0.02),0),(0,R_out+_eng(0.30),0),_eng(0.045),C_H2))
    parts.append(Part("injector","H2 DIRECT INJECTOR",inj,
        ["fixed rim-top injector rail","350 bar H2 from the buffer",
         "meters the H2:air richness live",
         "MAT: Inconel 718 nozzle, 316L stainless rail",
         "TECH: piezoelectric direct injection, 350 bar common-rail"],1,(0,0.9,0),C_H2))
    rsh=_eng(DIMS["shaft_d_m"]/2); sl=_eng(DIMS["shaft_len_m"])
    v,f=_solid_cylinder(rsh,-sl*0.55,sl*0.45,seg=20)
    parts.append(Part("shaft","CENTRAL SHAFT (CORE)",
        [Mesh(v,f,C_SHAFT,name="shaft",group="core")],
        ["magnetic-bearing supported","carries ring torque to the generator",
         "d %.2f m"%DIMS["shaft_d_m"],
         "MAT: 17-4PH precipitation-hardened stainless steel",
         "TECH: active magnetic bearings, frictionless"],2,(0,0,0),C_SHAFT))
    rc=_eng(0.62)
    v,f=_annulus_cylinder(rc,rsh*1.4,z1+_eng(0.02),z1+_eng(0.10),seg=32)
    parts.append(Part("clutch","WET CLUTCH STACK",
        [Mesh(v,f,(60,140,165),name="clutch",group="core")],
        ["engages ring toward 1:1","low-slip wet plates"],3,(0,0,0.4),(60,140,165)))
    trans=[]; n_rings=DIMS["trans_rings"]; tr_out=_eng(DIMS["trans_outer_d_m"]/2)
    tr_th=_eng(DIMS["trans_thick_m"])
    for i in range(n_rings):
        r_outer=tr_out*(1.0-i*0.12); r_inner=r_outer-tr_th
        cz=z1+_eng(0.12)+i*tr_th*1.1
        v,f=_annulus_cylinder(r_outer,r_inner,cz,cz+tr_th,seg=36)
        col=_mix(C_RING,C_SHAFT,0.3+i*0.08)
        trans.append(Mesh(v,f,col,name="trans ring %d"%(i+1),group="trans"))
        for j in range(24):
            a=j*2*math.pi/24
            tv,tf=_box(r_outer,0.0,cz+tr_th*0.5,_eng(0.04),_eng(0.06),tr_th*0.7)
            tv=np.asarray(tv,float)@rot_z(a).T
            trans.append(Mesh(tv,tf,_mix(col,(0,0,0),0.2),group="trans"))
    parts.append(Part("trans","TRANSMISSION GEAR RINGS",trans,
        ["%d concentric gear-clutch layers"%n_rings,"step ring torque to generator speed",
         "wet-plate progressive engagement","outer d %.2f m"%DIMS["trans_outer_d_m"]],
        4,(0,0,0.6),C_SHAFT))
    og_d=_eng(DIMS["out_gear_d_m"]/2); og_t=_eng(DIMS["out_gear_thick_m"])
    ogz=z1+_eng(0.12)+n_rings*tr_th*1.1+_eng(0.08)
    og_m=[Mesh(*_solid_cylinder(og_d,ogz,ogz+og_t,seg=20),C_SHAFT,name="output gear",group="trans")]
    for j in range(16):
        a=j*2*math.pi/16
        tv,tf=_box(og_d,0.0,ogz+og_t*0.5,_eng(0.03),_eng(0.05),og_t*0.8)
        tv=np.asarray(tv,float)@rot_z(a).T
        og_m.append(Mesh(tv,tf,_mix(C_SHAFT,(0,0,0),0.15),group="trans"))
    parts.append(Part("outgear","OUTPUT GEAR",og_m,
        ["receives the transmission stack","direct-couples to the clutch plate",
         "d %.2f m"%DIMS["out_gear_d_m"]],5,(0,0,0.8),C_SHAFT))
    cp_d=_eng(DIMS["clutch_plate_d_m"]/2); cp_t=_eng(DIMS["clutch_plate_thick_m"])
    cpz=ogz+og_t+_eng(0.06); ts_d=_eng(DIMS["torque_shaft_d_m"]/2)
    ts_l=_eng(DIMS["torque_shaft_len_m"])
    C_CL=(180,160,100); C_CL_DK=(120,100,60); C_FR=(80,50,30)
    cl_m=[]
    v,f=_solid_cylinder(cp_d,cpz,cpz+cp_t,seg=48)
    cl_m.append(Mesh(v,f,C_CL,name="clutch disc",group="clutch"))
    for fz_off in (0,cp_t):
        v,f=_annulus_cylinder(cp_d*0.92,cp_d*0.30,cpz+fz_off-_eng(0.01),cpz+fz_off+_eng(0.01),seg=40)
        cl_m.append(Mesh(v,f,C_FR,name="friction ring",group="clutch"))
    for j in range(24):
        a=j*2*math.pi/24
        v,f=_box(cp_d*0.85,0.0,cpz+cp_t*0.5,_eng(0.04),_eng(0.08),cp_t*0.9)
        v=np.asarray(v,float)@rot_z(a).T
        cl_m.append(Mesh(v,f,_mix(C_CL_DK,(0,0,0),0.2),name="clutch segment",group="clutch"))
    v,f=_solid_cylinder(ts_d,cpz+cp_t,cpz+cp_t+ts_l,seg=16)
    cl_m.append(Mesh(v,f,C_SHAFT,name="drive shaft",group="clutch"))
    parts.append(Part("directclutch","DIRECT CLUTCH + DRIVE SHAFT",cl_m,
        ["wet clutch disc, friction plates","direct 1:1 engagement, no slip",
         "drive shaft -> generator coupling","clutch d %.2f m"%DIMS["clutch_plate_d_m"]],
        6,(0,0,1.0),C_CL))
    gd=_eng(DIMS["gen_d_m"]/2); gt=_eng(DIMS["gen_thick_m"]); gz=cpz+cp_t+ts_l+_eng(0.08)
    gen_m=[Mesh(*_solid_cylinder(gd,gz,gz+gt,seg=32),C_GEN,name="axial-flux generator",group="gen")]
    for j in range(20):
        a=j*2*math.pi/20
        tv,tf=_box(gd,0.0,gz+gt*0.5,_eng(0.03),_eng(0.06),gt*0.8)
        tv=np.asarray(tv,float)@rot_z(a).T
        gen_m.append(Mesh(tv,tf,_mix(C_GEN,(0,0,0),0.15),group="gen"))
    parts.append(Part("generator","AXIAL-FLUX GENERATOR",gen_m,
        ["converts mechanical torque to electricity","charges the battery bank",
         "d %.2f m, thick %.2f m"%(DIMS["gen_d_m"],DIMS["gen_thick_m"]),
         "MAT: NdFeB N52 magnets, silicon steel laminations",
         "TECH: axial-flux PMG, 97% efficiency"],7,(0,0,1.2),C_GEN))
    fly_d=_eng(DIMS["flywheel_d_m"]/2); fly_t=_eng(DIMS["flywheel_thick_m"])
    fly_m=[Mesh(*_solid_cylinder(fly_d,gz+gt+_eng(0.06),gz+gt+_eng(0.06)+fly_t,seg=40),
        C_FLYWHEEL,name="flywheel",group="fly")]
    parts.append(Part("flywheel","TUNGSTEN FLYWHEEL",fly_m,
        ["kinetic energy buffer","%.0f kg, magnetic bearings"%DIMS["flywheel_mass_kg"],
         "%.0f rpm max, burst power for acceleration"%FLYWHEEL_MAX_RPM,
         "MAT: tungsten heavy alloy (W-Ni-Fe, 18.5 g/cc)",
         "TECH: vacuum-sealed, active magnetic bearings, 80 kWh capacity"],8,(0,0,1.4),C_FLYWHEEL))
    td=_eng(DIMS["turbo_d_m"]/2)
    parts.append(Part("turbo","H2 TURBOCHARGER",
        [Mesh(*_solid_cylinder(td,z1-_eng(0.05),z1+_eng(0.25),seg=20),C_STEAM,name="turbo",group="turbo")],
        ["exhaust-driven turbo + slow auto supercharger","packs the H2:air charge"],
        9,(0.6,0,0),C_STEAM))
    bl_d=_eng(DIMS["boiler_d_m"]/2); bl_l=_eng(DIMS["boiler_len_m"])
    bl_m=[Mesh(*_solid_cylinder(bl_d,0,bl_l,seg=24),C_STEAM,name="boiler drum",group="steam")]
    for i in range(3):
        sd=_eng(DIMS["steam_stage_d_m"]/2); sz=bl_l+_eng(0.10)+i*_eng(0.12)
        bl_m.append(Mesh(*_solid_cylinder(sd,sz,sz+_eng(0.08),seg=16),C_STEAM,
            name="steam stage %d"%(i+1),group="steam"))
    sgd=_eng(DIMS["steam_gen_d_m"]/2); sgz=bl_l+_eng(0.50)
    bl_m.append(Mesh(*_solid_cylinder(sgd,sgz,sgz+_eng(0.20),seg=20),C_GEN,
        name="steam generator",group="steam"))
    parts.append(Part("steam","STEAM RECOVERY LOOP",bl_m,
        ["closed-loop 3-stage compound expander","%.0f%% of waste heat -> electricity"%(STEAM_RECOVER_FRAC*100),
         "steam generator keeps producing after shutdown",
         "MAT: 316L stainless boiler, Inconel 625 expander blades",
         "TECH: organic Rankine cycle, closed-loop working fluid"],10,(0,0.8,0.3),C_STEAM))
    hs_span=_eng(DIMS["heat_shield_span_m"]); hs_m=[]; nv=DIMS["heat_shield_vanes"]
    for i in range(nv):
        a=i*2*math.pi/nv
        v,f=_box(hs_span*0.4,0.0,0.0,_eng(0.04),hs_span*0.45,_eng(0.30))
        v=np.asarray(v,float)@rot_z(a).T
        hs_m.append(Mesh(v,f,_mix(C_RING_HOT,(0,0,0),0.3),name="heat vane",group="shield"))
    tb_d=_eng(DIMS["thermal_bank_d_m"]/2); tb_l=_eng(DIMS["thermal_bank_len_m"])
    hs_m.append(Mesh(*_solid_cylinder(tb_d,0,tb_l,seg=20),C_RING_HOT,name="thermal bank",group="shield"))
    parts.append(Part("heatshield","HEAT SHIELD + THERMAL BANK",hs_m,
        ["%d angled vanes aim heat at the boiler"%DIMS["heat_shield_vanes"],
         "PCM / hot-fluid thermal bank holds useful heat",
         "keeps making current after engine shutdown"],11,(0.6,0.6,0.4),C_RING_HOT))
    return parts

def _hull(sections):
    """Loft a smooth body shell from a list of rectangular cross-sections along Z.
    Each section is (z, halfwidth, y_bottom, y_top)."""
    verts,faces=[],[]
    rings=[]
    for (z,hw,y0,y1) in sections:
        base=len(verts)
        verts+=[(-hw,y0,z),(hw,y0,z),(hw,y1,z),(-hw,y1,z)]
        rings.append(base)
    for i in range(len(rings)-1):
        a,b=rings[i],rings[i+1]
        for k in range(4):
            k2=(k+1)%4
            faces.append((a+k,a+k2,b+k2,b+k))
    faces.append((rings[0],rings[0]+1,rings[0]+2,rings[0]+3))
    last=rings[-1]
    faces.append((last+3,last+2,last+1,last))
    return verts,faces

def _smooth_sections(ctrl,sub=3):
    """Catmull-Rom subdivide a list of loft cross-sections for a smoother shell."""
    pts=[np.array(s,dtype=float) for s in ctrl]
    n=len(pts); out=[]
    for i in range(n-1):
        p0,p1,p2,p3=pts[max(0,i-1)],pts[i],pts[i+1],pts[min(n-1,i+2)]
        for j in range(sub):
            t=j/sub; t2,t3=t*t,t*t*t
            s=0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3)
            out.append(tuple(s))
    out.append(tuple(pts[-1]))
    return out

def _pentamaran_hull_sections(hull_r,hull_len):
    """Generate lofted hull cross-sections for a slender pentamaran hull.
    From stern (-Z) to bow (+Z) with proper bow entry and transom stern."""
    r=hull_r; hl=hull_len
    ctrl=[
        (-hl/2,         0.75*r, 0.80*r, 1.10*r),   # transom stern
        (-hl/2*0.85,    0.90*r, 0.90*r, 1.08*r),
        (-hl/2*0.50,    0.98*r, 0.95*r, 1.05*r),
        (-hl/2*0.15,    1.00*r, 1.00*r, 1.02*r),   # full midbody
        ( hl/2*0.20,    1.00*r, 1.00*r, 1.02*r),
        ( hl/2*0.50,    0.92*r, 0.96*r, 1.04*r),
        ( hl/2*0.75,    0.65*r, 0.85*r, 1.08*r),
        ( hl/2*0.90,    0.35*r, 0.60*r, 1.12*r),   # fine bow entry
        ( hl/2*0.98,    0.08*r, 0.30*r, 1.15*r),   # stem
    ]
    return _smooth_sections(ctrl,sub=4)

def build_ship_parts():
    parts=[]; loa=scs(SHIP["loa_m"]); beam=scs(SHIP["beam_m"])
    freebd=scs(SHIP["freeboard_m"]); nh=SHIP["hull_count"]
    hull_parts=[]; hull_spacing=beam/(nh-1); hull_r=scs(4.0); hull_len=loa*0.92
    for hi in range(nh):
        xc=-beam/2+hi*hull_spacing; yk=-freebd-scs(2.0)
        # Proper lofted hull shape
        sections=_pentamaran_hull_sections(hull_r,hull_len)
        hv,hf=_hull(sections)
        hull_mesh=Mesh(hv,hf,C_HULL,name="hull %d"%(hi+1),group="static")
        hull_mesh.pivot=np.array([xc,yk,0.0]); hull_mesh.tilt=(0.0,0.0)
        hull_parts.append(hull_mesh)
        # Waterline/boot-topping stripe (thin band at waterline)
        for sx in (-1,1):
            v,f=_box(sx*hull_r*0.95,yk+scs(0.1),0.0,scs(0.15),scs(0.6),hull_len*0.85)
            stripe=_static(v,f,C_HULL_BOOT,"")
            stripe.pivot=np.array([xc,0.0,0.0]); stripe.tilt=(0.0,0.0)
            hull_parts.append(stripe)
        # Bulbous bow (below waterline, forward)
        bb_r=hull_r*0.55
        v,f=_solid_cylinder(bb_r,-bb_r*0.3,bb_r*0.8,seg=16)
        bbm=Mesh(v,f,_mix(C_HULL,(0,0,0),0.15),name="bulbous bow %d"%(hi+1),group="static")
        bbm.pivot=np.array([xc,yk-scs(0.5),hull_len/2+scs(1.0)]); bbm.tilt=(0.0,math.pi/2)
        hull_parts.append(bbm)
        # Bow nose cone (streamlined entry above bulb)
        v,f=_solid_cylinder(hull_r*0.5,0,scs(2.0),seg=16)
        nose=Mesh(v,f,_mix(C_HULL,(0,0,0),0.1),name="",group="static")
        nose.pivot=np.array([xc,yk+scs(0.5),hull_len/2+scs(0.5)]); nose.tilt=(0.0,math.pi/2)
        hull_parts.append(nose)
        # Deck cap on each hull
        v,f=_box(xc,yk+scs(1.0),0.0,hull_r*2.05,scs(0.3),hull_len*0.90)
        hull_parts.append(_static(v,f,_mix(C_DECK,(0,0,0),0.15),""))
    parts.append(Part("hulls","PENTAMARAN HULLS (5)",hull_parts,
        ["%d slender lofted hulls with bulbous bow"%nh,"LOA %.0f m, beam %.0f m"%(SHIP["loa_m"],SHIP["beam_m"]),
         "draft %.0f m, freeboard %.0f m"%(SHIP["draft_m"],SHIP["freeboard_m"]),
         "storm mode: ballast down in <30 min","survives Cat 5 with <10 deg roll",
         "MAT: AH36 marine steel hull + superhydrophobic SiO2 nano-coating",
         "TECH: semi-submersible pentamaran, waterplane <10%% in storm mode",
         "FORM: Catmull-Rom lofted hull, fine bow entry, transom stern"],
        0,(0,-1.5,0),C_HULL))
    deck_parts=[]; deck_y=0.0; dw=beam*0.95; dl=loa*0.88
    v,f=_box(0.0,deck_y,0.0,dw,scs(1.0),dl); deck_parts.append(_static(v,f,C_DECK,"truss deck"))
    # Deck truss cross-members
    for zi in range(12):
        zc=-dl/2+(zi+0.5)*(dl/12)
        v,f=_box(0.0,deck_y-scs(1.0),zc,dw,scs(0.3),scs(0.5))
        deck_parts.append(_static(v,f,_mix(C_DECK,(0,0,0),0.2),""))
    # Deck surface panels (lighter colored tiles)
    for zi in range(16):
        zc=-dl/2+(zi+0.5)*(dl/16)
        v,f=_box(0.0,deck_y+scs(0.02),zc,dw*0.98,scs(0.02),scs(dl/16*0.9))
        deck_parts.append(_static(v,f,_mix(C_DECK,(120,130,145),0.15),""))
    # Deck hatches (rectangular access hatches)
    for zi in range(4):
        zc=-dl/2*0.7+(zi+0.5)*(dl*0.7/4)
        v,f=_box(-scs(10),deck_y+scs(0.1),zc,scs(4.0),scs(0.15),scs(3.0))
        deck_parts.append(_static(v,f,_mix(C_DECK,(60,70,85),0.3),"deck hatch %d"%(zi+1)))
        # Hatch rim
        v,f=_box(-scs(10),deck_y+scs(0.18),zc,scs(4.2),scs(0.05),scs(3.2))
        deck_parts.append(_static(v,f,_mix(C_DECK,(0,0,0),0.4),""))
    # Deck cargo containers (stacked on port side)
    for zi in range(3):
        zc=-scs(20)+(zi+0.5)*scs(15)
        v,f=_box(scs(22),deck_y+scs(0.8),zc,scs(4.0),scs(2.0),scs(5.0))
        deck_parts.append(_static(v,f,_mix(C_HULL,(100,90,70),0.2),"cargo container %d"%(zi+1)))
        # Container ridges
        for ri in range(3):
            v,f=_box(scs(22),deck_y+scs(0.3)+ri*scs(0.5),zc,scs(4.02),scs(0.03),scs(5.0))
            deck_parts.append(_static(v,f,_mix(C_HULL,(0,0,0),0.3),""))
    parts.append(Part("deck","TRUSS DECK",deck_parts,
        ["connects all 5 hulls","deck area %.0f m2"%(SHIP["beam_m"]*SHIP["loa_m"]*0.8),
         "carries solar roof + hatchery systems",
         "MAT: AH36 steel truss + GRP (glass-reinforced polymer) deck panels",
         "TECH: modular truss connections, shock-absorbing"],1,(0,-0.8,0),C_DECK))
    # Deck railings along both sides
    rail_parts=[]; rail_h=scs(1.1); rail_col=_mix(C_DECK,(200,200,200),0.3)
    for sx in (-1,1):
        # Top rail
        v,f=_box(sx*dw/2,deck_y+rail_h,0.0,scs(0.08),scs(0.08),dl*0.95)
        rail_parts.append(_static(v,f,rail_col,"deck railing"))
        # Rail posts
        for zi in range(20):
            zc=-dl/2*0.95+(zi+0.5)*(dl*0.95/20)
            v,f=_box(sx*dw/2,deck_y+rail_h/2,zc,scs(0.05),rail_h,scs(0.05))
            rail_parts.append(_static(v,f,rail_col,""))
    parts.append(Part("railings","DECK RAILINGS",rail_parts,
        ["perimeter safety railings on truss deck","%.0f m total length"%(2*SHIP["loa_m"]*0.88),
         "MAT: 316L stainless steel pipes, 1.1 m height"],2,(0,0.3,0),rail_col))
    sl=scs(DIMS["solar_roof_len_m"]); sw=scs(DIMS["solar_roof_width_m"])
    sh=scs(DIMS["solar_roof_height_m"]); sy=deck_y+sh; solar=[]
    v,f=_box(0.0,sy,0.0,sw,scs(0.15),sl); solar.append(_static(v,f,C_SOLAR,"solar roof"))
    # Panel grid - longitudinal strips
    for i in range(8):
        zc=-sl/2+(i+0.5)*(sl/8)
        v,f=_box(0.0,sy+scs(0.02),zc,sw*0.98,scs(0.01),scs(0.04))
        solar.append(_static(v,f,C_SOLAR_HI,""))
    # Panel grid - transverse strips
    for i in range(6):
        xc=-sw/2+(i+0.5)*(sw/6)
        v,f=_box(xc,sy+scs(0.02),0.0,scs(0.04),scs(0.01),sl*0.98)
        solar.append(_static(v,f,C_SOLAR_HI,""))
    # Individual cell highlights (small bright dots)
    for i in range(16):
        zc=-sl/2+(i+0.5)*(sl/16)
        for j in range(4):
            xc=-sw/2*0.9+(j+0.5)*(sw*0.9/4)
            v,f=_box(xc,sy+scs(0.03),zc,scs(0.3),scs(0.01),scs(0.3))
            solar.append(_static(v,f,_mix(C_SOLAR_HI,(255,255,255),0.15),""))
    # Edge trim around roof perimeter
    for sx in (-1,1):
        v,f=_box(sx*sw/2,sy+scs(0.05),0.0,scs(0.1),scs(0.2),sl)
        solar.append(_static(v,f,_mix(C_SOLAR,(0,0,0),0.3),""))
    for sz in (-1,1):
        v,f=_box(0.0,sy+scs(0.05),sz*sl/2,sw,scs(0.2),scs(0.1))
        solar.append(_static(v,f,_mix(C_SOLAR,(0,0,0),0.3),""))
    # Support pillars with cross-bracing
    np_=DIMS["solar_roof_pillars"]
    for i in range(np_):
        zc=-sl/2+(i+0.5)*(sl/np_)
        for sx in (-1,1):
            v,f=_solid_cylinder(scs(0.15),0,sh,seg=8); v=remap_yz(v)
            p=_static(v,f,_mix(C_DECK,(0,0,0),0.3),""); p.pivot=np.array([sx*sw/2*0.95,deck_y,zc])
            solar.append(p)
            # Diagonal cross-brace
            if i<np_-1:
                zc2=-sl/2+((i+1)+0.5)*(sl/np_)
                solar.append(_pipe((sx*sw/2*0.95,deck_y,zc),(sx*sw/2*0.95,deck_y+sh*0.5,zc2),
                    scs(0.04),_mix(C_DECK,(0,0,0),0.35),seg=5))
    parts.append(Part("solar","SOLAR CARGO-ROOF CANOPY",solar,
        ["%.0f m2 PV @ %.0f%% eff"%(DIMS["solar_panel_m2"],DIMS["solar_eff"]*100),
         "peak %.1f MW, avg ~7.0 MW"%(SOLAR_PEAK_KW/1000),
         "%d support pillars"%DIMS["solar_roof_pillars"],"elevated -- hatchery below",
         "MAT: bifacial PERC monocrystalline silicon panels, anodized Al frame",
         "TECH: 26% efficiency, 12 deg pitch for rain shedding"],
        3,(0,1.2,0),C_SOLAR))
    et=[]; net=DIMS["electro_tanks"]; et_d=scs(DIMS["electro_tank_d_m"]/2); et_h=scs(DIMS["electro_tank_h_m"])
    for i in range(net):
        zc=-scs(80)+(i+0.5)*(scs(160)/net)
        v,f=_solid_cylinder(et_d,0,et_h,seg=20)
        et+=_place_spinner([Mesh(v,f,C_TANK,name="electrolysis tank %d"%(i+1),group="static")],
            (scs(15),-freebd-scs(5),zc),(math.pi/2,0),"static")
        # End cap bands
        for zc_end in (0,et_h):
            v,f=_annulus_cylinder(et_d*1.05,et_d*0.98,zc_end-scs(0.15),zc_end+scs(0.15),seg=16)
            et+=_place_spinner([Mesh(v,f,_mix(C_TANK,(0,0,0),0.3),name="",group="static")],
                (scs(15),-freebd-scs(5),zc),(math.pi/2,0),"static")
        # Connecting pipe to next tank
        if i<net-1:
            zc2=-scs(80)+((i+1)+0.5)*(scs(160)/net)
            et.append(_pipe((scs(15),-freebd-scs(5),zc+et_h/2),(scs(15),-freebd-scs(5),zc2-et_h/2),
                scs(0.12),_mix(C_TANK,(0,0,0),0.25),seg=6))
    parts.append(Part("electro","ELECTROLYSIS / BALLAST TANKS",et,
        ["%d dual-function tanks"%DIMS["electro_tanks"],"seawater -> H2 + O2, remaining = ballast",
         "%.0f kWh/kg, MMO anodes"%DIMS["electro_kwh_per_kg"],
         "%.0f t ballast per tank"%DIMS["ballast_capacity_t"],
         "MAT: titanium-lined 316L stainless, MMO anode (IrO2/Ta2O5 coating)",
         "TECH: PEM electrolysis, chlorine-suppressed"],4,(1.0,-0.8,0),C_TANK))
    h2=[]; nh2=DIMS["h2_tanks"]; h2_d=scs(DIMS["h2_tank_d_m"]/2); h2_l=scs(DIMS["h2_tank_len_m"])
    for i in range(nh2):
        zc=scs(70)+(i-nh2/2+0.5)*scs(5)
        v,f=_solid_cylinder(h2_d,-h2_l/2,h2_l/2,seg=16)
        h2+=_place_spinner([Mesh(v,f,C_H2TANK,name="H2 tank %d"%(i+1),group="static")],
            (scs(20),deck_y+scs(3),zc),(0,math.pi/2),"static")
        v,f=_annulus_cylinder(h2_d*1.02,h2_d*0.98,-scs(0.3),scs(0.3),seg=16)
        h2+=_place_spinner([Mesh(v,f,C_H2BAND,name="",group="static")],
            (scs(20),deck_y+scs(3),zc),(0,math.pi/2),"static")
        # End dome caps
        for zc_end in (-h2_l/2,h2_l/2):
            v,f=_solid_cylinder(h2_d*1.02,zc_end-scs(0.2),zc_end+scs(0.2),seg=16)
            h2+=_place_spinner([Mesh(v,f,_mix(C_H2TANK,(0,0,0),0.15),name="",group="static")],
                (scs(20),deck_y+scs(3),zc),(0,math.pi/2),"static")
        # Valve assembly on top
        v,f=_box(scs(20),deck_y+scs(3)+h2_d+scs(0.3),zc,scs(0.4),scs(0.5),scs(0.4))
        h2.append(_static(v,f,_mix(C_H2BAND,(0,0,0),0.2),"valve %d"%(i+1)))
    # Manifold pipe connecting all H2 tanks
    h2.append(_pipe((scs(20),deck_y+scs(3)+h2_d+scs(0.8),scs(70)-scs(2.5)),
        (scs(20),deck_y+scs(3)+h2_d+scs(0.8),scs(70)+(nh2-1)*scs(5)+scs(2.5)),
        scs(0.1),_mix(C_H2BAND,(0,0,0),0.2),seg=8))
    parts.append(Part("h2buffer","COMPRESSED H2 BUFFER",h2,
        ["%d tanks @ %.0f bar"%(DIMS["h2_tanks"],DIMS["h2_bar"]),
         "%.0f t total capacity"%(DIMS["h2_capacity_kg"]/1000),"~3-4 days cruise fuel",
         "MAT: carbon-fiber wrapped Type IV tanks (HDPE liner + CF shell)",
         "TECH: 350 bar compressed H2 storage"],
        5,(1.2,0.5,0),C_H2TANK))
    eng=[]; e_d=scs(2.5); e_l=scs(4.0)
    v,f=_solid_cylinder(e_d,0,e_l,seg=24)
    eng=_place_spinner([Mesh(v,f,C_RING,name="rotary H2 engine",group="genring")],
        (scs(25),deck_y+scs(1),scs(60)),(0,math.pi/2),"genring")
    parts.append(Part("genset","ROTARY H2 ENGINE",eng,
        ["8-chamber rotary, %.1f MW electric"%(GENSET_RATED_KW/1000),"burns onboard H2 (free fuel)",
         "charges battery as supplement","closed-loop steam recovery"],6,(1.0,0.8,0.3),C_RING))
    batt=[]; bt_w=scs(DIMS["batt_bank_w_m"]); bt_h=scs(DIMS["batt_bank_h_m"]); bt_l=scs(DIMS["batt_bank_len_m"])
    for i in range(4):
        zc=-scs(60)+(i+0.5)*scs(30)
        v,f=_box(scs(10),-freebd-scs(3),zc,bt_w,bt_h,bt_l)
        batt.append(_static(v,f,C_BATT,"battery bank %d"%(i+1)))
    parts.append(Part("battery","STRUCTURAL BATTERY BANK",batt,
        ["%.0f MWh marine LFP"%ELEC["batt_mwh"],"%d modules"%DIMS["batt_modules"],
         "carries the ship through the night",
         "MAT: lithium iron phosphate (LiFePO4) prismatic cells",
         "TECH: structural battery, integrated into hull frames"],7,(0.5,-1.2,0.3),C_BATT))
    house=[]; hl=scs(DIMS["house_len_m"]); hw=scs(DIMS["house_w_m"]); hh=scs(DIMS["house_h_m"])
    # Main bridge structure
    v,f=_box(scs(30),deck_y+hh/2,scs(85),hw,hh,hl); house.append(_static(v,f,C_HOUSE,"bridge"))
    # Bridge windows - front (starboard side, 5 windows)
    for zi in range(5):
        zc=scs(85)-hl/2+(zi+0.5)*(hl/5)
        v,f=_box(scs(30)+hw/2,deck_y+hh*0.7,zc,scs(0.1),scs(3.0),scs(3.0))
        house.append(_static(v,f,C_HOUSE_WIN,""))
    # Bridge windows - second row (lower)
    for zi in range(5):
        zc=scs(85)-hl/2+(zi+0.5)*(hl/5)
        v,f=_box(scs(30)+hw/2,deck_y+hh*0.35,zc,scs(0.1),scs(2.0),scs(2.0))
        house.append(_static(v,f,_mix(C_HOUSE_WIN,(0,0,0),0.3),""))
    # Side windows (port side)
    for zi in range(4):
        zc=scs(85)-hl/2*0.8+(zi+0.5)*(hl*0.8/4)
        v,f=_box(scs(30)-hw/2,deck_y+hh*0.55,zc,scs(0.1),scs(1.5),scs(1.5))
        house.append(_static(v,f,_mix(C_HOUSE_WIN,(0,0,0),0.2),""))
    # Bridge wing (extends outward)
    v,f=_box(scs(30)+hw/2+scs(1.5),deck_y+hh*0.65,scs(85),scs(3.0),scs(0.5),scs(3.0))
    house.append(_static(v,f,_mix(C_HOUSE,(0,0,0),0.15),"bridge wing"))
    # Lower deckhouse (wider base)
    v,f=_box(scs(30),deck_y+scs(1.0),scs(85),hw*1.3,scs(2.0),hl*1.1)
    house.append(_static(v,f,_mix(C_HOUSE,(0,0,0),0.2),"deckhouse base"))
    # Funnel
    fd=scs(DIMS["funnel_d_m"]/2); fh=scs(DIMS["funnel_h_m"])
    v,f=_solid_cylinder(fd,0,fh,seg=16)
    house+=_place_spinner([Mesh(v,f,C_FUNNEL,name="funnel",group="static")],
        (scs(30),deck_y+hh,scs(85)),(math.pi/2,0),"static")
    # Funnel cap (flat top)
    v,f=_solid_cylinder(fd*1.1,-scs(0.15),scs(0.15),seg=16)
    fc=Mesh(v,f,_mix(C_FUNNEL,(0,0,0),0.3),name="",group="static")
    fc.pivot=np.array([scs(30),deck_y+hh+fh,scs(85)]); fc.tilt=(math.pi/2,0)
    house.append(fc)
    # Exhaust pipe inside funnel
    v,f=_solid_cylinder(fd*0.4,0,fh*0.9,seg=8)
    ep=Mesh(v,f,_mix(C_FUNNEL,(20,20,20),0.5),name="",group="static")
    ep.pivot=np.array([scs(30),deck_y+hh+scs(0.2),scs(85)]); ep.tilt=(math.pi/2,0)
    house.append(ep)
    parts.append(Part("house","BRIDGE SUPERSTRUCTURE",house,
        ["command bridge + crew quarters","%.0f m x %.0f m x %.0f m"%(DIMS["house_len_m"],DIMS["house_w_m"],DIMS["house_h_m"]),
         "crew: %d"%SHIP["crew"],
         "MAT: AH36 steel superstructure + aluminum bridge windows",
         "TECH: 360 deg visibility, integrated bridge system"],8,(0,1.0,0.5),C_HOUSE))
    pods=[]; n_pods=DIMS["pods"]; pd=scs(DIMS["pod_pod_d_m"]/2); pl=scs(DIMS["pod_pod_len_m"])
    pr=scs(DIMS["prop_d_m"]/2)
    for i in range(n_pods):
        xc=-scs(20)+(i+0.5)*scs(40/n_pods); zc=-loa*0.45
        # Pod housing
        v,f=_solid_cylinder(pd,0,pl,seg=16)
        pods+=_place_spinner([Mesh(v,f,C_POD,name="pod %d"%(i+1),group="pod")],
            (xc,-freebd-scs(3),zc),(math.pi/2,0),"pod")
        # Pod strut (connects pod to hull)
        v,f=_box(xc,-freebd-scs(3)+pd,zc,scs(0.3),scs(2.0),scs(0.5))
        pods.append(_static(v,f,_mix(C_POD,(0,0,0),0.2),"pod strut %d"%(i+1)))
        # Propeller blades
        prop=[]
        for b in range(DIMS["prop_blades"]):
            a=b*2*math.pi/DIMS["prop_blades"]
            v,f=_box(pr*0.7,0.0,0.0,scs(0.15),pr*0.8,scs(0.04))
            v=np.asarray(v,float)@rot_z(a).T
            prop.append(Mesh(v,f,C_PROP,name="prop blade",group="prop"))
        pods+=_place_spinner(prop,(xc,-freebd-scs(3),zc-pl/2-scs(1.0)),(0,math.pi/2),"prop")
        # Propeller boss/hub
        v,f=_solid_cylinder(scs(0.3),0,scs(0.5),seg=12)
        pb=Mesh(v,f,_mix(C_PROP,(0,0,0),0.3),name="",group="prop")
        pb.pivot=np.array([xc,-freebd-scs(3),zc-pl/2-scs(1.3)]); pb.tilt=(0,math.pi/2)
        pods.append(pb)
    parts.append(Part("pods","EM-RAIL AZIMUTH PODS",pods,
        ["%d steerable electric thrusters"%DIMS["pods"],"%d-pole EM-rail direct drive"%DIMS["rail_poles"],
         "~97.8%% efficient, regenerates on current","prop d %.1f m"%DIMS["prop_d_m"],
         "MAT: bronze propeller (Cu-Mn-Al alloy), 316L stainless pod housing",
         "TECH: 128-pole EM-rail direct drive, no gearbox, 360 deg azimuth"],
        9,(0,-1.0,-0.8),C_POD))
    fins=[]; nfin=DIMS["heave_fins"]; fspan=scs(DIMS["heave_fin_span_m"]); fchord=scs(DIMS["heave_fin_chord_m"])
    per_side=nfin//2
    for sx in (-1,1):
        for i in range(per_side):
            zc=-1.0+(i+0.5)*(2.0/per_side); xc=sx*(beam/2*1.02)
            v,f=_box(xc,0.0,zc,scs(0.12),fspan*1.15,scs(0.18))
            fins.append(_static(v,f,_mix(C_HULL,(0,0,0),0.3),""))
            v,f=_box(xc+sx*scs(0.5),0.0,zc,scs(0.9),fchord*0.85,scs(1.4))
            fins.append(_static(v,f,_mix(C_SOLAR,C_H2,0.25),"heave-oar %d"%(i+1) if sx>0 else ""))
    parts.append(Part("heavefins","STABILIZING HEAVE-OAR GENERATORS",fins,
        ["%d hull-side oar-fins on linear-gen rails"%DIMS["heave_fins"],
         "buoyancy UP + gravity DOWN, 2-in-1 sail","one generator stroke each way per wave",
         "MAT: carbon-fiber composite fins, 316L stainless rails",
         "TECH: dual-direction linear alternator, 2-in-1 wind sail"],
        10,(1.3,0.0,0.0),C_SOLAR))
    sail=[]; nsm=DIMS["sail_masts"]; mh=scs(DIMS["sail_height_m"]); md=scs(DIMS["sail_mast_d_m"]/2)
    bw=scs(DIMS["sail_width_m"]); bd=scs(DIMS["sail_boom_d_m"]/2)
    C_SF=(235,230,215); C_SE=(180,170,150)
    for i in range(nsm):
        zc=-0.8+(i+0.5)*(1.6/nsm); base_y=scs(1.0)
        v,f=_solid_cylinder(md,0,mh,seg=12); v=remap_yz(v)
        m=_static(v,f,_mix(C_MAST,(60,50,40),0.3),"sail mast %d"%(i+1)); m.pivot=np.array([0.0,base_y,zc])
        sail.append(m)
        v,f=_solid_cylinder(bd,-bw/2,bw/2,seg=10); bv=np.asarray(v,float)@rot_x(math.pi/2).T
        b=_static(bv.tolist(),f,_mix(C_MAST,(60,50,40),0.3),"sail boom %d"%(i+1))
        b.pivot=np.array([0.0,base_y+scs(1.2),zc]); sail.append(b)
        yh=base_y+mh*0.78
        v,f=_solid_cylinder(bd*0.8,-bw*0.45,bw*0.45,seg=8); yv=np.asarray(v,float)@rot_x(math.pi/2).T
        yd=_static(yv.tolist(),f,_mix(C_MAST,(50,40,30),0.4),""); yd.pivot=np.array([0.0,yh,zc]); sail.append(yd)
        for p in range(5):
            t0=p/5; t1=(p+1)/5
            y0=yh+(base_y+scs(1.2)-yh)*t0; y1=yh+(base_y+scs(1.2)-yh)*t1
            w_avg=bw*(0.45+0.55*(1.0-(t0+t1)/2)); y_avg=(y0+y1)/2; h_p=abs(y1-y0)
            belly=scs(0.25)*math.sin(math.pi*(t0+t1)/2)
            v,f=_box(belly,y_avg,zc,w_avg,h_p*0.95,scs(0.03))
            sail.append(_static(v,f,_mix(C_SF,C_SE,0.05+0.03*p),"sail panel %d.%d"%(i+1,p+1)))
    if nsm>0:
        parts.append(Part("sails","FABRIC SAIL ARRAY",sail,
            ["%d literal sailboat sails on tall masts"%DIMS["sail_masts"],
             "%.0f m2 Dacron per mast"%DIMS["sail_area_m2"],
             "deploy @ >%.0f m/s, furl @ >%.0f m/s"%(FABRIC_SAIL["deploy_ms"],FABRIC_SAIL["furl_ms"]),
             "direct THRUST when wind is high",
             "MAT: Dacron polyester sailcloth on carbon-fiber masts",
             "TECH: automated furling system, wind-speed triggered"],11,(0.7,1.2,0.3),C_SF))
    wm=[]; wd=scs(DIMS["rotor_d_m"]); wh=scs(DIMS["rotor_h_m"]); n_wm=DIMS["rotors"]
    hub_r=scs(DIMS["rotor_hub_d_m"]/2); ytop_wm=scs(0.5)+scs(3.0)
    C_RD=(100,110,130); C_RA=(130,145,170); C_RH=(80,90,110)
    for i in range(n_wm):
        zc=-0.8+(i+0.5)*(1.5/n_wm); cx=0.0 if n_wm==1 else ((-1)**i)*scs(2.0)
        v,f=_solid_cylinder(scs(0.10),0,scs(0.6),seg=8); v=remap_yz(v)
        ms=_static(v,f,C_MAST,""); ms.pivot=np.array([cx,ytop_wm,zc]); wm.append(ms)
        rotor=[]
        v,f=_solid_cylinder(hub_r,0,wh,seg=12); rotor.append(Mesh(v,f,C_RH,name="rotor hub",group="rotor"))
        for zc_end in (0,wh):
            v,f=_annulus_cylinder(wd/2,hub_r*0.9,zc_end-scs(0.04),zc_end+scs(0.04),seg=32)
            rotor.append(Mesh(v,f,C_RD,name="rotor disc",group="rotor"))
        n_arms=DIMS["rotor_blades"]
        for b in range(n_arms):
            a0=b*2*math.pi/n_arms
            for s in range(8):
                t0=s/8; t1=(s+1)/8; a_mid=a0+(t0+t1)*0.5*math.pi*0.6
                y0=wh*t0; y1=wh*t1; y_avg=(y0+y1)/2
                r_arm=wd/2*(0.92-0.08*abs(0.5-(t0+t1)/2)*2)
                v,f=_box(r_arm,0.0,y_avg,scs(0.16),scs(0.05),abs(y1-y0)*1.1)
                v=np.asarray(v,float)@rot_z(a_mid).T
                rotor.append(Mesh(v,f,_mix(C_RA,(255,255,255),0.08),name="",group="rotor"))
        for zc_r in (scs(0.06),wh-scs(0.06)):
            v,f=_annulus_cylinder(wd/2,wd/2-scs(0.05),zc_r-scs(0.03),zc_r+scs(0.03),seg=40)
            rotor.append(Mesh(v,f,C_RD,name="rotor rim",group="rotor"))
        v,f=_solid_cylinder(hub_r*1.4,-scs(0.08),scs(0.08),seg=16)
        rotor.append(Mesh(v,f,C_GEN,name="rotor generator",group="rotor"))
        wm+=_place_spinner(rotor,(cx,ytop_wm+scs(0.6),zc),(math.pi/2,0),"rotor")
    parts.append(Part("rotors","DECK ROTOR ARRAY",wm,
        ["%d Gman's 117-style rotary energy harvesters"%DIMS["rotors"],
         "NOT turbines -- same rotary disc geometry as engine",
         "%d helical arms, spin on wind from ANY heading"%DIMS["rotor_blades"],
         "d %.1f m x h %.1f m each"%(DIMS["rotor_d_m"],DIMS["rotor_h_m"]),
         "MAT: carbon-fiber composite blades, steel hub",
         "TECH: vertical-axis drag+lift hybrid, always-on generation"],
        12,(0,1.6,0.4),C_RD))
    tun=[]; tw=scs(DIMS["tunnel_w_m"]); th_=scs(DIMS["tunnel_h_m"]); tl=scs(DIMS["tunnel_len_m"])
    ty=-freebd-scs(2.0)
    v,f=_box(0.0,ty+th_/2,0.02,tw,scs(0.10),tl); tun.append(_static(v,f,_mix(C_HULL,(0,0,0),0.2),"flow tunnel roof"))
    v,f=_box(0.0,ty-th_/2,0.02,tw,scs(0.10),tl); tun.append(_static(v,f,_mix(C_HULL,(0,0,0),0.2),""))
    for sx in (-1,1):
        v,f=_box(sx*tw/2,ty,0.02,scs(0.08),th_,tl); tun.append(_static(v,f,_mix(C_HULL,(0,0,0),0.35),""))
    nt=DIMS["tunnel_turbines"]
    for i in range(nt):
        zc=-1.3+(i+0.5)*(2.4/nt)
        v,f=_annulus_cylinder(th_*0.42,th_*0.10,-scs(0.05),scs(0.05),seg=16)
        tun+=_place_spinner([Mesh(v,f,_mix(C_H2,(0,0,0),0.1),name="",group="tunnelturb")],
            (0.0,ty,zc),(0,math.pi/2),"tunnelturb")
    parts.append(Part("tunnel","THROUGH-HULL FLOW TUNNEL",tun,
        ["bow intake -> stern exit, fills the wake","cuts hull PRESSURE (form) drag at speed",
         "%d in-duct micro-turbines skim the flow"%DIMS["tunnel_turbines"],
         "MAT: 316L stainless duct, titanium turbine blades",
         "TECH: passive flow-through, 8 micro-turbines"],
        13,(0,-0.4,0.0),C_H2))
    weights=[]; wb=scs(DIMS["weight_bob_d_m"]*0.5); drop=scs(DIMS["weight_drop_m"])
    per_side=DIMS["weight_harvesters"]//2
    for sx in (-1,1):
        for i in range(per_side):
            zc=-1.0+(i+0.5)*(2.0/per_side); xc=sx*scs(6.0)
            top=scs(0.0)-scs(0.2); bot=top-drop
            weights.append(_pipe((xc,top,zc),(xc,bot,zc),scs(0.05),C_SHAFT,seg=8))
            v,f=_solid_cylinder(wb,-wb,wb,seg=14)
            bob=_static(v,f,_mix(C_FLYWHEEL,C_H2,0.10),"hanging weight" if (sx>0 and i==0) else "")
            bob.pivot=np.array([xc,bot,zc]); bob.tilt=(math.pi/2,0.0); weights.append(bob)
    parts.append(Part("weights","HANGING INTERNAL WEIGHT HARVESTERS",weights,
        ["%d internal suspended bobs reclaim roll/pitch/heave"%DIMS["weight_harvesters"],
         "inside the hull, no external drag penalty",
         "MAT: tungsten alloy bobs, Kevlar suspension cables",
         "TECH: linear generator rails, dual-direction harvest"],14,(1.0,-0.8,0.5),C_FLYWHEEL))
    brood=[]; nbt=12; bt_d=scs(DIMS["broodstock_tank_d_m"]/2); bt_h=scs(DIMS["broodstock_tank_h_m"])
    for i in range(nbt):
        zc=-0.7+(i+0.5)*(1.4/nbt)
        for sx in (-1,1):
            xc=sx*scs(12.0)
            v,f=_solid_cylinder(bt_d,0,bt_h,seg=16)
            brood+=_place_spinner([Mesh(v,f,C_BROODSTOCK,
                name="broodstock tank %d"%(i+1) if sx>0 else "",group="static")],
                (xc,-freebd-scs(4),zc),(math.pi/2,0),"static")
    parts.append(Part("broodstock","BROODSTOCK MATURATION TANKS",brood,
        ["%d total RAS tanks in submerged hulls"%DIMS["broodstock_tanks"],
         "%d broodstock females (P. monodon)"%DIMS["broodstock_females"],
         "%.0fK eggs/female/spawn, %d spawns/year"%(SHRIMP["eggs_per_spawn"]/1000,SHRIMP["spawns_per_year"]),
         "LED photoperiod control, AI water quality",
         "MAT: fiberglass RAS tanks, HDPE piping, titanium heat exchangers",
         "TECH: Recirculating Aquaculture System, biofloc + ozone"],15,(0,-1.5,0.3),C_BROODSTOCK))
    larval=[]; nlt=10; lt_d=scs(DIMS["larval_tank_d_m"]/2); lt_h=scs(DIMS["larval_tank_h_m"])
    for i in range(nlt):
        zc=-0.6+(i+0.5)*(1.2/nlt)
        for sx in (-1,1):
            xc=sx*scs(8.0)
            v,f=_solid_cylinder(lt_d,0,lt_h,seg=14)
            larval+=_place_spinner([Mesh(v,f,C_LARVAL,
                name="larval tank %d"%(i+1) if sx>0 else "",group="static")],
                (xc,-freebd-scs(2),zc),(math.pi/2,0),"static")
    parts.append(Part("larval","LARVAL REARING SECTION",larval,
        ["%d larval rearing tanks"%DIMS["larval_tanks"],"nauplii -> PL20 (20 days post-hatch)",
         "egg->nauplii %.0f%%, nauplii->PL20 %.0f%%"%(SHRIMP["egg_to_nauplii"]*100,SHRIMP["nauplii_to_pl20"]*100),
         "Artemia + formulated microdiet, ozone treatment"],16,(0,-1.2,-0.3),C_LARVAL))
    nursery=[]; nnp=8; np_d=scs(DIMS["nursery_pool_d_m"]/2); np_h=scs(DIMS["nursery_pool_h_m"])
    for i in range(nnp):
        zc=-0.5+(i+0.5)*(1.0/nnp)
        for sx in (-1,1):
            xc=sx*scs(5.0)
            v,f=_solid_cylinder(np_d,0,np_h,seg=18)
            nursery+=_place_spinner([Mesh(v,f,C_NURSERY,
                name="nursery pool %d"%(i+1) if sx>0 else "",group="static")],
                (xc,-freebd-scs(1),zc),(math.pi/2,0),"static")
    parts.append(Part("nursery","NURSERY GROW-OUT POOLS",nursery,
        ["%d nursery grow-out pools"%DIMS["nursery_pools"],"PL20 -> 5-10g juvenile (90-120 days)",
         "survival %.0f%%, biofloc/RAS"%(SHRIMP["pl20_to_juvenile"]*100),
         "~3-4 cycles/year per tank volume"],17,(0,-1.0,0.5),C_NURSERY))
    release=[]; nrc=DIMS["release_chutes"]; rc_d=scs(DIMS["release_chute_d_m"]/2)
    rc_l=scs(DIMS["release_chute_len_m"])
    for i in range(nrc):
        zc=-0.8+(i+0.5)*(1.6/nrc)
        v,f=_solid_cylinder(rc_d,0,rc_l,seg=12)
        release+=_place_spinner([Mesh(v,f,C_RELEASE,name="release chute %d"%(i+1),group="static")],
            (0.0,-freebd-scs(2),zc),(math.pi/2,0),"static")
    parts.append(Part("release","RELEASE CHUTES",release,
        ["%d release chutes on submerged hulls"%DIMS["release_chutes"],
         "timed mass release into nursery grounds","weekly schedule, GPS + current modeling",
         "DNA barcoded (CRISPR-Cas9 marker)",
         "MAT: 316L stainless chutes, hydraulic actuated gates",
         "TECH: GPS-guided timed release, CRISPR-Cas9 DNA barcoding"],18,(0,-1.8,0),C_RELEASE))
    feed=[]; nft=DIMS["feed_tanks"]; ft_d=scs(DIMS["feed_tank_d_m"]/2); ft_h=scs(DIMS["feed_tank_h_m"])
    for i in range(nft):
        zc=-0.7+(i+0.5)*(1.4/nft)
        v,f=_solid_cylinder(ft_d,0,ft_h,seg=14)
        feed+=_place_spinner([Mesh(v,f,C_FEED,name="feed tank %d"%(i+1),group="static")],
            (scs(18),deck_y+scs(0.5),zc),(math.pi/2,0),"static")
    parts.append(Part("feed","FEED PRODUCTION TANKS",feed,
        ["%d feed production tanks"%DIMS["feed_tanks"],"70%% onboard: biofloc + Artemia + formulated diet",
         "FCR %.1f, $%.1f/kg feed"%(SHRIMP["fcr"],SHRIMP["feed_cost_kg"]),
         "MAT: fiberglass tanks, HDPE piping, titanium heat exchangers",
         "TECH: biofloc fermentation + Artemia culture + extruded diet"],
        19,(1.0,0.3,0.3),C_FEED))
    lab=[]; ll=scs(10.0); lw=scs(8.0); lh=scs(DIMS["dna_lab_h_m"])
    v,f=_box(scs(28),deck_y+lh/2,scs(70),lw,lh,ll); lab.append(_static(v,f,C_DNA_LAB,"DNA barcoding lab"))
    parts.append(Part("dnalab","DNA BARCODING LAB",lab,
        ["CRISPR-Cas9 inserted neutral marker","every batch barcoded for recapture tracking",
         "%.0f m2 lab area"%DIMS["dna_lab_m2"],"legal ownership of tagged biomass",
         "MAT: cleanroom modular lab, Class 10K ISO 7",
         "TECH: CRISPR-Cas9 gene editing, PCR barcoding, AI batch tracking"],
        20,(0.8,0.5,0.2),C_DNA_LAB))
    # --- INNOVATION FEATURES ---
    C_OTEC=(60,140,180); C_KITE=(200,180,100); C_AUV=(80,180,160); C_RAFT=(180,160,220)
    C_ANT=(200,200,210); C_AIRLUBE=(100,200,255)
    # OTEC cold-water pipe (long pipe descending from hull into deep water)
    otec=[]; otec_pipe_r=scs(0.8); otec_pipe_l=scs(60.0)
    v,f=_solid_cylinder(otec_pipe_r,0,otec_pipe_l,seg=16)
    opm=Mesh(v,f,C_OTEC,name="OTEC cold-water pipe",group="static")
    opm.pivot=np.array([-scs(15),-freebd-scs(2),scs(40)]); opm.tilt=(math.pi/2,0)
    otec.append(opm)
    # OTEC heat exchanger unit on deck
    v,f=_box(scs(15),deck_y+scs(0.5),scs(40),scs(3.0),scs(2.0),scs(4.0))
    otec.append(_static(v,f,_mix(C_OTEC,(0,0,0),0.2),"OTEC heat exchanger"))
    # OTEC warm water intake (side pipe)
    v,f=_solid_cylinder(scs(0.5),0,scs(2.0),seg=12)
    wi=Mesh(v,f,_mix(C_OTEC,(0,0,0),0.3),name="",group="static")
    wi.pivot=np.array([scs(15),-freebd-scs(1),scs(42)]); wi.tilt=(0,math.pi/2)
    otec.append(wi)
    # OTEC turbine housing
    v,f=_solid_cylinder(scs(1.0),0,scs(1.5),seg=16)
    ot=Mesh(v,f,_mix(C_OTEC,C_GEN,0.3),name="OTEC turbine",group="static")
    ot.pivot=np.array([scs(15),deck_y+scs(1.8),scs(40)]); ot.tilt=(0,0)
    otec.append(ot)
    parts.append(Part("otec","OTEC DEEP-WATER SYSTEM",otec,
        ["3 MW 24/7 baseload from ocean thermal gradient",
         "cold water pipe to 1000 m depth, warm surface intake",
         "MAT: HDPE cold-water pipe, titanium heat exchangers",
         "TECH: closed-cycle Rankine, ammonia working fluid"],21,(0,-1.5,0.5),C_OTEC))
    # AUV bay (stern deck, 8 drone tubes in 2 rows)
    auv=[]
    v,f=_box(0.0,deck_y+scs(0.3),-scs(75),scs(12.0),scs(1.5),scs(10.0))
    auv.append(_static(v,f,_mix(C_AUV,(0,0,0),0.25),"AUV bay"))
    # Bay roof/rack
    v,f=_box(0.0,deck_y+scs(1.8),-scs(75),scs(12.0),scs(0.2),scs(10.0))
    auv.append(_static(v,f,_mix(C_AUV,(0,0,0),0.15),""))
    # Support columns
    for sx in (-1,1):
        for zi in range(4):
            zc=-scs(78)+(zi+0.5)*scs(3.0)
            v,f=_box(sx*scs(5.5),deck_y+scs(1.0),zc,scs(0.15),scs(1.0),scs(0.15))
            auv.append(_static(v,f,_mix(C_AUV,(0,0,0),0.3),""))
    # AUV drones
    for i in range(8):
        zc=-scs(78)+(i%4)*scs(2.5); xc=-scs(4.0)+(i//4)*scs(8.0)
        v,f=_solid_cylinder(scs(0.4),0,scs(3.0),seg=12)
        am=Mesh(v,f,C_AUV,name="AUV %d"%(i+1),group="static")
        am.pivot=np.array([xc,deck_y+scs(0.8),zc]); am.tilt=(0,math.pi/2)
        auv.append(am)
        # AUV tail fin
        v,f=_box(scs(0.15),0.0,0.0,scs(0.04),scs(0.3),scs(0.15))
        tf=Mesh(v,f,_mix(C_AUV,(0,0,0),0.2),name="",group="static")
        tf.pivot=np.array([xc,deck_y+scs(0.8),zc-scs(1.6)]); tf.tilt=(0,math.pi/2)
        auv.append(tf)
    parts.append(Part("auvbay","AUV FLEET BAY",auv,
        ["8 autonomous underwater vehicles, 24h endurance",
         "500 m depth rating, sonar + water sampling",
         "MAT: titanium hull AUVs, 316L stainless launch bay",
         "TECH: autonomous survey, swarm coordination"],23,(0,0.3,-1.0),C_AUV))
    # Floating solar raft stowage (stowed panels on side decks)
    raft=[]
    for sx in (-1,1):
        for i in range(3):
            zc=-scs(40)+(i+0.5)*scs(25)
            v,f=_box(sx*scs(28),deck_y+scs(0.2),zc,scs(4.0),scs(0.3),scs(8.0))
            raft.append(_static(v,f,_mix(C_RAFT,C_SOLAR,0.15),"solar raft %d"%(i+1) if sx>0 else ""))
            # Panel grid lines on raft
            for j in range(4):
                v,f=_box(sx*scs(28),deck_y+scs(0.36),zc-scs(3.0)+j*scs(2.0),scs(4.0),scs(0.02),scs(0.08))
                raft.append(_static(v,f,_mix(C_RAFT,(255,255,255),0.1),""))
    parts.append(Part("rafts","FLOATING SOLAR RAFTS (stowed)",raft,
        ["6 deployable floating solar raft modules",
         "2.0 MW additional PV when deployed at anchor",
         "MAT: HDPE float frames, bifacial PV panels",
         "TECH: auto-deploy/recover, mooring system"],24,(1.0,0.2,0.0),C_RAFT))
    # Communication antenna array (on bridge top)
    ant=[]
    # Main radar mast
    v,f=_solid_cylinder(scs(0.08),0,scs(8.0),seg=8); v=remap_yz(v)
    am2=_static(v,f,C_ANT,"radar mast"); am2.pivot=np.array([scs(30),deck_y+hh+scs(1.0),scs(85)])
    ant.append(am2)
    # Radar dish
    v,f=_solid_cylinder(scs(1.5),0,scs(0.15),seg=20)
    rd=Mesh(v,f,_mix(C_ANT,(100,100,110),0.3),name="radar dish",group="static")
    rd.pivot=np.array([scs(30),deck_y+hh+scs(8.0),scs(85)]); rd.tilt=(math.pi/2,0)
    ant.append(rd)
    # Communication whip antennas (3)
    for i in range(3):
        xc=scs(28)+i*scs(1.5)
        v,f=_solid_cylinder(scs(0.04),0,scs(5.0),seg=6); v=remap_yz(v)
        wa=_static(v,f,C_ANT,"whip antenna %d"%(i+1)); wa.pivot=np.array([xc,deck_y+hh+scs(0.5),scs(83)])
        ant.append(wa)
    # Satellite dome
    v,f=_solid_cylinder(scs(0.6),0,scs(0.5),seg=16)
    sd=Mesh(v,f,_mix(C_ANT,(80,80,90),0.4),name="satcom dome",group="static")
    sd.pivot=np.array([scs(32),deck_y+hh+scs(0.3),scs(87)]); sd.tilt=(0,0)
    ant.append(sd)
    # Nav lights (port red, starboard green)
    for sx,col in ((-1,(255,40,40)),(1,(40,255,40))):
        v,f=_solid_cylinder(scs(0.12),0,scs(0.15),seg=8)
        nl=Mesh(v,f,col,name="nav light",group="static")
        nl.pivot=np.array([sx*scs(35),deck_y+hh+scs(6.0),scs(85)]); nl.tilt=(0,0)
        ant.append(nl)
    parts.append(Part("antenna","COMMUNICATION + NAV ARRAY",ant,
        ["radar + satcom + VHF/UHF whip antennas",
         "port/starboard nav lights, AIS transponder",
         "MAT: 316L stainless mast, fiberglass radome",
         "TECH: Iridium satcom, X-band radar, AIS Class A"],25,(0,1.8,0.6),C_ANT))
    # Air lubrication system (bubbles along hull undersides)
    airlube=[]
    for hi in range(nh):
        xc=-beam/2+hi*hull_spacing
        # Compressor unit on deck
        if hi==0:
            v,f=_box(xc,deck_y+scs(0.3),-scs(50),scs(2.0),scs(1.0),scs(2.0))
            airlube.append(_static(v,f,_mix(C_AIRLUBE,(0,0,0),0.3),"air lube compressor"))
        # Bubble strip along hull bottom
        v,f=_box(xc,yk-scs(0.5),0.0,scs(0.15),scs(0.08),hull_len*0.80)
        airlube.append(_static(v,f,C_AIRLUBE,"air lube strip" if hi==0 else ""))
        # Bubble holes (small dots along strip)
        for zi in range(10):
            zc=-hull_len*0.38+(zi+0.5)*(hull_len*0.76/10)
            v,f=_solid_cylinder(scs(0.06),0,scs(0.04),seg=6)
            bh=Mesh(v,f,_mix(C_AIRLUBE,(255,255,255),0.3),name="",group="static")
            bh.pivot=np.array([xc,yk-scs(0.55),zc]); bh.tilt=(math.pi/2,0)
            airlube.append(bh)
    parts.append(Part("airlube","AIR LUBRICATION SYSTEM",airlube,
        ["micro-bubble carpet reduces hull drag 15-20%%",
         "compressor + perforated strips on all 5 hulls",
         "MAT: 316L stainless strips, silicone tubing",
         "TECH: air layer drag reduction, active control"],26,(-1.0,-1.2,0.0),C_AIRLUBE))
    # IMTA seaweed cultivation rafts (between hulls, at waterline)
    imta=[]; C_IMTA=(60,160,80)
    for zi in range(4):
        zc=-scs(30)+(zi+0.5)*scs(20)
        # Seaweed line between outer hulls
        v,f=_box(0.0,-freebd-scs(0.5),zc,beam*0.85,scs(0.1),scs(0.5))
        imta.append(_static(v,f,C_IMTA,"seaweed line %d"%(zi+1)))
        # Seaweed fronds (small green tufts)
        for xi in range(6):
            xc=-beam*0.35+xi*(beam*0.14)
            v,f=_box(xc,-freebd-scs(0.8),zc,scs(0.3),scs(0.6),scs(0.3))
            imta.append(_static(v,f,_mix(C_IMTA,(0,0,0),0.2),""))
    parts.append(Part("imta","IMTA SEAWEED CULTIVATION",imta,
        ["integrated multi-trophic aquaculture between hulls",
         "4 seaweed (Kappaphycus) long-lines at waterline",
         "absorbs N/P from shrimp effluent, bio-remediation",
         "MAT: HDPE long-line ropes, seeded seaweed",
         "TECH: nutrient bio-extraction, 40 t/season"],27,(0,-0.8,0.3),C_IMTA))
    return parts

def build_hatchery_parts():
    parts=[]
    brood=[]; nbt=8; bt_d=_hatch(DIMS["broodstock_tank_d_m"]/2); bt_h=_hatch(DIMS["broodstock_tank_h_m"])
    for i in range(nbt):
        xc=-_hatch(30)+(i%4)*_hatch(20); zc=-_hatch(15)+(i//4)*_hatch(20)
        v,f=_solid_cylinder(bt_d,0,bt_h,seg=20)
        brood+=_place_spinner([Mesh(v,f,C_BROODSTOCK,name="broodstock tank %d"%(i+1),group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
        v,f=_annulus_cylinder(bt_d*0.95,bt_d*0.3,bt_h-_hatch(0.1),bt_h,seg=16)
        brood+=_place_spinner([Mesh(v,f,_mix(C_BROODSTOCK,C_H2O,0.4),name="water",group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
    parts.append(Part("brood_detail","BROODSTOCK MATURATION",brood,
        ["%d RAS tanks, %d females total"%(DIMS["broodstock_tanks"],DIMS["broodstock_females"]),
         "P. monodon, selectively bred lines",
         "%.0fK eggs/female/spawn x %d/year"%(SHRIMP["eggs_per_spawn"]/1000,SHRIMP["spawns_per_year"]),
         "LED photoperiod, eyestalk ablation, AI monitoring",
         "MAT: fiberglass RAS tanks, HDPE piping, titanium heat exchangers",
         "TECH: Recirculating Aquaculture System, biofloc + ozone"],0,(0,0.5,0),C_BROODSTOCK))
    larval=[]; nlt=8; lt_d=_hatch(DIMS["larval_tank_d_m"]/2); lt_h=_hatch(DIMS["larval_tank_h_m"])
    for i in range(nlt):
        xc=_hatch(10)+(i%4)*_hatch(15); zc=-_hatch(15)+(i//4)*_hatch(20)
        v,f=_solid_cylinder(lt_d,0,lt_h,seg=18)
        larval+=_place_spinner([Mesh(v,f,C_LARVAL,name="larval tank %d"%(i+1),group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
        v,f=_annulus_cylinder(lt_d*0.95,lt_d*0.3,lt_h-_hatch(0.08),lt_h,seg=14)
        larval+=_place_spinner([Mesh(v,f,_mix(C_LARVAL,C_H2O,0.5),name="larval water",group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
    parts.append(Part("larval_detail","LARVAL REARING",larval,
        ["%d tanks: nauplii -> PL20 (20 days)"%DIMS["larval_tanks"],
         "egg->nauplii %.0f%%, nauplii->PL20 %.0f%%"%(SHRIMP["egg_to_nauplii"]*100,SHRIMP["nauplii_to_pl20"]*100),
         "Artemia + formulated microdiet","pure O2 injection, biofloc + ozone",
         "MAT: fiberglass tanks, HDPE piping, pure O2 diffusers",
         "TECH: staggered continuous batches, 52 cycles/year"],
        1,(0.8,0.5,0),C_LARVAL))
    nursery=[]; nnp=6; np_d=_hatch(DIMS["nursery_pool_d_m"]/2); np_h=_hatch(DIMS["nursery_pool_h_m"])
    for i in range(nnp):
        xc=-_hatch(20)+(i%3)*_hatch(20); zc=_hatch(15)+(i//3)*_hatch(20)
        v,f=_solid_cylinder(np_d,0,np_h,seg=22)
        nursery+=_place_spinner([Mesh(v,f,C_NURSERY,name="nursery pool %d"%(i+1),group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
        v,f=_annulus_cylinder(np_d*0.95,np_d*0.3,np_h-_hatch(0.08),np_h,seg=18)
        nursery+=_place_spinner([Mesh(v,f,_mix(C_NURSERY,C_BIOFLOC,0.3),name="biofloc water",group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
    parts.append(Part("nursery_detail","NURSERY GROW-OUT",nursery,
        ["%d pools: PL20 -> 5-10g juvenile"%DIMS["nursery_pools"],
         "survival %.0f%%, 90-120 days nursery"%(SHRIMP["pl20_to_juvenile"]*100),
         "super-intensive biofloc/RAS","~3-4 cycles/year per tank volume",
         "MAT: fiberglass pools, HDPE piping, titanium heat exchangers",
         "TECH: flow-through + recirculation, AI density control"],
        2,(0,0.8,0.5),C_NURSERY))
    release=[]; nrc=DIMS["release_chutes"]; rc_d=_hatch(DIMS["release_chute_d_m"]/2)
    rc_l=_hatch(DIMS["release_chute_len_m"])
    for i in range(nrc):
        xc=-_hatch(25)+(i+0.5)*_hatch(50/nrc)
        v,f=_solid_cylinder(rc_d,0,rc_l,seg=14)
        release+=_place_spinner([Mesh(v,f,C_RELEASE,name="release chute %d"%(i+1),group="release")],
            (xc,_hatch(5),_hatch(30)),(math.pi/2,0),"release")
    parts.append(Part("release_detail","RELEASE SYSTEM",release,
        ["%d release chutes on submerged hulls"%DIMS["release_chutes"],
         "timed mass release into nursery grounds","weekly schedule, GPS + current modeling",
         "DNA barcoded -- every batch tracked",
         "MAT: 316L stainless chutes, hydraulic actuated gates",
         "TECH: GPS-guided timed release, CRISPR-Cas9 DNA barcoding"],3,(0,1.0,0.3),C_RELEASE))
    feed=[]; nft=6; ft_d=_hatch(DIMS["feed_tank_d_m"]/2); ft_h=_hatch(DIMS["feed_tank_h_m"])
    for i in range(nft):
        xc=_hatch(20)+(i%3)*_hatch(12); zc=_hatch(20)+(i//3)*_hatch(15)
        v,f=_solid_cylinder(ft_d,0,ft_h,seg=16)
        feed+=_place_spinner([Mesh(v,f,C_FEED,name="feed tank %d"%(i+1),group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
    parts.append(Part("feed_detail","FEED PRODUCTION",feed,
        ["%d tanks: biofloc + Artemia + formulated diet"%DIMS["feed_tanks"],
         "70%% produced onboard, 30%% from shore","FCR %.1f, $%.1f/kg"%(SHRIMP["fcr"],SHRIMP["feed_cost_kg"]),
         "MAT: fiberglass tanks, HDPE piping, titanium heat exchangers",
         "TECH: biofloc fermentation + Artemia culture + extruded diet"],
        4,(0.5,0.3,0.8),C_FEED))
    lab=[]; ll=_hatch(12.0); lw=_hatch(10.0); lh=_hatch(DIMS["dna_lab_h_m"])
    v,f=_box(0.0,lh/2,_hatch(35),lw,lh,ll); lab.append(_static(v,f,C_DNA_LAB,"DNA barcoding lab"))
    parts.append(Part("dna_detail","DNA BARCODING LAB",lab,
        ["CRISPR-Cas9 inserted neutral marker","every batch barcoded for recapture tracking",
         "%.0f m2 lab, legal ownership of tagged biomass"%DIMS["dna_lab_m2"],
         "MAT: cleanroom modular lab, Class 10K ISO 7",
         "TECH: CRISPR-Cas9 gene editing, PCR barcoding, AI batch tracking"],
        5,(0.3,0.5,1.0),C_DNA_LAB))
    # ---- microalgae photobioreactor farm (FREE shrimp feed via photosynthesis) ----
    algae=[]; nap=8; ap_d=_hatch(DIMS["algae_pond_d_m"]/2); ap_h=_hatch(DIMS["algae_pond_h_m"])
    for i in range(nap):
        xc=-_hatch(35)+(i%4)*_hatch(22); zc=-_hatch(25)+(i//4)*_hatch(20)
        # pond base (shallow circular pond)
        v,f=_solid_cylinder(ap_d,0,ap_h,seg=24)
        algae+=_place_spinner([Mesh(v,f,C_ALGAE_POND,name="algae pond %d"%(i+1),group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
        # water surface (green tinted = algae culture)
        v,f=_annulus_cylinder(ap_d*0.98,ap_d*0.1,ap_h-_hatch(0.05),ap_h,seg=20)
        algae+=_place_spinner([Mesh(v,f,C_ALGAE_WATER,name="algae culture",group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
    # photobioreactor tubes (vertical cylinders)
    npbr=6; pbr_d=_hatch(DIMS["algae_pbr_d_m"]/2); pbr_h=_hatch(DIMS["algae_pbr_h_m"])
    for i in range(npbr):
        xc=_hatch(30)+(i%3)*_hatch(10); zc=_hatch(25)+(i//3)*_hatch(12)
        v,f=_solid_cylinder(pbr_d,0,pbr_h,seg=16)
        algae+=_place_spinner([Mesh(v,f,C_ALGAE_PBR,name="photobioreactor %d"%(i+1),group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
        # LED ring at top
        v,f=_annulus_cylinder(pbr_d*1.1,pbr_d*0.9,pbr_h-_hatch(0.2),pbr_h,seg=12)
        algae+=_place_spinner([Mesh(v,f,(200,100,100),name="LED ring",group="static")],
            (xc,0,zc),(math.pi/2,0),"static")
    parts.append(Part("algae_farm","MICROALGAE PHOTOBIOREACTOR FARM",algae,
        ["FREE SHRIMP FEED via photosynthesis: sun + CO2 + seawater -> algae",
         "Species: %s + %s + %s"%(ALGAE_FARM["species_primary"],ALGAE_FARM["species_secondary"],ALGAE_FARM["species_tertiary"]),
         "%d open ponds (%.0f m dia) + %d photobioreactors (%.0f m dia x %.0f m)"%(
             DIMS["algae_ponds"],DIMS["algae_pond_d_m"],DIMS["algae_photobioreactors"],
             DIMS["algae_pbr_d_m"],DIMS["algae_pbr_h_m"]),
         "Total area: %.0f m2, greenhouse: %.0f m2"%(DIMS["algae_pond_area_m2"],DIMS["algae_greenhouse_m2"]),
         "Growth rate: %.0f g/m2/day, harvest every %.0f days"%(
             ALGAE_FARM["growth_rate_g_m2_day"],ALGAE_FARM["harvest_interval_days"]),
         "Protein: %.0f%%, Lipid: %.0f%%, Carb: %.0f%%, Pigment: %.0f%%"%(
             ALGAE_FARM["protein_content_pct"],ALGAE_FARM["lipid_content_pct"],
             ALGAE_FARM["carb_content_pct"],ALGAE_FARM["pigment_content_pct"]),
         "Replaces %.0f%% of commercial feed. FCR improves %.1f -> %.1f"%(
             ALGAE_FARM["feed_replacement_frac"]*100,SHRIMP["fcr"],ALGAE_FARM["fcr_with_algae"]),
         "Annual production: %.0f t/vessel, Fleet: %.0f t/yr"%(
             algae_production_t_per_year(),fleet_algae_production_t_per_year()),
         "CO2 captured: %.0f t/yr, O2 produced: %.0f t/yr (per vessel)"%(
             algae_co2_captured_t_per_year(),algae_o2_produced_t_per_year()),
         "Feed cost: $0.00/kg (FREE, like fuel). Savings: $%.0fM/yr/vessel"%(
             algae_feed_savings_usd_per_year()/1e6),
         "LED night supplement: 660nm red + 450nm blue, %d kW"%ALGAE_FARM["led_supplement_kw"],
         "Nutrients: hatchery wastewater + seawater minerals (closed loop)",
         "MAT: fiberglass ponds with HDPE liner, glass PBR tubes, LED arrays",
         "TECH: photosynthesis, AI hyperspectral monitoring, centrifuge harvest, spray dryer"],
        6,(0.2,0.8,0.3),C_ALGAE))
    return parts

# SECTION 5 -- MARINE PHYSICS / ENERGY + SHRIMP PRODUCTION BIOLOGY

def sun_factor(hour_of_day):
    x=(hour_of_day-6.0)/12.0
    if x<=0.0 or x>=1.0: return 0.0
    return math.sin(x*math.pi)

def solar_kw(sun): return SOLAR_PEAK_KW*clamp(sun)
def sea_drag_mult(sea_state): return 1.0+SEA_STATE_DRAG*clamp(sea_state)
def hull_coat_factor(sea_state=0.0,superhydrophobic=False):
    base=1.0-(HULL_COAT["dry_frac"]+HULL_COAT["sea_frac"]*clamp(sea_state))
    if superhydrophobic:
        base*=1.0-SUPERHYDROPHOBIC["drag_reduction_frac"]
    return base
def drift_speed_kn(wind_ms=AMBIENT_WIND_MS,current_kn=DRIFT["current_drift_kn"]):
    sail_kn=0.0
    if wind_ms>=DRIFT["min_wind_ms"]:
        sail_kn=DRIFT["sail_drift_kn"]*clamp(wind_ms/8.0,0.0,1.5)
    return min(DRIFT["max_speed_kn"],current_kn+sail_kn)
def drift_drag_mult():
    return SUPERHYDROPHOBIC["drift_drag_mult"]
def trawl_catch_kg(dt_h,trawl_deployed):
    if not trawl_deployed: return 0.0
    return HARVEST["catch_rate_kg_per_hr"]*dt_h
def trawl_power_kw(trawl_deployed):
    return HARVEST["trawl_power_kw"] if trawl_deployed else 0.0
def tunnel_drag_factor(v_kn):
    cut=TUNNEL["base"]+TUNNEL["speed_gain"]*clamp(v_kn/TUNNEL["ref_kn"]); return 1.0-cut
def propulsion_kw(v_kn,sea_state=0.0,superhydrophobic=False):
    calm=PROP_COEF_KW*max(0.0,v_kn)**3
    drag=hull_coat_factor(sea_state,superhydrophobic)*tunnel_drag_factor(v_kn)
    return calm*sea_drag_mult(sea_state)*drag/PROP_TRAIN_EFF
def sustainable_speed_kn(prop_kw,sea_state=0.0,v_guess=9.0,superhydrophobic=False):
    if prop_kw<=0.0: return 0.0
    v=max(0.5,v_guess)
    for _ in range(6):
        denom=PROP_COEF_KW*sea_drag_mult(sea_state)*hull_coat_factor(sea_state,superhydrophobic)*tunnel_drag_factor(v)/PROP_TRAIN_EFF
        if denom<=1e-9: return 0.0
        v=(prop_kw/denom)**(1.0/3.0)
    return v
def heave_fin_kw(sea_state,v_kn,wind_ms=AMBIENT_WIND_MS):
    area=DIMS["heave_fins"]*DIMS["heave_fin_area_m2"]
    stroke_m=DIMS["heave_fin_span_m"]*clamp(sea_state/HEAVE_SEA_REF,0.0,1.0)
    force_n=1025.0*9.81*(DIMS["heave_fin_area_m2"]*0.25)*clamp(sea_state)
    work_per_fin_w=force_n*stroke_m/HEAVE_FIN["heave_period_s"]*2.0
    wave_kw=DIMS["heave_fins"]*work_per_fin_w*HEAVE_FIN["gen_eff"]/1000.0
    true_wind=max(0.0,wind_ms-v_kn*KN_TO_MS*0.4)
    sail_kw=(0.5*1.225*HEAVE_FIN["wind_cd"]*area*true_wind**3*HEAVE_FIN["wind_eff"]/1000.0)*0.02
    return wave_kw+sail_kw
def rotor_ship_kw(v_kn,wind_ms=AMBIENT_WIND_MS):
    n=DIMS["rotors"]; swept_m2=DIMS["rotor_d_m"]*DIMS["rotor_h_m"]
    true_wind=max(0.0,wind_ms+v_kn*KN_TO_MS*0.15)
    p_w=n*0.5*1.225*swept_m2*true_wind**3*ROTOR_SHIP["cp"]*ROTOR_SHIP["gen_eff"]
    return p_w/1000.0
def fabric_sail_drive_kw(v_kn,wind_ms=AMBIENT_WIND_MS):
    true_wind=max(0.0,wind_ms*FABRIC_SAIL["heading_gain"]+v_kn*KN_TO_MS*0.10)
    if true_wind<FABRIC_SAIL["deploy_ms"] or true_wind>FABRIC_SAIL["furl_ms"]: return 0.0
    n=DIMS["sail_masts"]; area=n*DIMS["sail_area_m2"]
    p_w=0.5*1.225*area*true_wind**3*FABRIC_SAIL["cd"]*FABRIC_SAIL["trim_eff"]
    return p_w/1000.0
def hanging_weight_kw(sea_state,v_kn):
    stroke=DIMS["weight_drop_m"]*clamp(sea_state/WEIGHT_HARVEST["sea_ref"],0.0,1.0)
    swing=DIMS["weight_swing_span_m"]*clamp(sea_state+0.15*v_kn/12.0,0.0,1.0)
    bob_mass=0.52*(1025.0*math.pi*(DIMS["weight_bob_d_m"]*0.5)**3/6.0)
    pitch_term=1.0+WEIGHT_HARVEST["pitch_gain"]*clamp(v_kn/12.0)
    work_per_cycle_j=bob_mass*9.81*max(0.0,stroke+0.55*swing)*pitch_term
    power_w=DIMS["weight_harvesters"]*work_per_cycle_j/HEAVE_FIN["heave_period_s"]
    return power_w*WEIGHT_HARVEST["gen_eff"]/1000.0
def tunnel_turbine_kw(v_kn):
    flow_kw=0.5*1025.0*(DIMS["tunnel_w_m"]*DIMS["tunnel_h_m"])*(max(0.0,v_kn)*KN_TO_MS)**3/1000.0*0.0006
    return flow_kw*TUNNEL["turbine_eff"]
def solar_lens_kw(sun,block_temp_c):
    aperture_m2=math.pi*(DIMS["sunlens_aperture_m"]*0.5)**2
    fade=clamp((THERM["shutdown_c"]-block_temp_c)/(THERM["shutdown_c"]-SUN_LENS["defocus_temp_c"]))
    return aperture_m2*SOLAR_IRRADIANCE_W*DIMS["solar_eff"]*SUN_LENS["optical_eff"]*sun*fade/1000.0
def h2_made_kg(electric_kwh): return max(0.0,electric_kwh)/ELECTROLYSIS_KWH_KG
def h2_energy_elec_kwh(kg): return kg*H2_LHV_KWH_KG*H2_ENGINE_EFF
def diesel_fuel_tonnes(distance_nm,speed_kn):
    hours=distance_nm/max(1e-6,speed_kn)
    p_kw=PROP_COEF_KW*speed_kn**3/PROP_TRAIN_EFF+HOTEL_KW
    return p_kw*hours*VOYAGE["diesel_sfoc_g_kwh"]/1e6
def diesel_cost_usd(distance_nm,speed_kn): return diesel_fuel_tonnes(distance_nm,speed_kn)*VOYAGE["diesel_price_per_t"]

# --- SHRIMP PRODUCTION MATH ---
def shrimp_eggs_per_year():
    return SHRIMP["broodstock_females"]*SHRIMP["eggs_per_spawn"]*SHRIMP["spawns_per_year"]
def shrimp_nauplii_per_year():
    return shrimp_eggs_per_year()*SHRIMP["egg_to_nauplii"]
def shrimp_pl20_per_year():
    return shrimp_nauplii_per_year()*SHRIMP["nauplii_to_pl20"]
def shrimp_juveniles_per_year():
    return shrimp_pl20_per_year()*SHRIMP["pl20_to_juvenile"]
def shrimp_juveniles_per_vessel_per_year():
    return shrimp_juveniles_per_year()
def fleet_juveniles_per_year(n_vessels=12):
    return shrimp_juveniles_per_vessel_per_year()*n_vessels
def shrimp_biomass_tonnes_per_year():
    return shrimp_juveniles_per_year()*SHRIMP["juvenile_size_g"]/1e6
def shrimp_harvest_biomass_tonnes():
    """If juveniles grow to harvest size, total biomass."""
    return shrimp_juveniles_per_year()*SHRIMP["harvest_size_g"]/1e6
def shrimp_nursery_feed_tonnes_per_year():
    """Feed needed onboard to grow juveniles from egg to release size (7.5g).
    Shrimp are released at juvenile size and feed in the wild after that."""
    return shrimp_biomass_tonnes_per_year()*SHRIMP["fcr"]
def shrimp_feed_tonnes_per_year():
    """Total feed if all juveniles were grown to harvest size (for revenue calc)."""
    return shrimp_harvest_biomass_tonnes()*SHRIMP["fcr"]
def shrimp_revenue_per_year(price_per_kg=4.85):
    return shrimp_harvest_biomass_tonnes()*1000*price_per_kg

# --- Microalgae / phytoplankton photobioreactor farm (FREE feed via photosynthesis) ---
def algae_production_kg_per_day(sun=1.0):
    """Daily microalgae biomass production from ponds + photobioreactors.
    Photosynthesis: sun + CO2 + seawater nutrients -> algae biomass.
    Growth rate scales with sunlight (0 at night, peak at midday)."""
    area=DIMS["algae_pond_area_m2"]
    rate=ALGAE_FARM["growth_rate_g_m2_day"]  # g/m²/day at full sun
    pond_kg=area*rate*clamp(sun)/1000.0
    # Photobioreactors produce at higher density, 24/7 with LED supplement
    pbr_area=DIMS["algae_photobioreactors"]*math.pi*(DIMS["algae_pbr_d_m"]/2)**2
    pbr_rate=rate*3.0  # 3x density in closed PBRs
    pbr_kg=pbr_area*pbr_rate/1000.0*0.7  # 70% from LED at night
    return pond_kg+pbr_kg

def algae_production_t_per_year():
    """Annual microalgae production per vessel (average sun = 0.5)."""
    return algae_production_kg_per_day(0.5)*365.0/1000.0

def algae_feed_replacement_t_per_year():
    """How much commercial feed is replaced by algae (80% replacement)."""
    return algae_production_t_per_year()*ALGAE_FARM["feed_replacement_frac"]

def algae_co2_captured_t_per_year():
    """CO2 captured via photosynthesis (1.83 kg CO2 per kg algae biomass)."""
    return algae_production_t_per_year()*1.83

def algae_o2_produced_t_per_year():
    """Oxygen produced via photosynthesis (1.2 kg O2 per kg algae biomass)."""
    return algae_production_t_per_year()*1.2

def algae_feed_savings_usd_per_year():
    """Money saved by using free algae instead of commercial feed."""
    return algae_feed_replacement_t_per_year()*1000*ALGAE_FARM["diesel_feed_equivalent_usd_per_kg"]

def fleet_algae_production_t_per_year(n=12):
    return algae_production_t_per_year()*n

# SECTION 6 -- MARINE POWERTRAIN + HATCHERY SIMULATION

class MarinePowertrain:
    def __init__(self):
        self.batt_kwh=ELEC["batt_mwh"]*1000.0
        self.soc=ELEC["soc_start"]
        self.h2_kg=DIMS["h2_capacity_kg"]*0.5
        self.h2_max=float(DIMS["h2_capacity_kg"])
        self.fly_I=0.5*DIMS["flywheel_mass_kg"]*(DIMS["flywheel_d_m"]*0.5)**2
        self.fly_omega=0.0; self.fly_rpm=0.0
        self.ring_rpm=0.0; self.gen_rpm=0.0
        self.genset_on=False; self.block_temp_c=THERM["ambient_c"]
        self.speed_kn=0.0; self.throttle=0.0
        self.rudder_deg=0.0; self.heading_deg=0.0
        self.ballast_fore_t=0.0; self.trim_deg=0.0
        self.cargo_t=0.0
        self.solar_kwh=0.0; self.prop_kwh=0.0; self.harvest_kwh=0.0
        self.regen_boost_kwh=0.0; self.sail_kwh=0.0; self.solar_lens_kwh=0.0
        self.h2_made=0.0; self.h2_used=0.0
        self.engine_off_ticks=0; self.total_ticks=0
        self.mode="SOLAR CRUISE"; self.flow={}
        for k in ("solar","electro","genset","steam","prop","batt","heave","rotor",
                  "tunnel","weights","sunlens","sail","regenboost",
                  "otec","digester","kite","float_solar"):
            self.flow[k]=0.0
        # Hatchery state
        self.hatchery_cycle_day=0
        self.juveniles_produced=0.0
        self.juveniles_released=0.0
        self.feed_consumed_kg=0.0
        self.release_events=0
        # Vessel operational mode (DRIFT / HARVEST / TRANSIT / STORM)
        self.vessel_mode="DRIFT"
        self.prev_vessel_mode="DRIFT"
        self.transform_progress=1.0  # 1.0 = fully transformed, 0.0 = start
        self.trawl_deployed=False
        self.trawl_deploy_frac=0.0  # 0=retracted, 1=fully deployed
        self.drift_current_kn=DRIFT["current_drift_kn"]
        self.catch_kg=0.0
        self.catch_total_kg=0.0
        self.storm_ballast_frac=0.0  # 0=light, 1=fully ballasted down
        self.superhydrophobic_active=True
        self.sail_minimal_deployed=False
        self.sail_minimal_frac=0.0
        # Recapture and DNA barcoding
        self.recapture_frac=0.0
        self.dna_barcoded_batches=0
        self.recapture_value_usd=0.0
        # Catch processing
        self.catch_frozen_kg=0.0
        self.catch_packaged_kg=0.0
        self.catch_bycatch_kg=0.0
        self.catch_revenue_usd=0.0
        # Financial tracking
        self.fleet_vessels=1
        self.total_revenue_usd=0.0
        self.carbon_credit_usd=0.0
        self.tech_license_usd=0.0
        self.data_sales_usd=0.0
        # Free-fuel metrics
        self.free_fuel_savings_usd=0.0
        self.h2_round_trip_eff=0.0
        # Microalgae photobioreactor farm (FREE shrimp feed via photosynthesis)
        self.algae_produced_kg=0.0
        self.algae_harvested_kg=0.0
        self.algae_to_shrimp_kg=0.0
        self.algae_storage_kg=0.0
        self.algae_co2_captured_kg=0.0
        self.algae_o2_produced_kg=0.0
        self.algae_feed_replaced_kg=0.0
        self.algae_feed_savings_usd=0.0
        self.algae_led_on=False
        self.algae_growth_rate=0.0  # current g/m²/day
        # AI systems: self-driving, self-breeding, self-herding, self-maintaining
        # Self-driving
        self.ai_drive_active=True
        self.ai_drive_decisions=0
        self.ai_route_optimizations=0
        self.ai_collision_avoidances=0
        self.ai_auto_mode_switches=0
        self.ai_weather_reroutes=0
        self.ai_drive_confidence=1.0  # 0-1, how confident the AI is in current route
        self.ai_manual_override=False
        # Self-breeding
        self.ai_breed_active=True
        self.ai_breed_generations=0
        self.ai_breed_genetic_gain_pct=0.0
        self.ai_breed_diversity=0.50  # starts at 0.50, target >0.35
        self.ai_breed_inbreeding=0.0  # keep <0.125
        self.ai_breed_families_tracked=0
        self.ai_breed_traits_improved={"growth":0.0,"survival":0.0,"fcr":0.0}
        self.ai_breed_spawns_predicted=0
        self.ai_breed_egg_quality_score=1.0  # 0-1
        # Self-herding
        self.ai_herd_active=True
        self.ai_herd_schools_tracked=0
        self.ai_herd_recapture_predictions=0
        self.ai_herd_predator_alerts=0
        self.ai_herd_fleet_contracts=0
        self.ai_herd_tracking_accuracy=AI_SYSTEMS["self_herding"]["tracking_accuracy_pct"]
        self.ai_herd_drones_active=0
        self.ai_herd_edna_samples=0
        self.ai_herd_migration_patterns_learned=0
        # Self-maintaining
        self.ai_maint_active=True
        self.ai_maint_predictions=0
        self.ai_maint_repairs_scheduled=0
        self.ai_maint_repairs_completed=0
        self.ai_maint_auto_repairs=0
        self.ai_maint_anomalies_detected=0
        self.ai_maint_uptime_pct=100.0
        self.ai_maint_sensor_readings=0
        self.ai_maint_parts_3d_printed=0
        self.ai_maint_system_health={}  # subsystem -> health score 0-1
        # Orchestrator
        self.ai_orchestrator_active=True
        self.ai_total_decisions=0
        self.ai_model_updates=0
        self.ai_learning_cycles=0
        # === INNOVATION STATE ===
        # OTEC baseload power
        self.otec_kw=OTEC["rated_kw"]
        self.otec_kwh=0.0
        # Air lubrication
        self.air_lube_active=True
        # Kite sail
        self.kite_deployed=False
        self.kite_kw=0.0
        self.kite_kwh=0.0
        # IMTA seaweed
        self.imta_seaweed_kg=0.0
        self.imta_nitrogen_removed_kg=0.0
        self.imta_revenue_usd=0.0
        # BSF larvae
        self.bsf_larvae_kg=0.0
        self.bsf_feed_kg=0.0
        # Anaerobic digester
        self.digester_kw=DIGESTER["biogas_kw"]
        self.digester_kwh=0.0
        self.digester_biogas_m3=0.0
        # Yeast single-cell protein
        self.yeast_protein_kg=0.0
        self.yeast_feed_kg=0.0
        # Biofloc system (primary feed source)
        self.biofloc_active=BIOFLOC["enabled"]
        self.biofloc_feed_kg=0.0
        # Floating solar rafts
        self.floating_solar_deployed=False
        self.floating_solar_kw=0.0
        # AUV fleet
        self.auv_count=AUV_FLEET["count"]
        self.auv_deployed=0
        # Swarm intelligence
        self.swarm_coordination_active=SWARM_AI["enabled"]
        self.swarm_decisions=0
        # Continuous release
        self.continuous_release_active=CONTINUOUS_RELEASE["enabled"]
        self.continuous_release_count=0
        # Acoustic/pheromone recapture
        self.acoustic_conditioning_active=ACOUSTIC_RECAPTURE["enabled"]
        self.acoustic_recapture_boost=ACOUSTIC_RECAPTURE["recapture_boost_pct"]/100.0
        # Feed self-sufficiency tracking
        self.total_feed_self_sufficiency_pct=0.0  # algae + BSF + yeast
        self.total_feed_replaced_kg=0.0  # separate from algae_feed_replaced_kg
        # Partner fleet
        self.partner_vessels_active=0
        # Combined energy
        self.total_renewable_kw=0.0

    @property
    def h2_frac(self): return self.h2_kg/self.h2_max
    @property
    def engine_off_frac(self):
        return self.engine_off_ticks/max(1,self.total_ticks)
    @property
    def h2_selfsuff(self):
        total=self.h2_made+self.h2_used
        return self.h2_made/max(1e-6,total)
    @property
    def free_fuel(self):
        return self.h2_selfsuff>=0.99 and self.h2_made>0.1
    @property
    def free_feed(self):
        """True when algae+BSF+yeast covers >=100% of shrimp feed demand."""
        return self.total_feed_self_sufficiency_pct>=99.0
    @property
    def algae_feed_coverage(self):
        """Fraction of shrimp feed demand met by onboard algae production."""
        if self.total_ticks<2: return 0.0
        elapsed_h=self.total_ticks*1800.0/3600.0  # approx elapsed hours
        feed_needed_kg=shrimp_feed_tonnes_per_year()*1000/8760.0*elapsed_h
        return min(1.0,self.algae_feed_replaced_kg/max(1.0,feed_needed_kg))
    @property
    def ai_all_active(self):
        return self.ai_drive_active and self.ai_breed_active and self.ai_herd_active and self.ai_maint_active
    @property
    def ai_autonomy_level(self):
        if self.ai_manual_override: return "MANUAL OVERRIDE"
        if self.ai_all_active: return "FULLY AUTONOMOUS"
        active=sum([self.ai_drive_active,self.ai_breed_active,self.ai_herd_active,self.ai_maint_active])
        if active==0: return "MANUAL"
        return "PARTIAL (%d/4)"%active
    @property
    def ai_breed_improvement_summary(self):
        g=self.ai_breed_traits_improved
        return "Growth +%.0f%%, Survival +%.0f%%, FCR -%.0f%%"%(
            g["growth"]*100,g["survival"]*100,g["fcr"]*100)
    @property
    def ai_maint_avg_health(self):
        if not self.ai_maint_system_health: return 1.0
        return sum(self.ai_maint_system_health.values())/len(self.ai_maint_system_health)
    @property
    def diesel_saved_usd(self):
        dt_t,dt_c=_diesel_ref()
        return dt_c*(self.total_ticks/max(1,self.total_ticks))
    @property
    def fleet_valuation_usd(self):
        per_vessel=FINANCE["shrimp_revenue_per_vessel_year_usd"]+FINANCE["carbon_credit_per_vessel_year_usd"]+FINANCE["tech_license_per_vessel_year_usd"]+FINANCE["data_sales_per_vessel_year_usd"]
        years_elapsed=max(0.01,self.total_ticks*1800.0/8760.0)  # approx
        return per_vessel*self.fleet_vessels*years_elapsed*0.1  # 10% of revenue as valuation
    @property
    def roi_multiple(self):
        return self.fleet_valuation_usd/max(1.0,FINANCE["investment_usd"])

    def fly_kwh(self):
        return 0.5*self.fly_I*self.fly_omega**2/3.6e6

    def set_vessel_mode(self,mode):
        if mode not in VESSEL_MODES: return
        if mode==self.vessel_mode: return
        self.prev_vessel_mode=self.vessel_mode
        self.vessel_mode=mode
        self.transform_progress=0.0
        if mode=="HARVEST": self.trawl_deployed=True
        elif mode=="DRIFT":
            self.trawl_deployed=False; self.sail_minimal_deployed=True
        elif mode=="STORM":
            self.trawl_deployed=False; self.sail_minimal_deployed=False

    @property
    def is_drifting(self): return self.vessel_mode=="DRIFT"
    @property
    def is_harvesting(self): return self.vessel_mode=="HARVEST"
    @property
    def is_transiting(self): return self.vessel_mode=="TRANSIT"
    @property
    def is_storm(self): return self.vessel_mode=="STORM"
    @property
    def superhydrophobic_on(self): return self.superhydrophobic_active and self.vessel_mode in ("DRIFT","HARVEST","TRANSIT")

    def route_storage(self,kwh):
        if kwh>=0:
            charge=kwh*STORAGE["battery_rt"]
            room=(ELEC["soc_max"]-self.soc)*self.batt_kwh
            accepted=min(charge,room)
            self.soc+=accepted/self.batt_kwh
        else:
            draw=-kwh/STORAGE["battery_rt"]
            avail=(self.soc-ELEC["soc_min"])*self.batt_kwh
            drawn=min(draw,avail)
            self.soc-=drawn/self.batt_kwh

    def update_demo(self,dt):
        self.update(dt,sun=0.85,sea_state=0.25)

    def update(self,dt,sun,sea_state):
        self.total_ticks+=1
        dt_h=dt/3600.0
        # ---- vessel mode transformation progress ----
        if self.transform_progress<1.0:
            transform_rate=1.0/(HARVEST["trawl_deploy_time_min"]*60.0)
            self.transform_progress=min(1.0,self.transform_progress+dt*transform_rate)
        # ---- trawl deployment animation ----
        trawl_target=1.0 if self.trawl_deployed else 0.0
        self.trawl_deploy_frac+=(trawl_target-self.trawl_deploy_frac)*min(1.0,dt/30.0)
        # ---- minimal sail deployment ----
        sail_min_target=1.0 if self.sail_minimal_deployed else 0.0
        self.sail_minimal_frac+=(sail_min_target-self.sail_minimal_frac)*min(1.0,dt/15.0)
        # ---- storm ballast ----
        storm_target=1.0 if self.is_storm else 0.0
        self.storm_ballast_frac+=(storm_target-self.storm_ballast_frac)*min(1.0,dt/(STORM_MODE["ballast_time_min"]*60.0))
        # ---- drift mode: superhydrophobic hull, minimal sail, current drift ----
        if self.is_drifting:
            v_drift=drift_speed_kn(AMBIENT_WIND_MS,self.drift_current_kn)
            self.speed_kn+=(v_drift-self.speed_kn)*min(1.0,dt/60.0)
            sol_kw=solar_kw(sun)
            # OTEC + digester + floating solar (innovations)
            otec_kw=self.otec_kw if OTEC["enabled"] else 0.0
            digester_kw_=self.digester_kw if DIGESTER["enabled"] else 0.0
            self.kite_deployed=False; kite_kw_=0.0
            if FLOATING_SOLAR["enabled"]:
                self.floating_solar_deployed=True
                sol_kw+=FLOATING_SOLAR["additional_peak_kw"]*sun
            else:
                self.floating_solar_deployed=False
            heave_kw=heave_fin_kw(sea_state,self.speed_kn)
            windmill_kw_=rotor_ship_kw(self.speed_kn)
            weight_kw=hanging_weight_kw(sea_state,self.speed_kn)
            tunnel_kw=tunnel_turbine_kw(self.speed_kn)
            lens_kw=solar_lens_kw(sun,self.block_temp_c)
            harvest_kw=heave_kw+windmill_kw_+weight_kw+tunnel_kw
            regen_boost_kw=harvest_kw*REGEN_BOOST["direct_frac"]*REGEN_BOOST["pod_boost_eff"]
            harvest_to_batt_kw=harvest_kw*(1.0-REGEN_BOOST["direct_frac"])
            # drift power draw is minimal (hatchery + hotel only)
            prop_kw=DRIFT["power_draw_kw"]
            sail_kw=0.0  # minimal sail is direct thrust, not electric
            # genset rarely needed in drift
            if self.soc<GENSET_CRIT_SOC:
                self.genset_on=True
            elif self.soc>GENSET_OFF_SOC:
                self.genset_on=False
            genset_elec_kw=0.0; fuel_thermal_kw=0.0; waste_kw=0.0; steam_kw=0.0
            if self.genset_on:
                load_kw=max(GENSET_MIN_KW,min(GENSET_RATED_KW,(ELEC["soc_max"]-self.soc)*self.batt_kwh*0.5))
                fuel_thermal_kw=load_kw/(H2_ENGINE_EFF*0.95)
                genset_elec_kw=load_kw*0.95; waste_kw=fuel_thermal_kw-genset_elec_kw
                steam_kw=waste_kw*STEAM_RECOVER_FRAC+lens_kw
                genset_total_kw=genset_elec_kw+steam_kw
                h2_burn=fuel_thermal_kw*dt_h/H2_LHV_KWH_KG
                self.h2_kg=max(0.0,self.h2_kg-h2_burn); self.h2_used+=h2_burn
                self.block_temp_c=max(THERM["ambient_c"],self.block_temp_c+(waste_kw*(1.0-THERM["heat_trap_frac"]*0.0)-(self.block_temp_c-THERM["ambient_c"])*0.9)*dt/max(1e-6,THERM["block_mass_kj_c"]))
            else:
                genset_total_kw=0.0
                self.block_temp_c+=(THERM["ambient_c"]-self.block_temp_c)*min(1.0,dt/120.0)
            if not self.genset_on: self.engine_off_ticks+=1
            # electrolysis from surplus
            spare=sol_kw+harvest_to_batt_kw-prop_kw
            electro_kw=0.0
            if self.soc>=ELECTRO_SOC_FLOOR and self.h2_frac<0.999 and spare>0.0:
                taper=SYNERGY["electro_taper"]*(0.5+0.5*self.h2_frac)
                electro_kw=clamp(spare,0.0,ELECTROLYSER_MAX_KW)*(1.0-taper)
                made=h2_made_kg(electro_kw*dt_h)
                self.h2_kg=min(self.h2_max,self.h2_kg+made); self.h2_made+=made
            net_kw=sol_kw+genset_total_kw+harvest_to_batt_kw-prop_kw-electro_kw
            self.route_storage(net_kw*dt_h)
            self.harvest_kwh+=harvest_kw*dt_h; self.regen_boost_kwh+=regen_boost_kw*dt_h
            self.solar_kwh+=sol_kw*dt_h; self.prop_kwh+=prop_kw*dt_h
            self.solar_lens_kwh+=lens_kw*dt_h
            self.flow={"solar":sol_kw,"electro":electro_kw,"genset":genset_elec_kw,
                       "steam":steam_kw,"prop":prop_kw,"batt":net_kw,
                       "heave":heave_kw,"rotor":windmill_kw_,"tunnel":tunnel_kw,
                       "weights":weight_kw,"sunlens":lens_kw,"sail":0.0,
                       "regenboost":regen_boost_kw,
                       "otec":otec_kw,"digester":digester_kw_,"kite":kite_kw_,
                       "float_solar":FLOATING_SOLAR["additional_peak_kw"]*sun if self.floating_solar_deployed else 0.0}
            if self.genset_on: self.mode="DRIFT + ENGINE CHARGE"
            elif electro_kw>50: self.mode="DRIFT + H2 MAKE"
            elif sun<0.01: self.mode="DRIFT (NIGHT)"
            else: self.mode="DRIFT (FREE)"
            # hatchery runs in drift mode
            self._update_hatchery(dt_h,sun)
            self._update_ai(dt_h,dt,sun,sea_state)
            self._update_animation(dt,genset_total_kw)
            return
        # ---- harvest mode: trawl deployed, active propulsion ----
        if self.is_harvesting:
            sol_kw=solar_kw(sun)
            # OTEC + digester (innovations)
            otec_kw=self.otec_kw if OTEC["enabled"] else 0.0
            digester_kw_=self.digester_kw if DIGESTER["enabled"] else 0.0
            self.kite_deployed=False; kite_kw_=0.0
            self.floating_solar_deployed=False
            heave_kw=heave_fin_kw(sea_state,self.speed_kn)
            windmill_kw_=rotor_ship_kw(self.speed_kn)
            weight_kw=hanging_weight_kw(sea_state,self.speed_kn)
            tunnel_kw=tunnel_turbine_kw(self.speed_kn)
            lens_kw=solar_lens_kw(sun,self.block_temp_c)
            harvest_kw=heave_kw+windmill_kw_+weight_kw+tunnel_kw
            harvest_to_batt_kw=harvest_kw*(1.0-REGEN_BOOST["direct_frac"])
            regen_boost_kw=harvest_kw*REGEN_BOOST["direct_frac"]*REGEN_BOOST["pod_boost_eff"]
            # trawl speed
            v_target=HARVEST["trawl_speed_kn"]
            self.speed_kn+=(v_target-self.speed_kn)*min(1.0,dt/40.0)
            trawl_kw=trawl_power_kw(self.trawl_deploy_frac>0.5)
            prop_kw=propulsion_kw(self.speed_kn,sea_state,self.superhydrophobic_on)+HOTEL_KW+trawl_kw
            # catch
            if self.trawl_deploy_frac>0.5:
                caught=trawl_catch_kg(dt_h,True)
                self.catch_kg+=caught; self.catch_total_kg+=caught
                # catch processing: freeze, package, sort bycatch
                bycatch=caught*CATCH_PROC["bycatch_discard_frac"]
                shrimp_caught=caught-bycatch
                self.catch_bycatch_kg+=bycatch
                frozen=min(shrimp_caught,CATCH_PROC["freeze_capacity_kg_per_hr"]*dt_h)
                self.catch_frozen_kg+=frozen
                packaged=min(frozen,CATCH_PROC["packaging_kg_per_hr"]*dt_h)
                self.catch_packaged_kg+=packaged
                self.catch_revenue_usd+=packaged*CATCH_PROC["shrimp_price_usd_per_kg"]
                # DNA barcode each batch
                self.dna_barcoded_batches+=1
                # recapture rate approaches target with more data
                target=RECAPTURE["target_frac"]
                self.recapture_frac+=(target-self.recapture_frac)*min(1.0,dt/3600.0)
                # recapture value: juveniles released × survival × recapture × harvest value
                if self.juveniles_released>0:
                    harvestable=self.juveniles_released*RECAPTURE["juvenile_to_harvest_survival"]*self.recapture_frac
                    self.recapture_value_usd=harvestable*(RECAPTURE["harvest_size_g"]/1000.0)*RECAPTURE["recapture_value_usd_per_kg"]
            # genset
            if self.soc<GENSET_ON_SOC or (self.soc<GENSET_OFF_SOC and self.genset_on):
                self.genset_on=True
            elif self.soc>GENSET_OFF_SOC:
                self.genset_on=False
            if self.genset_on and self.block_temp_c>=THERM["shutdown_c"]:
                self.genset_on=False
            genset_elec_kw=0.0; fuel_thermal_kw=0.0; waste_kw=0.0; steam_kw=0.0
            if self.genset_on:
                load_kw=max(GENSET_MIN_KW,min(GENSET_RATED_KW,(ELEC["soc_max"]-self.soc)*self.batt_kwh*0.5))
                fuel_thermal_kw=load_kw/(H2_ENGINE_EFF*0.95)
                genset_elec_kw=load_kw*0.95; waste_kw=fuel_thermal_kw-genset_elec_kw
                steam_kw=waste_kw*STEAM_RECOVER_FRAC+lens_kw
                genset_total_kw=genset_elec_kw+steam_kw
                h2_burn=fuel_thermal_kw*dt_h/H2_LHV_KWH_KG
                self.h2_kg=max(0.0,self.h2_kg-h2_burn); self.h2_used+=h2_burn
                self.block_temp_c=max(THERM["ambient_c"],self.block_temp_c+(waste_kw*(1.0-THERM["heat_trap_frac"]*0.0)-(self.block_temp_c-THERM["ambient_c"])*0.9)*dt/max(1e-6,THERM["block_mass_kj_c"]))
            else:
                genset_total_kw=0.0
                self.block_temp_c+=(THERM["ambient_c"]-self.block_temp_c)*min(1.0,dt/120.0)
            if not self.genset_on: self.engine_off_ticks+=1
            spare=sol_kw+harvest_to_batt_kw-prop_kw
            electro_kw=0.0
            if self.soc>=ELECTRO_SOC_FLOOR and self.h2_frac<0.999 and spare>0.0:
                taper=SYNERGY["electro_taper"]*(0.5+0.5*self.h2_frac)
                electro_kw=clamp(spare,0.0,ELECTROLYSER_MAX_KW)*(1.0-taper)
                made=h2_made_kg(electro_kw*dt_h)
                self.h2_kg=min(self.h2_max,self.h2_kg+made); self.h2_made+=made
            net_kw=sol_kw+genset_total_kw+harvest_to_batt_kw-prop_kw-electro_kw
            self.route_storage(net_kw*dt_h)
            self.harvest_kwh+=harvest_kw*dt_h; self.regen_boost_kwh+=regen_boost_kw*dt_h
            self.solar_kwh+=sol_kw*dt_h; self.prop_kwh+=prop_kw*dt_h
            self.solar_lens_kwh+=lens_kw*dt_h
            self.flow={"solar":sol_kw,"electro":electro_kw,"genset":genset_elec_kw,
                       "steam":steam_kw,"prop":prop_kw,"batt":net_kw,
                       "heave":heave_kw,"rotor":windmill_kw_,"tunnel":tunnel_kw,
                       "weights":weight_kw,"sunlens":lens_kw,"sail":0.0,
                       "regenboost":regen_boost_kw,
                       "otec":otec_kw,"digester":digester_kw_,"kite":kite_kw_,
                       "float_solar":0.0}
            if self.genset_on: self.mode="HARVEST + ENGINE"
            elif self.trawl_deploy_frac>0.5: self.mode="HARVEST (TRAWL)"
            else: self.mode="HARVEST (DEPLOY)"
            self._update_hatchery(dt_h,sun)
            self._update_ai(dt_h,dt,sun,sea_state)
            self._update_animation(dt,genset_total_kw)
            return
        # ---- storm mode: ballast down, survival ----
        if self.is_storm:
            self.speed_kn*=max(0.0,1.0-dt/120.0)  # slow to stop
            sol_kw=solar_kw(sun)*0.1  # mostly storm clouds
            heave_kw=heave_fin_kw(1.0,self.speed_kn)*2.0  # big seas = big harvest
            windmill_kw_=rotor_ship_kw(self.speed_kn)*0.5  # furl rotors partially
            weight_kw=hanging_weight_kw(1.0,self.speed_kn)*2.0
            tunnel_kw=tunnel_turbine_kw(self.speed_kn)
            harvest_kw=heave_kw+windmill_kw_+weight_kw+tunnel_kw
            harvest_to_batt_kw=harvest_kw*(1.0-REGEN_BOOST["direct_frac"])
            regen_boost_kw=harvest_kw*REGEN_BOOST["direct_frac"]*REGEN_BOOST["pod_boost_eff"]
            prop_kw=HOTEL_KW*0.5  # minimal hotel power
            sail_kw=0.0
            # genset only if critical
            if self.soc<GENSET_CRIT_SOC: self.genset_on=True
            elif self.soc>0.40: self.genset_on=False
            genset_elec_kw=0.0; steam_kw=0.0; genset_total_kw=0.0
            if self.genset_on:
                load_kw=GENSET_MIN_KW
                fuel_thermal_kw=load_kw/(H2_ENGINE_EFF*0.95)
                genset_elec_kw=load_kw*0.95; genset_total_kw=genset_elec_kw
                h2_burn=fuel_thermal_kw*dt_h/H2_LHV_KWH_KG
                self.h2_kg=max(0.0,self.h2_kg-h2_burn); self.h2_used+=h2_burn
            if not self.genset_on: self.engine_off_ticks+=1
            net_kw=sol_kw+genset_total_kw+harvest_to_batt_kw-prop_kw
            self.route_storage(net_kw*dt_h)
            self.harvest_kwh+=harvest_kw*dt_h
            self.solar_kwh+=sol_kw*dt_h; self.prop_kwh+=prop_kw*dt_h
            self.flow={"solar":sol_kw,"electro":0.0,"genset":genset_elec_kw,
                       "steam":steam_kw,"prop":prop_kw,"batt":net_kw,
                       "heave":heave_kw,"rotor":windmill_kw_,"tunnel":tunnel_kw,
                       "weights":weight_kw,"sunlens":0.0,"sail":0.0,
                       "regenboost":regen_boost_kw,
                       "otec":OTEC["rated_kw"] if OTEC["enabled"] else 0.0,
                       "digester":DIGESTER["biogas_kw"] if DIGESTER["enabled"] else 0.0,
                       "kite":0.0,"float_solar":0.0}
            self.mode="STORM SURVIVAL"
            self._update_hatchery(dt_h,sun*0.1)
            self._update_ai(dt_h,dt,sun*0.1,sea_state)
            self._update_animation(dt,genset_total_kw)
            return
        # ---- transit mode (original logic, enhanced with superhydrophobic) ----
        sol_kw=solar_kw(sun)
        is_night=sun<0.01
        # OTEC baseload (24/7) + digester baseload
        otec_kw=self.otec_kw if OTEC["enabled"] else 0.0
        digester_kw_=self.digester_kw if DIGESTER["enabled"] else 0.0
        self.kite_deployed=False; kite_kw_=0.0
        # Floating solar rafts in drift mode
        if FLOATING_SOLAR["enabled"] and self.vessel_mode=="DRIFT":
            self.floating_solar_deployed=True
            sol_kw+=FLOATING_SOLAR["additional_peak_kw"]*sun
        else:
            self.floating_solar_deployed=False
        heave_kw=heave_fin_kw(sea_state,self.speed_kn)
        windmill_kw_=rotor_ship_kw(self.speed_kn)
        weight_kw=hanging_weight_kw(sea_state,self.speed_kn)
        tunnel_kw=tunnel_turbine_kw(self.speed_kn)
        sail_kw=fabric_sail_drive_kw(self.speed_kn)
        lens_kw=solar_lens_kw(sun,self.block_temp_c)
        harvest_kw=heave_kw+windmill_kw_+weight_kw+tunnel_kw
        harvest_to_batt_kw=harvest_kw*(1.0-REGEN_BOOST["direct_frac"])
        regen_boost_kw=harvest_kw*REGEN_BOOST["direct_frac"]*REGEN_BOOST["pod_boost_eff"]
        # sustainable speed with superhydrophobic hull + air lubrication
        renew_kw=sol_kw+harvest_to_batt_kw+regen_boost_kw+sail_kw+otec_kw+digester_kw_+kite_kw_
        prop_budget=max(0.0,renew_kw-HOTEL_KW*0.3)
        v_free=sustainable_speed_kn(prop_budget,sea_state,v_guess=max(MIN_CRUISE_KN,self.speed_kn),superhydrophobic=self.superhydrophobic_on)
        v_free=max(MIN_CRUISE_KN,v_free)
        boost=self.soc>=SYNERGY["batt_boost_soc"] and not self.genset_on
        v_target=v_free
        if boost: v_target=min(MAX_CRUISE_KN,v_free+SYNERGY["flywheel_burst_kn"])
        if sail_kw>50: v_target=min(MAX_CRUISE_KN,v_target+SYNERGY["sail_bonus_max"]*clamp(sail_kw/SYNERGY["sail_bonus_kw"]))
        v_target=clamp(v_target,MIN_CRUISE_KN,MAX_CRUISE_KN)
        self.speed_kn+=(v_target-self.speed_kn)*min(1.0,dt/20.0)
        prop_kw=propulsion_kw(self.speed_kn,sea_state,self.superhydrophobic_on)+HOTEL_KW
        # genset
        if self.soc<GENSET_ON_SOC or (self.soc<GENSET_OFF_SOC and self.genset_on):
            self.genset_on=True
        elif self.soc>GENSET_OFF_SOC:
            self.genset_on=False
        if self.genset_on and self.block_temp_c>=THERM["shutdown_c"]:
            self.genset_on=False
        genset_elec_kw=0.0; fuel_thermal_kw=0.0; waste_kw=0.0; steam_kw=0.0
        if self.genset_on:
            load_kw=max(GENSET_MIN_KW,min(GENSET_RATED_KW,(ELEC["soc_max"]-self.soc)*self.batt_kwh*0.5))
            fuel_thermal_kw=load_kw/(H2_ENGINE_EFF*0.95)
            genset_elec_kw=load_kw*0.95
            waste_kw=fuel_thermal_kw-genset_elec_kw
            steam_kw=waste_kw*STEAM_RECOVER_FRAC+lens_kw
            genset_total_kw=genset_elec_kw+steam_kw
            h2_burn=fuel_thermal_kw*dt_h/H2_LHV_KWH_KG
            self.h2_kg=max(0.0,self.h2_kg-h2_burn); self.h2_used+=h2_burn
            heat_in=waste_kw*(1.0-THERM["heat_trap_frac"]*0.0)
            cool=(self.block_temp_c-THERM["ambient_c"])*0.9
            dT=(heat_in-cool)*dt/max(1e-6,THERM["block_mass_kj_c"])
            self.block_temp_c=max(THERM["ambient_c"],self.block_temp_c+dT)
        else:
            genset_total_kw=0.0
            self.block_temp_c+=(THERM["ambient_c"]-self.block_temp_c)*min(1.0,dt/120.0)
        if not self.genset_on: self.engine_off_ticks+=1
        # electrolysis from solar surplus
        spare=sol_kw+harvest_to_batt_kw-prop_kw
        electro_kw=0.0
        if self.soc>=ELECTRO_SOC_FLOOR and self.h2_frac<0.999 and spare>0.0:
            taper=SYNERGY["electro_taper"]*(0.5+0.5*self.h2_frac)
            electro_kw=clamp(spare,0.0,ELECTROLYSER_MAX_KW)*(1.0-taper)
            made=h2_made_kg(electro_kw*dt_h)
            self.h2_kg=min(self.h2_max,self.h2_kg+made); self.h2_made+=made
        net_kw=sol_kw+genset_total_kw+harvest_to_batt_kw-prop_kw-electro_kw
        self.route_storage(net_kw*dt_h)
        self.harvest_kwh+=harvest_kw*dt_h; self.regen_boost_kwh+=regen_boost_kw*dt_h
        self.sail_kwh+=sail_kw*dt_h; self.solar_lens_kwh+=lens_kw*dt_h
        self.fly_omega*=max(0.0,1.0-dt*0.00002)
        if net_kw>100.0 and self.fly_kwh()<80.0:
            spill=min(net_kw-100.0,200.0)*dt_h
            if spill>0.0:
                E=max(0.0,self.fly_kwh()+spill)*3.6e6
                self.fly_omega=min(math.sqrt(max(0.0,2*E/self.fly_I)),FLYWHEEL_MAX_RPM*2*math.pi/60.0)
        self.fly_rpm=self.fly_omega*60.0/(2*math.pi)
        # animation state
        tgt_ring=3000.0 if self.genset_on else (600.0 if genset_total_kw>5 else 0.0)
        self.ring_rpm+=(tgt_ring-self.ring_rpm)*min(1.0,dt/30.0)
        self.gen_rpm+=(tgt_ring*1.7-self.gen_rpm)*min(1.0,dt/30.0)
        # tallies
        self.solar_kwh+=sol_kw*dt_h; self.prop_kwh+=prop_kw*dt_h
        self.flow={"solar":sol_kw,"electro":electro_kw,"genset":genset_elec_kw,
                   "steam":steam_kw,"prop":prop_kw,"batt":net_kw,
                   "heave":heave_kw,"rotor":windmill_kw_,"tunnel":tunnel_kw,
                   "weights":weight_kw,"sunlens":lens_kw,"sail":sail_kw,
                   "regenboost":regen_boost_kw,
                   "otec":otec_kw,"digester":digester_kw_,"kite":kite_kw_,
                   "float_solar":self.floating_solar_kw}
        batt_boosting=(self.soc>=SYNERGY["batt_boost_soc"] and not self.genset_on and self.speed_kn>v_free*1.02)
        regen_active=regen_boost_kw>10.0; sail_active=sail_kw>20.0
        if self.genset_on and boost: self.mode="ENGINE CHARGE + BOOST"
        elif self.genset_on and regen_active and sail_active: self.mode="ENGINE CHARGE + RENEW"
        elif self.genset_on and sail_active: self.mode="ENGINE CHARGE + SAIL"
        elif self.genset_on: self.mode="ENGINE CHARGING"
        elif boost: self.mode="BOOST CRUISE"
        elif batt_boosting and regen_active and sail_active: self.mode="FULL SYNERGY"
        elif batt_boosting and regen_active: self.mode="REGEN + BATT BOOST"
        elif batt_boosting: self.mode="BATTERY BOOST"
        elif regen_active and sail_active: self.mode="REGEN + SAIL"
        elif regen_active and self.speed_kn>v_free*1.02: self.mode="REGEN BOOST"
        elif sail_active and self.speed_kn>v_free*1.02: self.mode="SAIL BOOST"
        elif is_night: self.mode="NIGHT BATTERY"
        elif electro_kw>50: self.mode="SOLAR + H2 MAKE"
        else: self.mode="SOLAR CRUISE"
        # ---- hatchery + animation + AI ----
        self._update_hatchery(dt_h,sun)
        self._update_ai(dt_h,dt,sun,sea_state)
        self._update_animation(dt,genset_total_kw)

    def _update_hatchery(self,dt_h,sun=0.5):
        """Hatchery simulation: juvenile production, feed, weekly release, algae farm, financial tracking."""
        self.hatchery_cycle_day+=dt_h/24.0
        juv_per_hour=shrimp_juveniles_per_vessel_per_year()/8760.0
        self.juveniles_produced+=juv_per_hour*dt_h
        feed_kg_per_hour=shrimp_nursery_feed_tonnes_per_year()*1000/8760.0
        self.feed_consumed_kg+=feed_kg_per_hour*dt_h
        # ---- microalgae photobioreactor farm (FREE feed via photosynthesis) ----
        # Sun + CO2 + seawater nutrients -> algae biomass -> shrimp feed
        sun_eff=clamp(sun,0.0,1.0)
        self.algae_led_on=sun_eff<0.15  # LED supplement at night
        # Production: ponds scale with sunlight, PBRs have LED backup
        pond_kg_per_h=algae_production_kg_per_day(sun_eff)/24.0
        self.algae_growth_rate=ALGAE_FARM["growth_rate_g_m2_day"]*sun_eff
        produced_kg=pond_kg_per_h*dt_h
        self.algae_produced_kg+=produced_kg
        # CO2 captured and O2 produced via photosynthesis
        self.algae_co2_captured_kg+=produced_kg*1.83
        self.algae_o2_produced_kg+=produced_kg*1.2
        # Harvest every 3 days (continuous small harvest each hour)
        harvest_kg=produced_kg*0.95  # 95% of production is harvested
        self.algae_harvested_kg+=harvest_kg
        # Feed to shrimp: algae provides 30% of total nursery feed (sized to demand)
        # Physical production tracked for CO2/O2, but feed contribution is proportional
        algae_feed_kg=feed_kg_per_hour*FEED_SELF_SUFFICIENCY["algae_pct"]/100.0*dt_h
        self.algae_to_shrimp_kg+=algae_feed_kg
        self.algae_feed_replaced_kg+=algae_feed_kg
        # Remaining production goes to storage (for future use or sale)
        self.algae_storage_kg=min(ALGAE_FARM["storage_capacity_t"]*1000,
                                  self.algae_storage_kg+harvest_kg-algae_feed_kg)
        # Feed cost savings: algae replaces commercial feed at $1.2/kg equivalent
        self.algae_feed_savings_usd=algae_feed_kg*ALGAE_FARM["diesel_feed_equivalent_usd_per_kg"]
        # free-fuel savings: diesel equivalent of H2 used
        diesel_equiv_kg=self.h2_used*H2_LHV_KWH_KG/(VOYAGE["diesel_sfoc_g_kwh"]*1e-3*H2_ENGINE_EFF)
        self.free_fuel_savings_usd=diesel_equiv_kg/1000.0*VOYAGE["diesel_price_per_t"]
        # H2 round-trip efficiency
        if self.h2_made>0.1 and self.h2_used>0.1:
            self.h2_round_trip_eff=FREE_FUEL["electrolyser_eff"]*FREE_FUEL["h2_engine_eff"]
        # financial revenue (continuous, all modes)
        year_frac=dt_h/8760.0
        self.total_revenue_usd+=FINANCE["shrimp_revenue_per_vessel_year_usd"]*year_frac*self.fleet_vessels
        self.carbon_credit_usd+=FINANCE["carbon_credit_per_vessel_year_usd"]*year_frac*self.fleet_vessels
        self.tech_license_usd+=FINANCE["tech_license_per_vessel_year_usd"]*year_frac*self.fleet_vessels
        self.data_sales_usd+=FINANCE["data_sales_per_vessel_year_usd"]*year_frac*self.fleet_vessels
        # ---- IMTA seaweed polyculture ----
        imta_kg_per_h=IMTA["production_t_per_year"]*1000/8760.0
        imta_kg=imta_kg_per_h*dt_h
        self.imta_seaweed_kg+=imta_kg
        self.imta_nitrogen_removed_kg+=imta_kg*0.015  # 1.5% N content
        self.imta_revenue_usd+=imta_kg*IMTA["revenue_usd_per_year"]/(IMTA["production_t_per_year"]*1000)
        # ---- BSF larvae (waste to protein, 15% of feed) ----
        bsf_kg=feed_kg_per_hour*FEED_SELF_SUFFICIENCY["bsf_pct"]/100.0*dt_h
        self.bsf_larvae_kg+=bsf_kg
        self.bsf_feed_kg+=bsf_kg
        # ---- Yeast single-cell protein (H2 + CO2 -> protein, 5% of feed) ----
        yeast_kg=feed_kg_per_hour*FEED_SELF_SUFFICIENCY["yeast_pct"]/100.0*dt_h
        self.yeast_protein_kg+=yeast_kg
        self.yeast_feed_kg+=yeast_kg
        # ---- Anaerobic digester (waste to biogas) ----
        self.digester_biogas_m3+=DIGESTER["biogas_m3_per_day"]*dt_h/24.0
        self.digester_kwh+=DIGESTER["biogas_kw"]*dt_h
        # ---- OTEC baseload power ----
        self.otec_kwh+=self.otec_kw*dt_h
        # ---- Kite sail propulsion ----
        if self.kite_deployed:
            self.kite_kw=KITE_SAIL["propulsion_kw_avg"]
            self.kite_kwh+=self.kite_kw*dt_h
        else:
            self.kite_kw=0.0
        # ---- Floating solar rafts (drift mode only) ----
        if self.floating_solar_deployed and self.vessel_mode=="DRIFT":
            self.floating_solar_kw=FLOATING_SOLAR["additional_peak_kw"]*sun_eff
        else:
            self.floating_solar_kw=0.0
        # ---- AUV fleet deployment ----
        self.auv_deployed=self.auv_count if (self.is_harvesting or self.vessel_mode=="DRIFT") else 0
        # ---- Swarm intelligence ----
        if self.swarm_coordination_active:
            self.swarm_decisions+=1
        # ---- Continuous release mode ----
        if self.continuous_release_active:
            release_per_h=CONTINUOUS_RELEASE["release_rate_per_hour"]
            self.continuous_release_count+=int(release_per_h*dt_h)
            self.juveniles_released+=release_per_h*dt_h
        # ---- Feed self-sufficiency calculation ----
        # Biofloc: 50% of feed replaced by bacterial protein from waste
        if self.biofloc_active:
            biofloc_kg=feed_kg_per_hour*BIOFLOC["replacement_pct"]/100.0*dt_h
            self.biofloc_feed_kg+=biofloc_kg
        self.total_feed_replaced_kg=(self.algae_feed_replaced_kg+self.bsf_feed_kg+
                                      self.yeast_feed_kg+self.biofloc_feed_kg)
        if self.feed_consumed_kg>0.1:
            self.total_feed_self_sufficiency_pct=min(100.0,100.0*self.total_feed_replaced_kg/self.feed_consumed_kg)
        # ---- Combined renewable energy ----
        self.total_renewable_kw=(self.flow.get("solar",0)+self.otec_kw+self.digester_kw+
                                  self.kite_kw+self.floating_solar_kw)
        # ---- Partner fleet activation ----
        if self.fleet_vessels>1:
            self.partner_vessels_active=int(PARTNER_FLEET["partner_vessels"]*self.fleet_vessels/12)
        if self.hatchery_cycle_day>=7.0 and not self.continuous_release_active:
            self.juveniles_released+=self.juveniles_produced
            self.juveniles_produced=0.0
            self.release_events+=1
            self.hatchery_cycle_day=0.0
        elif self.continuous_release_active:
            self.juveniles_produced=0.0  # continuous release, no batch
            if self.hatchery_cycle_day>=7.0:
                self.hatchery_cycle_day=0.0
                self.release_events+=1

    def _update_ai(self,dt_h,dt,sun,sea_state):
        """AI systems update: self-driving, self-breeding, self-herding, self-maintaining.
        The vessel is fully autonomous — AI operates all systems, crew supervises."""
        if not self.ai_orchestrator_active: return
        dt_s=dt  # simulation seconds
        # ===== SELF-DRIVING (autonomous navigation) =====
        if self.ai_drive_active and not self.ai_manual_override:
            self.ai_drive_decisions+=1
            # Route optimization: adjust speed based on conditions
            if sea_state>0.6 and self.vessel_mode=="TRANSIT":
                self.ai_weather_reroutes+=1
                self.ai_drive_confidence=max(0.6,self.ai_drive_confidence-dt_s*0.001)
            elif sea_state<0.3 and self.vessel_mode=="TRANSIT":
                self.ai_drive_confidence=min(1.0,self.ai_drive_confidence+dt_s*0.0005)
            # Collision avoidance: random encounters
            if self.total_ticks%50==0 and self.speed_kn>5:
                self.ai_collision_avoidances+=1
            # Auto mode selection: AI can suggest mode switches
            if self.total_ticks%200==0:
                if sea_state>0.8 and self.vessel_mode!="STORM":
                    self.ai_auto_mode_switches+=1
                elif sun>0.7 and self.vessel_mode=="TRANSIT" and self.soc>0.8:
                    self.ai_route_optimizations+=1
        # ===== SELF-BREEDING (genetic optimization) =====
        if self.ai_breed_active:
            # Each hatchery cycle (~7 days) = ~1 breeding decision
            cycle_frac=dt_h/(7.0*24.0)
            self.ai_breed_spawns_predicted+=int(cycle_frac*SHRIMP["broodstock_females"]*0.1)
            # Genetic gain accumulates over generations (4 gen/yr)
            gen_frac=cycle_frac*AI_SYSTEMS["self_breeding"]["generations_per_year"]
            self.ai_breed_genetic_gain_pct+=gen_frac*AI_SYSTEMS["self_breeding"]["genetic_gain_per_gen_pct"]
            # Trait improvements
            self.ai_breed_traits_improved["growth"]=min(0.25,self.ai_breed_traits_improved["growth"]+gen_frac*0.25)
            self.ai_breed_traits_improved["survival"]=min(0.18,self.ai_breed_traits_improved["survival"]+gen_frac*0.18)
            self.ai_breed_traits_improved["fcr"]=min(0.12,self.ai_breed_traits_improved["fcr"]+gen_frac*0.12)
            # Diversity slowly decreases as selection pressure increases, but AI manages it
            self.ai_breed_diversity=max(AI_SYSTEMS["self_breeding"]["diversity_target"],
                                        self.ai_breed_diversity-gen_frac*0.02)
            # Inbreeding increases slowly but AI keeps it below max
            self.ai_breed_inbreeding=min(AI_SYSTEMS["self_breeding"]["inbreeding_max"],
                                         self.ai_breed_inbreeding+gen_frac*0.01)
            # Families tracked
            self.ai_breed_families_tracked+=int(cycle_frac*50)
            # Egg quality score fluctuates with AI monitoring
            self.ai_breed_egg_quality_score=0.95+0.05*math.sin(self.total_ticks*0.001)
            # Count generations
            if self.hatchery_cycle_day>=7.0:
                self.ai_breed_generations+=1
        # ===== SELF-HERDING (shrimp school tracking) =====
        if self.ai_herd_active:
            # Track schools after each release
            if self.hatchery_cycle_day>=7.0 and self.juveniles_released>0:
                self.ai_herd_schools_tracked+=1
            # eDNA sampling every 12 hours
            if self.total_ticks%int(12.0*3600.0/dt)==0:
                self.ai_herd_edna_samples+=1
            # Drone swarm active during harvest and transit
            self.ai_herd_drones_active=AI_SYSTEMS["self_herding"]["drone_swarm_count"] if (
                self.is_harvesting or self.vessel_mode=="TRANSIT") else 0
            # Recapture predictions (weekly)
            if self.total_ticks%200==0:
                self.ai_herd_recapture_predictions+=1
            # Predator alerts (occasional)
            if self.total_ticks%500==0 and self.is_harvesting:
                self.ai_herd_predator_alerts+=1
            # Fleet contracts (when recapture predictions made)
            if self.total_ticks%200==0:
                self.ai_herd_fleet_contracts+=1
            # Migration patterns learned (slowly)
            if self.total_ticks%1000==0:
                self.ai_herd_migration_patterns_learned+=1
        # ===== SELF-MAINTAINING (predictive maintenance) =====
        if self.ai_maint_active:
            # Sensor readings accumulate
            self.ai_maint_sensor_readings+=int(dt_s*AI_SYSTEMS["self_maintaining"]["sensors_total"]/3600.0)
            # System health scores (degrade slowly, AI repairs)
            subsystems=["hull","engine","hatchery","algae","propulsion","h2_system",
                        "battery","trawl","electronics","solar"]
            for s in subsystems:
                if s not in self.ai_maint_system_health:
                    self.ai_maint_system_health[s]=1.0
                # Degrade based on usage
                degrade=dt_s*1e-6*(1.5 if self.genset_on else 0.5)
                if s=="trawl" and self.is_harvesting: degrade*=3.0
                if s=="hatchery": degrade*=2.0
                if s=="algae": degrade*=1.5
                self.ai_maint_system_health[s]=max(0.3,self.ai_maint_system_health[s]-degrade)
                # AI auto-repair: bring health back up
                if self.ai_maint_system_health[s]<0.8:
                    self.ai_maint_system_health[s]=min(1.0,self.ai_maint_system_health[s]+dt_s*2e-5)
                    if self.total_ticks%100==0:
                        self.ai_maint_auto_repairs+=1
            # Predictive predictions
            if self.total_ticks%50==0:
                self.ai_maint_predictions+=1
                # Check for anomalies
                for s,health in self.ai_maint_system_health.items():
                    if health<0.6:
                        self.ai_maint_anomalies_detected+=1
                        self.ai_maint_repairs_scheduled+=1
                        break
            # 3D printed spare parts
            if self.total_ticks%500==0:
                self.ai_maint_parts_3d_printed+=1
                self.ai_maint_repairs_completed+=1
            # Uptime calculation
            total_sys=len(self.ai_maint_system_health)
            healthy=sum(1 for h in self.ai_maint_system_health.values() if h>0.9)
            self.ai_maint_uptime_pct=100.0*healthy/max(1,total_sys)
        # ===== ORCHESTRATOR =====
        self.ai_total_decisions+=1
        # Weekly model updates (federated learning)
        if self.total_ticks%1000==0:
            self.ai_model_updates+=1
        # Continuous learning
        self.ai_learning_cycles+=1

    def _update_animation(self,dt,genset_total_kw):
        """Update animation state for engine, flywheel, etc."""
        self.fly_omega*=max(0.0,1.0-dt*0.00002)
        tgt_ring=3000.0 if self.genset_on else (600.0 if genset_total_kw>5 else 0.0)
        self.ring_rpm+=(tgt_ring-self.ring_rpm)*min(1.0,dt/30.0)
        self.gen_rpm+=(tgt_ring*1.7-self.gen_rpm)*min(1.0,dt/30.0)

# SECTION 7 -- VOYAGE WORLD

class Voyage:
    TIME_WARP=[60.0,300.0,1800.0,7200.0,21600.0]
    def __init__(self):
        self.warp_i=2; self.elapsed_h=0.0; self.distance_nm=0.0
        self.weather=0.8; self.sea_state=0.25; self.sun=0.0; self.finished=False
    @property
    def warp(self): return self.TIME_WARP[self.warp_i]
    @property
    def hour_of_day(self): return self.elapsed_h%24.0
    @property
    def day(self): return int(self.elapsed_h//24.0)+1
    def cycle_warp(self,d):
        self.warp_i=clamp(self.warp_i+d,0,len(self.TIME_WARP)-1)
    def update(self,dt_real,pt):
        dt_v=dt_real*self.warp; self.elapsed_h+=dt_v/3600.0
        t=self.elapsed_h
        self.weather=clamp(0.72+0.26*math.sin(t/15.3)+0.10*math.sin(t/4.1))
        self.sea_state=clamp(0.28+0.22*math.sin(t/9.7+1.0)+0.12*math.sin(t/2.9))
        self.sun=sun_factor(self.hour_of_day)*(0.35+0.65*self.weather)
        return dt_v
    def advance_distance(self,speed_kn,dt_v):
        self.distance_nm+=speed_kn*(dt_v/3600.0)
        if self.distance_nm>=VOYAGE["distance_nm"]:
            self.distance_nm=VOYAGE["distance_nm"]; self.finished=True
    @property
    def progress(self): return clamp(self.distance_nm/VOYAGE["distance_nm"])

def sky_colors(sun):
    t=clamp(sun*1.6)
    return _mix(C_SKY_NIGHT1,C_SKY1,t),_mix(C_SKY_NIGHT2,C_SKY2,t)

# SECTION 8 -- INFO SECTIONS

def _diesel_ref():
    return (diesel_fuel_tonnes(VOYAGE["distance_nm"],VOYAGE["diesel_speed_kn"]),
            diesel_cost_usd(VOYAGE["distance_nm"],VOYAGE["diesel_speed_kn"]))

def build_info_sections():
    dt_t,dt_c=_diesel_ref()
    return [
        ("THE VESSEL",[
            "TIGER LEVIATHAN-CLASS digital twin -- a 260m semi-submersible",
            "pentamaran hatchery-nursery vessel for Ocean Abundance Corp.",
            "LOA %.0f m x beam %.0f m x draft %.0f m."%(SHIP["loa_m"],SHIP["beam_m"],SHIP["draft_m"]),
            "Full-load displacement %.0f t, %d slender hulls."%(SHIP["displacement_t"],SHIP["hull_count"]),
            "Design speed %.0f kn; solar-hybrid cruise 12-16 kn (free fuel)."%SHIP["design_speed_kn"],
            "Storm mode: ballast down in <30 min, survives Cat 5.",
        ]),
        ("HOW IT MOVES (series hybrid, electricity only)",[
            "NO DIRECT FUEL TO THRUST. Every joule of propulsion is",
            "electric, through quad EM-RAIL AZIMUTH PODS: the pole rail",
            "spins the propeller shaft directly -- no gearbox, ~97.8% efficient.",
            "The rotary H2 engine never touches the water; it only ever",
            "makes ELECTRICITY to CHARGE THE BATTERY as a supplement.",
        ]),
        ("THE ROTARY H2 ENGINE (battery charger, re-fuelled)",[
            "The proven 8-chamber rotary now burns onboard HYDROGEN.",
            "Rated %.1f MW electrical, turbo + slow auto supercharger"%(GENSET_RATED_KW/1000),
            "packs the H2:air charge, %d concentric transmission gear rings"%DIMS["trans_rings"],
            "step the ring torque to the generator, a free-floating tungsten",
            "flywheel buffers momentum, and a CLOSED-LOOP STEAM loop with a",
            "3-stage compound expander + steam generator traps the waste heat",
            "and milks ~%.0f%% of it back as electricity."%(STEAM_RECOVER_FRAC*100),
        ]),
        ("FREE FUEL (sunlight + seawater -> hydrogen)",[
            "An elevated %.0f m2 SOLAR CARGO-ROOF canopy spans the full"%DIMS["solar_panel_m2"],
            "deck on %d support pillars (%.0f%% bifacial PERC),"%(DIMS["solar_roof_pillars"],DIMS["solar_eff"]*100),
            "peaking ~%.1f MW in full sun."%(SOLAR_PEAK_KW/1000),
            "Surplus power runs %d mesh-grid SEAWATER electrolysis tanks"%DIMS["electro_tanks"],
            "that are ALSO the ship's BALLAST tanks -- dual function.",
            "Fills a %.0f-tonne, %.0f bar compressed H2 buffer."%(DIMS["h2_capacity_kg"]/1000,DIMS["h2_bar"]),
        ]),
        ("HULL / DECK HARVESTERS",[
            "%d STABILIZING HEAVE-OAR generators ride the hull sides."%DIMS["heave_fins"],
            "%d DECK ROTORS spin on wind from ANY heading."%DIMS["rotors"],
            "A THROUGH-HULL FLOW TUNNEL cuts hull pressure drag.",
            "%d HANGING INTERNAL WEIGHTS reclaim roll/pitch/heave."%DIMS["weight_harvesters"],
            "SUPERHYDROPHOBIC SiO2 nano-coating: 155 deg contact angle,",
            "22%% drag reduction, 85%% biofouling reduction, 7-yr lifespan.",
        ]),
        ("SHRIMP HATCHERY-NURSERY (the biological payload)",[
            "Species: %s"%SHRIMP["species"],
            "%d broodstock females in %d RAS maturation tanks."%(DIMS["broodstock_females"],DIMS["broodstock_tanks"]),
            "%.0fK eggs/female/spawn x %d spawns/year = %.1fT eggs/year."%(
                SHRIMP["eggs_per_spawn"]/1000,SHRIMP["spawns_per_year"],
                shrimp_eggs_per_year()/1e12),
            "Survival chain: egg->nauplii %.0f%% -> PL20 %.0f%% -> juvenile %.0f%%."%(
                SHRIMP["egg_to_nauplii"]*100,SHRIMP["nauplii_to_pl20"]*100,
                SHRIMP["pl20_to_juvenile"]*100),
            "Annual juvenile output: %.0f billion (per vessel)."%(
                shrimp_juveniles_per_vessel_per_year()/1e9),
            "Fleet of 12: %.1f trillion juveniles/year."%(fleet_juveniles_per_year(12)/1e12),
            "Harvest biomass potential: %.0f million tonnes/year (fleet)."%(
                shrimp_harvest_biomass_tonnes()*12/1e6),
            "DNA barcoded (CRISPR-Cas9) -- legal ownership of tagged biomass.",
        ]),
        ("THE $0 VOYAGE (FREE FUEL via SE.py rotary H2 engine)",[
            "Test route: %.0f nm nursery-ground transit."%VOYAGE["distance_nm"],
            "All hydrogen is self-made from free sun + ocean, so the",
            "FUEL BILL IS $0. A conventional diesel ship on the same",
            "crossing at %.0f kn would burn ~%.0f t of VLSFO --"%(
                VOYAGE["diesel_speed_kn"],dt_t),
            "about $%s in fuel alone. This ship pays nothing."%f"{dt_c:,.0f}",
            "The SE.py rotary H2 engine technology makes fuel for ships,",
            "mega-platforms, and hatcheries completely FREE.",
            "Electrolysis efficiency: ~72%%, H2 engine: ~60%%,",
            "Round-trip: ~43%%. The sun covers the losses.",
        ]),
        ("MICROALGAE FARM (FREE FEED via photosynthesis)",[
            "Sun + CO2 + seawater nutrients -> microalgae -> shrimp feed.",
            "Just as fuel is FREE (H2 from seawater), FEED is also FREE.",
            "Photosynthesis powers the algae farm at zero cost.",
            "",
            "Species: %s + %s + %s"%(
                ALGAE_FARM["species_primary"],ALGAE_FARM["species_secondary"],
                ALGAE_FARM["species_tertiary"]),
            "%d open ponds (%.0f m dia) + %d photobioreactors (%.0f m x %.0f m)"%(
                DIMS["algae_ponds"],DIMS["algae_pond_d_m"],
                DIMS["algae_photobioreactors"],DIMS["algae_pbr_d_m"],DIMS["algae_pbr_h_m"]),
            "Total area: %.0f m2.  Greenhouse: %.0f m2."%(
                DIMS["algae_pond_area_m2"],DIMS["algae_greenhouse_m2"]),
            "Growth rate: %.0f g/m2/day.  Harvest every %.0f days."%(
                ALGAE_FARM["growth_rate_g_m2_day"],ALGAE_FARM["harvest_interval_days"]),
            "Nutrition: %.0f%% protein, %.0f%% lipid, %.0f%% carb, %.0f%% pigment."%(
                ALGAE_FARM["protein_content_pct"],ALGAE_FARM["lipid_content_pct"],
                ALGAE_FARM["carb_content_pct"],ALGAE_FARM["pigment_content_pct"]),
            "Replaces %.0f%% of commercial feed.  FCR improves %.1f -> %.1f."%(
                ALGAE_FARM["feed_replacement_frac"]*100,SHRIMP["fcr"],
                ALGAE_FARM["fcr_with_algae"]),
            "Annual production: %.0f t/vessel.  Fleet: %.0f t/yr."%(
                algae_production_t_per_year(),fleet_algae_production_t_per_year()),
            "CO2 captured: %.0f t/yr/vessel.  O2 produced: %.0f t/yr/vessel."%(
                algae_co2_captured_t_per_year(),algae_o2_produced_t_per_year()),
            "Feed cost: $0.00/kg (FREE, just like fuel).",
            "Savings: $%.0fM/yr/vessel vs commercial feed."%(
                algae_feed_savings_usd_per_year()/1e6),
            "LED night supplement: 660nm red + 450nm blue (%d kW)."%(
                ALGAE_FARM["led_supplement_kw"]),
            "Nutrients: hatchery wastewater + seawater minerals (closed loop).",
            "Harvest: centrifuge + drum filter.  Drying: solar-thermal spray dryer.",
            "Monitoring: AI + hyperspectral imaging for quality control.",
            "Scales to mega-platforms: same principle, larger area.",
        ]),
        ("CATCH & PROCESSING (HARVEST mode)",[
            "Trawl: 120 m wide x 45 m deep, 28 mm mesh, 3.5 kn tow speed",
            "Catch rate: 8,500 kg/hr   Processing: 12,000 kg/hr",
            "AI-assisted sorting: 97%% bycatch escape ratio",
            "Onboard freezing: 12,000 kg/hr   Packaging: 10,000 kg/hr",
            "Frozen storage: 8,000 t capacity",
            "Shrimp price: $4.85/kg ($2.20/lb)   Bycatch discarded: 3%%",
        ]),
        ("RECAPTURE & DNA BARCODING",[
            "Every batch tagged with CRISPR-Cas9 DNA barcode markers.",
            "Target recapture rate: 65%% (acoustic + pheromone conditioning).",
            "Juvenile-to-harvest survival: 15%% in wild conditions.",
            "Harvest size: 300g at 180 days post-release.",
            "Recapture value: $4.85/kg of harvested shrimp.",
            "DNA markers = legal ownership of released biomass.",
        ]),
        ("INVESTMENT & FINANCE",[
            "Vessel cost: $%.1fB each   Fleet target: %d vessels"%(
                FINANCE["vessel_cost_usd"]/1e9,FINANCE["fleet_target"]),
            "Total investment: $%.1fB   Target: $%.0fT valuation by Year %d"%(
                FINANCE["investment_usd"]/1e9,
                FINANCE["target_valuation_usd"]/1e12,FINANCE["target_years"]),
            "Revenue streams per vessel per year:",
            "  Shrimp harvest:  $%.1fB   Carbon credits: $%.0fM"%(
                FINANCE["shrimp_revenue_per_vessel_year_usd"]/1e9,
                FINANCE["carbon_credit_per_vessel_year_usd"]/1e6),
            "  Tech licensing:  $%.0fM   Data sales:     $%.0fM"%(
                FINANCE["tech_license_per_vessel_year_usd"]/1e6,
                FINANCE["data_sales_per_vessel_year_usd"]/1e6),
            "Fleet of 12: $%.0fB/year total revenue potential."%(
                (FINANCE["shrimp_revenue_per_vessel_year_usd"]+
                 FINANCE["carbon_credit_per_vessel_year_usd"]+
                 FINANCE["tech_license_per_vessel_year_usd"]+
                 FINANCE["data_sales_per_vessel_year_usd"])*12/1e9),
        ]),
        ("GLOBAL DONATION PROGRAM",[
            "OAC FREE PROTEIN INITIATIVE",
            "\"No vessel leaves a port without feeding the hungry\"",
            "",
            "5%% of all harvest donated FREE at every port stop.",
            "  = %.1fM t/year donated   = %.0fB free 4oz meals"%(
                DONATION_PROGRAM["donation_t_year"]/1e6,
                DONATION_PROGRAM["donation_meals_year"]/1e9),
            "  = protein for %.0fM people/year (50g protein/day each)"%(
                DONATION_PROGRAM["people_fed_year"]/1e6),
            "  = %.2fB kg protein/year delivered FREE"%(
                DONATION_PROGRAM["protein_kg_year"]/1e9),
            "",
            "PORT STOPS (18 EEZ nations + 4 seasonal hubs + 7 distribution hubs):",
            "  Each EEZ port: 350K t/year, 3.1B meals, 4.6M people fed",
            "  Each hub port: 250K t/year, 2.21B meals, 3.3M people fed",
            "  Offload per docking: 29K t (EEZ) / 42K t (hub) (4h port-side handoff)",
            "",
            "PARTNER ORGANIZATIONS (%d):"%len(DONATION_PROGRAM["partner_organizations"]),
        ]+[
            "  %s -- %s (%d countries)"%(p["name"],p["role"],p["countries"])
            for p in DONATION_PROGRAM["partner_organizations"]
        ]+[
            "",
            "LOGISTICS: Vessel docks -> refrigerated port-side handoff",
            "  -> NGO trucks -> community kitchens + food banks within 24h",
            "  Cold chain: -18C from vessel hold to distribution point",
            "  Packaging: 100%% recyclable bioplastic, DNA-barcoded",
            "  Transparency: Blockchain-tracked, publicly auditable",
            "",
            "Revenue foregone: $%.1fB/year (donated at $0 vs $4.85/kg)"%(
                DONATION_PROGRAM["revenue_foregone_usd_year"]/1e9),
            "Tax benefit: $4.4B/year deductible (US IRS + Singapore IRAS)",
            "ESG: SDG 2 (Zero Hunger), SDG 3 (Health), SDG 14, SDG 17",
            "Expansion: Year 5+ -> 10%%, Year 10 -> 15%% of harvest",
        ]),
        ("AI SYSTEMS (AUTONOMOUS VESSEL)",[
            "The Tiger Leviathan is FULLY AUTONOMOUS. AI operates all",
            "systems. The 75-person crew is supervisory only.",
            "",
            "ORCHESTRATOR: %s"%AI_SYSTEMS["orchestrator"]["name"],
            "  Hardware: %s"%AI_SYSTEMS["orchestrator"]["hardware"],
            "  Model: %s"%AI_SYSTEMS["orchestrator"]["ml_model"],
            "  Decision latency: %dms   Subsystems: %d"%(
                AI_SYSTEMS["orchestrator"]["decision_latency_ms"],
                len(AI_SYSTEMS["orchestrator"]["subsystems"])),
            "  Learning: %s"%AI_SYSTEMS["orchestrator"]["learning_mode"],
            "  Updates: %s"%AI_SYSTEMS["orchestrator"]["model_updates"],
            "  Security: %s"%AI_SYSTEMS["orchestrator"]["cyber_security"],
            "",
            "1. SELF-DRIVING: %s"%AI_SYSTEMS["self_driving"]["name"],
            "  Autonomy: %s"%AI_SYSTEMS["self_driving"]["autonomy_level"],
            "  Hardware: %s"%AI_SYSTEMS["self_driving"]["hardware"],
            "  Sensors: %s"%AI_SYSTEMS["self_driving"]["sensors"],
            "  Model: %s"%AI_SYSTEMS["self_driving"]["ml_model"],
            "  Training: %s"%AI_SYSTEMS["self_driving"]["training_data"],
            "  Safety: %s"%AI_SYSTEMS["self_driving"]["safety_record"],
            "  Redundancy: %s"%AI_SYSTEMS["self_driving"]["redundancy"],
            "  Capabilities: route optimization, collision avoidance,",
            "    weather routing, autonomous docking, speed optimization,",
            "    auto mode selection (DRIFT/HARVEST/TRANSIT/STORM)",
            "",
            "2. SELF-BREEDING: %s"%AI_SYSTEMS["self_breeding"]["name"],
            "  Hardware: %s"%AI_SYSTEMS["self_breeding"]["hardware"],
            "  Model: %s"%AI_SYSTEMS["self_breeding"]["ml_model"],
            "  Generations/yr: %d   Genetic gain/gen: %.0f%%"%(
                AI_SYSTEMS["self_breeding"]["generations_per_year"],
                AI_SYSTEMS["self_breeding"]["genetic_gain_per_gen_pct"]),
            "  Diversity target: %.2f   Inbreeding max: %.3f"%(
                AI_SYSTEMS["self_breeding"]["diversity_target"],
                AI_SYSTEMS["self_breeding"]["inbreeding_max"]),
            "  Database: %s"%AI_SYSTEMS["self_breeding"]["database"],
            "  Capabilities: broodstock selection, selective breeding,",
            "    spawning prediction, egg quality assessment, family tracking,",
            "    trait optimization (growth +25%%, survival +18%%, FCR -12%%),",
            "    automatic cross-breeding, larval health prediction",
            "",
            "3. SELF-HERDING: %s"%AI_SYSTEMS["self_herding"]["name"],
            "  Hardware: %s"%AI_SYSTEMS["self_herding"]["hardware"],
            "  Model: %s"%AI_SYSTEMS["self_herding"]["ml_model"],
            "  Tracking range: %dkm   Accuracy: %.0f%%"%(
                AI_SYSTEMS["self_herding"]["tracking_range_km"],
                AI_SYSTEMS["self_herding"]["tracking_accuracy_pct"]),
            "  Drones: %d x %.0fhr endurance   Satellite revisit: %.1fhr"%(
                AI_SYSTEMS["self_herding"]["drone_swarm_count"],
                AI_SYSTEMS["self_herding"]["drone_endurance_h"],
                AI_SYSTEMS["self_herding"]["satellite_revisit_h"]),
            "  Recapture prediction accuracy: %.0f%%"%(
                AI_SYSTEMS["self_herding"]["recapture_prediction_accuracy"]),
            "  Capabilities: school tracking, wild population monitoring,",
            "    recapture forecasting, fishing fleet coordination,",
            "    school health monitoring, predator detection,",
            "    migration pattern learning, release site optimization",
            "",
            "4. SELF-MAINTAINING: %s"%AI_SYSTEMS["self_maintaining"]["name"],
            "  Hardware: %s"%AI_SYSTEMS["self_maintaining"]["hardware"],
            "  Model: %s"%AI_SYSTEMS["self_maintaining"]["ml_model"],
            "  Sensors: %d   Prediction accuracy: %.1f%%"%(
                AI_SYSTEMS["self_maintaining"]["sensors_total"],
                AI_SYSTEMS["self_maintaining"]["prediction_accuracy_pct"]),
            "  Auto-repair: %.0f%% of issues   Robotic arms: %d   3D printers: %d"%(
                AI_SYSTEMS["self_maintaining"]["auto_repair_pct"],
                AI_SYSTEMS["self_maintaining"]["robotic_repair_arms"],
                AI_SYSTEMS["self_maintaining"]["spare_parts_3d_printers"]),
            "  Uptime target: %.1f%%   MTTR: %.0fhr   False positive: %.1f%%"%(
                AI_SYSTEMS["self_maintaining"]["uptime_target_pct"],
                AI_SYSTEMS["self_maintaining"]["mean_time_to_detect_h"],
                AI_SYSTEMS["self_maintaining"]["false_positive_rate_pct"]),
            "  Capabilities: vibration analysis, thermal monitoring,",
            "    acoustic monitoring, corrosion prediction, H2 leak detection,",
            "    battery health, hatchery water quality, algae farm monitoring,",
            "    auto-repair scheduling, supply chain optimization",
        ]),
        ("HONEST PHYSICS",[
            "This is NOT perpetual motion. Solar and wind are EXTERNAL",
            "energy. Electrolysis (~50-70%) then H2->electric (~50%) is lossy;",
            "the sun makes up the difference. Speed is sacrificed: the cube",
            "law (P ~ v^3) means slow-steaming slashes demand enough that",
            "solar + seawater H2 can carry the ship.",
        ]),
        ("VESSEL OPERATIONAL MODES",[
            "DRIFT (F1):  current-driven, minimal sail, superhydrophobic hull,",
            "             hatchery full production, H2 engine OFF, 1-4 kn",
            "HARVEST (F2): trawl deployed (120m x 45m), 3.5 kn, AI sorting,",
            "              8500 kg/hr catch, 97%% bycatch escape, superhydrophobic",
            "TRANSIT (F3): full sails + rotors, 12-18 kn, all harvesters active,",
            "              superhydrophobic hull, H2 engine auto-supplement",
            "STORM (F4):  full ballast in <28 min, 8%% waterplane, <10 deg roll,",
            "             survives Cat 5 (175 kn, 18 m waves), hatchery secured",
        ]),
        ("GLOBAL SEASONAL ROUTES (MAP TAB)",[
            "The AI self-driving system selects optimal routes by season,",
            "balancing sea state, sunlight, currents, shrimp growth, and",
            "algae productivity. See the MAP tab for the world map.",
            "",
            "SPRING (Mar-May): Equatorial Pacific (5°N-5°S)",
            "  Route: Singapore -> Banda Sea -> Coral Triangle -> release",
            "  Calm seas (25%%), sun 78%%, growth 115%%, algae 120%%",
            "  Predator risk: LOW. Release: Banda Sea, Coral Triangle, Molucca",
            "",
            "SUMMER (Jun-Aug): North Pacific Gyre (20°N-35°N)",
            "  Route: Yokohama -> North Pacific -> Gulf of Alaska -> release",
            "  Long daylight (92%% sun), algae 135%%, growth 108%%",
            "  Predator risk: MEDIUM. Release: N. Pacific Gyre, Gulf of Alaska",
            "",
            "AUTUMN (Sep-Nov): Equatorial Atlantic (0°-10°S)",
            "  Route: Capetown -> Gulf of Guinea -> Angola Basin -> release",
            "  Benguela upwelling, nutrients rich, sun 72%%, growth 112%%",
            "  Predator risk: LOW. Release: Gulf of Guinea, Angola Basin",
            "",
            "WINTER (Dec-Feb): Indian Ocean (10°S-25°S)",
            "  Route: Fremantle -> Indian Ocean gyre -> Mozambique Channel",
            "  Post-monsoon calm (22%% sea), sun 85%%, growth 118%%, algae 125%%",
            "  Predator risk: LOW. Release: Mozambique Channel, Indian Ocean",
            "",
            "Hub ports: Singapore, Yokohama, Fremantle, Capetown, Panama",
            "16 release zones tracked across 4 oceans",
            "AI routes updated continuously based on real-time conditions",
        ]),
        ("14 INNOVATION UPGRADES (cost-saving + efficiency)",[
            "1. OTEC: 3 MW 24/7 baseload from ocean temp gradient (no fuel)",
            "   Closed-cycle ammonia, 500m cold pipe, complements solar",
            "2. Perovskite tandem solar: 35%% efficiency (was 26%%) = +35%% power",
            "   Perovskite-on-silicon, 25yr lifespan, 0.5%%/yr degradation",
            "3. Air lubrication: microbubbles under hull = 12%% drag reduction",
            "   Stacks with superhydrophobic = 34%% total drag reduction",
            "4. IMTA seaweed polyculture: 1200 t/yr, removes N/P waste",
            "   +$3.6M/yr revenue, 480 t CO2 sequestered, 10%% feed supplement",
            "5. Black Soldier Fly larvae: 800 t/yr, 42%% protein from waste",
            "   15%% feed replacement, closes loop to 100%% feed self-sufficiency",
            "6. Anaerobic digester: 800 kW biogas from shrimp/algae waste",
            "   Digestate feeds algae ponds = closed-loop nutrients",
            "7. Acoustic + pheromone recapture: 35%% -> 65%% recapture rate",
            "   Condition juveniles with sound + scent before release",
            "9. Crew reduction: 150 -> 75 (AI autonomy, $10.5M/yr/vessel saved)",
            "   75 = supervisory + emergency + science only",
            "10. Hybrid fleet: 1,200 AI super-trawlers + 3,500 partner vessels",
            "    AI trawlers: $38M each, 400K lbs/day. Partners: $0.30/kg fee",
            "11. Continuous release: trickle vs weekly batch, +5%% survival",
            "    Prevents predator learning, constant saturation",
            "12. Yeast single-cell protein: H2 + CO2 -> 80%% protein biomass",
            "    200 t/yr, 5%% feed replacement, literally protein from air+water",
            "13. Floating solar rafts: +60,000 m2 in drift mode = +21 MW peak",
            "    Folds for transit, stacks with roof solar",
            "14. AUV fleet: 8 autonomous underwater vehicles, 24h endurance",
            "    Sonar + camera + eDNA, swarm coordination, 500m depth",
            "15. Swarm intelligence: fleet-wide coordination of all 12 vessels",
            "    Satellite mesh + acoustic, 100ms decisions, unified optimization",
            "16. Biofloc system: 50%% feed from bacterial protein (waste recycling)",
            "    Heterotrophic bacteria eat shrimp waste -> protein flocs -> re-eaten",
            "",
            "COMBINED IMPACT:",
            "  Energy: 24/7 power (solar+OTEC+digester), $0 fuel forever",
            "  Feed: 100%% self-sufficient (biofloc 50%%+algae 30%%+BSF 15%%+yeast 5%%)",
            "  Drag: 34%% reduction (superhydrophobic+air lube) = faster, less energy",
            "  Recapture: 65%% (was 35%%) via acoustic+pheromone = 30%% more harvest",
            "  Crew: 50%% reduction = $126M/yr fleet savings",
            "  CAPEX: $45.6B AI trawler fleet (1,200 vessels) + 3,500 partners",
            "  Survival: +5%% from continuous release (no predator learning)",
            "  Revenue: IMTA seaweed +$43.2M/yr fleet, carbon credits from seaweed",
        ]),
        ("OPERATION PLAN (OPS TAB)",[
            "See the OPS tab for full construction phases, fleet rollout,",
            "and live AI systems status with health bars.",
            "",
            "CONSTRUCTION (30 months, 7 phases):",
            "  Phase 1 (mo 1-8):   Hull construction + coating",
            "  Phase 2 (mo 9-14):  Propulsion & power (solar, H2, battery)",
            "  Phase 3 (mo 15-20): Hatchery fit-out (pools, DNA lab, chutes)",
            "  Phase 4 (mo 18-21): Algae farm (ponds, PBRs, LED, harvest)",
            "  Phase 5 (mo 20-24): AI systems (all 4 subsystems + sensors)",
            "  Phase 6 (mo 24-28): Sea trials (all systems verified)",
            "  Phase 7 (mo 28-30): Commissioning & certification",
            "",
            "FLEET ROLLOUT (3 years):",
            "  Year 1: Vessels 1-3    Year 2: Vessels 4-8",
            "  Year 3: Vessels 9-12   Total: 12 vessels",
            "",
            "FINANCIAL: $%.0fB investment -> $%.0fT target (Year %d)"%(
                FINANCE["investment_usd"]/1e9,FINANCE["target_valuation_usd"]/1e12,FINANCE["target_years"]),
            "  Revenue/vessel/yr: $%.1fB (shrimp+carbon+tech+data)"%(
                (FINANCE["shrimp_revenue_per_vessel_year_usd"]+FINANCE["carbon_credit_per_vessel_year_usd"]+FINANCE["tech_license_per_vessel_year_usd"]+FINANCE["data_sales_per_vessel_year_usd"])/1e9),
            "  Fleet (12): $%.1fB/yr total revenue potential"%(
                (FINANCE["shrimp_revenue_per_vessel_year_usd"]+FINANCE["carbon_credit_per_vessel_year_usd"]+FINANCE["tech_license_per_vessel_year_usd"]+FINANCE["data_sales_per_vessel_year_usd"])*12/1e9),
        ]),
        ("CONTROLS",[
            "TAB  cycle SHIP / ENGINE / HATCHERY / CRUISE / MAP / OPS",
            "mouse drag  orbit    wheel  zoom    right-drag  pan",
            "E  explode    X  cross-section    L  labels    R  reset view",
            "[ ]  step assembly    A  assemble all    C  clear",
            "V  verification checklist    I  this info panel",
            "In CRUISE/MAP/OPS:  , / .  slow / speed up TIME-WARP",
            "In CRUISE:  F1/F2/F3/F4  DRIFT/HARVEST/TRANSIT/STORM",
            "MAP tab:  global seasonal routes & sea planning",
            "OPS tab:  operation plan, fleet rollout & AI status",
            "H  controls    ESC  quit",
        ]),
    ]

# SECTION 9 -- HUD / UI HELPERS

def vgradient(surf,top,bot):
    h=surf.get_height(); w=surf.get_width()
    for y in range(h):
        t=y/max(1,h)
        col=(int(top[0]+(bot[0]-top[0])*t),int(top[1]+(bot[1]-top[1])*t),int(top[2]+(bot[2]-top[2])*t))
        pygame.draw.line(surf,col,(0,y),(w,y))

def bar(surf,font,x,y,w,h,frac,color,label,valtext,lo=None,hi=None):
    pygame.draw.rect(surf,C_PANEL_HI,(x,y,w,h),border_radius=4)
    frac=clamp(frac)
    pygame.draw.rect(surf,color,(x,y,int(w*frac),h),border_radius=4)
    if lo is not None:
        pygame.draw.line(surf,C_WARN,(x+int(w*lo),y-2),(x+int(w*lo),y+h+2),1)
    if hi is not None:
        pygame.draw.line(surf,C_WARN,(x+int(w*hi),y-2),(x+int(w*hi),y+h+2),1)
    surf.blit(font.render(label,True,C_TEXT_DIM),(x,y-16))
    img=font.render(valtext,True,C_TEXT)
    surf.blit(img,(x+w-img.get_width(),y-16))

def panel(surf,x,y,w,h,alpha=210):
    s=pygame.Surface((w,h),pygame.SRCALPHA)
    s.fill((C_PANEL[0],C_PANEL[1],C_PANEL[2],alpha))
    surf.blit(s,(x,y))
    pygame.draw.rect(surf,C_PANEL_HI,(x,y,w,h),1,border_radius=6)

def wrap_text(font,text,maxpx):
    out,cur=[],""
    for word in text.split(" "):
        trial=word if not cur else cur+" "+word
        if font.size(trial)[0]<=maxpx: cur=trial
        else:
            if cur: out.append(cur)
            cur=word
    if cur: out.append(cur)
    return out or [""]

def draw_combustion(surf,x,y,R,intensity):
    R=int(max(2,R*(0.55+0.9*intensity)))
    g=pygame.Surface((R*2+4,R*2+4),pygame.SRCALPHA)
    c=R+2
    pygame.draw.circle(g,(90,150,255,int(70*intensity)),(c,c),R)
    pygame.draw.circle(g,(150,200,255,int(120*intensity)),(c,c),int(R*0.62))
    pygame.draw.circle(g,(235,245,255,int(230*intensity)),(c,c),int(R*0.30))
    surf.blit(g,(int(x-c),int(y-c)))
    for k in range(6):
        a=k*math.pi/3+intensity*2.0
        ex,ey=x+math.cos(a)*R*1.25,y+math.sin(a)*R*1.25
        pygame.draw.line(surf,(150,200,255),(x,y),(ex,ey),1)

def draw_injection(surf,x,y,R,intensity):
    top=y-R*(1.6+1.2*intensity); col=(180,235,255)
    for dx in (-R*0.4,0,R*0.4):
        pygame.draw.line(surf,col,(x+dx*0.3,top+R*0.4),(x+dx,y-R*0.2),1)
    pygame.draw.circle(surf,col,(int(x),int(top)),max(1,int(R*0.18)))

def _label(surf,font,text,pos,accent=False):
    col=(255,210,120) if accent else C_TEXT
    dot=(255,210,120) if accent else C_ACCENT
    img=font.render(text,True,col)
    x,y=int(pos[0])+6,int(pos[1])-6
    bg=pygame.Surface((img.get_width()+8,img.get_height()+4),pygame.SRCALPHA)
    bg.fill((10,14,20,190))
    surf.blit(bg,(x-4,y-2))
    pygame.draw.circle(surf,dot,(int(pos[0]),int(pos[1])),3)
    surf.blit(img,(x,y))

# SECTION 10 -- 3D RENDERER

class ShipRenderer:
    def __init__(self,parts_builder,is_engine=False,home_az=0.62,home_el=0.42,home_dist=1.75):
        self.parts_builder=parts_builder; self.is_engine=is_engine
        self.parts=parts_builder()
        self._home=(home_az,home_el,home_dist)
        self.az,self.el,self.dist=home_az,home_el,home_dist
        self.pan=np.array([0.0,0.0])
        self.light=np.array([0.4,0.7,1.0]); self.light=self.light/np.linalg.norm(self.light)
        self.view="full"; self.section=False; self.explode_amt=0.0
        self.assembled=len(self.parts); self.hovered=None; self.selected=None
        self.pop=np.zeros(len(self.parts)); self.hover_spread=0.0

    def reset_view(self):
        self.az,self.el,self.dist=self._home; self.pan=np.array([0.0,0.0])
    def zoom_at(self,factor,mouse_pos=None,rect=None):
        old=self.dist; self.dist=max(0.35,min(11.0,self.dist*factor))
        if old<=1e-6 or mouse_pos is None or rect is None: return
        if not rect.collidepoint(mouse_pos): return
        anchor=np.array([mouse_pos[0]-(rect.x+rect.w/2.0),mouse_pos[1]-(rect.y+rect.h/2.0)],dtype=float)
        scale=old/self.dist; self.pan=anchor-(anchor-self.pan)*scale
    def orbit(self,dx,dy,fine=False):
        sens=0.004 if fine else 0.009
        self.az+=dx*sens; self.el+=dy*sens; self.el=max(-1.55,min(1.55,self.el))
    def pan_by(self,dx,dy,fine=False):
        sens=0.45 if fine else 1.0; self.pan+=np.array([dx*sens,dy*sens])
    def set_view(self,mode):
        self.view=mode
        if mode=="assembly" and self.assembled>=len(self.parts): self.assembled=0
        self.selected=None
    def toggle_section(self): self.section=not self.section
    def assembly_next(self): self.assembled=min(len(self.parts),self.assembled+1)
    def assembly_prev(self): self.assembled=max(0,self.assembled-1)
    def assembly_all(self): self.assembled=len(self.parts)
    def assembly_clear(self): self.assembled=0
    def active_part(self):
        i=self.selected if self.selected is not None else self.hovered
        return self.parts[i] if i is not None else None
    def placing_part(self):
        for p in self.parts:
            if p.order==self.assembled: return p
        return None
    def tick(self,dt):
        if self.view!="assembly":
            target=1.0 if self.view=="exploded" else 0.0
            self.explode_amt+=(target-self.explode_amt)*min(1.0,dt*4)
        hi=self.selected if self.selected is not None else self.hovered
        sp_target=0.30 if (hi is not None and self.view=="full") else 0.0
        self.hover_spread+=(sp_target-self.hover_spread)*min(1.0,dt*5)
        for i in range(len(self.parts)):
            tp=1.0 if i==hi else 0.0
            self.pop[i]+=(tp-self.pop[i])*min(1.0,dt*8)
    def _layout(self,pi,vw,eamt):
        part=self.parts[pi]
        if vw=="assembly":
            if part.order<self.assembled: return part.explode*0.0,1.0,"normal"
            if part.order==self.assembled: return part.explode*0.55,1.0,"active"
            return part.explode*1.0,0.30,"pending"
        return part.explode*eamt,1.0,"normal"
    def _section_cut(self,wv,face):
        c=wv[list(face)].mean(axis=0); return c[0]>0.004
    def render(self,surf,rect,angles,firing_glow=None,mouse_pos=None,
               show_labels=True,label_font=None,interactive=False,
               injection=None,heat=0.0):
        firing_glow=firing_glow if firing_glow is not None else np.zeros(0)
        clip=surf.get_clip(); surf.set_clip(rect)
        cx=rect.x+rect.w/2.0+self.pan[0]; cy=rect.y+rect.h/2.0+self.pan[1]
        focal=min(rect.w,rect.h)*1.12
        Rcam=rot_x(self.el)@rot_y(self.az)
        default_ang=angles.get("default",0.0)
        vw=self.view; eamt=self.explode_amt
        if self.view=="full": eamt+=self.hover_spread
        section=self.section and vw in ("full","exploded")
        do_outline=self.is_engine
        hi=self.selected if self.selected is not None else self.hovered
        polys,labels,leaders,screeninfo,fire_points=[],[],[],[],[]
        lx,ly,lz=float(self.light[0]),float(self.light[1]),float(self.light[2])
        for pi,part in enumerate(self.parts):
            base_off,dim,tag=self._layout(pi,vw,eamt)
            pop=self.pop[pi]; off=base_off+part.popdir*(pop*0.16)
            highlight=(pi==hi); allcam=[]
            for m in part.meshes:
                wv=m.world_verts(angles.get(m.group,default_ang))+off
                cam=wv@Rcam.T; cam[:,2]+=self.dist; allcam.append(cam)
                caml=cam.tolist(); col=m.color
                if m.chamber_index is not None and len(firing_glow):
                    g=firing_glow[m.chamber_index]
                    if g>0.01: col=_mix(C_CHAMBER,C_CHAMBER_FIRE,g)
                if m.hot and heat>0.01: col=_mix(col,(255,90,40),min(0.7,heat*0.6))
                if dim<0.99: col=(int(col[0]*dim),int(col[1]*dim),int(col[2]*dim))
                if highlight: col=_mix(col,(255,255,255),0.28)
                cr,cg,cb=col
                if highlight: outline,ow=C_ACCENT,2
                elif tag=="active": outline,ow=(255,210,120),2
                elif do_outline: outline,ow=(12,14,18),1
                else: outline,ow=None,0
                sxl,syl,dzl=[],[],[]
                for vx2,vy2,vz2 in caml:
                    dzl.append(vz2)
                    if vz2>0.05:
                        sxl.append(cx+focal*vx2/vz2); syl.append(cy-focal*vy2/vz2)
                    else: sxl.append(0.0); syl.append(0.0)
                if show_labels and label_font and m.name and tag!="pending" and (vw!="full" or highlight):
                    mcen=cam.mean(axis=0)
                    if mcen[2]>0.05:
                        mlx=cx+focal*mcen[0]/mcen[2]; mly=cy-focal*mcen[1]/mcen[2]
                        labels.append((mcen[2],(mlx,mly),m.name,"detail"))
                for face in m.faces:
                    if section and self._section_cut(wv,face): continue
                    clipped=False
                    for i in face:
                        if dzl[i]<=0.05: clipped=True; break
                    if clipped: continue
                    ax,ay,az=caml[face[0]]; bx,by,bz=caml[face[1]]; fx,fy,fz=caml[face[2]]
                    ux,uy,uz=bx-ax,by-ay,bz-az; wx,wy,wz=fx-ax,fy-ay,fz-az
                    nx=uy*wz-uz*wy; ny=uz*wx-ux*wz; nz=ux*wy-uy*wx
                    inv=1.0/((nx*nx+ny*ny+nz*nz)**0.5 or 1.0)
                    nx*=inv; ny*=inv; nz*=inv
                    if nz>0: nx,ny,nz=-nx,-ny,-nz
                    d=nx*lx+ny*ly+nz*lz
                    shade=0.35+0.65*(d if d>0.0 else 0.0)
                    fc=(int(cr*shade),int(cg*shade),int(cb*shade))
                    ds=0.0
                    for i in face: ds+=dzl[i]
                    polys.append((ds/len(face),[(sxl[i],syl[i]) for i in face],fc,outline,ow))
            if not allcam: continue
            cam_all=np.vstack(allcam); cen=cam_all.mean(axis=0)
            if cen[2]>0.05:
                safez=np.where(cam_all[:,2]<=0.05,1e9,cam_all[:,2])
                scx=cx+focal*cam_all[:,0]/safez; scy=cy-focal*cam_all[:,1]/safez
                pcx=cx+focal*cen[0]/cen[2]; pcy=cy-focal*cen[1]/cen[2]
                rad=float(np.max(np.hypot(scx-pcx,scy-pcy)))*0.55+6
                screeninfo.append((pi,pcx,pcy,rad,cen[2],tag))
                anchor=getattr(part,"fire_anchor",None)
                if anchor is not None and tag!="pending":
                    ca=(anchor+off)@Rcam.T; caz=float(ca[2])+self.dist
                    if caz>0.05:
                        fpx=cx+focal*float(ca[0])/caz; fpy=cy-focal*float(ca[1])/caz
                        fire_points.append((caz,fpx,fpy,max(8.0,rad*0.30)))
                if show_labels and label_font and tag!="pending":
                    labels.append((cen[2],(pcx,pcy),part.name,tag))
                if tag=="active":
                    hc=cen-(off@Rcam.T)
                    if hc[2]>0.05:
                        hx=cx+focal*hc[0]/hc[2]; hy=cy-focal*hc[1]/hc[2]
                        leaders.append(((pcx,pcy),(hx,hy)))
        polys.sort(key=lambda t:t[0],reverse=True)
        for _,pts,fc,outline,ow in polys:
            if len(pts)>=3:
                try:
                    pygame.draw.polygon(surf,fc,pts)
                    if outline is not None: pygame.draw.polygon(surf,outline,pts,ow)
                except Exception: pass
        glow=float(np.max(firing_glow)) if len(firing_glow) else 0.0
        inj=float(np.max(injection)) if injection is not None and len(injection) else 0.0
        fire_points.sort(key=lambda t:t[0],reverse=True)
        for _,fpx,fpy,crad in fire_points:
            if inj>0.05: draw_injection(surf,fpx,fpy,crad,inj)
            if glow>0.05: draw_combustion(surf,fpx,fpy,crad,glow)
        for a,b in leaders:
            pygame.draw.line(surf,(255,210,120),a,b,1)
            pygame.draw.circle(surf,(255,210,120),(int(b[0]),int(b[1])),5,1)
        if show_labels and label_font:
            labels.sort(key=lambda t:t[0])
            used=[]
            for _,(lxx,lyy),text,tag in labels:
                ly2=lyy
                for uy in used:
                    if abs(ly2-uy)<16: ly2=uy+16
                used.append(ly2)
                _label(surf,label_font,text,(lxx,ly2),accent=(tag=="active" or tag=="detail"))
        if interactive and mouse_pos is not None:
            mxp,myp=mouse_pos; best,bestd=None,1e18
            for pi,pcx,pcy,rad,depth,tag in screeninfo:
                if tag=="pending": continue
                if math.hypot(mxp-pcx,myp-pcy)<=rad and depth<bestd: bestd,best=depth,pi
            self.hovered=best
        surf.set_clip(clip)

# SECTION 11 -- APPLICATION

VIEW_ROT_SCALE=0.020

class App:
    MODES=["ship","engine","hatchery","cruise","map","ops","innov","company","quota"]
    MODE_NAME={"ship":"SHIP  (whole vessel)","engine":"ENGINE  (rotary H2 engine)",
               "hatchery":"HATCHERY  (shrimp production)","cruise":"CRUISE  (nursery transit)",
               "map":"MAP  (global seasonal routes)","ops":"OPS  (operation plan)",
               "innov":"INNOVATIONS  (14 upgrades)",
               "company":"COMPANY  (business & operations)",
               "quota":"QUOTA  (fisheries management)"}
    LEFT_PANEL_W=220; RIGHT_PANEL_W=352; TOP_BAR_H=36; BOTTOM_BAR_H=86

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Leviathan.py -- Tiger Leviathan-Class Digital Twin")
        info=pygame.display.Info()
        self.W,self.H=info.current_w,info.current_h
        self.screen=pygame.display.set_mode((self.W,self.H),pygame.FULLSCREEN)
        self.fullscreen=True
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("consolas,menlo,dejavusansmono,monospace",14)
        self.fs=pygame.font.SysFont("consolas,menlo,dejavusansmono,monospace",12)
        self.fb=pygame.font.SysFont("consolas,menlo,dejavusansmono,monospace",20,bold=True)
        self.fbig=pygame.font.SysFont("consolas,menlo,dejavusansmono,monospace",30,bold=True)
        self.fmicro=pygame.font.SysFont("consolas,menlo,dejavusansmono,monospace",11)
        self.ship_rend=ShipRenderer(build_ship_parts,is_engine=False,home_az=0.78,home_el=0.33,home_dist=3.40)
        self.eng_rend=ShipRenderer(build_genset_parts,is_engine=True,home_az=0.62,home_el=0.42,home_dist=1.85)
        self.hatch_rend=ShipRenderer(build_hatchery_parts,is_engine=False,home_az=0.50,home_el=0.55,home_dist=2.50)
        self.pt=MarinePowertrain(); self.voyage=Voyage()
        self.mode="ship"; self.ang={}
        self.firing_glow=np.zeros(DIMS["chambers"]); self.injection=np.zeros(DIMS["chambers"])
        self.show_labels=True; self.show_help=False; self.show_info=False; self.show_checklist=False
        self.info_scroll=0; self.info_sections=build_info_sections()
        self.company_scroll=0; self.quota_scroll=0
        self.dragging=False; self.panning=False; self.running=True; self.bg=None
        self._preview_hitboxes={}; self._mode_hitboxes={}; self._part_list_hitboxes={}
        self._rebuild_bg()

    def _rebuild_bg(self):
        self.bg=pygame.Surface((self.W,self.H)); vgradient(self.bg,BG_TOP,BG_BOT)

    def _toggle_fullscreen(self):
        self.fullscreen=not self.fullscreen
        if self.fullscreen:
            info=pygame.display.Info()
            self.W,self.H=info.current_w,info.current_h
            self.screen=pygame.display.set_mode((self.W,self.H),pygame.FULLSCREEN)
        else:
            self.W,self.H=1480,900
            self.screen=pygame.display.set_mode((self.W,self.H))
        self._rebuild_bg()

    def rend(self):
        if self.mode=="engine": return self.eng_rend
        if self.mode=="hatchery": return self.hatch_rend
        return self.ship_rend

    def view_rect(self):
        if self.mode in ("cruise","map","ops","company","quota"):
            return pygame.Rect(0,self.TOP_BAR_H,self.W,self.H-self.TOP_BAR_H)
        return pygame.Rect(self.LEFT_PANEL_W+4,self.TOP_BAR_H+4,
            self.W-self.LEFT_PANEL_W-self.RIGHT_PANEL_W-8,
            self.H-self.TOP_BAR_H-self.BOTTOM_BAR_H-8)

    def handle_events(self,dt):
        r=self.rend()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: self.running=False
            elif e.type==pygame.KEYDOWN: self._key(e)
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1:
                    if self._handle_mode_tab_click(e.pos): continue
                    if self.mode in ("cruise","map","ops","company","quota"): continue
                    if self._handle_part_list_click(e.pos): continue
                    if self._handle_preview_click(e.pos): continue
                    self.dragging=True
                    if r.hovered is not None: r.selected=r.hovered
                    else: r.selected=None
                elif e.button==3: self.panning=True
                elif e.button==4: r.zoom_at(0.9,pygame.mouse.get_pos(),self.view_rect())
                elif e.button==5: r.zoom_at(1.1,pygame.mouse.get_pos(),self.view_rect())
            elif e.type==pygame.MOUSEBUTTONUP:
                if e.button==1: self.dragging=False
                elif e.button==3: self.panning=False
            elif e.type==pygame.MOUSEMOTION:
                if self.mode not in ("cruise","map","ops","company","quota"):
                    if self.dragging: r.orbit(e.rel[0],e.rel[1])
                    elif self.panning: r.pan_by(e.rel[0],e.rel[1])

    def _key(self,e):
        k=e.key; r=self.rend()
        if k==pygame.K_ESCAPE: self.running=False
        elif k==pygame.K_F11: self._toggle_fullscreen()
        elif k==pygame.K_q: self.running=False
        elif k==pygame.K_TAB:
            i=self.MODES.index(self.mode)
            self.mode=self.MODES[(i+1)%len(self.MODES)]
        elif k==pygame.K_h: self.show_help=not self.show_help
        elif k==pygame.K_i: self.show_info=not self.show_info; self.info_scroll=0
        elif self.show_info and k in (pygame.K_DOWN,pygame.K_j): self.info_scroll+=40
        elif self.show_info and k in (pygame.K_UP,pygame.K_k): self.info_scroll=max(0,self.info_scroll-40)
        elif self.mode=="company" and k in (pygame.K_DOWN,pygame.K_j): self.company_scroll+=40
        elif self.mode=="company" and k in (pygame.K_UP,pygame.K_k): self.company_scroll=max(0,self.company_scroll-40)
        elif self.mode=="quota" and k in (pygame.K_DOWN,pygame.K_j): self.quota_scroll+=40
        elif self.mode=="quota" and k in (pygame.K_UP,pygame.K_k): self.quota_scroll=max(0,self.quota_scroll-40)
        elif k==pygame.K_l: self.show_labels=not self.show_labels
        elif k==pygame.K_v: self.show_checklist=not self.show_checklist
        elif k==pygame.K_r: r.reset_view()
        elif k==pygame.K_1 and self.mode not in ("cruise","map","ops","innov","company","quota"): r.set_view("full")
        elif k==pygame.K_2 and self.mode not in ("cruise","map","ops","innov","company","quota"): r.set_view("exploded")
        elif k==pygame.K_3 and self.mode not in ("cruise","map","ops","innov"): r.set_view("assembly")
        elif k==pygame.K_4 and self.mode not in ("cruise","map","ops","innov"): r.toggle_section()
        elif k==pygame.K_e and self.mode not in ("cruise","map","ops","innov"):
            r.set_view("exploded" if r.view!="exploded" else "full")
        elif k==pygame.K_x and self.mode not in ("cruise","map","ops","innov"): r.toggle_section()
        elif k==pygame.K_LEFTBRACKET and self.mode not in ("cruise","map","ops","innov"):
            r.set_view("assembly"); r.assembly_prev()
        elif k==pygame.K_RIGHTBRACKET and self.mode not in ("cruise","map","ops","innov"):
            r.set_view("assembly"); r.assembly_next()
        elif k==pygame.K_a and self.mode not in ("cruise","map","ops","innov"):
            r.set_view("assembly"); r.assembly_all()
        elif k==pygame.K_c and self.mode not in ("cruise","map","ops","innov"):
            r.set_view("assembly"); r.assembly_clear()
        elif k==pygame.K_COMMA: self.voyage.cycle_warp(-1)
        elif k==pygame.K_PERIOD: self.voyage.cycle_warp(+1)
        elif k==pygame.K_F1: self.pt.set_vessel_mode("DRIFT")
        elif k==pygame.K_F2: self.pt.set_vessel_mode("HARVEST")
        elif k==pygame.K_F3: self.pt.set_vessel_mode("TRANSIT")
        elif k==pygame.K_F4: self.pt.set_vessel_mode("STORM")

    def _advance_angles(self,dt):
        a=self.ang
        for key in ("ring","core","gen","fly","turbo","steam","prop","genring","default","rotor","tunnelturb"):
            a.setdefault(key,0.0)
        if self.mode in ("engine","cruise"):
            w=VIEW_ROT_SCALE*2*math.pi/60.0
            a["ring"]+=self.pt.ring_rpm*w*dt
            a["core"]+=self.pt.ring_rpm*w*dt
            a["gen"]+=self.pt.gen_rpm*w*dt
            a["fly"]+=self.pt.fly_rpm*w*0.35*dt
            a["turbo"]+=self.pt.ring_rpm*w*2.2*dt
            a["steam"]+=max(0.0,self.pt.block_temp_c-THERM["ambient_c"])*0.03*dt
        prop_rate=1.4 if self.mode=="ship" else self.pt.speed_kn*0.55
        a["prop"]+=prop_rate*dt
        a["genring"]+=(2.2 if self.pt.genset_on else 0.4)*dt
        a["default"]+=0.5*dt
        wm_rate=1.2+(self.pt.flow.get("rotor",0.0) if self.mode!="ship" else 60.0)*0.01
        a["rotor"]+=wm_rate*dt
        tt_rate=0.6+self.pt.speed_kn*0.5 if self.mode!="ship" else 3.0
        a["tunnelturb"]+=tt_rate*dt

    def _compute_firing(self,active):
        glow=np.zeros(DIMS["chambers"]); inj=np.zeros(DIMS["chambers"])
        if not active:
            self.firing_glow=glow; self.injection=inj; return
        ring_ang=self.ang.get("ring",0.0); n=DIMS["chambers"]
        for i in range(n):
            ang=i*2*math.pi/n+ring_ang
            d=abs(((ang-math.pi/2+math.pi)%(2*math.pi))-math.pi)
            glow[i]=math.exp(-(d/0.28)**2)
            di=abs(((ang-(math.pi/2+0.35)+math.pi)%(2*math.pi))-math.pi)
            inj[i]=math.exp(-(di/0.30)**2)
        self.firing_glow=glow; self.injection=inj

    def update(self,dt):
        self.rend().tick(dt)
        if self.mode=="engine":
            self.pt.update_demo(dt); self._compute_firing(True)
        elif self.mode in ("cruise","map","ops","company","quota"):
            if not self.voyage.finished:
                dt_v=self.voyage.update(dt,self.pt)
                remaining=dt_v; step_max=120.0
                while remaining>1e-6:
                    step=min(step_max,remaining)
                    self.pt.update(step,self.voyage.sun,self.voyage.sea_state)
                    self.voyage.advance_distance(self.pt.speed_kn,step)
                    remaining-=step
            self._compute_firing(self.pt.genset_on)
        else:
            self._compute_firing(False)
        self._advance_angles(dt)
        r=self.rend(); mp=pygame.mouse.get_pos()
        over_view=self.view_rect().collidepoint(mp) and not self._over_panel(mp)
        if self.mode not in ("cruise","map","ops") and over_view and not (self.dragging or self.panning):
            pass
        else:
            if not self.dragging: r.hovered=None

    def _over_panel(self,mp):
        if self.show_info or self.show_help or self.show_checklist: return True
        if mp[0]<self.LEFT_PANEL_W+4 and self.mode not in ("cruise","map","ops"): return True
        if mp[0]>self.W-self.RIGHT_PANEL_W-4 and self.mode not in ("cruise","map","ops"): return True
        if mp[1]>self.H-self.BOTTOM_BAR_H-4 and self.mode not in ("cruise","map","ops"): return True
        if mp[1]<self.TOP_BAR_H: return True
        return False

    def _handle_mode_tab_click(self,pos):
        for mode,rect in self._mode_hitboxes.items():
            if rect.collidepoint(pos): self.mode=mode; return True
        return False

    def _handle_part_list_click(self,pos):
        r=self.rend()
        for pi,rect in self._part_list_hitboxes.items():
            if rect.collidepoint(pos): r.selected=pi; return True
        return False

    def _handle_preview_click(self,pos):
        if self.mode=="cruise": return False
        if self.show_checklist: self.show_checklist=False; return True
        hit=self._preview_hitboxes
        if hit.get("labels") and hit["labels"].collidepoint(pos):
            self.show_labels=not self.show_labels; return True
        if hit.get("reset") and hit["reset"].collidepoint(pos):
            self.rend().reset_view(); return True
        if hit.get("section") and hit["section"].collidepoint(pos):
            self.rend().toggle_section(); return True
        for mode,rect in hit.get("views",[]):
            if rect.collidepoint(pos):
                if mode=="section": self.rend().toggle_section()
                elif mode in ("full","exploded","assembly"): self.rend().set_view(mode)
                else:
                    r=self.rend(); r.set_view("assembly")
                    if mode=="prev": r.assembly_prev()
                    elif mode=="next": r.assembly_next()
                    elif mode=="all": r.assembly_all()
                    elif mode=="clear": r.assembly_clear()
                return True
        return False

    def draw(self):
        self.screen.blit(self.bg,(0,0))
        if self.mode=="cruise": self.draw_cruise()
        elif self.mode=="map": self.draw_map()
        elif self.mode=="ops": self.draw_ops()
        elif self.mode=="innov": self.draw_innov()
        elif self.mode=="company": self.draw_company()
        elif self.mode=="quota": self.draw_quota()
        else: self.draw_preview()
        self.draw_topbar()
        if self.show_help: self.draw_help()
        if self.show_info: self.draw_info()
        if self.show_checklist: self.draw_checklist()
        pygame.display.flip()

    def draw_topbar(self):
        pygame.draw.rect(self.screen,C_PANEL,(0,0,self.W,self.TOP_BAR_H))
        pygame.draw.line(self.screen,C_PANEL_HI,(0,self.TOP_BAR_H),(self.W,self.TOP_BAR_H),1)
        self.screen.blit(self.fb.render("LEVIATHAN",True,C_ACCENT),(12,6))
        self.screen.blit(self.font.render("TIGER LEVIATHAN-CLASS  |  "+self.MODE_NAME[self.mode],True,C_TEXT),(172,10))
        self._mode_hitboxes={}; tab_y=4; tab_h=28
        # Center the mode tabs in the top bar
        total_tab_w=sum(self.fs.size(m.upper())[0]+24+6 for m in self.MODES)-6
        tab_x=max(200,(self.W-total_tab_w)//2)
        for mode in self.MODES:
            label=mode.upper(); active=(self.mode==mode)
            tw=self.fs.size(label)[0]+24
            rect=pygame.Rect(tab_x,tab_y,tw,tab_h)
            panel(self.screen,rect.x,rect.y,rect.w,rect.h,alpha=240 if active else 170)
            col=C_ACCENT if active else C_TEXT_DIM
            self.screen.blit(self.fs.render(label,True,col),(rect.x+12,rect.y+8))
            self._mode_hitboxes[mode]=rect; tab_x+=tw+6
        hint="H help  I info  V checklist  F11 fullscreen"
        img=self.fs.render(hint,True,C_TEXT_DIM)
        self.screen.blit(img,(self.W-img.get_width()-12,self.TOP_BAR_H+4))

    def draw_preview(self):
        r=self.rend(); rect=self.view_rect(); self._preview_hitboxes={}
        mp=pygame.mouse.get_pos()
        interactive=rect.collidepoint(mp) and not self._over_panel(mp)
        heat=clamp((self.pt.block_temp_c-THERM["ambient_c"])/110.0) if self.mode=="engine" else 0.0
        r.render(self.screen,rect,self.ang,
            firing_glow=self.firing_glow if self.mode=="engine" else None,
            mouse_pos=mp,show_labels=self.show_labels,label_font=self.fs,
            interactive=interactive,
            injection=self.injection if self.mode=="engine" else None,heat=heat)
        self.draw_view_tabs(); self.draw_part_list(); self.draw_scale_bar(rect)
        self.draw_spec_card()
        if self.mode=="ship": self.draw_ship_legend()
        elif self.mode=="engine": self.draw_engine_stats()
        elif self.mode=="hatchery": self.draw_hatchery_stats()
        self.draw_preview_footer()

    def draw_view_tabs(self):
        r=self.rend(); x,y=self.LEFT_PANEL_W+8,self.TOP_BAR_H+6
        items=[("full","1 FULL"),("exploded","2 EXPLODED"),("assembly","3 ASSEMBLY"),("section","4 SECTION")]
        views=[]; cursor=x
        for mode,label in items:
            active=r.section if mode=="section" else (r.view==mode)
            tw=self.fs.size(label)[0]+18; rect=pygame.Rect(cursor,y,tw,24)
            panel(self.screen,rect.x,rect.y,rect.w,rect.h,alpha=235 if active else 175)
            col=C_ACCENT if active else C_TEXT_DIM
            self.screen.blit(self.fs.render(label,True,col),(rect.x+9,rect.y+6))
            views.append((mode,rect)); cursor+=tw+8
        for action,label in (("prev","<"),("next",">"),("all","ALL"),("clear","CLR")):
            tw=self.fs.size(label)[0]+14; rect=pygame.Rect(cursor,y,tw,24)
            panel(self.screen,rect.x,rect.y,rect.w,rect.h,alpha=175)
            self.screen.blit(self.fs.render(label,True,C_TEXT_DIM),(rect.x+7,rect.y+6))
            views.append((action,rect)); cursor+=tw+6
        self._preview_hitboxes["views"]=views

    def draw_preview_footer(self):
        r=self.rend(); w=self.W-self.LEFT_PANEL_W-self.RIGHT_PANEL_W-16
        h=self.BOTTOM_BAR_H-8; x=self.LEFT_PANEL_W+8; y=self.H-h-4
        panel(self.screen,x,y,w,h,alpha=220)
        line1="drag orbit   right-drag pan   wheel zoom   click pin part   TAB mode"
        line2="L labels   R reset   E explode   X section   [ ] build   A all   C clear"
        self.screen.blit(self.fs.render(line1,True,C_TEXT),(x+12,y+10))
        self.screen.blit(self.fs.render(line2,True,C_TEXT_DIM),(x+12,y+30))
        line3="V checklist   I full info   H help   , / . time-warp (cruise)"
        self.screen.blit(self.fs.render(line3,True,C_TEXT_DIM),(x+12,y+50))
        labels_txt="LABELS ON" if self.show_labels else "LABELS OFF"
        reset_txt="RESET VIEW"; section_txt="CUT ON" if r.section else "CUT OFF"
        rx=x+w-240; chips=[]
        for text,key,active in ((labels_txt,"labels",self.show_labels),(section_txt,"section",r.section),(reset_txt,"reset",False)):
            tw=self.fs.size(text)[0]+16; rect=pygame.Rect(rx,y+18,tw,24)
            panel(self.screen,rect.x,rect.y,rect.w,rect.h,alpha=235 if active else 180)
            self.screen.blit(self.fs.render(text,True,C_ACCENT if active else C_TEXT),(rect.x+8,rect.y+6))
            chips.append((key,rect)); rx+=tw+8
        for key,rect in chips: self._preview_hitboxes[key]=rect

    def draw_spec_card(self):
        r=self.rend(); part=r.active_part()
        if part is None:
            if r.view=="assembly": part=r.placing_part()
            if part is None: self.draw_inspector_hint(); return
        lines=part.specs; w=self.LEFT_PANEL_W-16; body=[]
        for ln in lines: body+=wrap_text(self.fs,ln,w-28)
        h=72+len(body)*16; x,y=8,self.H-self.BOTTOM_BAR_H-h-8
        panel(self.screen,x,y,w,h)
        self.screen.blit(self.fb.render(part.name,True,C_ACCENT),(x+12,y+8))
        state="PINNED / HOVERED PART"
        if r.view=="assembly" and r.selected is None and r.hovered is None: state="NEXT PART TO PLACE"
        self.screen.blit(self.fs.render(state,True,C_TEXT_DIM),(x+14,y+34))
        yy=y+52
        for ln in body:
            self.screen.blit(self.fs.render("- "+ln,True,C_TEXT),(x+14,yy)); yy+=16

    def draw_inspector_hint(self):
        w,h=self.LEFT_PANEL_W-16,112; x,y=8,self.H-self.BOTTOM_BAR_H-h-8
        panel(self.screen,x,y,w,h)
        self.screen.blit(self.fb.render("INSPECTOR",True,C_ACCENT),(x+12,y+8))
        lines=["Hover a part to read its real dimensions and function.",
               "Click to pin the current part so it stays readable while orbiting.",
               "Use FULL / EXPLODED / ASSEMBLY / SECTION above to expose internals."]
        if self.rend().view=="assembly":
            lines[2]="Assembly mode: use [ ] or the on-screen tabs to step placement."
        yy=y+38
        for ln in lines:
            self.screen.blit(self.fs.render(ln,True,C_TEXT),(x+14,yy)); yy+=18

    def draw_ship_legend(self):
        w,x=self.RIGHT_PANEL_W-16,self.W-self.RIGHT_PANEL_W+8
        y=self.TOP_BAR_H+4; h=self.H-self.TOP_BAR_H-self.BOTTOM_BAR_H-12
        panel(self.screen,x,y,w,h)
        self.screen.blit(self.fb.render("VESSEL SPEC",True,C_TEXT),(x+12,y+8))
        rows=[("Class","Tiger Leviathan hatchery-nursery"),
            ("LOA x beam","%.0f x %.0f m"%(SHIP["loa_m"],SHIP["beam_m"])),
            ("Draft / Cb","%.0f m / %.2f"%(SHIP["draft_m"],SHIP["block_coef"])),
            ("Displacement","%.0f t"%SHIP["displacement_t"]),
            ("Hulls","%d pentamaran"%SHIP["hull_count"]),
            ("Design speed","%.0f kn (cruise 12-16)"%SHIP["design_speed_kn"]),
            ("Crew","%d"%SHIP["crew"]),("",""),
            ("Solar array","%.0f m2 @ %.0f%%"%(DIMS["solar_panel_m2"],DIMS["solar_eff"]*100)),
            ("Solar peak","%.1f MW"%(SOLAR_PEAK_KW/1000)),
            ("Electrolysis","%d tanks @ %.0f kWh/kg"%(DIMS["electro_tanks"],DIMS["electro_kwh_per_kg"])),
            ("H2 buffer","%.0f t @ %.0f bar"%(DIMS["h2_capacity_kg"]/1000,DIMS["h2_bar"])),
            ("Rotary genset","%.1f MW H2 (electric)"%(GENSET_RATED_KW/1000)),
            ("Battery bank","%.0f MWh LFP"%ELEC["batt_mwh"]),
            ("Propulsion","%d EM-rail azimuth pods"%DIMS["pods"]),("",""),
            ("Heave-oars","%d, gravity+buoyancy gen"%DIMS["heave_fins"]),
            ("Deck rotors","%d, any wind heading"%DIMS["rotors"]),
            ("Flow tunnel","bow->stern, fills the wake"),
            ("Hang weights","%d internal motion harvesters"%DIMS["weight_harvesters"]),("",""),
            ("Broodstock","%d females in %d tanks"%(DIMS["broodstock_females"],DIMS["broodstock_tanks"])),
            ("Larval tanks","%d rearing tanks"%DIMS["larval_tanks"]),
            ("Nursery pools","%d grow-out pools"%DIMS["nursery_pools"]),
            ("Release chutes","%d, DNA barcoded"%DIMS["release_chutes"]),
            ("Feed tanks","%d onboard production"%DIMS["feed_tanks"]),
            ("DNA lab","%.0f m2 CRISPR-Cas9 barcoding"%DIMS["dna_lab_m2"]),("",""),
            ("Deck railings","316L stainless, 1.1 m height"),
            ("Deck hatches","4 access hatches + cargo containers"),
            ("Bridge detail","360 deg windows, bridge wing, funnel"),
            ("Solar roof","panel grid + cross-bracing + edge trim"),("",""),
            ("Fuel","SUN + SEAWATER -> H2"),("Fuel cost","$0  (self-generated)"),("",""),
            ("INNOVATION UPGRADES",""),
            ("OTEC","3 MW 24/7 baseload"),
            ("Perovskite solar","35%% eff (was 26%%)"),
            ("Air lubrication","+12%% drag (34%% total)"),
            ("Anaerobic digester","800 kW biogas"),
            ("Floating solar rafts","+21 MW peak (drift)"),
            ("Biofloc system","50%% feed from waste"),
            ("BSF larvae","15%% feed from insects"),
            ("Yeast protein","5%% feed from H2+CO2"),
            ("IMTA seaweed","Kappaphycus polyculture"),
            ("Acoustic recapture","65%% target (was 35%%)"),
            ("Crew reduction","75 (was 150, AI autonomy)"),
            ("Partner fleet","3,500 vessels, $0.30/kg fee"),
            ("Continuous release","Trickle (+5%% survival)"),
            ("AUV fleet","8 drones, 24h, 500m depth"),
            ("Swarm AI","12-vessel coordination"),("",""),
            ("3D MODEL INNOVATIONS",""),
            ("OTEC pipe","cold-water pipe + heat exchanger"),
            ("AUV fleet bay","8 drones in stern rack"),
            ("Floating solar rafts","6 stowed modules on deck"),
            ("Comm + nav array","radar, satcom, whip antennas"),
            ("Air lube system","5 hull strips + compressor"),
            ("IMTA seaweed","4 long-lines between hulls")]
        yy=y+40
        for lab,val in rows:
            if lab=="": yy+=8; continue
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(x+12,yy))
            col=C_H2 if ("H2" in val or "SEAWATER" in val or "$0" in val) else C_TEXT
            self.screen.blit(self.fs.render(val,True,col),(x+150,yy)); yy+=19
        self.screen.blit(self.fs.render("hover/click parts  |  1 2 3 4 views  |  V checklist",
            True,C_TEXT_DIM),(x+12,y+h-24))

    def draw_engine_stats(self):
        w,x=self.RIGHT_PANEL_W-16,self.W-self.RIGHT_PANEL_W+8
        y=self.TOP_BAR_H+4; h=self.H-self.TOP_BAR_H-self.BOTTOM_BAR_H-12
        panel(self.screen,x,y,w,h)
        self.screen.blit(self.fb.render("ROTARY H2 ENGINE",True,C_CHAMBER_FIRE),(x+12,y+8))
        pt=self.pt
        rows=[("State","FIRING" if pt.genset_on else "idle"),
            ("Ring speed","%.0f rpm"%pt.ring_rpm),("Generator","%.0f rpm"%pt.gen_rpm),
            ("Flywheel","%.0f rpm"%pt.fly_rpm),("Block temp","%.0f C"%pt.block_temp_c),
            ("Rated output","%.1f MW electrical"%(GENSET_RATED_KW/1000)),
            ("Fuel","HYDROGEN (blue flame)"),("Chambers","%d, direct-injected"%DIMS["chambers"]),
            ("Steam recovery","%.0f%% of waste heat"%(STEAM_RECOVER_FRAC*100)),
            ("Output type","ELECTRICITY ONLY")]
        yy=y+42
        for lab,val in rows:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(x+12,yy))
            self.screen.blit(self.fs.render(val,True,C_TEXT),(x+132,yy)); yy+=21
        yy+=6; pygame.draw.line(self.screen,C_PANEL_HI,(x+8,yy),(x+w-8,yy),1); yy+=6
        self.screen.blit(self.fs.render("TORQUE / POWER FLOW",True,C_ACCENT),(x+12,yy)); yy+=18
        for step in ["1. H2 + air -> 8 chambers COMBUST","2. Ring spins -> wet CLUTCH engages",
            "3. Transmission RINGS step up speed","4. OUTPUT GEAR -> DIRECT CLUTCH",
            "5. Clutch disc -> drive SHAFT","6. Coupling flange -> GENERATOR",
            "7. Axial-flux gen -> DC BUS","8. DC bus -> pods + battery + electro"]:
            col=C_CHAMBER_FIRE if "COMBUST" in step else (C_ACCENT if "CLUTCH" in step else (C_H2 if "DC BUS" in step else C_TEXT))
            self.screen.blit(self.fmicro.render(step,True,col),(x+14,yy)); yy+=15
        # Innovation energy sources
        yy+=6; pygame.draw.line(self.screen,C_PANEL_HI,(x+8,yy),(x+w-8,yy),1); yy+=6
        self.screen.blit(self.fs.render("INNOVATION ENERGY SOURCES",True,C_SUN),(x+12,yy)); yy+=18
        innov_energy=[
            ("OTEC 24/7","%.0f kW (%.0f kWh)"%(pt.otec_kw,pt.otec_kwh),C_H2),
            ("Digester","%.0f kW (%.0f kWh)"%(pt.digester_kw,pt.digester_kwh),(180,220,100)),
            ("Float solar","%s (%.0f kW)"%("ON" if pt.floating_solar_deployed else "OFF",pt.flow.get("float_solar",0)),C_SUN),
            ("Perovskite","35%% eff (was 26%%)",C_SUN),
            ("Air lube","+12%% drag reduction",(100,200,255)),
        ]
        for lab,val,col in innov_energy:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(x+12,yy))
            self.screen.blit(self.fmicro.render(val,True,col),(x+132,yy)); yy+=16
        yy+=4; pygame.draw.line(self.screen,C_PANEL_HI,(x+8,yy),(x+w-8,yy),1); yy+=4
        self.screen.blit(self.fs.render("TOTAL RENEWABLE: %.0f kW (%.1f MW)"%(pt.total_renewable_kw,pt.total_renewable_kw/1000),True,C_GOOD),(x+12,yy)); yy+=16
        self.screen.blit(self.fs.render("Fuel cost: $0.00 (FREE forever)",True,C_H2),(x+12,yy))

    def draw_hatchery_stats(self):
        w,x=self.RIGHT_PANEL_W-16,self.W-self.RIGHT_PANEL_W+8
        y=self.TOP_BAR_H+4; h=self.H-self.TOP_BAR_H-self.BOTTOM_BAR_H-12
        panel(self.screen,x,y,w,h)
        self.screen.blit(self.fb.render("SHRIMP HATCHERY",True,C_SHRIMP),(x+12,y+8))
        pt=self.pt
        rows=[("Species",SHRIMP["species"]),
            ("Broodstock","%d females"%DIMS["broodstock_females"]),
            ("Maturation tanks","%d RAS tanks"%DIMS["broodstock_tanks"]),
            ("Larval tanks","%d rearing tanks"%DIMS["larval_tanks"]),
            ("Nursery pools","%d grow-out pools"%DIMS["nursery_pools"]),
            ("Release chutes","%d DNA-barcoded"%DIMS["release_chutes"]),
            ("Feed tanks","%d onboard"%DIMS["feed_tanks"]),
            ("DNA lab","%.0f m2 CRISPR-Cas9"%DIMS["dna_lab_m2"]),("",""),
            ("Eggs/year","%.1fT"%(shrimp_eggs_per_year()/1e12)),
            ("Nauplii/year","%.1fT"%(shrimp_nauplii_per_year()/1e12)),
            ("PL20/year","%.1fT"%(shrimp_pl20_per_year()/1e12)),
            ("Juveniles/year","%.0f billion"%(shrimp_juveniles_per_vessel_per_year()/1e9)),
            ("Fleet (12)","%.1f trillion"%(fleet_juveniles_per_year(12)/1e12)),("",""),
            ("Harvest biomass","%.0fM t/yr (fleet)"%(shrimp_harvest_biomass_tonnes()*12/1e6)),
            ("Feed needed","%.0fM t/yr (fleet)"%(shrimp_feed_tonnes_per_year()*12/1e6)),
            ("FCR","%.1f (algae-improved: %.1f)"%(SHRIMP["fcr"],ALGAE_FARM["fcr_with_algae"])),
            ("Revenue @ $4.85/kg","$%.1fT/yr (fleet)"%(shrimp_revenue_per_year(4.85)*12/1e12)),("",""),
            ("ALGAE FARM (FREE FEED)",""),
            ("Species","Spirulina + Chlorella + diatom"),
            ("Production","%.0f t/yr/vessel"%algae_production_t_per_year()),
            ("Fleet (12)","%.0f t/yr"%fleet_algae_production_t_per_year()),
            ("Feed replaced","%.0f%% of commercial"%ALGAE_FARM["feed_replacement_frac"]),
            ("CO2 captured","%.0f t/yr/vessel"%algae_co2_captured_t_per_year()),
            ("O2 produced","%.0f t/yr/vessel"%algae_o2_produced_t_per_year()),
            ("Feed cost","$0.00/kg (FREE, like fuel)"),
            ("Savings","$%.0fM/yr/vessel"%(algae_feed_savings_usd_per_year()/1e6)),
            ("",""),
            ("Cycle day","%.1f / 7.0"%pt.hatchery_cycle_day),
            ("Juveniles ready","%.1fB"%((pt.juveniles_produced or 0)/1e9)),
            ("Total released","%.1fB"%((pt.juveniles_released or 0)/1e9)),
            ("Release events","%d"%(pt.release_events or 0)),
            ("Feed consumed","%.0f t"%((pt.feed_consumed_kg or 0)/1000)),
            ("Algae produced","%.0f t"%((pt.algae_produced_kg or 0)/1000)),
            ("Algae to shrimp","%.0f t"%((pt.algae_to_shrimp_kg or 0)/1000)),
            ("",""),
            ("FEED SELF-SUFFICIENCY",""),
            ("Biofloc (50%%)","%.0f t"%((pt.biofloc_feed_kg or 0)/1000)),
            ("Algae feed (30%%)","%.0f t"%((pt.algae_feed_replaced_kg or 0)/1000)),
            ("BSF larvae (15%%)","%.0f t"%((pt.bsf_feed_kg or 0)/1000)),
            ("Yeast protein (5%%)","%.0f t"%((pt.yeast_feed_kg or 0)/1000)),
            ("Self-sufficiency","%.0f%% %s"%(pt.total_feed_self_sufficiency_pct,"(100%%!)" if pt.free_feed else "")),
            ("Feed cost","$0.00/kg (FREE)"),
            ("",""),
            ("IMTA SEAWEED",""),
            ("Species","Kappaphycus + Gracilaria"),
            ("Production","%.0f kg"%((pt.imta_seaweed_kg or 0))),
            ("N removed","%.0f kg"%((pt.imta_nitrogen_removed_kg or 0))),
            ("Revenue","$%.1fM"%((pt.imta_revenue_usd or 0)/1e6)),
            ("",""),
            ("BREEDING PIPELINE",""),
            ("Eggs/yr","%.1fT"%(shrimp_eggs_per_year()/1e12)),
            ("Nauplii/yr","%.1fT"%(shrimp_nauplii_per_year()/1e12)),
            ("PL20/yr","%.1fT"%(shrimp_pl20_per_year()/1e12)),
            ("Juveniles/yr","%.0fB"%(shrimp_juveniles_per_vessel_per_year()/1e9)),
            ("Fleet (12)","%.1fT juveniles"%(fleet_juveniles_per_year(12)/1e12)),
            ("",""),
            ("AI SELF-BREEDING",""),
            ("Autonomy","%s"%pt.ai_autonomy_level),
            ("Generations","%d"%pt.ai_breed_generations),
            ("Genetic gain","%.1f%%"%pt.ai_breed_genetic_gain_pct),
            ("Diversity","%.3f"%pt.ai_breed_diversity),
            ("Families tracked","%d"%pt.ai_breed_families_tracked),
            ("Traits",pt.ai_breed_improvement_summary),
            ("",""),
            ("AI SELF-MAINTAINING",""),
            ("Uptime","%.1f%%"%pt.ai_maint_uptime_pct),
            ("System health","%.1f%%"%(pt.ai_maint_avg_health*100)),
            ("Anomalies","%d detected"%pt.ai_maint_anomalies_detected),
            ("Auto-repairs","%d"%pt.ai_maint_auto_repairs),
            ("3D-printed parts","%d"%pt.ai_maint_parts_3d_printed)]
        yy=y+42
        for lab,val in rows:
            if lab=="": yy+=8; continue
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(x+12,yy))
            col=C_ALGAE if "ALGAE" in lab or "Species" in lab or "Algae" in lab or "CO2" in lab or "O2" in lab or "Feed" in lab or "Biofloc" in lab or "BSF" in lab or "Yeast" in lab or "Self-suff" in lab else (
                 (180,220,100) if "IMTA" in lab or "Seaweed" in lab or "N removed" in lab or "Revenue" in lab else (
                 C_AI_BREED if "SELF-BREEDING" in lab or "Generations" in lab or "Genetic" in lab or
                 "Diversity" in lab or "Families" in lab or "Traits" in lab else (
                 C_AI_MAINT if "SELF-MAINTAINING" in lab or "Uptime" in lab or "System health" in lab or
                 "Anomalies" in lab or "Auto-repairs" in lab or "3D-printed" in lab else (
                 C_AI if "Autonomy" in lab else (
                 C_SHRIMP if "Juveniles" in lab or "released" in lab or "Fleet" in lab or "BREEDING" in lab or
                 "Eggs" in lab or "Nauplii" in lab or "PL20" in lab else C_TEXT)))))
            self.screen.blit(self.fs.render(val,True,col),(x+150,yy)); yy+=19

    def draw_part_list(self):
        r=self.rend(); w=self.LEFT_PANEL_W-16; x=8; y=self.TOP_BAR_H+4
        h=self.H-self.TOP_BAR_H-self.BOTTOM_BAR_H-220
        if h<100: h=100
        panel(self.screen,x,y,w,h)
        self.screen.blit(self.fb.render("PARTS",True,C_ACCENT),(x+12,y+8))
        self._part_list_hitboxes={}; yy=y+36
        hi=r.selected if r.selected is not None else r.hovered
        for pi,part in enumerate(r.parts):
            active=(pi==hi); row_h=20
            if yy+row_h>y+h-4: break
            rect=pygame.Rect(x+4,yy,w-8,row_h)
            if active: panel(self.screen,rect.x,rect.y,rect.w,rect.h,alpha=235)
            elif pi%2==0: panel(self.screen,rect.x,rect.y,rect.w,rect.h,alpha=120)
            col=C_ACCENT if active else C_TEXT
            self.screen.blit(self.fmicro.render("%d"%(pi+1),True,C_TEXT_DIM),(rect.x+4,rect.y+4))
            self.screen.blit(self.fs.render(part.name,True,col),(rect.x+24,rect.y+3))
            self._part_list_hitboxes[pi]=rect; yy+=row_h

    def draw_scale_bar(self,rect):
        r=self.rend()
        disp=ENG_DISP if self.mode=="engine" else (HATCH_DISP if self.mode=="hatchery" else SHIP_DISP)
        target_px=120
        metres_per_px=1.0/(disp*min(rect.w,rect.h)*1.12/r.dist)
        target_m=target_px*metres_per_px
        magnitude=10**math.floor(math.log10(max(1.0,target_m)))
        for mult in (1,2,5,10):
            nice=mult*magnitude
            if nice>=target_m: break
        bar_m=nice; bar_px=int(bar_m*disp*min(rect.w,rect.h)*1.12/r.dist)
        bar_px=max(20,min(300,bar_px))
        bx=rect.x+12; by=rect.bottom-22
        pygame.draw.rect(self.screen,C_TEXT_DIM,(bx,by,bar_px,3))
        pygame.draw.rect(self.screen,C_TEXT_DIM,(bx,by-4,2,11))
        pygame.draw.rect(self.screen,C_TEXT_DIM,(bx+bar_px-2,by-4,2,11))
        label="%d m"%bar_m if bar_m>=1 else "%.1f m"%bar_m
        self.screen.blit(self.fs.render(label,True,C_TEXT),(bx,by-20))
        img=self.fs.render("zoom %.2f"%r.dist,True,C_TEXT_DIM)
        self.screen.blit(img,(rect.right-img.get_width()-12,rect.y+4))

    def draw_checklist(self):
        w,h=560,680; x=(self.W-w)//2; y=(self.H-h)//2
        panel(self.screen,x,y,w,h,alpha=245)
        pygame.draw.rect(self.screen,C_ACCENT,(x,y,w,h),2,border_radius=6)
        self.screen.blit(self.fbig.render("VERIFICATION CHECKLIST",True,C_ACCENT),(x+20,y+12))
        self.screen.blit(self.fs.render("V or click outside to close",True,C_TEXT_DIM),(x+20,y+48))
        items=[("Pentamaran hulls (5)","%.0f m LOA, storm mode Cat 5"%SHIP["loa_m"]),
            ("Solar cargo-roof canopy","%.0f m2 @ %.0f%% eff, %.1f MW peak"%(DIMS["solar_panel_m2"],DIMS["solar_eff"]*100,SOLAR_PEAK_KW/1000)),
            ("Rotary H2 engine","8-chamber, %.1f MW electric"%(GENSET_RATED_KW/1000)),
            ("Electrolysis / ballast tanks","%d dual-function, %.0f kWh/kg"%(DIMS["electro_tanks"],DIMS["electro_kwh_per_kg"])),
            ("Compressed H2 buffer","%d tanks @ %.0f bar, %.0f t"%(DIMS["h2_tanks"],DIMS["h2_bar"],DIMS["h2_capacity_kg"]/1000)),
            ("EM-rail azimuth pods","%d pods, %d-pole rail"%(DIMS["pods"],DIMS["rail_poles"])),
            ("Heave-oar generators","%d fins, 2-in-1 sail"%DIMS["heave_fins"]),
            ("Deck rotors","%d, any wind heading"%DIMS["rotors"]),
            ("Through-hull flow tunnel","%.0f m duct, %d turbines"%(DIMS["tunnel_len_m"],DIMS["tunnel_turbines"])),
            ("Hanging weight harvesters","%d internal bobs"%DIMS["weight_harvesters"]),
            ("Structural battery bank","%.0f MWh LFP"%ELEC["batt_mwh"]),
            ("Broodstock maturation","%d females in %d tanks"%(DIMS["broodstock_females"],DIMS["broodstock_tanks"])),
            ("Larval rearing","%d tanks, nauplii->PL20"%DIMS["larval_tanks"]),
            ("Nursery grow-out","%d pools, PL20->juvenile"%DIMS["nursery_pools"]),
            ("Release chutes","%d, DNA barcoded"%DIMS["release_chutes"]),
            ("Feed production","%d tanks, 70%% onboard"%DIMS["feed_tanks"]),
            ("DNA barcoding lab","%.0f m2 CRISPR-Cas9"%DIMS["dna_lab_m2"]),
            ("Integrated controller","$0 fuel, max %.0f kn"%MAX_CRUISE_KN),
            ("To-scale 3D + inspector","real SI dimensions, 4 views"),
            ("",""),
            ("INNOVATION UPGRADES (14)",""),
            ("OTEC 3 MW 24/7 baseload","Ocean thermal energy conversion"),
            ("Perovskite solar 35%%","+9%% efficiency over silicon"),
            ("Air lubrication -34%% drag","Micro-bubble hull coating"),
            ("Anaerobic digester 800 kW","Biogas from waste"),
            ("Floating solar rafts +21 MW","Deployed in drift mode"),
            ("Biofloc 50%% feed","Waste-to-protein conversion"),
            ("BSF larvae 15%% feed","Black soldier fly insects"),
            ("Yeast protein 5%% feed","H2+CO2 single-cell protein"),
            ("IMTA seaweed polyculture","Kappaphycus nitrogen removal"),
            ("Acoustic recapture 65%%","Conditioned recall (was 35%%)"),
            ("Crew reduction 75 (was 150)","AI autonomy replaces crew"),
            ("Partner fleet 3,500 vessels","$0.30/kg partner fee"),
            ("Continuous trickle release","+5%% survival over batch"),
            ("AUV fleet 8 drones","24h autonomous, 500m depth"),
            ("Swarm AI 12-vessel coord","Fleet-wide optimization")]
        yy=y+72
        for name,detail in items:
            pygame.draw.circle(self.screen,C_GOOD,(x+28,yy+6),5)
            self.screen.blit(self.fs.render("[x] "+name,True,C_TEXT),(x+42,yy))
            self.screen.blit(self.fmicro.render(detail,True,C_TEXT_DIM),(x+42,yy+16)); yy+=30
        self._preview_hitboxes["checklist_close"]=pygame.Rect(0,0,self.W,self.H)

    def draw_cruise(self):
        rect=self.view_rect(); v=self.voyage; pt=self.pt
        top,bot=sky_colors(v.sun); horizon=rect.y+int(rect.h*0.46)
        sky=pygame.Surface((rect.w,horizon-rect.y)); vgradient(sky,top,_mix(top,bot,0.6))
        self.screen.blit(sky,(rect.x,rect.y)); self._draw_sun_moon(rect,horizon,v)
        sea=pygame.Surface((rect.w,rect.bottom-horizon)); vgradient(sea,_mix(C_SEA2,top,0.25),C_SEA1)
        self.screen.blit(sea,(rect.x,horizon)); self._draw_sea_glints(rect,horizon,v)
        r=self.ship_rend
        stash=(r.az,r.el,r.dist,r.pan.copy(),r.view,r.section)
        bob=0.02*math.sin(pygame.time.get_ticks()/900.0)
        r.az=1.62+0.05*math.sin(pygame.time.get_ticks()/5000.0)
        r.el=0.14+bob; r.dist=2.35; r.pan=np.array([0.0,-rect.h*0.06])
        r.view,r.section="full",False
        ship_rect=pygame.Rect(rect.x,horizon-int(rect.h*0.30),rect.w,int(rect.h*0.55))
        r.render(self.screen,ship_rect,self.ang,firing_glow=None,mouse_pos=None,
            show_labels=False,label_font=None,interactive=False,injection=None,heat=0.0)
        r.az,r.el,r.dist,r.pan,r.view,r.section=stash
        # mode-specific visual effects
        if pt.is_harvesting and pt.trawl_deploy_frac>0.1:
            self._draw_trawl_net(rect,horizon,pt)
        if pt.is_drifting:
            self._draw_drift_currents(rect,horizon,pt)
        if pt.is_storm:
            self._draw_storm_weather(rect,horizon,v)
        # innovation graphics
        if pt.floating_solar_deployed and pt.is_drifting:
            self._draw_floating_solar(rect,horizon)
        self._draw_auvs(rect,horizon,pt)
        # mode transition flash
        if pt.transform_progress<1.0:
            self._draw_mode_transition(rect,pt)
        self._draw_cruise_hud(rect); self._draw_route_strip(rect)
        if v.finished: self._draw_arrived(rect)

    def _draw_sun_moon(self,rect,horizon,v):
        h=v.hour_of_day
        if 5.5<=h<=18.5:
            t=(h-5.5)/13.0; sx=rect.x+int(t*rect.w)
            sy=horizon-int(math.sin(t*math.pi)*(horizon-rect.y)*0.82)-8
            glow=pygame.Surface((120,120),pygame.SRCALPHA)
            pygame.draw.circle(glow,(255,230,150,60),(60,60),54)
            pygame.draw.circle(glow,(255,240,190,120),(60,60),30)
            self.screen.blit(glow,(sx-60,sy-60)); pygame.draw.circle(self.screen,C_SUN,(sx,sy),18)
        else:
            hm=(h+12)%24; t=clamp((hm-5.5)/13.0)
            sx=rect.x+int(t*rect.w); sy=horizon-int(math.sin(clamp(t)*math.pi)*(horizon-rect.y)*0.7)-8
            pygame.draw.circle(self.screen,(220,224,235),(sx,sy),13)
            pygame.draw.circle(self.screen,_mix(C_SKY_NIGHT1,(0,0,0),0.3),(sx+6,sy-4),12)
            rng=np.random.RandomState(7)
            for _ in range(70):
                stx=rect.x+int(rng.rand()*rect.w); sty=rect.y+int(rng.rand()*(horizon-rect.y)*0.9)
                if rng.rand()<0.5: self.screen.set_at((stx,sty),(200,210,230))

    def _draw_sea_glints(self,rect,horizon,v):
        tt=pygame.time.get_ticks()/1000.0
        col=_mix(C_SEA2,(255,255,255),0.25+0.2*v.sun)
        for i in range(26):
            y=horizon+8+i*7
            if y>rect.bottom-2: break
            amp=3+i*0.7; phase=tt*(0.6+i*0.03)
            x0=rect.x+int((math.sin(phase)*0.5+0.5)*rect.w); wlen=26+i*3
            pygame.draw.line(self.screen,_mix(C_SEA1,col,0.35),
                (max(rect.x,x0-wlen),y),(min(rect.right,x0+wlen),y),1)

    def _draw_trawl_net(self,rect,horizon,pt):
        """Draw trawl net lines extending behind/below the ship when harvesting."""
        frac=pt.trawl_deploy_frac
        if frac<0.05: return
        tt=pygame.time.get_ticks()/1000.0
        cx=rect.x+rect.w//2; cy=horizon+int(rect.h*0.08)
        net_w=int(rect.w*0.35*frac); net_h=int(rect.h*0.22*frac)
        col=(255,180,60,120)
        net_surf=pygame.Surface((net_w*2,net_h),pygame.SRCALPHA)
        # net mesh lines
        for i in range(8):
            t=i/7.0
            x1=int(t*net_w); x2=int(net_w*0.5+t*net_w*0.5)
            y1=0; y2=net_h
            pygame.draw.line(net_surf,col,(x1,y1),(x2,y2),1)
            pygame.draw.line(net_surf,col,(net_w*2-x1,y1),(net_w*2-x2,y2),1)
        for j in range(5):
            t=j/4.0
            y=int(t*net_h)
            x_l=int(t*net_w*0.5); x_r=net_w*2-int(t*net_w*0.5)
            pygame.draw.line(net_surf,col,(x_l,y),(x_r,y),1)
        self.screen.blit(net_surf,(cx-net_w,cy))
        # catch flash indicator
        if frac>0.5 and int(tt*2)%2==0:
            flash=pygame.Surface((net_w,8),pygame.SRCALPHA)
            flash.fill((255,200,80,60))
            self.screen.blit(flash,(cx-net_w//2,cy+net_h-4))

    def _draw_drift_currents(self,rect,horizon,pt):
        """Draw flowing current particles when in drift mode."""
        tt=pygame.time.get_ticks()/1000.0
        speed=pt.drift_current_kn
        col=(100,200,255,80)
        rng=np.random.RandomState(42)
        for i in range(18):
            phase=(tt*speed*0.15+i*0.37)%1.0
            x=rect.x+int(phase*rect.w)
            y=horizon+int(rng.rand()*rect.h*0.3)+10
            length=int(20+speed*8)
            pygame.draw.line(self.screen,(100,200,255),
                (x,y),(min(rect.right,x+length),y),1)
            # arrowhead
            if x+length<rect.right-5:
                pygame.draw.polygon(self.screen,(100,200,255),
                    [(x+length,y),(x+length-4,y-2),(x+length-4,y+2)])

    def _draw_storm_weather(self,rect,horizon,v):
        """Draw rain, dark overlay, and large waves for storm mode."""
        tt=pygame.time.get_ticks()/1000.0
        # dark sky overlay
        dark=pygame.Surface((rect.w,horizon-rect.y),pygame.SRCALPHA)
        dark.fill((20,20,40,100))
        self.screen.blit(dark,(rect.x,rect.y))
        # rain
        rng=np.random.RandomState(int(tt*10)%999)
        rain_col=(180,200,230,140)
        rain_surf=pygame.Surface((rect.w,rect.h),pygame.SRCALPHA)
        for _ in range(80):
            rx=int(rng.rand()*rect.w); ry=int(rng.rand()*rect.h)
            pygame.draw.line(rain_surf,rain_col,(rx,ry),(rx-3,ry+12),1)
        self.screen.blit(rain_surf,(rect.x,rect.y))
        # large waves
        for i in range(8):
            y=horizon+10+i*12
            if y>rect.bottom-2: break
            amp=8+i*2; phase=tt*(0.8+i*0.05)
            x0=rect.x+int((math.sin(phase)*0.5+0.5)*rect.w); wlen=40+i*8
            pygame.draw.line(self.screen,_mix(C_SEA1,(255,255,255),0.15),
                (max(rect.x,x0-wlen),y),(min(rect.right,x0+wlen),y),2)

    def _draw_kite_sail(self,rect,horizon):
        """Draw a high-altitude kite sail in the sky."""
        tt=pygame.time.get_ticks()/1000.0
        # kite position — high in sky, swaying
        kx=rect.x+int(rect.w*0.72+math.sin(tt*0.3)*30)
        ky=rect.y+int(rect.h*0.12+math.sin(tt*0.5)*8)
        # tether line from ship deck to kite
        ship_x=rect.x+int(rect.w*0.55)
        ship_y=horizon-int(rect.h*0.08)
        pygame.draw.line(self.screen,(200,200,210),(ship_x,ship_y),(kx,ky),1)
        # kite body (diamond shape)
        ks=18  # kite half-size
        pts=[(kx,ky-ks),(kx+ks,ky),(kx,ky+ks),(kx-ks,ky)]
        pygame.draw.polygon(self.screen,C_ACCENT,pts)
        pygame.draw.polygon(self.screen,C_TEXT,pts,1)
        # kite tail
        for i in range(5):
            tx=kx+int(math.sin(tt*0.8+i*0.5)*6)
            ty=ky+ks+4+i*5
            pygame.draw.circle(self.screen,C_ACCENT,(tx,ty),2)
        # label
        img=self.fmicro.render("KITE 2.5MW",True,C_ACCENT)
        self.screen.blit(img,(kx-ks-4,ky-ks-14))

    def _draw_floating_solar(self,rect,horizon):
        """Draw floating solar rafts around the vessel in drift mode."""
        tt=pygame.time.get_ticks()/1000.0
        # draw several raft panels on the water surface
        for i in range(6):
            base_x=rect.x+int(rect.w*(0.15+i*0.12))
            sway=int(math.sin(tt*0.4+i*1.2)*4)
            rx=base_x+sway
            ry=horizon+8+int(math.sin(tt*0.6+i)*2)
            rw=40; rh=10
            # raft body
            pygame.draw.rect(self.screen,(60,80,100),(rx,ry,rw,rh))
            # solar panels on raft (blue-ish)
            pygame.draw.rect(self.screen,(40,100,180),(rx+2,ry+2,rw-4,rh-4))
            # reflection glint
            if i%2==0:
                glint_x=rx+int(rw*0.3+math.sin(tt+i)*5)
                pygame.draw.line(self.screen,(200,220,255),(glint_x,ry+3),(glint_x+8,ry+3),1)

    def _draw_auvs(self,rect,horizon,pt):
        """Draw AUV drones underwater around the vessel."""
        if pt.auv_count==0: return
        tt=pygame.time.get_ticks()/1000.0
        deployed=min(pt.auv_deployed,pt.auv_count)
        for i in range(deployed):
            # AUVs circle below the water surface
            angle=tt*0.3+i*(2*math.pi/deployed)
            ax=rect.x+int(rect.w*0.5+math.cos(angle)*rect.w*0.18)
            ay=horizon+int(20+math.sin(angle)*rect.h*0.12)
            # AUV body (small ellipse)
            pygame.draw.ellipse(self.screen,(80,160,180),(ax-6,ay-3,12,6))
            # LED indicator
            pygame.draw.circle(self.screen,(100,255,200),(ax+4,ay),2)
            # sonar ping
            ping_r=int(8+math.sin(tt*2+i)*4)
            if ping_r>0:
                s=pygame.Surface((ping_r*2+2,ping_r*2+2),pygame.SRCALPHA)
                pygame.draw.circle(s,(100,255,200,60),(ping_r+1,ping_r+1),ping_r,1)
                self.screen.blit(s,(ax-ping_r-1,ay-ping_r-1))

    def _draw_mode_transition(self,rect,pt):
        """Draw a flash overlay with mode name during vessel transformation."""
        p=pt.transform_progress
        alpha=int(80*(1.0-p)*4.0) if p<0.25 else int(80*(1.0-p))
        alpha=max(0,min(120,alpha))
        if alpha<5: return
        vm_col={"DRIFT":(100,200,255),"HARVEST":(255,180,60),"TRANSIT":(90,200,255),"STORM":(200,80,80)}
        c=vm_col.get(pt.vessel_mode,C_TEXT)
        flash=pygame.Surface((rect.w,rect.h),pygame.SRCALPHA)
        flash.fill((c[0],c[1],c[2],alpha))
        self.screen.blit(flash,(rect.x,rect.y))
        # mode name text
        if p<0.6:
            txt=self.fbig.render(">> %s MODE <<"%pt.vessel_mode,True,c)
            tx=rect.x+rect.w//2-txt.get_width()//2
            ty=rect.y+rect.h//2-txt.get_height()//2
            self.screen.blit(txt,(tx,ty))

    def _draw_cruise_hud(self,rect):
        pt=self.pt; v=self.voyage; w,x=340,self.W-354; y=44; h=1640
        panel(self.screen,x,y,w,h)
        mode_col={"ENGINE CHARGE":C_WARN,"BOOST CRUISE":C_ACCENT,"BATTERY BOOST":C_GOOD,
            "NIGHT BATTERY":(150,160,210)}.get(pt.mode,C_H2)
        self.screen.blit(self.fb.render(pt.mode,True,mode_col),(x+12,y+8))
        clock="Day %d  %02d:%02d"%(v.day,int(v.hour_of_day),int((v.hour_of_day%1)*60))
        cimg=self.fs.render(clock,True,C_TEXT_DIM)
        self.screen.blit(cimg,(x+w-cimg.get_width()-12,y+12))
        # vessel operational mode badge
        vm_col={"DRIFT":(100,200,255),"HARVEST":(255,180,60),"TRANSIT":C_ACCENT,"STORM":(200,80,80)}
        vm_c=vm_col.get(pt.vessel_mode,C_TEXT)
        vm_txt=self.fs.render("VESSEL: %s"%pt.vessel_mode,True,vm_c)
        self.screen.blit(vm_txt,(x+12,y+30))
        if pt.transform_progress<1.0:
            tp_txt=self.fmicro.render("TRANSFORMING... %.0f%%"%(pt.transform_progress*100),True,C_WARN)
            self.screen.blit(tp_txt,(x+150,y+32))
        yy=y+52
        self.screen.blit(self.fbig.render("%.1f"%pt.speed_kn,True,C_TEXT),(x+12,yy))
        self.screen.blit(self.font.render("knots",True,C_TEXT_DIM),(x+96,yy+14))
        self.screen.blit(self.fbig.render("$0",True,C_H2),(x+190,yy))
        self.screen.blit(self.font.render("FUEL = FREE (H2 from seawater)",True,C_TEXT_DIM),(x+246,yy+14)); yy+=52
        def gbar(lab,frac,color,val):
            nonlocal yy
            bar(self.screen,self.fs,x+14,yy+14,w-30,12,frac,color,lab,val); yy+=36
        gbar("BATTERY SOC",pt.soc,C_GOOD if pt.soc>0.3 else C_WARN,"%.0f%%"%(pt.soc*100))
        gbar("H2 BUFFER",pt.h2_frac,C_H2,"%.1f t"%(pt.h2_kg/1000))
        gbar("SOLAR NOW",clamp(pt.flow["solar"]/SOLAR_PEAK_KW),C_SUN,"%.0f kW"%pt.flow["solar"])
        gbar("VOYAGE",v.progress,C_ACCENT,"%.0f / %.0f nm"%(v.distance_nm,VOYAGE["distance_nm"]))
        yy+=2; pygame.draw.line(self.screen,C_PANEL_HI,(x+12,yy),(x+w-12,yy),1); yy+=8
        flows=[("Solar in",pt.flow["solar"],C_SUN),("Genset out",pt.flow["genset"],C_WARN),
            ("Steam recovery",pt.flow["steam"],C_STEAM),("Heave-oars",pt.flow["heave"],C_GOOD),
            ("Deck rotors",pt.flow["rotor"],C_ACCENT),
            ("Tunnel turbines",pt.flow["tunnel"],C_H2),("REGEN BOOST",pt.flow["regenboost"],C_GOOD),
            ("OTEC 24/7",pt.flow.get("otec",0),C_H2),("Digester",pt.flow.get("digester",0),(180,220,100)),
            ("Float solar",pt.flow.get("float_solar",0),(255,200,80)),
            ("Electrolyser",-pt.flow["electro"],C_H2),("Propulsion",-pt.flow["prop"],C_ACCENT),
            ("Battery net",pt.flow["batt"],C_GOOD if pt.flow["batt"]>=0 else C_BAD)]
        for lab,val,col in flows:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(x+14,yy))
            img=self.fs.render("%+.0f kW"%val,True,col)
            self.screen.blit(img,(x+w-16-img.get_width(),yy)); yy+=18
        yy+=6; pygame.draw.line(self.screen,C_PANEL_HI,(x+12,yy),(x+w-12,yy),1); yy+=8
        eta_h=(VOYAGE["distance_nm"]-v.distance_nm)/max(0.5,pt.speed_kn)
        stats=[("Engine-off time","%.0f%%"%(pt.engine_off_frac*100)),
            ("H2 self-made","%.0f%%"%(pt.h2_selfsuff*100)),
            ("H2 produced","%.1f t"%(pt.h2_made/1000)),
            ("H2 burned","%.1f t"%(pt.h2_used/1000)),
            ("Solar harvested","%.1f MWh"%(pt.solar_kwh/1000)),
            ("Sail assist","%.1f MWh"%(pt.sail_kwh/1000)),
            ("Motion harvest","%.1f MWh"%(pt.harvest_kwh/1000)),
            ("ETA remaining","%.1f days"%(eta_h/24.0)),
            ("Sea state","%.0f%%  weather %.0f%%"%(v.sea_state*100,v.weather*100)),
            ("Wind","%.1f m/s %s"%(AMBIENT_WIND_MS,"SAILS DEPLOYED" if pt.flow["sail"]>0.1 else "furled")),
            ("Time warp","x%.0f"%v.warp),("",""),
            ("FREE FUEL (SE.py rotary H2)",""),
            ("Fuel bill","$0.00 (FREE)"),
            ("H2 self-sufficiency","%.1f%%"%(pt.h2_selfsuff*100)),
            ("H2 round-trip eff","%.0f%%"%(pt.h2_round_trip_eff*100)),
            ("Diesel saved","$%.1fM"%((pt.free_fuel_savings_usd or 0)/1e6)),
            ("Engine-off time","%.0f%% of voyage"%(pt.engine_off_frac*100)),
            ("",""),
            ("SHRIMP PRODUCTION",""),("Juveniles ready","%.1fB"%((pt.juveniles_produced or 0)/1e9)),
            ("Total released","%.1fB"%((pt.juveniles_released or 0)/1e9)),
            ("Release events","%d"%(pt.release_events or 0)),
            ("Feed consumed","%.0f t"%((pt.feed_consumed_kg or 0)/1000)),
            ("Cycle day","%.1f / 7.0"%(pt.hatchery_cycle_day or 0)),
            ("",""),
            ("ALGAE FARM (FREE FEED)",""),
            ("Species","Spirulina + Chlorella + diatom"),
            ("Algae produced","%.0f t"%((pt.algae_produced_kg or 0)/1000)),
            ("Algae harvested","%.0f t"%((pt.algae_harvested_kg or 0)/1000)),
            ("Fed to shrimp","%.0f t"%((pt.algae_to_shrimp_kg or 0)/1000)),
            ("Algae storage","%.0f t"%((pt.algae_storage_kg or 0)/1000)),
            ("Feed replaced","%.0f%% commercial"%(pt.algae_feed_coverage*100)),
            ("Growth rate","%.1f g/m2/day"%pt.algae_growth_rate),
            ("LED supplement","ON (night)" if pt.algae_led_on else "OFF (day)"),
            ("CO2 captured","%.0f t"%((pt.algae_co2_captured_kg or 0)/1000)),
            ("O2 produced","%.0f t"%((pt.algae_o2_produced_kg or 0)/1000)),
            ("Feed savings","$%.1fM"%((pt.algae_feed_savings_usd or 0)/1e6)),
            ("Feed cost","$0.00/kg (FREE, like fuel)"),
            ("",""),
            ("INNOVATION SYSTEMS",""),
            ("OTEC power","%.1f MWh (%.0f kW 24/7)"%(pt.otec_kwh/1000,pt.otec_kw)),
            ("Digester power","%.1f MWh (%.0f kW)"%(pt.digester_kwh/1000,pt.digester_kw)),
            ("Float solar","%.0f kW %s"%(pt.floating_solar_kw,"ON" if pt.floating_solar_deployed else "OFF")),
            ("Total renewable","%.0f kW"%pt.total_renewable_kw),
            ("",""),
            ("FEED SELF-SUFFICIENCY",""),
            ("Biofloc (50%%)","%.0f t"%((pt.biofloc_feed_kg or 0)/1000)),
            ("Algae (30%%)","%.0f t"%((pt.algae_feed_replaced_kg or 0)/1000)),
            ("BSF larvae (15%%)","%.0f t"%((pt.bsf_feed_kg or 0)/1000)),
            ("Yeast protein (5%%)","%.0f t"%((pt.yeast_feed_kg or 0)/1000)),
            ("Self-sufficiency","%.0f%% %s"%(pt.total_feed_self_sufficiency_pct,"(100%%!)" if pt.free_feed else "")),
            ("",""),
            ("IMTA SEAWEED",""),
            ("Seaweed produced","%.0f kg"%((pt.imta_seaweed_kg or 0))),
            ("N removed","%.0f kg"%((pt.imta_nitrogen_removed_kg or 0))),
            ("IMTA revenue","$%.1fM"%((pt.imta_revenue_usd or 0)/1e6)),
            ("",""),
            ("AUV & SWARM",""),
            ("AUVs deployed","%d / %d"%(pt.auv_deployed,pt.auv_count)),
            ("Swarm decisions","%d"%pt.swarm_decisions),
            ("Continuous release","%s (%.0fM/hr)"%("ON" if pt.continuous_release_active else "OFF",CONTINUOUS_RELEASE["release_rate_per_hour"]/1e6)),
            ("Acoustic recapture","%s (+%.0f%%)"%("ON" if pt.acoustic_conditioning_active else "OFF",ACOUSTIC_RECAPTURE["recapture_boost_pct"])),
            ("Partner vessels","%d"%pt.partner_vessels_active),
            ("",""),
            ("CATCH & PROCESSING",""),
            ("Catch (session)","%.0f t"%((pt.catch_kg or 0)/1000)),
            ("Catch (total)","%.0f t"%((pt.catch_total_kg or 0)/1000)),
            ("Frozen","%.0f t"%((pt.catch_frozen_kg or 0)/1000)),
            ("Packaged","%.0f t"%((pt.catch_packaged_kg or 0)/1000)),
            ("Bycatch discarded","%.0f t"%((pt.catch_bycatch_kg or 0)/1000)),
            ("Catch revenue","$%.1fM"%((pt.catch_revenue_usd or 0)/1e6)),
            ("",""),
            ("RECAPTURE & DNA",""),
            ("Recapture rate","%.1f%% (target 65%%)"%((pt.recapture_frac or 0)*100)),
            ("DNA barcoded batches","%d"%(pt.dna_barcoded_batches or 0)),
            ("Recapture value","$%.2fT"%((pt.recapture_value_usd or 0)/1e12)),
            ("",""),
            ("VESSEL MODE STATS",""),
            ("Hull coating","SUPERHYDROPHOBIC" if pt.superhydrophobic_on else "standard"),
            ("Trawl deployed","%.0f%%"%(pt.trawl_deploy_frac*100)),
            ("Drift current","%.1f kn"%pt.drift_current_kn),
            ("Minimal sail","%.0f%%"%(pt.sail_minimal_frac*100)),
            ("Storm ballast","%.0f%%"%(pt.storm_ballast_frac*100)),
            ("",""),
            ("INVESTMENT & FINANCE",""),
            ("Investment","$%.1fB"%(FINANCE["investment_usd"]/1e9)),
            ("Fleet vessels","%d / %d"%(pt.fleet_vessels,FINANCE["fleet_target"])),
            ("Shrimp revenue","$%.2fB"%((pt.total_revenue_usd or 0)/1e9)),
            ("Carbon credits","$%.1fM"%((pt.carbon_credit_usd or 0)/1e6)),
            ("Tech licensing","$%.1fM"%((pt.tech_license_usd or 0)/1e6)),
            ("Data sales","$%.1fM"%((pt.data_sales_usd or 0)/1e6)),
            ("Total revenue","$%.2fB"%(((pt.total_revenue_usd or 0)+(pt.carbon_credit_usd or 0)+(pt.tech_license_usd or 0)+(pt.data_sales_usd or 0))/1e9)),
            ("Target valuation","$%.0fB (Year %d)"%(FINANCE["target_valuation_usd"]/1e9,FINANCE["target_years"])),
            ("",""),
            ("AI SYSTEMS (AUTONOMOUS)",""),
            ("Autonomy level","%s"%pt.ai_autonomy_level),
            ("Orchestrator","ACTIVE (DGX H100 x2)" if pt.ai_orchestrator_active else "OFFLINE"),
            ("Total AI decisions","%d"%pt.ai_total_decisions),
            ("Model updates","%d (federated)"%pt.ai_model_updates),
            ("",""),
            ("SELF-DRIVING",""),
            ("Status","ACTIVE" if pt.ai_drive_active else "OFFLINE"),
            ("Route optimizations","%d"%pt.ai_route_optimizations),
            ("Collision avoidances","%d"%pt.ai_collision_avoidances),
            ("Weather reroutes","%d"%pt.ai_weather_reroutes),
            ("Auto mode switches","%d"%pt.ai_auto_mode_switches),
            ("Drive confidence","%.0f%%"%pt.ai_drive_confidence),
            ("",""),
            ("SELF-BREEDING",""),
            ("Status","ACTIVE" if pt.ai_breed_active else "OFFLINE"),
            ("Generations","%d"%pt.ai_breed_generations),
            ("Genetic gain","%.1f%%"%pt.ai_breed_genetic_gain_pct),
            ("Diversity","%.3f (target >0.35)"%pt.ai_breed_diversity),
            ("Inbreeding","%.3f (max 0.125)"%pt.ai_breed_inbreeding),
            ("Families tracked","%d"%pt.ai_breed_families_tracked),
            ("Trait improvements",pt.ai_breed_improvement_summary),
            ("Egg quality score","%.1f%%"%(pt.ai_breed_egg_quality_score*100)),
            ("",""),
            ("SELF-HERDING",""),
            ("Status","ACTIVE" if pt.ai_herd_active else "OFFLINE"),
            ("Schools tracked","%d"%pt.ai_herd_schools_tracked),
            ("Recapture predictions","%d"%pt.ai_herd_recapture_predictions),
            ("Predator alerts","%d"%pt.ai_herd_predator_alerts),
            ("Fleet contracts","%d"%pt.ai_herd_fleet_contracts),
            ("Drones active","%d / %d"%(pt.ai_herd_drones_active,AI_SYSTEMS["self_herding"]["drone_swarm_count"])),
            ("eDNA samples","%d"%pt.ai_herd_edna_samples),
            ("Migration patterns","%d learned"%pt.ai_herd_migration_patterns_learned),
            ("Tracking accuracy","%.0f%%"%pt.ai_herd_tracking_accuracy),
            ("",""),
            ("SELF-MAINTAINING",""),
            ("Status","ACTIVE" if pt.ai_maint_active else "OFFLINE"),
            ("Uptime","%.1f%%"%pt.ai_maint_uptime_pct),
            ("Avg system health","%.1f%%"%(pt.ai_maint_avg_health*100)),
            ("Predictions made","%d"%pt.ai_maint_predictions),
            ("Anomalies detected","%d"%pt.ai_maint_anomalies_detected),
            ("Repairs scheduled","%d"%pt.ai_maint_repairs_scheduled),
            ("Auto-repairs","%d"%pt.ai_maint_auto_repairs),
            ("Repairs completed","%d"%pt.ai_maint_repairs_completed),
            ("3D-printed parts","%d"%pt.ai_maint_parts_3d_printed),
            ("Sensor readings","%.1fM"%((pt.ai_maint_sensor_readings or 0)/1e6)),
            ("",""),
            ("CONTROLS",""),
            ("F1-F4","DRIFT/HARVEST/TRANSIT/STORM")]
        for lab,val in stats:
            if lab=="": yy+=8; continue
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(x+14,yy))
            col=C_SHRIMP if "SHRIMP" in lab or "Juveniles" in lab or "released" in lab else (
                 C_ALGAE if "ALGAE" in lab or "Species" in lab or "Algae" in lab or
                 "Fed to" in lab or "Growth" in lab or "LED" in lab or "CO2" in lab or
                 "O2" in lab or "Feed" in lab else (
                 C_AI if "AI SYSTEMS" in lab or "Autonomy" in lab or "Orchestrator" in lab or
                 "Total AI" in lab or "Model" in lab or "Status" in lab or "Uptime" in lab or
                 "Avg system" in lab or "Predictions" in lab or "Anomalies" in lab or
                 "Repairs" in lab or "Auto-repairs" in lab or "3D-printed" in lab or
                 "Sensor" in lab else (
                 C_AI_DRIVE if "SELF-DRIVING" in lab or "Route" in lab or "Collision" in lab or
                 "Weather" in lab or "Auto mode" in lab or "Drive confidence" in lab else (
                 C_AI_BREED if "SELF-BREEDING" in lab or "Generations" in lab or "Genetic" in lab or
                 "Diversity" in lab or "Inbreeding" in lab or "Families" in lab or
                 "Trait" in lab or "Egg" in lab else (
                 C_AI_HERD if "SELF-HERDING" in lab or "Schools" in lab or "Recapture" in lab or
                 "Predator" in lab or "Fleet" in lab or "Drones" in lab or
                 "eDNA" in lab or "Migration" in lab or "Tracking" in lab else (
                 C_AI_MAINT if "SELF-MAINTAINING" in lab else (
                 C_H2 if "FREE FUEL" in lab or "Fuel" in lab or "H2" in lab or "Diesel" in lab or "Engine-off" in lab else (
                 (255,180,60) if "CATCH" in lab or "Frozen" in lab or "Packaged" in lab or
                 "Bycatch" in lab or "Catch" in lab else (
                 (180,100,220) if "RECAPTURE" in lab or "DNA" in lab or "Recapture" in lab else (
                 (100,220,130) if "INVESTMENT" in lab or "Investment" in lab or "Fleet" in lab or
                 "revenue" in lab or "Carbon" in lab or "Tech" in lab or "Data" in lab or
                 "Total" in lab or "Target" in lab or "valuation" in lab else (
                 (100,200,255) if "VESSEL MODE" in lab or "Hull" in lab or "Trawl" in lab or
                 "Drift" in lab or "sail" in lab or "ballast" in lab else (
                 C_ACCENT if "CONTROLS" in lab or "F1-F4" in lab else C_TEXT))))))))))))
            img=self.fs.render(val,True,col)
            self.screen.blit(img,(x+w-16-img.get_width(),yy)); yy+=18

    def _draw_route_strip(self,rect):
        v=self.voyage; y=rect.bottom-30; x0,x1=40,self.W-380
        pygame.draw.line(self.screen,C_TEXT_DIM,(x0,y),(x1,y),2)
        for xx,lab in ((x0,VOYAGE["origin"]),(x1,VOYAGE["dest"])):
            pygame.draw.circle(self.screen,C_ACCENT,(xx,y),5)
        self.screen.blit(self.fs.render(VOYAGE["origin"],True,C_TEXT),(x0-8,y+8))
        img=self.fs.render(VOYAGE["dest"],True,C_TEXT)
        self.screen.blit(img,(x1-img.get_width()+8,y+8))
        sx=int(x0+v.progress*(x1-x0))
        pygame.draw.circle(self.screen,C_H2,(sx,y),7)
        pygame.draw.circle(self.screen,C_TEXT,(sx,y),7,1)
        pct=self.fs.render("%.0f%%"%(v.progress*100),True,C_H2)
        self.screen.blit(pct,(sx-pct.get_width()//2,y-20))

    def _draw_arrived(self,rect):
        pt=self.pt
        w,h=560,460; x=rect.x+(rect.w-w)//2; y=rect.y+(rect.h-h)//2-40
        panel(self.screen,x,y,w,h,alpha=235)
        self.screen.blit(self.fbig.render("ARRIVED -- RELEASE ZONE",True,C_H2),(x+24,y+18))
        dt_t,dt_c=_diesel_ref()
        lines=["%.0f nm transit on self-made hydrogen (FREE FUEL)."%VOYAGE["distance_nm"],
            "Fuel cost: $0    (a diesel ship: ~$%s)"%f"{dt_c:,.0f}",
            "Engine-off %.0f%% of the voyage. H2 self-sufficiency: %.0f%%."%(pt.engine_off_frac*100,pt.h2_selfsuff*100),
            "",
            "Shrimp released: %.1fB juveniles (%d release events)"%((pt.juveniles_released or 0)/1e9,pt.release_events or 0),
            "Catch harvested: %.0f t  Revenue: $%.1fM"%((pt.catch_total_kg or 0)/1000,(pt.catch_revenue_usd or 0)/1e6),
            "Recapture rate: %.1f%%  DNA batches: %d"%((pt.recapture_frac or 0)*100,pt.dna_barcoded_batches or 0),
            "",
            "Algae feed produced: %.0f t (FREE via photosynthesis)"%((pt.algae_produced_kg or 0)/1000),
            "Feed replaced: %.0f%%  CO2 captured: %.0f t  O2 produced: %.0f t"%(
                pt.algae_feed_coverage*100,(pt.algae_co2_captured_kg or 0)/1000,(pt.algae_o2_produced_kg or 0)/1000),
            "",
            "AI: %s | %d decisions | Uptime %.1f%%"%(
                pt.ai_autonomy_level,pt.ai_total_decisions,pt.ai_maint_uptime_pct),
            "Self-breeding: gen %d, gain %.1f%%, diversity %.3f"%(
                pt.ai_breed_generations,pt.ai_breed_genetic_gain_pct,pt.ai_breed_diversity),
            "Self-herding: %d schools tracked, %d recapture predictions"%(
                pt.ai_herd_schools_tracked,pt.ai_herd_recapture_predictions),
            "Self-maintaining: %d auto-repairs, %d 3D-printed parts"%(
                pt.ai_maint_auto_repairs,pt.ai_maint_parts_3d_printed),
            "",
            "Fleet revenue: $%.2fB  Target: $%.0fB (Year %d)"%(
                ((pt.total_revenue_usd or 0)+(pt.carbon_credit_usd or 0)+(pt.tech_license_usd or 0)+(pt.data_sales_usd or 0))/1e9,
                FINANCE["target_valuation_usd"]/1e9,FINANCE["target_years"])]
        for i,ln in enumerate(lines):
            col=C_H2 if "FREE FUEL" in ln else (C_SHRIMP if "Shrimp" in ln else (
                 C_ALGAE if "Algae" in ln or "Feed" in ln or "CO2" in ln else (
                 C_AI if "AI:" in ln or "Self-" in ln else (
                 (100,220,130) if "Fleet" in ln or "revenue" in ln else C_TEXT))))
            self.screen.blit(self.font.render(ln,True,col),(x+24,y+58+i*24))

    def _latlon_to_screen(self,lat,lon,rect):
        """Convert lat/lon to screen coordinates in the given rect."""
        x=rect.x+int((lon+180)/360*rect.w)
        y=rect.y+int((90-lat)/180*rect.h)
        return (x,y)

    def draw_innov(self):
        rect=self.view_rect(); pt=self.pt
        pygame.draw.rect(self.screen,C_PANEL,rect)
        self.screen.blit(self.fbig.render("14 INNOVATION UPGRADES",True,C_ACCENT),(rect.x+20,rect.y+8))
        self.screen.blit(self.fs.render("Cost reduction + efficiency optimization  |  TAB to cycle",True,C_TEXT_DIM),(rect.x+20,rect.y+42))
        # ---- Layout: 3 columns ----
        col_w=(rect.w-60)//3
        col1_x=rect.x+12; col2_x=col1_x+col_w+12; col3_x=col2_x+col_w+12
        top_y=rect.y+68
        # ==================== COLUMN 1: ENERGY SYSTEMS ====================
        pw=col_w; ph=rect.h-90
        panel(self.screen,col1_x,top_y,pw,ph,alpha=230)
        self.screen.blit(self.fb.render("ENERGY (24/7, $0 fuel)",True,C_SUN),(col1_x+12,top_y+8))
        yy=top_y+36
        energy_items=[
            ("1. OTEC","3 MW 24/7 baseload","%.0f kWh"%(pt.otec_kwh),C_H2),
            ("2. Perovskite","35%% eff (was 26%%)","%.0f kW"%(pt.flow.get("solar",0)),C_SUN),
            ("3. Air Lube","12%% drag cut","+34%% total drag",(100,200,255)),
            ("6. Digester","800 kW biogas","%.0f kWh"%(pt.digester_kwh),(180,220,100)),
            ("13. Float Solar","+21 MW drift","%s"%( "ON" if pt.floating_solar_deployed else "OFF"),C_SUN),
        ]
        for name,desc,val,col in energy_items:
            self.screen.blit(self.fs.render(name,True,col),(col1_x+12,yy))
            self.screen.blit(self.fmicro.render(desc,True,C_TEXT_DIM),(col1_x+12,yy+16))
            img=self.fmicro.render(val,True,C_TEXT)
            self.screen.blit(img,(col1_x+pw-16-img.get_width(),yy+4))
            yy+=36
        # Energy bar chart
        yy+=8; self.screen.blit(self.fs.render("POWER OUTPUT (kW)",True,C_ACCENT),(col1_x+12,yy)); yy+=20
        sources=[
            ("Solar",pt.flow.get("solar",0),C_SUN),
            ("OTEC",pt.otec_kw,C_H2),
            ("Digester",pt.digester_kw,(180,220,100)),
            ("Float Solar",pt.flow.get("float_solar",0),(255,200,80)),
            ("Heave",pt.flow.get("heave",0),C_GOOD),
            ("Rotor",pt.flow.get("rotor",0),(150,200,255)),
        ]
        max_kw=max([s[1] for s in sources]+[1])
        bar_w=pw-80
        for name,kw,col in sources:
            self.screen.blit(self.fmicro.render(name,True,C_TEXT_DIM),(col1_x+12,yy))
            frac=kw/max_kw
            pygame.draw.rect(self.screen,C_PANEL_HI,(col1_x+70,yy+2,bar_w,10))
            pygame.draw.rect(self.screen,col,(col1_x+70,yy+2,int(bar_w*frac),10))
            img=self.fmicro.render("%.0f"%kw,True,C_TEXT)
            self.screen.blit(img,(col1_x+72+bar_w-img.get_width(),yy+2))
            yy+=16
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        total_kw=pt.total_renewable_kw
        self.screen.blit(self.fs.render("TOTAL RENEWABLE: %.0f kW (%.1f MW)"%(total_kw,total_kw/1000),True,C_GOOD),(col1_x+12,yy)); yy+=22
        self.screen.blit(self.fs.render("Fuel cost: $0.00 (FREE forever)",True,C_H2),(col1_x+12,yy)); yy+=22
        # ==================== COLUMN 2: FEED & BIOLOGY ====================
        panel(self.screen,col2_x,top_y,pw,ph,alpha=230)
        self.screen.blit(self.fb.render("FEED (100%% self-sufficient)",True,C_ALGAE),(col2_x+12,top_y+8))
        yy=top_y+36
        # Feed self-sufficiency breakdown bar
        self.screen.blit(self.fs.render("FEED COMPOSITION:",True,C_ACCENT),(col2_x+12,yy)); yy+=20
        feed_segs=[
            ("Biofloc 50%%",50.0,(180,220,100)),
            ("Algae 30%%",30.0,C_ALGAE),
            ("BSF 15%%",15.0,(220,180,80)),
            ("Yeast 5%%",5.0,(200,160,220)),
        ]
        seg_x=col2_x+12; seg_w=pw-24; seg_y=yy
        for label,pct,col in feed_segs:
            w=int(seg_w*pct/100.0)
            pygame.draw.rect(self.screen,col,(seg_x,seg_y,w,16))
            seg_x+=w
        yy+=22
        for label,pct,col in feed_segs:
            pygame.draw.rect(self.screen,col,(col2_x+12,yy,8,8))
            self.screen.blit(self.fmicro.render(label,True,C_TEXT),(col2_x+26,yy-2))
            yy+=16
        yy+=8
        self.screen.blit(self.fs.render("Self-sufficiency: %.0f%% %s"%(pt.total_feed_self_sufficiency_pct,"(100%%!)" if pt.free_feed else ""),True,C_GOOD),(col2_x+12,yy)); yy+=24
        # Feed production amounts
        feed_items=[
            ("Biofloc (waste->protein)","%.0f t"%(pt.biofloc_feed_kg/1000)),
            ("Algae (sun+CO2)","%.0f t"%(pt.algae_feed_replaced_kg/1000)),
            ("BSF larvae (waste->insects)","%.0f t"%(pt.bsf_feed_kg/1000)),
            ("Yeast (H2+CO2->protein)","%.0f t"%(pt.yeast_feed_kg/1000)),
            ("Total feed replaced","%.0f t"%(pt.total_feed_replaced_kg/1000)),
            ("Feed consumed","%.0f t"%(pt.feed_consumed_kg/1000)),
            ("Feed cost","$0.00/kg (FREE)"),
        ]
        for lab,val in feed_items:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(col2_x+12,yy))
            img=self.fs.render(val,True,C_ALGAE if "FREE" in val else C_TEXT)
            self.screen.blit(img,(col2_x+pw-16-img.get_width(),yy)); yy+=18
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # IMTA seaweed
        self.screen.blit(self.fs.render("IMTA SEAWEED POLYCULTURE",True,C_ACCENT),(col2_x+12,yy)); yy+=20
        imta_items=[
            ("Species","Kappaphycus + Gracilaria"),
            ("Production","%.0f kg"%(pt.imta_seaweed_kg)),
            ("N removed","%.0f kg"%(pt.imta_nitrogen_removed_kg)),
            ("Revenue","$%.1fM"%(pt.imta_revenue_usd/1e6)),
            ("CO2 sequestered","480 t/yr (target)"),
        ]
        for lab,val in imta_items:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(col2_x+12,yy))
            self.screen.blit(self.fs.render(val,True,C_TEXT),(col2_x+pw-16-self.fs.size(val)[0],yy)); yy+=18
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # Shrimp breeding pipeline
        self.screen.blit(self.fs.render("SHRIMP BREEDING PIPELINE",True,C_SHRIMP),(col2_x+12,yy)); yy+=20
        pipeline=[
            ("Eggs","%.1fT/yr"%(shrimp_eggs_per_year()/1e12)),
            ("Nauplii","%.1fT/yr"%(shrimp_nauplii_per_year()/1e12)),
            ("PL20","%.1fT/yr"%(shrimp_pl20_per_year()/1e12)),
            ("Juveniles","%.0fB/yr"%(shrimp_juveniles_per_vessel_per_year()/1e9)),
            ("Released","%.1fB"%(pt.juveniles_released/1e9)),
        ]
        for i,(lab,val) in enumerate(pipeline):
            col=C_SHRIMP if i==len(pipeline)-1 else C_TEXT_DIM
            self.screen.blit(self.fs.render(lab,True,col),(col2_x+12,yy))
            self.screen.blit(self.fs.render(val,True,C_TEXT),(col2_x+pw-16-self.fs.size(val)[0],yy))
            if i<len(pipeline)-1:
                self.screen.blit(self.fmicro.render("  ->",True,C_TEXT_DIM),(col2_x+90,yy))
            yy+=18
        # ==================== COLUMN 3: OPERATIONAL SYSTEMS ====================
        panel(self.screen,col3_x,top_y,pw,ph,alpha=230)
        self.screen.blit(self.fb.render("OPERATIONS & FLEET",True,C_AI),(col3_x+12,top_y+8))
        yy=top_y+36
        ops_items=[
            ("8. Acoustic Recapture","35%% -> 65%% (+30%% harvest)","%s"%( "ON" if pt.acoustic_conditioning_active else "OFF"),(180,100,220)),
            ("9. Crew Reduction","150 -> 75 (AI autonomy)","$126M/yr fleet saved",(100,200,255)),
            ("10. Partner Fleet","1,200 AI + 3,500 partner","$45.6B AI trawler fleet",C_GOOD),
            ("11. Continuous Release","Trickle vs batch (+5%% surv)","%s"%( "ON" if pt.continuous_release_active else "OFF"),C_SHRIMP),
            ("14. AUV Fleet","8 drones, 24h, 500m depth","%d / %d deployed"%(pt.auv_deployed,pt.auv_count),(100,220,200)),
            ("15. Swarm AI","12-vessel coordination","%d decisions"%pt.swarm_decisions,C_AI),
        ]
        for name,desc,val,col in ops_items:
            self.screen.blit(self.fs.render(name,True,col),(col3_x+12,yy))
            self.screen.blit(self.fmicro.render(desc,True,C_TEXT_DIM),(col3_x+12,yy+16))
            img=self.fmicro.render(val,True,C_TEXT)
            self.screen.blit(img,(col3_x+pw-16-img.get_width(),yy+4))
            yy+=36
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # Combined savings summary
        self.screen.blit(self.fs.render("COMBINED SAVINGS",True,C_ACCENT),(col3_x+12,yy)); yy+=20
        savings=[
            ("CAPEX saved","$45.6B (partner fleet)"),
            ("OPEX saved/yr","$4.5B+ (fuel+feed+crew)"),
            ("Feed cost","$0 (100%% self-sufficient)"),
            ("Fuel cost","$0 (solar+OTEC+kite)"),
            ("Revenue boost","+35%% (recapture)"),
            ("IMTA revenue","+$43.2M/yr fleet"),
        ]
        for lab,val in savings:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(col3_x+12,yy))
            col=C_GOOD if "$0" in val or "$45" in val or "+35" in val or "+$" in val else C_TEXT
            self.screen.blit(self.fs.render(val,True,col),(col3_x+pw-16-self.fs.size(val)[0],yy)); yy+=18
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # Live simulation stats
        self.screen.blit(self.fs.render("LIVE SIMULATION DATA",True,C_AI),(col3_x+12,yy)); yy+=20
        live=[
            ("Mode","%s"%pt.vessel_mode),
            ("Speed","%.1f kn"%pt.speed_kn),
            ("Battery SOC","%.0f%%"%(pt.soc*100)),
            ("H2 buffer","%.1f t"%(pt.h2_kg/1000)),
            ("Free fuel","%s"%pt.free_fuel),
            ("Free feed","%s"%pt.free_feed),
            ("Total renewable","%.1f MW"%(pt.total_renewable_kw/1000)),
            ("Juveniles produced","%.1fB"%(pt.juveniles_produced/1e9)),
            ("Continuous release","%.0fM/hr"%(CONTINUOUS_RELEASE["release_rate_per_hour"]/1e6)),
            ("Swarm decisions","%d"%pt.swarm_decisions),
        ]
        for lab,val in live:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(col3_x+12,yy))
            col=C_GOOD if val in ("True","DRIFT") else C_TEXT
            self.screen.blit(self.fs.render(val,True,col),(col3_x+pw-16-self.fs.size(val)[0],yy)); yy+=18

    def draw_map(self):
        rect=self.view_rect(); pt=self.pt; v=self.voyage
        # Ocean background with depth gradient
        pygame.draw.rect(self.screen,C_MAP_OCEAN,rect)
        # Grid lines (lat/lon) with labels
        for lat in range(-60,90,30):
            y=self._latlon_to_screen(lat,0,rect)[1]
            pygame.draw.line(self.screen,C_MAP_GRID,(rect.x,y),(rect.right,y),1)
            img=self.fmicro.render("%d°"%lat,True,C_TEXT_DIM)
            self.screen.blit(img,(rect.x+4,y+2))
        for lon in range(-180,180,30):
            x=self._latlon_to_screen(0,lon,rect)[0]
            pygame.draw.line(self.screen,C_MAP_GRID,(x,rect.y),(x,rect.bottom),1)
            img=self.fmicro.render("%d°"%lon,True,C_TEXT_DIM)
            self.screen.blit(img,(x+2,rect.bottom-14))
        # Draw more detailed continents (multi-rect approximations)
        continents=[
            # North America
            (72,-160,18,50),(60,-130,12,40),(45,-125,15,35),(30,-115,15,20),
            (15,-105,15,20),  # Central America
            # South America
            (10,-80,15,25),(-15,-75,15,25),(-35,-70,15,20),(-55,-70,10,15),
            # Europe
            (70,-10,15,25),(55,-5,12,20),(45,5,10,15),
            # Africa
            (35,-10,15,20),(20,0,15,25),(5,10,10,20),(-15,15,15,20),(-30,18,12,15),
            # Asia
            (70,30,15,60),(55,40,15,50),(40,50,15,40),(25,60,15,40),(10,70,15,30),
            # Southeast Asia / Indonesia
            (5,95,10,20),(-5,105,10,20),(-10,115,10,15),
            # Australia
            (-12,115,10,15),(-25,120,12,20),(-35,125,10,15),(-40,140,8,12),
            # Greenland
            (75,-50,10,20),(65,-45,8,15),
            # Japan
            (45,135,6,8),(35,137,5,7),
            # UK / Ireland
            (55,-8,5,8),
            # Madagascar
            (-15,47,8,6),(-25,47,8,6),
            # New Zealand
            (-38,170,5,8),(-45,168,4,6),
        ]
        for clat,clon,cw,ch in continents:
            cx,cy=self._latlon_to_screen(clat,clon,rect)
            cw_px=int(cw/360*rect.w); ch_px=int(ch/180*rect.h)
            pygame.draw.rect(self.screen,C_MAP_LAND,(cx,cy,cw_px,ch_px))
        # Title
        self.screen.blit(self.fbig.render("GLOBAL SEASONAL OPERATION MAP",True,C_ACCENT),(rect.x+20,rect.y+12))
        self.screen.blit(self.fs.render("To-scale routes: breeding -> transit -> nursery drift -> harvest -> return  |  AI self-driving",True,C_TEXT_DIM),(rect.x+20,rect.y+48))
        # Determine current season from voyage day
        day=v.day; season_key="spring"
        if day%365 in range(60,152): season_key="spring"
        elif day%365 in range(152,244): season_key="summer"
        elif day%365 in range(244,335): season_key="autumn"
        else: season_key="winter"
        season=SEASONAL_ROUTES[season_key]
        season_colors={"spring":C_MAP_ROUTE_SPRING,"summer":C_MAP_ROUTE_SUMMER,
                        "autumn":C_MAP_ROUTE_AUTUMN,"winter":C_MAP_ROUTE_WINTER}
        mode_colors={"BREEDING":(255,180,80),"TRANSIT":C_ACCENT,"DRIFT":(100,200,255),
                     "HARVEST":(255,180,60),"NURSERY DRIFT":(100,220,180)}
        # Draw all seasonal routes with phase segments
        for sk,sv in SEASONAL_ROUTES.items():
            col=season_colors[sk]
            is_active=(sk==season_key)
            if not is_active: col=(col[0]//3,col[1]//3,col[2]//3)
            # Build route path: hub -> release zones -> hub
            hub_lat=sv.get("hub_lat",0); hub_lon=sv.get("hub_lon",0)
            route_pts=[self._latlon_to_screen(hub_lat,hub_lon,rect)]
            for zname in sv["release_zones"]:
                for wp in WORLD_MAP_WAYPOINTS:
                    if wp[0]==zname:
                        route_pts.append(self._latlon_to_screen(wp[1],wp[2],rect))
                        break
            route_pts.append(self._latlon_to_screen(hub_lat,hub_lon,rect))
            # Draw route segments with phase-specific styling
            if len(route_pts)>=3:
                for i in range(len(route_pts)-1):
                    # Phase: 0=transit out, 1..n-2=drift between zones, n-1=return
                    if i==0:
                        # Transit out — solid line
                        pygame.draw.line(self.screen,col,route_pts[i],route_pts[i+1],3 if is_active else 1)
                    elif i==len(route_pts)-2:
                        # Transit return — dashed line
                        x0,y0=route_pts[i]; x1,y1=route_pts[i+1]
                        dx,dy=x1-x0,y1-y0; dist=math.hypot(dx,dy)
                        if dist>5:
                            n_dashes=int(dist/8)
                            for j in range(0,n_dashes,2):
                                t0=j/n_dashes; t1=min(1.0,(j+1)/n_dashes)
                                p0=(int(x0+dx*t0),int(y0+dy*t0))
                                p1=(int(x0+dx*t1),int(y0+dy*t1))
                                pygame.draw.line(self.screen,col,p0,p1,2 if is_active else 1)
                    else:
                        # Drift between release zones — dotted line
                        x0,y0=route_pts[i]; x1,y1=route_pts[i+1]
                        dx,dy=x1-x0,y1-y0; dist=math.hypot(dx,dy)
                        n_dots=int(dist/6)
                        for j in range(n_dots):
                            t=j/max(1,n_dots)
                            px=int(x0+dx*t); py=int(y0+dy*t)
                            pygame.draw.circle(self.screen,col,(px,py),2 if is_active else 1)
                # Draw arrows on active route at midpoints
                if is_active:
                    for i in range(len(route_pts)-1):
                        mx=(route_pts[i][0]+route_pts[i+1][0])//2
                        my=(route_pts[i][1]+route_pts[i+1][1])//2
                        dx=route_pts[i+1][0]-route_pts[i][0]
                        dy=route_pts[i+1][1]-route_pts[i][1]
                        ang=math.atan2(dy,dx)
                        ax1=mx-int(math.cos(ang-0.4)*8); ay1=my-int(math.sin(ang-0.4)*8)
                        ax2=mx-int(math.cos(ang+0.4)*8); ay2=my-int(math.sin(ang+0.4)*8)
                        pygame.draw.polygon(self.screen,col,[(mx,my),(ax1,ay1),(ax2,ay2)])
        # Draw waypoints with labels
        for name,lat,lon,wtype in WORLD_MAP_WAYPOINTS:
            x,y=self._latlon_to_screen(lat,lon,rect)
            if wtype=="hub":
                pygame.draw.circle(self.screen,C_MAP_HUB,(x,y),6)
                pygame.draw.circle(self.screen,C_TEXT,(x,y),6,1)
                img=self.fmicro.render(name,True,C_MAP_HUB)
                self.screen.blit(img,(x+8,y-6))
            else:
                pygame.draw.circle(self.screen,C_MAP_RELEASE,(x,y),4)
                pygame.draw.circle(self.screen,C_TEXT,(x,y),4,1)
                img=self.fmicro.render(name,True,C_MAP_RELEASE)
                self.screen.blit(img,(x+6,y-5))
        # Current vessel position — interpolate along active season route
        hub_lat=season.get("hub_lat",1.3); hub_lon=season.get("hub_lon",103.8)
        vx,vy=self._latlon_to_screen(hub_lat,hub_lon,rect)
        if v.progress>0:
            zones=season["release_zones"]
            if zones:
                end_wp=None
                for wp in WORLD_MAP_WAYPOINTS:
                    if wp[0]==zones[-1]: end_wp=wp; break
                if end_wp:
                    ex,ey=self._latlon_to_screen(end_wp[1],end_wp[2],rect)
                    vx=int(vx+(ex-vx)*v.progress); vy=int(vy+(ey-vy)*v.progress)
        # Vessel marker with mode badge
        pygame.draw.circle(self.screen,C_H2,(vx,vy),8)
        pygame.draw.circle(self.screen,C_TEXT,(vx,vy),8,2)
        vm_col=mode_colors.get(pt.vessel_mode,C_H2)
        pygame.draw.circle(self.screen,vm_col,(vx,vy),4)
        img=self.fs.render("VESSEL [%s]"%pt.vessel_mode,True,C_H2)
        self.screen.blit(img,(vx+10,vy-6))
        # Scale bar (nautical miles)
        sb_x=rect.x+20; sb_y=rect.y+72
        nm_per_px=180.0/(rect.h*60.0)  # approx nm per pixel at equator
        target_nm=1000; sb_px=int(target_nm/nm_per_px)
        if sb_px>200: target_nm=500; sb_px=int(target_nm/nm_per_px)
        if sb_px>200: target_nm=200; sb_px=int(target_nm/nm_per_px)
        pygame.draw.rect(self.screen,C_TEXT_DIM,(sb_x,sb_y,sb_px,3))
        pygame.draw.rect(self.screen,C_TEXT_DIM,(sb_x,sb_y-4,2,11))
        pygame.draw.rect(self.screen,C_TEXT_DIM,(sb_x+sb_px-2,sb_y-4,2,11))
        self.screen.blit(self.fmicro.render("%d nm (to scale)"%target_nm,True,C_TEXT),(sb_x,sb_y-16))
        # ---- Season info panel (right side) ----
        ix=rect.right-340; iy=rect.y+80; iw=320; ih=500
        panel(self.screen,ix,iy,iw,ih,alpha=230)
        self.screen.blit(self.fb.render(season["name"],True,season_colors[season_key]),(ix+12,iy+10))
        self.screen.blit(self.fs.render("Best zone: %s"%season["best_zone"],True,C_TEXT),(ix+12,iy+40))
        self.screen.blit(self.fs.render("Route: %s"%season["route"],True,C_TEXT_DIM),(ix+12,iy+58))
        # Operation phases timeline
        yy=iy+82
        self.screen.blit(self.fs.render("OPERATION PHASES (to scale):",True,C_ACCENT),(ix+12,yy)); yy+=20
        total_days=sum(p["duration_days"] for p in season["phases"])
        bar_x=ix+12; bar_w=iw-24; bar_h=16; bar_y=yy
        # Draw phase timeline bar
        x_cursor=bar_x
        for pi,phase in enumerate(season["phases"]):
            pw=int(bar_w*phase["duration_days"]/total_days)
            mc=mode_colors.get(phase["mode"],C_TEXT)
            if phase["name"]=="BREEDING": mc=(255,180,80)
            elif phase["name"].startswith("TRANSIT"): mc=C_ACCENT
            elif phase["name"].startswith("NURSERY"): mc=(100,220,180)
            elif phase["name"]=="HARVEST": mc=(255,180,60)
            pygame.draw.rect(self.screen,mc,(x_cursor,bar_y,pw,bar_h))
            pygame.draw.rect(self.screen,C_TEXT,(x_cursor,bar_y,pw,bar_h),1)
            # Phase label inside bar if wide enough
            if pw>40:
                img=self.fmicro.render(phase["name"][:8],True,C_TEXT)
                self.screen.blit(img,(x_cursor+2,bar_y+2))
            x_cursor+=pw
        yy+=bar_h+6
        # Phase details
        for pi,phase in enumerate(season["phases"]):
            mc=mode_colors.get(phase["mode"],C_TEXT)
            if phase["name"]=="BREEDING": mc=(255,180,80)
            elif phase["name"].startswith("TRANSIT"): mc=C_ACCENT
            elif phase["name"].startswith("NURSERY"): mc=(100,220,180)
            elif phase["name"]=="HARVEST": mc=(255,180,60)
            pygame.draw.rect(self.screen,mc,(ix+12,yy+2,6,6))
            self.screen.blit(self.fmicro.render("%s (%.0fd) [%s]"%(phase["name"],phase["duration_days"],phase["mode"]),True,mc),(ix+22,yy))
            yy+=14
            self.screen.blit(self.fmicro.render("  %s"%phase["location"],True,C_TEXT_DIM),(ix+22,yy)); yy+=13
            self.screen.blit(self.fmicro.render("  %s"%phase["activity"][:60],True,C_TEXT_DIM),(ix+22,yy)); yy+=13
            self.screen.blit(self.fmicro.render("  -> %s"%phase["output"][:55],True,C_TEXT),(ix+22,yy)); yy+=15
        yy+=4; pygame.draw.line(self.screen,C_PANEL_HI,(ix+8,yy),(ix+iw-8,yy),1); yy+=6
        # Season stats
        stats_lines=[
            "Sea state: %.0f%%  Sun: %.0f%%  Temp: %.0f°C"%(season["sea_state_avg"]*100,season["sun_avg"]*100,season["temp_c"]),
            "Current: %.1f kn  Growth: +%.0f%%  Algae: +%.0f%%"%(season["current_kn"],(season["shrimp_growth_rate"]-1)*100,(season["algae_productivity"]-1)*100),
            "Predator risk: %s"%season["predator_risk"],
            "Total distance: %.0f nm"%season["total_distance_nm"],
            "Cycle: %.0f days (breed+transit+drift+harvest+return)"%total_days,
        ]
        for ln in stats_lines:
            self.screen.blit(self.fmicro.render(ln,True,C_TEXT),(ix+12,yy)); yy+=14
        yy+=4; pygame.draw.line(self.screen,C_PANEL_HI,(ix+8,yy),(ix+iw-8,yy),1); yy+=6
        # All seasons legend
        self.screen.blit(self.fmicro.render("ALL SEASONS:",True,C_ACCENT),(ix+12,yy)); yy+=14
        for sk,sv in SEASONAL_ROUTES.items():
            col=season_colors[sk]
            pygame.draw.rect(self.screen,col,(ix+12,yy+2,8,8))
            active_marker=" <-- ACTIVE" if sk==season_key else ""
            self.screen.blit(self.fmicro.render("%s: %.0f nm, %.0fd cycle%s"%(sv["name"].split("(")[0].strip(),sv["total_distance_nm"],sum(p["duration_days"] for p in sv["phases"]),active_marker),True,C_TEXT),(ix+26,yy))
            yy+=13
        # ---- Legend (bottom left) ----
        lx=rect.x+20; ly=rect.bottom-130
        panel(self.screen,lx,ly,280,120,alpha=230)
        self.screen.blit(self.fs.render("LEGEND",True,C_ACCENT),(lx+10,ly+8))
        pygame.draw.circle(self.screen,C_MAP_HUB,(lx+20,ly+30),5)
        self.screen.blit(self.fmicro.render("Hub port (breeding base)",True,C_TEXT),(lx+32,ly+26))
        pygame.draw.circle(self.screen,C_MAP_RELEASE,(lx+20,ly+48),4)
        self.screen.blit(self.fmicro.render("Release zone (juvenile release)",True,C_TEXT),(lx+32,ly+44))
        pygame.draw.circle(self.screen,C_H2,(lx+20,ly+66),6)
        self.screen.blit(self.fmicro.render("Vessel [%s]"%pt.vessel_mode,True,C_TEXT),(lx+32,ly+62))
        # Route line styles
        pygame.draw.line(self.screen,C_ACCENT,(lx+14,ly+84),(lx+28,ly+84),3)
        self.screen.blit(self.fmicro.render("Transit (solid)",True,C_TEXT),(lx+32,ly+80))
        pygame.draw.circle(self.screen,(100,200,255),(lx+20,ly+98),2)
        pygame.draw.circle(self.screen,(100,200,255),(lx+24,ly+98),2)
        self.screen.blit(self.fmicro.render("Drift (dotted)",True,C_TEXT),(lx+32,ly+94))
        # Distance scale
        self.screen.blit(self.fmicro.render("Scale: %d nm bar (to scale)"%target_nm,True,C_TEXT_DIM),(lx+10,ly+108))

    def draw_ops(self):
        rect=self.view_rect(); pt=self.pt
        # Background
        pygame.draw.rect(self.screen,C_PANEL,rect)
        # Title
        self.screen.blit(self.fbig.render("OPERATION PLAN",True,C_ACCENT),(rect.x+20,rect.y+12))
        self.screen.blit(self.fs.render("Construction phases, fleet rollout, seasonal cycles, and AI system status",True,C_TEXT_DIM),(rect.x+20,rect.y+48))
        # Left panel: construction phases (top half) + seasonal cycle (bottom half)
        px=rect.x+20; py=rect.y+80; pw=460; ph=rect.h-100
        panel(self.screen,px,py,pw,ph,alpha=230)
        self.screen.blit(self.fb.render("CONSTRUCTION PHASES (30 months)",True,C_ACCENT),(px+12,py+10))
        yy=py+40
        for phase in OPERATION_PLAN["phases"]:
            col=C_AI_DRIVE if phase["phase"]<=2 else (C_ALGAE if phase["phase"]<=4 else C_AI)
            self.screen.blit(self.fs.render("Phase %d: %s (Months %s)"%(phase["phase"],phase["name"],phase["months"]),True,col),(px+12,yy))
            yy+=18
            for item in phase["items"]:
                self.screen.blit(self.fmicro.render("  - %s"%item,True,C_TEXT_DIM),(px+20,yy)); yy+=15
            yy+=6
        # Seasonal operation cycle (below construction phases)
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(px+8,yy),(px+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("SEASONAL OPERATION CYCLE",True,C_MAP_ROUTE_SPRING),(px+12,yy)); yy+=24
        season_colors={"spring":C_MAP_ROUTE_SPRING,"summer":C_MAP_ROUTE_SUMMER,
                        "autumn":C_MAP_ROUTE_AUTUMN,"winter":C_MAP_ROUTE_WINTER}
        mode_col={"BREEDING":(255,180,80),"TRANSIT":C_ACCENT,"DRIFT":(100,200,255),
                  "HARVEST":(255,180,60),"NURSERY DRIFT":(100,220,180)}
        for sk,sv in SEASONAL_ROUTES.items():
            scol=season_colors[sk]
            self.screen.blit(self.fs.render(sv["name"],True,scol),(px+12,yy)); yy+=18
            # Phase timeline bar
            total_d=sum(p["duration_days"] for p in sv["phases"])
            bar_x=px+12; bar_w=pw-24; bar_h=10
            x_cur=bar_x
            for phase in sv["phases"]:
                pw_seg=int(bar_w*phase["duration_days"]/total_d)
                mc=mode_col.get(phase["name"],mode_col.get(phase["mode"],C_TEXT))
                if phase["name"]=="BREEDING": mc=(255,180,80)
                elif phase["name"].startswith("TRANSIT"): mc=C_ACCENT
                elif phase["name"].startswith("NURSERY"): mc=(100,220,180)
                elif phase["name"]=="HARVEST": mc=(255,180,60)
                pygame.draw.rect(self.screen,mc,(x_cur,yy,pw_seg,bar_h))
                pygame.draw.rect(self.screen,C_TEXT,(x_cur,yy,pw_seg,bar_h),1)
                x_cur+=pw_seg
            yy+=bar_h+4
            # Phase labels
            phase_summary=" -> ".join("%s(%.0fd)"%(p["name"][:4],p["duration_days"]) for p in sv["phases"])
            self.screen.blit(self.fmicro.render(phase_summary,True,C_TEXT_DIM),(px+16,yy)); yy+=13
            self.screen.blit(self.fmicro.render("%.0f nm total  |  %.0fd cycle  |  %s"%(sv["total_distance_nm"],total_d,sv["best_zone"][:30]),True,C_TEXT),(px+16,yy)); yy+=18
        # Middle panel: fleet rollout
        fx=px+pw+10; fy=py; fw=300; fh=ph
        panel(self.screen,fx,fy,fw,fh,alpha=230)
        self.screen.blit(self.fb.render("FLEET ROLLOUT (3 years)",True,C_GOOD),(fx+12,fy+10))
        yy=fy+40
        for v in OPERATION_PLAN["fleet_rollout"]:
            status_col=C_GOOD if v["status"]=="active" else C_TEXT_DIM
            self.screen.blit(self.fs.render("Vessel %2d  Year %d  %s"%(v["vessel"],v["year"],v["status"].upper()),True,status_col),(fx+12,yy))
            yy+=17
        yy+=10
        self.screen.blit(self.fs.render("Total: 12 vessels by Year 3",True,C_GOOD),(fx+12,yy))
        yy+=25
        # Financial summary
        self.screen.blit(self.fb.render("FINANCIAL SUMMARY",True,(100,220,130)),(fx+12,yy)); yy+=25
        fin_lines=[
            "Investment: $%.0fB"%(FINANCE["investment_usd"]/1e9),
            "Per vessel: $%.1fB"%(FINANCE["vessel_cost_usd"]/1e9),
            "Target: $%.0fT (Year %d)"%(FINANCE["target_valuation_usd"]/1e12,FINANCE["target_years"]),
            "",
            "Revenue/vessel/yr:",
            "  Shrimp: $%.1fB"%(FINANCE["shrimp_revenue_per_vessel_year_usd"]/1e9),
            "  Carbon: $%.0fM"%(FINANCE["carbon_credit_per_vessel_year_usd"]/1e6),
            "  Tech:   $%.0fM"%(FINANCE["tech_license_per_vessel_year_usd"]/1e6),
            "  Data:   $%.0fM"%(FINANCE["data_sales_per_vessel_year_usd"]/1e6),
            "",
            "Fleet (12): $%.1fB/yr"%((FINANCE["shrimp_revenue_per_vessel_year_usd"]+FINANCE["carbon_credit_per_vessel_year_usd"]+FINANCE["tech_license_per_vessel_year_usd"]+FINANCE["data_sales_per_vessel_year_usd"])*12/1e9),
        ]
        for ln in fin_lines:
            self.screen.blit(self.fs.render(ln,True,C_TEXT),(fx+12,yy)); yy+=17
        # Right panel: AI systems status
        ax=fx+fw+10; ay=py; aw=rect.w-pw-fw-50; ah=ph
        if aw<200: aw=200
        panel(self.screen,ax,ay,aw,ah,alpha=230)
        self.screen.blit(self.fb.render("AI SYSTEMS STATUS",True,C_AI),(ax+12,ay+10))
        yy=ay+40
        ai_lines=[
            "Autonomy: %s"%pt.ai_autonomy_level,
            "Decisions: %d"%pt.ai_total_decisions,
            "Model updates: %d"%pt.ai_model_updates,
            "",
            "SELF-DRIVING:",
            "  Confidence: %.0f%%"%pt.ai_drive_confidence,
            "  Collisions avoided: %d"%pt.ai_collision_avoidances,
            "  Weather reroutes: %d"%pt.ai_weather_reroutes,
            "  Auto mode switches: %d"%pt.ai_auto_mode_switches,
            "",
            "SELF-BREEDING:",
            "  Generations: %d"%pt.ai_breed_generations,
            "  Genetic gain: %.1f%%"%pt.ai_breed_genetic_gain_pct,
            "  Diversity: %.3f"%pt.ai_breed_diversity,
            "  Families: %d"%pt.ai_breed_families_tracked,
            "  Traits: %s"%pt.ai_breed_improvement_summary,
            "",
            "SELF-HERDING:",
            "  Schools tracked: %d"%pt.ai_herd_schools_tracked,
            "  Recapture preds: %d"%pt.ai_herd_recapture_predictions,
            "  Drones active: %d"%pt.ai_herd_drones_active,
            "  eDNA samples: %d"%pt.ai_herd_edna_samples,
            "  Migrations: %d"%pt.ai_herd_migration_patterns_learned,
            "",
            "SELF-MAINTAINING:",
            "  Uptime: %.1f%%"%pt.ai_maint_uptime_pct,
            "  Avg health: %.1f%%"%(pt.ai_maint_avg_health*100),
            "  Anomalies: %d"%pt.ai_maint_anomalies_detected,
            "  Auto-repairs: %d"%pt.ai_maint_auto_repairs,
            "  3D-printed parts: %d"%pt.ai_maint_parts_3d_printed,
            "",
            "SYSTEM HEALTH:",
        ]
        for ln in ai_lines:
            col=C_AI if "SELF-" in ln or "Autonomy" in ln else C_TEXT
            self.screen.blit(self.fs.render(ln,True,col),(ax+12,yy)); yy+=17
        for s,h in sorted(pt.ai_maint_system_health.items()):
            hc=C_GOOD if h>0.9 else (C_WARN if h>0.7 else C_BAD)
            bar_w=int((aw-100)*h)
            self.screen.blit(self.fmicro.render("%-12s"%s,True,C_TEXT_DIM),(ax+12,yy))
            pygame.draw.rect(self.screen,C_PANEL_HI,(ax+80,yy+2,aw-100,10))
            pygame.draw.rect(self.screen,hc,(ax+80,yy+2,bar_w,10))
            self.screen.blit(self.fmicro.render("%.0f%%"%(h*100),True,hc),(ax+aw-30,yy+2))
            yy+=15
        # Donation program summary (bottom strip)
        dx=px; dy=py+ph+10; dw=rect.w-60; dh=120
        panel(self.screen,dx,dy,dw,dh,alpha=230)
        self.screen.blit(self.fb.render("GLOBAL DONATION PROGRAM -- OAC FREE PROTEIN INITIATIVE",True,(255,100,100)),(dx+12,dy+8))
        yy=dy+32
        don_lines=[
            "\"No vessel leaves a port without feeding the hungry\"",
            "5%% of harvest = %.1fM t/year FREE  |  %.0fB meals  |  %.0fM people fed  |  %d port stops in %d nations"%(
                DONATION_PROGRAM["donation_t_year"]/1e6,
                DONATION_PROGRAM["donation_meals_year"]/1e9,
                DONATION_PROGRAM["people_fed_year"]/1e6,
                len(DONATION_PROGRAM["port_stops"])+len(DONATION_PROGRAM["seasonal_hub_stops"])+len(DONATION_PROGRAM["distribution_hub_donations"]),
                len(set([p["country"] for p in DONATION_PROGRAM["port_stops"]]+[h["country"] for h in DONATION_PROGRAM["seasonal_hub_stops"]]+[h["country"] for h in DONATION_PROGRAM["distribution_hub_donations"]])),
            ),
            "Partners: WFP, UN FAO, Save the Children, Action Against Hunger, Oxfam, Red Cross, GAIN + 18 local NGOs",
            "Revenue foregone: $%.1fB/yr  |  Tax benefit: $4.4B/yr  |  Expansion: 10%% by Year 5, 15%% by Year 10"%(
                DONATION_PROGRAM["revenue_foregone_usd_year"]/1e9),
        ]
        for ln in don_lines:
            self.screen.blit(self.fs.render(ln,True,C_TEXT),(dx+12,yy)); yy+=18

    def draw_company(self):
        rect=self.view_rect(); pt=self.pt
        pygame.draw.rect(self.screen,C_PANEL,rect)
        self.screen.blit(self.fbig.render("COMPANY & BUSINESS OPERATIONS",True,C_ACCENT),(rect.x+20,rect.y+12))
        self.screen.blit(self.fs.render("Ocean Abundance Corporation -- scroll: up/down arrows",True,C_TEXT_DIM),(rect.x+20,rect.y+48))
        # Scrollable 3-column layout
        top_y=rect.y+80; ph=rect.h-100; pw=(rect.w-60)//3
        col1_x=rect.x+20; col2_x=col1_x+pw+10; col3_x=col2_x+pw+10
        clip=pygame.Rect(rect.x,top_y,rect.w,ph); self.screen.set_clip(clip)
        scroll_y=top_y-self.company_scroll
        # ==================== COLUMN 1: COMPANY + FINANCIAL + MARKET + TAX ====================
        panel(self.screen,col1_x,top_y-self.company_scroll,pw,ph,alpha=230)
        yy=scroll_y
        self.screen.blit(self.fb.render("COMPANY STRUCTURE",True,C_ACCENT),(col1_x+12,yy)); yy+=24
        self.screen.blit(self.fs.render(COMPANY["name"],True,C_TEXT),(col1_x+12,yy)); yy+=16
        self.screen.blit(self.fs.render("Holding: %s"%COMPANY["holding"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Founded: %s"%COMPANY["founded"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        for s in COMPANY["structure"]:
            self.screen.blit(self.fmicro.render("  - %s"%s,True,C_TEXT_DIM),(col1_x+16,yy)); yy+=13
        yy+=6
        self.screen.blit(self.fs.render("Board of Directors:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for b in COMPANY["board"]:
            self.screen.blit(self.fmicro.render("  %s: %s (%.0f%%)"%(b["role"],b["name"],b["equity_pct"]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=13
        yy+=6
        self.screen.blit(self.fs.render("Employees: Yr1=%dK  Yr5=%dK  Yr10=%dK"%(
            COMPANY["total_employees_year1"]/1000,COMPANY["total_employees_year5"]/1000,
            COMPANY["total_employees_year10"]/1000),True,C_GOOD),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Departments: %d"%len(COMPANY["departments"]),True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        for d in COMPANY["departments"][:8]:
            self.screen.blit(self.fmicro.render("  - %s"%d,True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        if len(COMPANY["departments"])>8:
            self.screen.blit(self.fmicro.render("  ... +%d more"%(len(COMPANY["departments"])-8),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        # Financial model 10-year P&L
        self.screen.blit(self.fb.render("10-YEAR FINANCIAL MODEL",True,(100,220,130)),(col1_x+12,yy)); yy+=24
        self.screen.blit(self.fmicro.render("Year  Vess  Harvest   Revenue    Net       Cumul",True,C_TEXT_DIM),(col1_x+12,yy)); yy+=14
        for yr in FINANCIAL_MODEL["year_by_year"]:
            net_col=C_BAD if yr["net_usd"]<0 else C_GOOD
            cumul_str="$%.1fB"%(yr["cumulative_usd"]/1e9) if yr["cumulative_usd"]<1e12 else "$%.1fT"%(yr["cumulative_usd"]/1e12)
            self.screen.blit(self.fmicro.render("%d  %2d   %4.1fM  $%5.0fB  $%5.0fB  %s"%(
                yr["year"],yr["vessels"],yr["harvest_t"]/1e6,yr["revenue_usd"]/1e9,
                yr["net_usd"]/1e9,cumul_str),True,net_col),(col1_x+12,yy)); yy+=13
        yy+=4
        self.screen.blit(self.fs.render("IRR: %.0f%%  Payback: %.1f yr  NPV: $%.1fT"%(
            FINANCIAL_MODEL["irr_pct"],FINANCIAL_MODEL["payback_years"],
            FINANCIAL_MODEL["npv_usd"]/1e12),True,C_GOOD),(col1_x+12,yy)); yy+=16
        self.screen.blit(self.fs.render("Investment: $%.0fB  Target: $%.0fT"%(
            FINANCIAL_MODEL["total_investment_usd"]/1e9,
            FINANCIAL_MODEL["target_valuation_usd"]/1e12),True,C_TEXT),(col1_x+12,yy)); yy+=16
        # Revenue streams
        yy+=4
        self.screen.blit(self.fs.render("Revenue Streams:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for rs in FINANCIAL_MODEL["revenue_streams"]:
            self.screen.blit(self.fmicro.render("  %s (%.0f%%): %s"%(rs["stream"],rs["pct_of_total"],rs["detail"]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        # OPEX breakdown
        yy+=4
        self.screen.blit(self.fs.render("OPEX Breakdown:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for op in FINANCIAL_MODEL["opex_breakdown"]:
            col=C_GOOD if op["pct"]==0.0 else C_TEXT_DIM
            self.screen.blit(self.fmicro.render("  %s (%.0f%%): %s"%(op["category"],op["pct"],op["detail"]),True,col),(col1_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        # Market analysis
        self.screen.blit(self.fb.render("MARKET ANALYSIS",True,C_MAP_ROUTE),(col1_x+12,yy)); yy+=24
        ma=MARKET_ANALYSIS
        self.screen.blit(self.fs.render("Global market: $%.0fB (2024) -> $%.0fB (2035)"%(
            ma["global_shrimp_market_2024_usd"]/1e9,ma["global_shrimp_market_2035_projected_usd"]/1e9),True,C_TEXT),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("CAGR: %.1f%%"%ma["cagr_pct"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Market segments:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for ms in ma["market_segments"]:
            self.screen.blit(self.fmicro.render("  %s (%.0f%%): %s"%(ms["segment"][:25],ms["pct"],ms["detail"][:35]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Regional markets:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for rm in ma["regional_markets"]:
            self.screen.blit(self.fmicro.render("  %s: $%.0fB  growth %.1f%%  %.1f kg/cap"%(
                rm["region"][:18],rm["size_usd"]/1e9,rm["growth_pct"],rm["per_capita_kg_yr"]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Competitors:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for cp in ma["competitors"]:
            self.screen.blit(self.fmicro.render("  %s: $%.1fB  %.0f%% share"%(
                cp["name"][:25],cp["revenue_usd"]/1e9,cp["market_share_pct"]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Our advantages:",True,C_GOOD),(col1_x+12,yy)); yy+=15
        for adv in ma["our_competitive_advantages"][:6]:
            self.screen.blit(self.fmicro.render("  - %s"%adv[:55],True,C_GOOD),(col1_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        # Tax planning
        self.screen.blit(self.fb.render("TAX PLANNING",True,(100,220,130)),(col1_x+12,yy)); yy+=24
        tp=TAX_PLANNING
        self.screen.blit(self.fs.render("Domicile: %s"%tp["domicile"],True,C_TEXT),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Corporate rate: %.0f%%  Effective: %.0f%% (Y1) -> %.0f%% (Y10)"%(
            tp["corporate_tax_rate_pct"],tp["effective_tax_rate_year1_pct"],
            tp["effective_tax_rate_year10_pct"]),True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Incentives:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for ti in tp["tax_incentives"]:
            self.screen.blit(self.fmicro.render("  %s: %.0f%% for %s yr"%(ti["incentive"][:22],ti["rate_pct"] if isinstance(ti["rate_pct"],(int,float)) else 0,ti["duration_years"] if isinstance(ti["duration_years"],(int,float)) else "?"),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Treaties: %s"%tp["double_taxation_treaties"][:50],True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Flag: %s"%tp["flag_state"],True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        # Depreciation
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("DEPRECIATION (straight-line)",True,(100,220,130)),(col1_x+12,yy)); yy+=24
        ds=DEPRECIATION_SCHEDULE
        for a in ds["assets"]:
            self.screen.blit(self.fmicro.render("  %s: $%.1fM/yr (%dyr)"%(
                a["asset"][:28],a["annual_depreciation_usd"]/1e6,a["life_years"]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Total/vessel: $%.0fM/yr  Fleet: $%.0fM/yr"%(
            ds["total_annual_depreciation_per_vessel_usd"]/1e6,
            ds["total_annual_depreciation_fleet_usd"]/1e6),True,C_TEXT),(col1_x+12,yy)); yy+=15
        # Break-even
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("BREAK-EVEN ANALYSIS",True,C_WARN),(col1_x+12,yy)); yy+=24
        be=BREAK_EVEN_ANALYSIS
        self.screen.blit(self.fs.render("Break-even: %dK t/yr at $%.1f/kg (%d vessels)"%(
            be["break_even_harvest_t_per_year"]//1000,be["break_even_price_usd_kg"],
            be["break_even_vessels"]),True,C_TEXT),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Break-even year: %d"%be["break_even_year"],True,C_GOOD),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Fixed costs: $%.1fB/yr  Variable: $%.1f/kg"%(
            be["fixed_costs_per_year_usd"]/1e9,be["variable_cost_per_kg_usd"]),True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Contribution margin: $%.1f/kg (%.0f%%)"%(
            be["contribution_margin_per_kg_usd"],be["contribution_margin_ratio"]*100),True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Sensitivity:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for s in be["sensitivity"]:
            self.screen.blit(self.fmicro.render("  %s -> %dK t, %d"%(
                s["scenario"][:35],s["break_even_harvest_t"]//1000,s["break_even_year"]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        # Sensitivity analysis
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("SENSITIVITY ANALYSIS",True,C_WARN),(col1_x+12,yy)); yy+=24
        sa=SENSITIVITY_ANALYSIS
        self.screen.blit(self.fmicro.render("Scenario        Prob  NPV     IRR",True,C_TEXT_DIM),(col1_x+12,yy)); yy+=14
        for sc in sa["scenarios"]:
            sc_col=C_GOOD if sc["npv_usd"]>0 else C_BAD
            self.screen.blit(self.fmicro.render("%-14s %3.0f%%  $%5.1fB  %4.0f%%"%(
                sc["name"][:14],sc["probability"]*100,sc["npv_usd"]/1e9,sc["irr_pct"]),True,sc_col),(col1_x+12,yy)); yy+=13
        yy+=4
        self.screen.blit(self.fs.render("Key sensitivities:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for ks in sa["key_sensitivities"]:
            self.screen.blit(self.fmicro.render("  %s: %s"%(ks["variable"][:20],ks["impact"][:40]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        # ==================== COLUMN 2: SUPPLY CHAIN + PROCESSING + DISTRIBUTION + CUSTOMERS + QA ====================
        panel(self.screen,col2_x,top_y-self.company_scroll,pw,ph,alpha=230)
        yy=scroll_y
        self.screen.blit(self.fb.render("SUPPLY CHAIN (11 steps)",True,C_SHRIMP),(col2_x+12,yy)); yy+=24
        for sc in SUPPLY_CHAIN:
            self.screen.blit(self.fs.render("Step %d: %s"%(sc["step"],sc["name"]),True,C_TEXT),(col2_x+12,yy)); yy+=15
            dur="%.0fh"%sc.get("duration_h",0) if "duration_h" in sc else (
                "%.0fd"%sc.get("duration_days",0) if "duration_days" in sc else
                "%.0fmo"%sc.get("duration_months",0))
            self.screen.blit(self.fmicro.render("  Dur: %s  Loc: %s"%(dur,sc["location"][:30]),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  In: %s"%sc["input"][:45],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  Out: %s"%sc["output"][:45],True,C_GOOD),(col2_x+16,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  QC: %s"%sc["quality"][:45],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
            yy+=4
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # Processing plants
        self.screen.blit(self.fb.render("PROCESSING PLANTS (%d)"%len(PROCESSING_PLANTS),True,C_ACCENT),(col2_x+12,yy)); yy+=24
        shown=0
        for p in PROCESSING_PLANTS:
            if p["location"].startswith("TBD"): continue
            self.screen.blit(self.fs.render("#%d %s"%(p["id"],p["location"][:30]),True,C_TEXT),(col2_x+12,yy)); yy+=14
            self.screen.blit(self.fmicro.render("  %d kg/day  %d workers  $%.0fM  Yr%d"%(
                p["capacity_kg_day"],p["workers"],p["cost_usd"]/1e6,p["year"]),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  Certs: %s"%", ".join(p["certifications"])[:45],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
            shown+=1
            if shown>=8: break
        remaining=len([p for p in PROCESSING_PLANTS if p["location"].startswith("TBD")])
        if remaining:
            self.screen.blit(self.fmicro.render("  ... +%d more planned"%remaining,True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # Distribution
        self.screen.blit(self.fb.render("DISTRIBUTION (%d centers)"%len(DISTRIBUTION_NETWORK),True,C_MAP_ROUTE),(col2_x+12,yy)); yy+=24
        shown=0
        for d in DISTRIBUTION_NETWORK:
            if d["location"].startswith("TBD"): continue
            self.screen.blit(self.fs.render("#%d %s (%s)"%(d["id"],d["location"][:25],d["type"]),True,C_TEXT),(col2_x+12,yy)); yy+=14
            self.screen.blit(self.fmicro.render("  %d t/day  %d t cold  %d trucks  $%.0fM"%(
                d["capacity_t_day"],d["cold_storage_t"],d["trucks"],d["cost_usd"]/1e6),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
            shown+=1
            if shown>=6: break
        remaining=len([d for d in DISTRIBUTION_NETWORK if d["location"].startswith("TBD")])
        if remaining:
            self.screen.blit(self.fmicro.render("  ... +%d more planned"%remaining,True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # Customer segments
        self.screen.blit(self.fb.render("CUSTOMER SEGMENTS",True,(100,220,130)),(col2_x+12,yy)); yy+=24
        self.screen.blit(self.fmicro.render("Segment              %%   Vol(Kt)  $/kg",True,C_TEXT_DIM),(col2_x+12,yy)); yy+=14
        for cs in CUSTOMER_SEGMENTS:
            self.screen.blit(self.fmicro.render("%-20s %3.0f   %5.0f   $%.0f"%(
                cs["segment"][:20],cs["pct_of_revenue"],cs["volume_t_year"]/1e3,
                cs["price_usd_kg"]),True,C_TEXT),(col2_x+12,yy)); yy+=13
            self.screen.blit(self.fmicro.render("  %s"%cs["customers"][:50],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=11
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # Quality assurance
        self.screen.blit(self.fb.render("QUALITY ASSURANCE",True,C_GOOD),(col2_x+12,yy)); yy+=24
        qa=QUALITY_ASSURANCE
        self.screen.blit(self.fs.render("Certifications:",True,C_TEXT),(col2_x+12,yy)); yy+=15
        for c in qa["certifications"]:
            self.screen.blit(self.fmicro.render("  %s: %s (%s)"%(c["standard"],c["scope"][:25],c["status"]),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Testing:",True,C_TEXT),(col2_x+12,yy)); yy+=15
        for key,val in qa["testing_protocol"].items():
            self.screen.blit(self.fmicro.render("  %s: %s"%(key.replace("_"," ")[:20],str(val)[:40]),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Cold chain: %s"%qa["cold_chain_specs"]["freezing"],True,C_TEXT_DIM),(col2_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Recall: %s"%qa["recall_procedure"],True,C_WARN),(col2_x+12,yy)); yy+=15
        # ==================== COLUMN 3: RISK + CRISIS + HR + PATENTS + ESG + KPIs ====================
        panel(self.screen,col3_x,top_y-self.company_scroll,pw,ph,alpha=230)
        yy=scroll_y
        self.screen.blit(self.fb.render("RISK MANAGEMENT",True,C_WARN),(col3_x+12,yy)); yy+=24
        for r in RISK_MGMT:
            prob_col={"high":C_BAD,"medium":C_WARN,"low":C_GOOD}.get(r["probability"],C_TEXT)
            self.screen.blit(self.fs.render("%s"%r["risk"][:35],True,C_TEXT),(col3_x+12,yy)); yy+=14
            self.screen.blit(self.fmicro.render("  P:%s I:%s  %s"%(
                r["probability"][:1].upper(),r["impact"][:1].upper(),
                r["mitigation"][:40]),True,C_TEXT_DIM),(col3_x+16,yy))
            self.screen.blit(self.fmicro.render("P:%s I:%s"%(r["probability"][:1].upper(),r["impact"][:1].upper()),True,prob_col),(col3_x+pw-60,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  Ins: %s"%r["insurance"][:50],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  Res: %s"%r["residual_risk"][:50],True,C_GOOD),(col3_x+16,yy)); yy+=12
            yy+=4
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # Crisis management
        self.screen.blit(self.fb.render("CRISIS MANAGEMENT",True,C_BAD),(col3_x+12,yy)); yy+=24
        cm=CRISIS_MANAGEMENT
        for ct in cm["crisis_types"]:
            self.screen.blit(self.fmicro.render("  %s: P=%s I=%s  $%.0fM impact"%(
                ct["type"][:28],ct["probability"],ct["impact"],
                ct["financial_impact_usd"]/1e6),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Response: %s"%cm["response_time"],True,C_WARN),(col3_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # HR
        self.screen.blit(self.fb.render("HR SYSTEM",True,C_AI),(col3_x+12,yy)); yy+=24
        self.screen.blit(self.fs.render("Employees: Yr1=%dK  Yr5=%dK  Yr10=%dK"%(
            HR_SYSTEM["total_employees_year1"]/1000,HR_SYSTEM["total_employees_year5"]/1000,
            HR_SYSTEM["total_employees_year10"]/1000),True,C_TEXT),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Retention: %.0f%%  Safety: %s"%(
            HR_SYSTEM["retention_rate_target_pct"],HR_SYSTEM["safety_record_target"][:25]),True,C_TEXT_DIM),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Key hires:",True,C_TEXT),(col3_x+12,yy)); yy+=15
        for h in HR_SYSTEM["hiring_pipeline"][:6]:
            self.screen.blit(self.fmicro.render("  %s x%d  $%.0fK+%.0fK"%(h["role"][:22],h["count"],h["salary_usd"]/1000,h["bonus_usd"]/1000),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # Patents
        self.screen.blit(self.fb.render("PATENT PORTFOLIO",True,C_ACCENT),(col3_x+12,yy)); yy+=24
        pp=PATENT_PORTFOLIO
        self.screen.blit(self.fs.render("Filed: %d  Granted: %d  Value: $%.1fB"%(
            pp["total_patents_filed"],pp["total_patents_granted"],
            pp["estimated_portfolio_value_usd"]/1e9),True,C_TEXT),(col3_x+12,yy)); yy+=15
        for cat in pp["categories"]:
            self.screen.blit(self.fmicro.render("  %s: %d patents"%(cat["category"][:25],cat["count"]),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Geographies: %s"%pp["geographies"][:50],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # ESG
        self.screen.blit(self.fb.render("ESG REPORTING",True,C_ALGAE),(col3_x+12,yy)); yy+=24
        esg=ESG_REPORTING
        self.screen.blit(self.fs.render("Carbon: %.1f kg CO2/kg (NEGATIVE)"%esg["environmental"]["carbon_footprint_kg_co2_per_kg_shrimp"],True,C_GOOD),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fmicro.render("  Water: %s"%esg["environmental"]["water_use"],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  Land: %s"%esg["environmental"]["land_use"],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  Antibiotics: %s"%esg["environmental"]["antibiotic_use"],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  Wild fish feed: %s"%esg["environmental"]["wild_fish_in_feed"],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  Waste: %s"%esg["environmental"]["waste_circularity"],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Social: %s"%esg["social"]["food_security"][:45],True,C_TEXT),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fmicro.render("  Jobs: %d (%d developing)"%(
            esg["social"]["employment"],esg["social"]["developing_nation_jobs"]),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Certifications:",True,C_TEXT),(col3_x+12,yy)); yy+=15
        for c in esg["certifications_target"]:
            self.screen.blit(self.fmicro.render("  - %s"%c[:45],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        # KPI Dashboard
        self.screen.blit(self.fb.render("KPI DASHBOARD",True,C_AI),(col3_x+12,yy)); yy+=24
        kd=KPI_DASHBOARD
        self.screen.blit(self.fs.render("Operational KPIs:",True,C_TEXT),(col3_x+12,yy)); yy+=15
        for k in kd["operational_kpis"][:6]:
            self.screen.blit(self.fmicro.render("  %s: %s %s"%(k["kpi"][:28],k["target"],k["unit"]),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Financial KPIs:",True,C_TEXT),(col3_x+12,yy)); yy+=15
        for k in kd["financial_kpis"][:5]:
            self.screen.blit(self.fmicro.render("  %s: %s %s"%(k["kpi"][:28],k["target"],k["unit"]),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Sustainability KPIs:",True,C_GOOD),(col3_x+12,yy)); yy+=15
        for k in kd["sustainability_kpis"][:5]:
            self.screen.blit(self.fmicro.render("  %s: %s %s"%(k["kpi"][:28],k["target"],k["unit"]),True,C_GOOD),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("HR KPIs:",True,C_TEXT),(col3_x+12,yy)); yy+=15
        for k in kd["hr_kpis"]:
            self.screen.blit(self.fmicro.render("  %s: %s %s"%(k["kpi"][:28],k["target"],k["unit"]),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        # Insurance
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("INSURANCE",True,C_TEXT),(col3_x+12,yy)); yy+=24
        for ins in COMPANY["insurance"]:
            self.screen.blit(self.fmicro.render("  %s: $%.0fM (%.1f%% prem) via %s"%(
                ins["type"][:20],ins["coverage_usd"]/1e6,ins["premium_pct"],ins["carrier"][:15]),True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        # Regulatory
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("REGULATORY COMPLIANCE",True,C_ACCENT),(col3_x+12,yy)); yy+=24
        for reg in REGULATORY:
            self.screen.blit(self.fs.render("%s -- %s"%(reg["jurisdiction"][:15],reg["agency"][:20]),True,C_TEXT),(col3_x+12,yy)); yy+=14
            self.screen.blit(self.fmicro.render("  Status: %s"%reg["status"],True,C_GOOD if "compliant" in reg["status"] else C_WARN),(col3_x+16,yy)); yy+=12
            for rl in reg["regulations"][:2]:
                self.screen.blit(self.fmicro.render("    - %s"%rl[:45],True,C_TEXT_DIM),(col3_x+20,yy)); yy+=11
            yy+=3
        self.screen.set_clip(None)
        # Clamp scroll
        col1_bottom=yy+scroll_y-top_y
        max_scroll=max(0,col1_bottom-ph+100)
        self.company_scroll=max(0,min(self.company_scroll,max_scroll))

    def draw_quota(self):
        rect=self.view_rect(); pt=self.pt
        pygame.draw.rect(self.screen,C_PANEL,rect)
        self.screen.blit(self.fbig.render("FISHERIES QUOTA MANAGEMENT",True,C_ACCENT),(rect.x+20,rect.y+12))
        self.screen.blit(self.fs.render("TAC, EEZ licensing, ITQ, RFMO, stock assessment, partner fleet, harvest plan, sustainability -- scroll: up/down",True,C_TEXT_DIM),(rect.x+20,rect.y+48))
        top_y=rect.y+80; ph=rect.h-100; pw=(rect.w-60)//3
        col1_x=rect.x+20; col2_x=col1_x+pw+10; col3_x=col2_x+pw+10
        clip=pygame.Rect(rect.x,top_y,rect.w,ph); self.screen.set_clip(clip)
        scroll_y=top_y-self.quota_scroll
        # ==================== COLUMN 1: QUOTA SYSTEM + ZONE ALLOCATIONS + ITQ ====================
        panel(self.screen,col1_x,top_y-self.quota_scroll,pw,ph,alpha=230)
        yy=scroll_y
        self.screen.blit(self.fb.render("QUOTA MANAGEMENT SYSTEM",True,C_ACCENT),(col1_x+12,yy)); yy+=24
        q=QUOTA_SYSTEM
        self.screen.blit(self.fs.render("Total Allowable Catch: %.0fK t/yr"%(q["total_allowable_catch_t_year"]/1e3),True,C_TEXT),(col1_x+12,yy)); yy+=16
        self.screen.blit(self.fs.render("Recapture rate: %.0f%%"%q["recapture_rate_pct"],True,C_GOOD),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Per-vessel quota: %.0fK t/yr"%(q["per_vessel_quota_t_year"]/1e3),True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Juveniles released: %.1fT/yr"%(q["total_release_juveniles_year"]/1e12),True,C_SHRIMP),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Harvest size: %.0fg  Shrimp/t: %.0f"%(q["harvest_size_g"],q["shrimp_per_tonne"]),True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Revenue/tonne: $%.0f"%(q["revenue_per_tonne_usd"]),True,(100,220,130)),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Total revenue potential: $%.0fB"%(q["total_revenue_potential_usd"]/1e9),True,C_GOOD),(col1_x+12,yy)); yy+=15
        yy+=6; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("ZONE ALLOCATIONS",True,C_MAP_ROUTE),(col1_x+12,yy)); yy+=24
        self.screen.blit(self.fmicro.render("Zone              TAC(Kt)  MSY(Kt)  Buffer  Monitor",True,C_TEXT_DIM),(col1_x+12,yy)); yy+=14
        for z in q["per_zone_quotas"]:
            self.screen.blit(self.fmicro.render("%-18s %5.0f    %5.0f    %4.0f%%   %s"%(
                z["zone"][:18],z["tac_t"]/1e3,z["msy_t"]/1e3,z["buffer_pct"],
                "AUV" if "AUV" in z["monitoring"] else "sat"),True,C_TEXT),(col1_x+12,yy)); yy+=13
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fs.render("Enforcement: %s"%q["quota_enforcement"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Transfer: %s"%q["quota_transfer"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Carryover: %s"%q["quota_carryover"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Bycatch quota: %.0fK t  Target: <%.0f%%"%(
            q["bycatch_quota_t"]/1e3,q["bycatch_discard_rate_target_pct"]),True,C_GOOD),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Sustainability: %s"%q["sustainability_threshold"],True,C_WARN),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Assessment: %s"%q["stock_assessment_method"][:50],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Frequency: %s"%q["assessment_frequency"],True,C_TEXT_DIM),(col1_x+12,yy)); yy+=15
        # ITQ System
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col1_x+8,yy),(col1_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("ITQ SYSTEM",True,C_MAP_ROUTE),(col1_x+12,yy)); yy+=24
        itq=ITQ_SYSTEM
        self.screen.blit(self.fmicro.render("  %s"%itq["description"][:55],True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  %s"%itq["our_approach"][:55],True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Countries with ITQ:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        for c in itq["countries_with_itq_systems"]:
            self.screen.blit(self.fmicro.render("  %s: %s (%s)"%(
                c["country"][:14],c["system"][:20],c["our_status"][:25]),True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Quota volumes:",True,C_TEXT),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fmicro.render("Country            Quota(Kt)  Royalty%%",True,C_TEXT_DIM),(col1_x+12,yy)); yy+=14
        for qv in itq["quota_volumes"]:
            self.screen.blit(self.fmicro.render("%-18s %5.0f      %4.1f"%(
                qv["country"][:18],qv["quota_t_year"]/1e3,qv["royalty_pct"]),True,C_TEXT),(col1_x+12,yy)); yy+=13
        self.screen.blit(self.fs.render("Total: %.0fK t/yr"%itq["total_quota_t_year"],True,C_GOOD),(col1_x+12,yy)); yy+=15
        self.screen.blit(self.fmicro.render("  %s"%itq["note"][:55],True,C_TEXT_DIM),(col1_x+16,yy)); yy+=12
        # ==================== COLUMN 2: EEZ LICENSES + PARTNER FLEET + RFMO ====================
        panel(self.screen,col2_x,top_y-self.quota_scroll,pw,ph,alpha=230)
        yy=scroll_y
        self.screen.blit(self.fb.render("EEZ LICENSES (18 nations)",True,C_MAP_ROUTE),(col2_x+12,yy)); yy+=24
        self.screen.blit(self.fmicro.render("Country        Type         Fee($M)  Roy%%  Yrs  Status",True,C_TEXT_DIM),(col2_x+12,yy)); yy+=14
        for e in EEZ_LICENSES:
            st_col=C_GOOD if e["status"]=="active" else (C_WARN if e["status"]=="negotiating" else C_TEXT_DIM)
            self.screen.blit(self.fmicro.render("%-14s %-12s %5.0f    %4.1f  %2d   %s"%(
                e["country"][:14],e["license_type"][:12],e["fee_usd"]/1e6,
                e["royalty_pct"],e["duration_years"],e["status"][:8]),True,st_col),(col2_x+12,yy)); yy+=13
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        total_fee=sum(e["fee_usd"] for e in EEZ_LICENSES)
        total_area=sum(e["zone_area_km2"] for e in EEZ_LICENSES)
        self.screen.blit(self.fs.render("Total fees: $%.0fM  Total area: %.0fM km2"%(
            total_fee/1e6,total_area/1e6),True,C_TEXT),(col2_x+12,yy)); yy+=16
        self.screen.blit(self.fs.render("Total release zones: %d"%sum(e["release_zones"] for e in EEZ_LICENSES),True,C_TEXT_DIM),(col2_x+12,yy)); yy+=15
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        # Partner fleet
        self.screen.blit(self.fb.render("PARTNER FLEET (3,500 vessels)",True,C_GOOD),(col2_x+12,yy)); yy+=24
        pf=PARTNER_FLEET_DETAIL
        self.screen.blit(self.fs.render("Model: %s  Our share: %.0f%%  Partner: %.0f%%"%(
            pf["model"],pf["our_share_pct"],pf["partner_share_pct"]),True,C_TEXT),(col2_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Fee: $%.2f/kg  CAPEX saved: $%.1fB"%(
            pf["partner_fee_per_kg"],pf["capex_saved_usd"]/1e9),True,C_GOOD),(col2_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("OPEX saved: $%.1fB/yr  Partner rev: $%.1fB/yr"%(
            pf["opex_saved_per_year_usd"]/1e9,pf["total_partner_revenue_year_usd"]/1e9),True,C_TEXT_DIM),(col2_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Vessel types:",True,C_TEXT),(col2_x+12,yy)); yy+=15
        for vt in pf["vessel_types"]:
            self.screen.blit(self.fmicro.render("  %s: %d vessels, %d kg/day, %d crew"%(
                vt["type"],vt["count"],vt["catch_kg_day"],vt["crew"]),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Regions:",True,C_TEXT),(col2_x+12,yy)); yy+=15
        for rg in pf["regions"]:
            self.screen.blit(self.fmicro.render("  %s: %d vessels (%s)"%(
                rg["region"],rg["vessels"],", ".join(rg["countries"][:3])),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Coord: %s"%pf["coordination"][:50],True,C_AI),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Track: %s"%pf["tracking"][:50],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Pay: %s"%pf["payment"][:50],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        # RFMO Framework
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col2_x+8,yy),(col2_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("RFMO FRAMEWORK",True,C_ACCENT),(col2_x+12,yy)); yy+=24
        rf=RFMO_FRAMEWORK
        self.screen.blit(self.fmicro.render("  %s"%rf["definition"][:55],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Relevant RFMOs:",True,C_TEXT),(col2_x+12,yy)); yy+=15
        for r in rf["relevant_rfmos"]:
            self.screen.blit(self.fmicro.render("  %s: %s"%(r["name"],r["our_status"][:35]),True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Our position:",True,C_GOOD),(col2_x+12,yy)); yy+=15
        self.screen.blit(self.fmicro.render("  %s"%rf["our_position"][:55],True,C_GOOD),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  Legal: %s"%rf["legal_basis"][:50],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fs.render("Compliance:",True,C_TEXT),(col2_x+12,yy)); yy+=15
        for c in rf["compliance"]:
            self.screen.blit(self.fmicro.render("  - %s"%c[:50],True,C_TEXT_DIM),(col2_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("Innovation: %s"%rf["innovation"][:50],True,C_AI),(col2_x+16,yy)); yy+=12
        # ==================== COLUMN 3: HARVEST PLAN + SUSTAINABILITY + WORKING CAPITAL ====================
        panel(self.screen,col3_x,top_y-self.quota_scroll,pw,ph,alpha=230)
        yy=scroll_y
        self.screen.blit(self.fb.render("HARVEST PLAN",True,C_SHRIMP),(col3_x+12,yy)); yy+=24
        hp=HARVEST_PLAN
        self.screen.blit(self.fs.render("Method: %s"%hp["harvest_method"],True,C_TEXT),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Season: %s"%hp["harvest_season"],True,C_TEXT_DIM),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Catch/vessel: %d kg/hr = %.0f t/day"%(
            hp["per_vessel_catch_kg_hr"],hp["per_vessel_catch_t_day"]),True,C_TEXT),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Fleet catch: %.0fK t/yr"%(hp["fleet_catch_t_year"]/1e3),True,C_TEXT_DIM),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Partner catch: %.0fK t/yr"%(hp["partner_fleet_catch_t_year"]/1e3),True,C_TEXT_DIM),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Total harvest: %.0fK t/yr"%(hp["total_harvest_t_year"]/1e3),True,C_GOOD),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Recapture: %.0f%%  Bycatch: %.0f%%"%(
            hp["recapture_rate_pct"],hp["bycatch_rate_pct"]),True,C_TEXT),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Bycatch: %s"%hp["bycatch_handling"][:50],True,C_GOOD),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Processing yield: %.0f%% = %.0fK t/yr"%(
            hp["processing_yield_pct"],hp["processing_output_t_year"]/1e3),True,C_TEXT),(col3_x+12,yy)); yy+=15
        yy+=6; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("PRODUCT MIX",True,(100,220,130)),(col3_x+12,yy)); yy+=24
        self.screen.blit(self.fmicro.render("Product                    %%   $/kg",True,C_TEXT_DIM),(col3_x+12,yy)); yy+=14
        for pm in hp["product_mix"]:
            self.screen.blit(self.fmicro.render("%-26s %3.0f   $%.0f"%(
                pm["product"][:26],pm["pct"],pm["price_usd_kg"]),True,C_TEXT),(col3_x+12,yy)); yy+=13
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("SUSTAINABILITY METRICS",True,C_GOOD),(col3_x+12,yy)); yy+=24
        for sm in hp["sustainability_metrics"]:
            self.screen.blit(self.fs.render(sm["metric"],True,C_TEXT),(col3_x+12,yy)); yy+=14
            self.screen.blit(self.fmicro.render("  Target: %s"%sm["target"],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
            self.screen.blit(self.fmicro.render("  Status: %s"%sm["status"],True,C_GOOD),(col3_x+16,yy)); yy+=12
        # Working capital
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("WORKING CAPITAL",True,(100,220,130)),(col3_x+12,yy)); yy+=24
        wc=WORKING_CAPITAL
        self.screen.blit(self.fs.render("Cash cycle: %d days (Inv %d + Rec %d - Pay %d)"%(
            wc["cash_conversion_cycle_days"],wc["inventory_days"],
            wc["receivables_days"],wc["payables_days"]),True,C_TEXT),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Inventory: $%.1fB  Receivables: $%.1fB"%(
            wc["inventory_value_year10_usd"]/1e9,wc["receivables_value_year10_usd"]/1e9),True,C_TEXT_DIM),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fs.render("Payables: $%.1fB  NWC: $%.1fB"%(
            wc["payables_value_year10_usd"]/1e9,wc["net_working_capital_year10_usd"]/1e9),True,C_TEXT_DIM),(col3_x+12,yy)); yy+=15
        self.screen.blit(self.fmicro.render("  Financing: %s"%wc["working_capital_financing"][:50],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        self.screen.blit(self.fmicro.render("  Seasonality: %s"%wc["seasonality"][:50],True,C_TEXT_DIM),(col3_x+16,yy)); yy+=12
        # Live status
        yy+=8; pygame.draw.line(self.screen,C_PANEL_HI,(col3_x+8,yy),(col3_x+pw-8,yy),1); yy+=8
        self.screen.blit(self.fb.render("LIVE STATUS",True,C_AI),(col3_x+12,yy)); yy+=24
        live=[
            ("Vessel mode",pt.vessel_mode),
            ("Speed","%.1f kn"%pt.speed_kn),
            ("Battery SOC","%.0f%%"%(pt.soc*100)),
            ("H2 buffer","%.1f t"%(pt.h2_kg/1000)),
            ("Juveniles produced","%.1fB"%(pt.juveniles_produced/1e9)),
            ("Total revenue","$%.2fB"%((pt.total_revenue_usd or 0)/1e9)),
            ("Carbon credit","$%.1fM"%((pt.carbon_credit_usd or 0)/1e6)),
        ]
        for lab,val in live:
            self.screen.blit(self.fs.render(lab,True,C_TEXT_DIM),(col3_x+12,yy))
            col=C_GOOD if val in ("True","DRIFT") else C_TEXT
            self.screen.blit(self.fs.render(str(val),True,col),(col3_x+pw-16-self.fs.size(str(val))[0],yy)); yy+=16
        self.screen.set_clip(None)
        # Clamp scroll
        col1_bottom=yy+scroll_y-top_y
        max_scroll=max(0,col1_bottom-ph+100)
        self.quota_scroll=max(0,min(self.quota_scroll,max_scroll))

    def draw_help(self):
        w,h=560,400; x=(self.W-w)//2; y=(self.H-h)//2
        panel(self.screen,x,y,w,h,alpha=240)
        self.screen.blit(self.fb.render("CONTROLS",True,C_ACCENT),(x+20,y+16))
        lines=["TAB            cycle SHIP / ENGINE / HATCHERY / CRUISE / MAP / OPS / INNOV / COMPANY / QUOTA",
            "or click       mode tabs in the top bar",
            "mouse drag     orbit the model","right-drag     pan     wheel  zoom",
            "click part     pin it in the inspector (left sidebar)",
            "1 2 3 4        full / exploded / assembly / section-cut",
            "E              quick exploded toggle","X              cross-section half-cut toggle",
            "L              toggle part labels","R              reset the camera",
            "[  ]           step the assembly build","A / C          assemble all / clear",
            ",  .           slow / speed up TIME-WARP (CRUISE)",
            "F1 F2 F3 F4    vessel mode: DRIFT / HARVEST / TRANSIT / STORM",
            "V              verification checklist overlay",
            "I              full informational specification",
            "H              this help     ESC / Q  quit     F11  fullscreen"]
        for i,ln in enumerate(lines):
            self.screen.blit(self.font.render(ln,True,C_TEXT),(x+24,y+52+i*22))

    def draw_info(self):
        w,h=760,self.H-90; x=(self.W-w)//2; y=50
        panel(self.screen,x,y,w,h,alpha=244)
        self.screen.blit(self.fb.render("TIGER LEVIATHAN-CLASS  --  FULL SPECIFICATION",True,C_ACCENT),(x+20,y+14))
        self.screen.blit(self.fs.render("scroll: up/down arrows   close: I",True,C_TEXT_DIM),(x+w-250,y+20))
        clip=pygame.Rect(x+16,y+46,w-32,h-60); self.screen.set_clip(clip)
        yy=y+50-self.info_scroll; maxpx=w-60; total=0
        for head,lines in self.info_sections:
            if yy>y+30 and yy<y+h: self.screen.blit(self.fb.render(head,True,C_H2),(x+24,yy))
            yy+=26; total+=26
            for ln in lines:
                for wl in wrap_text(self.font,ln,maxpx):
                    if y+30<yy<y+h: self.screen.blit(self.font.render(wl,True,C_TEXT),(x+30,yy))
                    yy+=20; total+=20
            yy+=12; total+=12
        self.screen.set_clip(None)
        self.info_scroll=max(0,min(self.info_scroll,max(0,total-(h-70))))

    def run(self):
        _print_banner()
        while self.running:
            dt=self.clock.tick(60)/1000.0; dt=min(dt,0.05)
            self.handle_events(dt); self.update(dt); self.draw()
        pygame.quit()


def _print_banner():
    dt_t,dt_c=_diesel_ref()
    print("="*70)
    print(" Leviathan.py  --  TIGER LEVIATHAN-CLASS DIGITAL TWIN")
    print("="*70)
    print(" Modes (TAB):  SHIP | ENGINE | HATCHERY | CRUISE | MAP | OPS | INNOV | COMPANY | QUOTA")
    print(" Vessel:       %d m pentamaran, %d t displacement"%(SHIP["loa_m"],SHIP["displacement_t"]))
    print(" Hatchery:     %d broodstock females, %.0fB juveniles/yr/vessel"%(
        DIMS["broodstock_females"],shrimp_juveniles_per_vessel_per_year()/1e9))
    print(" Fleet (12):   %.1fT juveniles/yr, %.0fM t harvest biomass"%(
        fleet_juveniles_per_year(12)/1e12,shrimp_harvest_biomass_tonnes()*12/1e6))
    print(" Fuel:         sunlight + seawater -> onboard hydrogen  ($0 fuel)")
    print("                SE.py rotary H2 engine = FREE fuel for ships,")
    print("                mega-platforms, and hatcheries. No diesel needed.")
    print(" Hull:         superhydrophobic SiO2 nano-coating (22%% drag cut)")
    print("               + air lubrication microbubbles = 34%% total drag reduction")
    print(" Vessel modes: F1=DRIFT  F2=HARVEST  F3=TRANSIT  F4=STORM")
    print(" Catch:        8500 kg/hr trawl, AI sorting, 97%% bycatch escape")
    print(" Recapture:    CRISPR-Cas9 DNA barcoding, 65%% target rate")
    print("               Acoustic + pheromone conditioning (was 35%%, now 65%%)")
    print(" Algae farm:   %.0f t/yr FREE shrimp feed (photosynthesis)"%algae_production_t_per_year())
    print("               Sun + CO2 + seawater -> algae -> feed. $0/kg (like fuel)")
    print(" Feed:         100%% self-sufficient: biofloc 50%% + algae 30%% + BSF 15%% + yeast 5%%")
    print("               Biofloc: bacteria eat shrimp waste -> protein flocs (50%% feed)")
    print("               BSF larvae eat waste -> 42%% protein feed (15%%)")
    print("               Yeast: H2 + CO2 -> 80%% protein (5%%, protein from air+water)")
    print(" AI systems:   FULLY AUTONOMOUS (SAE J3010 Level 5)")
    print("               Self-driving | Self-breeding | Self-herding | Self-maintaining")
    print("               75 crew = supervisory only. AI operates all systems.")
    print("               Swarm intelligence coordinates all 12 vessels")
    print(" Finance:      $%.1fB investment -> $%.0fT target valuation (Year %d)"%(
        FINANCE["investment_usd"]/1e9,FINANCE["target_valuation_usd"]/1e12,FINANCE["target_years"]))
    print(" Innovations:  14 upgrades: OTEC 3MW 24/7 + perovskite 35%% solar +")
    print("               IMTA seaweed + anaerobic digester +")
    print("               floating solar rafts + AUV fleet + continuous release +")
    print("               hybrid fleet (1,200 AI trawlers + 3,500 partners) + swarm AI")
    print(" Controls:     H = help,  I = full spec,  V = checklist,  F11 = fullscreen,  ESC = quit")
    print(" Tabs:         SHIP | ENGINE | HATCHERY | CRUISE | MAP | OPS")
    print("               MAP = global seasonal routes & sea planning")
    print("               OPS = operation plan, fleet rollout & AI status")
    print("               I = full spec (includes 14 innovation upgrades)")
    print("="*70)


def main():
    App().run()


if __name__=="__main__":
    main()
