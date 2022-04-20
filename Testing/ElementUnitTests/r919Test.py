# r919Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/16/2018

from CRAMmsg.unusedCRAMmsg.r919InventoryManagement import r919InventoryManagement
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 28
MSG_ID = 919
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0x2468
FIRING_UNIT_ID = 0x1357
MISSILES_READY = 0x9131
INTERCEPTOR_KIND = 0x07
# uint8 spare
# uint32 spare
# uint32 spare


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x1C, 0x03, 0x97, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x24, 0x68, 0x13, 0x57, 0x91, 0x31, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00])


def run919Test():
    test919JSONSimple()
    test919FromBytes()
    test919ToBytes()
    print('919 Inventory Management: PASS')


def test919JSONSimple():
    msg = r919InventoryManagement(WEAPON_ID, FIRING_UNIT_ID, MISSILES_READY, INTERCEPTOR_KIND)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: r919'


def test919ToBytes():
    msg = r919InventoryManagement(WEAPON_ID, FIRING_UNIT_ID, MISSILES_READY, INTERCEPTOR_KIND)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r919 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r919 toBytes'


def test919FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r919 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r919 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r919 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r919 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r919 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: r919 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID, 'Firing Unit ID wrong: r919 fromBytes'
    assert msg.missilesReady.data == MISSILES_READY, 'Missiles Ready wrong: r919 fromBytes'
    assert msg.interceptorKind.data == INTERCEPTOR_KIND, 'drone Kind wrong: r919 fromBytes'
