#!/usr/bin/env python
import signal
import sys
import serial
import time
import datetime
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
import pandas as pd

#Open text file where data will be written
f = open('/media/rems/REMS/rems.txt', 'a')

#Define InfluxDB variables that correspond to the remote PC:
token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
org = "UoL_environmental_monitoring"
bucket = "REMS"

#Initialize the client with the scpecified variables:
client = InfluxDBClient(url="http://138.253.48.88:8086", token=token, org=org)

#Define data writing mode:
write_api = client.write_api(write_options=SYNCHRONOUS)

#Data serial reading:
def signal_handler(signal, frame):
        print(" bye")
        f.closed
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
)

#Sort the data and save it in a dictionary called "raw_data":
while 1:
    x=ser.readline()
    if len(x)>0:
        today = datetime.date.today()
        now = datetime.datetime.now()
        f.write(str(now) + "\t" + x.decode())
        if x is not None:
                node_id, status, voltage, atmega_temperature, wakeup_time, temperature, humidity, rssi = x.split()
                node_id = int(node_id)
                node_id = str(node_id)
                print(node_id)

                raw_data = {}
                raw_data['node_id'] = int(node_id)
                raw_data['status'] = int(status)
                raw_data['voltage'] = float(voltage)
                raw_data['atmega_temperature'] = float(atmega_temperature)
                raw_data['wakeup_time'] = int(wakeup_time)
                raw_data['temperature'] = float(temperature)
                raw_data['humidity'] = float(humidity)
                raw_data['rssi'] = int(rssi)
         
                myTags = {
                        "unit_id": str(99),
                        "location": "none",
                        "sensor": "none"
                        }        


# Separate data of each sensor:

                if "2" in node_id:
                        myTags = {
                        "unit_id": str(node_id),
                        "location": "LOCATION 1",
                        "sensor": "SHT85"
                        }

#Write data to InfluxDB as "node_id 2":
                        df = pd.DataFrame(data=raw_data, index=[pd.Timestamp.utcnow()]) #Create data frame
                        write_api.write(bucket, org, df, data_frame_measurement_name="node_id 2") # Write data to influxdb - "node_id 2" measurement directory


                if "3" in node_id:
                        myTags = {
                        "unit_id": str(node_id),
                        "location": "LOCATION 2",
                        "sensor": "SHT85"
                        }        

#Write data to InfluxDB as "node_id 3":
                        df = pd.DataFrame(data=raw_data, index=[pd.Timestamp.utcnow()])
                       # write_api = client.write_api(write_options=SYNCHRONOUS)
                        write_api.write(bucket, org, df, data_frame_measurement_name="node_id 3") # Write data to influxdb - "node_id 3" measurement directory


#Display the data on the RaspberryPi:

                print (df)
                print (myTags)

#Dispose the Client
client.close()
