from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors

from modules.vulnerability_manager import get_all_vulnerabilities


def build_vulnerability_section(styles):

    heading = styles["Heading2"]

    elements = []

    elements.append(

        Paragraph(

            "Vulnerability Assessment",

            heading

        )

    )

    elements.append(

        Spacer(1,15)

    )

    data=[

        [

            "Asset",

            "CVE",

            "Severity",

            "Name"

        ]

    ]

    vulnerabilities=get_all_vulnerabilities()

    for vulnerability in vulnerabilities:

        data.append([

            vulnerability["asset_name"],

            vulnerability["cve_id"],

            vulnerability["severity"],

            vulnerability["vulnerability_name"]

        ])

    table=Table(data)

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

        Spacer(1,25)

    )

    return elements