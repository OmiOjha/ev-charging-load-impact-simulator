"""
EV Charging Load Impact Simulator - Data Pipeline & Generation
Generates scientifically grounded raw telemetry data, performs rigorous data cleaning,
validates against physical constraints, and outputs both raw and cleaned datasets.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)

def generate_raw_dataset(num_sessions=3500, output_path="datasets/raw_ev_charging_data.csv"):
    vehicle_specs = [
        {"model": "Tesla Model 3", "battery_kwh": 60.0, "max_ac_kw": 11.0, "v2g_ready": True, "weight": 0.32},
        {"model": "Tesla Model Y", "battery_kwh": 75.0, "max_ac_kw": 11.0, "v2g_ready": True, "weight": 0.28},
        {"model": "Ford F-150 Lightning", "battery_kwh": 98.0, "max_ac_kw": 19.2, "v2g_ready": True, "weight": 0.12},
        {"model": "Hyundai Ioniq 5", "battery_kwh": 77.4, "max_ac_kw": 11.0, "v2g_ready": True, "weight": 0.10},
        {"model": "Chevy Bolt EV", "battery_kwh": 65.0, "max_ac_kw": 7.2, "v2g_ready": False, "weight": 0.08},
        {"model": "Nissan Leaf", "battery_kwh": 40.0, "max_ac_kw": 6.6, "v2g_ready": True, "weight": 0.05},
        {"model": "Commercial Delivery Van", "battery_kwh": 85.0, "max_ac_kw": 22.0, "v2g_ready": False, "weight": 0.05},
    ]

    models = [v["model"] for v in vehicle_specs]
    weights = [v["weight"] for v in vehicle_specs]
    spec_lookup = {v["model"]: v for v in vehicle_specs}

    user_profiles = [
        {"type": "Residential_Commuter", "prob": 0.65, "arr_mean": 18.5, "arr_std": 1.5, "dwell_mean": 12.0, "dwell_std": 2.0},
        {"type": "Workplace_Commuter", "prob": 0.20, "arr_mean": 8.5, "arr_std": 0.8, "dwell_mean": 8.5, "dwell_std": 1.0},
        {"type": "Commercial_Fleet", "prob": 0.10, "arr_mean": 20.0, "arr_std": 1.0, "dwell_mean": 7.0, "dwell_std": 1.5},
        {"type": "Public_Fastcharge", "prob": 0.05, "arr_mean": 14.0, "arr_std": 3.0, "dwell_mean": 0.75, "dwell_std": 0.25},
    ]

    base_date = datetime(2026, 4, 15)
    records = []

    for i in range(num_sessions):
        session_id = f"SES-2026-{i+1:05d}"
        v_model = np.random.choice(models, p=weights)
        spec = spec_lookup[v_model]

        # Profile selection
        p_weights = [p["prob"] for p in user_profiles]
        profile = np.random.choice(user_profiles, p=p_weights)
        user_type = profile["type"]

        # Arrival & dwell time calculation
        arr_hour = np.random.normal(profile["arr_mean"], profile["arr_std"]) % 24.0
        dwell_hours = max(0.2, np.random.normal(profile["dwell_mean"], profile["dwell_std"]))

        arr_minutes = int(arr_hour * 60)
        arrival_dt = base_date + timedelta(minutes=arr_minutes)
        departure_dt = arrival_dt + timedelta(minutes=int(dwell_hours * 60))

        # Charger selection
        if user_type == "Public_Fastcharge":
            charger_type = np.random.choice(["DC_Fast_50kW", "DC_Fast_150kW"], p=[0.7, 0.3])
            charger_kw = 50.0 if charger_type == "DC_Fast_50kW" else 150.0
        elif user_type == "Commercial_Fleet":
            charger_type = "Level_2_Commercial_22kW"
            charger_kw = min(spec["max_ac_kw"], 22.0)
        elif user_type == "Workplace_Commuter":
            charger_type = "Level_2_Workplace_11kW"
            charger_kw = min(spec["max_ac_kw"], 11.0)
        else: # Residential
            charger_type = np.random.choice(["Level_1_1.4kW", "Level_2_7.2kW", "Level_2_11kW"], p=[0.10, 0.70, 0.20])
            if charger_type == "Level_1_1.4kW":
                charger_kw = 1.4
            elif charger_type == "Level_2_7.2kW":
                charger_kw = min(spec["max_ac_kw"], 7.2)
            else:
                charger_kw = min(spec["max_ac_kw"], 11.0)

        # Battery initial SoC and target SoC
        init_soc = np.clip(np.random.normal(35.0, 15.0), 5.0, 75.0)
        target_soc = np.random.choice([80.0, 90.0, 100.0], p=[0.45, 0.40, 0.15])
        if target_soc <= init_soc:
            target_soc = min(100.0, init_soc + 20.0)

        battery_cap = spec["battery_kwh"]
        efficiency = 0.90
        net_energy_needed = (target_soc - init_soc) / 100.0 * battery_cap
        energy_requested = net_energy_needed / efficiency

        # Feeder node assignment (13-bus distribution system)
        feeder_node = f"Bus_{np.random.randint(1, 14)}"

        # Telemetry flags
        v2g_ready = spec["v2g_ready"] and (charger_type in ["Level_2_7.2kW", "Level_2_11kW", "Level_2_Commercial_22kW"])
        meter_health = "NORMAL"

        # Inject realistic noise / anomalies (~3.5% dirty records for raw dataset)
        rand_anomaly = np.random.rand()
        if rand_anomaly < 0.008:
            # Corrupted negative dwell time or arrival after departure
            departure_dt = arrival_dt - timedelta(minutes=int(np.random.randint(10, 120)))
        elif rand_anomaly < 0.016:
            # Missing SoC or negative SoC
            init_soc = np.nan
        elif rand_anomaly < 0.024:
            # Power spike sensor anomaly
            charger_kw = 999.0
            meter_health = "TELEMETRY_SPIKE"
        elif rand_anomaly < 0.032:
            # Zero energy recorded despite connected duration
            energy_requested = 0.0
        elif rand_anomaly < 0.038:
            # Target SoC missing
            target_soc = np.nan

        records.append({
            "session_id": session_id,
            "vehicle_model": v_model,
            "battery_capacity_kwh": battery_cap,
            "user_type": user_type,
            "charger_type": charger_type,
            "charger_power_rating_kw": round(charger_kw, 2),
            "arrival_timestamp": arrival_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "departure_timestamp": departure_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "initial_soc_percent": round(init_soc, 2) if not np.isnan(init_soc) else np.nan,
            "target_soc_percent": round(target_soc, 2) if not np.isnan(target_soc) else np.nan,
            "energy_requested_kwh": round(energy_requested, 3),
            "grid_feeder_node": feeder_node,
            "v2g_hardware_enabled": v2g_ready,
            "meter_status": meter_health
        })

    df_raw = pd.DataFrame(records)
    df_raw.to_csv(output_path, index=False)
    print(f"Generated raw dataset: {output_path} ({len(df_raw)} records, {df_raw.isna().sum().sum()} NaNs)")
    return df_raw

def clean_and_process_dataset(raw_path="datasets/raw_ev_charging_data.csv", cleaned_path="datasets/cleaned_ev_charging_data.csv"):
    df = pd.read_csv(raw_path)
    initial_count = len(df)

    # 1. Parsing timestamps
    df["arrival_dt"] = pd.to_datetime(df["arrival_timestamp"])
    df["departure_dt"] = pd.to_datetime(df["departure_timestamp"])

    # 2. Filter out reverse time order anomalies (arrival >= departure)
    df["dwell_hours"] = (df["departure_dt"] - df["arrival_dt"]).dt.total_seconds() / 3600.0
    valid_dwell = df["dwell_hours"] > 0.15 # At least 9 minutes
    df = df[valid_dwell].copy()

    # 3. Handle missing SoC values using group-wise median imputation based on user_type
    median_init_soc = df.groupby("user_type")["initial_soc_percent"].transform("median")
    df["initial_soc_percent"] = df["initial_soc_percent"].fillna(median_init_soc).fillna(35.0)

    median_target_soc = df.groupby("user_type")["target_soc_percent"].transform("median")
    df["target_soc_percent"] = df["target_soc_percent"].fillna(median_target_soc).fillna(85.0)

    # Physical check: Target SoC must be strictly greater than initial SoC
    df.loc[df["target_soc_percent"] <= df["initial_soc_percent"], "target_soc_percent"] = np.minimum(
        100.0, df.loc[df["target_soc_percent"] <= df["initial_soc_percent"], "initial_soc_percent"] + 20.0
    )

    # 4. Filter power spike anomalies (e.g. 999 kW)
    valid_power = (df["charger_power_rating_kw"] > 0.5) & (df["charger_power_rating_kw"] <= 350.0)
    df = df[valid_power].copy()

    # 5. Recompute/validate energy requested based on battery physics
    efficiency = 0.90
    ideal_energy = ((df["target_soc_percent"] - df["initial_soc_percent"]) / 100.0) * df["battery_capacity_kwh"] / efficiency
    # Replace zero or corrupted energy with physically modeled energy
    df.loc[df["energy_requested_kwh"] <= 0.05, "energy_requested_kwh"] = ideal_energy

    # 6. Feature Engineering
    # Min charging time in hours at nominal rating
    df["min_charging_duration_hours"] = df["energy_requested_kwh"] / df["charger_power_rating_kw"]
    # Flexibility ratio: Dwell Time / Min Required Charge Time
    # If ratio > 1.0, user has idle dwell time that can be shifted or modulated!
    df["charging_flexibility_index"] = np.round(df["dwell_hours"] / np.maximum(0.1, df["min_charging_duration_hours"]), 2)

    # Arrival hour decimal (e.g., 18.5 = 18:30)
    df["arrival_hour_float"] = df["arrival_dt"].dt.hour + df["arrival_dt"].dt.minute / 60.0

    # Drop intermediate columns and save
    df = df.drop(columns=["arrival_dt", "departure_dt"])
    df.to_csv(cleaned_path, index=False)

    print(f"Data cleaning complete: {cleaned_path}")
    print(f"Retained {len(df)} of {initial_count} records ({len(df)/initial_count*100:.1f}%)")
    return df

def generate_grid_baseline_and_solar():
    """
    Generates realistic 24-hour feeder baseline load curve (MW) for a 2.5 MVA substation
    and normalized solar irradiance PV generation profile.
    """
    hours = np.linspace(0, 23, 24)
    # Typical dual-peak residential/commercial load profile (Pecan Street / IEEE benchmark)
    # Base load ~0.8 MW, morning peak at 9 AM (~1.2 MW), evening peak at 8 PM (~1.65 MW)
    baseline_load_mw = (
        0.75
        + 0.45 * np.exp(-((hours - 8.5) ** 2) / 8.0)
        + 0.90 * np.exp(-((hours - 20.0) ** 2) / 10.0)
        + 0.15 * np.sin(hours / 24.0 * 2 * np.pi)
    )
    baseline_load_mw = np.round(np.clip(baseline_load_mw, 0.65, 1.75), 3)

    # Solar generation profile: Bell curve peaked around 12:30 PM (solar noon)
    solar_profile_pu = np.maximum(0.0, np.exp(-((hours - 12.5) ** 2) / 7.5) - 0.05)
    solar_profile_pu[hours < 6] = 0.0
    solar_profile_pu[hours > 19] = 0.0
    solar_profile_pu = np.round(solar_profile_pu / np.max(solar_profile_pu), 3)

    # Substation Transformer Specifications
    # 2.5 MVA transformer, 0.95 power factor nominal capacity = 2.375 MW
    df_grid = pd.DataFrame({
        "hour": hours.astype(int),
        "baseline_load_mw": baseline_load_mw,
        "transformer_rated_capacity_mw": 2.375,
        "transformer_emergency_limit_mw": 2.650,
        "feeder_nominal_voltage_kv": 12.47,
        "ambient_temp_celsius": [18, 17, 16, 16, 17, 19, 22, 25, 28, 31, 33, 34, 35, 35, 34, 32, 30, 27, 24, 22, 21, 20, 19, 18]
    })
    df_grid.to_csv("datasets/distribution_grid_hourly_load.csv", index=False)

    df_solar = pd.DataFrame({
        "hour": hours.astype(int),
        "solar_pv_capacity_factor": solar_profile_pu,
        "installed_pv_capacity_kw": 800.0,
        "solar_generation_kw": np.round(solar_profile_pu * 800.0, 1),
        "bess_rated_power_kw": 400.0,
        "bess_energy_capacity_kwh": 1200.0
    })
    df_solar.to_csv("datasets/solar_generation_profile.csv", index=False)
    print("Generated grid baseline load and solar profile CSVs.")

if __name__ == "__main__":
    generate_raw_dataset()
    clean_and_process_dataset()
    generate_grid_baseline_and_solar()
