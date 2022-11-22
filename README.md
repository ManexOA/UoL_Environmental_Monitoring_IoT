# Project: Environmental Monitoring IoT
# Author: Manex Ormazabal
# Location: University of Liverpool - Physics Department - Liverpool Semiconductor Detector Centre - Cleanroom
# Date: 22/11/2022
# Description:
This project was created for the environmental monitoring of cleanrooms used mainly in the ATLAS ITk project at the physics department of the University of Liverpool. For this, an IoT system was develped to monitor diferent measurements such us Temperature, Humidity or Dust Particles in the environment.
Preliminary, for measuring the temperature and humidity SW854 sensors were used and as a particle counter, Dylos was used.
After, the Canary board was also used as a sensor which integrates temperature, humidity and dust particle measurements in a single device.
All data measured by the sensors was read and controlled by a Raspberry Pi. Then, a separate Linux PC was used for monitoring and visualizing all the data, thanks to InfluxDB and Grafana interfaces that were installed on it.
