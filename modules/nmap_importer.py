import xml.etree.ElementTree as ET

from modules.asset_manager import (
    add_asset,
    get_all_assets
)

from modules.service_manager import add_service
from modules.db import get_connection


class NmapImporter:

    def import_scan(self, filepath):

        tree = ET.parse(filepath)
        root = tree.getroot()

        existing_assets = get_all_assets()

        existing_ips = {

            asset["ip_address"]

            for asset in existing_assets

        }

        imported = 0
        skipped = 0

        for host in root.findall("host"):

            # -----------------------------
            # Check Host Status
            # -----------------------------

            status = host.find("status")

            if status is None:
                continue

            if status.attrib.get("state") != "up":
                continue

            # -----------------------------
            # Get IP Address
            # -----------------------------

            address = host.find("address")

            if address is None:
                continue

            ip = address.attrib.get("addr")

            if ip in existing_ips:

                skipped += 1
                continue

            # -----------------------------
            # Hostname
            # -----------------------------

            hostname = "Unknown"

            hostnames = host.find("hostnames")

            if hostnames is not None:

                hostname_tag = hostnames.find("hostname")

                if hostname_tag is not None:

                    hostname = hostname_tag.attrib.get(
                        "name",
                        "Unknown"
                    )

            # -----------------------------
            # Asset Information
            # -----------------------------

            asset_type = "Host"
            criticality = "Medium"

            add_asset(

                hostname,
                ip,
                asset_type,
                criticality

            )

            existing_ips.add(ip)

            imported += 1

            # -----------------------------
            # Get Asset ID
            # -----------------------------

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(

                "SELECT id FROM assets WHERE ip_address=?",

                (ip,)

            )

            asset = cursor.fetchone()

            connection.close()

            if asset is None:
                continue

            asset_id = asset["id"]

            # -----------------------------
            # Import Services
            # -----------------------------

            ports = host.find("ports")

            if ports is None:
                continue

            for port in ports.findall("port"):

                state = port.find("state")

                if state is None:
                    continue

                if state.attrib.get("state") != "open":
                    continue

                port_number = int(

                    port.attrib.get("portid", 0)

                )

                protocol = port.attrib.get(

                    "protocol",

                    "tcp"

                )

                service_name = "Unknown"

                version = ""

                service = port.find("service")

                if service is not None:

                    service_name = service.attrib.get(

                        "name",

                        "Unknown"

                    )

                    product = service.attrib.get(

                        "product",

                        ""

                    )

                    version_number = service.attrib.get(

                        "version",

                        ""

                    )

                    extra = service.attrib.get(

                        "extrainfo",

                        ""

                    )

                    version = " ".join(

                        part

                        for part in [

                            product,

                            version_number,

                            extra

                        ]

                        if part

                    )

                add_service(

                    asset_id,

                    port_number,

                    protocol,

                    service_name,

                    version

                )

        return {

            "imported": imported,

            "skipped": skipped

        }