#!/usr/bin/env python
import requests 
import json
import psutil
from datetime import datetime
import socket
import time 
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


id=0

if len(sys.argv) < 4:
	print("Usage ./monitor IP port -p")
	quit()
tcpIP=sys.argv[1]
tcpPort=int(sys.argv[2])
mPass= getpass.getpass()

#continually send computer stats (every 15 seconds)
while 1:
	#create new AES cipher
	mAES= AESCipher(mPass)
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
	data=sock.recv(1024)
	newId=mAES.decrypt(data)
	if id == 0:
		id=newId
	#concat message with | as the delimiter
	message= str(id) + "|" + str(currentTime) + "|" + str(userPostition) + "|" +str(cpuUsage) + "|" + str(memoryUsage) + "|" +str(diskUsage)
	#encrypt the bytes and send
	sendData= mAES.encrypt(message)
	sock.send(sendData)

	#print the data we sent
	print(currentTime)
	print(userPostition)
	print(cpuUsage)
	print(memoryUsage)
	print(diskUsage)

	#sleep for 15 seconds
	time.sleep(5)
