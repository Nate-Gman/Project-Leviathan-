# Tiger Leviathan-Class Vessel — Operation & Launch Plan

## 1. Vessel Operational Modes

The Tiger Leviathan operates in four primary modes, selectable via F1–F4 in the digital twin or via bridge command:

### 1.1 DRIFT Mode (F1)

| Parameter | Value |
|---|---|
| Primary Propulsion | Ocean current (1.8 kn baseline) |
| Sail Assist | Minimal sail (120 m² deployed, +1.2 kn) |
| Max Speed | 4.0 kn |
| Power Draw | 180 kW (hotel load + hatchery) |
| Hull Mode | Superhydrophobic active |
| Ballast | Light (minimum draft) |
| Hatchery | Active — full production + release |
| Sail Deployment | Minimal (wind >1.5 m/s) |

**Operational Profile:**
- Vessel drifts on ocean currents with minimal sail deployment
- Superhydrophobic hull coating reduces drag by 22%, enabling drift at <2 kn even in calm conditions
- All energy from solar (day), heave-oars, rotors, and tunnel turbines
- H2 engine OFF — zero fuel consumption
- Hatchery at full production: broodstock spawning, larval rearing, nursery grow-out, continuous trickle releases (35M/hr)
- Default mode for nursery ground operations

**Transformation Sequence:**
1. Retract full sails (if deployed), deploy minimal sail (120 m²)
2. Deactivate propulsion pods (switch to regeneration mode)
3. Activate superhydrophobic hull coating verification
4. Lighten ballast (pump out to minimum draft)
5. Confirm hatchery systems at full capacity
6. Transformation time: ~60 seconds (simulated)

### 1.2 HARVEST Mode (F2)

| Parameter | Value |
|---|---|
| Trawl Speed | 3.5 kn |
| Trawl Width | 120 m |
| Trawl Depth | 45 m |
| Mesh Size | 28 mm |
| Trawl Power | 1,200 kW |
| Catch Rate | 8,500 kg/hr |
| Processing Rate | 12,000 kg/hr |
| Bycatch Escape | 97% (AI-assisted sorting) |
| Hull Mode | Superhydrophobic active |
| Ballast | Harvest (balanced) |

**Operational Profile:**
- Active trawl deployment for shrimp harvesting — bulk deck trawl (below) or the FARM drone spread fencing a located school into the TED/BRD smart trawl (Section 14)
- Trawl deploys in 25 minutes (animated transformation); a drone-fenced set runs ~4 h and lands ~40 t
- AI-assisted sorting with 97% bycatch escape ratio
- H2 engine supplements power when battery SOC <25%
- Catch tracked in real-time (session + cumulative)
- Processing onboard: sorting, freezing, packaging

**Transformation Sequence:**
1. Deploy trawl nets (120 m width, 45 m depth, 25 min)
2. Adjust speed to 3.5 kn trawl speed
3. Activate AI sorting system
4. Balance ballast for trawl stability
5. Confirm superhydrophobic hull active (reduces trawl drag)
6. Transformation time: 25 minutes (trawl deployment)

### 1.3 TRANSIT Mode (F3)

| Parameter | Value |
|---|---|
| Target Speed | 12.0 kn |
| Max Speed | 18.0 kn |
| Sails | Deployed (>3.5 m/s wind) |
| Rotors | Deployed (always-on) |
| Hull Mode | Superhydrophobic active |
| Ballast | Transit (optimized trim) |

**Operational Profile:**
- High-speed cruise between nursery grounds
- Full sail deployment (10 masts × 900 m² = 9,000 m² total)
- All energy harvesting systems active: solar, rotors, heave-oars, tunnel turbines, weight harvesters
- H2 engine engages when battery SOC <25%, disengages at >70%
- Flywheel provides burst power for acceleration
- Superhydrophobic hull reduces drag by 22% at transit speeds
- Hatchery continues production during transit

**Transformation Sequence:**
1. Retract trawl (if deployed)
2. Deploy full fabric sail array (automated, wind-triggered)
3. Activate all rotor arrays
4. Set transit ballast (optimized trim)
5. Engage propulsion pods at transit power
6. Transformation time: ~90 seconds

### 1.4 STORM Mode (F4)

| Parameter | Value |
|---|---|
| Ballast Time | 28 minutes (+23,185 t seawater taken on) |
| Waterplane Fraction | ~12% of box area (semi-submerged, columns flooded) |
| Storm Displacement | 153,851 t |
| Storm GM | 5.66 m |
| Max Roll | 3.7 deg in the Cat-5 design sea (verified) |
| Heave Response | 1.8 m in 18 m waves |
| Air Gap | 23 m clear deck-to-wave |
| Survival Wind | 175 kn (Cat 5) |
| Survival Wave Height | 18 m at 12 s period |
| Hull Mode | Superhydrophobic active |
| Ballast | Storm (fully ballasted down) |
| Propulsion | Minimal (station-keeping only) |
| Hatchery | Secured (production paused) |

**Operational Profile:**
- Emergency survival mode for Category 5 hurricane conditions
- Full ballast deployment in 28 minutes → vessel submerges to ~12% waterplane (+23,185 t)
- Minimal power: hotel load + emergency systems only
- Sails furled, rotors locked, trawl retracted
- Hatchery secured: pumps on backup, feeding paused
- Superhydrophobic hull reduces wave impact loads
- Vessel rides out storm with 3.7 deg roll (verified audit figure; design allowance <10 deg)

**Transformation Sequence:**
1. Furl all sails immediately
2. Lock rotor arrays
3. Retract trawl (if deployed)
4. Open all ballast tanks → flood to storm draft
5. Secure hatchery systems (backup power)
6. Switch to emergency power mode
7. Transformation time: 28 minutes (ballast-limited)

---

## 2. Launch Sequence

### 2.1 Pre-Launch Checklist

- [ ] Hull integrity verified (all 5 hulls pressure-tested)
- [ ] Superhydrophobic coating applied and verified (contact angle ≥150°)
- [ ] All 6 H2 tanks filled to 350 bar (120 t total)
- [ ] Battery bank charged to 65% SOC (117 MWh)
- [ ] All 4 azimuth pods tested (360° rotation, forward/reverse)
- [ ] Solar canopy integrity verified (45,600 m² fixed + 60,000 m² towed rafts)
- [ ] Hatchery RAS systems cycled for 7 days continuous
- [ ] Broodstock loaded (200,000 females *P. monodon*)
- [ ] Feed inventory loaded (30-day supply)
- [ ] DNA barcoding lab operational (CRISPR-Cas9 markers ready)
- [ ] Crew aboard (75 personnel — AI operates all systems; crew is supervisory + emergency)
- [ ] Storm mode ballast system tested (full deployment <28 min)
- [ ] Communication systems online (satellite, AIS, weather routing)
- [ ] Release chutes tested (hydraulic gate operation)

### 2.2 Launch Day Sequence

| Time | Action |
|---|---|
| T-4:00 | Final hull inspection, confirm all checklist items |
| T-3:00 | Crew briefing, bridge systems activation |
| T-2:00 | H2 engine cold-start test (5 min idle, verify steam loop) |
| T-1:30 | Solar canopy power output verification |
| T-1:00 | Disconnect shore power, switch to battery + solar |
| T-0:30 | Release lines prepared, tugs stationed |
| T-0:10 | All systems GO/NO-GO poll (bridge + engineering + hatchery) |
| T-0:00 | **LAUNCH** — cast off lines, engage pods at slow-ahead |
| T+0:15 | Clear harbor, increase to TRANSIT mode (12 kn) |
| T+1:00 | First open-sea systems check: all energy flows nominal |
| T+2:00 | Switch to DRIFT mode at first nursery ground |
| T+2:30 | Begin hatchery production cycle (broodstock spawning) |

---

## 3. Deployment Timeline (10-Year Plan)

### Year 1: Vessel Construction & Sea Trials

| Quarter | Milestone |
|---|---|
| Q1 | Hull fabrication begins (shipyard Phase 1) |
| Q2 | Hull assembly, ballast system installation |
| Q3 | Deck, superstructure, solar canopy installation |
| Q4 | Energy & propulsion systems, hatchery fit-out |

**Budget:** $2.5 billion (vessel construction)

### Year 2: Commissioning & First Production

| Quarter | Milestone |
|---|---|
| Q1 | Sea trials, storm mode verification, crew training |
| Q2 | First deployment to equatorial nursery grounds |
| Q3 | First hatchery production cycle (broodstock → larvae → PL20) |
| Q4 | First juvenile release (target: 50 billion juveniles) |

**Budget:** $1.0 billion (commissioning, crew, initial operations)
**Cumulative:** $3.5 billion

### Year 3: Full Production & Fleet Expansion

| Quarter | Milestone |
|---|---|
| Q1 | Vessel 1 at full production (1.32 trillion PL20 + 370 million juveniles/year) |
| Q2 | Begin construction of Vessels 2–4 (3 additional) |
| Q3 | First harvest cycle (trawl mode, catch tracking) |
| Q4 | DNA barcoding recapture data: verify >50% recapture rate |

**Budget:** $4.0 billion (3 additional vessels + operations)
**Cumulative:** $7.5 billion

### Year 4: Fleet at 6 Vessels

