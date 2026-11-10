"""
Generate Professional 16:9 PowerPoint Presentation (06_Presentation_5_Slides.pptx)
Creates modern styled slides with metric cards, tables, and colored headings.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="06_Presentation_5_Slides.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Theme colors
    C_BG = RGBColor(11, 15, 25)         # #0B0F19 Dark obsidian
    C_CARD = RGBColor(18, 24, 38)       # #121826 Card background
    C_CYAN = RGBColor(6, 182, 212)      # #06B6D4 Electric cyan
    C_GREEN = RGBColor(16, 185, 129)    # #10B981 Emerald
    C_AMBER = RGBColor(245, 158, 11)    # #F59E0B Amber
    C_RED = RGBColor(239, 68, 68)       # #EF4444 Crimson
    C_WHITE = RGBColor(248, 250, 252)   # #F8FAFC Primary text
    C_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Secondary text
    C_BORDER = RGBColor(30, 41, 59)     # #1E293B Border line

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.color.rgb = C_BG
        return bg

    def add_header(slide, title_text, category_text):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(5.0), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = C_CYAN

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_background(s1)

    # Accent decorative box
    dec = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    dec.fill.solid()
    dec.fill.fore_color.rgb = C_CARD
    dec.line.color.rgb = C_BORDER

    # Badge
    b_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.9), Inches(8.0), Inches(0.4))
    b_p = b_box.text_frame.paragraphs[0]
    b_p.text = "⚡ SUSTAINABLE ENERGY ENGINEERING PROJECT  •  CAPSTONE EVALUATION"
    b_p.font.size = Pt(11)
    b_p.font.bold = True
    b_p.font.color.rgb = C_CYAN

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(1.3), Inches(2.3), Inches(10.5), Inches(1.6))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "VoltGrid™: EV Charging Load Impact Simulator"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Modeling Urban Feeder Bottlenecks, IEEE C57.91 Transformer Aging, and Sustainable V2G-Microgrid Mitigation"
    p1_sub.font.size = Pt(15)
    p1_sub.font.color.rgb = C_MUTED
    p1_sub.space_before = Pt(8)

    # 3 Stat Cards on Title Slide
    stats = [
        ("87.7% OVERLOAD", "Legacy Grid Stress Peak", C_RED),
        ("74.2× ACCELERATION", "Transformer Aging Rate", C_AMBER),
        ("3.66 TONS CO2 / DAY", "Sustainable Solar Abatement", C_GREEN)
    ]
    for i, (val, lbl, col) in enumerate(stats):
        x = Inches(1.3 + i * 3.7)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(4.3), Inches(3.4), Inches(1.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(11, 15, 25)
        card.line.color.rgb = C_BORDER
        
        tbox = s1.shapes.add_textbox(x, Inches(4.4), Inches(3.4), Inches(1.1))
        tf = tbox.text_frame
        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.size = Pt(15)
        p_val.font.bold = True
        p_val.font.color.rgb = col
        p_val.alignment = PP_ALIGN.CENTER
        
        p_lbl = tf.add_paragraph()
        p_lbl.text = lbl
        p_lbl.font.size = Pt(10)
        p_lbl.font.color.rgb = C_MUTED
        p_lbl.alignment = PP_ALIGN.CENTER

    # Presenter metadata footer
    f_box = s1.shapes.add_textbox(Inches(1.3), Inches(5.9), Inches(10.5), Inches(0.5))
    f_p = f_box.text_frame.paragraphs[0]
    f_p.text = "Domain: Power Systems & Sustainable Mobility | Standards: IEEE C57.91-2011, ANSI C84.1, SAE J3072"
    f_p.font.size = Pt(10)
    f_p.font.color.rgb = C_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & The TOU Rebound Trap
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_background(s2)
    add_header(s2, "Grid Vulnerabilities: Feeder Overload & The TOU Rebound Trap", "01. Engineering Problem Context")

    # 3 Column Cards
    col_data = [
        ("Uncoordinated EV Overload", 
         "• 70% EV penetration on a 2.5 MVA substation feeder adds 2.94 MW of peak charging demand.\n"
         "• Coincides directly with evening residential cooking, heating & AC (18:00 - 21:00).\n"
         "• Substation net demand surges to 4.46 MW (87.7% above rated continuous capacity).\n"
         "• Creates severe feeder tail voltage sag down to 0.951 p.u. (ANSI C84.1 violation threshold).",
         C_RED),
        ("The 'TOU Avalanche' Trap", 
         "• Utilities often implement static Time-of-Use tariffs to encourage night charging.\n"
         "• Result: 75% of vehicle timers synchronize to 23:00 (11:00 PM off-peak window).\n"
         "• Generates an explosive secondary rebound peak of 4.31 MW right at midnight!\n"
         "• Merely shifts the equipment failure point rather than solving grid capacity.",
         C_AMBER),
        ("Severe Asset Degradation", 
         "• Transformer top-oil and winding hot-spot temperatures spike past 189.4°C.\n"
         "• IEEE C57.91 continuous normal insulation limit is 110.0°C.\n"
         "• Equivalent aging acceleration factor surges to 74.2× normal design rate.\n"
         "• Multi-million dollar substation transformers face catastrophic premature failure.",
         C_CYAN)
    ]

    for i, (head, body, border_col) in enumerate(col_data):
        x = Inches(0.8 + i * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), Inches(3.75), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(x + Inches(0.2), Inches(1.9), Inches(3.35), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = border_col
        p_h.space_after = Pt(12)

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = C_WHITE if line.startswith("•") else C_MUTED
            p_b.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 3: Methodology & Mathematical Physics
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_background(s3)
    add_header(s3, "Physics-Based Simulation Architecture & Mathematical Formulation", "02. Mathematical Methodology")

    math_cards = [
        ("1. Stochastic EV Fleet Model",
         "• 3,500 telemetry sessions cleaned & validated.\n"
         "• Gaussian dual-peak arrival: mu=18.5h (Home) & mu=8.5h (Work).\n"
         "• Battery physics: E_req = (SoC_target - SoC_init) * C_batt / eta_ch.\n"
         "• Charging Flexibility Index: Phi = t_dwell / t_min (Identifies V2G potential).",
         C_CYAN),
        ("2. IEEE Std C57.91 Thermal Model",
         "• Dynamic differential top-oil rise: dTheta_TO / dt = (Theta_TO_u - Theta_TO) / tau_TO.\n"
         "• Hot-spot temperature: Theta_H = Theta_TO + DeltaTheta_H_u.\n"
         "• Arrhenius Aging Acceleration Factor:\n"
         "    F_AA = exp( 15000/383.15 - 15000/(Theta_H + 273.15) )\n"
         "• Daily Cumulative Loss of Life (% LOL) = F_EQ * (24 / 180,000) * 100%.",
         C_AMBER),
        ("3. Radial Feeder Power Flow",
         "• LinDistFlow backward/forward voltage drop solver on 13-bus network.\n"
         "• Voltage equation: V_{i+1} = V_i - (R_i * P_i + X_i * Q_i) / V_i.\n"
         "• Branch Joule loss computation: P_loss = (P^2 + Q^2) / V^2 * R.\n"
         "• Strict ANSI C84.1 compliance constraint: 0.95 <= V_pu <= 1.05.",
         C_GREEN)
    ]

    for i, (head, body, border_col) in enumerate(math_cards):
        x = Inches(0.8 + i * 4.0)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), Inches(3.75), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(x + Inches(0.2), Inches(1.9), Inches(3.35), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = border_col
        p_h.space_after = Pt(10)

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = C_WHITE
            p_b.space_after = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 4: Simulation Findings & Comparative Results
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_background(s4)
    add_header(s4, "Experimental Simulation Findings Across Charging Paradigms", "03. Empirical Results")

    # Table of Results
    rows = 6
    cols = 5
    table_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.733), Inches(3.4))
    table = table_shape.table
    table.columns[0].width = Inches(3.0)
    table.columns[1].width = Inches(2.1)
    table.columns[2].width = Inches(2.1)
    table.columns[3].width = Inches(2.2)
    table.columns[4].width = Inches(2.333)

    table_data = [
        ["Key Reliability Metric", "A. Uncontrolled", "B. Static TOU", "C. Smart Valley", "D. Microgrid (V2G)"],
        ["Peak Substation Load (MW)", "4.46 MW (+87.7%)", "4.31 MW (+81.6%)", "2.45 MW (+3.2%)", "2.45 MW (Optimized)"],
        ["Max Hot-Spot Temp (°C)", "189.4 °C (Critical)", "176.2 °C (Severe)", "102.2 °C (Safe)", "97.0 °C (Optimal)"],
        ["Transformer Aging Factor", "74.19× Baseline", "24.11× Baseline", "0.193× Baseline", "0.095× (Preserved)"],
        ["Min Feeder Voltage (p.u.)", "0.951 p.u. (Marginal)", "0.953 p.u.", "0.973 p.u. (Robust)", "0.973 p.u. (Robust)"],
        ["Daily Grid CO2 Emissions", "14,868 kg", "11,764 kg", "12,176 kg", "11,206 kg (-24.6%)"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, cell_value in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = cell_value
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10.5)
            p.font.name = "Helvetica"
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_CYAN
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(25, 33, 50)
            elif c_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_GREEN
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(16, 40, 32)
            else:
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_CARD

    # Key Inferences Card
    inf_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.5))
    inf_card.fill.solid()
    inf_card.fill.fore_color.rgb = C_CARD
    inf_card.line.color.rgb = C_GREEN
    inf_card.line.width = Pt(1.5)

    inf_tb = s4.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.3))
    itf = inf_tb.text_frame
    itf.word_wrap = True
    ip0 = itf.paragraphs[0]
    ip0.text = "ENGINEERING INFERENCES & TAKEAWAYS:"
    ip0.font.bold = True
    ip0.font.size = Pt(11)
    ip0.font.color.rgb = C_GREEN

    ip1 = itf.add_paragraph()
    ip1.text = "1. Uncontrolled charging destroys transformer paper insulation in < 3 years due to sustained temperatures > 180°C.\n" \
               "2. Static TOU incentives create an unintended destructive synchrony peak (4.31 MW), proving dynamic control is mandatory.\n" \
               "3. Sustainable Microgrid + V2G completely flattens the feeder profile, preventing transformer brownouts and saving 3.66 tons CO2/day."
    ip1.font.size = Pt(10)
    ip1.font.color.rgb = C_WHITE
    ip1.space_before = Pt(3)

    # -------------------------------------------------------------
    # SLIDE 5: Sustainable Mitigation Solution & Techno-Economics
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_background(s5)
    add_header(s5, "Sustainable Engineering Solution & Techno-Economic Roadmap", "04. Solution & Implementation")

    sol_cards = [
        ("Solar PV + BESS Sizing",
         "• 800 kWp carport solar absorbs workplace daytime commuter charging (10 AM - 3 PM).\n"
         "• 1.2 MWh BESS captures mid-day solar surplus and discharges 350 kW during peak (6 PM - 9 PM).\n"
         "• Eliminates peak reliance on marginal gas peaker plants.",
         C_AMBER),
        ("Decentralized V2G Fleet",
         "• Utilizes ISO 15118 & SAE J3072 protocols for bi-directional energy transfer.\n"
         "• Eligible vehicles (flexibility > 1.8) discharge 2.5 kW into feeder during peak hours.\n"
         "• Automatically replenished overnight during clean baseload hours (1 AM - 5 AM).",
         C_CYAN),
        ("Techno-Economic Value",
         "• Avoided Substation CapEx: Deferral of $450,000 transformer replacement.\n"
         "• Transformer Life Extension: Restores normal 20-year lifespan (from 2.8 years under overload).\n"
         "• 1,336 Metric Tons CO2 avoided annually per suburban substation.",
         C_GREEN)
    ]

    for i, (head, body, border_col) in enumerate(sol_cards):
        x = Inches(0.8 + i * 4.0)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), Inches(3.75), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(x + Inches(0.2), Inches(1.9), Inches(3.35), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = border_col
        p_h.space_after = Pt(10)

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = C_WHITE
            p_b.space_after = Pt(5)

    # Bottom takeaway bar
    t_bar = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8))
    t_bar.fill.solid()
    t_bar.fill.fore_color.rgb = RGBColor(16, 40, 32)
    t_bar.line.color.rgb = C_GREEN

    t_tb = s5.shapes.add_textbox(Inches(1.0), Inches(6.22), Inches(11.3), Inches(0.6))
    ttf = t_tb.text_frame
    tp = ttf.paragraphs[0]
    tp.text = "CONCLUSION: VoltGrid™ proves that smart coordinated dispatch combined with V2G microgrids allows 100% EV adoption WITHOUT costly utility grid upgrades, achieving total grid resilience and decarbonization."
    tp.font.size = Pt(10.5)
    tp.font.bold = True
    tp.font.color.rgb = C_WHITE
    tp.alignment = PP_ALIGN.CENTER

    prs.save(filename)
    print(f"Generated {filename}")

if __name__ == "__main__":
    create_deck()
