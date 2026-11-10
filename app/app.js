/**
 * VoltGrid™ Web Simulator Engine
 * Live Grid Dispatch, Transformer Thermal Modeling, Voltage Flow, and Interactive UI
 */

// Grid Constants
const SUBSTATION_RATED_MW = 2.375; // 2.5 MVA at 0.95 PF
const SUBSTATION_EMERGENCY_MW = 2.650;
const ANSI_MIN_VOLTAGE = 0.950;
const IEEE_HOTSPOT_LIMIT_C = 110.0;

// Base 24h Non-EV load profile (MW)
const BASELINE_LOAD_MW = [
  0.78, 0.75, 0.72, 0.71, 0.74, 0.82, 0.98, 1.25, 1.42, 1.38, 
  1.32, 1.28, 1.25, 1.22, 1.20, 1.25, 1.35, 1.55, 1.68, 1.72, 
  1.65, 1.45, 1.15, 0.92
];

// Solar capacity factor (normalized 0 to 1)
const SOLAR_PROFILE = [
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.18, 0.42, 0.68, 
  0.88, 0.98, 1.00, 0.95, 0.82, 0.60, 0.32, 0.12, 0.02, 0.0, 
  0.0, 0.0, 0.0, 0.0
];

// Marginal grid carbon intensity (kg CO2 / MWh)
const CARBON_INTENSITY = [
  160, 150, 150, 150, 160, 180, 240, 320, 310, 220, 140, 100, 
  90, 90, 120, 210, 330, 480, 520, 510, 480, 380, 280, 210
];

// State
let currentScenario = 'uncontrolled';
let evPenetration = 0.70;
let solarCapacityKw = 800;
let bessCapacityKwh = 1200;
let overlayAll = true;

// Sample fleet telemetry dataset (first 25 records for table)
const FLEET_SAMPLES = [
  { id: "SES-00101", model: "Tesla Model 3", batt: 60, user: "Residential Commuter", evse: "Level 2 (7.2kW)", arr: "18:24", soc: "32% -> 80%", req: "32.0 kWh", flex: "2.7x", v2g: "Yes" },
  { id: "SES-00102", model: "Tesla Model Y", batt: 75, user: "Residential Commuter", evse: "Level 2 (11.0kW)", arr: "19:05", soc: "28% -> 90%", req: "51.7 kWh", flex: "2.3x", v2g: "Yes" },
  { id: "SES-00103", model: "Ford F-150 Lightning", batt: 98, user: "Residential Commuter", evse: "Level 2 (19.2kW)", arr: "17:45", soc: "41% -> 90%", req: "53.4 kWh", flex: "3.8x", v2g: "Yes" },
  { id: "SES-00104", model: "Nissan Leaf", batt: 40, user: "Residential Commuter", evse: "Level 2 (6.6kW)", arr: "18:10", soc: "20% -> 85%", req: "28.9 kWh", flex: "2.5x", v2g: "Yes" },
  { id: "SES-00105", model: "Hyundai Ioniq 5", batt: 77, user: "Workplace Commuter", evse: "Level 2 (11.0kW)", arr: "08:35", soc: "45% -> 85%", req: "34.4 kWh", flex: "2.6x", v2g: "Yes" },
  { id: "SES-00106", model: "Chevy Bolt EV", batt: 65, user: "Residential Commuter", evse: "Level 2 (7.2kW)", arr: "19:30", soc: "38% -> 80%", req: "30.3 kWh", flex: "2.4x", v2g: "No" },
  { id: "SES-00107", model: "Commercial Van", batt: 85, user: "Commercial Fleet", evse: "Level 2 (22.0kW)", arr: "20:15", soc: "18% -> 90%", req: "68.0 kWh", flex: "1.9x", v2g: "No" },
  { id: "SES-00108", model: "Tesla Model 3", batt: 60, user: "Public Fastcharge", evse: "DC Fast (50kW)", arr: "14:20", soc: "15% -> 80%", req: "43.3 kWh", flex: "0.8x", v2g: "No" },
  { id: "SES-00109", model: "Hyundai Ioniq 5", batt: 77, user: "Residential Commuter", evse: "Level 2 (11.0kW)", arr: "18:50", soc: "35% -> 90%", req: "47.1 kWh", flex: "2.5x", v2g: "Yes" },
  { id: "SES-00110", model: "Tesla Model Y", batt: 75, user: "Workplace Commuter", evse: "Level 2 (11.0kW)", arr: "08:15", soc: "40% -> 80%", req: "33.3 kWh", flex: "2.8x", v2g: "Yes" },
  { id: "SES-00111", model: "Ford F-150 Lightning", batt: 98, user: "Residential Commuter", evse: "Level 2 (11.0kW)", arr: "17:15", soc: "25% -> 85%", req: "65.3 kWh", flex: "2.2x", v2g: "Yes" },
  { id: "SES-00112", model: "Chevy Bolt EV", batt: 65, user: "Workplace Commuter", evse: "Level 2 (7.2kW)", arr: "09:00", soc: "50% -> 80%", req: "21.7 kWh", flex: "2.7x", v2g: "No" },
  { id: "SES-00113", model: "Nissan Leaf", batt: 40, user: "Public Fastcharge", evse: "DC Fast (50kW)", arr: "13:05", soc: "20% -> 80%", req: "26.7 kWh", flex: "0.9x", v2g: "No" },
  { id: "SES-00114", model: "Tesla Model 3", batt: 60, user: "Residential Commuter", evse: "Level 2 (7.2kW)", arr: "18:40", soc: "30% -> 85%", req: "36.7 kWh", flex: "2.3x", v2g: "Yes" },
  { id: "SES-00115", model: "Commercial Van", batt: 85, user: "Commercial Fleet", evse: "Level 2 (22.0kW)", arr: "19:50", soc: "22% -> 85%", req: "59.5 kWh", flex: "2.1x", v2g: "No" }
];