| Quarter | Milestone |
|---|---|
| Q1 | Vessels 2–4 launched and deployed |
| Q2 | Begin construction of Vessels 5–6 |
| Q3 | Fleet production: ~7.9 trillion PL20 + 2.2 billion juveniles/year (6 vessels) |
| Q4 | First commercial harvest revenue |

**Budget:** $2.5 billion (2 additional vessels + operations)
**Cumulative:** $10.0 billion

### Year 5: Full Fleet (12 Vessels) & $4 Trillion Valuation

| Quarter | Milestone |
|---|---|
| Q1 | Vessels 5–6 launched |
| Q2 | Begin construction of Vessels 7–12 |
| Q3 | Fleet at 6 vessels: ~7.9 trillion PL20 + 2.2 billion juveniles/year |
| Q4 | **$4 trillion valuation achieved** (biomass ownership + recapture revenue) |

**Budget:** $1.0 billion (operations, Vessels 7–12 construction)
**Cumulative:** $11.0 billion

### Years 6–10: Market Domination

| Year | Fleet Size | Annual Release (PL20 + juveniles) | Annual Revenue |
|---|---|---|---|
| 6 | 8 vessels | 10.6 T + 3.0 B | $800 B |
| 7 | 10 vessels | 13.2 T + 3.7 B | $1.2 T |
| 8 | 12 vessels | 15.9 T + 4.4 B | $1.6 T |
| 9 | 12 vessels (full) | 15.9 T + 4.4 B | $2.0 T |
| 10 | 12 vessels (full) | 15.9 T + 4.4 B | $2.4 T |

---

## 4. Investment Summary

### No-Risk Investment Thesis

| Metric | Value |
|---|---|
| Total Investment | $10–11 billion |
| Valuation at Year 5 | $4 trillion+ |
| ROI (5-year) | 363× |
| Shrimp Recapture Rate | 65% steady-state (Y1 35% → Y2 62% ramp; DNA-barcoded audit trail) |
| Fleet Production (Year 5+) | 15.9 trillion PL20 + 4.4 billion juveniles/year |
| Annual Revenue (Year 10) | $2.4 trillion |
| Fuel Cost | $0 (self-generated hydrogen) |
| Engine-Off Time | >60% of voyage time |

### Revenue Streams

1. **Shrimp Harvest:** Tagged juveniles grow to 300g harvest size in wild; recaptured via licensed fishing fleets paying royalty
2. **Biomass Ownership:** CRISPR-Cas9 DNA markers prove legal ownership of released shrimp
3. **Carbon Credits:** Zero-fuel operation + ocean restoration = tradeable carbon offsets
4. **Technology Licensing:** Rotary H2 engine, superhydrophobic hull, RAS hatchery IP
5. **Data Sales:** Ocean current, weather, marine biology data to research institutions

### Risk Mitigation

| Risk | Mitigation |
|---|---|
| Storm damage | STORM mode: Cat 5 survival, 3.7° roll verified |
| Fuel cost volatility | $0 fuel — self-generated H2 from seawater |
| Biofouling | Superhydrophobic coating: 85% reduction |
| Disease in hatchery | RAS + ozone + AI monitoring, isolated tanks |
| Recapture uncertainty | DNA barcoding proves ownership; 65% conditioned target + drone-fenced capture |
| Crew safety | 75 crew (supervisory), storm mode, redundant systems |
| Regulatory | DNA markers = legal biomass ownership framework |

---

## 5. Operational Cycle (Weekly)

### Standard Nursery Ground Operation

| Day | Mode | Activity |
|---|---|---|
| 1–5 | DRIFT | Hatchery production, continuous trickle release (35M/hr), current-driven drift |
| Continuous | DRIFT | **Two-tier release** — PL20 mass + 7.5g juvenile edge seeding (GPS-guided, timed to tides, dusk windows) |
| Per set | FARM | **Drone-herding sets** — 48-drone fence drops in ~4 min, swims formation, walks school to smart trawl (4 h/set, up to 6 sets/day) |
| 6 | HARVEST | Smart-trawl lift + partner-fleet coordination; cod-end closes at 40 t estimate |
| 7 | TRANSIT | Relocate to next nursery ground (12 kn, 4–8 hours) |

### The Seasonal Ranch Cycle (per zone)

Three-plus rotating ranch zones (~80 km x 20 km) run the enhance-don't-mine cycle:

| Phase | Season | Days | Operations |
|---|---|---|---|
| RELEASE | spring | 45 | Drone-assisted release + nutrient boosters (6 t/zone) |
| GROW | summer | 90 | AUV survey grid, eDNA census, enrichment drift |
| HERD+HARVEST | autumn | 60 | Drone fence -> smart trawl sets, adults only |
| REST+ROTATE | winter | 170 | Zone rests (2 fallow years); fleet moves to next zone |

### Storm Response Protocol

1. **Detection:** Weather satellite + onboard barometer alert (24-hr warning)
2. **Decision:** Bridge commander orders STORM mode if Cat 3+ approaching
3. **Transformation:** Furl sails, lock rotors, retract trawl, flood ballast (28 min)
4. **Ride-out:** Semi-submerged at ~12% waterplane, 3.7° roll + 6.8° wind heel in the Cat-5 design sea (verified); GM 5.66 m storm-ballasted
5. **Recovery:** Pump out ballast, resume DRIFT or TRANSIT mode
6. **Inspection:** Hull integrity scan, hatchery system check, resume operations

---

## 6. Crew Operations (75 -- AI Autonomous)

The vessel runs at SAE Level 5 autonomy; the crew is **supervisory + emergency response only**. AI autonomy reduced the complement from 150 to 75 (saving $10.5M/vessel/year). Every station retains a human override.

### Bridge Watch (24/7) -- 7

- **Captain:** 1
- **Watch Officers:** 4 (6-hour rotating watches)
- **Weather Router:** 1 (real-time storm tracking)
- **AI Systems Officer (bridge):** 1

### Engineering (24/7) -- 8

- **Chief Engineer:** 1
- **Watch Engineers:** 4 (6-hour rotating watches)
- **H2 Systems Specialist:** 1
- **Electrical/Electronics:** 1
- **Predictive-Maintenance Tech:** 1 (robotic arms, 3D-printed spares)

### Hatchery & Aquaculture (24/7) -- 40

- **Hatchery Manager:** 1
- **Aquaculture Biologists:** 5 (selective-breeding program, health)
- **Broodstock Team:** 8 (spawning, egg collection, water quality)
- **Larval Team:** 10 (nauplii→PL20 rearing, feeding, O2 management)
- **Nursery Team:** 8 (PL20→juvenile grow-out, biofloc management)
- **Feed Production:** 3 (algae, BSF, biofloc, yeast)
- **DNA Lab:** 3 (CRISPR barcoding, PCR, batch tracking)
- **Release Team:** 2 (chute operation, GPS release planning)

### Deck & Farm Operations (Day shift) -- 15

- **Bosun:** 1
- **Deckhands:** 6 (sail operation, trawl deployment, maintenance)
- **Drone/Herding Operators:** 4 (reel spread, magazine, drone turnaround)
- **Harvest Processing:** 4 (sorting, freezing, packaging oversight)

### Support -- 5

- **Medical Officer:** 1
- **Security:** 2
- **Cook/Steward:** 2

**Total:** 75 crew

---

## 7. Catch Processing Pipeline (HARVEST Mode)

Two harvest systems work in parallel:

- **Drone-herded smart trawl (FARM spread):** 48 tethered drones fence a located school into a 16 m mouth, TED/BRD four-panel otter trawl — 40 t sets, 90% shrimp purity, up to 6 sets/day. This is the precision harvest of released cohorts inside ranch zones.
- **Bulk trawl (ship deck trawl):** 120 m width described below — used for partner-fleet offload consolidation and opportunistic sets on open grounds.

### Trawl Operations

| Parameter | Value |
|---|---|
| Trawl Width | 120 m |
| Trawl Depth | 45 m |
| Mesh Size | 28 mm |
| Tow Speed | 3.5 kn |
| Deploy Time | 25 minutes |
| Catch Rate | 8,500 kg/hr |
| Processing Rate | 12,000 kg/hr |

### Onboard Processing

1. **AI Sorting:** Computer vision identifies species; 97% bycatch escape ratio
2. **Freezing:** Blast freezer capacity 10,000 kg/hr at -40°C
3. **Packaging:** Automated packaging line at 8,000 kg/hr
4. **Frozen Storage:** 5,000 t capacity hold
5. **Bycatch:** 3% discarded (mostly jellyfish, small fish — returned to sea alive)

### Catch Revenue

| Metric | Value |
|---|---|
| Shrimp Price | $14/kg |
| Daily Catch (24hr trawl) | ~204 t |
| Daily Revenue | ~$2.86M |
| Annual Revenue (200 trawl days) | ~$572M per vessel |

---

## 8. Recapture & DNA Barcoding System

### How It Works

