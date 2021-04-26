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
	self.__RFData.append(str(lat).encode("hex"))
	self.__RFData.append(str(long).encode("hex"))
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
	for i, data in enumerate(self.__RFData):
	    if (i == 1):
		self.__formattedList.append(int("$".encode("hex"), 16))
	    for index in range(0, len(data), 2):
		self.__formattedList.append(int(data[index:index+2], 16))
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


def parseTx(packet):
    for byte in packet:
        if (byte == 0x7E):
            lengthVector = [packet[1], packet[2]]
	    print(lengthVector)
            length = lengthVector[1] + 3
	    print(length)
            remainder = packet[3:length]
	    print(BytesToHex(remainder))
            RFData = remainder[14:length]
	    print(BytesToHex(RFData))

