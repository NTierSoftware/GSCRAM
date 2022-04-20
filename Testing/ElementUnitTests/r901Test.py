# r901Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/6/2018

from CRAMmsg.unusedCRAMmsg.r901LinkInit import r901LinkInit
from CRAMmsg.unusedCRAMmsg.r901LinkInit import r901Consts
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.Header import HeaderConsts

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 76
MSG_ID = 901
KIND = HeaderConsts.InterfaceKind.AI3.value.data # 0x00
PART_COUNT = 2

FCR_ID_A = 0xE2
FCR_IP_FORMAT_A = r901Consts.FCR_IP_Format.IPV6_FORMAT.value.data
FCR_IP_ADDRESS_A = 0x20010DB8AC10FE010000000000000000

FCR_ID_B = 0x48
FCR_IP_FORMAT_B = r901Consts.FCR_IP_Format.IPV4_FORMAT.value.data
FCR_IP_ADDRESS_B = 0x12ABFE09
FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x4C, 0x03, 0x85, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE2, 0x01,
                   0x20, 0x01, 0x0D, 0xB8, 0xAC, 0x10, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x12, 0xAB, 0xFE, 0x09])


def run901Test():
    test901JSONSimple()
    test901FromBytes()
    test901ToBytes()
    test901Reverse()
    print("901 Link Initialization: PASS")


def test901JSONSimple():
    msg = r901LinkInit([FCR_ID_A, FCR_ID_B], [FCR_IP_FORMAT_A, FCR_IP_FORMAT_B], [FCR_IP_ADDRESS_A, FCR_IP_ADDRESS_B])
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test901ToBytes():
    msg = r901LinkInit([FCR_ID_A, FCR_ID_B], [FCR_IP_FORMAT_A, FCR_IP_FORMAT_B], [FCR_IP_ADDRESS_A, FCR_IP_ADDRESS_B])
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r901 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r901 toBytes'


def test901FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r901 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r901 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r901 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r901 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r901 fromBytes'
    
    assert msg.fcrIds[0].data == FCR_ID_A, 'First FCR ID wrong: r901 fromBytes'
    assert msg.fcrIpFormats[0].data == FCR_IP_FORMAT_A, 'First FCR IP Format wrong: r901 fromBytes'
    assert msg.fcrIpAddresses[0].data == FCR_IP_ADDRESS_A, 'First FCR IP ADDRESS wrong: r901 fromBytes'
    assert msg.fcrIds[1].data == FCR_ID_B, 'Second FCR ID wrong: r901 fromBytes'
    assert msg.fcrIpFormats[1].data == FCR_IP_FORMAT_B, 'Second FCR IP Format wrong: r901 fromBytes'
    assert msg.fcrIpAddresses[1].data == FCR_IP_ADDRESS_B, 'Second FCR IP Address wrong: r901 fromBytes'


def test901Reverse():
    msg = r901LinkInit([FCR_ID_A, FCR_ID_B], [FCR_IP_FORMAT_A, FCR_IP_FORMAT_B], [FCR_IP_ADDRESS_A, FCR_IP_ADDRESS_B])
    byteList = msg.getByteArray()
    msg2 = getMessageFromBytes(byteList)
    assert msg.header.messageLength.data == msg2.header.messageLength.data, 'Invalid inverse: r901'
    assert msg.header.messageId.data == msg2.header.messageId.data, 'Invalid inverse: r901'
    assert msg.header.interfaceKind.data == msg2.header.interfaceKind.data, 'Invalid inverse: r901'
    assert msg.header.partCount.data == msg2.header.partCount.data, 'Invalid inverse: r901'
    assert msg.header.transmitTime.data == msg2.header.transmitTime.data, 'Invalid inverse: r901'
    
    assert msg.fcrIds[0].data == msg2.fcrIds[0].data, 'Invalid inverse: r901'
    assert msg.fcrIpFormats[0].data == msg2.fcrIpFormats[0].data, 'Invalid inverse:r901'
    assert msg.fcrIpAddresses[0].data == msg2.fcrIpAddresses[0].data, 'Invalid inverse:r901'
    assert msg.fcrIds[1].data == msg2.fcrIds[1].data, 'Invalid inverse:r901'
    assert msg.fcrIpFormats[1].data == msg2.fcrIpFormats[1].data, 'Invalid inverse:r901'
    assert msg.fcrIpAddresses[1].data == msg2.fcrIpAddresses[1].data, 'Invalid inverse:r901'