1. **CRISPR-Cas9 Barcoding:** Every batch of released animals receives a unique DNA barcode marker at the chute
2. **Two-tier release:** GPS-guided timed release into nursery grounds via 8 DNA-barcoded 2.0 m chutes — 1.32 trillion PL20 (0.02 g, mass release into zone interior) + 370 million juveniles (7.5 g, edge-seeded into sheltered nursery) per vessel per year
3. **Growth:** Released animals grow to 300 g harvest size in ~180 days in the wild — 6% of PL20 and 18% of juveniles survive to harvest under acoustic conditioning + predator saturation
4. **Drone herding:** The 48-drone "fish dog" spread fences the school into TED/BRD smart trawls (95.6% derived delivery, 84% located-to-landed); partner and AI trawlers work the wider grounds
5. **Recapture:** Licensed fleets + own spread land 65% of the released cohort; DNA marker proves ownership of every landed animal — only barcoded shrimp are kept
6. **Settlement:** Partner vessels earn $0.30/kg; OAC retains 65% of harvest value at $7.00/kg wholesale (revenue share 65/35)

### Recapture Economics (per vessel, model-derived)

| Metric | Value |
|---|---|
| Target Recapture Rate | 65% steady-state (Year 1: 35%, Year 2: 62%) |
| Survival to harvest | 6% (PL20) / 18% (juvenile) |
| Harvest Size | 300 g at 180 days |
| Adults at harvest | ~79.5 billion/vessel/yr |
| Landed biomass | ~15.5 M t/vessel/yr (65% recapture) |
| Fleet (12) harvest | 186.1 M t/yr |
| Own-spread share | 57,600 t/yr (0.37% of vessel recapture) — the rest is partner + AI trawlers |

### The Acoustic + Pheromone Programme

| Parameter | Value |
|---|---|
| Conditioning | 200 Hz, 7 days pre-release (8 underwater speakers) |
| Lure | Species-specific crustacean attractant (12 pheromone dispensers) |
| Baseline recapture | 35% (unconditioned ocean ranching) |
| Boost | +30 percentage points → 65% |
| Benchmark | Salmon ocean ranching ~4% |

---

## 9. Free Fuel via SE.py Rotary H2 Engine

### The SE.py Technology

The Tiger Leviathan is powered by the same proven rotary H2 engine technology from SE.py (the HOHEV-H2 Marine Rotary Digital Twin). This makes fuel for ships, mega-platforms, and hatcheries **completely FREE**.

### How Free Fuel Works

1. **Solar Canopy:** 17,600 m² canopy + 28,000 m² deployable wings (45,600 m² fixed total) of perovskite-on-silicon tandem cells (35% efficiency) → 37 MW peak; plus 60,000 m² towed floating rafts (+21 MW) deployed in DRIFT mode
2. **Electrolysis:** 20 MW PEM electrolysers split seawater → H2 + O2 (44 kWh/kg = 76% LHV efficiency)
3. **Storage:** 120 t H2 at 350 bar in 6 Type IV carbon-fiber tanks — 3-4 day buffer
4. **Combustion:** 8-chamber rotary H2 engine burns H2 → electricity (60% efficiency)
5. **Round-trip:** Solar → H2 → electricity ≈ 46% LHV round-trip (sun covers the losses)
6. **Night baseload:** OTEC closed-cycle ammonia plant, 3 MW / 26 MWh per day from the 500 m thermal gradient — no sun required
7. **Cost:** $0.00 per tonne of fuel (vs $950/t for diesel VLSFO)

### Free Fuel Impact

| Metric | Value |
|---|---|
| Fuel Cost | $0 (vs ~$950/t diesel) |
| H2 Self-Sufficiency | >99% (all H2 made onboard from seawater) |
| Engine-Off Time | >60% of voyage (solar + harvesters sufficient) |
| Diesel Saved (per transit) | ~$450,000 per 2,400 nm voyage |
| Annual Fuel Savings (per vessel) | ~$50M+ (vs equivalent diesel ship) |
| Fleet Annual Savings (12 vessels) | ~$600M+/year |

### Application to Mega-Platforms

The SE.py rotary H2 engine technology scales to:
- **Ships:** Any vessel size — replace diesel engines with rotary H2 + solar + electrolysis
- **Mega-Platforms:** Offshore aquaculture platforms, floating cities, energy islands
- **Hatcheries:** Land-based RAS hatcheries powered by solar + H2 (zero grid connection)
- **Cost:** Capital cost only (solar panels + electrolysis + H2 tanks + engine). Fuel is forever free.

---

## 10. Microalgae Photobioreactor Farm (FREE Shrimp Feed)

### The Concept

Just as fuel is FREE (H2 from seawater via SE.py rotary engine), **shrimp feed is also FREE**. The vessel hosts an onboard microalgae farm that uses photosynthesis to produce nutrient-rich algae biomass — the natural food source for shrimp.

### How Free Feed Works

1. **Sunlight:** Free, unlimited energy source (same solar canopy + greenhouse skylights)
2. **CO2:** Captured from atmosphere + hatchery RAS exhaust (closed loop)
3. **Nutrients:** Hatchery wastewater + seawater minerals (zero external input)
4. **Photosynthesis:** Microalgae convert sun + CO2 + nutrients into protein-rich biomass
5. **Harvest:** Centrifuge + drum filter every 3 days
6. **Feed:** 80% of commercial feed replaced by algae — FCR improves from 1.3 to 1.05
7. **Cost:** $0.00/kg (vs $1.20/kg commercial feed)

### Species Cultured

| Species | Role | Protein % |
|---|---|---|
| Spirulina platensis | Primary protein source | 65% |
| Chlorella vulgaris | Lipid + vitamin supplement | 65% |
| Thalassiosira weissflogii (diatom) | Shrimp larval feed | 35% |

### Farm Infrastructure

| Component | Value |
|---|---|
| Open ponds | 40 ponds, 15 m diameter, 0.8 m deep |
| Photobioreactors | 20 PBRs, 3 m diameter, 8 m tall (~15x areal density) |
| Total culture area | ~14,137 m² ponds + PBRs (under ~17,671 m² greenhouse) |
| Growth rate | 150 g/m²/day (25% photosynthetic efficiency) |
| Harvest interval | 2 days (~2,789 kg/day gross) |
| LED night supplement | 200 kW (660nm red + 450nm blue) |
| Pump / draw | 80 kW circulation / 150 kW farm total |
| Storage capacity | 500 t |
| Harvest method | Centrifuge + drum filter |
| Drying method | Solar-thermal spray dryer |
| Quality monitoring | AI + hyperspectral imaging |

### Production & Impact

| Metric | Value |
|---|---|
| Annual production (per vessel) | ~631 t |
| Fleet (12) production | ~7,570 t/yr |
| Commercial feed replaced | 80% (FCR-improving supplement) |
| FCR improvement | 1.3 → 1.05 |
| CO2 captured (per vessel) | ~1,154 t/yr |
| O2 produced (per vessel) | ~757 t/yr |
| Feed cost | $0.00/kg (FREE) |
| Protein / lipid / carb / pigment | 65% / 8% / 20% / 7% |
| Nutrient source | Hatchery wastewater + seawater + digester digestate (closed loop) |
| CO2 source | Atmosphere + hatchery RAS exhaust + electrolyser O2 (closed loop) |

### Scalability to Mega-Platforms

The microalgae farm principle scales to any floating platform:
- **Ships:** Onboard ponds + PBRs (as implemented on Tiger Leviathan)
- **Mega-platforms:** Large-scale greenhouse ponds on deck
- **Floating farms:** Dedicated algae production platforms
- **Land-based hatcheries:** Greenhouse PBR arrays with solar power
- **Cost:** Capital only. Feed = forever free (like fuel).

---

## 11. AI Systems (Fully Autonomous Vessel)

### Overview

The Tiger Leviathan is **FULLY AUTONOMOUS** — AI operates all systems. The 75-person crew is supervisory only (reduced from 150 by AI autonomy). Four AI subsystems + a central orchestrator manage every aspect of vessel operation.

### Central AI Orchestrator

| Component | Value |
|---|---|
| Name | LEVIATHAN CENTRAL AI |
| Hardware | NVIDIA DGX H100 x2 (primary + backup), 256 GB HBM3 |
| Model | Multi-agent reinforcement learning, 5.5B params total |
| Decision latency | 30ms |
| Coordination | gRPC + shared memory |
| Learning mode | Continuous (online learning from all sensor data) |
| Model updates | Weekly (federated learning across fleet) |
| Cyber security | Quantum-resistant encryption, air-gapped backup |
| Human override | Always available (manual control, remote command) |

### 1. Self-Driving (Autonomous Navigation)

| Component | Value |
|---|---|
| Autonomy level | SAE J3010 Level 5 (full autonomous, no human required) |
| Hardware | NVIDIA DRIVE Atlan x4 + redundant IMU + GPS+GLONASS+Galileo |
| Sensors | Radar x4, lidar x2, sonar x8, AIS, satellite weather, optical cameras x16 |
| ML model | Transformer-based trajectory planner, 2.3B params |
| Training data | 10M+ nautical miles simulated + 500K real-world hours |
| Safety record | Zero incidents in 10M sim miles |
| Redundancy | Triple-redundant compute, dual GPS, backup manual override |
| Insurance | Lloyd's Register Autonomous Notation |

**Capabilities:**
- Route optimization (currents, wind, waves, fuel)
- Collision avoidance (ships, ice, debris, marine life)
- Weather routing (storm avoidance, calm-sea seeking)
- Autonomous docking (port approach, mooring)
- Speed optimization (arrive on schedule, minimize energy)
- Auto mode selection (auto-switch DRIFT/HARVEST/TRANSIT/STORM)

### 2. Self-Breeding (Genetic Optimization)

