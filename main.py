import XBee.spi
import spidev
import GPS.position as position
import IMU.data
import time
from threading import Thread

NUMBER_OF_THREADS = 10
NUMBER_OF_OTHER_XBEE = 2

ADDRESS_TABLE = [
		 [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0x9E],
		 [0x00, 0x13, 0xA2, 0x00]
		]

thread1setup = False
thread2setup = False
thread3setup = False
thread4setup = False


def updateIMU(thread, location, data):
    global thread1setup
    thread1setup = True
    while True:
        data.setHeading(IMU.data.calcHeading(IMU.data.getLocalHeading(),
                                            -112.348769,
                                            34.607282,
                                            IMU.data.DMtoDD(location.getLong()),
                                            IMU.data.DMtoDD(location.getLat())))

        data.setDistance(IMU.data.calcDist(-112.348769,
                                            34.607282,
                                            IMU.data.DMtoDD(location.getLong()),
                                            IMU.data.DMtoDD(location.getLat())))


def updateGPS(thread, location):
    global thread2setup
    thread2setup = True
    while True:
	location.updateDictionary()


def writeXBee(thread, spidevXBee):
    global thread3setup
    thread3setup = True
    address = [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0x9E]
    while True:
	TxPacket = XBee.spi.TxPacket(location.getLat(),
					location.getLong(),
					address)
	TxPacket.createList()
	spidevXBee.xfer2(TxPacket.getList())
	sleep(1)


def readXBee(thread, spidevXBee):
    global thread4setup
    thread4setup = True
    while True:
	if (XBee.spi.BytesToHex(spidevXBee.readbytes(1)) == '0x7E'):
	    lengthVector = XBee.spi.BytesToHex(spidevXBee.readbytes(2))
	    length = int(lengthVector[1], 16)
	    remainder = XBee.spi.BytesToHex(spidevXBee.readbytes(length))
	    RFData = remainder[14:length]

def main():
    # Initializations

    # location initializations
    location = position.Location() # Initialize location class

    # IMU initializations
    data = IMU.data.IMUdata()
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
	time.sleep(1)

    return 0


if __name__ == '__main__':
    main()
