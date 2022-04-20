# rt922Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/6/2018

from CRAMmsg.rt922MeteorologicalData import rt922MeteorlogicalData
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 36
MSG_ID = 922
KIND = 0
PART_COUNT = 0

AMBIENT_TEMP = -1000 # 0xFC18
WIND_SPEED = 20 # 0x0014
WIND_DIR = 0x1000
ABS_ATM_P = 0x0F03
FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x24, 0x03, 0x9A, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0xFC, 0x18, 0x00, 0x14, 0x10, 0x00, 0x0F, 0x03, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def run922Test():
    test922JSONSimple()
    test922FromBytes()
    test922ToBytes()
    test922Reverse()
    print("922 Meteorological Data: PASS")


def test922JSONSimple():
    msg = rt922MeteorlogicalData(AMBIENT_TEMP, WIND_SPEED, WIND_DIR, ABS_ATM_P)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test922ToBytes():
    msg = rt922MeteorlogicalData(AMBIENT_TEMP, WIND_SPEED, WIND_DIR, ABS_ATM_P)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): rt922 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: rt922 toBytes'
    
def test922FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: rt922 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: rt922 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: rt922 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: rt922 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: rt922 fromBytes'
    
    assert msg.ambientTemp.data == AMBIENT_TEMP, 'Ambient Temperature wrong: rt922 fromBytes'
    assert msg.windSpd.data == WIND_SPEED, 'Wind Speed wrong: rt922 fromBytes'
    assert msg.windDir.data == WIND_DIR, 'Wind Direction wrong: rt922 fromBytes'
    assert msg.absAtmPressure.data == ABS_ATM_P, 'Absolute Atmospheric Pressure wrong: rt922 fromBytes'

def test922Reverse():
    msg = rt922MeteorlogicalData(AMBIENT_TEMP, WIND_SPEED, WIND_DIR, ABS_ATM_P)
    byteList = msg.getByteArray()
    msg2 = getMessageFromBytes(byteList)
    assert msg.header.messageLength.data == msg2.header.messageLength.data, 'Invalid inverse: rt922'
    assert msg.header.messageId.data == msg2.header.messageId.data, 'Invalid inverse: rt922'
    assert msg.header.interfaceKind.data == msg2.header.interfaceKind.data, 'Invalid inverse: rt922'
    assert msg.header.partCount.data == msg2.header.partCount.data, 'Invalid inverse: rt922'
    assert msg.header.transmitTime.data == msg2.header.transmitTime.data, 'Invalid inverse: rt922'
    
    assert msg.ambientTemp.data == msg2.ambientTemp.data, 'Invalid inverse: rt922'
    assert msg.windSpd.data == msg2.windSpd.data, 'Invalid inverse:rt922'
    assert msg.windDir.data == msg2.windDir.data, 'Invalid inverse:rt922'
    assert msg.absAtmPressure.data == msg2.absAtmPressure.data, 'Invalid inverse:rt922'
