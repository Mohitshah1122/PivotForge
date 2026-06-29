import os
import matplotlib.pyplot as plt

from modules.vulnerability_manager import get_all_vulnerabilities
from modules.asset_manager import get_all_assets


class ReportCharts:

    def __init__(self):
        os.makedirs("reports/charts", exist_ok=True)

    # =====================================
    # Vulnerability Severity Bar Chart
    # =====================================

    def generate_vulnerability_chart(self):

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

        labels = ["Critical", "High", "Medium", "Low"]

        values = [critical, high, medium, low]

        colors = ["#d32f2f", "#f57c00", "#fbc02d", "#43a047"]

        plt.figure(figsize=(8, 4.5))

        bars = plt.bar(labels, values, color=colors)

        plt.title("Vulnerability Severity Distribution", fontsize=15, fontweight="bold")

        plt.xlabel("Severity")
        plt.ylabel("Count")

        plt.grid(axis="y", linestyle="--", alpha=0.4)

        for bar in bars:

            height = bar.get_height()

            plt.text(
                bar.get_x() + bar.get_width()/2,
                height + 0.05,
                str(int(height)),
                ha="center"
            )

        plt.tight_layout()

        output = "reports/charts/vulnerability_chart.png"

        plt.savefig(output, dpi=300)

        plt.close()

        return output

    # =====================================
    # Asset Type Pie Chart
    # =====================================

    def generate_asset_chart(self):

        assets = get_all_assets()

        counts = {}

        for asset in assets:

            asset_type = asset["asset_type"]

            counts[asset_type] = counts.get(asset_type, 0) + 1

        labels = list(counts.keys())
        values = list(counts.values())

        chart_colors = [
            "#1976D2",
            "#43A047",
            "#FB8C00",
            "#8E24AA",
            "#E53935",
            "#00897B",
            "#6D4C41",
            "#5E35B1"
        ]

        plt.figure(figsize=(8, 6))

        wedges, texts, autotexts = plt.pie(
            values,
            labels=None,
            autopct="%1.1f%%",
            startangle=90,
            colors=chart_colors
        )

        plt.legend(
            wedges,
            labels,
            title="Asset Types",
            loc="center left",
            bbox_to_anchor=(1.0, 0.5)
        )

        plt.title(
            "Enterprise Asset Distribution",
            fontsize=14,
            fontweight="bold"
        )

        plt.tight_layout()

        output = "reports/charts/asset_chart.png"

        plt.savefig(output, dpi=300, bbox_inches="tight")

        plt.close()

        return output