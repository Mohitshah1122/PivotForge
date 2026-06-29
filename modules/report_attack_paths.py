from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib import colors


def build_attack_path_section(styles, graph):

    heading = styles["Heading2"]

    body = styles["BodyText"]

    elements = []

    elements.append(

        Paragraph(

            "Attack Path Summary",

            heading

        )

    )

    elements.append(

        Spacer(1,15)

    )

    nodes = graph.node_list()

    edges = graph.edge_list()

    if len(nodes) >= 2:

        source = nodes[0]

        destination = nodes[-1]

    else:

        source = "N/A"

        destination = "N/A"

    data = [

        ["Metric", "Value"],

        ["Entry Point", source],

        ["Target Asset", destination],

        ["Assets in Graph", str(len(nodes))],

        ["Relationships", str(len(edges))],

        ["Estimated Attack Complexity", "Medium"]

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

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER")

    ]))

    elements.append(table)

    elements.append(

        Spacer(1,15)

    )

    elements.append(

        Paragraph(

            "This summary provides a high-level overview of the current attack graph. Future versions of PivotForge will calculate optimal attack paths, shortest paths, privilege escalation routes, and risk scores using graph algorithms.",

            body

        )

    )

    elements.append(

        Spacer(1,25)

    )

    return elements