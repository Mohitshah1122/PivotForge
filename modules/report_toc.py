from reportlab.platypus import (
    Paragraph,
    Spacer,
    PageBreak
)


def build_toc_section(styles):

    heading = styles["Heading2"]
    body = styles["BodyText"]

    elements = []

    elements.append(PageBreak())

    elements.append(
        Paragraph(
            "Table of Contents",
            heading
        )
    )

    elements.append(Spacer(1, 20))

    contents = [

        "1. Executive Summary",

        "2. Asset Inventory",

        "3. Vulnerability Assessment",

        "4. Relationship Mapping",

        "5. Attack Path Summary",

        "6. Risk Assessment",

        "7. Security Recommendations"

    ]

    for item in contents:

        elements.append(
            Paragraph(item, body)
        )

        elements.append(
            Spacer(1, 8)
        )

    elements.append(
        Spacer(1, 20)
    )

    return elements