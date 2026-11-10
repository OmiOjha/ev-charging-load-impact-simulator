# EV CHARGING LOAD IMPACT ON A DISTRIBUTION TRANSFORMER AND SUSTAINABLE MICROGRID MITIGATION
### Smart Charging, Solar PV, Battery Storage and Vehicle-to-Grid Analysis (VoltGrid Simulator)
**Sustainable Energy Engineering (SEE) Project**

---

### A PROJECT REPORT
**Submitted by**
- **SHREYAS KUMAR** [Reg No: RA2311003050085]
- **OMI OJHA** [Reg No: RA2311003050095]  
*IV B.Tech, Computer Science and Engineering*

**Under the guidance of**  
**Dr. R. Logudurai**  
*(Associate Professor, Department of SoC)*

*in partial fulfillment of the requirements for the course of*  
**SUSTAINABLE ENERGY ENGINEERING**  
*in*  
**BACHELOR OF TECHNOLOGY – COMPUTER SCIENCE AND ENGINEERING**

**DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING**  
**FACULTY OF ENGINEERING AND TECHNOLOGY**  
**SRM INSTITUTE OF SCIENCE AND TECHNOLOGY**  
**TIRUCHIRAPPALLI – 621105**  
**NOVEMBER 2026**

---

## BONAFIDE CERTIFICATE

Certified that this project report titled **"EV CHARGING LOAD IMPACT ON A DISTRIBUTION TRANSFORMER AND SUSTAINABLE MICROGRID MITIGATION"** is the bonafide work of **SHREYAS KUMAR (Register No. RA2311003050085)** and **OMI OJHA (Register No. RA2311003050095)**, students of IV B.Tech Computer Science and Engineering, who carried out the project work for the course **Sustainable Energy Engineering** under my supervision during the academic year 2026-2027.

Certified further that, to the best of my knowledge, the work reported herein does not form part of any other project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.

| SIGNATURE | SIGNATURE |
|:---|:---|
| **Dr. R. Logudurai**<br>Associate Professor / Guide<br>Department of SoC | **Dr. S. Kanaga Suba Raja**<br>Head of the Department<br>Department of CSE |

*Submitted for the project viva-voce examination held on ____________________*

**INTERNAL EXAMINER** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **EXTERNAL EXAMINER**

---

## DECLARATION

We, **Shreyas Kumar (Register No. RA2311003050085)** and **Omi Ojha (Register No. RA2311003050095)**, students of IV B.Tech Computer Science and Engineering, Faculty of Engineering and Technology, SRM Institute of Science and Technology, Tiruchirappalli, hereby declare that the project report entitled **"EV Charging Load Impact on a Distribution Transformer and Sustainable Microgrid Mitigation"** submitted for the course Sustainable Energy Engineering is a record of original work carried out by us under the guidance of **Dr. R. Logudurai**, Department of SoC.

We further declare that this work has not been submitted, in part or in full, to any other university or institution for the award of any degree, diploma or similar title.

**Place:** Tiruchirappalli  
**Date:** November 2026  

**Shreyas Kumar** (RA2311003050085)  
**Omi Ojha** (RA2311003050095)  

---

## ACKNOWLEDGEMENT

We express our sincere gratitude to the management of **SRM Institute of Science and Technology, Tiruchirappalli**, for providing the facilities and learning environment that made this project possible.

We are thankful to the Dean of the Faculty of Engineering and Technology and to **Dr. S. Kanaga Suba Raja**, Head of the Department of Computer Science and Engineering, for their encouragement and support throughout our study.

We owe a deep debt of gratitude to our project guide, **Dr. R. Logudurai**, Associate Professor, Department of SoC, for the valuable guidance, constructive suggestions and continuous motivation that helped us complete this work successfully.

We also thank all the faculty members of the department, our friends and classmates for their help and feedback, and finally our parents for their constant support and encouragement.

**Shreyas Kumar**  
**Omi Ojha**  

---

## ABSTRACT

The rapid growth of electric vehicles (EVs) adds large, clustered loads to distribution networks that were sized before EVs existed. When charging is uncontrolled, the EV peak coincides with the evening residential peak and can overload neighbourhood transformers, accelerate insulation ageing, depress feeder voltage and raise carbon emissions. This project presents **VoltGrid**, a Python and web-based simulator that quantifies these impacts for a 2.5 MVA, 12.47 kV, 13-bus radial feeder with 70 % EV penetration.

