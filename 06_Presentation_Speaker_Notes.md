# VoltGrid™: 5-Slide Presentation Speaker Notes & Delivery Script

## Slide 1: Title & Overview (0:00 – 0:45)
- **Title:** VoltGrid™: EV Charging Load Impact Simulator
- **Subtitle:** Modeling Urban Feeder Overloads, IEEE C57.91 Transformer Degradation, and Sustainable V2G-Microgrid Mitigation
- **Presenter Cues:**
  - *"Good morning/afternoon, professors and committee members. Today, I am proud to present our Sustainable Energy Engineering project: **VoltGrid™**."*
  - *"As our transportation sector electrifies, the primary barrier is no longer battery range or vehicle manufacturing—it is the local electric distribution grid."*
  - *"Our project asks a fundamental question: What happens to a standard 2.5 MVA neighborhood substation when 70% of households adopt electric vehicles? And more importantly: Can we solve this challenge sustainably using smart coordination and microgrids without spending millions on transformer upgrades?"*
  - *"In this 5-slide briefing, we present our physics-based findings, mathematical models, empirical telemetry datasets, and real-time interactive decision support platform."*

---

## Slide 2: Problem Formulation & The "TOU Rebound Trap" (0:45 – 1:30)
- **Title:** Grid Stress Points & The TOU Rebound Paradox
- **Presenter Cues:**
  - *"Let's look at Slide 2, where we outline the core engineering vulnerability."*
  - *"Under uncontrolled charging—where drivers simply arrive home from work between 5:00 PM and 9:00 PM and plug in their 7.2 kW or 11 kW Level 2 chargers—their charging demand adds 2.94 Megawatts directly on top of the existing domestic dinner, AC, and appliance peak."*
  - *"This pushes total feeder load to 4.46 MW, representing an 87.7% overload on our 2.38 MW continuous rated transformer."*
  - *"Now, the conventional utility answer has been: 'Let's offer a Time-of-Use tariff with cheap electricity starting at 11:00 PM.' But as shown in the middle card, this triggers a dangerous phenomenon known as the 'TOU Avalanche Rebound Peak'."*
  - *"Modern EVs have built-in timers. When thousands of vehicles detect the 11:00 PM off-peak signal, they all start charging simultaneously. The result? A massive 4.31 MW rebound spike right at midnight. Static pricing merely shifts the bottleneck in time without protecting the grid."*
  - *"Under both uncontrolled and TOU regimes, the transformer hot-spot surges past 176°C, causing an insulation aging acceleration factor of over 74 times normal. A 20-year transformer would fail in under three years."*

---

## Slide 3: Engineering Methodology & Mathematical Formulation (1:30 – 2:15)
- **Title:** Physics-Based Simulation Architecture & Mathematical Formulation
- **Presenter Cues:**
  - *"Slide 3 details our rigorous scientific methodology, spanning three mathematical domains."*
  - *"First, we generated and cleaned an empirical dataset of 3,500 real-world EV charging sessions covering Tesla Model 3s and Ys, Ford F-150 Lightnings, Hyundai Ioniqs, delivery vans, and fleet vehicles. We introduced a new metric called the **Charging Flexibility Index ($\Phi = t_{dwell} / t_{min}$)**, which identifies vehicles with surplus dwell time suitable for load shifting."*
  - *"Second, we implemented the official **IEEE Std C57.91-2011 thermal differential model**. We model top-oil and winding hot-spot temperature rises dynamically, then compute the Arrhenius Aging Acceleration Factor ($F_{AA}$) to quantify cumulative loss of life."*
  - *"Third, we solved the **LinDistFlow radial power flow equations** across an IEEE 13-bus distribution feeder to evaluate voltage sags and line losses at every hour."*

---

## Slide 4: Simulation Findings & Comparative Results (2:15 – 3:00)
- **Title:** Comparative Quantitative Findings Across Charging Paradigms
- **Presenter Cues:**
  - *"Moving to Slide 4, here is our quantitative comparison across the four charging regimes."*
  - *"Notice the stark differences: In Uncontrolled Charging (Column 1), peak demand is 4.46 MW and the hot-spot hits 189.4°C. In Static TOU (Column 2), the rebound peak hits 4.31 MW and 176.2°C."*
  - *"However, look at Column 3 (Smart Valley Filling) and Column 4 (Our Sustainable Microgrid with V2G):"*
    - *"Peak demand is capped at 2.45 MW—comfortably within the transformer's operational envelope."*
    - *"Hot-spot temperatures drop to 97°C—well below the IEEE 110°C continuous limit."*
    - *"The aging multiplier plummets from 74× down to 0.095×, fully preserving the asset's design life."*
    - *"Feeder bus voltage remains at 0.973 p.u., completely eliminating the threat of brownouts."*
    - *"And in our microgrid scenario, daily operational carbon emissions drop by over 3,660 kg of CO₂ per day!"*

---

## Slide 5: The Sustainable Mitigation Solution & Techno-Economic Impact (3:00 – 3:45)
- **Title:** The Sustainable Engineering Solution & Techno-Economic Roadmap
- **Presenter Cues:**
  - *"Finally, on Slide 5, we present our complete sustainable solution architecture and techno-economic business case."*
  - *"Our tri-pillar design integrates:*
    1. *An 800 kWp solar carport array that directly powers daytime workplace charging.*
    2. *A 1.2 MWh Battery Energy Storage System (BESS) that stores mid-day solar excess and discharges 350 kW during evening peak.*
    3. *A decentralized Vehicle-to-Grid (V2G) coordination scheme leveraging ISO 15118 and SAE J3072 standards, where participating parked EVs inject up to 2.5 kW into the feeder during critical peak hours and recharge overnight from clean wind baseload.*
  - *"Techno-economically, this avoids a $450,000 substation transformer replacement, extends asset life by 17 years, and eliminates 1,336 tons of CO₂ per substation annually."*
  - *"We also packaged this entire engine into a real-time web simulator, VoltGrid™, with live interactive sliders and Monte Carlo stress testing."*
  - *"Thank you for your time. I welcome any questions from the panel!"*
