from reportlab.platypus import (
    Paragraph,
    Spacer,
    PageBreak
)

from modules.vulnerability_manager import get_all_vulnerabilities


def build_recommendation_section(styles):

    heading = styles["Heading2"]

    body = styles["BodyText"]

    elements = []

    elements.append(PageBreak())

    elements.append(

        Paragraph(

            "Security Recommendations",

            heading

        )

    )

    elements.append(

        Spacer(1,15)

    )

    vulnerabilities = get_all_vulnerabilities()

    critical = 0

    high = 0

    medium = 0

    low = 0

    for vulnerability in vulnerabilities:

        severity = vulnerability["severity"].lower()

        if severity == "critical":

            critical += 1

        elif severity == "high":

            high += 1

        elif severity == "medium":

            medium += 1

        else:

            low += 1

    recommendations = []

    if critical > 0:

        recommendations.append(

            "• Immediately patch all Critical vulnerabilities."

        )

    if high > 0:

        recommendations.append(

            "• Review High severity vulnerabilities within 7 days."

        )

    if medium > 0:

        recommendations.append(

            "• Schedule remediation for Medium vulnerabilities."

        )

    recommendations.extend([

        "• Enable Multi-Factor Authentication (MFA) for privileged accounts.",

        "• Segment critical servers using VLANs or firewalls.",

        "• Restrict administrative access using least privilege.",

        "• Monitor lateral movement between enterprise assets.",

        "• Perform regular vulnerability scanning and attack path analysis.",

        "• Keep operating systems and applications updated.",

        "• Review firewall rules and remove unnecessary access.",

        "• Protect sensitive databases using network segmentation and strong authentication."

    ])

    for index, recommendation in enumerate(recommendations, start=1):

        elements.append(

            Paragraph(

                f"{index}. {recommendation}",

                body

            )

        )

        elements.append(

            Spacer(1,8)

        )

    return elements