| Component | Value |
|---|---|
| Hardware | GPU cluster (8x A100), genome sequencer (Oxford Nanopore) |
| ML model | GAN-based genotype→phenotype predictor, 1.7B params |
| Generations/year | 4 |
| Genetic gain/generation | 8.0% |
| Diversity target | >0.35 |
| Inbreeding max | <0.125 |
| Database | 10M+ shrimp genomes, 500K phenotype records |

**Capabilities:**
- Broodstock selection (growth rate, disease resistance, size)
- Selective breeding (EBV + genomic selection, no GMO)
- Spawning prediction (eyestalk ablation timing, photoperiod)
- Egg quality assessment (computer vision, 99.2% accuracy)
- Family tracking (pedigree database, inbreeding avoidance)
- Trait optimization (growth +25%, survival +18%, FCR -12%)
- Automatic cross-breeding (maintain genetic diversity >0.35)
- Larval health prediction (first-feeding success >95%)

### 3. Self-Herding (Shrimp School Tracking)

| Component | Value |
|---|---|
| Hardware | Hydroacoustic array x32, satellite ocean color, 48 tethered herding drones + 8 free AUVs |
| ML model | CNN+LSTM school tracker, 850M params |
| Tracking range | 250 km |
| Tracking accuracy | 94% |
| Herding drones | 48 tethered "fish dogs" (12 h endurance, 120 m depth) + 8 AUV scouts (24 h, 500 m) |
| Stimuli | Acoustic 20–100 Hz + 470 nm LED + bubble curtain + 0.5 V/m e-field |
| Formations | wall / funnel / arc / sweep — RL policy retrained fleet-wide every set |
| Satellite revisit | 3.5 hours |
| eDNA sampling | Every 12 hours |
| Recapture prediction accuracy | 87% (85% hotspot prediction per set) |

**Capabilities:**
- Released shrimp school tracking (acoustic + satellite)
- Wild population monitoring (ocean color + eDNA sampling)
- Recapture forecasting (predict when/where shrimp reach harvest size)
- Fishing fleet coordination (auto-negotiate recapture contracts)
- School health monitoring (growth rate, mortality, predation)
- Predator detection (sharks, whales, large fish — alert fishing fleets)
- Migration pattern learning (seasonal, temperature, current-driven)
- Release site optimization (current modeling, predator avoidance)
- Fence formation control (wall / funnel / arc / sweep — RL swarm policy, retrained every set)
- Stimulus auto-tuning (amplitude follows school density + mood)

### 4. Self-Maintaining (Predictive Maintenance)

| Component | Value |
|---|---|
| Hardware | Vibration sensors x480, thermal cameras x24, acoustic monitors x128 |
| ML model | Transformer-based anomaly detector, 1.2B params |
| Total sensors | 660 |
| Prediction accuracy | 96.5% |
| Mean time to detect | 2.0 hours |
| False positive rate | 1.2% |
| Auto-repair capability | 78% of issues |
| Robotic repair arms | 4 |
| 3D spare parts printers | 2 |
| Uptime target | 99.5% |

**Capabilities:**
- Vibration analysis (bearing wear, imbalance, misalignment)
- Thermal monitoring (overheating, insulation degradation)
- Acoustic monitoring (cavitation, leaks, abnormal noise)
- Corrosion prediction (hull coating degradation rate)
- H2 system leak detection (ppb-level sensitivity)
- Battery health (SOC degradation, cell balancing, thermal runaway prediction)
- Hatchery water quality (ammonia, nitrite, pH, O2 — auto-correct)
- Algae farm monitoring (growth rate, contamination, nutrient levels)
- Auto-repair scheduling (3D-printed spare parts, robotic repair)
- Supply chain optimization (predict parts need, auto-order)

### Crew Role

The 75-person crew is **supervisory only**:
- Monitor AI system status and health
- Override in emergencies (manual control always available)
- Scientific research and data validation
- Regulatory compliance and port liaison
- AI does the work; crew ensures safety and oversight

---

## 12. Global Seasonal Routes & Sea Planning

### Overview

The AI self-driving system selects optimal routes by season, balancing sea state, sunlight, currents, shrimp growth rates, algae productivity, and predator risk. The MAP tab in the digital twin shows the world ocean map with all seasonal routes color-coded.

### Spring (Mar-May) — Equatorial Pacific

| Parameter | Value |
|---|---|
| Best zone | Equatorial Pacific (5°N-5°S) |
| Route | Singapore → Banda Sea → Coral Triangle → open Pacific release |
| Reason | Calm seas, high phytoplankton bloom, post-monsoon nutrients |
| Sea state avg | 25% |
| Sun avg | 78% |
| Current | 1.2 kn |
| Water temp | 29°C |
| Shrimp growth | 115% (seasonal factor) |
| Algae productivity | 120% |
| Predator risk | LOW |
| Release zones | Banda Sea, Coral Triangle, Molucca Sea |

### Summer (Jun-Aug) — North Pacific Gyre

| Parameter | Value |
|---|---|
| Best zone | North Pacific Gyre (20°N-35°N) |
| Route | Yokohama → North Pacific → Gulf of Alaska → release zone |
| Reason | Long daylight (max solar), warm surface, productive gyre edges |
| Sea state avg | 30% |
| Sun avg | 92% (maximum) |
| Current | 0.8 kn |
| Water temp | 22°C |
| Shrimp growth | 108% |
| Algae productivity | 135% (maximum, longest daylight) |
| Predator risk | MEDIUM |
| Release zones | North Pacific Gyre, Gulf of Alaska, Bering Sea edge |

### Autumn (Sep-Nov) — Equatorial Atlantic

| Parameter | Value |
|---|---|
| Best zone | Equatorial Atlantic (0°-10°S) |
| Route | Capetown → Gulf of Guinea → Angola Basin → release zone |
| Reason | Benguela upwelling, nutrient-rich, stable trade winds |
| Sea state avg | 28% |
| Sun avg | 72% |
| Current | 1.0 kn |
| Water temp | 27°C |
| Shrimp growth | 112% |
| Algae productivity | 110% |
| Predator risk | LOW |
| Release zones | Gulf of Guinea, Angola Basin, Benguela Current |

### Winter (Dec-Feb) — Indian Ocean

| Parameter | Value |
|---|---|
| Best zone | Indian Ocean (10°S-25°S) |
| Route | Fremantle → Indian Ocean gyre → Mozambique Channel → release |
| Reason | Calm post-monsoon, warm Leeuwin Current, high productivity |
| Sea state avg | 22% (calmest) |
| Sun avg | 85% |
| Current | 1.5 kn (strongest, drift-friendly) |
| Water temp | 28°C |
| Shrimp growth | 118% (highest) |
| Algae productivity | 125% |
| Predator risk | LOW |
| Release zones | Mozambique Channel, Indian Ocean Gyre, Java Sea |

### Hub Ports

| Port | Lat | Lon | Role |
|---|---|---|---|
| Singapore | 1.3°N | 103.8°E | Primary hub (Pacific operations) |
| Yokohama | 35.4°N | 139.6°E | North Pacific hub |
| Fremantle | 32.1°S | 115.7°E | Indian Ocean hub |
| Capetown | 33.9°S | 18.4°E | Atlantic hub |
| Panama | 8.9°N | 79.5°W | Americas hub |

### Release Zones (16 total)

All 16 release zones are tracked across 4 oceans. The AI self-herding system monitors released shrimp schools via hydroacoustic arrays, satellite ocean color, eDNA sampling, and drone swarms.

### Route Selection Logic

The AI self-driving system continuously optimizes routes based on:
1. **Sea state** — calmer seas = less energy, safer hatchery
2. **Sunlight** — more sun = more solar power + algae production
3. **Currents** — favorable currents = drift mode (zero fuel)
4. **Shrimp growth** — warm, nutrient-rich waters = faster growth
5. **Algae productivity** — sunlight + nutrients = more free feed
6. **Predator risk** — avoid zones with high predator activity
7. **Release timing** — coordinate with optimal release conditions

---

## 13. 17 Innovation Upgrades — Cost Reduction & Efficiency Optimization

The following innovations are modelled in the Tiger Leviathan digital twin (Section 3 of `Leviathan.py`). Sixteen are active; **#7 (kite sails) is retained as an evaluated-and-rejected option** so the reasoning survives.

### Energy Innovations

| # | Innovation | Impact | Details |
|---|-----------|--------|---------|
| 1 | **OTEC (Ocean Thermal Energy Conversion)** | 3 MW 24/7 baseload | Closed-cycle ammonia, 500 m cold pipe, uses ocean temp gradient. Complements solar for night power. |
| 2 | **Perovskite tandem solar cells** | +34.6% power from same area | 35% efficiency (was 26% PERC). Perovskite-on-silicon, 25 yr lifespan. |
| 3 | **Air lubrication system** | 12% drag reduction | Microbubbles under hull. Stacks with superhydrophobic coating = 34% total drag cut. |
| 6 | **Anaerobic digester** | 800 kW biogas | Converts shrimp/algae waste to biogas. Digestate feeds algae ponds = closed loop. |
| 7 | **Kite sails** | REJECTED | 500 m² kite at 400 m, 2.5 MW avg — evaluated and dropped; not practical for a shrimp drifter. Solar+OTEC+H2 sufficient. |
| 13 | **Floating solar rafts** | +21 MW peak (drift mode) | 60,000 m² additional solar deployed when stationary. Folds for transit. |

