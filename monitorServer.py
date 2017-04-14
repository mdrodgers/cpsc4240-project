#!/usr/bin/env python
import socket
import mysql.connector
from datetime import date
import sys

#temp localhost ip for testing
if len(sys.argv) < 2:
	print("Usage ./monitorServer port")
	quit()
udpIP = "127.0.0.1"
udpPort = int(sys.argv[1])
#set up the tcp socket and bind, wait for incoming connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
sock.bind((udpIP, udpPort))
sock.listen(1) 

#continually listen for new data
while 1:
	#accept new connections and print ip address
	conn, addr = sock.accept()
	print("New connection from ", addr)
	db = mysql.connector.connect(user="root", password="password", db="statsdb")
	cur= db.cursor(buffered=True)
	
	#find the largest ID so far, set to 1 larger
	query= ("SELECT MAX(id),ip FROM stats")
	cur.execute(query)
	row=cur.fetchone()
	if row != None:
		id=row[0]+1
	
	id=str(id)
	conn.send(id.decode())

	while 1:
		#recv and decode the data 
		data = conn.recv(1024).decode()
		if not data:
			break
		#split the message based on the delimiter
		id= data.split("|")[0]
		currentTime= data.split("|")[1]
		userPosition=data.split("|")[2]
		cpuUsage= data.split("|")[3]
		memoryUsage= data.split("|")[4]
		diskUsage= data.split("|")[5]

		#printing for testing purposes
		print("ID: %s" % id)
		print("Current time: %s" % currentTime)
		print("User Position: %s"% userPosition)
		print("CPU Usage: %s" % cpuUsage)
		print("Memory Usage: %s" % memoryUsage)
		print("Disk Usage: %s" % diskUsage)

		#this is where we will insert the data into our database
		addData= ("INSERT INTO stats " "(id, ip, time, geolocation, cpu, memory, disk) "
				   "VALUES (%s, %s, %s, %s, %s, %s, %s)")

		currentValues= (id, addr[0], currentTime, userPosition, float(cpuUsage), float(memoryUsage), float(diskUsage))

		cur.execute(addData, currentValues)
		db.commit()
		cur.close()
	conn.close()
