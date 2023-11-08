#!/usr/bin/python3
import sys
import time
import serial
import csv
from datetime import datetime
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions

import argparse, serial, time, sys

#Define variables and the client of the remote PC to write to InfluxDB open source server (OSS)
OSS_url = "http://138.253.48.88:8086"
OSS_token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
OSS_org = "UoL_environmental_monitoring"
OSS_bucket = "REMS_Strip Modules"
#Initialize OSS Client
OSS_client = InfluxDBClient(url=OSS_url, token=OSS_token, org=OSS_org)

# Define data writing mode for the Client
write_api_OSS = OSS_client.write_api(write_options=WriteOptions(batch_size=1))



#******************************************

# Read serial data (Taking specified Port and Baud Rate arguments)
def readSerial(args):
    """Read the serial output and print it to screen."""

    #------------------------------------------

    #serial setup
    ser = serial.Serial(
        port = args.port,
        baudrate = args.baudrate,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 60)
    ser.flushInput()

    #------------------------------------------
    #loop
    while True:
        try:
            print(time.strftime("%Y%m%d%H%M%S"), ser.readline().decode("utf-8", errors="ignore").strip("\n"))
        except KeyboardInterrupt:
            print()
            sys.exit(0)


        # read serial port until '\n'

        data = ser.readline().rstrip().decode().split()
#* "decode()" function converts bytes to strings
#* "split()" function creates a list of comma delimited strings
                        
        # create dict with captured data and timestamp
        counts = {
            'Date/Time' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "Temperature(°C)":data[0],
            "Relative humidity(%)":data[1],
            "Dewpoint temperature(°C)":data[2],
            "Dust particles(0.5-10μm/ft3)":data[3]
        }

        # Display data in the shell
        print(counts)

        json_body = [{"measurement":"Environmental data",
                "tags":{"Device":"Canary board"},
                "fields":{
                    "Temperature(°C)":float(data[0]),
                    "Relative humidity(%)":float(data[1]),
                    "Dewpoint temperature(°C)":float(data[2]),
                    "Dust particles(0.5-10μm/ft3)":float(data[3])
                    }
            }]



        #Write data to InfluxDB OSS
        write_api_OSS.write(OSS_bucket, OSS_org, json_body)


    self.ser.close()


#******************************************
if __name__ == "__main__":

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description="%prog [options]")
    parser.add_argument("-p", "--port", dest="port", default="/dev/ttyUSB0", help="serial port, usually \"/dev/cu.SLAB_USBtoUART\" or \"/dev/ttyUSB0\"")
    parser.add_argument("-b", "--baudrate", dest="baudrate", default=115200, help="baud rate")
    args = parser.parse_args()
    
    #------------------------------------------
    #Call the function "read serial" sending input arguments
    readSerial(args)
    print()
