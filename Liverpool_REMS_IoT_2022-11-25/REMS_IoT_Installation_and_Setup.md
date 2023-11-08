# REMS ENVIRONMENTAL MONITORING IOT System

* Author: Manex Ormazabal Arregi
* Email: manex@liverpool.ac.uk
* Company: University of Liverpool - Physics Department
* Date: 05/12/2022

These instructions show how to do the installation and configuration of the REMS IoT system for environmental monitoring, specifically made for monitoring the environment of the clean rooms located at the University of Liverpool - Physics department.
In this case, RaspberryPi-s have been used as a passive unit for data acquisition through different sensors, and a stand-alone PC has been used for visualizing the data in form of graphs with InfluxDB and Grafana interfaces.

(note: if you are using just one machine for both data acquistion and for visualizing data in InfluxDB and Grafana, the isntructions to follow might be slightly different and it may not be neccesary
to do all the setup and installation as showed in these instructions.)


## 1. Used Hardware and Software

 1.1- Hardware:

    - 2x Raspberry Pi
    - PC with Linux operative system
    - USB stick 32GB
    - Jeelink Wi-Fi receiver
    - 2x Arduino Temperature and Humidity sensors
    - Dylos DC1700 particle counter

 1.2- Software:

    - Raspbian GNU/Linux 11 (Bullseye) on Raspberry Pi-s
    - Ubuntu 22.04 on the PC
    - Python v3 on the Raspberry Pi and the PC
    - InfluxDB-CLIENT v1.34.0 Python library (for InfluxDB v2.x) on the Raspberry Pi and the PC
    - Pandas python library on the Raspberry Pi
    - pySerial python library on the Raspberry Pi
    - InfluxDB 2.x OSS on the PC only
    - Grafana OSS (Server) on the PC
    - Grafana CLI version 9.2.4 on the PC
    - InfluxDB and Grafana web interfaces accessible from any remote PC

## 2. Network details 

 2.1- IP addresses of the machines:
 
    - Raspberry Pi 1 (tmp/hum):----------------192.168.202.87
    - Raspberry Pi 2 (Dylos):------------------192.168.202.88
    - Raspberry Pi 3 (Canary board):-----------169.254.144.148
    - Linux PC:--------------------------------138.253.48.88
    
 2.2- Ports:
 
    - InfluxDB OSS web interface:--------------port 8086
    - Grafana web interface:-------------------port 3000

## 3. Installation and Setup instructions

2.1- On the RaspberryPi:

- Install Python v3 (if already not coming by default with the RPi OS)
- Install python pip3
- Install latest InfluxDB-CLIENT (In our case v1.34.0 was installed)
- Install pySerial python library for serial data reading
- Install Pandas python library to create data frames
-* Install libatlas-base-dev (if "libcblas.so.3 Error: No such file or directory" is given)

2.2- On the PC:

- Install InfluxDB V2.x version (In our case, V2.4 was installed)
- Install Grafana OSS 
- Install Python v3
- Install pip3
- Install latest InfluxDB-CLIENT (In our case v1.34.0 was installed)

2.3- On the InfluxDB OSS:

- Login to the InfluxDB OSS web interface by typing the ip address of the PC and followed by the port (in this case 8086). Example: "138.253.48.88:8086".
- Create a bucket (In our case with the name "REMS")
- Create a Token

2.4- On the RaspberryPi:

- Open the python script (e.g."SHT85_SerialRead_influxdb_OSS.py") with an editor (nano, emacs, vim...etc).

- Add your "org", "token" and "bucket" names created on the InfluxDB OSS
  
  *Example: token = "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw=="
            org = "UoL_environmental_monitoring"
            bucket = "REMS"

- Edit the "Initialize the Client" part adding the "url" of the remote PC, followed by the "token" and the "org"
  
  *Example: client = InfluxDBClient(url="http://138.253.48.88:8086", token=token, org=org)

- If you also need to write data to a text file, make sure you also edit the directory and the name of the file you are writing to on the python script.


## 4. Setup the influxDB CLIENT

- In our case, this was made as follows:

  influx config create --config-name envuser \
    --host-url http://138.253.48.88:8086 \
    --org "UoL_environmental_monitoring" \
    --token "gtWbY-DSA8NgaPyr_pEGQwf0W7T__2YcvQwmYoPGsU-7Tuvyz2dD1PfYGM7juGj3iAPZd6YNX2s9lX-FOL9Iiw==" \
    --active

  *More information: https://docs.influxdata.com/influxdb/v2.4/tools/influx-cli/?t=Linux

