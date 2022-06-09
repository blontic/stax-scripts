import os
import json
from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

workloads_client = StaxClient('workloads')
workloads = workloads_client.ReadWorkloads()

# will delete workloads that are not deleted and contain any part of the below value
WORKLOAD_NAME = "Smoke Test"

for workload in workloads["Workloads"]:
    if WORKLOAD_NAME in workload["Name"]:
        if workload["Status"] != "DELETED":
            print(f"Deleting Workload: {workload['Name']}, Status: {workload['Status']}")
            response = workloads_client.DeleteWorkload(workload_id=workload["Id"])
            print(json.dumps(response, indent=4, sort_keys=True))
