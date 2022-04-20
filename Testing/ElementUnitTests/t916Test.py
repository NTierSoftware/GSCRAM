# t916Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/17/2018

from CRAMmsg.unusedCRAMmsg.t916WeaponNoFireSectors import t916WeaponNoFireSectors
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.Header import HeaderConsts

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 48
MSG_ID = 916
KIND = HeaderConsts.InterfaceKind.AI3.value.data  # 0x00
PART_COUNT = 2

WEAPON_ID = 0x3280
FIRING_UNIT_ID = 0x4291
AZIMUTHS = [0x3344, 0x8102]
HALF_SECTOR_WIDTHS = [0x88, 0x14]
AZIMUTH_RATES = [-64, -97]  # [0xC0, 0x9F]
ELEVATIONS = [2012, -373]  # [0x07DC, 0xFE8B]
# uint16 spares
# uint32 spares
# uint32 spares

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x30, 0x03, 0x94, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x32, 0x80, 0x42, 0x91, 0x33, 0x44, 0x88, 0xC0, 0x07, 0xDC, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x81, 0x02, 0x14, 0x9F,
                   0xFE, 0x8B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def run916Test():
    test916JSONSimple()
    test916FromBytes()
    test916ToBytes()
    print("916 Weapon No Fire Sectors: PASS")


def test916JSONSimple():
    msg = t916WeaponNoFireSectors(WEAPON_ID, FIRING_UNIT_ID, AZIMUTHS, HALF_SECTOR_WIDTHS, AZIMUTH_RATES, ELEVATIONS)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test916ToBytes():
    msg = t916WeaponNoFireSectors(WEAPON_ID, FIRING_UNIT_ID, AZIMUTHS, HALF_SECTOR_WIDTHS, AZIMUTH_RATES, ELEVATIONS)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t916 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t916 toBytes'


def test916FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t916 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t916 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t916 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t916 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t916 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t916 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID, 'Firing Unit ID wrong: t916 fromBytes'
    assert msg.azimuths[0].data == AZIMUTHS[0], 'Azimuth 0 wrong: t916 fromBytes'
    assert msg.halfSectorWidths[0].data == HALF_SECTOR_WIDTHS[0], 'Half Sector Width 0 wrong: t916 fromBytes'
    assert msg.azimuthRates[0].data == AZIMUTH_RATES[0], 'Azimuth Rate 0 wrong: t916 fromBytes'
    assert msg.elevations[0].data == ELEVATIONS[0], 'Elevations 0 wrong: t916 fromBytes'
    assert msg.azimuths[1].data == AZIMUTHS[1], 'Azimuth 1 wrong: t916 fromBytes'
    assert msg.halfSectorWidths[1].data == HALF_SECTOR_WIDTHS[1], 'Half Sector Width 1 wrong: t916 fromBytes'
    assert msg.azimuthRates[1].data == AZIMUTH_RATES[1], 'Azimuth Rate 1 wrong: t916 fromBytes'
    assert msg.elevations[1].data == ELEVATIONS[1], 'Elevations 1 wrong: t916 fromBytes'
