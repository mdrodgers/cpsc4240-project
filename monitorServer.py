#!/usr/bin/env python
import socket
import mysql.connector
from datetime import date
import sys
import getpass
import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES 

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()
        

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


#temp localhost ip for testing
if len(sys.argv) < 5:
	print("Usage ./monitorServer <port> -u <user> -p")
	quit()
mPass= getpass.getpass()


username= sys.argv[3]
udpIP = "127.0.0.1"
udpPort = int(sys.argv[1])
#set up the tcp socket and bind, wait for incoming connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
sock.bind((udpIP, udpPort))
sock.listen(1) 

#continually listen for new data
while 1:
	mAES= AESCipher(mPass)
	#accept new connections and print ip address
	conn, addr = sock.accept()
	print("New connection from %s" % addr[0])
	try:
		db = mysql.connector.connect(user=username, password=mPass, db="statsdb")
		
	except Exception, e:
		print("Incorrect MySQL password. Exiting.")
		exit()
	cur= db.cursor(buffered=True)
	#find the largest ID so far, set to 1 larger
	query= ("SELECT MAX(id),ip FROM stats")
	
	cur.execute(query)
	row=cur.fetchone()
	if row != None:
		id=row[0]+1
	
	id=str(id)
	sendData=mAES.encrypt(id)
	conn.send(sendData)

	#reset cipher
	mAES= AESCipher(mPass)
	#recv and decode the data 
	recvData = conn.recv(1024)
	data=mAES.decrypt(recvData)
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
