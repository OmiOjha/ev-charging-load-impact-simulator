# EV Charging Load Impact Simulator - Data Dictionary & Dataset Specification

## 1. Overview
This dataset suite models stochastic electric vehicle (EV) charging patterns, feeder-level baseline electricity demand, and solar photovoltaic (PV) generation profiles for an urban-suburban distribution substation (12.47 kV / 2.5 MVA transformer rating).

---

## 2. Dataset Files Summary

| File Name | Format | Records | Primary Purpose |
|:---|:---|:---|:---|
| `raw_ev_charging_data.csv` | CSV | 3,500 | Unfiltered telemetry data containing real-world sensor noise, NaNs, power spikes, and invalid timestamps. |
| `cleaned_ev_charging_data.csv` | CSV | 3,447 | Validated, imputed, and feature-engineered dataset ready for grid load flow and thermal simulation. |
| `distribution_grid_hourly_load.csv` | CSV | 24 | Baseline hourly non-EV electrical load (MW) and ambient temperatures for a 2.5 MVA substation transformer. |
| `solar_generation_profile.csv` | CSV | 24 | Hourly normalized PV capacity factor and generation output for an 800 kW solar carport / rooftop array. |

---

## 3. Schema & Feature Definitions

### A. EV Charging Sessions Data (`cleaned_ev_charging_data.csv`)

| Field Name | Data Type | Physical Unit | Description & Realistic Engineering Bounds |
|:---|:---|:---|:---|
| `session_id` | String | Identifier | Unique transaction key (e.g. `SES-2026-00042`). |
| `vehicle_model` | String | Categorical | Vehicle nameplate (Tesla Model 3/Y, Ford Lightning, Ioniq 5, Bolt, Leaf, Delivery Van). |
| `battery_capacity_kwh` | Float | kWh | Usable battery pack energy capacity [40.0 - 98.0 kWh]. |
| `user_type` | String | Categorical | Behavioral cluster: `Residential_Commuter`, `Workplace_Commuter`, `Commercial_Fleet`, `Public_Fastcharge`. |
| `charger_type` | String | Categorical | EVSE level: `Level_1_1.4kW`, `Level_2_7.2kW`, `Level_2_11kW`, `Level_2_Commercial_22kW`, `DC_Fast_50kW`, `DC_Fast_150kW`. |
| `charger_power_rating_kw`| Float | kW | Nameplate maximum continuous delivery power rating [1.4 - 150.0 kW]. |
| `arrival_timestamp` | Datetime | YYYY-MM-DD HH:MM:SS | Connection timestamp logged at plug insertion. |
| `departure_timestamp` | Datetime | YYYY-MM-DD HH:MM:SS | Disconnection timestamp logged at unplug event. |
| `initial_soc_percent` | Float | % | Battery state of charge upon arrival [5.0% - 75.0%]. |
| `target_soc_percent` | Float | % | Desired departure state of charge [80.0% - 100.0%]. |
| `energy_requested_kwh` | Float | kWh | Total energy transferred including 90% onboard/inverter conversion efficiency: $E = \frac{(SoC_{target} - SoC_{init})}{100 \times \eta} \times C_{batt}$. |
| `grid_feeder_node` | String | Categorical | Assigned distribution feeder bus location (`Bus_1` through `Bus_13`). |
| `v2g_hardware_enabled` | Boolean | True/False | Whether vehicle inverter and EVSE support bidirectional Vehicle-to-Grid power injection. |
| `meter_status` | String | Categorical | Sensor health indicator (`NORMAL`, `TELEMETRY_SPIKE`). |
| `dwell_hours` | Float | Hours | Total physical duration EV is plugged into the charger: $t_{dwell} = t_{dep} - t_{arr}$. |
| `min_charging_duration_hours`| Float | Hours | Minimum time required to deliver requested energy at maximum charger power: $t_{min} = \frac{E_{req}}{P_{charger}}$. |
| `charging_flexibility_index`| Float | Ratio | Metric indicating deferrable charging flexibility: $\Phi = \frac{t_{dwell}}{t_{min}}$. Values > 1.0 indicate viable load-shifting window. |
| `arrival_hour_float` | Float | Hours (0-24) | Decimal hour of arrival for statistical distribution and time-series clustering. |

---

## 4. Data Quality & Preprocessing Methodology

The pipeline script (`data_pipeline.py`) systematically remediates sensor corruption:
1. **Timestamp Inversion Filtering**: Removed instances where $t_{departure} \le t_{arrival}$ caused by asynchronous clock resets.
2. **Missing Value Imputation**: Missing $SoC_{init}$ and $SoC_{target}$ filled using cluster medians grouped by `user_type` to preserve behavioral variances.
3. **Outlier Clamping**: Filtered erroneous telemetry spikes ($P > 350\text{ kW}$) resulting from bit flips in metering equipment.
4. **Physical Thermodynamic Consistency**: Enforced $SoC_{target} \ge SoC_{init} + 10\%$ and recomputed energy demands to ensure energy balance conservation.
