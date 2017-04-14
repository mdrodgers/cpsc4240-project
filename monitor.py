#!/usr/bin/env python
import requests 
import json
import psutil
from datetime import datetime
import socket
import time 
import sys
id=0

if len(sys.argv) < 3:
	print("Usage ./monitor IP port")
	quit()
tcpIP=sys.argv[1]
tcpPort=int(sys.argv[2])
#continually send computer stats (every 15 seconds)
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

	#set up the tcp socket and attempt to connect
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((tcpIP, tcpPort))
	newId=sock.recv(1024).decode()
	if id == 0:
		id=newId
	#concat message with | as the delimiter
	message= str(id) + "|" + str(currentTime) + "|" + str(userPostition) + "|" +str(cpuUsage) + "|" + str(memoryUsage) + "|" +str(diskUsage)
	#encode the bytes and send
	sock.send(message.encode())

	#print the data we sent
	print(currentTime)
	print(userPostition)
	print(cpuUsage)
	print(memoryUsage)
	print(diskUsage)

	#sleep for 5 minutes
	time.sleep(15)
