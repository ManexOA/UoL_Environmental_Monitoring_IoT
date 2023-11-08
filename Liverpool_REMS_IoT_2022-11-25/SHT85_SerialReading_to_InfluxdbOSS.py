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
#f = open('/media/pi4/REMS/rems.txt', 'a')

#Define variables and the client to write to InfluxDB open source server (OSS)
OSS_url = "http://138.253.48.88:8086"
OSS_token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
OSS_org = "UoL_environmental_monitoring"
OSS_bucket = "REMS_Strip Modules"

#Initialize OSS Client
OSS_client = InfluxDBClient(url=OSS_url, token=OSS_token, org=OSS_org)


#Serial data reading
def signal_handler(signal, frame):
        print(" bye")
        #f.closed
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Define serial reading parameters:

ser = serial.Serial(     
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
)

while 1:
     x=ser.readline() #Read serial data
     if len(x)>0:   #Wait until data comes through the serial port
         today = datetime.date.today()
         now = datetime.datetime.now() 
         #f.write(str(now) + "\t" + x.decode()) #Write data to text file
         serial_data = x.split() #Convert bytes into a list of separated bytes

         if x is not None:

# Create a dictionary with bytes converted to integers/floats:
                raw_data = {}
                raw_data['node_id'] = int(serial_data[0])
                raw_data['status'] = int(serial_data[1])
                raw_data['voltage(V)'] = float(serial_data[2])
                raw_data['atmega_temperature(°C)'] = float(serial_data[3])
                raw_data['wakeup_time(s)'] = int(serial_data[4])
                raw_data['temperature(°C)'] = float(serial_data[5])
                raw_data['relative humidity(%)'] = float(serial_data[6])
                raw_data['rssi(Signal strength(db))'] = int(serial_data[7])

#Classify incoming data based on data source device type (e.g. node_id 2 or node_id 3 sensor modules):

                if "2" in str(serial_data[0]):

                        json_body = [{"measurement":"Environmental data",
                                        "tags":{"Device":"SHT85 node_id 2"},
                                        "fields": raw_data

                                }]


                if "3" in str(serial_data[0]):

                        json_body = [{"measurement":"Environmental data",
                                        "tags":{"Device":"SHT85 node_id 3"},
                                        "fields": raw_data 

                                }]

#Create a data frame:
                df = pd.DataFrame(data=raw_data, index=[pd.Timestamp.utcnow()])

#Display data in terminal:
                print (df)
                
#Send data to InfluxDB OSS:
                write_api_OSS = OSS_client.write_api(write_options=SYNCHRONOUS)
                write_api_OSS.write(OSS_bucket, OSS_org, json_body)

#Dispose the Client
client.close()