**Combined energy: 24/7 power from solar + OTEC + digester. $0 fuel forever.**

### Feed & Biology Innovations

| # | Innovation | Impact | Details |
|---|-----------|--------|---------|
| 4 | **IMTA seaweed polyculture** | +$3.6M/yr revenue | Kappaphycus + Gracilaria. Removes 18 t N + 2.4 t P/yr, 480 t CO2 sequestered, 10% feed supplement. |
| 5 | **Black Soldier Fly larvae** | 15% feed replacement | 800 t/yr, 42% protein. Eats shrimp processing waste. Closes loop to 100% feed. |
| 12 | **Yeast single-cell protein** | 5% feed replacement | Cupriavidus necator converts H2 + CO2 to 80% protein. Protein from air and water. |
| 16 | **Biofloc system** | 50% feed replacement | Heterotrophic bacteria convert shrimp waste to protein flocs. Shrimp re-eat their waste. |

**Combined feed: 100% self-sufficient (biofloc + algae + BSF + yeast + IMTA). $0 feed cost.**

### Operational Innovations

| # | Innovation | Impact | Details |
|---|-----------|--------|---------|
| 8 | **Acoustic + pheromone recapture** | 35% → 65% recapture | 7-day 200 Hz conditioning + species-specific lure before release. +30 points over baseline. |
| 9 | **Crew reduction** | 150 → 75 crew | AI autonomy. $10.5M/yr/vessel saved ($126M/yr fleet). |
| 10 | **Partner fleet model** | $45.6B CAPEX saved | 3,500 existing fishing vessels + 1,200 AI trawlers. $0.30/kg partner fee, 65/35 share. |
| 11 | **Continuous release** | +5% survival | 35M/hr trickle vs weekly batch. Predator saturation — no learnable pattern. |
| 14 | **AUV fleet** | 8 free scouts | 24 h endurance, 500 m depth. Sonar + camera + eDNA + acoustic receivers. |
| 15 | **Swarm intelligence** | Fleet-wide optimization | Satellite mesh + acoustic. Coordinates all 12 vessels as unified fleet. |
| 17 | **Drone shrimp herding** | +400% catch/set | 48 tethered "fish dog" drones fence schools into a TED/BRD smart trawl — see Section 14. |

### Combined Impact Summary

| Category | Before | After | Savings/Improvement |
|----------|--------|-------|---------------------|
| Energy | Solar only (day) | Solar + OTEC + digester (24/7) | $0 fuel, night power |
| Feed | 70% onboard ($816M/yr) | 100% self-sufficient | $816M/yr saved |
| Drag | 22% reduction | 34% reduction | +12% efficiency |
| Recapture | 35% baseline | 65% | +86% landed biomass |
| Crew | 150/vessel | 75/vessel | $126M/yr fleet |
| Harvest | Blind trawl, 8 t/set | Drone-fenced smart trawl, 40 t/set | +400% per set |
| Trawler CAPEX | $45.6B (1,200 vessels) | $0 incremental (partner model) | $45.6B saved |
| Trawler OPEX | $3.6B/yr | $0 (partner fee $0.30/kg) | $3.6B/yr saved |
| Survival | Batch release | Continuous +5% | More harvest |
| Revenue | Shrimp only | Shrimp + seaweed + carbon + data | +$43.2M/yr fleet |

**Total CAPEX savings: $45.6B+ | Total OPEX savings: $4.5B+/yr | Harvest gain: +400% catch per drone-fenced set**

---

## 14. Drone Shrimp Herding Operations (FARM Spread)

The FARM spread is the signature harvesting system: a reel of tethered underwater drones deploys a moving stimulus fence that walks a located school into the net — sheepdogs, underwater.

### 14.1 Equipment

| Component | Specification |
|---|---|
| Multi-thread reel | 6 drums × 8 grooves = **48 tethered drone lines**, 90 kW servo |
| Magazine | 64-drone carousel (16 slots), 240 kW charge ring |
| Drop chutes | 4 × 40 deg chutes, 1.8 s drop, flared exit + air-bleed ring (<0.3 m splash) |
| Tether | 280 m fibre/electrical umbilical per drone (263 m required to outermost fence slot) |
| Drone | 0.9 m × 0.28 m, 14 kg, 4 kn, 12 h endurance, 120 m depth, 3 ducted thrusters |
| Sensors | Imaging sonar (80 m) + stereo cam + eDNA + DVL + CTD + hydrophone |
| Stimuli | Acoustic 20–100 Hz + 470 nm blue LED + bubble curtain + 0.5 V/m e-field |
| AI | 22 TOPS edge module; RL swarm-herding policy retrained fleet-wide every set; 10 Hz target tracking |
| Free scouts | 8 AUVs (24 h endurance, 500 m depth) survey ahead of the fence |
| Bubble plant | 180 kW compressor feeding per-drone curtain manifolds |
| Set power | 613 kW total (14.7 MWh/day at 6 sets) — inside the 266 MWh/day solar budget |

### 14.2 Set Procedure (~4 h)

1. **Locate:** Free AUVs + headrope sonar census the school; AI picks the formation and fence origin (85% hotspot prediction accuracy)
2. **Drop:** Magazine feeds 4 chutes at 12 drones/min — full 48-drone spread swimming in ~4.0 min
3. **Fence:** Drones take stations 8.3 m apart across the 400 m spread; stimulus amplitude auto-tunes to school density and mood
4. **Drive:** Formation walks the school up-drift toward the net — **wall** (push ahead), **funnel** (converge on mouth), **arc** (close behind then walk), **sweep** (rotating bottom sweep)
5. **Concentrate:** 5x density increase across 25:1 spread-to-mouth funnel; up to 10 nm / 7.4 km² swept per set
6. **Net:** Headrope sonar confirms density; cod-end camera + tension sensors close the set at the 40 t estimate
7. **Lift:** 12 min lift; 28 mm AI-variable mesh + 55° TED + BRD release non-target animals (~90% shrimp purity)
8. **Recover:** Umbilical winch-in at 15 drones/min (~3.2 min) — no swimmer ever enters the water
9. **Turnaround:** 45 min charge + freshwater desalination rinse kills biofilm on the rack; drones re-queued in the carousel

### 14.3 Performance (model-derived, --verify audited)

| Metric | Value |
|---|---|
| Delivery to net mouth | 95.6% (engage × hold × funnel stages) |
| Located-to-landed | 84% end-to-end |
| Coverage | 23 drones required at 9 m stimulus reach vs 48 deployed — gap-free |
| Endurance margin | 4.1 h mission vs 12 h battery = +7.9 h |
| Catch per set | 40 t (vs 8 t unfenced baseline = +400%) |
| Daily catch | 240 t at 6 sets/day |
| Annual own-trawl | 57,600 t at 240 fishing days (0.37% of vessel recapture — partners land the rest) |

### 14.4 Sustainability Controls

- Only DNA-barcoded released cohorts are kept; wild penaeids escape via TED/BRD
- 25% standing-biomass take cap per zone; 2 fallow years per zone in the rotation
- Benthic-safe rockhopper footrope; 2.5 kn tow speed; sets only inside licensed ranch zones
- eDNA + AUV census confirms zone recovery before the next RELEASE phase

---

## 15. Business Plan — From Net to Consumer

The complete value chain, exactly as modelled in the digital twin (`SUPPLY_CHAIN` + `HARVEST_PLAN` + `FINANCE`). Every number below is derived by the model, not asserted.

### 15.1 The 11-Step Supply Chain (steady-state, full fleet)

| # | Step | Duration | Location | Input -> Output |
|---|---|---|---|---|
| 1 | Broodstock spawning | 6 h | Onboard RAS maturation tanks | 200K domesticated P. monodon females -> 1.8T eggs/yr (12 spawns) |
| 2 | Egg incubation | 24 h | Incubation tanks (28-30 C, 32-35 ppt, pH 7.8-8.2) | 1.8T eggs -> 1.7T nauplii (92% hatch) |
| 3 | Larval rearing | 25 days | Larval tanks (Artemia + microdiet, ozone, biofloc) | 1.7T nauplii -> 1.32T PL20 (80%; tank volume is the ceiling, not hatch rate) |
| 4 | Nursery grow-out | 90 days | Flow-through nursery pools, 40 kg/m3 | 435.7M PL20 diverted -> 370.4M juveniles at 7.5 g (85%; capped by onboard feed) |
| 5 | Ocean release | continuous | 8 DNA-barcoded chutes on station | 1.32T PL20 + 370.4M juveniles/vessel -> trickle release, predator saturation |
| 6 | Ocean grow-out | 6 months | Wild ocean, EEZ nursery grounds | -> 79.5B harvestable adults at 300 g (6% PL20 / 18% juvenile survival) |
| 7 | Harvest | 8 h sets | Drone-fenced smart trawl + 3,500 partners | 51.7B recaptured (65%) = 15.5M t live/vessel/yr |
| 8 | Processing | 4 h | 40 processing plants | 186.1M t live -> 115.4M t product (62% yield) |
| 9 | Cold chain | 3 days | 80 distribution centres | 115.4M t at unbroken -18 C, GPS + blockchain tracked |
| 10 | Retail | 2 days | Food service, retail, industrial, pharma, feed, pet | 109.6M t sold at $7.00/kg avg -> ~970B 4oz meals/yr |
| 11 | Donation offload | 4 h | Every docking stop | 5% of product = 5.77M t -> 51.1B free meals -> 75.9M people |

