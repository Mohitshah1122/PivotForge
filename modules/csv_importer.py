import pandas as pd

from modules.asset_manager import (
    add_asset,
    get_all_assets
)


class CSVImporter:

    def import_assets(self, filepath):

        dataframe = pd.read_csv(filepath)

        existing_assets = get_all_assets()

        existing_ips = set()

        existing_names = set()

        for asset in existing_assets:

            existing_ips.add(asset["ip_address"])

            existing_names.add(asset["asset_name"].lower())

        imported = 0
        skipped = 0
        failed = 0

        for _, row in dataframe.iterrows():

            try:

                asset_name = str(row["asset_name"]).strip()

                ip_address = str(row["ip_address"]).strip()

                asset_type = str(row["asset_type"]).strip()

                criticality = str(row["criticality"]).strip()

                if (
                    ip_address in existing_ips
                    or
                    asset_name.lower() in existing_names
                ):

                    skipped += 1

                    continue

                add_asset(

                    asset_name,

                    ip_address,

                    asset_type,

                    criticality

                )

                existing_ips.add(ip_address)

                existing_names.add(asset_name.lower())

                imported += 1

            except:

                failed += 1

        return {

            "total": len(dataframe),

            "imported": imported,

            "skipped": skipped,

            "failed": failed

        }