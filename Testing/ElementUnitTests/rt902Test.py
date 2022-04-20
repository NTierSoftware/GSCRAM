# rt902Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/6/2018

from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.rt902WeaponHeartbeat import rt902WeaponHeartbeat
from CRAMmsg.rt902WeaponHeartbeat import rt902Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 20
MSG_ID = 902
KIND = HeaderConsts.InterfaceKind.AI3.value
PART_COUNT = 0
TIME = 0x1000
TIME2 = 0x1F02
TIME3 = 0x2AB31110

WEAPON_ID = 0xF12A
WEAPON_ID2 = 0xA1A1
IF_VERSION = rt902Consts.IFVersion.SUPPORTS_137_ICD_REV_C.value  # 0x09
IF_VERSION2 = rt902Consts.IFVersion.SUPPORTS_137_ICD_REV_A.value  #0x07
ACTION_REQ = rt902Consts.ActionRequest.WES_DATA_COLLECTION.value
ACTION_REQ2 = rt902Consts.ActionRequest.NO_STATEMENT.value

BYTES_A = bytearray([0x00, 0x00, 0x00, 0x14, 0x03, 0x86, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0xF1, 0x2A, 0x09, 0x01, 0x00, 0x00, 0x00, 0x00])
BYTES_B = bytearray([0x00, 0x00, 0x00, 0x14, 0x03, 0x86, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x02, 0xF1, 0x2A, 0x09, 0x01, 0x00, 0x00, 0x00, 0x00])

BYTES_C = bytearray([0x00, 0x00, 0x00, 0x14, 0x03, 0x86, 0x00, 0x00, 0x2A, 0xB3, 0x11, 0x10, 0xA1, 0xA1, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00])

def run902Test():
    test902JSONSimple()
    test902FromBytes()
    test902ToBytes()
    test902Reverse()
    print("902 Weapon Heartbeat: PASS")


def test902JSONSimple():
    msg = rt902WeaponHeartbeat(WEAPON_ID, IF_VERSION, ACTION_REQ)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test902ToBytes():
    testHeader = Header(MSG_LENGTH, MSG_ID, KIND, PART_COUNT, TIME)
    msg = rt902WeaponHeartbeat(WEAPON_ID, IF_VERSION, ACTION_REQ, testHeader)
    assert msg.getByteArray() == BYTES_A, 'First byte array failed: rt902 toBytes'
    
    msg = rt902WeaponHeartbeat(WEAPON_ID, IF_VERSION, ACTION_REQ)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): rt902 toBytes'
    msg.header.transmitTime = ElementUInt32(TIME2)
    assert msg.getByteArray() == BYTES_B, 'Second byte array failed: rt902 toBytes'


def test902FromBytes():
    msg = getMessageFromBytes(BYTES_C)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: rt902 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: rt902 fromBytes'
    assert msg.header.interfaceKind.data == KIND.data, 'Interface Kind wrong: rt902 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: rt902 fromBytes'
    assert msg.header.transmitTime.data == TIME3, 'Transmit Time wrong: rt902 fromBytes'
    
    assert msg.weaponId.data == WEAPON_ID2, 'Weapon ID wrong: rt902 fromBytes'
    assert msg.IFVersion.data == IF_VERSION2.data, 'IF Version wrong: rt902 fromBytes'
    assert msg.actionRequest.data == ACTION_REQ2.data, 'Action Request wrong: rt902 fromBytes'
    return

def test902Reverse():
    msg = rt902WeaponHeartbeat(WEAPON_ID, IF_VERSION, ACTION_REQ)
    byteList = msg.getByteArray()
    msg2 = getMessageFromBytes(byteList)
    assert msg.header.messageLength.data == msg2.header.messageLength.data, 'Invalid inverse: rt902'
    assert msg.header.messageId.data == msg2.header.messageId.data, 'Invalid inverse: rt902'
    assert msg.header.interfaceKind.data == msg2.header.interfaceKind.data, 'Invalid inverse: rt902'
    assert msg.header.partCount.data == msg2.header.partCount.data, 'Invalid inverse: rt902'
    assert msg.header.transmitTime.data == msg2.header.transmitTime.data, 'Invalid inverse: rt902'
    assert msg.weaponId.data == msg2.weaponId.data, 'Invalid inverse: rt902'
    assert msg.IFVersion.data == msg2.IFVersion.data, 'Invalid inverse:rt902'
    assert msg.actionRequest.data == msg.actionRequest.data, 'Invalid inverse: rt902'

