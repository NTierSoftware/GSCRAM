# t926Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/15/2018

from CRAMmsg.r926WeaponEmplacement import r926WeaponEmplacement
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 72
MSG_ID = 926
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0x8731
WEAPON_KIND = 0x0008
VALID_TIME = 0x99399192
ECEF_X = -1  # 0xFFFFFFFF
ECEF_Y = 1  # 0x00000001
ECEF_Z = -3  # 0xFFFFFFFD
ECEF_VX = -4  # 0xFFFFFFFC
ECEF_VY = -6  # 0xFFFFFFFA
ECEF_VZ = -8  # 0xFFFFFFF8
ELEVATION = -16  # 0xFFF0
AZIMUTH = 0x82EE
PLATFORM_AZIMUTH = 0x73BE


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x48, 0x03, 0x9E, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x87, 0x31, 0x00, 0x08, 0x99, 0x39, 0x91, 0x92, 0xFF, 0xFF, 0xFF, 0xFF,
                   0x00, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFD, 0xFF, 0xFF, 0xFF, 0xFC,
                   0xFF, 0xFF, 0xFF, 0xFA, 0xFF, 0xFF, 0xFF, 0xF8, 0xFF, 0xF0, 0x82, 0xEE,
                   0x73, 0xBE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def run926Test():
    test926JSONSimple()
    test926FromBytes()
    test926ToBytes()
    print("926 Weapon Emplacement: PASS")


def test926JSONSimple():
    msg = r926WeaponEmplacement(WEAPON_ID, WEAPON_KIND, VALID_TIME, ECEF_X, ECEF_Y, ECEF_Z, ECEF_VX, ECEF_VY, ECEF_VZ,
                                ELEVATION, AZIMUTH, PLATFORM_AZIMUTH)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: t926'


def test926ToBytes():
    msg = r926WeaponEmplacement(WEAPON_ID, WEAPON_KIND, VALID_TIME, ECEF_X, ECEF_Y, ECEF_Z, ECEF_VX, ECEF_VY, ECEF_VZ,
                                ELEVATION, AZIMUTH, PLATFORM_AZIMUTH)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t926 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t926 toBytes'


def test926FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t926 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t926 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t926 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t926 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t926 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t926 fromBytes'
    assert msg.weaponKind.data == WEAPON_KIND, 'Weapon Kind wrong: t926 fromBytes'
    assert msg.validTime.data == VALID_TIME, 'Valid Time wrong: t926 fromBytes'
    assert msg.ECEF_X.data == ECEF_X, 'ECEF X wrong: t926 fromBytes'
    assert msg.ECEF_Y.data == ECEF_Y, 'ECEF Y wrong: t926 fromBytes'
    assert msg.ECEF_Z.data == ECEF_Z, 'ECEF Z wrong: t926 fromBytes'
    assert msg.ECEF_Vx.data == ECEF_VX, 'Track ECEF Vx wrong: t925 fromBytes'
    assert msg.ECEF_Vy.data == ECEF_VY, 'Track ECEF Vy wrong: t925 fromBytes'
    assert msg.ECEF_Vz.data == ECEF_VZ, 'Track ECEF Vz wrong: t925 fromBytes'
    assert msg.elevation.data == ELEVATION, 'Elevation wrong: t925 fromBytes'
    assert msg.azimuth.data == AZIMUTH, 'Azimuth wrong: t925 fromBytes'
    assert msg.platformAzimuth.data == PLATFORM_AZIMUTH, 'Platform Azimuth wrong: t925 fromBytes'

