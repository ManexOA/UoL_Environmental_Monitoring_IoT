#!/usr/bin/python3
import sys
import time
import serial
import csv
from datetime import datetime
from influxdb_client.client.write_api import WriteApi, SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions


#Define variables and the client of the remote PC to write to InfluxDB open source server (OSS)
OSS_url = "http://138.253.48.88:8086"
OSS_token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
OSS_org = "UoL_environmental_monitoring"
OSS_bucket = "REMS_Strip Modules"
#Initialize OSS Client
OSS_client = InfluxDBClient(url=OSS_url, token=OSS_token, org=OSS_org)

# Define data writing mode for the Client
write_api_OSS = OSS_client.write_api(write_options=WriteOptions(batch_size=1))


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
		
			#Extract serial output from Dylos
		
            #The serial output format is small counts, comma, large counts, carriage return, line feed:
            #Example:
            #675,19<CR><LF>
            #Units are particles/.01 cubic foot
            #For example, a reading of 2 means 200 particles per cubic foot
            #(These values ​​are on the same scale as the values ​​displayed on the Dylos machine)
            #Data is output every minute 

                 data = self.ser.readline().decode('utf-8')
                 small, large = data.split(',') #place the outputs into separate variables
                 small = float(small) 
                 large = float(large)

            # Convert values to "particles per cubic foot(ft3)"
                 small_particles = small*100
                 large_particles = large*100
            
			# create dict with captured data and timestamp
                 counts = {
				     'Date/Time' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
				     'Small particles (>0.5um particles / ft3)' : small_particles, # >0.5um
				     'Large particles (>2.5um particles / ft3)' : large_particles # >2.5um				
			     }


			# Display data in the terminal
                 print(counts)

                 json_body = [{"measurement":"Environmental data",
					     "tags":{"Device":"DYLOS Particle counter"},
					     "fields":{
						           "small particles (>0.5um particles / ft3)":small_particles,
						           "large particles (>2.5um particles / ft3)":large_particles
						          }
				             }]


                        # Write data to InfluxDB OSS
                 write_api_OSS.write(OSS_bucket, OSS_org, json_body)


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
