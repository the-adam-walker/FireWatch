import XBee.spi
import spidev
import GPS.position as position
import IMU.data
import time
from threading import Thread

NUMBER_OF_THREADS = 4
NUMBER_OF_OTHER_XBEE = 2

# [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0x9E],
ADDRESS_TABLE = [
		 [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0xD0],
		 [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA5, 0x17]
		]

DATA_OUT = [[0.0, 0.0], [0.0, 0.0]]
XBEE = []

thread1setup = False
thread2setup = False
thread3setup = False
thread4setup = False


def updateIMU(thread, location, data):
    global thread1setup, NUMBER_OF_OTHER_XBEE, XBEE
    thread1setup = True
    while True:
	#-112.348769
	#34.607282
	for xbee in range(NUMBER_OF_OTHER_XBEE):
            data.setHeading(IMU.data.calcHeading(IMU.data.getLocalHeading(),
                                                XBEE[xbee][1].getLong(),
                                                XBEE[xbee][1].getLat(),
                                                IMU.data.DMtoDD(location.getLong()),
                                                IMU.data.DMtoDD(location.getLat())))

            data.setDistance(IMU.data.calcDist(XBEE[xbee][1].getLong(),
                                                XBEE[xbee][1].getLat(),
                                                IMU.data.DMtoDD(location.getLong()),
                                                IMU.data.DMtoDD(location.getLat())))

	    DATA_OUT[xbee][0] = data.getHeading()
	    DATA_OUT[xbee][1] = data.getDistance()


def updateGPS(thread, location):
    global thread2setup
    thread2setup = True
    while True:
	location.updateDictionary()


def writeXBee(thread, spidevXBee):
    global thread3setup, ADDRESS_TABLE, NUMBER_OF_OTHER_XBEE
    thread3setup = True
    while True:
	for address in range(len(NUMBER_OF_OTHER_XBEE)):
	    TxPacket = XBee.spi.TxPacket(location.getLat(),
					    location.getLong(),
					    ADDRESS_TABLE[address])
	    TxPacket.createList()
	    spidevXBee.xfer2(TxPacket.getList())
	    sleep(1)


def readXBee(thread, spidevXBee):
    global thread4setup, XBEE, NUMBER_OF_OTHER_XBEE
    thread4setup = True
    while True:
	if (spidevXBee.readbytes(1) == 0x7E):
	    lengthVector = spidevXBee.readbytes(2)
	    length = lengthVector[1] + 3
	    remainder = XBee.spi.BytesToHex(spidevXBee.readbytes(length))
	    address = remainder[1:9]
	    RFData = remainder[12:length]
	    half = len(RFData) / 2
	    lat = RFData[:half]
	    long = RFData[half:]
	    for xbee in range(NUMBER_OF_OTHER_XBEE):
		if (XBEE[xbee][0] == address):
		    XBEE[xbee][1].setLat(lat)
		    XBEE[xbee][1].setLong(long)


def main():
    # Initializations
    global XBEE, NUMBER_OF_OTHER_XBEE, ADDRESS_TABLE

    # location initializations
    location = position.Location() # Initialize location class

    # IMU initializations
    data = IMU.data.IMUdata()
    for xbee in range(NUMBER_OF_OTHER_XBEE):
	XBEE.append([ADDRESS_TABLE[xbee], position.Location()])
    localHeading = 0.0

    # SPI initializations
    spidevXBee = spidev.SpiDev(0,0)
    XBee.spi.__init__(spidevXBee)


    # Thread Initialization
    threads = []

    # Thread 1
    print("Starting Thread 1...")
    t = Thread(target = updateIMU, args=(1, location, data))
    t.daemon = True
    threads.append(t)
    t.start()
    while (not thread1setup):
	pass
    print("Thread 1 Started")

    # Thread 2
    print("Starting Thread 2...")
    t = Thread(target = updateGPS, args=(2, location))
    t.daemon = True
    threads.append(t)
    t.start()
    while (not thread2setup):
	pass
    print("Thread 2 Started")

    # Thread 3
    #print("Starting Thread 3...")
    #t = Thread(target = writeXBee, args=(3))
    #t.daemon = True
    #threads.append(t)
    #t.start()
    #while (not thread3setup):
    #	pass
    #print("Thread 3 Started")

    # Thread 4
    #print("Starting Thread 4...")
    #t = Thread(targer = readXBee, args=(4))
    #t.daemon = true
    #threads.append(t)
    #t.start()
    #while (not thread4setup):
    #    pass
    #print("Thread 4 Started")

    # Main Loop
    while True:
        print("Distance: " + str(data.getDistance()))
	print("Heading: " + str(data.getHeading()))
	#print("Lat: " + str(location.getLat()))
	#print("Long: " + str(location.getLong()))
	time.sleep(1)

    return 0


if __name__ == '__main__':
    main()
