# rt915Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/7/2018

from CRAMmsg.rt915NetTime import rt915NetTime
from CRAMmsg.rt915NetTime import rt915Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 40
MSG_ID = 915
KIND = 0
PART_COUNT = 0

MESSAGE_TYPE_A = rt915Consts.msgType.REQUEST.value.data  # 0x00
WEAPON_ID_A = 0x771D
REQUEST_TIME_A = 0xABCDEF01
RECEIPT_TIME_A = 0x00000000
RESPONSE_TIME_A = 0x00000000

MESSAGE_TYPE_B = rt915Consts.msgType.RESPONSE.value.data  # 0x01
WEAPON_ID_B = 0x771D
REQUEST_TIME_B = 0xABCDEF01
RECEIPT_TIME_B = 0xBBBBBB61
RESPONSE_TIME_B = 0xCBBBE212

FAKE_TIME = 0xCCCCCCCC

BYTES_A = bytearray([0x00, 0x00, 0x00, 0x28, 0x03, 0x93, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x00, 0x00, 0x77, 0x1D, 0xAB, 0xCD, 0xEF, 0x01, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00])

BYTES_B = bytearray([0x00, 0x00, 0x00, 0x28, 0x03, 0x93, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x01, 0x00, 0x77, 0x1D, 0xAB, 0xCD, 0xEF, 0x01, 0xBB, 0xBB, 0xBB, 0x61,
                     0xCB, 0xBB, 0xE2, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00])


def run915Test():
    test915JSONSimple()
    test915_getNumBytes()
    test915FromBytes()
    test915ToBytes()
    print("915 Network Time Performance: PASS")


def test915JSONSimple():
    msg = rt915NetTime(MESSAGE_TYPE_A, WEAPON_ID_A, REQUEST_TIME_A, RECEIPT_TIME_A, RESPONSE_TIME_A)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test915_getNumBytes():
    msg1 = getMessageFromBytes(BYTES_A)
    assert msg1.getNumBytes() == MSG_LENGTH, 'First getNumBytes failed: rt915'
    msg2 = rt915NetTime(MESSAGE_TYPE_A, WEAPON_ID_A, REQUEST_TIME_A, RECEIPT_TIME_A, RESPONSE_TIME_A)
    assert msg2.getNumBytes() == MSG_LENGTH, 'Second getNumBytes failed: rt915'
    msg3 = getMessageFromBytes(BYTES_B)
    assert msg3.getNumBytes() == MSG_LENGTH, 'Third getNumBytes failed: rt915'
    msg4 = rt915NetTime(MESSAGE_TYPE_B, WEAPON_ID_B, REQUEST_TIME_B, RECEIPT_TIME_B, RESPONSE_TIME_B)
    assert msg4.getNumBytes() == MSG_LENGTH, 'Fourth getNumBytes failed: rt915'


def test915ToBytes():
    msg1 = rt915NetTime(MESSAGE_TYPE_A, WEAPON_ID_A, REQUEST_TIME_A, RECEIPT_TIME_A, RESPONSE_TIME_A)
    assert msg1.header.transmitTime.data + 5000 > millisSinceMidnight(), 'First transmit time way off (>5 seconds): rt915 toBytes'
    msg1.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg1.getByteArray() == BYTES_A, 'First byte array failed: rt915 toBytes'

    msg2 = rt915NetTime(MESSAGE_TYPE_B, WEAPON_ID_B, REQUEST_TIME_B, RECEIPT_TIME_B, RESPONSE_TIME_B)
    assert msg2.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Second transmit time way off (>5 seconds): rt915 toBytes'
    msg2.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg2.getByteArray() == BYTES_B, 'Second byte array failed: rt915 toBytes'


def test915FromBytes():
    msg = getMessageFromBytes(BYTES_A)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: rt915 fromBytes'

    '''
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: rt902 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: rt902 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: rt902 fromBytes'
    assert msg.header.transmitTime.data == TIME3, 'Transmit Time wrong: rt902 fromBytes'

    assert msg.weaponId.data == WEAPON_ID2, 'Weapon ID wrong: rt902 fromBytes'
    assert msg.IFVersion.data == IF_VERSION2.data, 'IF Version wrong: rt902 fromBytes'
    return
    '''