**Per-vessel economics (derived):** 15.5M t live capture -> $67.3B shrimp revenue + $4.06B ancillary -> **$71.4B revenue/vessel/yr**. Fleet: **$856.3B revenue, $347.8B OPEX, $508.6B EBITDA (59%)**.

### 15.2 Product Mix & Pricing (of 115.4M t/yr processed product)

| Product | % of volume | Price | Volume | Revenue |
|---|---|---|---|---|
| IQF frozen 16/20 count | 20% | $8.00/kg | 23.1M t | $184.6B |
| IQF frozen 21/25 count | 25% | $6.50/kg | 28.8M t | $187.5B |
| IQF frozen 26/30 count | 20% | $5.50/kg | 23.1M t | $126.9B |
| IQF frozen 31/40 count | 15% | $4.50/kg | 17.3M t | $77.9B |
| Cooked, peeled | 10% | $7.00/kg | 11.5M t | $80.8B |
| Block frozen | 5% | $3.50/kg | 5.8M t | $20.2B |
| Value-added (paste, powder, oil) | 5% | $12.00/kg | 5.8M t | $69.2B |

Blended realization: **~$7.00/kg** across the mix. Byproducts (chitin $50/kg, astaxanthin $2,000/kg, shrimp oil $30/kg) add **6% of shrimp value = $4.0B/vessel/yr**.

### 15.3 Customer Segments & Channels

| Segment | % revenue | Key customers | Volume | Price |
|---|---|---|---|---|
| Food service distributors | 45% | Sysco, US Foods, Brakes, METRO | 900K t/yr | $9.00/kg |
| Retail chains | 30% | Walmart, Costco, Tesco, Carrefour, AEON, Aldi | 600K t/yr | $11.00/kg |
| Industrial processors | 15% | Thai Union, CP Foods, Trident | 300K t/yr | $7.00/kg |
| Pharmaceutical/nutraceutical | 5% | Astareal, DSM, BASF | 50K t/yr | $50.00/kg |
| Aquaculture feed | 3% | Skretting, Cargill, BioMar | 60K t/yr | $6.00/kg |
| Pet food | 2% | Mars, Nestle Purina, Hill's | 40K t/yr | $5.00/kg |

Channels: direct B2B long-term supply agreements, category managers (private label + branded), commodity contracts, and specialty B2B for extracts.

### 15.4 Ancillary Revenue (per vessel/yr)

| Stream | Value |
|---|---|
| Shrimp sales | $67.3B |
| Byproducts (chitin, astaxanthin, oil) | $4.04B |
| Carbon credits (48,000 t CO2 @ $100/t) | $4.96M |
| Technology licensing | $10.0M |
| Data sales | $2.0M |
| IMTA seaweed | $0.96M |
| **Total** | **$71.4B/vessel -> $856.3B fleet** |

### 15.5 Unit Economics (per kg of product, steady-state)

| Line | Rate (model) |
|---|---|
| Processing | $0.85/kg product |
| Cold chain logistics | $0.45/kg product |
| Partner-fleet fee | $0.30/kg live weight |
| EEZ royalty | 6.5% of harvest value |
| Crew | $140K/person/yr x 75 |
| Maintenance | 3% of vessel value/yr |
| Insurance | 1.2% of vessel value/yr |
| Consumables | $6M/vessel/yr |
| SG&A | 6% of revenue |
| R&D | 4% of revenue |
| Compliance | $60M/yr fleet |
| Fuel / Feed | **$0 / $0** |
| **Total OPEX** | **$3.01/kg product -> $347.8B/yr fleet** |

Break-even: **$3.01/kg** = $0.34 per 4oz meal -- the floor price for protein on Earth.

---

## 16. Processing & Distribution Network

### 16.1 Processing Plants (40 facilities)

| Tier | Plants | Location examples | Capacity | Cost | Staff |
|---|---|---|---|---|---|
| Tier 1 | 4 | Ho Chi Minh City, Mumbai, Guayaquil, Jakarta | 150 t/day | $60M | 1,200 |
| Tier 2 | 3 | Mazatlan, Recife, Manila | 112 t/day | $45M | 900 |
| Named site | 1 | Chittagong, Bangladesh | 87 t/day | $35M | 700 |
| Zone-standard | 32 | TBD siting, zones 2-8 | 100 t/day each | $40M | 800 |

**Standard equipment fit (Tier 1):** IQF freezers x8, peeling lines x4, AI sorting x2, packaging lines x6, metal detectors x3, x-ray scanners x2, vacuum sealers x8, 5,000 t cold storage on-site.

**Certifications:** HACCP + BRCGS + IFS + ISO 22000 (Year 2), ASC + BAP 4-star (Year 3), MSC for the ocean-ranched component (Year 4).

**Output:** IQF 16/20-31/40 counts, cooked peeled tail-on, block frozen, shrimp paste, shrimp powder, value-added.

### 16.2 Cold Chain Specification (QA-audited)

| Stage | Spec |
|---|---|
| Freezing | IQF at -35 C within 4 h of catch |
| Storage | -18 C throughout |
| Transport | Reefer containers -18 C +/- 2 C, GPS + data loggers |
| Integrity target | 99.99% unbroken cold chain |
| Traceability | DNA barcode + batch + timestamp, farm-to-fork |
| Recall | 48 h global recall via DNA batch tracking |
| Shelf life | 24 months frozen, validated monthly |

### 16.3 Distribution Network (80 centres)

| Tier | Centres | Sites | Capacity | Cold storage | Fleet | Cost each |
|---|---|---|---|---|---|---|
| Mega-hubs | 5 | Los Angeles, Rotterdam, Singapore, Dubai, Shanghai | 1,500-2,000 t/day | 12-15K t | 80-150 trucks + rail | $60-80M |
| Regional | 3 | Tokyo, New York, Sao Paulo | 800-1,000 t/day | 6-8K t | 50-60 trucks | $35-40M |
| Regional (planned grid) | 72 | 8 regions x 9 sites | 600 t/day | 5K t | standard | ~$30M |

**Aggregate throughput:** ~60K t/day cold-chain capacity against a fleet output of ~435K t/day live weight -- plant-to-hub scheduling is orchestrated by the same swarm AI that routes the vessels.

### 16.4 Partner-Fleet Logistics

| Vessel class | Count | Catch | Crew |
|---|---|---|---|
| Small trawler (<15 m) | 1,500 | 500 kg/day | 4 |
| Medium trawler (15-25 m) | 1,200 | 1,500 kg/day | 6 |
| Large trawler (25-40 m) | 600 | 3,000 kg/day | 8 |
| Factory trawler (>40 m) | 200 | 8,000 kg/day | 20 |

- **Regions:** SE Asia 1,200 / Latin America 700 / South Asia 600 / West Africa 400 / East Africa 300 / Other 300
- **Kit per vessel:** GPS tracker + AIS + DNA barcode scanner + eDNA sampler
- **Payment:** smart contract -- automatic $0.30/kg on verified DNA-barcoded delivery; 65/35 revenue share
- **Training:** 3-day certification (sustainable catch, TED/BRD use, scanner protocol)
- **Coordination:** swarm AI assigns catch zones, routes, timing; vessels never crowd a zone

---

## 17. Donation Logistics ("No vessel leaves a port without feeding the hungry")

| Parameter | Value |
|---|---|
| Donation share | 5% of all product = 5.77M t/yr |
| Free meals | 51.1 billion x 4oz (113 g) portions/yr |
| People fed | 75.9 million (full 50 g/day annual protein) |
| Per-vessel offload | ~480,750 t/yr across its port stops |
| Port stops | 29 across 25 nations: 18 EEZ ports + 4 seasonal hubs + 7 distribution hubs = 282 port calls/yr |
| EEZ ports (18) | Jakarta, HCMC, Guayaquil, Mumbai, Manila, Bangkok, Recife, Mazatlan, Lima, Lagos, Chittagong, Darwin, Antananarivo, Dakar, Yangon, Colombo, Dar es Salaam, Cartagena -- 245,489 t/yr each, 12 stops/yr, 2.17B meals, 3.23M people |
| Seasonal hubs (4) | Singapore, Yokohama, Fremantle, Capetown -- 122,745 t/yr each, 6 stops/yr |
| Distribution hubs (7) | LA, Rotterdam, Dubai, Shanghai, Tokyo, New York, Sao Paulo -- 122,745 t/yr each, 6 stops/yr |
| Per offload | ~20,457 t uniform across all stops |
| Revenue foregone | $40.4B/yr | Cost to OAC: $7.5B/yr | Tax-deductible $40.4B/yr |
| Handoff | 4 h port-side, fresh or frozen IQF, DNA-barcoded pouches, -18 C |
| Last mile | 8 NGO partners (WFP, FAO, Save the Children, Action Against Hunger, Oxfam, Red Cross/Red Crescent, GAIN, local NGOs) -> community kitchens + food banks within 24 h |
| Expansion | Year 5+: raise to 10% of product; Year 10: 15% target |

