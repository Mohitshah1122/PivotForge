from config.report_config import PROJECT_NAME
from config.report_config import REPORT_TITLE
from config.report_config import COPYRIGHT
from config.report_config import SECURITY_CLASSIFICATION

from datetime import datetime


from datetime import datetime
from config.report_config import *


def draw_header_footer(canvas, doc):

    canvas.saveState()

    width, height = doc.pagesize

    # -----------------------------
    # Header
    # -----------------------------

    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(40, height - 35, PROJECT_NAME)

    canvas.setFont("Helvetica", 10)
    canvas.drawString(40, height - 50, REPORT_TITLE)

    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawRightString(width - 40, height - 35, SECURITY_CLASSIFICATION)

    canvas.drawRightString(width - 40, height - 50, f"Page {canvas.getPageNumber()}")

    canvas.line(
        35,
        height - 60,
        width - 35,
        height - 60
    )

    # -----------------------------
    # Footer
    # -----------------------------

    canvas.line(
        35,
        40,
        width - 35,
        40
    )

    canvas.setFont("Helvetica", 9)

    canvas.drawString(
        40,
        25,
        COPYRIGHT
    )

    canvas.drawRightString(
        width - 40,
        25,
        datetime.now().strftime("%d-%m-%Y")
    )

    canvas.restoreState()