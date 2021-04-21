#Author: Adam Walker
#Python: v2.7.0
#Date: 2/8/2020
#Version: 1.0

import serial  # Allows for read from the serial port
import logging # Allows for logging of data

class Location:

    def __init__(self):
    	self.ser = serial.Serial("/dev/serial0", baudrate = 9600, timeout = 0.5)
	self.lon = -11220.90409
	self.lat = 3436.4572


    def updateDictionary(self): # Updates the current_location dictionary with the correct NMEA sentence (GNRMC)
     	data = self.ser.readline()
	latlong = [0.0, 0,0]
        if data[0:6] == "$GNRMC":
            sdata = data.split(",")
	    if (sdata[3] == ""):
		sdata[3] = "3514.792004"
	    if (sdata[5] == ""):
		sdata[5] = "-11645.999654"
	    sdata[3] = float(sdata[3])
	    sdata[5] = float(sdata[5])
	    if sdata[4] == 'S': # n/s
	        sdata[3] = -(sdata[3])
	    if sdata[6] == 'W': # e/w
	        sdata[5] = -(sdata[5])
            self.lat = sdata[3] #latitude
            self.lon = sdata[5] #longitute


    def getLat(self):
        return self.lat

    def getLong(self):
	return self.lon

    def setLong(self, data):
	self.lon = data

    def setLat(self, data):
	self.lat = data