A synthetic dataset of 3,500 EV charging sessions was generated, cleaned to 3,447 validated records and combined with a base load profile and an 800 kWp solar profile. Four strategies were simulated: uncontrolled charging, a static time-of-use tariff, smart valley-filling and a microgrid with solar PV, a 1,200 kWh battery and vehicle-to-grid support. Transformer winding hot-spot temperature and ageing follow the IEEE C57.91 model, feeder voltage and losses follow a LinDistFlow model, and carbon emissions use an hourly marginal intensity profile.

Uncontrolled charging raised the substation peak to 4.46 MW (87.7 % above the 2.375 MW rating), the hot-spot to 189 °C and the ageing rate to 74 times normal. The TOU tariff only shifted the peak to 23:00 (4.31 MW). Smart valley-filling cut the peak to 2.45 MW and the hot-spot to 102 °C, and the microgrid further reduced daily $CO_2$ by 24.6 % and feeder losses by 30 % relative to uncontrolled charging. The results rely on synthetic data and a single typical day, and the report discusses these limitations. The simulator is supplied with an interactive dashboard (about 2,600 lines of code).

**Keywords:** Electric Vehicles, Smart Charging, Vehicle-to-Grid, Distribution Transformer Ageing, IEEE C57.91, LinDistFlow, Solar PV, Battery Storage, Sustainable Energy.

---

## TABLE OF CONTENTS

- **1. INTRODUCTION** .......................................................... 1
  - 1.1 Background
  - 1.2 Motivation
  - 1.3 Scope of the Project
  - 1.4 Organisation of the Report
- **2. BACKGROUND AND RELATED CONCEPTS** .......................................................... 2
  - 2.1 EV Charging and Distribution Assets
  - 2.2 Transformer Thermal Ageing (IEEE C57.91)
  - 2.3 Voltage Regulation on Radial Feeders
  - 2.4 Smart Charging, Solar PV, Storage and V2G
- **3. PROBLEM STATEMENT AND OBJECTIVES** .......................................................... 2
  - 3.1 Problem Statement
  - 3.2 Objectives
- **4. SYSTEM DESCRIPTION AND DATA** .......................................................... 3
  - 4.1 Test Feeder and Resources
  - 4.2 Datasets
  - 4.3 Data Preprocessing
- **5. METHODOLOGY** .......................................................... 4
  - 5.1 Overall Workflow
  - 5.2 Charging Scenarios
  - 5.3 Transformer Thermal and Ageing Model
  - 5.4 Feeder Voltage and Loss Model
  - 5.5 Carbon Accounting
- **6. IMPLEMENTATION** .......................................................... 5
  - 6.1 Project Structure
  - 6.2 VoltGrid Web Dashboard
- **7. RESULTS AND DISCUSSION** .......................................................... 6
  - 7.1 Substation Load
  - 7.2 Transformer Temperature and Ageing
  - 7.3 Feeder Voltage and Losses
  - 7.4 Solar, Storage and V2G Dispatch
  - 7.5 Carbon Emissions
  - 7.6 Achievement of Objectives
- **8. LIMITATIONS** .......................................................... 9
- **9. FUTURE ENHANCEMENTS** .......................................................... 9
- **10. CONCLUSION** .......................................................... 9
- **REFERENCES** .......................................................... 10

### LIST OF FIGURES
- Figure 1: Methodology workflow of the study (Page 4)
- Figure 2: 24-hour substation net load for the four charging scenarios (Page 6)
- Figure 3: Winding hot-spot temperature against the 110 °C limit (Page 7)
- Figure 4: Bus voltage profile along the feeder at peak loading (Page 7)
- Figure 5: Microgrid dispatch of solar PV, BESS and V2G (Page 8)
- Figure 6: Daily operational $CO_2$ emissions by scenario (Page 8)

### LIST OF TABLES
- Table 1: Main system parameters (Page 3)
- Table 2: Datasets used in the study (Page 3)
- Table 3: Charging scenarios compared (Page 4)
- Table 4: Source file sizes (Page 5)
- Table 5: Summary of simulation results (24-hour day) (Page 6)
- Table 6: Objectives versus outcome (Page 9)

