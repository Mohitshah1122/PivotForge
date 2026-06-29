from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors

from modules.asset_manager import get_all_assets


def build_asset_section(styles):

    heading = styles["Heading2"]

    body = styles["BodyText"]

    elements = []

    elements.append(

        Paragraph(

            "Asset Inventory",

            heading

        )

    )

    elements.append(

        Spacer(1,15)

    )

    data=[

        [

            "Asset",

            "IP",

            "Type",

            "Criticality"

        ]

    ]

    assets=get_all_assets()

    for asset in assets:

        data.append([

            asset["asset_name"],

            asset["ip_address"],

            asset["asset_type"],

            asset["criticality"]

        ])

    table=Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

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