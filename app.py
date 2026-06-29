from flask import Flask, render_template, request, redirect, send_file
from modules.nmap_importer import NmapImporter
import sqlite3
from modules.db import get_connection
from modules.audit_logger import add_log
from modules.search_manager import SearchManager
from modules.dashboard_analytics import DashboardAnalytics
from modules.asset_details import AssetDetails
from modules.service_manager import get_all_services
from modules.db import initialize_database
from modules.csv_importer import CSVImporter

import os

from werkzeug.utils import secure_filename
from modules.asset_manager import add_asset, get_all_assets, delete_asset
from modules.vulnerability_manager import add_vulnerability, get_all_vulnerabilities
from modules.relationship_manager import add_relationship, get_all_relationships, delete_relationship
from modules.graph_engine import GraphEngine
from modules.attack_path_engine import AttackPathEngine
from modules.graph_visualizer import GraphVisualizer
from modules.report_generator import ReportGenerator
from modules.demo_data import load_demo_data

app = Flask(__name__)

initialize_database()

graph_engine = GraphEngine()
attack_engine = AttackPathEngine()
graph_visualizer = GraphVisualizer()
report_generator = ReportGenerator()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# LOAD DEMO DATA
# ==========================================

@app.route("/load-demo")
def load_demo():

    load_demo_data()

    graph_engine.build_graph()
    attack_engine.refresh()

    return redirect("/dashboard")


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    graph_engine.build_graph()

    return render_template(
        "dashboard.html",
        total_assets=len(get_all_assets()),
        total_vulnerabilities=len(get_all_vulnerabilities()),
        total_relationships=len(get_all_relationships()),
        total_nodes=graph_engine.total_nodes(),
        total_edges=graph_engine.total_edges()
    )


# ==========================================
# ASSETS
# ==========================================

@app.route("/assets", methods=["GET", "POST"])
def assets():

    if request.method == "POST":

        add_asset(
            request.form["asset_name"],
            request.form["ip_address"],
            request.form["asset_type"],
            request.form["criticality"]
        )

        graph_engine.build_graph()

        return redirect("/assets")

    return render_template(
        "assets.html",
        assets=get_all_assets()
    )


@app.route("/delete_asset/<int:asset_id>")
def remove_asset(asset_id):

    delete_asset(asset_id)

    graph_engine.build_graph()

    return redirect("/assets")


# ==========================================
# VULNERABILITIES
# ==========================================

@app.route("/vulnerabilities", methods=["GET", "POST"])
def vulnerabilities():

    if request.method == "POST":

        add_vulnerability(
            request.form["asset_id"],
            request.form["cve_id"],
            request.form["vulnerability_name"],
            request.form["severity"],
            request.form["description"]
        )

        return redirect("/vulnerabilities")

    return render_template(
        "vulnerabilities.html",
        assets=get_all_assets(),
        vulnerabilities=get_all_vulnerabilities()
    )


# ==========================================
# RELATIONSHIPS
# ==========================================

@app.route("/relationships", methods=["GET", "POST"])
def relationships():

    if request.method == "POST":

        add_relationship(
            request.form["source_asset"],
            request.form["destination_asset"],
            request.form["relationship_type"]
        )

        graph_engine.build_graph()

        return redirect("/relationships")

    return render_template(
        "relationships.html",
        assets=get_all_assets(),
        relationships=get_all_relationships()
    )


@app.route("/delete_relationship/<int:relationship_id>")
def remove_relationship(relationship_id):

    delete_relationship(relationship_id)

    graph_engine.build_graph()

    return redirect("/relationships")


# ==========================================
# ATTACK PATHS
# ==========================================

@app.route("/attack-paths", methods=["GET", "POST"])
def attack_paths():

    attack_engine.refresh()

    path = []

    risk = None

    if request.method == "POST":

        source = request.form["source"]

        destination = request.form["destination"]

        algorithm = request.form["algorithm"]

        if algorithm == "bfs":

            path = attack_engine.bfs_path(

                source,

                destination

            )

        elif algorithm == "dfs":

            path = attack_engine.dfs_path(

                source,

                destination

            )

        else:

            path = attack_engine.dijkstra_path(

                source,

                destination

            )

        from modules.risk_engine import RiskEngine

        risk_engine = RiskEngine()

        risk = risk_engine.analyze(path)

    return render_template(

        "attack_paths.html",

        nodes=attack_engine.get_assets(),

        edges=graph_engine.edge_list(),

        path=path,

        risk=risk

    )

