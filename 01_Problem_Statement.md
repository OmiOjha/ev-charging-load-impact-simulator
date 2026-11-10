# Problem Statement: EV Charging Load Impact Simulator
**Project Title:** Impact Modeling, Thermal Degradation Analysis, and Sustainable Microgrid Mitigation for High-Penetration EV Charging on Urban Distribution Grids  
**Domain:** Sustainable Energy Engineering / Smart Grid Systems  
**Applicable Standards:** IEEE Std C57.91-2011, ANSI C84.1 Range A, SAE J3072, ISO 15118  

---

### 1. Problem Context & Engineering Challenge
The global transition toward electrified mobility is accelerating exponentially. However, contemporary urban and suburban medium-to-low voltage (MV/LV) distribution grids were architected decades ago under assumptions of passive, unidirectional power flow with predictable coincident diversity factors. Uncoordinated electric vehicle (EV) charging—characterized by simultaneous high-power Level 2 (7.2–19.2 kW) and DC Fast Charging (50–150 kW) connections upon residential arrival (17:00–21:00)—imposes severe, non-coincident peak demands directly on top of legacy residential peak hours.

On a representative 2.5 MVA / 12.47 kV distribution substation feeder, a 70% EV penetration rate escalates peak demand from 1.52 MW to **4.46 MW** (an **87.7% overload**). This unmanaged load induces two critical failure modes:
1. **Severe Feeder Voltage Sag:** Voltage at downstream radial buses drops to **0.951 p.u.**, threatening brownouts and violating **ANSI C84.1 Range A limits (0.95–1.05 p.u.)**.
2. **Exponential Transformer Thermal Degradation:** According to **IEEE Std C57.91-2011**, transformer winding hot-spot temperatures soar to **189.4°C** (far exceeding the 110°C continuous design threshold). The resulting Aging Acceleration Factor ($F_{AA}$) reaches **74.2× normal**, depleting years of transformer insulation asset life within weeks.
3. **The Static Tariff Failure Paradox:** Utility implementation of static Time-of-Use (TOU) tariffs inadvertently triggers synchronized charging timers at off-peak commencement (23:00), producing an "avalanche rebound peak" of **4.31 MW** and failing to protect infrastructure.

---

### 2. Research Objectives & System Boundaries
This project develops **VoltGrid™**, an end-to-end, physics-grounded engineering simulator to quantify these impacts and deploy closed-loop sustainable solutions:
- **Stochastic Fleet Characterization:** Clean and model 3,500+ empirical EV charging sessions capturing varied battery capacities (40–98 kWh), arrival distributions, dwell times, and charging flexibility indices ($\Phi = t_{dwell} / t_{min}$).
- **Coupled Power Flow & Thermal Aging Engine:** Simulate radial backward/forward voltage drop (LinDistFlow) across a 13-bus network and dynamic top-oil/hot-spot differential heat transfer according to IEEE Std C57.91.
- **Sustainable Microgrid & V2G Optimization:** Formulate algorithmic smart valley-filling charging coupled with an 800 kWp carport solar PV array, a 1.2 MWh BESS, and bidirectional Vehicle-to-Grid (V2G) peak-shaving dispatch.
- **Interactive Decision-Support Platform:** Deliver a real-time web simulator allowing grid planners to stress-test penetration rates, size DER assets, and evaluate techno-economic and carbon abatement outcomes.

---

### 3. Quantitative Target Benchmarks

| Metric | Legacy Uncontrolled EV Load | Static TOU Rebound | VoltGrid™ Sustainable Solution | Engineering Target |
|:---|:---:|:---:|:---:|:---:|
| **Peak Feeder Demand** | 4.46 MW (+87.7% Overload) | 4.31 MW (+81.6% Overload) | **2.45 MW (+3.2% Controlled)** | $< 2.50\text{ MW}$ (Transformer Rated) |
| **Max Hot-Spot Temp** | 189.4 °C | 176.2 °C | **97.0 °C** | $< 110.0\text{ °C}$ (IEEE C57.91) |
| **Asset Aging Multiplier ($F_{EQ}$)** | 74.19× | 24.11× | **0.095× (Preserved)** | $\le 1.0\times$ (Design Baseline) |
| **Min Feeder Bus Voltage** | 0.951 p.u. | 0.953 p.u. | **0.973 p.u.** | $\ge 0.950\text{ p.u.}$ (ANSI C84.1) |
| **Daily Carbon Footprint** | 14,868 kg CO₂ | 11,764 kg CO₂ | **11,206 kg CO₂ (-24.6%)** | Maximized Renewable Self-Consumption |