**Port stops:** 18 EEZ nations (Jakarta, Ho Chi Minh City, Guayaquil, Mumbai, Manila, Bangkok, Recife, Mazatlan, Lima, Lagos, Chittagong, Darwin, Antananarivo, Dakar, Yangon, Colombo, Dar es Salaam, Cartagena) + 4 seasonal hubs (Singapore, Yokohama, Fremantle, Capetown) + 7 distribution hubs = **29 stops across 25+ nations**.

**NGO partners (8):** UN WFP (last-mile, conflict zones), UN FAO (nutrition monitoring), Save the Children (school meals), Action Against Hunger (feeding centres), Oxfam (community + gender equity), Red Cross/Red Crescent (disaster relief), GAIN (fortification), local NGOs (port-city food banks).

**Nutrition per donated meal:** 27.1 g protein, 300 mg omega-3, 35 mcg iodine, 38 mcg selenium, 1.1 mcg B12, 112 kcal.

---

## 18. Financial Spine (model-derived)

| Metric | Value |
|---|---|
| Total investment | $12.985B ($750M x 12 vessels + $4.0B infrastructure) |
| Fleet revenue (steady state) | $856.3B/yr |
| Fleet OPEX | $347.8B/yr |
| Fleet EBITDA | $508.6B/yr (59% margin) |
| Target valuation | $5.09T (10x EBITDA) |
| Payback | <1 year of steady-state operation |
| 20-yr cumulative net profit | $8.5T (zero-failure simulation) |
| 20-yr cumulative harvest | 3,466M t |
| Stress events survived | 160 storms/disease/equipment events, 0 failures |

**Year-1 financial shape (model):** 3 vessels at 15% of steady output -> 7.0M t harvest, $32.1B revenue, $18.9B EBITDA, $16.9B net, 2,467 employees, 3.8% market share.

**KPI dashboard (operational):** 1.32T PL20 + 370M juveniles released/vessel/yr | 65% recapture | 15.5M t harvest/vessel/yr | 95% uptime | 100% energy + feed self-sufficiency | 97% bycatch escape | 62% processing yield | 99.99% cold-chain integrity | 100% DNA barcode coverage.

**KPI dashboard (financial):** $856B revenue | 59% EBITDA margin | 53% net margin | $3.01/kg break-even | NPV@8% = $2.35T | IRR 300% | payback <1 yr.

---

## 19. Funding Structure & CAPEX Schedule

### 19.1 Sources ($12.985B total)

| Source | Amount | Share | Terms |
|---|---|---|---|
| World Bank / IFC green loan | $4.3B | 33% | 2.5% interest, 20-year term |
| China Exim Bank | $3.2B | 25% | 3.0% interest, 15-year term |
| Saudi PIF | $2.2B | 17% | Equity, 12% stake |
| Founder + team equity | $1.1B | 8% | Equity, 40% stake |
| Operating cash flow (2026+) | $2.2B | 17% | Self-funded from Year-1 EBITDA |

### 19.2 Use of Proceeds (per vessel, straight-line base)

| Asset class | Cost | Life | Salvage | Annual depreciation |
|---|---|---|---|---|
| Hull, columns, pontoons | $412.5M | 25 yr | 10% | $14.85M |
| Hatchery, nursery, RAS | $165.0M | 15 yr | 5% | $10.45M |
| Solar, OTEC, H2 energy | $97.5M | 20 yr | 5% | $4.63M |
| AI, computing, sensors | $45.0M | 5 yr | 0% | $9.00M |
| AUV fleet + drones | $30.0M | 7 yr | 5% | $4.07M |
| **Per vessel** | **$750.0M** | | | **$43.0M/yr** |
| **Fleet (12)** | **$9.0B** | | | **$516.0M/yr** |

Accelerated depreciation available: 3-year write-off on AI/computing, 50% Year-1 bonus on green tech.

### 19.3 CAPEX Phasing (fraction of $12.985B program)

| Year | % | Amount | Focus |
|---|---|---|---|
| 2026 | 42% | $5.45B | Vessels 1-3 + Tier-1 plants + mega-hubs |
| 2027 | 34% | $4.41B | Vessels 4-8 + plants 5-16 + regional centres |
| 2028 | 18% | $2.34B | Vessels 9-12 + plants 17-24 |
| 2029 | 3% | $0.39B | Plants 25-32 + distribution 41-60 |
| 2030 | 2% | $0.26B | Plants 33-40 + distribution 61-80 |
| 2031-35 | 1% | $0.13B | Refits, upgrades, new-species facilities |

---

## 20. 10-Year Financial Model (model-derived, flat $7.00/kg)

| Year | Vessels | Harvest | Revenue | EBITDA | Net | Cumulative | Employees | Share |
|---|---|---|---|---|---|---|---|---|
| 2026 | 3 | 7.0M t | $32.1B | $18.9B | $16.9B | $0.01T | 2,467 | 3.8% |
| 2027 | 8 | 68.2M t | $314.0B | $186.3B | $167.4B | $0.19T | 13,593 | 36.8% |
| 2028 | 12 | 138.5M t | $727.9B | $432.2B | $388.7B | $0.58T | 29,930 | 85.3% |
| 2029 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $1.03T | 35,000 | steady |
| 2030 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $1.49T | 35,000 | steady |
| 2031 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $1.95T | 35,000 | steady |
| 2032 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $2.41T | 35,000 | steady |
| 2033 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $2.86T | 35,000 | steady |
| 2034 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $3.32T | 35,000 | steady |
| 2035 | 12 | 186.1M t | $856.3B | $508.6B | $457.4B | $3.78T | 35,000 | steady |

Model assumptions: $7.00/kg held via market-making volume + EEZ exclusivity, 25-yr vessel life, straight-line depreciation, 17% statutory / 10% effective tax, 90-day working-capital cycle, 8% discount rate.

---

## 21. Unit Economics Detail

### 21.1 OPEX Structure (fleet steady-state, $347.8B/yr)

| Line | Model rate | Annual cost |
|---|---|---|
| Crew | $140K x 75 x 12 vessels + shore staff | ~$4.9B |
| Maintenance + spares | 3% of vessel value | $270M/yr fleet |
| Insurance | 1.2% of vessel value | $108M/yr fleet |
| Consumables | $6M x 12 | $72M |
| Processing | $0.85/kg product | ~$98.1B |
| Cold chain | $0.45/kg product | ~$51.9B |
| Partner fee | $0.30/kg live | ~$55.8B |
| EEZ royalties | 6.5% of harvest value | ~$78.2B |
| SG&A | 6% of revenue | ~$51.4B |
| R&D | 4% of revenue | ~$34.3B |
| Compliance | fixed | $60M |
| Fuel / Feed | solar + algae loop | $0 / $0 |

### 21.2 Working Capital

| Metric | Value |
|---|---|
| Inventory | 60 days frozen product |
| Receivables | 30 days |
| Payables | 45 days |
| Cash conversion cycle | 45 days |
| Net working capital (Y10) | $2.8B |
| Facility | $3B revolver (DBS + JP Morgan, SOFR + 150 bps) |

### 21.3 Tax Structure

| Item | Value |
|---|---|
| Domicile | OAC Holdings Pte Ltd, Singapore (MPA flag state) |
| Statutory rate | 17% |
| Effective rate | 5% (Y1) -> 8% (Y5) -> 10% (Y10) |
| Incentives | Pioneer 5%/15yr, Maritime Sector 5%/10yr, Investment Allowance 100% CAPEX write-off, HQ Award 15%/5yr |
| Tonnage tax option | $4.50/net-tonne available vs corporate tax |
| Treaties | 80+ double-taxation treaties incl. all EEZ nations |
| Dividends | 0% withholding; foreign dividends exempt (headline tax >=15%) |
| Transfer pricing | Arm's-length, OECD-compliant, per-vessel entity agreements |

---

## 22. Sensitivity, Break-Even & Risk

### 22.1 Scenario Analysis (model-derived)

| Scenario | Probability | Assumptions | EBITDA |
|---|---|---|---|
| Optimistic | 20% | Survival 3x base, $7/kg | $1,445.7B |
| Target | 30% | Survival 1.4x base (Y1-3 research goal) | $40.0B |
| Base case | 35% | Published survival, 65% recapture, $7/kg | $508.6B |
| Pessimistic | 15% | Survival halved, 35% recapture | $274.3B |

**Dominant variable:** ocean survival of released stock — it alone swings payback from ~9 days to ~10 years. Vessel cost, crew and price move outcomes by tens of percent; survival moves them by multiples.

### 22.2 Break-Even Analysis

| Metric | Value |
|---|---|
| Break-even price | $3.014/kg product |
| Break-even harvest | 80.1M t/yr (43% of steady output) |
| Fixed costs | $636M/yr |
| Variable cost | $1.30/kg |
| Contribution margin | $5.70/kg |
| Break-even year | 2026 (first operating year) |

Survival sensitivities: x0.5 -> 93.0M t / $274B EBITDA | x1.0 -> 186.1M t / $509B | x3.0 -> 558M t / $1,446B. Recapture at 35% instead of 65% -> 100.2M t.

### 22.3 Risk Register (summary — full playbook in §24)