// Calculation functions
function computeProfiles(pen, solarKw, bessKwh) {
  const hours = Array.from({ length: 24 }, (_, i) => i);
  const pBase = [...BASELINE_LOAD_MW];
  const pSolarMw = SOLAR_PROFILE.map(cf => (cf * solarKw) / 1000.0);

  // Scaled EV demands
  const evTotalMwh = 24.5 * (pen / 0.70); // Fleet daily energy

  // 1. Uncontrolled profile: Peak between 18:00 - 21:00
  const evUncontrolled = hours.map(h => {
    let factor = 0.01;
    if (h >= 17 && h <= 22) factor = 0.16 + 0.04 * Math.sin((h - 17) / 5 * Math.PI);
    else if (h >= 8 && h <= 12) factor = 0.05;
    else if (h >= 23 || h <= 5) factor = 0.02;
    return (evTotalMwh * factor);
  });
  const netUncontrolled = hours.map(h => pBase[h] + evUncontrolled[h]);

  // 2. TOU Tariff: Massive rebound spike at 23:00 (11 PM)
  const evTou = hours.map(h => {
    let factor = 0.015;
    if (h === 23) factor = 0.32;
    else if (h === 0 || h === 1) factor = 0.22;
    else if (h >= 2 && h <= 5) factor = 0.06;
    else if (h >= 8 && h <= 12) factor = 0.04;
    return (evTotalMwh * factor);
  });
  const netTou = hours.map(h => pBase[h] + evTou[h]);

  // 3. Smart Valley Filling: Smooth distribution into valley
  const evSmart = hours.map(h => {
    let factor = 0.02;
    if (h >= 0 && h <= 5) factor = 0.12;
    else if (h >= 11 && h <= 14) factor = 0.08;
    else if (h >= 18 && h <= 21) factor = 0.02; // Peak shaved
    return (evTotalMwh * factor);
  });
  const netSmart = hours.map(h => pBase[h] + evSmart[h]);

  // 4. Sustainable Microgrid + V2G
  // Solar absorbs daytime; BESS discharges at peak; V2G injects at peak
  const bessPowerMaxMw = Math.min(0.40, bessKwh / 3000.0);
  const netMicrogrid = hours.map(h => {
    let p = pBase[h] + evSmart[h] - pSolarMw[h];
    // BESS action
    if (h >= 18 && h <= 21) {
      p -= bessPowerMaxMw; // BESS discharge
      p -= 0.18 * pen; // V2G fleet injection
    } else if (h >= 11 && h <= 14) {
      p += bessPowerMaxMw * 0.7; // BESS solar charge
    } else if (h >= 1 && h <= 4) {
      p += 0.08 * pen; // V2G overnight recharge
    }
    return Math.max(0.45, p);
  });

  return {
    hours,
    pBase,
    pSolarMw,
    uncontrolled: netUncontrolled,
    tou: netTou,
    smart: netSmart,
    microgrid: netMicrogrid
  };
}

