"""
Generate Professional PDF for 01_Problem_Statement.pdf using ReportLab.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf(filename="01_Problem_Statement.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0284C7'),
        spaceAfter=8
    )

    sec_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=2
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("PROBLEM STATEMENT: EV CHARGING LOAD IMPACT SIMULATOR", title_style))
    elements.append(Paragraph("Project: Impact Modeling, Thermal Degradation Analysis, and Microgrid Mitigation for High-Penetration EV Charging | Standards: IEEE C57.91, ANSI C84.1", meta_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=6))

    # Section 1
    elements.append(Paragraph("1. Problem Context & Infrastructure Vulnerability", sec_heading))
    p1 = ("The global transition toward electrified mobility is accelerating exponentially. However, contemporary urban and suburban "
          "medium-to-low voltage (MV/LV) distribution grids were architected decades ago under assumptions of passive, unidirectional "
          "power flows with predictable coincident diversity factors. Uncoordinated electric vehicle (EV) charging—characterized by simultaneous "
          "high-power Level 2 (7.2–19.2 kW) and DC Fast Charging (50–150 kW) connections upon evening residential arrival (17:00–21:00)—imposes "
          "severe, non-coincident peak demands directly on top of legacy residential peak hours.<br/>"
          "On a representative 2.5 MVA / 12.47 kV distribution substation feeder, a 70% EV penetration escalates peak demand from 1.52 MW to "
          "<b>4.46 MW (an 87.7% overload)</b>. This unmanaged load induces severe feeder voltage sag down to <b>0.951 p.u.</b> (violating ANSI C84.1 limits), "
          "and according to <b>IEEE Std C57.91-2011</b>, drives transformer winding hot-spot temperatures to <b>189.4°C</b>. This triggers an Aging "
          "Acceleration Factor (F_AA) of <b>74.2× normal</b>, destroying transformer insulation life within weeks. Furthermore, static Time-of-Use (TOU) "
          "tariffs fail by inducing synchronized charging timers at off-peak onset (23:00), generating an avalanche rebound peak of <b>4.31 MW</b>.")
    elements.append(Paragraph(p1, body_style))

    # Section 2
    elements.append(Paragraph("2. Project Objectives & Engineering Scope", sec_heading))
    b1 = "• <b>Stochastic Fleet Characterization:</b> Model 3,500+ empirical EV sessions capturing arrival times, dwell durations, battery sizes (40–98 kWh), and flexibility indices (Phi = t_dwell / t_min)."
    b2 = "• <b>Coupled Power Flow & Thermal Aging Engine:</b> Formulate 13-bus radial LinDistFlow voltage solver and dynamic top-oil/hot-spot differential heat transfer equations (IEEE Std C57.91)."
    b3 = "• <b>Sustainable Microgrid & V2G Optimization:</b> Develop coordinated smart valley-filling, integrated with an 800 kWp solar PV array, a 1.2 MWh BESS, and bidirectional Vehicle-to-Grid (V2G) peak shaving."
    b4 = "• <b>Interactive Decision-Support Platform:</b> Deliver a full-stack real-time simulator to stress-test grid penetration scenarios and quantify asset degradation and carbon abatement."
    for b in [b1, b2, b3, b4]:
        elements.append(Paragraph(b, bullet_style))

    # Section 3
    elements.append(Paragraph("3. Quantitative Engineering Benchmarks & Mitigation Target Matrix", sec_heading))
    
    # Table data
    table_data = [
        [Paragraph("<b>Performance Metric</b>", body_style),
         Paragraph("<b>Uncontrolled Legacy</b>", body_style),
         Paragraph("<b>Static TOU Rebound</b>", body_style),
         Paragraph("<b>VoltGrid™ Microgrid</b>", body_style),
         Paragraph("<b>Engineering Standard</b>", body_style)],
        [Paragraph("Peak Feeder Demand", body_style), "4.46 MW (+87.7%)", "4.31 MW (+81.6%)", "<b>2.45 MW (+3.2%)</b>", "< 2.50 MW (Rated)"],
        [Paragraph("Max Hot-Spot Temp", body_style), "189.4 °C", "176.2 °C", "<b>97.0 °C</b>", "< 110.0 °C (IEEE C57.91)"],
        [Paragraph("Aging Factor (F_EQ)", body_style), "74.19×", "24.11×", "<b>0.095× (Preserved)</b>", "<= 1.0× (Design Base)"],
        [Paragraph("Min Bus Voltage", body_style), "0.951 p.u.", "0.953 p.u.", "<b>0.973 p.u.</b>", ">= 0.950 p.u. (ANSI C84.1)"],
        [Paragraph("Daily CO2 Emissions", body_style), "14,868 kg", "11,764 kg", "<b>11,206 kg (-24.6%)</b>", "Max Solar Self-Supply"]
    ]

    t = Table(table_data, colWidths=[120, 100, 100, 115, 95])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (3,1), (3,-1), colors.HexColor('#ECFDF5')), # highlight green for solution
    ]))
    elements.append(t)

    doc.build(elements)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_pdf()
