from modules.asset_manager import get_all_assets
from modules.asset_risk_engine import AssetRiskEngine
from modules.vulnerability_manager import get_all_vulnerabilities
from modules.relationship_manager import get_all_relationships
from modules.service_manager import get_all_services


class DashboardAnalytics:

    def __init__(self):
        pass

    # ---------------------------------
    # Total Assets
    # ---------------------------------

    def total_assets(self):

        return len(get_all_assets())

    # ---------------------------------
    # Total Vulnerabilities
    # ---------------------------------

    def total_vulnerabilities(self):

        return len(get_all_vulnerabilities())

    # ---------------------------------
    # Total Relationships
    # ---------------------------------

    def total_relationships(self):

        return len(get_all_relationships())

    # ---------------------------------
    # Total Services
    # ---------------------------------

    def total_services(self):

        return len(get_all_services())

    # ---------------------------------
    # Critical Vulnerabilities
    # ---------------------------------

    def critical_vulnerabilities(self):

        total = 0

        for vulnerability in get_all_vulnerabilities():

            if vulnerability["severity"].lower() == "critical":

                total += 1

        return total

    # ---------------------------------
    # Critical Assets
    # ---------------------------------

    def critical_assets(self):

        total = 0

        for asset in get_all_assets():

            if asset["criticality"].lower() == "critical":

                total += 1

        return total
    
        # ---------------------------------
    # Overall Security Score
    # ---------------------------------

    def security_score(self):

        assets = self.total_assets()

        vulnerabilities = self.total_vulnerabilities()

        critical = self.critical_vulnerabilities()

        score = 100

        score -= vulnerabilities * 5

        score -= critical * 10

        if score < 0:

            score = 0

        return score
    
        # ---------------------------------
    # Overall Risk Level
    # ---------------------------------

    def risk_level(self):

        score = self.security_score()

        if score >= 85:

            return "Low"

        elif score >= 65:

            return "Medium"

        elif score >= 40:

            return "High"

        else:

            return "Critical"
        
            # ---------------------------------
    # Top 5 Riskiest Assets
    # ---------------------------------

    def top_risky_assets(self):

        engine = AssetRiskEngine()

        assets = get_all_assets()

        risk_list = []

        for asset in assets:

            score = engine.calculate(asset["id"])

            risk_list.append({

                "name": asset["asset_name"],

                "score": score

            })

        risk_list.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        return risk_list[:5]