### LIST OF ABBREVIATIONS
- **ANSI:** American National Standards Institute
- **BESS:** Battery Energy Storage System
- **EV:** Electric Vehicle
- **EVSE:** EV Supply Equipment
- **FAA / FEQ:** Ageing Acceleration / Equivalent Ageing Factor
- **IEEE:** Institute of Electrical and Electronics Engineers
- **LOL:** Loss of Life
- **PAR:** Peak-to-Average Ratio
- **PV:** Photovoltaic
- **SoC:** State of Charge
- **TOU:** Time of Use
- **V2G:** Vehicle-to-Grid

---

## 1. INTRODUCTION

### 1.1 Background
Transport electrification is one of the main routes to lower carbon emissions, and electric vehicles (EVs) are being adopted rapidly in cities and suburbs. Each vehicle, however, adds a large and highly clustered electrical load to the local distribution network. A single 7.2 kW home charger draws more power than the rest of a typical household, and when many owners plug in after returning from work, the evening residential peak and the EV peak coincide. Neighbourhood distribution transformers and feeders, which were sized for the pre-EV load, are then pushed beyond their ratings.

Overloading shortens the life of the transformer insulation, depresses voltage at the far end of the feeder, and increases line losses. Because the grid often meets the evening peak with gas-fired peaking plants, the added load is also supplied by the most carbon-intensive generation of the day. Whether EV adoption is genuinely sustainable therefore depends not only on how many EVs there are, but on when and how they charge.

This report describes the **VoltGrid EV Charging Load Impact Simulator**, a software study carried out for the Sustainable Energy Engineering (SEE) course at SRM Institute of Science and Technology, Tiruchirappalli. The study models a 2.5 MVA, 12.47 kV urban-suburban substation and compares four charging strategies, from uncontrolled charging to a solar-plus-storage microgrid with vehicle-to-grid (V2G) support, using a transformer thermal-ageing model and a radial feeder voltage model.

### 1.2 Motivation
- **Grid reliability:** EV clusters can overload distribution transformers long before generation capacity becomes a problem.
- **Asset life and cost:** hot-spot temperature drives insulation ageing exponentially, so a few hours of overload can cost months of life.
- **Sustainability:** EVs only reduce emissions if they charge when clean energy, such as midday solar, is available.
- **Learning value:** the project combines data engineering, power-system modelling, optimisation logic and an interactive web dashboard.

### 1.3 Scope of the Project
The work covers synthetic EV charging telemetry and its cleaning, four hourly charging scenarios, an IEEE C57.91 thermal model, a 13-bus LinDistFlow feeder model, an operational carbon estimate and an interactive web dashboard. Network reconfiguration, protection studies, harmonics, battery degradation, tariffs and economic analysis are outside the scope of this version and are listed as future work in Chapter 9.

### 1.4 Organisation of the Report
Chapter 2 reviews the relevant background. Chapter 3 states the problem and objectives. Chapter 4 describes the test system and data. Chapter 5 presents the methodology and Chapter 6 the implementation. Chapter 7 discusses the results. Chapters 8 to 10 cover limitations, future enhancements and the conclusion.

---

## 2. BACKGROUND AND RELATED CONCEPTS

### 2.1 EV Charging and Distribution Assets
Residential and workplace EVs are usually charged on Level 1 (about 1.4 kW) or Level 2 (7 to 22 kW) AC equipment, while public fast chargers deliver 50 to 150 kW DC. Because most vehicles are parked far longer than the time needed to charge, the charging load is highly flexible: the same energy can be delivered at a different time without inconveniencing the driver. Uncontrolled ("dumb") charging ignores this flexibility and starts as soon as the plug is inserted [3].

### 2.2 Transformer Thermal Ageing (IEEE C57.91)
The life of a liquid-immersed distribution transformer is set by the temperature of its winding insulation. IEEE Std C57.91 [1] relates load, ambient temperature, top-oil temperature and winding hot-spot temperature, and defines an ageing acceleration factor that equals 1.0 at a reference hot-spot temperature of 110 °C. Above this temperature insulation life is consumed at an exponentially increasing rate. Because the oil has a thermal time constant of a few hours, short overloads are partly absorbed, while sustained evening overloads are not.

