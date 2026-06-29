from datetime import datetime

from modules.asset_manager import get_all_assets
from modules.vulnerability_manager import get_all_vulnerabilities
from modules.relationship_manager import get_all_relationships


def report_statistics(graph):

    return {

        "assets": len(get_all_assets()),

        "vulnerabilities": len(get_all_vulnerabilities()),

        "relationships": len(get_all_relationships()),

        "nodes": graph.total_nodes(),

        "edges": graph.total_edges()

    }


def report_date():

    return datetime.now().strftime("%d %B %Y %H:%M")