// Thermal hot-spot temperature simulation
function computeThermalMetrics(loadSeries) {
  const peakMw = Math.max(...loadSeries);
  const K_peak = peakMw / SUBSTATION_RATED_MW;
  // IEEE C57.91 estimate: Theta_H ~ 30 + 55*(K^1.6) + 25*(K^1.6)
  const hotspotC = 30 + 80.0 * Math.pow(K_peak, 1.6);
  // FAA = exp(15000/383.15 - 15000/(Theta_H + 273.15))
  const faa = Math.exp( (15000.0 / 383.15) - (15000.0 / (hotspotC + 273.15)) );
  return {
    peakMw: peakMw.toFixed(3),
    hotspotC: hotspotC.toFixed(1),
    faa: faa.toFixed(2),
    overloadPct: Math.max(0, ((peakMw - SUBSTATION_RATED_MW) / SUBSTATION_RATED_MW * 100)).toFixed(1)
  };
}

// Feeder voltage drop calculation across 13 buses
function computeVoltageProfile(peakMw) {
  const buses = Array.from({ length: 13 }, (_, i) => i + 1);
  const loadRatio = peakMw / 2.5;
  // LinDistFlow radial drop approximation
  const voltages = buses.map(b => {
    if (b === 1) return 1.0;
    const drop = 0.0042 * (b - 1) * loadRatio;
    return Math.max(0.85, 1.0 - drop);
  });
  const minV = Math.min(...voltages);
  return { buses, voltages, minV: minV.toFixed(3) };
}

// Carbon emissions calculation
function computeDailyCarbon(loadSeries) {
  let totalCo2 = 0;
  for (let h = 0; h < 24; h++) {
    totalCo2 += loadSeries[h] * CARBON_INTENSITY[h];
  }
  return Math.round(totalCo2);
}

// Charts
let loadChartInstance = null;
let voltageChartInstance = null;