### 2.3 Voltage Regulation on Radial Feeders
In a radial feeder, power flowing through the line resistance and reactance causes voltage to fall with distance from the substation. ANSI C84.1 [2] sets the acceptable service voltage at 0.95 to 1.05 per unit (Range A). The LinDistFlow approximation [4] computes bus voltages from the cumulative active and reactive power flowing in each branch and is widely used for planning studies.

### 2.4 Smart Charging, Solar PV, Storage and V2G
Coordinated ("valley-filling") charging moves flexible demand to hours of low base load [5]. Solar PV supplies energy at midday, and a battery energy storage system (BESS) can absorb surplus solar and release it during the evening peak. Vehicles with bidirectional chargers can additionally inject a small amount of power during the peak (V2G) and recharge overnight [6]. Together these resources form a "sustainable microgrid" that reduces both the peak demand on the transformer and the carbon intensity of the energy used.

---

## 3. PROBLEM STATEMENT AND OBJECTIVES

### 3.1 Problem Statement
Utilities and planners need a simple, transparent way to quantify how much EV charging a neighbourhood transformer and feeder can accept, what damage uncontrolled charging causes, and how much of that damage can be avoided by smart charging and local clean energy. Existing commercial tools are heavy, closed and expensive, while published studies rarely provide code and data that students can run and modify.

### 3.2 Objectives
1. To build a reproducible data pipeline that generates, cleans and validates EV charging session data.
2. To model four charging strategies for a 2.5 MVA feeder: uncontrolled, static time-of-use (TOU), smart valley-filling and solar + BESS + V2G.
3. To evaluate each strategy using transformer loading, winding hot-spot temperature, ageing, feeder voltage, line losses and $CO_2$ emissions.
4. To compare the strategies against engineering limits (nameplate rating, 110 °C hot-spot, 0.95 p.u. voltage).
5. To deliver an interactive web dashboard (VoltGrid) so that penetration, solar size and storage size can be varied.

---

## 4. SYSTEM DESCRIPTION AND DATA

### 4.1 Test Feeder and Resources
The test system is a radial 12.47 kV feeder with 13 buses fed from a 2.5 MVA substation transformer. At 0.95 power factor the transformer supplies 2.375 MW continuously, and a short-time emergency limit of 2.65 MW is assumed. Table 1 lists the main parameters.

#### Table 1: Main system parameters
| Item | Value |
|:---|:---|
| **Substation transformer** | 2.5 MVA, 12.47 kV; rated 2.375 MW at 0.95 pf; emergency limit 2.65 MW |
| **Feeder** | 13 buses, 12 branches, 6.5 km in total; r = 0.35 Ω/km, x = 0.38 Ω/km |
| **Base load** | Dual-peak profile: 0.71 MW minimum (14:00), 1.52 MW peak (20:00) |
| **Solar PV** | 800 kWp carport / rooftop array (peak output 800 kW at 12:00 to 13:00) |
| **Battery storage (BESS)** | 400 kW / 1,200 kWh |
| **EV penetration (default)**| 70 % of the cleaned session set (2,412 sessions); adjustable from 10 % to 100 % |

### 4.2 Datasets
Four CSV files describe the system (Table 2). The EV session data are synthetic and were generated with a fixed random seed from assumed vehicle mixes (Tesla Model 3 and Y, Ford F-150 Lightning, Hyundai Ioniq 5, Chevrolet Bolt, Nissan Leaf, delivery van) and four user clusters: residential commuters (65 %), workplace commuters (20 %), commercial fleet (10 %) and public fast charging (5 %). About 3.8 % of the raw records were deliberately corrupted to mimic real telemetry faults.

#### Table 2: Datasets used in the study
| File | Records | Purpose |
|:---|:---:|:---|
| `raw_ev_charging_data.csv` | 3,500 | Unfiltered sessions with injected noise, missing values and spikes |
| `cleaned_ev_charging_data.csv` | 3,447 | Validated and feature-engineered sessions used for simulation |
| `distribution_grid_hourly_load.csv` | 24 | Hourly base load (MW) and ambient temperature |
| `solar_generation_profile.csv` | 24 | Hourly PV capacity factor and output of the 800 kWp array |

