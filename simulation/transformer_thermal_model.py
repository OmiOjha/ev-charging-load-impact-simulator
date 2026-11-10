"""
IEEE Std C57.91-2011 Distribution Transformer Thermal & Degradation Model
Calculates top-oil temperature, winding hot-spot temperature, aging acceleration factor (FAA),
and percentage loss-of-life (%LOL) under dynamic EV charging loads.
"""

import numpy as np
import pandas as pd

class TransformerThermalModel:
    def __init__(self, 
                 rated_mva=2.5, 
                 power_factor=0.95,
                 delta_theta_to_r=55.0,  # Rated top-oil rise over ambient (°C)
                 delta_theta_h_r=25.0,   # Rated hot-spot rise over top-oil (°C)
                 tau_to=3.0,             # Top-oil thermal time constant (hours)
                 tau_w=0.10,             # Winding thermal time constant (hours)
                 loss_ratio_r=5.0,       # Ratio of load losses to no-load losses at rated load
                 oil_exponent_n=0.8,     # Cooling exponent for oil
                 winding_exponent_m=0.8  # Cooling exponent for winding
                 ):
        self.rated_mw = rated_mva * power_factor # ~2.375 MW
        self.delta_theta_to_r = delta_theta_to_r
        self.delta_theta_h_r = delta_theta_h_r
        self.tau_to = tau_to
        self.tau_w = tau_w
        self.R = loss_ratio_r
        self.n = oil_exponent_n
        self.m = winding_exponent_m

    def simulate_24h(self, hourly_load_mw, ambient_temp_c):
        """
        Simulates 24-hour thermal profile given hourly load array and ambient temperature.
        Returns dictionary of time series and aggregate degradation metrics.
        """
        hours = len(hourly_load_mw)
        dt = 1.0 # 1 hour time step

        # Load ratio K = S / S_rated
        K = np.array(hourly_load_mw) / self.rated_mw

        theta_to = np.zeros(hours)
        theta_h = np.zeros(hours)
        faa = np.zeros(hours)

        # Initial steady-state estimate based on hour 0 load
        K0 = K[0]
        delta_to_init = self.delta_theta_to_r * (((K0**2 * self.R + 1.0) / (self.R + 1.0)) ** self.n)
        theta_to[0] = ambient_temp_c[0] + delta_to_init
        delta_h_init = self.delta_theta_h_r * (K0 ** (2 * self.m))
        theta_h[0] = theta_to[0] + delta_h_init

        # Simulate dynamic thermal response using Euler integration
        for t in range(1, hours):
            # Ultimate top-oil rise for current load
            delta_to_u = self.delta_theta_to_r * (((K[t]**2 * self.R + 1.0) / (self.R + 1.0)) ** self.n)
            theta_to_u = ambient_temp_c[t] + delta_to_u

            # Dynamic top-oil temperature update
            theta_to[t] = theta_to[t-1] + (dt / self.tau_to) * (theta_to_u - theta_to[t-1])

            # Ultimate winding hot-spot rise
            delta_h_u = self.delta_theta_h_r * (K[t] ** (2 * self.m))
            # Winding time constant is fast (0.1h), so quasi-steady state is accurate
            theta_h[t] = theta_to[t] + delta_h_u

        # Calculate Aging Acceleration Factor (F_AA) according to IEEE C57.91
        # Reference hot-spot temperature is 110 °C for 65°C rise insulation
        # FAA = exp(15000/383 - 15000 / (Theta_H + 273))
        for t in range(hours):
            temp_kelvin = theta_h[t] + 273.15
            faa[t] = np.exp( (15000.0 / 383.15) - (15000.0 / temp_kelvin) )

        # Equivalent Aging Factor (F_EQ) over 24 hours
        feq = np.mean(faa)

        # Percentage Loss of Life (%LOL) for 24 hours
        # Normal insulation life = 180,000 hours
        normal_daily_lol = (24.0 / 180000.0) * 100.0 # ~0.0133% per normal day
        actual_daily_lol = feq * normal_daily_lol
        relative_life_loss_factor = feq # 1.0 is normal baseline

        return {
            "top_oil_temp_c": np.round(theta_to, 2),
            "hotspot_temp_c": np.round(theta_h, 2),
            "aging_factor_faa": np.round(faa, 3),
            "feq": round(float(feq), 3),
            "max_hotspot_temp_c": round(float(np.max(theta_h)), 2),
            "max_top_oil_temp_c": round(float(np.max(theta_to)), 2),
            "daily_loss_of_life_pct": round(float(actual_daily_lol), 5),
            "normal_daily_loss_pct": round(float(normal_daily_lol), 5),
            "aging_multiplier": round(float(relative_life_loss_factor), 2),
            "max_loading_pct": round(float(np.max(K) * 100.0), 2)
        }