## 5. Enable TLS encryption for https communication

  In InfluxDB V2, to enable HTTPS communication you need TLS certificate.

  This is a must if you need to connect to an InfluxDB server from a remote client using 
  https network protocol. To enable HTTPS with InfluxDB, you need a Transport Layer Security (TLS) certificate,
  also known as a Secured Sockets Layer (SSL) certificate.

  *More information: https://docs.influxdata.com/influxdb/v2.5/security/enable-tls/

## 6. Setup Grafana web interface

6.1- Install Grafana. A good installation guide is provided here: https://grafana.com/docs/grafana/latest/installation/

6.2- Go to the web browser and login to Grafana with the ip address and the port (3000 by default). 
  Use "admin" username and "admin" password to login.

6.3- Configure the "Data Source Settings" of type InfluxDB:
 - Select settings name
 - Select query language "Flux"
 - In the "HTTP" section write the "url" address with the PC's ip address and the port. Example: "http://138.253.48.88:8086"
 - In the "InfluxDB Details" section, your InfluxDB org name, Token and the Bucket name.
 - Finally, click on "save & test". If everything is correct it should show a green coloured message. If not, it will show a red message.

6.4- Create a new dashboard
   - Add a new Panel
   - Select your Data Source (Previously created in "Data Source Settings")
   - Add Query (In the "Query Inspector"), and add the following lines to filter the data you want to plot: 

```bash
     from(bucket: "REMS")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "data")
  |> filter(fn: (r) => r["_field"] == "temperature")
  |> filter(fn: (r) => r["location"] == "lab_gladd2")
  |> filter(fn: (r) => r["sensor"] == "SHT85")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

## 7. The Startup of the system:

- Make sure if the influxDB service is running on the PC. 

  To check the service status type:
  ```bash
  sudo service influxdb status
  ```
  To start the service type:
  ```bash
  sudo service influxdb start
  ```
  To stop the service type
  ```bash
  sudo service influxdb stop
  ```

- On the raspberryPi, go to "serial" folder, where the executable python script is, and run the program.
  You can run the python script by typing: <python3 "program name.py">.
  -Example:
  ```bash 
  python3 SHT85_SerialReading_to_InfluxdbOSS.py
  ```
-* if the python file requires root permission (sudo command) to be lanched, follow these steps to remove the root permission:
  1. Add your RPi username to the dialout:
  ```bash
  sudo adduser <the user you want to add> dialout
  ```
  2. Finally log out and log in again, or Reboot the machine.


- If the program is working, login to the InfluxDB OSS web interface from the PC. To login just type "http://138.253.48.88:8086" on the web browser. Once you have logged in, check if there is data in the Bucket and if you can visualize it on the "Data Explorer".

- Go to Grafana web interface by typing "http://138.253.48.88:3000" on the web browser, and check if there is data coming through InfluxDB on a Panel that you created. You might need to set some filters in the Query section to visualize a specific measurement data.



## Used web sources

- [ ] [Influxdb-client python library WriteApi function] (https://pypi.org/project/influxdb-client/#writes)
- [ ] [InfluxDB and Grafana installation for RaspberryPi] (https://simonhearne.com/2020/pi-influx-grafana/)
- [ ] [InfluxDB-Client python instructions] (https://github.com/influxdata/influxdb-client-python)
- [ ] [InfluxDB data sending ith Python example] (https://thenewstack.io/obtaining-and-storing-time-series-data-with-python/)
- [ ] [Create a database in InfluxDB tutorial] (https://devconnected.com/how-to-create-a-database-on-influxdb-1-7-2-0/)
- [ ] [InfluxDB-Client python library WriteApi function instructions] (https://influxdb-client.readthedocs.io/en/stable/usage.html#write)
- [ ] [Influxdb Cloud data sending from python instructions] (https://www.influxdata.com/blog/how-influxdb-open-source-complements-influxdb-cloud/)
- [ ] [Dylos serial reading example python script] (https://github.com/drjct/dylos_raspberrypi/blob/master/main.py)

## Future work

- Set alarms to pop-up a message when a measurement is out of normal range or if there is an issue in the system.
- Set the RPi-s to run the program automatically on boot, without having to launch anything from the terminal.
- Fix the issue of "Timeout Error": The program stops working after working for a while.
- Intall a remote access tool (e.g. VNC or Tiger) to access the Master PC' and control its desktop remotelly from anywhere outside the office, as well as to visualize data on InfluxDB and Grafana.