| Risk | Prob. | Impact | Response | Cover |
|---|---|---|---|---|
| Vessel loss | low | severe | Evacuate, insure, replacement in 18 mo | $2.0B |
| Disease (EMS/AHPND/WSSV) | medium | moderate | No net-pen density; eDNA monitor; broodstock quarantine | $0.5B |
| EEZ revocation | low | moderate | 18-nation spread; UNCLOS arbitration; relocate | self-insured |
| Food-safety recall | low | severe | 48-h DNA-barcode recall; root-cause + transparency | $0.5B |
| Cyber attack | medium | moderate | Air-gapped controls, manual override, SOC 2 | $0.2B |
| Storm (Cat 5) | medium | low | STORM mode: 3.7 deg roll verified, never flees | hull + BI |
| Market collapse | low | medium | $3.01/kg cost floor — profitable at any survivable price | n/a |

### 22.4 Regulatory & Certification Path (summary — full matrix in §25)

| Jurisdiction | Agencies | Compliance route | Timing |
|---|---|---|---|
| Maritime | IMO (SOLAS, MARPOL, BWM) | Compliant by design; Lloyd's + DNV class | At launch |
| Fisheries | FAO Code of Conduct | Exceeds standards; MSC ocean-ranched pending | Year 4 |
| USA | FDA HACCP (21 CFR 123), NOAA, USCG | FDA registration + USCG COI | Year 1 |
| EU | EFSA, EMSA, EU Aquaculture Reg | EU health certificate, IFS | Year 2 |
| China | GACC, Maritime Safety | GB 2733 aquatic product standards | Year 2 |
| EEZ nations | 18 licensing ministries | ITQ-style licences + 5-8% royalty + DNA audit trail | Before first release |

---

## 23. EEZ Licensing & Market Access ($895M one-time, 90 release zones)

Exclusive ocean ranching rights negotiated with 18 EEZ nations. This is the **market-access layer** of the business plan: no licence = no release zone, no recapture rights, no distribution territory.

### 23.1 Licence Portfolio (model-derived)

| Nation | EEZ area | Fee | Royalty | Term | Zones | Naval base |
|---|---|---|---|---|---|---|
| Indonesia | 6.0M km2 | $120M | 8.0% | 25 yr | 12 | Jakarta |
| Vietnam | 1.1M km2 | $80M | 7.0% | 20 yr | 8 | Ho Chi Minh City |
| India | 2.3M km2 | $90M | 7.5% | 20 yr | 10 | Mumbai |
| Ecuador | 1.0M km2 | $60M | 6.0% | 20 yr | 6 | Guayaquil |
| Philippines | 2.2M km2 | $70M | 7.0% | 20 yr | 8 | Manila |
| Australia | 8.5M km2 | $100M | 8.0% | 20 yr | 5 | Darwin |
| Brazil | 3.6M km2 | $85M | 7.0% | 20 yr | 6 | Recife |
| Mexico | 3.1M km2 | $65M | 6.5% | 20 yr | 5 | Mazatlan |
| Peru | 0.9M km2 | $45M | 6.0% | 15 yr | 4 | Lima |
| Thailand | 0.3M km2 | $30M | 6.0% | 15 yr | 4 | Bangkok |
| Colombia | 0.6M km2 | $28M | 6.0% | 15 yr | 3 | Cartagena |
| Nigeria | 0.2M km2 | $25M | 5.0% | 15 yr | 3 | Lagos |
| Sri Lanka | 0.5M km2 | $22M | 6.0% | 15 yr | 3 | Colombo |
| Madagascar | 0.5M km2 | $20M | 5.0% | 15 yr | 3 | Antananarivo |
| Myanmar | 0.5M km2 | $18M | 5.0% | 15 yr | 3 | Yangon |
| Bangladesh | 0.1M km2 | $15M | 5.0% | 10 yr | 3 | Chittagong |
| Senegal | 0.2M km2 | $12M | 5.0% | 10 yr | 2 | Dakar |
| Tanzania | 0.2M km2 | $10M | 5.0% | 10 yr | 2 | Dar es Salaam |
| **Total** | **31.8M km2** | **$895M** | **6.5% blended** | 10-25 yr | **90** | 18 |

- **Blended royalty** flows through OPEX as the $55.6B/yr "EEZ licenses" line.
- **Concentration cap**: no single nation controls >18% of grounds (Indonesia largest).
- **DNA-barcode audit trail** proves recaptured shrimp are our released stock -- the legal backbone distinguishing ranching from wild extraction.

### 23.2 Quota Zones (TAC vs MSY, 20% buffer)

| Zone | TAC (M t/yr) | MSY (M t/yr) | Harvest < MSY |
|---|---|---|---|
| Indonesia EEZ | 46.5 | 58.2 | 20% buffer |
| Vietnam EEZ | 28.8 | 36.1 | 20% buffer |
| Ecuador EEZ | 22.3 | 27.9 | 20% buffer |
| India EEZ | 20.5 | 25.6 | 20% buffer |
| Philippines EEZ | 14.9 | 18.6 | 20% buffer |
| Brazil EEZ | 12.3 | 15.4 | 20% buffer |
| Mexico EEZ | 10.2 | 12.8 | 20% buffer |
| Other EEZs | 39.8 | 49.8 | 20% buffer |
| **Fleet total** | **186.1** | **232.6** | year-round |

### 23.3 ITQ Strategy & RFMO Position

- **ITQ argument**: released shrimp are *additional biomass*, not extracted wild stock -> negotiate "ocean-ranching quota" separate from wild-catch quota; pay 5-8% royalty in lieu of quota purchase; voluntary caps prevent market flooding.
- **RFMO position**: observer member APFIC + WCPFC; coordinate bycatch reporting with IOTC; propose new category "Enhanced Ocean Ranching."
- **Legal basis**: UNCLOS Part VII high-seas freedoms + bilateral EEZ licences. Released shrimp become wild at release; recapture is regulated fishing under licence.

---

## 24. Insurance, Risk & Crisis Management

### 24.1 Insurance Stack (RISK_MGMT, model-derived)

| Cover | Limit | Trigger |
|---|---|---|
| Marine hull | $750M / vessel | total loss, storm, collision |
| Business interruption | $300M / vessel | >30-day operational halt |
| Loss of catch | $500M / vessel | disease, escape, survival miss |
| Environmental liability | $1B | ecosystem impact event |
| Cyber liability | $200M | AI/navigation compromise |
| Political risk (OPIC/Sinosure) | licence value | EEZ revocation |
| Food-safety liability | $500M | recall, contamination |

### 24.2 Crisis Playbook (CRISIS_MANAGEMENT, model-derived)

| Crisis | P | Impact | Response | Financial exposure |
|---|---|---|---|---|
| Vessel loss | low | severe | evacuate -> insurance -> replacement in 18 mo | $2.0B insured |
| Disease (EMS/AHPND/WSSV) | med | moderate | no pen density; eDNA monitor; quarantine broodstock | $0.5B insured |
| EEZ revocation | low | moderate | 18-nation diversification; UNCLOS arbitration; relocate | $0.3B self-insured |
| Food-safety recall | low | severe | 48-h global recall via DNA batch; root-cause transparency | $0.2B |
| Cyber attack on AI | med | moderate | air-gapped backup controls; manual override; SOC 2 | $0.1B |
| Climate event | high | low | storm mode; fleet relocates to alternate EEZ | $50M |
| Regulatory ban | low | severe | UNCLOS challenge; pivot to contained aquaculture | $1.0B self-insured |
| Price collapse | med | moderate | lowest-cost producer ($0 fuel+feed); byproducts; licensing | unhedged |

---

## 25. Regulatory & Certification Matrix (REGULATORY, model-derived)

| Jurisdiction | Agency | Key regulations | Status | Certification |
|---|---|---|---|---|
| International | IMO | SOLAS, MARPOL, ballast-water | compliant by design | Lloyd's Register + DNV-GL |
| International | FAO | Code of Conduct for Responsible Fisheries | exceeds standards | MSC pending |
| USA | FDA + NOAA + USCG | Seafood HACCP (21 CFR 123), Magnuson-Stevens, USCG 46 CFR | compliant by design | FDA registration + USCG COI |
| EU | EFSA + EMSA | Food Hygiene 852/2004, Animal Health 2016/429 | compliant by design | EU health certificate |
| China | GACC | GB 2733, quarantine import rules | compliant by design | GACC registration |
| EEZ nations (18) | Fisheries ministries | ranching licence, royalty compliance, EIA, stock reporting | negotiating | bilateral agreements |
| Environmental | IUCN + CITES + Ramsar | wetland protection near nursery grounds | compliant by design | EIA per zone |

---

## 26. IP & Patent Portfolio (PATENT_PORTFOLIO, model-derived)

- **50 patents filed, 12 granted**, ~**$2.0B** estimated portfolio value
- Geographies: US, EU, China, Japan, Singapore, Australia, Brazil, India
- Strategy: file early, file broad; trade secrets for AI models + genetic lines

| Category | Count | Key patents |
|---|---|---|
| Energy systems | 12 | solar-to-H2 round trip, OTEC integration, heave-oar generator |
| Hull + naval architecture | 8 | semi-sub pentamaran w/ storm ballast, superhydrophobic coating |
| Aquaculture + hatchery | 10 | floating broodstock maturation, continuous release chute, biofloc RAS |
| AI + autonomy | 8 | multi-vessel swarm coordination, predictive maintenance, autonomous harvest |
| Feed production | 6 | integrated algae PBR + BSF waste conversion, closed-loop feed |
| Genetics + DNA | 4 | neutral CRISPR barcode, DNA recapture tracking |
| Acoustic + pheromone | 2 | underwater conditioning, species-specific dispenser |
