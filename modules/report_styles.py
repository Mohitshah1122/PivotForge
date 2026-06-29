from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def get_report_styles():

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER
    title.textColor = colors.darkred

    heading = styles["Heading2"]
    heading.textColor = colors.darkblue

    body = styles["BodyText"]

    return {

        "title": title,

        "heading": heading,

        "body": body

    }


def dashboard_style():

    return [

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER")

    ]