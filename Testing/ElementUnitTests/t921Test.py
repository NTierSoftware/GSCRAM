# t921Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/17/2018

from CRAMmsg.unusedCRAMmsg.t921LauncherCutout import t921LauncherCutout
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.Header import HeaderConsts

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 80
MSG_ID = 921
KIND = HeaderConsts.InterfaceKind.AI3.value.data  # 0x00
PART_COUNT = 2

WEAPON_ID = 0x3280
FIRING_UNIT_ID = 0x4291
# uint32 spare
# uint32 spare
CUTOUT_IDS = [0x01, 0xAB]
CUTOUT_KINDS = [0x01, 0x02]
# uint16 spares
LEFT_AZS = [0x6714, 0x9923]
RIGHT_AZS = [0xA871, 0xB3C4]
UPPER_ELS = [-50, -678]  # [0xFFCE, 0xFD5A]
LOWER_ELS = [-1, 64]  # [0xFFFF, 0x0040]
# uint32 spares
# uint32 spares
# uint32 spares
# uint32 spares

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x50, 0x03, 0x99, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x32, 0x80, 0x42, 0x91, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x01, 0x01, 0x00, 0x00, 0x67, 0x14, 0xA8, 0x71, 0xFF, 0xCE, 0xFF, 0xFF,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0xAB, 0x02, 0x00, 0x00, 0x99, 0x23, 0xB3, 0xC4,
                   0xFD, 0x5A, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def run921Test():
    test921JSONSimple()
    test921FromBytes()
    test921ToBytes()
    print("921 Launcher Cutout: PASS")


def test921JSONSimple():
    msg = t921LauncherCutout(WEAPON_ID, FIRING_UNIT_ID, CUTOUT_IDS, CUTOUT_KINDS, LEFT_AZS, RIGHT_AZS, UPPER_ELS,
                             LOWER_ELS)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test921ToBytes():
    msg = t921LauncherCutout(WEAPON_ID, FIRING_UNIT_ID, CUTOUT_IDS, CUTOUT_KINDS, LEFT_AZS, RIGHT_AZS, UPPER_ELS,
                             LOWER_ELS)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t921 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t921 toBytes'


def test921FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t921 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t921 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t921 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t921 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t921 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t921 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID, 'Firing Unit ID wrong: t921 fromBytes'
    assert msg.cutoutIds[0].data == CUTOUT_IDS[0], 'Cutout ID 0 wrong: t921 fromBytes'
    assert msg.cutoutKinds[0].data == CUTOUT_KINDS[0], 'Cutout Kind 0 wrong: t921 fromBytes'
    assert msg.leftAzs[0].data == LEFT_AZS[0], 'Left Az 0 wrong: t921 fromBytes'
    assert msg.rightAzs[0].data == RIGHT_AZS[0], 'Right Az 0 wrong: t921 fromBytes'
    assert msg.upperEls[0].data == UPPER_ELS[0], 'Upper El 0 wrong: t921 fromBytes'
    assert msg.lowerEls[0].data == LOWER_ELS[0], 'Lower El 0 wrong: t921 fromBytes'
    
    assert msg.cutoutIds[1].data == CUTOUT_IDS[1], 'Cutout ID 1 wrong: t921 fromBytes'
    assert msg.cutoutKinds[1].data == CUTOUT_KINDS[1], 'Cutout Kind 1 wrong: t921 fromBytes'
    assert msg.leftAzs[1].data == LEFT_AZS[1], 'Left Az 1 wrong: t921 fromBytes'
    assert msg.rightAzs[1].data == RIGHT_AZS[1], 'Right Az 1 wrong: t921 fromBytes'
    assert msg.upperEls[1].data == UPPER_ELS[1], 'Upper El 1 wrong: t921 fromBytes'
    assert msg.lowerEls[1].data == LOWER_ELS[1], 'Lower El 1 wrong: t921 fromBytes'
   
