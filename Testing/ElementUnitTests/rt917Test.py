# r913Test.py
# rt917Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/16/2018

from CRAMmsg.unusedCRAMmsg.rt917Operator import rt917Operator
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 20
MSG_ID = 917
KIND = 0
PART_COUNT = 8

MSG_TEXT = 'Airspace'  # [0x41, 0x69, 0x72, 0x73, 0x70, 0x61, 0x63, 0x65]

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x14, 0x03, 0x95, 0x00, 0x08, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x41, 0x69, 0x72, 0x73, 0x70, 0x61, 0x63, 0x65])


def run917Test():
    test917JSONSimple()
    test917FromBytes()
    test917ToBytes()
    print('917 Operator: PASS')


def test917JSONSimple():
    msg = rt917Operator(MSG_TEXT)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: rt917'


def test917ToBytes():
    msg = rt917Operator(MSG_TEXT)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): rt917 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: rt917 toBytes'


def test917FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: rt917 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: rt917 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: rt917 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: rt917 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: rt917 fromBytes'

    assert msg.msgText.getDataObject() == MSG_TEXT, 'Message Text wrong: rt917 fromBytes'
