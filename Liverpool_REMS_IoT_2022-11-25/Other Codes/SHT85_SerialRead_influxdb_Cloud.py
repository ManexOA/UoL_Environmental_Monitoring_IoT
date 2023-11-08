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


#Define variables and the client to write to InfluxDB Cloud
#cloud_token = "e54n689WZqkIepfjp5pn1tMYqg9Dy_itZhYIqwiMwn8fROnXtNAIw00rAUtHSHIvd61D65ob4HHCo_EWBHTsMA=="
#cloud_org = "m.ormazabal-arregi@liverpool.ac.uk"
#cloud_url = "https://europe-west1-1.gcp.cloud2.influxdata.com"
#cloud_bucket = "rems"

#Initialize Cloud Client
#cloud_client = InfluxDBClient(url=cloud_url, token=cloud_token, org=cloud_org)



#Data serial reading from sensors
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

#Store data in a Pandas data frame
while 1:
    x=ser.readline()
    if len(x)>0:
        today = datetime.date.today()
        now = datetime.datetime.now()
        f.write(str(now) + "\t" + x.decode())
        if x is not None:

                x = node_id, status, voltage, atmega_temperature, wakeup_time, temperature, humidity, rssi = x.split()



                raw_data = {}
                raw_data['node_id'] = int(node_id)
                raw_data['status'] = int(status)
                raw_data['voltage'] = float(voltage)
                raw_data['atmega_temperature'] = float(atmega_temperature)
                raw_data['wakeup_time'] = int(wakeup_time)
                raw_data['temperature'] = float(temperature)
                raw_data['humidity'] = float(humidity)
                raw_data['rssi(Signal strength)'] = int(rssi)
         

#Classify data into type of data source:

                if "2" in str(node_id):

                        json_body = [{"measurement":"Environmental data",
                                        "tags":{"Device":"SHT85 node_id 2"},
                                        "fields": raw_data

                                }]



                if "3" in str(node_id):

                        json_body = [{"measurement":"Environmental data",
                                        "tags":{"Device":"SHT85 node_id 3"},
                                        "fields": raw_data 

                                }]


#Create data frame:

                df = pd.DataFrame(data=raw_data, index=[pd.Timestamp.utcnow()])

#Write data to InfluxDB Cloud:

                write_api_cloud = cloud_client.write_api(write_options=SYNCHRONOUS)
                write_api_cloud.write(cloud_bucket, cloud_org, json_body)

#Display data
                print (df)

#Dispose the Client
client.close()
