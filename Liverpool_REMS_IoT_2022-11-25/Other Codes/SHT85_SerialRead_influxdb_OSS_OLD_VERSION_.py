#!/usr/bin/python3
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

#Define variables and the client to write to InfluxDB open source (OSS)
OSS_url = "http://138.253.48.88:8086"
OSS_token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
OSS_org = "UoL_environmental_monitoring"
OSS_bucket = "REMS_Strip Modules"

#Initialize OSS Client
OSS_client = InfluxDBClient(url=OSS_url, token=OSS_token, org=OSS_org)


#Serial data reading
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


while 1:
    x=ser.readline()
    if len(x)>0:
        today = datetime.date.today()
        now = datetime.datetime.now() 
        f.write(str(now) + "\t" + x.decode())
        if x is not None:
        
# Create a byte list with the serial data
                x = node_id, status, voltage, atmega_temperature, wakeup_time, temperature, relative_humidity, rssi = x.split() 

# Create a dictionary with data bytes converted to float/integers
                raw_data = {} 
                raw_data['node_id'] = int(node_id)
                raw_data['status'] = int(status)
                raw_data['voltage(V)'] = float(voltage)
                raw_data['atmega_temperature(°C)'] = float(atmega_temperature)
                raw_data['wakeup_time(s)'] = int(wakeup_time)
                raw_data['temperature(°C)'] = float(temperature)
                raw_data['relative humidity(%)'] = float(relative_humidity)
                raw_data['rssi(Signal strength(db))'] = int(rssi)
         
                             
#Classify incoming data into type of data source (node_id 2 or node_id 3):

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

#Display data
                print (df)
                
#Send data to the InfluxDB OSS:
                write_api_OSS = OSS_client.write_api(write_options=SYNCHRONOUS)
                write_api_OSS.write(OSS_bucket, OSS_org, json_body)

#Dispose the Client
client.close()
