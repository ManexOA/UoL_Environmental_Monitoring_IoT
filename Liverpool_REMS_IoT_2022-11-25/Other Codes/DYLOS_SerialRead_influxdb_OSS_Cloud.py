# The MIT License (MIT)

# Copyright (c) 2016 Nicholas E. Johnson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
import serial
import csv
from datetime import datetime
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client import InfluxDBClient,WriteOptions


#Define variables and the client to write to InfluxDB open source (OSS)
OSS_url = "http://138.253.48.88:8086"
OSS_token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
OSS_org = "UoL_environmental_monitoring"
OSS_bucket = "REMS_Strip Modules"
#Initialize OSS Client
OSS_client = InfluxDBClient(url=OSS_url, token=OSS_token, org=OSS_org)


#Define variables and the client to write to InfluxDB Cloud
cloud_token = "e54n689WZqkIepfjp5pn1tMYqg9Dy_itZhYIqwiMwn8fROnXtNAIw00rAUtHSHIvd61D65ob4HHCo_EWBHTsMA=="
cloud_org = "m.ormazabal-arregi@liverpool.ac.uk"
cloud_url = "https://europe-west1-1.gcp.cloud2.influxdata.com"
cloud_bucket = "rems"
#Initialize Cloud Client
cloud_client = InfluxDBClient(url=cloud_url, token=cloud_token, org=cloud_org)


# Define data writing mode for both Clients
write_api_OSS = OSS_client.write_api(write_options=WriteOptions(batch_size=1))
write_api_cloud = cloud_client.write_api(write_options=WriteOptions(batch_size=1))


__author__ = "Nicholas E. Johnson <nejohnson2@gmail.com>"
__copyright__ = "Copyright (C) 2016 Nicholas Johnson"
__license__ = "MIT"
__version__ = "v1.0"

class Dylos(object):
	"""docstring for Dylos"""
	def __init__(self, port):
		self.port = port
		try:
			self.ser = serial.Serial(port=self.port 
							, baudrate=9600
							, parity=serial.PARITY_NONE
							, stopbits=serial.STOPBITS_ONE
							, bytesize=serial.EIGHTBITS)
		except IOError as e:
			print("Serial connection failed\n%s" %(e))
			raise

		self.ser.flushInput()
		self.ser.flushOutput()
		time.sleep(0.1)			

	def write_csv(self, results):
		'''Write data to a csv file'''
		fname = '/media/rems/REMS/dylos.txt'

		with open(fname, 'a') as f:
			w = csv.DictWriter(f, results.keys())
			w.writerow(results)

		f.close()

	def read(self, store=False):
		"""Read serial data in non-blocking

		Parameters:
		----------
		store: boolean,
			Set true to write to csv file
		"""			
		print("Listening for Dylos data...")
                
		while True:
			# read serial port until '\n'
			data = self.ser.readline().rstrip().split(b',')

			# calculate 0.5-2.5um 
			greater_pm2_5 = int(data[1])

			corrFactor = 1./0.0283168*100
                        
			# create dict with captured data and timestamp
			counts = {
				'time' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
				'small' : float(data[0])*corrFactor, # >0.5um
				'large' : float(data[1])*corrFactor # >2.5um				
			}

			# Display data in the shell
			print(counts)

			json_body = [{"measurement":"Environmental data",
					"tags":{"Device":"DYLOS Particle counter"},
					"fields":{
						">0.5um ppm (small)":float(data[0])*corrFactor,
						">2.5um ppm (large)":float(data[1])*corrFactor
						}
				}]


                        # Write data to InfluxDB OSS
			write_api_OSS.write(OSS_bucket, OSS_org, json_body)

			# Write data to InfluxDB Cloud
			write_api_cloud.write(cloud_bucket, cloud_org, json_body)



		self.ser.close()		

	def __del__(self):
		'''Cleanup'''
		try:
			self.ser.close()
			print("Closed serial port")
		except:
			pass
		print("Cleaning up Dylos class")


if __name__ == '__main__':
	port = '/dev/ttyUSB0'

	try:
		d = Dylos(port)
	except:
		print("Unable to setup serial communication")
		sys.exit()
	# runs forever
	d.read()

	sys.exit()
