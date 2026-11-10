"""
Radial Distribution Feeder Power Flow & Voltage Drop Model
Models voltage sag across 13 feeder buses, line resistance/reactance,
voltage deviation index (VDI), and active power line losses.
"""

import numpy as np

class RadialFeederModel:
    def __init__(self, num_buses=13, nominal_kv=12.47):
        self.num_buses = num_buses
        self.nominal_kv = nominal_kv
        self.v_base = 1.0 # Per-unit base voltage at substation (Bus 1)

        # Realistic line impedance parameters along radial feeder segments
        # Distance between nodes ~ 400 - 800 meters, total feeder length ~ 6.5 km
        # R and X in per-unit on 2.5 MVA, 12.47 kV base
        # Z_base = (12.47 kV)^2 / 2.5 MVA = 62.2 ohm
        np.random.seed(101)
        self.r_km = 0.35 # ohm/km
        self.x_km = 0.38 # ohm/km
        self.segment_lengths_km = np.array([0.5, 0.6, 0.4, 0.7, 0.5, 0.6, 0.5, 0.6, 0.4, 0.5, 0.6, 0.6]) # 12 branches
        self.z_base = (nominal_kv ** 2) / 2.5

        self.r_pu = (self.r_km * self.segment_lengths_km) / self.z_base
        self.x_pu = (self.x_km * self.segment_lengths_km) / self.z_base

        # Standard non-EV load distribution fraction across buses 2..13
        # Substation is Bus 1
        self.bus_load_shares = np.array([
            0.00, # Bus 1 (Substation Slack Bus)
            0.05, # Bus 2
            0.08, # Bus 3
            0.09, # Bus 4
            0.07, # Bus 5
            0.12, # Bus 6 (Commercial center)
            0.08, # Bus 7
            0.10, # Bus 8
            0.11, # Bus 9
            0.09, # Bus 10
            0.08, # Bus 11
            0.07, # Bus 12
            0.06  # Bus 13 (Feeder end / rural edge)
        ])

    def solve_feeder_snapshot(self, total_p_mw, total_q_mvar=None):
        """
        Solves radial backward/forward voltage drop approximation (LinDistFlow)
        given total substation active and reactive power.
        """
        if total_q_mvar is None:
            # Assume overall power factor of 0.95 lagging
            total_q_mvar = total_p_mw * np.tan(np.arccos(0.95))

        p_base_mw = 2.5
        total_p_pu = total_p_mw / p_base_mw
        total_q_pu = total_q_mvar / p_base_mw

        bus_p_pu = total_p_pu * self.bus_load_shares
        bus_q_pu = total_q_pu * self.bus_load_shares

        # Cumulative branch flows from tail (Bus 13) to head (Bus 1)
        branch_p_pu = np.zeros(self.num_buses - 1)
        branch_q_pu = np.zeros(self.num_buses - 1)

        # Backward sweep for branch flows
        p_cum = 0.0
        q_cum = 0.0
        for i in reversed(range(self.num_buses - 1)):
            p_cum += bus_p_pu[i + 1]
            q_cum += bus_q_pu[i + 1]
            branch_p_pu[i] = p_cum
            branch_q_pu[i] = q_cum

        # Forward sweep for bus voltages: V_{i+1} = V_i - (r*P + x*Q) / V_i
        voltages_pu = np.ones(self.num_buses)
        branch_losses_pu = np.zeros(self.num_buses - 1)

        for i in range(self.num_buses - 1):
            v_curr = voltages_pu[i]
            # LinDistFlow approximation
            delta_v = (self.r_pu[i] * branch_p_pu[i] + self.x_pu[i] * branch_q_pu[i]) / v_curr
            voltages_pu[i + 1] = max(0.80, v_curr - delta_v)
            # Line loss: I^2 * R ~ (P^2 + Q^2) / V^2 * R
            branch_losses_pu[i] = ((branch_p_pu[i]**2 + branch_q_pu[i]**2) / (v_curr**2)) * self.r_pu[i]

        total_loss_mw = float(np.sum(branch_losses_pu) * p_base_mw)
        min_v_pu = float(np.min(voltages_pu))
        min_v_bus = int(np.argmin(voltages_pu) + 1)
        vdi = float(np.sqrt(np.mean((1.0 - voltages_pu)**2))) # Voltage Deviation Index

        return {
            "bus_voltages_pu": np.round(voltages_pu, 4),
            "min_voltage_pu": round(min_v_pu, 4),
            "min_voltage_bus": min_v_bus,
            "voltage_sag_violation": bool(min_v_pu < 0.95), # ANSI C84.1 Range A (0.95 p.u.)
            "total_line_loss_mw": round(total_loss_mw, 4),
            "voltage_deviation_index": round(vdi, 4)
        }

    def simulate_24h_voltages(self, hourly_load_mw_series):
        """
        Runs voltage snapshot for all 24 hours.
        """
        hourly_min_v = []
        hourly_losses_mw = []
        bus_profiles_24h = []

        for p_mw in hourly_load_mw_series:
            res = self.solve_feeder_snapshot(p_mw)
            hourly_min_v.append(res["min_voltage_pu"])
            hourly_losses_mw.append(res["total_line_loss_mw"])
            bus_profiles_24h.append(res["bus_voltages_pu"])

        return {
            "hourly_min_voltage_pu": np.round(hourly_min_v, 4),
            "hourly_losses_mw": np.round(hourly_losses_mw, 4),
            "daily_total_loss_mwh": round(float(np.sum(hourly_losses_mw)), 3),
            "min_voltage_24h": round(float(np.min(hourly_min_v)), 4),
            "voltage_violation_hours": int(np.sum(np.array(hourly_min_v) < 0.95)),
            "bus_voltages_at_peak": bus_profiles_24h[np.argmax(hourly_load_mw_series)]
        }
