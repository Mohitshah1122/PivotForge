from datetime import datetime
from reportlab.platypus import Image
from modules.report_charts import ReportCharts
from modules.report_toc import build_toc_section
from modules.report_layout import draw_header_footer
from modules.report_recommendations import build_recommendation_section
from modules.report_risk import build_risk_section
from modules.report_attack_paths import build_attack_path_section
from modules.report_relationships import build_relationship_section
from modules.report_assets import build_asset_section
from modules.report_vulnerabilities import build_vulnerability_section
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from config.report_config import *

from modules.asset_manager import get_all_assets
from modules.graph_engine import GraphEngine
from modules.relationship_manager import get_all_relationships
from modules.vulnerability_manager import get_all_vulnerabilities


class ReportGenerator:

    def __init__(self):
        self.graph = GraphEngine()

    def generate(self):

        self.graph.build_graph()
        

        charts = ReportCharts()

        vulnerability_chart = charts.generate_vulnerability_chart()

        asset_chart = charts.generate_asset_chart()
        
        filename = "reports/PivotForge_Report.pdf"

        doc = SimpleDocTemplate(
    filename,
    rightMargin=30,
    leftMargin=30,
    topMargin=90,
    bottomMargin=50
)
        # ------------------------
        # PDF Metadata
        # ------------------------

        doc.title = REPORT_TITLE
        doc.author = AUTHOR
        doc.subject = SUBJECT
        doc.creator = CREATOR
        doc.producer = PRODUCER

        styles = getSampleStyleSheet()

        title = styles["Title"]
        title.alignment = TA_CENTER

        heading = styles["Heading2"]

        body = styles["BodyText"]

        elements = []

        # ======================================================
        # COVER PAGE
        # ======================================================

        elements.append(
            Paragraph(PROJECT_NAME, title)
        )

        elements.append(Spacer(1, 15))

        elements.append(
            Paragraph(PROJECT_TAGLINE, heading)
        )

        elements.append(Spacer(1, 25))

        elements.append(
            Paragraph(REPORT_TITLE, styles["Heading1"])
        )

        elements.append(Spacer(1, 30))

        elements.append(
            Paragraph(
                f"<b>Organization :</b> {COMPANY_NAME}",
                body
            )
        )

        elements.append(
            Paragraph(
                f"<b>Analyst :</b> {ANALYST_NAME}",
                body
            )
        )

        elements.append(
            Paragraph(
                f"<b>Version :</b> {REPORT_VERSION}",
                body
            )
        )

        elements.append(
            Paragraph(
                f"<b>Security Classification :</b> {SECURITY_CLASSIFICATION}",
                body
            )
        )

        elements.append(
            Paragraph(
                f"<b>Generated :</b> {datetime.now().strftime('%d %B %Y %H:%M')}",
                body
            )
        )

        elements.append(Spacer(1, 40))

        

        elements.extend(
    build_toc_section(styles)
)
        elements.append(PageBreak())
        

        # ======================================================
        # EXECUTIVE SUMMARY
        # ======================================================

        elements.append(
            Paragraph(
                "Executive Summary",
                heading
            )
        )

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph(
                "PivotForge analyzed the enterprise environment and generated the following security statistics.",
                body
            )
        )

        elements.append(Spacer(1, 20))

        total_assets = len(get_all_assets())

        total_vulnerabilities = len(get_all_vulnerabilities())

        total_relationships = len(get_all_relationships())

        total_nodes = self.graph.total_nodes()

        total_edges = self.graph.total_edges()

        dashboard = [

            ["Security Metric", "Value"],

            ["Total Assets", total_assets],

            ["Total Vulnerabilities", total_vulnerabilities],

            ["Trust Relationships", total_relationships],

            ["Attack Graph Nodes", total_nodes],

            ["Attack Graph Edges", total_edges]

        ]

        table = Table(
            dashboard,
            colWidths=[280, 120]
        )

        table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8)

        ]))

        elements.append(table)

        elements.append(Spacer(1, 30))

        # =====================================
        # Vulnerability Chart
        # =====================================

        elements.append(

    Paragraph(

        "Vulnerability Severity Distribution",

        heading

    )

)

        elements.append(

    Spacer(1,10)

)

        elements.append(

    Image(

        vulnerability_chart,

        width=420,

        height=240

    )

)

        elements.append(

    Spacer(1,25)

)

# =====================================
# Asset Type Chart
# =====================================

        elements.append(PageBreak())
        elements.append(

    Paragraph(

        "Asset Type Distribution",

        heading

    )

)

        elements.append(

    Spacer(1,10)

)

        elements.append(

    Image(

        asset_chart,

        width=360,

        height=270

    )

)

        elements.append(

    Spacer(1,20)

)

        elements.append(

    Paragraph(

        "Vulnerability Severity Distribution",

        heading

    )

)

        elements.append(

    Spacer(1,15)

)

        elements.append(

    Image(

        vulnerability_chart,

        width=420,

        height=240

    )

)

        elements.append(

    Spacer(1,20)

)

        # ======================================================
        # SECURITY OVERVIEW
        # ======================================================

        elements.append(
            Paragraph(
                "Security Overview",
                heading
            )
        )

        elements.append(Spacer(1, 10))

        if total_vulnerabilities >= 5:

            risk = "HIGH"

        elif total_vulnerabilities >= 2:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        elements.append(

            Paragraph(

                f"<b>Overall Risk Level :</b> {risk}",

                body

            )

        )

        elements.append(Spacer(1, 10))

        elements.append(

            Paragraph(

                "This report identifies enterprise assets, vulnerabilities and trust relationships that could allow attackers to move laterally inside the environment.",

                body

            )

        )

        elements.append(Spacer(1, 25))
      
        elements.append(PageBreak())

        elements.extend(

    build_asset_section(styles)

)
        elements.append(PageBreak())
        elements.extend(

    build_vulnerability_section(styles)

)
        elements.append(PageBreak())
        elements.extend(

    build_relationship_section(styles)

)   
        elements.append(PageBreak())
        elements.extend(

    build_attack_path_section(

        styles,

        self.graph

    )

) 
        
        elements.extend(

    build_risk_section(

        styles

    )

)
        elements.extend(

    build_recommendation_section(

        styles

    )

)
        elements.append(

            Paragraph(

                COPYRIGHT,

                body

            )

        )

        

        doc.build(

    elements,

    onFirstPage=draw_header_footer,

    onLaterPages=draw_header_footer

)

        return filename