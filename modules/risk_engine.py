from modules.vulnerability_manager import get_all_vulnerabilities


class RiskEngine:

    def __init__(self):

        pass

    # ----------------------------------------
    # Calculate Risk Score
    # ----------------------------------------

    def calculate_score(self, attack_path):

        vulnerability_count = len(get_all_vulnerabilities())

        path_length = len(attack_path)

        score = (

            vulnerability_count * 15

            +

            path_length * 10

        )

        if score > 100:

            score = 100

        return score

    # ----------------------------------------
    # Risk Level
    # ----------------------------------------

    def calculate_level(self, score):

        if score <= 25:

            return "Low"

        elif score <= 50:

            return "Medium"

        elif score <= 75:

            return "High"

        else:

            return "Critical"

    # ----------------------------------------
    # Full Risk Analysis
    # ----------------------------------------

    def analyze(self, attack_path):

        score = self.calculate_score(attack_path)

        level = self.calculate_level(score)

        return {

            "score": score,

            "level": level

        }