### 4.3 Data Preprocessing
The pipeline (`data_pipeline.py`) removed sessions whose departure was not after arrival (dwell shorter than 9 minutes), imputed missing initial and target state of charge (SoC) with medians for each user type, rejected power readings above 350 kW, replaced zero energy values using battery physics, and enforced a target SoC above the initial SoC. Of the 3,500 raw records, 3,447 (98.5 %) were retained.

Energy per session was computed as:
$$E = \frac{SoC_{target} - SoC_{initial}}{100 \times \eta} \times C_{battery}$$
with a charging efficiency $\eta = 0.90$, and a charging flexibility index $\Phi = \frac{t_{dwell}}{t_{min}}$ was added. The cleaned data have a mean energy request of 41.1 kWh, a mean dwell of 10.1 h, and 89 % of sessions have $\Phi$ above 1, meaning that most charging can be shifted in time.

---

## 5. METHODOLOGY

### 5.1 Overall Workflow
Figure 1 shows the workflow. Cleaned sessions are converted into hourly EV load under each strategy and added to the base load. The resulting net load of the substation is passed to the transformer and feeder models, and the metrics are exported for plotting and for the dashboard.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  1. INPUT DATA  │       │ 2. DATA PIPELINE│       │  3. SCENARIOS   │
│ EV sessions     │──────>│ Validate/impute │──────>│ A Uncontrolled  │
│ Base feeder load│       │ Clamp outliers  │       │ B Static TOU    │
│ Solar PV profile│       │ 3,447 clean ses.│       │ C Valley filling│
└─────────────────┘       └─────────────────┘       │ D Solar+BESS+V2G│
                                                            │
                                                            ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   6. OUTPUTS    │       │   5. METRICS    │       │ 4. GRID MODELS  │
│ JSON & CSV files│<──────│ Peak, PAR, OL   │<──────│ IEEE C57.91     │
│ 8 figures, App  │       │ Hot-spot, LOL   │       │ Thermal/Ageing  │
│ Scenario ranking│       │ Voltage, losses │       │ LinDistFlow 13b │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```
*Figure 1: Methodology workflow of the EV Charging Impact Study*

### 5.2 Charging Scenarios
#### Table 3: Charging scenarios compared
| Scenario | Description |
|:---|:---|
| **Baseline** | Base feeder load with no EVs; reference case. |
| **A. Uncontrolled** | Each EV charges at full charger power from the hour of arrival until its energy request is met. |
| **B. Static TOU tariff** | Residential commuters delay charging to 23:00 (start of off-peak price); all other users charge on arrival. |
| **C. Smart valley-filling** | 22 % of the EV energy is non-deferrable; the remaining 78 % is allocated to hours in inverse proportion to the base load, with 17:00 to 22:00 suppressed. |
| **D. Microgrid (solar + BESS + V2G)** | Scenario C plus 800 kWp PV; BESS charges from solar (10:00 to 14:00, up to 350 kW) and discharges 320 kW at 18:00 to 21:00; V2G injects up to 0.22 MW × eligible fraction at 18:00 to 20:00 and recharges overnight. |

### 5.3 Transformer Thermal and Ageing Model
The hourly load is expressed as a per-unit ratio $K = P / P_{rated}$. The ultimate top-oil rise and the hot-spot rise follow IEEE C57.91 [1], and the top-oil temperature is advanced in one-hour Euler steps:

$$\Delta\theta_{TO, U} = \Delta\theta_{TO, R} \left[ \frac{K^2 R + 1}{R + 1} \right]^n$$

$$\theta_{TO}(t) = \theta_{TO}(t-1) + \frac{\Delta t}{\tau_{TO}} [\theta_{TO, U} - \theta_{TO}(t-1)]$$

$$\theta_H = \theta_{TO} + \Delta\theta_{H, R} K^{2m}$$

$$F_{AA} = \exp\left[ \frac{15000}{383} - \frac{15000}{\theta_H + 273} \right]; \quad F_{EQ} = \text{mean}(F_{AA}); \quad LOL\% = F_{EQ} \times \left( \frac{24}{180000} \right) \times 100$$

The parameters are $\Delta\theta_{TO, R} = 55\text{ }^\circ\text{C}$, $\Delta\theta_{H, R} = 25\text{ }^\circ\text{C}$, $\tau_{TO} = 3\text{ h}$, $R = 5$ and $n = m = 0.8$. Normal insulation life is taken as 180,000 hours, so a day at $F_{EQ} = 1$ consumes about 0.0133 % of life. Ambient temperature varies from 16 °C at night to 35 °C in the afternoon.

### 5.4 Feeder Voltage and Loss Model
Total substation power is shared among buses 2 to 13 using fixed load shares (for example 12 % at the commercial centre, bus 6). A backward sweep accumulates branch flows $P_i$ and $Q_i$ (0.95 pf lagging), and a forward sweep applies the LinDistFlow voltage drop:

$$V_{i+1} = V_i - \frac{r_i P_i + x_i Q_i}{V_i}; \quad P_{loss, i} = \left[ \frac{P_i^2 + Q_i^2}{V_i^2} \right] r_i$$

### 5.5 Carbon Accounting
Daily operational emissions are computed as the sum over 24 hours of net substation load multiplied by an hourly marginal carbon intensity, which ranges from 90 kg/MWh at midday (solar) to 520 kg/MWh at 18:00 (gas peakers). The intensity profile is an assumption made in the simulation code and not a measured grid value.

---

## 6. IMPLEMENTATION

### 6.1 Project Structure
The project is written in Python 3 (NumPy, pandas, Matplotlib) for the simulation and in HTML, CSS and JavaScript (Chart.js) for the dashboard.

```
see-project/
|-- datasets/     data_pipeline.py, raw and cleaned EV data, grid load, solar profile
|-- simulation/   smart_charge_optimizer.py, transformer_thermal_model.py,
|                 grid_feeder_model.py, run_simulation.py, generate_plots.py,
|                 simulation_summary.json, scenario_hourly_timeseries.csv
|-- figures/      8 PNG figures (load, hot-spot, voltage, demand, dispatch, ...)
`-- app/          index.html, styles.css, app.js (VoltGrid dashboard)
```

