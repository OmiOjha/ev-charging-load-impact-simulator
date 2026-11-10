"""
Smart Charging Optimizer & Scenario Dispatch Engine
Implements Uncontrolled, TOU Rebound, Coordinated Valley Filling,
and Microgrid Solar PV + BESS + V2G bi-directional optimization.
"""

import numpy as np
import pandas as pd

class SmartChargeOptimizer:
    def __init__(self, cleaned_data_path="datasets/cleaned_ev_charging_data.csv",
                 grid_load_path="datasets/distribution_grid_hourly_load.csv",
                 solar_path="datasets/solar_generation_profile.csv"):
        self.df_ev = pd.read_csv(cleaned_data_path)
        self.df_grid = pd.read_csv(grid_load_path)
        self.df_solar = pd.read_csv(solar_path)
        self.hours = 24

    def simulate_scenarios(self, penetration_rate=0.60):
        """
        Runs all 4 scenarios for a given EV penetration rate (0.0 to 1.0).
        Penetration rate maps to a fleet of up to ~1,000 active EVs on the feeder.
        """
        # Sample active fleet according to penetration rate
        sample_size = int(len(self.df_ev) * penetration_rate)
        sample_size = max(50, min(sample_size, len(self.df_ev)))
        fleet = self.df_ev.sample(n=sample_size, random_state=42).copy()

        # Scale factor to represent neighborhood feeder scale (~450-800 residential/commercial units)
        scale_factor = 0.22 * (penetration_rate / 0.60)

        # Baseline grid load
        p_base = self.df_grid["baseline_load_mw"].values
        p_solar_mw = self.df_solar["solar_generation_kw"].values / 1000.0 # Convert to MW
        ambient_temp = self.df_grid["ambient_temp_celsius"].values

        # -----------------------------------------------------------------
        # Scenario A: Uncontrolled / Dumb Charging
        # -----------------------------------------------------------------
        ev_uncontrolled_hourly_kw = np.zeros(24)
        for _, row in fleet.iterrows():
            arr_h = int(np.floor(row["arrival_hour_float"])) % 24
            e_req = row["energy_requested_kwh"]
            p_max = row["charger_power_rating_kw"]
            remaining_e = e_req
            curr_h = arr_h
            while remaining_e > 0:
                p_deliver = min(p_max, remaining_e)
                ev_uncontrolled_hourly_kw[curr_h % 24] += p_deliver
                remaining_e -= p_deliver
                curr_h += 1
                if curr_h - arr_h > 24:
                    break

        p_ev_uncontrolled_mw = (ev_uncontrolled_hourly_kw * scale_factor) / 1000.0
        p_net_uncontrolled = p_base + p_ev_uncontrolled_mw

        # -----------------------------------------------------------------
        # Scenario B: Static Time-of-Use (TOU) Tariff with Rebound Peak
        # -----------------------------------------------------------------
        # 75% of residential users set timer to 23:00 (off-peak start)
        # Commercial and fast chargers charge upon arrival
        ev_tou_hourly_kw = np.zeros(24)
        for _, row in fleet.iterrows():
            e_req = row["energy_requested_kwh"]
            p_max = row["charger_power_rating_kw"]
            user_t = row["user_type"]
            arr_h = int(np.floor(row["arrival_hour_float"])) % 24

            if user_t == "Residential_Commuter" and (arr_h >= 16 or arr_h <= 22):
                start_h = 23 # Delay to 11 PM
            else:
                start_h = arr_h

            remaining_e = e_req
            curr_h = start_h
            while remaining_e > 0:
                p_deliver = min(p_max, remaining_e)
                ev_tou_hourly_kw[curr_h % 24] += p_deliver
                remaining_e -= p_deliver
                curr_h += 1
                if curr_h - start_h > 24:
                    break

        p_ev_tou_mw = (ev_tou_hourly_kw * scale_factor) / 1000.0
        p_net_tou = p_base + p_ev_tou_mw

        # -----------------------------------------------------------------
        # Scenario C: Smart Coordinated Charging (Valley Filling)
        # -----------------------------------------------------------------
        # Flatten net load by shifting deferrable charging into nighttime valley (00:00 - 06:00)
        # and daytime solar window (11:00 - 14:00)
        total_ev_energy_mwh = np.sum(p_ev_uncontrolled_mw)
        # Target flat level:
        valley_hours = [0, 1, 2, 3, 4, 5, 6, 11, 12, 13, 14]
        non_deferrable_mask = np.ones(24, dtype=bool)
        non_deferrable_mask[valley_hours] = False

        # Non-deferrable portion (workplace / DC fast / immediate needs ~25%)
        p_ev_smart_mw = np.zeros(24)
        p_ev_smart_mw = p_ev_uncontrolled_mw * 0.22 # Must charge immediately

        # Allocating remaining 78% energy inversely proportional to baseline load (water-filling)
        deferrable_energy = total_ev_energy_mwh - np.sum(p_ev_smart_mw)
        # Valley filling weights
        inv_load_weights = np.maximum(0.0, 1.95 - p_base)
        inv_load_weights[17:22] = 0.05 # Suppress evening peak hours 5 PM - 10 PM
        inv_load_weights = inv_load_weights / np.sum(inv_load_weights)
        p_ev_smart_mw += deferrable_energy * inv_load_weights
        p_net_smart = p_base + p_ev_smart_mw

        # -----------------------------------------------------------------
        # Scenario D: Sustainable Microgrid (Solar PV + BESS + V2G)
        # -----------------------------------------------------------------
        # 1. Solar PV absorbs daytime demand
        # 2. BESS (400 kW / 1200 kWh):
        #    - Charges during peak solar (10:00 - 15:00) up to 350 kW
        #    - Discharges during evening peak (18:00 - 21:00) up to 350 kW
        # 3. V2G: Eligible parked vehicles (v2g_ready & flexibility > 1.5)
        #    - Discharges up to 2.5 kW each during peak (18:00 - 21:00), providing ~0.25 MW relief
        #    - Recharges overnight
        p_bess_discharge_mw = np.zeros(24)
        p_bess_charge_mw = np.zeros(24)

        # BESS charging on excess solar
        for h in [10, 11, 12, 13, 14]:
            p_bess_charge_mw[h] = min(0.35, p_solar_mw[h] * 0.7)
        # BESS discharging at peak
        for h in [18, 19, 20, 21]:
            p_bess_discharge_mw[h] = 0.32

        # V2G injection
        p_v2g_mw = np.zeros(24)
        v2g_eligible_fraction = 0.40 * penetration_rate
        for h in [18, 19, 20]:
            p_v2g_mw[h] = 0.22 * v2g_eligible_fraction

        # Recharging V2G vehicles overnight (01:00 - 05:00)
        v2g_replenish_per_hour = np.sum(p_v2g_mw) / 4.0
        for h in [2, 3, 4, 5]:
            p_v2g_mw[h] -= v2g_replenish_per_hour # Negative means load/recharge

        # Net load for Scenario D
        # Net Load = P_base + P_ev_smart - P_solar - P_bess_net - P_v2g
        p_bess_net_mw = p_bess_discharge_mw - p_bess_charge_mw # Positive = power supplied to grid
        p_net_microgrid = p_base + p_ev_smart_mw - p_solar_mw - p_bess_net_mw - p_v2g_mw
        p_net_microgrid = np.clip(p_net_microgrid, 0.40, 2.5) # Physical floor

        return {
            "hours": np.arange(24),
            "baseline_load_mw": np.round(p_base, 3),
            "solar_generation_mw": np.round(p_solar_mw, 3),
            "uncontrolled": {
                "ev_load_mw": np.round(p_ev_uncontrolled_mw, 3),
                "net_load_mw": np.round(p_net_uncontrolled, 3)
            },
            "tou_tariff": {
                "ev_load_mw": np.round(p_ev_tou_mw, 3),
                "net_load_mw": np.round(p_net_tou, 3)
            },
            "smart_valley_filling": {
                "ev_load_mw": np.round(p_ev_smart_mw, 3),
                "net_load_mw": np.round(p_net_smart, 3)
            },
            "sustainable_microgrid_v2g": {
                "ev_load_mw": np.round(p_ev_smart_mw, 3),
                "bess_net_mw": np.round(p_bess_net_mw, 3),
                "v2g_mw": np.round(p_v2g_mw, 3),
                "net_load_mw": np.round(p_net_microgrid, 3)
            },
            "ambient_temp_c": ambient_temp,
            "rated_transformer_mw": 2.375,
            "emergency_limit_mw": 2.650
        }
