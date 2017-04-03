#!/usr/bin/env python
import requests 
import json
import psutil
from datetime import datetime
import socket
import time 
while 1:
	#record the current time
	currentTime= str(datetime.now()) 

	#record the GPS coordinates of user
	freeGeoIP = "http://freegeoip.net/json" 
	geoRequest = requests.get(freeGeoIP) 
	geoJson = geoRequest.json() 
	userPostition = [geoJson["latitude"], geoJson["longitude"]] 

	#record stats about computer 
	cpuUsage= psutil.cpu_percent()
	mem= psutil.virtual_memory()
	memoryUsage= mem.percent
	disk= psutil.disk_usage('/')
	diskUsage= disk.percent

	udpIP= "127.0.0.1"
	udpPort= 5005
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((udpIP, udpPort))
	message= str(currentTime) + "|" + str(userPostition) + "|" +str(cpuUsage) + "|" + str(memoryUsage) + "|" +str(diskUsage)
	sock.send(message.encode())

	print(currentTime)
	print(userPostition)
	print(cpuUsage)
	print(memoryUsage)
	print(diskUsage)

	time.sleep(5)
	