# VoltGrid™ EV Charging Load Impact Simulator
## 2–3 Minute Working Model Video Demo Script & Presentation Guide

> **Total Duration:** 2 minutes 45 seconds  
> **Presenter Tone:** Professional, authoritative, engineering-focused  
> **Visual Assets:** Live UI Demo (`http://127.0.0.1:8899`), Charts, Degradation Matrix, Feeder Voltage Heatmap

---

### Segment 1: Introduction & Problem Context (0:00 – 0:35)
- **On-Screen Action:**
  - Screen opens on VoltGrid™ Dashboard (`dark-theme`) showing the Substation at 2.5 MVA nameplate rating.
  - Cursor highlights the red KPI warning card: **Peak Load: 4.46 MW (+87.7% Over Rating)**.
- **Voiceover Narration:**
  > *"Hello everyone. As electric vehicle adoption accelerates, unmanaged charging poses an existential threat to urban distribution grids. In this project, we built **VoltGrid™**, an advanced physics-based EV Charging Load Impact Simulator.  
  > In our baseline suburban test feeder—modeled after an IEEE 13-bus radial network with a 2.5 MVA substation transformer—introducing an uncoordinated 70% EV penetration causes peak demand to spike to nearly 4.5 Megawatts. That is an 87.7% overload directly during evening residential peak hours, driving transformer hot-spot temperatures past 189°C and accelerating insulation loss of life by over 74 times the normal rate."*

---

### Segment 2: Testing Paradigms & The TOU Rebound Trap (0:35 – 1:15)
- **On-Screen Action:**
  - Presenter clicks on **'B. Static TOU Tariff'** in the left sidebar.
  - The live chart dynamically shifts: the evening peak drops, but a massive spike shoots up at 23:00 (11:00 PM).
  - Hover over the 23:00 peak on the canvas chart to show `4.31 MW`.
- **Voiceover Narration:**
  > *"Many utilities attempt to solve this with static Time-of-Use tariffs. But watch what happens when we switch to Scenario B: Static TOU.  
  > While evening charging is deferred, automated vehicle charge timers synchronize at 11:00 PM when the off-peak rate begins. This creates a severe 'avalanche rebound peak' of 4.31 Megawatts right at midnight! The transformer hot-spot still surges to 176°C, proving that simple static pricing merely moves the bottleneck rather than solving it."*

---

### Segment 3: Smart Coordinated Valley-Filling & Sustainable Microgrid (1:15 – 1:55)
- **On-Screen Action:**
  - Click on **'C. Smart Valley Filling'**, showing the net load line flattening smoothly into the overnight valley.
  - Next, click on **'D. Sustainable Microgrid'**.
  - Adjust the **Carport & Rooftop Solar PV** slider to 800 kWp and **BESS Storage** to 1,200 kWh.
  - Point to the green KPI cards: Peak Load drops to **2.45 MW**, Hot-spot to **97°C** (well below the IEEE 110°C threshold).
- **Voiceover Narration:**
  > *"To provide a true sustainable solution, VoltGrid™ implements two advanced mitigation architectures:  
  > In Scenario C, algorithmic smart charging coordinates charging schedules based on each vehicle's flexibility index, smoothly filling the overnight demand valley.  
  > In Scenario D, we integrate a sustainable microgrid with 800 kW of solar PV, a 1.2 MWh battery storage system, and bidirectional Vehicle-to-Grid (V2G) power flow. Parked vehicles discharge up to 2.5 kW during peak evening hours, shaving the peak, and recharge from surplus clean daytime solar and wind. Transformer thermal stress drops by over 92°C, and daily grid carbon emissions are reduced by 3,660 kg of CO₂."*

---

### Segment 4: Radial Feeder Voltage & Asset Degradation Matrix (1:55 – 2:30)
- **On-Screen Action:**
  - Scroll down smoothly to show the **Radial Feeder Bus Voltage Profile (LinDistFlow)** and the **Asset Reliability & Degradation Matrix**.
  - Highlight the ANSI C84.1 safety threshold at `0.95 p.u.`.
  - Type `'Tesla'` into the EV Telemetry Table search box to show real-time query filtering.
- **Voiceover Narration:**
  > *"Scrolling down, VoltGrid™ solves LinDistFlow power equations across all 13 feeder buses in real time. Under uncontrolled charging, downstream bus voltages drop to brownout levels of 0.951 p.u. With our microgrid solution, bus voltages remain safely above 0.973 p.u.  
  > Our asset degradation matrix integrates the IEEE Std C57.91 thermal model, quantifying the cumulative aging factor and showing how our smart solution preserves the 20-year design life of multi-million-dollar substation assets. Below, the simulator provides live telemetry auditing of 3,500 charging sessions with physical battery capacity and charging flexibility ratios."*

---

### Segment 5: Conclusion & Future Outlook (2:30 – 2:45)
- **On-Screen Action:**
  - Click the **'Export Run CSV'** button to show instant data export.
  - Return to top view of the dashboard.
- **Voiceover Narration:**
  > *"VoltGrid™ demonstrates that the electric vehicle transition does not require costly grid overhauls if coupled with smart coordination, localized solar storage, and V2G flexibility. All code, datasets, and simulation models are fully reproducible. Thank you!"*

---

### Recording Checklist for Video Submission
1. **Screen Resolution:** 1080p (1920x1080) or 2K.
2. **Audio:** Clear microphone with noise cancellation.
3. **Pacing:** Follow the 2:45 timing breakdown above.
4. **Demonstration File:** The animated web recording is saved in `media/voltgrid_live_demo_recording.webp` and screenshots in `media/screenshots/`.
