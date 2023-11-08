from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
org = "UoL_environmental_monitoring"
bucket = "REMS"

client = InfluxDBClient(url="http://138.253.48.88:8086", token=token, org=org)

# Write Data
write_api = client.write_api(write_options=SYNCHRONOUS)

sequence = ["mem,host=host1 used_percent=23.43234543",
            "mem,host=host1 available_percent=15.856523"]
write_api.write(bucket, org, sequence)

#Execute a Flux query
query = 'from(bucket: "REMS") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)
for table in tables:
    for record in table.records:
        print(record)

# Dispose the Client
client.close()
