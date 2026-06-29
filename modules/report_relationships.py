from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors

from modules.relationship_manager import get_all_relationships


def build_relationship_section(styles):

    heading = styles["Heading2"]

    elements = []

    elements.append(

        Paragraph(

            "Relationship Mapping",

            heading

        )

    )

    elements.append(

        Spacer(1,15)

    )

    data=[

        [

            "Source Asset",

            "Destination Asset",

            "Relationship"

        ]

    ]

    relationships=get_all_relationships()

    for relationship in relationships:

        data.append([

            relationship["source_name"],

            relationship["destination_name"],

            relationship["relationship_type"]

        ])

    table=Table(

        data,

        colWidths=[170,170,140]

    )

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),8)

    ]))

    elements.append(table)

    elements.append(

        Spacer(1,25)

    )

    return elements