import XBee.spi
import spidev
import GPS.position as position
import IMU.data
import time
from threading import Thread

NUMBER_OF_THREADS = 4
NUMBER_OF_OTHER_XBEE = 1
SPI = 0
# [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0x9E],
ADDRESS_TABLE = [
		 #[0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0xD0],
		 [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA5, 0x17]
		]

DATA_OUT = [[0.0, 0.0]] # for one xbee
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


def writeXBee(thread, spidevXBee, location):
    global thread3setup, ADDRESS_TABLE, NUMBER_OF_OTHER_XBEE
    thread3setup = True
    while True:
	for address in range(NUMBER_OF_OTHER_XBEE):
	    TxPacket = XBee.spi.TxPacket(location.getLat(),
					    location.getLong(),
					    ADDRESS_TABLE[address])
	    TxPacket.createList()
	    spidevXBee.xfer2(TxPacket.getList())


def readXBee(thread, spidevXBee):
    global thread4setup, XBEE, NUMBER_OF_OTHER_XBEE
    thread4setup = True
    while True:
        if (XBee.spi.BytesToHex(spidevXBee.readbytes(1)) == "0x7E"):
	    lengthVector = spidevXBee.readbytes(2)
	    length = lengthVector[1]
	    remainder = (spidevXBee.readbytes(length - 1))
	    address = remainder[1:9]
	    RFData = remainder[12:length]
	    half = 0
	    lat = ""
	    long = ""
	    for index, data in enumerate(RFData):
		if (hex(data)[2:4].decode("hex") == "$"):
		    half = index
	    for index, byte in enumerate(RFData):
		if index < half:
		    lat = lat + hex(byte)[2:4].decode("hex")
		if index > half:
		    long = long + hex(byte)[2:4].decode("hex")
	    for xbee in range(NUMBER_OF_OTHER_XBEE):
		if (XBEE[xbee][0] == address):
		    XBEE[xbee][1].setLat(IMU.data.DMtoDD(float(lat)))
		    XBEE[xbee][1].setLong(IMU.data.DMtoDD(float(long)))


def main():
    # Initializations
    global XBEE, NUMBER_OF_OTHER_XBEE, ADDRESS_TABLE, DATA_OUT, SPI

    # location initializations
    location = position.Location() # Initialize location class

    # IMU initializations
    data = IMU.data.IMUdata()
    for xbee in range(NUMBER_OF_OTHER_XBEE):
	XBEE.append([ADDRESS_TABLE[xbee], position.Location()])
    localHeading = 0.0

    # SPI initializations
    SPI = spidev.SpiDev(0,0)
    XBee.spi.__init__(SPI)


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
    print("Starting Thread 3...")
    t = Thread(target = writeXBee, args=(3, SPI, location))
    t.daemon = True
    threads.append(t)
    t.start()
    while (not thread3setup):
    	pass
    print("Thread 3 Started")

    # Thread 4
    print("Starting Thread 4...")
    t = Thread(target = readXBee, args=(4, SPI))
    t.daemon = True
    threads.append(t)
    t.start()
    while (not thread4setup):
        pass
    print("Thread 4 Started")

    # Main Loop
    while True:
        #print("Distance: " + str(data.getDistance()))
	#print("Heading: " + str(data.getHeading()))
	#print("Lat: " + str(location.getLat()))
	#print("Long: " + str(location.getLong()))
	#print(DATA_OUT)
	time.sleep(1)
	pass
    return 0


if __name__ == '__main__':
    main()