function initCharts() {
  const ctxLoad = document.getElementById('loadChart').getContext('2d');
  const ctxVoltage = document.getElementById('voltageChart').getContext('2d');

  loadChartInstance = new Chart(ctxLoad, {
    type: 'line',
    data: {
      labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1E293B',
          titleColor: '#F8FAFC',
          bodyColor: '#94A3B8',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)} MW`
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748B', font: { family: "'JetBrains Mono', monospace", size: 10 } }
        },
        y: {
          min: 0.4,
          suggestedMax: 4.8,
          grid: { color: 'rgba(255, 255, 255, 0.06)' },
          ticks: { color: '#64748B', font: { family: "'JetBrains Mono', monospace", size: 10 } },
          title: { display: true, text: 'Substation Load (MW)', color: '#94A3B8', font: { size: 11 } }
        }
      }
    }
  });

  voltageChartInstance = new Chart(ctxVoltage, {
    type: 'line',
    data: {
      labels: Array.from({ length: 13 }, (_, i) => `Bus ${i+1}`),
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748B', font: { family: "'JetBrains Mono', monospace", size: 9 } }
        },
        y: {
          min: 0.93,
          max: 1.01,
          grid: { color: 'rgba(255, 255, 255, 0.06)' },
          ticks: { color: '#64748B', font: { family: "'JetBrains Mono', monospace", size: 9 } },
          title: { display: true, text: 'Voltage (p.u.)', color: '#94A3B8', font: { size: 10 } }
        }
      }
    }
  });
}

function updateSimulation() {
  const profiles = computeProfiles(evPenetration, solarCapacityKw, bessCapacityKwh);
  const activeSeries = profiles[currentScenario];

  // Thermal & voltage results
  const metricsUnc = computeThermalMetrics(profiles.uncontrolled);
  const metricsTou = computeThermalMetrics(profiles.tou);
  const metricsSmart = computeThermalMetrics(profiles.smart);
  const metricsMicro = computeThermalMetrics(profiles.microgrid);
  const activeMetrics = computeThermalMetrics(activeSeries);

  const vRes = computeVoltageProfile(activeMetrics.peakMw);
  const co2Active = computeDailyCarbon(activeSeries);

  // Update KPI Ribbon
  document.getElementById('kpi-peak-val').innerText = activeMetrics.peakMw;
  const barPeak = document.getElementById('bar-peak-load');
  const overloadText = document.getElementById('kpi-peak-overload');
  if (parseFloat(activeMetrics.peakMw) > SUBSTATION_RATED_MW) {
    barPeak.className = 'fill-bar danger';
    barPeak.style.width = Math.min(100, (activeMetrics.peakMw / 4.8) * 100) + '%';
    overloadText.innerText = `+${activeMetrics.overloadPct}% Above Nameplate (2.38 MW)`;
    overloadText.style.color = '#EF4444';
  } else {
    barPeak.className = 'fill-bar success';
    barPeak.style.width = Math.min(100, (activeMetrics.peakMw / 4.8) * 100) + '%';
    overloadText.innerText = `Normal Range (-${(100 - (activeMetrics.peakMw/SUBSTATION_RATED_MW)*100).toFixed(1)}% Headroom)`;
    overloadText.style.color = '#10B981';
  }

  // Hot-spot KPI
  document.getElementById('kpi-hotspot-val').innerText = activeMetrics.hotspotC;
  document.getElementById('kpi-aging-mult').innerText = `${activeMetrics.faa}x`;
  const barHotspot = document.getElementById('bar-hotspot');
  if (parseFloat(activeMetrics.hotspotC) > IEEE_HOTSPOT_LIMIT_C) {
    barHotspot.className = 'fill-bar critical';
    barHotspot.style.width = '100%';
  } else {
    barHotspot.className = 'fill-bar success';
    barHotspot.style.width = ((activeMetrics.hotspotC / 120.0) * 100) + '%';
  }

  // Voltage KPI
  document.getElementById('kpi-voltage-val').innerText = vRes.minV;
  const barVoltage = document.getElementById('bar-voltage');
  const busChip = document.getElementById('bus-status-chip');
  if (parseFloat(vRes.minV) < ANSI_MIN_VOLTAGE) {
    barVoltage.className = 'fill-bar danger';
    busChip.className = 'chip-badge danger';
    busChip.innerText = 'Voltage Sag Violation (<0.95)';
    busChip.style.background = 'rgba(239, 68, 68, 0.2)';
    busChip.style.color = '#F87171';
  } else {
    barVoltage.className = 'fill-bar success';
    busChip.className = 'chip-badge info';
    busChip.innerText = 'ANSI C84.1 Compliant';
    busChip.style.background = 'rgba(16, 185, 129, 0.15)';
    busChip.style.color = '#34D399';
  }

  // Carbon KPI
  document.getElementById('kpi-carbon-val').innerText = co2Active.toLocaleString();
  const carbonDiff = computeDailyCarbon(profiles.uncontrolled) - co2Active;
  const carbonSub = document.getElementById('kpi-carbon-mitigated');
  if (carbonDiff > 100) {
    carbonSub.innerText = `-${carbonDiff.toLocaleString()} kg CO2/day Avoided!`;
    carbonSub.style.color = '#10B981';
  } else {
    carbonSub.innerText = 'Peaker Gas Generation Active';
    carbonSub.style.color = '#94A3B8';
  }

  // Update Load Chart Datasets
  const datasets = [];
  // Rated line
  datasets.push({
    label: 'Transformer Rating (2.375 MW)',
    data: Array(24).fill(SUBSTATION_RATED_MW),
    borderColor: '#7F1D1D',
    borderWidth: 1.5,
    borderDash: [6, 4],
    pointRadius: 0,
    fill: false
  });

  // Baseline
  datasets.push({
    label: 'Baseline (No EVs)',
    data: profiles.pBase,
    borderColor: '#64748B',
    borderWidth: 1.8,
    borderDash: [4, 4],
    pointRadius: 0,
    fill: false
  });

  if (overlayAll) {
    datasets.push({
      label: 'A. Uncontrolled',
      data: profiles.uncontrolled,
      borderColor: '#EF4444',
      borderWidth: currentScenario === 'uncontrolled' ? 3.0 : 1.4,
      pointRadius: 0
    });
    datasets.push({
      label: 'B. Static TOU Tariff',
      data: profiles.tou,
      borderColor: '#F59E0B',
      borderWidth: currentScenario === 'tou' ? 3.0 : 1.4,
      pointRadius: 0
    });
    datasets.push({
      label: 'C. Smart Valley Filling',
      data: profiles.smart,
      borderColor: '#06B6D4',
      borderWidth: currentScenario === 'smart' ? 3.0 : 1.4,
      pointRadius: 0
    });
    datasets.push({
      label: 'D. Microgrid Solar + V2G',
      data: profiles.microgrid,
      borderColor: '#10B981',
      borderWidth: currentScenario === 'microgrid' ? 3.2 : 1.4,
      pointRadius: 0
    });
  } else {
    // Only active scenario
    const colors = {
      uncontrolled: '#EF4444',
      tou: '#F59E0B',
      smart: '#06B6D4',
      microgrid: '#10B981'
    };
    datasets.push({
      label: currentScenario.toUpperCase(),
      data: activeSeries,
      borderColor: colors[currentScenario],
      borderWidth: 3.0,
      pointRadius: 3
    });
  }

  loadChartInstance.data.datasets = datasets;
  loadChartInstance.update('none');

  // Update Voltage Chart
  voltageChartInstance.data.datasets = [
    {
      label: 'ANSI C84.1 Min (0.95 p.u.)',
      data: Array(13).fill(0.950),
      borderColor: '#DC2626',
      borderWidth: 1.5,
      borderDash: [5, 4],
      pointRadius: 0
    },
    {
      label: 'Bus Voltage Profile',
      data: vRes.voltages,
      borderColor: parseFloat(vRes.minV) < 0.95 ? '#EF4444' : '#10B981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      borderWidth: 2.5,
      pointRadius: 4,
      pointBackgroundColor: '#F8FAFC'
    }
  ];
  voltageChartInstance.update('none');

  // Update Feeder Heatmap Bar
  const heatmapBar = document.getElementById('heatmap-bar');
  if (parseFloat(vRes.minV) < 0.95) {
    heatmapBar.style.background = 'linear-gradient(to right, #10B981 0%, #F59E0B 45%, #EF4444 80%)';
  } else {
    heatmapBar.style.background = 'linear-gradient(to right, #10B981 0%, #10B981 70%, #34D399 100%)';
  }

  // Update Matrix Table
  const tbody = document.getElementById('matrix-tbody');
  const scenariosSummary = [
    { name: "Uncontrolled", m: metricsUnc, status: "Critical Overload", badge: "danger" },
    { name: "Static TOU", m: metricsTou, status: "Rebound Peak", badge: "danger" },
    { name: "Smart Valley", m: metricsSmart, status: "Feeder Safe", badge: "safe" },
    { name: "Microgrid + V2G", m: metricsMicro, status: "Optimized & Green", badge: "safe" }
  ];

  tbody.innerHTML = scenariosSummary.map(s => `
    <tr>
      <td><strong>${s.name}</strong></td>
      <td>${s.m.peakMw} MW</td>
      <td style="color: ${parseFloat(s.m.hotspotC) > 110 ? '#F87171' : '#34D399'}">${s.m.hotspotC} °C</td>
      <td>${s.m.faa}x</td>
      <td><span class="matrix-badge ${s.badge}">${s.status}</span></td>
    </tr>
  `).join('');

  // Update Callout Banner
  const banner = document.getElementById('v2g-callout');
  const avoidedCo2 = (computeDailyCarbon(profiles.uncontrolled) - computeDailyCarbon(profiles.microgrid));
  const tempReduction = (metricsUnc.hotspotC - metricsMicro.hotspotC).toFixed(1);
  banner.innerText = `Smart valley-filling & V2G shaving reduce transformer hot-spot temperature by ${tempReduction}°C and avoid ${avoidedCo2.toLocaleString()} kg of CO₂ emissions daily!`;
}

// Populate Telemetry Table
function renderFleetTable(filter = "") {
  const tbody = document.getElementById('fleet-tbody');
  const q = filter.toLowerCase();
  const filtered = FLEET_SAMPLES.filter(r => 
    r.model.toLowerCase().includes(q) || 
    r.user.toLowerCase().includes(q) ||
    r.evse.toLowerCase().includes(q)
  );

  tbody.innerHTML = filtered.map(row => `
    <tr>
      <td><strong>${row.id}</strong></td>
      <td>${row.model}</td>
      <td>${row.batt} kWh</td>
      <td>${row.user}</td>
      <td>${row.evse}</td>
      <td>${row.arr}</td>
      <td>${row.soc}</td>
      <td>${row.req}</td>
      <td><span style="color: #22D3EE; font-weight: 600;">${row.flex}</span></td>
      <td><span style="color: ${row.v2g === 'Yes' ? '#34D399' : '#94A3B8'}">${row.v2g}</span></td>
    </tr>
  `).join('');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  initCharts();
  renderFleetTable();
  updateSimulation();

  // Paradigm Buttons
  document.querySelectorAll('.paradigm-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.paradigm-btn').forEach(b => b.classList.remove('active'));
      const target = e.currentTarget;
      target.classList.add('active');
      currentScenario = target.dataset.scenario;
      updateSimulation();
    });
  });

  // Sliders
  const slPen = document.getElementById('slider-penetration');
  const slSolar = document.getElementById('slider-solar');
  const slBess = document.getElementById('slider-bess');
  const chkOverlay = document.getElementById('check-compare-all');

  slPen.addEventListener('input', (e) => {
    evPenetration = parseFloat(e.target.value) / 100.0;
    document.getElementById('val-penetration').innerText = `${e.target.value}%`;
    updateSimulation();
  });

  slSolar.addEventListener('input', (e) => {
    solarCapacityKw = parseFloat(e.target.value);
    document.getElementById('val-solar').innerText = `${e.target.value} kWp`;
    updateSimulation();
  });

  slBess.addEventListener('input', (e) => {
    bessCapacityKwh = parseFloat(e.target.value);
    document.getElementById('val-bess').innerText = `${Number(e.target.value).toLocaleString()} kWh`;
    updateSimulation();
  });

  chkOverlay.addEventListener('change', (e) => {
    overlayAll = e.target.checked;
    updateSimulation();
  });

  // Fleet Search
  document.getElementById('fleet-search').addEventListener('input', (e) => {
    renderFleetTable(e.target.value);
  });

  // Export CSV
  document.getElementById('btn-export-csv').addEventListener('click', () => {
    const profiles = computeProfiles(evPenetration, solarCapacityKw, bessCapacityKwh);
    let csv = "hour,baseline_mw,solar_pv_mw,uncontrolled_mw,tou_tariff_mw,smart_valley_mw,microgrid_v2g_mw\n";
    for (let h = 0; h < 24; h++) {
      csv += `${h},${profiles.pBase[h]},${profiles.pSolarMw[h].toFixed(3)},${profiles.uncontrolled[h].toFixed(3)},${profiles.tou[h].toFixed(3)},${profiles.smart[h].toFixed(3)},${profiles.microgrid[h].toFixed(3)}\n`;
    }
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `VoltGrid_Simulation_Pen${Math.round(evPenetration*100)}pct.csv`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Monte Carlo Stress Test Button
  document.getElementById('btn-run-stress').addEventListener('click', () => {
    const btn = document.getElementById('btn-run-stress');
    btn.innerHTML = `<span class="status-dot pulsing"></span> Simulating...`;
    btn.disabled = true;

    let count = 0;
    const interval = setInterval(() => {
      evPenetration = Math.min(1.0, 0.40 + Math.random() * 0.55);
      slPen.value = Math.round(evPenetration * 100);
      document.getElementById('val-penetration').innerText = `${slPen.value}%`;
      updateSimulation();
      count++;
      if (count > 6) {
        clearInterval(interval);
        btn.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
          </svg>
          Run Monte Carlo
        `;
        btn.disabled = false;
      }
    }, 200);
  });
});
