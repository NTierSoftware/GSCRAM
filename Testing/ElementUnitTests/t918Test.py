# t918Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/8/2018

from CRAMmsg.unusedCRAMmsg.t918FCRStatus import t918FCRStatus
from CRAMmsg.unusedCRAMmsg.t918FCRStatus import t918Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 28
MSG_ID = 918
KIND = 0
PART_COUNT = 2

WEAPON_ID = 0x8910
FCR_IDS = [0x24, 0x73]
LINK_STATUSES = [t918Consts.LinkStatus.NO_STATEMENT.value, t918Consts.LinkStatus.OPERATIONAL.value]  # [0x00, 0x01]

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x1C, 0x03, 0x96, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x89, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00,
                   0x73, 0x01, 0x00, 0x00])


def run918Test():
    test918JSONSimple()
    test918FromBytes()
    test918ToBytes()
    print("918 Fire Control Radar Status: PASS")


def test918JSONSimple():
    msg = t918FCRStatus(WEAPON_ID, FCR_IDS, LINK_STATUSES)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test918ToBytes():
    msg = t918FCRStatus(WEAPON_ID, FCR_IDS, LINK_STATUSES)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t918 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t918 toBytes'


def test918FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t918 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t918 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t918 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t918 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t918 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t918 fromBytes'
    assert msg.fcrIds[0].data == FCR_IDS[0], 'First FCR ID wrong: t918 fromBytes'
    assert msg.linkStatuses[0].data == LINK_STATUSES[0].data, 'First Link Status wrong: t918 fromBytes'
    assert msg.fcrIds[1].data == FCR_IDS[1], 'Second FCR ID wrong: t918 fromBytes'
    assert msg.linkStatuses[1].data == LINK_STATUSES[1].data, 'Second Link Status wrong: t918 fromBytes'