#### Table 4: Source file sizes
| File | Role | Lines |
|:---|:---|:---:|
| `data_pipeline.py` | Data generation, cleaning, grid and solar profiles | 236 |
| `smart_charge_optimizer.py` | Scenario A to D dispatch logic | 174 |
| `transformer_thermal_model.py` | IEEE C57.91 thermal and ageing model | 94 |
| `grid_feeder_model.py` | 13-bus LinDistFlow voltage and loss model | 122 |
| `run_simulation.py`, `generate_plots.py` | Orchestration, metrics export and figures | 105 + 337 |
| `index.html`, `styles.css`, `app.js` | VoltGrid web dashboard | 297 + 675 + 560 |
| **Total** | | **2,600** |

### 6.2 VoltGrid Web Dashboard
The dashboard re-implements the scenario, thermal, voltage and carbon calculations in JavaScript so that results update instantly in the browser. The user selects a charging strategy and moves sliders for EV penetration (10 to 100 %), solar capacity (0 to 1,500 kWp) and storage (0 to 2,400 kWh). Four KPI cards show peak load, hot-spot temperature with the ageing multiple, minimum feeder voltage and daily $CO_2$. Charts show the 24-hour net load against the transformer limits and the bus voltage profile, a table compares reliability metrics, a "Run Monte Carlo" button steps the penetration rate through random values between 40 % and 95 %, and results can be exported as CSV. A filterable table lists the simulated EV fleet and its flexibility.

---

## 7. RESULTS AND DISCUSSION

All results are for the default case of 70 % EV penetration, 800 kWp PV and a 1,200 kWh BESS. Table 5 summarises the metrics of all five cases.

#### Table 5: Summary of simulation results (24-hour day)
| Metric | Baseline | A. Uncontrolled | B. Static TOU | C. Valley filling | D. Microgrid |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Peak load (MW)** | 1.52 | 4.46 | 4.31 | 2.45 | 2.45 |
| **Peak-to-average ratio** | 1.46 | 2.13 | 2.06 | 1.17 | 1.26 |
| **Above 2.375 MW rating (%)** | 0.0 | 87.7 | 81.6 | 3.2 | 3.2 |
| **Max hot-spot temp (°C)** | 63.6 | 189.4 | 176.2 | 102.2 | 97.0 |
| **Ageing factor $F_{EQ}$** | 0.002 | 74.190 | 24.110 | 0.193 | 0.095 |
| **Daily loss of life (%)** | 0.00002 | 0.98921 | 0.32147 | 0.00258 | 0.00127 |
| **Min feeder voltage (p.u.)** | 0.9836 | 0.9511 | 0.9527 | 0.9734 | 0.9734 |
| **Feeder losses (MWh/day)** | 0.175 | 0.847 | 0.790 | 0.679 | 0.596 |
| **$CO_2$ (kg/day)** | 6,761 | 14,868 | 11,764 | 12,176 | 11,206 |

