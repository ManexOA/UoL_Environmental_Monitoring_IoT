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

data = "mem,host=host1 used_percent=38.43234543"
write_api.write(bucket, org, data)

# Dispose the Client
client.close()
