import spidev
import time
import struct

class TxPacket:
    def __init__(self, lat, long, LongBitAddress):
	self.__delimiter = 0x7E
	self.__length = []
	self.__length.append(0x00)
	self.__length.append(0x22)
	self.__frameType = 0x10
	self.__frameID = 0x01
	self.__longBitAddress = []
	for byte in LongBitAddress:
	    self.__longBitAddress.append(byte)
	self.__shortBitAddress = []
	self.__shortBitAddress.append(0xFF)
	self.__shortBitAddress.append(0xFE)
	self.__broadcastRadius = 0x00
	self.__options = 0x00
	self.__RFData = []
	self.__RFData.append(float_to_hex(lat))
	self.__RFData.append(float_to_hex(long))
	self.__checksum = 0x00
	self.__formattedList = []

    def createList(self):
	self.__formattedList.append(self.__delimiter)
	for byte in self.__length:
	    self.__formattedList.append(byte)
	self.__formattedList.append(self.__frameType)
	self.__formattedList.append(self.__frameID)
	for byte in self.__longBitAddress:
	    self.__formattedList.append(byte)
	for byte in self.__shortBitAddress:
	    self.__formattedList.append(byte)
	self.__formattedList.append(self.__broadcastRadius)
	self.__formattedList.append(self.__options)
	for byte in self.__RFData:
	    byte = byte[2:]
	    for index in range(0, len(byte), 2):
		self.__formattedList.append(int(byte[index:index+2], 16))
	self.__formattedList[2] = int(hex(len(self.__formattedList) - 2), 16);
	self.__formattedList.append(calcChecksum(self.__formattedList))


    def readPacket(self):
	for byte in self.__formattedList:
	    readBytes(byte)
	print(self.__formattedList)

    def getList(self):
        return self.__formattedList


def __init__(spi):
    spi.mode = 0b00
    spi.max_speed_hz = 5000
    spi.bits_per_word = 8
    spi.loop = False
    spi.cshigh = True
    spi.lsbfirst = False
    spi.threewire = False


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def calcChecksum(data):
    checksum = 0
    data = data[3:]
    for byte in data:
	checksum += byte
    strChecksum = toHex(checksum)
    strChecksum = strChecksum[1:]
    return (0xFF - int(strChecksum, 16))


def readBytes(byte):
    print(''.join("0x{:02X}".format(byte)))


def toHex(byte):
    return ''.join("{:02X}".format(byte))


def BytesToHex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()


def parseTx():
    if (XBee.spi.BytesToHex(spidevXBee.readbytes(1)) == '0x7E'):
            lengthVector = XBee.spi.BytesToHex(spidevXBee.readbytes(2))
            length = int(lengthVector[1], 16)
            remainder = XBee.spi.BytesToHex(spidevXBee.readbytes(length))
            RFData = remainder[14:length]

def main():
    spi = spidev.SpiDev(0,0)
    __init__(spi)
    packet = TxPacket(123.123, 123.123,
		      [0x00, 0x13, 0xA2, 0x00, 0x41, 0x9A, 0xA4, 0x9E])
    packet.createList()
    packet.readPacket()
#    spi.xfer2(packet.getList())
#    spi.xfer2([0x7E, 0x00, 0x1A, 0x10, 0x01, 0x00, 0x13, 0xA2,
#	       0x00, 0x41, 0x9A, 0xA4, 0x9E, 0xFF, 0xFE, 0x00,
#               0x00, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57,
#               0x6F, 0x72, 0x6C, 0x64, 0x21, 0xE2])
#    while True:
#       read = BytesToHex(spi.readbytes(1))
#       print(read)
#       time.sleep(0.5)
    spi.close()


if __name__ == '__main__':
    main()