# ==========================================
# ENTERPRISE GRAPH
# ==========================================

@app.route("/graph")
def graph():

    graph_visualizer.generate_graph()

    return render_template("graph.html")
# ==========================================
# REPORTS
# ==========================================

# ==========================================
# REPORTS
# ==========================================

@app.route("/reports")
def reports():

    return render_template("reports.html")


@app.route("/generate-report")
def generate_report():

    filename = report_generator.generate()

    return send_file(

        filename,

        mimetype="application/pdf",

        as_attachment=False

    )


@app.route("/import-assets", methods=["GET", "POST"])
def import_assets():

    if request.method == "POST":

        file = request.files["csv_file"]

        if file.filename == "":
            return "No file selected."

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            "uploads",
            "csv",
            filename
        )

        file.save(filepath)

        importer = CSVImporter()

        summary = importer.import_assets(filepath)

        return f"""
        <h2>CSV Import Summary</h2>

        <p>Total Records : {summary['total']}</p>

        <p>Imported : {summary['imported']}</p>

        <p>Skipped : {summary['skipped']}</p>

        <p>Failed : {summary['failed']}</p>

        <br>

        <a href="/import-assets">Import Another File</a>
        """

    return render_template("import_assets.html")

@app.route("/import-nmap", methods=["GET", "POST"])
def import_nmap():

    if request.method == "POST":

        file = request.files["scan"]

        if file.filename == "":
            return "No file selected."

        filename = secure_filename(file.filename)

        filepath = os.path.join(

            "uploads",

            "nmap",

            filename

        )

        file.save(filepath)

        importer = NmapImporter()

        summary = importer.import_scan(filepath)

        return f"""
        <h2>Nmap Scan Imported Successfully</h2>

        <p>Imported Hosts : {summary['imported']}</p>

        <p>Skipped Hosts : {summary['skipped']}</p>

        <br>

        <a href="/import-nmap">Import Another Scan</a>

        <br><br>

        <a href="/assets">View Assets</a>
        """

    return render_template("import_nmap.html")


@app.route("/services")
def services():

    data = get_all_services()

    return render_template(

        "services.html",

        services=data

    )

@app.route("/asset/<int:asset_id>")
def asset_details(asset_id):

    details = AssetDetails()

    return render_template(

        "asset_details.html",

        asset=details.get_asset(asset_id),

        services=details.get_services(asset_id),

        vulnerabilities=details.get_vulnerabilities(asset_id),

        relationships=details.get_relationships(asset_id),

        risk=details.get_risk(asset_id)

    )

@app.route("/executive-dashboard")
def executive_dashboard():

    analytics = DashboardAnalytics()

    return render_template(

    "executive_dashboard.html",

    assets=analytics.total_assets(),

    vulnerabilities=analytics.total_vulnerabilities(),

    relationships=analytics.total_relationships(),

    services=analytics.total_services(),

    critical_assets=analytics.critical_assets(),

    critical_vulnerabilities=analytics.critical_vulnerabilities(),

    security_score=analytics.security_score(),

    risk_level=analytics.risk_level(),

    top_assets=analytics.top_risky_assets()

)

@app.route("/search", methods=["GET", "POST"])
def search():

    assets = []
    vulnerabilities = []
    services = []
    keyword = ""

    if request.method == "POST":

        keyword = request.form["keyword"]

        manager = SearchManager()

        results = manager.search(keyword)

        assets = results["assets"]
        vulnerabilities = results["vulnerabilities"]
        services = results["services"]

    return render_template(

        "search.html",

        keyword=keyword,

        assets=assets,

        vulnerabilities=vulnerabilities,

        services=services

    )

@app.route("/logs")
def logs():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY timestamp DESC
    """)

    logs = cursor.fetchall()
    connection.close()

    return render_template("logs.html", logs=logs)
# ==========================================
# START APPLICATION
# ==========================================


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)