### 7.1 Substation Load
Without EVs the base load peaks at 1.52 MW, well below the rating. Uncontrolled charging adds an EV peak that coincides with the evening residential peak, giving 4.46 MW at 20:00, which is 87.7 % above nameplate and above the 2.65 MW emergency limit for five hours. The static TOU tariff does not remove the problem: because residential users all start at 23:00, a rebound peak of 4.31 MW appears at 23:00 and the transformer exceeds its rating for eight hours. Smart valley-filling cuts the peak to 2.45 MW (a 45 % reduction from Scenario A) and the peak-to-average ratio from 2.13 to 1.17.

*(Refer to Figure 2 in the compiled report PDF: 24-hour substation net load for the four charging scenarios)*

### 7.2 Transformer Temperature and Ageing
Uncontrolled charging drives the winding hot-spot to 189 °C, far above the 110 °C reference, and the ageing factor reaches 74.2, so the transformer loses about 0.99 % of its life in one day, roughly 74 times the normal rate (0.0133 %). The TOU case is still severe (176 °C, $F_{EQ} = 24.1$). Smart valley-filling holds the hot-spot at 102 °C and the microgrid at 97 °C, both below 110 °C, with $F_{EQ}$ of 0.19 and 0.095, i.e. the transformer ages well below the normal rate ($F_{EQ} < 1$), although still above the no-EV baseline value of 0.002.

*(Refer to Figure 3 in the compiled report PDF: Winding hot-spot temperature against the 110 °C limit)*

### 7.3 Feeder Voltage and Losses
At the evening peak the voltage at the feeder tail (bus 13) falls to 0.9511 p.u. under uncontrolled charging and 0.9527 p.u. under TOU, just above the 0.95 p.u. limit of ANSI C84.1, so no hour violates the limit in the default case. Smart charging improves the minimum voltage to 0.9734 p.u. Feeder losses fall from 0.847 MWh/day (A) to 0.679 (C) and 0.596 MWh/day (D), a 30 % cut for the microgrid. The margin under uncontrolled charging is thin: a higher penetration rate would be expected to cross the limit, which the user can examine by raising the penetration slider in the dashboard.

*(Refer to Figure 4 in the compiled report PDF: Bus voltage profile along the feeder at peak loading)*

### 7.4 Solar, Storage and V2G Dispatch
Figure 5 shows the microgrid dispatch. Solar output peaks at 800 kW at midday and charges the BESS between 10:00 and 14:00; the BESS then discharges 320 kW from 18:00 to 21:00, and V2G adds a small injection at 18:00 to 20:00. The evening load therefore falls markedly. The remaining maximum of 2.45 MW occurs at 22:00, just after the discharge window ends, which shows that the dispatch window, not the storage size alone, limits the peak.

*(Refer to Figure 5 in the compiled report PDF: Microgrid dispatch of solar PV, BESS and V2G)*

### 7.5 Carbon Emissions
Uncontrolled charging more than doubles the daily emissions compared with the no-EV baseline (14,868 against 6,761 kg/day) because the extra energy is supplied at the high-carbon evening hours. The microgrid reduces emissions to 11,206 kg/day, avoiding 3,662 kg of $CO_2$ per day (24.6 %). An important observation is that smart valley-filling (12,176 kg) emits slightly more than the static TOU case (11,764 kg): flattening the load protects the transformer but does not by itself minimise carbon, because the shifted energy lands in night hours whose assumed marginal intensity (150 to 240 kg/MWh) is higher than at midday. Carbon-aware scheduling is therefore a separate objective from peak shaving.

*(Refer to Figure 6 in the compiled report PDF: Daily operational $CO_2$ emissions by scenario)*

