"""
Full Simulation Orchestrator
Executes all 4 charging regimes through the IEEE C57.91 thermal model
and radial feeder power flow solver, computing comparative metrics and exporting data.
"""

import json
import numpy as np
import pandas as pd
from smart_charge_optimizer import SmartChargeOptimizer
from transformer_thermal_model import TransformerThermalModel
from grid_feeder_model import RadialFeederModel

def run_full_simulation(penetration_rate=0.70):
    print(f"--- Running EV Charging Load Impact Simulation (Penetration: {penetration_rate*100:.0f}%) ---")
    optimizer = SmartChargeOptimizer()
    scenarios_data = optimizer.simulate_scenarios(penetration_rate=penetration_rate)

    transformer = TransformerThermalModel(rated_mva=2.5, power_factor=0.95)
    feeder = RadialFeederModel(num_buses=13, nominal_kv=12.47)

    ambient_temp = scenarios_data["ambient_temp_c"]
    rated_mw = scenarios_data["rated_transformer_mw"]

    scenarios = [
        ("Baseline (No EVs)", scenarios_data["baseline_load_mw"]),
        ("Uncontrolled Charging", scenarios_data["uncontrolled"]["net_load_mw"]),
        ("Static TOU Tariff", scenarios_data["tou_tariff"]["net_load_mw"]),
        ("Smart Valley Filling", scenarios_data["smart_valley_filling"]["net_load_mw"]),
        ("Sustainable Microgrid (V2G + Solar)", scenarios_data["sustainable_microgrid_v2g"]["net_load_mw"])
    ]

    summary_metrics = {}
    timeseries_dict = {
        "hour": scenarios_data["hours"],
        "baseline_load_mw": scenarios_data["baseline_load_mw"],
        "ambient_temp_c": ambient_temp,
        "solar_pv_mw": scenarios_data["solar_generation_mw"]
    }

    # Marginal carbon intensity factor:
    # Daytime solar = 0.05 kg/kWh, Off-peak wind = 0.15 kg/kWh, Evening peaker gas = 0.52 kg/kWh
    carbon_intensity_kg_mwh = np.array([
        160, 150, 150, 150, 160, 180, 240, 320, 310, 220, 140, 100, 
        90, 90, 120, 210, 330, 480, 520, 510, 480, 380, 280, 210
    ])

    for name, load_mw in scenarios:
        thermal_res = transformer.simulate_24h(load_mw, ambient_temp)
        feeder_res = feeder.simulate_24h_voltages(load_mw)

        peak_mw = float(np.max(load_mw))
        avg_mw = float(np.mean(load_mw))
        par = round(peak_mw / avg_mw, 3)
        overload_pct = max(0.0, round(((peak_mw - rated_mw) / rated_mw) * 100.0, 2))

        # Daily Carbon Emissions (kg CO2)
        total_co2_kg = round(float(np.sum(load_mw * carbon_intensity_kg_mwh)), 1)

        key = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("+", "plus")
        summary_metrics[key] = {
            "name": name,
            "peak_load_mw": round(peak_mw, 3),
            "average_load_mw": round(avg_mw, 3),
            "peak_to_average_ratio": par,
            "overload_pct_above_rating": overload_pct,
            "is_transformer_overloaded": bool(peak_mw > rated_mw),
            "max_hotspot_temp_c": thermal_res["max_hotspot_temp_c"],
            "hotspot_temp_exceeded_110c": bool(thermal_res["max_hotspot_temp_c"] > 110.0),
            "aging_acceleration_feq": thermal_res["feq"],
            "transformer_aging_multiplier": thermal_res["aging_multiplier"],
            "daily_loss_of_life_pct": thermal_res["daily_loss_of_life_pct"],
            "min_voltage_pu": feeder_res["min_voltage_24h"],
            "voltage_sag_violation_hours": feeder_res["voltage_violation_hours"],
            "daily_feeder_losses_mwh": feeder_res["daily_total_loss_mwh"],
            "daily_carbon_emissions_kg": total_co2_kg
        }

        timeseries_dict[f"{key}_load_mw"] = np.round(load_mw, 3)
        timeseries_dict[f"{key}_hotspot_c"] = thermal_res["hotspot_temp_c"]
        timeseries_dict[f"{key}_min_v_pu"] = feeder_res["hourly_min_voltage_pu"]

    # Save summary JSON
    with open("simulation/simulation_summary.json", "w") as f:
        json.dump(summary_metrics, f, indent=4)

    # Save timeseries CSV
    df_timeseries = pd.DataFrame(timeseries_dict)
    df_timeseries.to_csv("simulation/scenario_hourly_timeseries.csv", index=False)

    print("Simulation complete! Results exported to:")
    print(" - simulation/simulation_summary.json")
    print(" - simulation/scenario_hourly_timeseries.csv")

    for k, v in summary_metrics.items():
        print(f"\n[{v['name']}]")
        print(f"  Peak Load: {v['peak_load_mw']} MW (Overload: {v['overload_pct_above_rating']}%)")
        print(f"  Max Hot-spot Temp: {v['max_hotspot_temp_c']} °C | Aging Factor: {v['aging_acceleration_feq']}x normal")
        print(f"  Min Feeder Voltage: {v['min_voltage_pu']} p.u. (Sag violations: {v['voltage_sag_violation_hours']} hrs)")
        print(f"  Daily Carbon: {v['daily_carbon_emissions_kg']} kg CO2")

    return summary_metrics

if __name__ == "__main__":
    run_full_simulation()
