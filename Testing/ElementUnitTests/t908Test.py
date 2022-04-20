# t908Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/15/2018

from CRAMmsg.unusedCRAMmsg.t908LaunchPoint import t908LaunchPoint
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 60
MSG_ID = 908
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0xD3F2
# uint16 spare
SYSTEM_TRACK_ID = 0x9781DD10
ELP_LAT = -3  # 0xFFFFFFFD
ELP_LONG = -2  # 0xFFFFFFFE
ELP_ALT = 4  # 0x00000004
UNCERT_MAJOR_AXIS = 0x23470981
UNCERT_MINOR_AXIS = 0xBCEDAFAD
UNCERT_ELLIPSE_ROT = 0x029F113A
LAUNCH_TIME = 0x7081FF09
# uint32 spare
# uint32 spare
# uint32 spare


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x3C, 0x03, 0x8C, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0xD3, 0xF2, 0x00, 0x00, 0x97, 0x81, 0xDD, 0x10, 0xFF, 0xFF, 0xFF, 0xFD,
                   0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x04, 0x23, 0x47, 0x09, 0x81,
                   0xBC, 0xED, 0xAF, 0xAD, 0x02, 0x9F, 0x11, 0x3A, 0x70, 0x81, 0xFF, 0x09,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def run908Test():
    test908JSONSimple()
    test908FromBytes()
    test908ToBytes()
    print('908 Launch InterpCRAM: PASS')


def test908JSONSimple():
    msg = t908LaunchPoint(WEAPON_ID, SYSTEM_TRACK_ID, ELP_LAT, ELP_LONG, ELP_ALT, UNCERT_MAJOR_AXIS, UNCERT_MINOR_AXIS,
                          UNCERT_ELLIPSE_ROT, LAUNCH_TIME)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: t908'


def test908ToBytes():
    msg = t908LaunchPoint(WEAPON_ID, SYSTEM_TRACK_ID, ELP_LAT, ELP_LONG, ELP_ALT, UNCERT_MAJOR_AXIS, UNCERT_MINOR_AXIS,
                          UNCERT_ELLIPSE_ROT, LAUNCH_TIME)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t908 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t908 toBytes'


def test908FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t908 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t908 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t908 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t908 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t908 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t908 fromBytes'
    assert msg.sysTrackId.data == SYSTEM_TRACK_ID, 'System Track ID wrong: t908 fromBytes'
    assert msg.elpLat.data == ELP_LAT, 'Elp Latitude wrong: t908 fromBytes'
    assert msg.elpLong.data == ELP_LONG, 'Elp Longitude wrong: t908 fromBytes'
    assert msg.elpAlt.data == ELP_ALT, 'Elp Altitude wrong: t908 fromBytes'
    assert msg.uncertMajorAxis.data == UNCERT_MAJOR_AXIS, 'Uncert Major Axis wrong: t908 fromBytes'
    assert msg.uncertMinorAxis.data == UNCERT_MINOR_AXIS, 'Uncert Minor Axis wrong: t908 fromBytes'
    assert msg.uncertEllipseRot.data == UNCERT_ELLIPSE_ROT, 'Uncert Ellipse Rot wrong: t908 fromBytes'
    assert msg.launchTime.data == LAUNCH_TIME, 'Launch Time wrong: t908 fromBytes'
