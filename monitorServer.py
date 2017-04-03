#!/usr/bin/env python
import socket

udpIP = "127.0.0.1"
udpPort = 5005
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
sock.bind((udpIP, udpPort))
sock.listen(1) 

while 1:
	conn, addr = sock.accept()
	print("New connection from ", addr)
	while 1:
		data = conn.recv(1024).decode()
		if not data:
			break
		print("Received:", data)

		currentTime= data.split("|")[0]
		userPosition=data.split("|")[1]
		cpuUsage= data.split("|")[2]
		memoryUsage= data.split("|")[3]
		diskUsage= data.split("|")[4]

		print("Current time: ", currentTime)
		print("User Position: ", userPosition)
		print("CPU Usage: ", cpuUsage, "%")
		print("Memory Usage: ", memoryUsage, "%")
		print("Disk Usage: ", diskUsage, "%")
	conn.close()