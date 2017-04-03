#!/usr/bin/env python
import socket
import mysql.connector

#temp localhost ip for testing
udpIP = "127.0.0.1"
udpPort = 8008
#set up the tcp socket and bind, wait for incoming connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
sock.bind((udpIP, udpPort))
sock.listen(1) 

#continually listen for new data
while 1:
	#accept new connections and print ip address
	conn, addr = sock.accept()
	print("New connection from ", addr)
	while 1:
		#recv and decode the data 
		data = conn.recv(1024).decode()
		if not data:
			break
		#split the message based on the delimiter
		currentTime= data.split("|")[0]
		userPosition=data.split("|")[1]
		cpuUsage= data.split("|")[2]
		memoryUsage= data.split("|")[3]
		diskUsage= data.split("|")[4]

		#printing for testing purposes
		print("Current time: ", currentTime)
		print("User Position: ", userPosition)
		print("CPU Usage: ", cpuUsage, "%")
		print("Memory Usage: ", memoryUsage, "%")
		print("Disk Usage: ", diskUsage, "%")

		#this is where we will insert the data into our database
		db = mysql.connector.connect(user="cpsc424", db="statsdb")
		cur= db.cursor()

		addData= ("INSERT INTO stats " "(currentTime, userPosition, cpuUsage, memoryUsage, diskUsage) "
				   "VALUES (%(currentTime)s, %(userPosition)s, %(cpuUsage)s, %(memoryUsage)s, %(diskUsage)s)")
		cur.execute(addData)
		db.commit()
		cur.close()
	conn.close()