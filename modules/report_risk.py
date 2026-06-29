from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors

from modules.asset_manager import get_all_assets
from modules.vulnerability_manager import get_all_vulnerabilities
from modules.relationship_manager import get_all_relationships


def build_risk_section(styles):

    heading = styles["Heading2"]

    body = styles["BodyText"]

    elements = []

    elements.append(PageBreak())

    elements.append(

        Paragraph(

            "Risk Assessment",

            heading

        )

    )

    elements.append(

        Spacer(1,15)

    )

    assets = len(get_all_assets())

    vulnerabilities = len(get_all_vulnerabilities())

    relationships = len(get_all_relationships())

    risk_score = (

        vulnerabilities * 10

        +

        relationships * 2

        +

        assets

    )

    if risk_score >= 80:

        level = "CRITICAL"

    elif risk_score >= 50:

        level = "HIGH"

    elif risk_score >= 25:

        level = "MEDIUM"

    else:

        level = "LOW"

    data = [

        [

            "Metric",

            "Value"

        ],

        [

            "Risk Score",

            str(risk_score)

        ],

        [

            "Risk Level",

            level

        ],

        [

            "Assets",

            str(assets)

        ],

        [

            "Vulnerabilities",

            str(vulnerabilities)

        ],

        [

            "Relationships",

            str(relationships)

        ]

    ]

    table = Table(

        data,

        colWidths=[220,220]

    )

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkred),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

    ]))

    elements.append(table)

    elements.append(

        Spacer(1,20)

    )

    elements.append(

        Paragraph(

            "The calculated score represents the estimated overall exposure of the enterprise environment based on the current asset inventory, vulnerability count, and trust relationships.",

            body

        )

    )

    return elements