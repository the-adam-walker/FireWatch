import math
import time
import IMU

M_PI = 3.14159265358979323846

class IMUdata:

    def __init__(self):
        IMU.detectIMU()
	IMU.initIMU()
	self.heading = 0
	self.distance = 0

    def getHeading(self):
	return self.heading

    def getDistance(self):
	return self.distance

    def setDistance(self, distance):
	self.distance = distance

    def setHeading(self, heading):
	self.heading = heading


def getLocalHeading():

    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    #Normalize accelerometer raw values.
    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    #Calculate pitch and roll
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm/math.cos(pitch))

    #X compensation
    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2$
        magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
    else:                                                                #LSM9DS1
        magXcomp = MAGx*math.cos(pitch)-MAGz*math.sin(pitch)

    #Y compensation
    if(IMU.BerryIMUversion == 1 or IMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2$
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)
    else:                                                                #LSM9DS1
        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)

    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360

    return tiltCompensatedHeading


def DMtoDD(number):

    strNumber = str(number)
    x = strNumber.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:] + "." + tail
    dd = float(deg) + float(min)/60
    dd = float(format(dd, '.6f'))
    return dd


def calcDist(oLong, oLat, lLong, lLat):

    dlat = oLat - lLat
    dlong = oLong - lLong
    a = (math.sin(dlat/2)**2) + (math.cos(lLat)*math.cos(oLat)*(math.sin(dlong/2)**2))
    c = 2*math.atan(math.radians(math.sqrt(a)/math.sqrt(1-a)))
    d = c * 6371
    return float(format(d * 1000, '.3f'))


def calcHeading(heading, oLong, oLat, lLong, lLat):

    long = oLong - lLong
    lat = oLat - lLat

    if (long == 0 and lat == 0):
	return 0

    if (long == 0 and lat > 0): # directly north of us
	return -heading
    elif (long == 0 and lat < 0): #directly south of us
	return (180 - heading)
    elif (long > 0 and lat == 0): # directly east of us
	return (90 - heading)
    elif (long < 0 and lat == 0): # directly west of us
	return (270 - h)
    else:
	return quadrantHeading(heading, lat, long)

def quadrantHeading(heading, lat, long):

    angleOfOther = math.degrees(math.atan(abs(lat)/abs(long)))

    if (long > 0 and lat < 0): # southeast
	return (180 - angleOfOther - heading)
    elif (long > 0 and lat > 0): # northeast
	return (angleOfOther - heading)
    elif (long < 0 and lat > 0): # northwest
	return (360 - angleOfOther - heading)
    elif (long < 0 and lat < 0): # southwest
	return (180 + angleOfOther - heading)
    else:
	return 404