### 7.6 Achievement of Objectives
#### Table 6: Objectives versus outcome
| No. | Objective | Outcome |
|:---:|:---|:---|
| **1** | Reproducible data pipeline | **Achieved:** 3,500 raw to 3,447 clean sessions with documented rules |
| **2** | Four charging strategies modelled | **Achieved:** Scenarios A to D plus baseline |
| **3** | Thermal, voltage, loss and $CO_2$ metrics | **Achieved:** 14 metrics per scenario exported to JSON and CSV |
| **4** | Comparison against limits | **Partly:** C and D keep the hot-spot below 110 °C but peak at 2.45 MW, 3.2 % above nameplate |
| **5** | Interactive dashboard | **Achieved:** VoltGrid with three sliders, KPI cards, charts and CSV export |

---

## 8. LIMITATIONS

- **Synthetic data:** EV sessions, base load, solar and ambient temperature are generated, not measured, so the numbers illustrate relative behaviour and are not a forecast for a real feeder.
- **Single typical day:** only one 24-hour day at hourly resolution is simulated; seasons, weekends and sub-hourly peaks are not covered.
- **Simplified network:** a balanced, single-phase-equivalent radial feeder with fixed load shares and LinDistFlow approximation; no unbalance, taps or capacitor control.
- **Heuristic scheduling:** valley-filling uses fixed weights and a 22 % non-deferrable share, not a formal optimisation with driver constraints.
- **Assumed carbon intensity and fixed V2G, BESS rules:** no battery degradation, round-trip losses or economics are modelled.
- **Residual overload:** Scenarios C and D still reach 2.45 MW (3.2 % above nameplate) for one hour, within the 2.65 MW emergency limit.

---

## 9. FUTURE ENHANCEMENTS

- Replace synthetic data with real charger logs and smart-meter data from a utility or campus.
- Use linear or mixed-integer optimisation for charging with driver departure-time constraints and a carbon-aware objective.
- Add multi-day and seasonal simulation, three-phase unbalanced power flow and voltage-regulation devices.
- Include BESS degradation, V2G battery wear, tariffs and a payback analysis.
- Extend the dashboard with uploads of user data and a rolling forecast of load and solar.

---

## 10. CONCLUSION

The VoltGrid study shows, within the stated assumptions, that EV charging on an existing 2.5 MVA feeder is manageable only if it is coordinated. At 70 % penetration, uncontrolled charging raises the peak to 4.46 MW, heats the winding to 189 °C and ages the transformer 74 times faster than normal, and a simple TOU tariff merely moves the peak to 23:00. Smart valley-filling reduces the peak by 45 % and removes the thermal hazard, and adding solar, storage and V2G lowers the daily $CO_2$ by 24.6 % and feeder losses by 30 % compared with uncontrolled charging. The results also show that peak shaving and decarbonisation are different goals and need to be designed together. The code, data and dashboard form a reproducible base for future work on real data and optimised control.

---

## REFERENCES

[1] IEEE Std C57.91-2011, *IEEE Guide for Loading Mineral-Oil-Immersed Transformers and Step-Voltage Regulators*, IEEE, 2012.  
[2] ANSI C84.1-2020, *American National Standard for Electric Power Systems and Equipment: Voltage Ratings (60 Hz)*, NEMA, 2020.  
[3] K. Clement-Nyns, E. Haesen and J. Driesen, "The impact of charging plug-in hybrid electric vehicles on a residential distribution grid," *IEEE Trans. Power Syst.*, vol. 25, no. 1, pp. 371-380, 2010.  
[4] M. E. Baran and F. F. Wu, "Network reconfiguration in distribution systems for loss reduction and load balancing," *IEEE Trans. Power Del.*, vol. 4, no. 2, pp. 1401-1407, 1989.  
[5] E. Sortomme, M. M. Hindi, S. D. J. MacPherson and S. S. Venkata, "Coordinated charging of plug-in hybrid electric vehicles to minimize distribution system losses," *IEEE Trans. Smart Grid*, vol. 2, no. 1, pp. 198-205, 2011.  
[6] W. Kempton and J. Tomić, "Vehicle-to-grid power fundamentals: Calculating capacity and net revenue," *J. Power Sources*, vol. 144, no. 1, pp. 268-279, 2005.
