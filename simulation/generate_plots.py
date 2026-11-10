"""
Publication-Quality Figure Generator for Project Report & Presentation
Generates 8 high-resolution 300 DPI figures illustrating grid load curves,
transformer thermal degradation, voltage sag profiles, and microgrid dispatch.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os

import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from smart_charge_optimizer import SmartChargeOptimizer
from grid_feeder_model import RadialFeederModel
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "lines.linewidth": 2.2,
    "figure.autolayout": True
})

OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df_ts = pd.read_csv("simulation/scenario_hourly_timeseries.csv")
with open("simulation/simulation_summary.json") as f:
    summary = json.load(f)

hours = df_ts["hour"]

# Color palette
C_BASE = "#64748B"       # Slate Gray
C_UNCONTROLLED = "#EF4444" # Crimson Red
C_TOU = "#F59E0B"         # Amber
C_SMART = "#06B6D4"       # Cyan / Teal
C_V2G = "#10B981"         # Emerald Green
C_LIMIT = "#7F1D1D"       # Dark Red limit line

# -------------------------------------------------------------
# Figure 1: Feeder 24h Net Load Profiles across Scenarios
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.plot(hours, df_ts["baseline_load_mw"], label="Baseline (No EVs)", color=C_BASE, linestyle="--", linewidth=2.0)
ax.plot(hours, df_ts["uncontrolled_charging_load_mw"], label="Scenario A: Uncontrolled Charging", color=C_UNCONTROLLED)
ax.plot(hours, df_ts["static_tou_tariff_load_mw"], label="Scenario B: Static TOU Tariff", color=C_TOU)
ax.plot(hours, df_ts["smart_valley_filling_load_mw"], label="Scenario C: Smart Valley Filling", color=C_SMART)
ax.plot(hours, df_ts["sustainable_microgrid_v2g_plus_solar_load_mw"], label="Scenario D: Microgrid (Solar + V2G)", color=C_V2G, linewidth=2.6)

# Capacity lines
ax.axhline(2.375, color=C_LIMIT, linestyle="-.", linewidth=1.8, label="Transformer Nameplate Rating (2.375 MW)")
ax.axhline(2.650, color="#991B1B", linestyle=":", linewidth=1.5, label="Substation Emergency Limit (2.650 MW)")

# Annotations
ax.annotate("Evening Coincident Peak\n(87.7% Overload)", 
            xy=(19.5, float(df_ts['uncontrolled_charging_load_mw'].max())),
            xytext=(14, 4.3),
            arrowprops=dict(facecolor=C_UNCONTROLLED, shrink=0.08, width=1.5, headwidth=7),
            fontweight="bold", color=C_UNCONTROLLED, bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec=C_UNCONTROLLED, lw=1))

ax.annotate("TOU Avalanche Peak\n(Timer Synchronization)", 
            xy=(23, float(df_ts.loc[df_ts['hour']==23, 'static_tou_tariff_load_mw'].values[0])),
            xytext=(16.5, 3.6),
            arrowprops=dict(facecolor=C_TOU, shrink=0.08, width=1.5, headwidth=7),
            fontweight="bold", color=C_TOU, bbox=dict(boxstyle="round,pad=0.3", fc="#FFFBEB", ec=C_TOU, lw=1))

ax.set_title("Figure 1: 24-Hour Feeder Net Load Profile Across Charging Paradigms", fontweight="bold", pad=12)
ax.set_xlabel("Hour of the Day (00:00 - 23:00)")
ax.set_ylabel("Substation Net Load (MW)")
ax.set_xlim(0, 23)
ax.set_ylim(0.4, 4.8)
ax.set_xticks(range(0, 24, 2))
ax.legend(loc="upper left", framealpha=0.92)
plt.savefig(f"{OUTPUT_DIR}/fig1_load_profiles_comparison.png")
plt.close()

# -------------------------------------------------------------
# Figure 2: Transformer Winding Hot-spot Temperature (IEEE C57.91)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.plot(hours, df_ts["baseline_no_evs_hotspot_c"], label="Baseline (No EVs)", color=C_BASE, linestyle="--")
ax.plot(hours, df_ts["uncontrolled_charging_hotspot_c"], label="Uncontrolled Charging (Peak: 189.4°C)", color=C_UNCONTROLLED)
ax.plot(hours, df_ts["static_tou_tariff_hotspot_c"], label="Static TOU Tariff (Peak: 176.2°C)", color=C_TOU)
ax.plot(hours, df_ts["smart_valley_filling_hotspot_c"], label="Smart Valley Filling (Peak: 102.2°C)", color=C_SMART)
ax.plot(hours, df_ts["sustainable_microgrid_v2g_plus_solar_hotspot_c"], label="Microgrid Solar + V2G (Peak: 97.0°C)", color=C_V2G, linewidth=2.5)

ax.axhline(110.0, color="#B91C1C", linestyle="-.", linewidth=2.0, label="IEEE C57.91 Continuous Normal Limit (110°C)")
ax.fill_between(hours, 110, 200, color="#FEE2E2", alpha=0.35, label="Insulation Thermal Hazard Zone (FAA >> 1.0)")

ax.set_title("Figure 2: Distribution Transformer Winding Hot-Spot Temperature Dynamics", fontweight="bold", pad=12)
ax.set_xlabel("Hour of the Day (00:00 - 23:00)")
ax.set_ylabel("Hot-Spot Temperature (°C)")
ax.set_xlim(0, 23)
ax.set_ylim(40, 200)
ax.set_xticks(range(0, 24, 2))
ax.legend(loc="upper left", framealpha=0.92)
plt.savefig(f"{OUTPUT_DIR}/fig2_transformer_hotspot_temp.png")
plt.close()

# -------------------------------------------------------------
# Figure 3: Radial Feeder Voltage Sag Profile across Nodes (Bus 1 to 13)
# -------------------------------------------------------------
from grid_feeder_model import RadialFeederModel
feeder = RadialFeederModel(13, 12.47)
peak_uncontrolled_mw = summary["uncontrolled_charging"]["peak_load_mw"]
peak_tou_mw = summary["static_tou_tariff"]["peak_load_mw"]
peak_smart_mw = summary["smart_valley_filling"]["peak_load_mw"]
peak_v2g_mw = summary["sustainable_microgrid_v2g_plus_solar"]["peak_load_mw"]
peak_base_mw = summary["baseline_no_evs"]["peak_load_mw"]

v_base = feeder.solve_feeder_snapshot(peak_base_mw)["bus_voltages_pu"]
v_uncontrolled = feeder.solve_feeder_snapshot(peak_uncontrolled_mw)["bus_voltages_pu"]
v_tou = feeder.solve_feeder_snapshot(peak_tou_mw)["bus_voltages_pu"]
v_smart = feeder.solve_feeder_snapshot(peak_smart_mw)["bus_voltages_pu"]
v_v2g = feeder.solve_feeder_snapshot(peak_v2g_mw)["bus_voltages_pu"]

buses = np.arange(1, 14)
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.plot(buses, v_base, 'o--', color=C_BASE, label=f"Baseline Peak ({peak_base_mw:.2f} MW)")
ax.plot(buses, v_uncontrolled, 's-', color=C_UNCONTROLLED, label=f"Uncontrolled Peak ({peak_uncontrolled_mw:.2f} MW)")
ax.plot(buses, v_tou, '^-', color=C_TOU, label=f"TOU Rebound Peak ({peak_tou_mw:.2f} MW)")
ax.plot(buses, v_smart, 'd-', color=C_SMART, label=f"Smart Coordinated Peak ({peak_smart_mw:.2f} MW)")
ax.plot(buses, v_v2g, 'p-', color=C_V2G, linewidth=2.5, label=f"Microgrid Solar+V2G Peak ({peak_v2g_mw:.2f} MW)")

ax.axhline(0.95, color="#DC2626", linestyle="-.", linewidth=2.0, label="ANSI C84.1 Minimum Voltage Standard (0.95 p.u.)")
ax.fill_between(buses, 0.90, 0.95, color="#FEE2E2", alpha=0.35, label="Under-Voltage Brownout Zone")

ax.set_title("Figure 3: Feeder Bus Voltage Sag Profiles at Peak Loading", fontweight="bold", pad=12)
ax.set_xlabel("Distribution Feeder Bus Index (Bus 1 Substation -> Bus 13 Feeder Tail)")
ax.set_ylabel("Bus Voltage (Per-Unit p.u.)")
ax.set_xlim(1, 13)
ax.set_ylim(0.94, 1.01)
ax.set_xticks(range(1, 14))
ax.legend(loc="lower left", framealpha=0.92)
plt.savefig(f"{OUTPUT_DIR}/fig3_feeder_voltage_sag.png")
plt.close()

# -------------------------------------------------------------
# Figure 4: EV Charging Demand Breakdown by User Cluster
# -------------------------------------------------------------
df_cleaned = pd.read_csv("datasets/cleaned_ev_charging_data.csv")
agg_type = df_cleaned.groupby("user_type").agg(
    count=("session_id", "count"),
    total_energy_kwh=("energy_requested_kwh", "sum"),
    mean_flexibility=("charging_flexibility_index", "mean"),
    mean_power_kw=("charger_power_rating_kw", "mean")
).reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
colors_donut = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444"]
labels = [x.replace("_", " ") for x in agg_type["user_type"]]

wedges, texts, autotexts = ax1.pie(
    agg_type["total_energy_kwh"], 
    labels=labels, 
    autopct='%1.1f%%',
    startangle=140, 
    colors=colors_donut,
    wedgeprops=dict(width=0.4, edgecolor='w')
)
for at in autotexts:
    at.set_fontweight("bold")
ax1.set_title("A. Energy Demand Share by EV User Type", fontweight="bold")

bars = ax2.bar(range(len(labels)), agg_type["mean_flexibility"], color=colors_donut, edgecolor="#334155", width=0.55)
ax2.axhline(1.0, color="#DC2626", linestyle="--", linewidth=1.5, label="Flexibility Threshold (Ratio = 1.0)")
ax2.set_ylabel("Charging Flexibility Index (Dwell / Min Time)")
ax2.set_title("B. Load Shifting & V2G Potential Index", fontweight="bold")
ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels, rotation=20, ha="right")
ax2.legend(loc="upper left")

plt.suptitle("Figure 4: EV Telemetry Fleet Composition & Flexibility Potential", fontweight="bold", y=1.02)
plt.savefig(f"{OUTPUT_DIR}/fig4_charging_demand_breakdown.png")
plt.close()

# -------------------------------------------------------------
# Figure 5: Sustainable Microgrid Dispatch (Solar, BESS, V2G)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
p_solar = df_ts["solar_pv_mw"] * 1000.0 # kW
optimizer = SmartChargeOptimizer()
sc_d = optimizer.simulate_scenarios(0.70)["sustainable_microgrid_v2g"]

p_ev_kw = sc_d["ev_load_mw"] * 1000.0
p_bess_kw = sc_d["bess_net_mw"] * 1000.0
p_v2g_kw = sc_d["v2g_mw"] * 1000.0

ax.plot(hours, p_solar, label="Solar PV Generation (800 kWp)", color="#EAB308", linewidth=2.5)
ax.plot(hours, p_ev_kw, label="Coordinated EV Charging Demand", color=C_SMART, linewidth=2.2)
ax.plot(hours, p_bess_kw, label="BESS Net Power (Discharge > 0 / Charge < 0)", color="#8B5CF6", linestyle="--", linewidth=2.0)
ax.plot(hours, p_v2g_kw, label="V2G Fleet Grid Injection (Peak Shaving)", color=C_V2G, linewidth=2.2)

ax.axhline(0, color="#64748B", linestyle=":", linewidth=1.0)
ax.set_title("Figure 5: Sustainable Microgrid Operational Dispatch Strategy", fontweight="bold", pad=12)
ax.set_xlabel("Hour of the Day (00:00 - 23:00)")
ax.set_ylabel("Power Output / Demand (kW)")
ax.set_xlim(0, 23)
ax.set_xticks(range(0, 24, 2))
ax.legend(loc="upper right", framealpha=0.92)
plt.savefig(f"{OUTPUT_DIR}/fig5_solar_v2g_dispatch.png")
plt.close()

# -------------------------------------------------------------
# Figure 6: Transformer Aging Acceleration Factor (F_AA) & Daily Loss of Life
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
scenarios_names = ["Baseline", "Uncontrolled", "Static TOU", "Smart Valley", "Microgrid V2G"]
feq_values = [
    summary["baseline_no_evs"]["aging_acceleration_feq"],
    summary["uncontrolled_charging"]["aging_acceleration_feq"],
    summary["static_tou_tariff"]["aging_acceleration_feq"],
    summary["smart_valley_filling"]["aging_acceleration_feq"],
    summary["sustainable_microgrid_v2g_plus_solar"]["aging_acceleration_feq"]
]
bar_colors = [C_BASE, C_UNCONTROLLED, C_TOU, C_SMART, C_V2G]

bars1 = ax1.bar(range(len(scenarios_names)), feq_values, color=bar_colors, edgecolor="#1E293B", width=0.6)
ax1.set_ylabel("Equivalent Aging Factor (F_EQ) [Log Scale]")
ax1.set_yscale("log")
ax1.set_title("A. Transformer Insulation Degradation Multiplier", fontweight="bold")
ax1.set_xticks(range(len(scenarios_names)))
ax1.set_xticklabels(scenarios_names, rotation=25, ha="right")
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.25, f"{yval:.2f}x", ha='center', va='bottom', fontsize=9, fontweight='bold')

# Loss of life %
lol_values = [
    summary["baseline_no_evs"]["daily_loss_of_life_pct"] * 365,
    summary["uncontrolled_charging"]["daily_loss_of_life_pct"] * 365,
    summary["static_tou_tariff"]["daily_loss_of_life_pct"] * 365,
    summary["smart_valley_filling"]["daily_loss_of_life_pct"] * 365,
    summary["sustainable_microgrid_v2g_plus_solar"]["daily_loss_of_life_pct"] * 365
]
bars2 = ax2.bar(range(len(scenarios_names)), lol_values, color=bar_colors, edgecolor="#1E293B", width=0.6)
ax2.axhline(100.0 / 20.0, color="#DC2626", linestyle="--", label="Normal Annual Design Depr. (5.0%/yr)")
ax2.set_ylabel("Annual Transformer Loss of Life (% LOL / Year)")
ax2.set_title("B. Cumulative Annual Substation Asset Loss of Life", fontweight="bold")
ax2.set_xticks(range(len(scenarios_names)))
ax2.set_xticklabels(scenarios_names, rotation=25, ha="right")
ax2.legend(loc="upper left")

plt.suptitle("Figure 6: IEEE C57.91 Transformer Asset Aging & Reliability Degradation", fontweight="bold", y=1.02)
plt.savefig(f"{OUTPUT_DIR}/fig6_transformer_aging_acceleration.png")
plt.close()

# -------------------------------------------------------------
# Figure 7: Peak-to-Average Ratio (PAR) & Feeder Energy Losses
# -------------------------------------------------------------
pen_levels = [0.20, 0.40, 0.60, 0.80, 1.00]
par_uncontrolled = []
par_smart = []
losses_uncontrolled = []
losses_smart = []

for p in pen_levels:
    sc = optimizer.simulate_scenarios(p)
    # Uncontrolled
    p_unc = sc["uncontrolled"]["net_load_mw"]
    par_unc = np.max(p_unc) / np.mean(p_unc)
    loss_unc = feeder.simulate_24h_voltages(p_unc)["daily_total_loss_mwh"]
    par_uncontrolled.append(par_unc)
    losses_uncontrolled.append(loss_unc)
    # Smart
    p_smt = sc["sustainable_microgrid_v2g"]["net_load_mw"]
    par_smt = np.max(p_smt) / np.mean(p_smt)
    loss_smt = feeder.simulate_24h_voltages(p_smt)["daily_total_loss_mwh"]
    par_smart.append(par_smt)
    losses_smart.append(loss_smt)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
pen_pct = [int(p*100) for p in pen_levels]

ax1.plot(pen_pct, par_uncontrolled, 'o-', color=C_UNCONTROLLED, label="Uncontrolled Charging", linewidth=2.2)
ax1.plot(pen_pct, par_smart, 's-', color=C_V2G, label="Microgrid Solar + V2G", linewidth=2.2)
ax1.set_xlabel("EV Feeder Penetration Rate (%)")
ax1.set_ylabel("Peak-to-Average Ratio (PAR)")
ax1.set_title("A. Grid Load Factor Optimization", fontweight="bold")
ax1.legend()

ax2.plot(pen_pct, losses_uncontrolled, 'o-', color=C_UNCONTROLLED, label="Uncontrolled Line Losses", linewidth=2.2)
ax2.plot(pen_pct, losses_smart, 's-', color=C_V2G, label="Microgrid Line Losses", linewidth=2.2)
ax2.set_xlabel("EV Feeder Penetration Rate (%)")
ax2.set_ylabel("Daily Line Losses (MWh/day)")
ax2.set_title("B. Distribution Feeder I²R Joule Losses", fontweight="bold")
ax2.legend()

plt.suptitle("Figure 7: Impact of Scaling EV Penetration on Grid Efficiency", fontweight="bold", y=1.02)
plt.savefig(f"{OUTPUT_DIR}/fig7_peak_to_average_ratio.png")
plt.close()

# -------------------------------------------------------------
# Figure 8: Grid Carbon Emissions Mitigation
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
co2_data = [
    summary["baseline_no_evs"]["daily_carbon_emissions_kg"],
    summary["uncontrolled_charging"]["daily_carbon_emissions_kg"],
    summary["static_tou_tariff"]["daily_carbon_emissions_kg"],
    summary["smart_valley_filling"]["daily_carbon_emissions_kg"],
    summary["sustainable_microgrid_v2g_plus_solar"]["daily_carbon_emissions_kg"]
]
bars = ax.bar(range(len(scenarios_names)), co2_data, color=bar_colors, edgecolor="#1E293B", width=0.55)
ax.set_ylabel("Daily Grid Operating Emissions (kg CO2 / day)")
ax.set_title("Figure 8: Operational Carbon Abatement via Solar Integration & Smart V2G", fontweight="bold", pad=12)
ax.set_xticks(range(len(scenarios_names)))
ax.set_xticklabels(scenarios_names, rotation=20, ha="right")

# Annotate reduction
co2_diff = summary["uncontrolled_charging"]["daily_carbon_emissions_kg"] - summary["sustainable_microgrid_v2g_plus_solar"]["daily_carbon_emissions_kg"]
ax.annotate(f"3,661 kg CO2/day Avoided\n(-24.6% Operational Footprint)",
            xy=(4, summary["sustainable_microgrid_v2g_plus_solar"]["daily_carbon_emissions_kg"]),
            xytext=(2.3, 13800),
            arrowprops=dict(facecolor=C_V2G, shrink=0.08, width=1.5, headwidth=7),
            fontweight="bold", color="#065F46", bbox=dict(boxstyle="round,pad=0.3", fc="#ECFDF5", ec=C_V2G, lw=1))

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 180, f"{int(yval):,} kg", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylim(0, 16500)
plt.savefig(f"{OUTPUT_DIR}/fig8_carbon_emissions_mitigation.png")
plt.close()

print(f"Generated all 8 figures successfully in {OUTPUT_DIR}/")
