# r911Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/15/2018

from CRAMmsg.unusedCRAMmsg.r911LauncherPrePosition import r911LauncherPrePosition
from CRAMmsg.unusedCRAMmsg.r911LauncherPrePosition import r911Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 24
MSG_ID = 911
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0xD3F2
FIRING_UNIT_ID = 0x45FA
AZIMUTH = 0x8911
ELEVATION = -8  # 0xFFF8
PRE_POSITION_REASON = r911Consts.PrePositionReason.C2S_OPERATOR.value.data  # 0x05
# uint8 spare
# uint16 spare

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x18, 0x03, 0x8F, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0xD3, 0xF2, 0x45, 0xFA, 0x89, 0x11, 0xFF, 0xF8, 0x05, 0x00, 0x00, 0x00])


def run911Test():
    test911JSONSimple()
    test911FromBytes()
    test911ToBytes()
    print('911 Launcher Pre-Position: PASS')


def test911JSONSimple():
    msg = r911LauncherPrePosition(WEAPON_ID, FIRING_UNIT_ID, AZIMUTH, ELEVATION, PRE_POSITION_REASON)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: r911'


def test911ToBytes():
    msg = r911LauncherPrePosition(WEAPON_ID, FIRING_UNIT_ID, AZIMUTH, ELEVATION, PRE_POSITION_REASON)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r911 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r911 toBytes'


def test911FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r911 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r911 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r911 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r911 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r911 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: r911 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID, 'Firing Unit ID wrong: r911 fromBytes'
    assert msg.azimuth.data == AZIMUTH, 'Azimuth wrong: r911 fromBytes'
    assert msg.elevation.data == ELEVATION, 'Elevation wrong: r911 fromBytes'
    assert msg.prePositionReason.data == PRE_POSITION_REASON, 'Pre-Position Reason wrong: r911 fromBytes'