import os
from operator import itemgetter
from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

workloads_client = StaxClient('workloads')
workload_catalogues = workloads_client.ReadCatalogueItems()

# will delete workload catalogues and all versions that are active and contain any part of the below value
WORKLOAD_CATALOGUE_NAME = "Smoke Test"

for catalogues in workload_catalogues["WorkloadCatalogues"]:
    for catalogue_item in sorted(catalogues["WorkloadCatalogueItems"], key=itemgetter("CreatedTS"), reverse=True):
        if (
            WORKLOAD_CATALOGUE_NAME in catalogue_item["Name"]
            and catalogue_item["Status"] == "ACTIVE"
        ):
            print(f"Found {catalogue_item['Name']}, Id: {catalogue_item['Id']}")

            for version in catalogue_item["Versions"]:
                print(f"Deleting version {version['Id']}")
                workloads_client.DeleteCatalogueVersion(
                    catalogue_id=catalogue_item["Id"],
                    version_id=version["Id"],
                )

            print(f"Deleting {catalogue_item['Name']}, {catalogue_item['Id']}")
            workloads_client.DeleteCatalogueItem(catalogue_id=catalogue_item["Id"])
