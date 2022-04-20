# r923Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/16/2018

from CRAMmsg.unusedCRAMmsg.r923SensorRegBiasCorrection import r923SensorRegBiasCorrection
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 88
MSG_ID = 923
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0x2468
FIRING_UNIT_ID = 0x1357
TIME_BIAS = -456  # 0xFE38
ELEV_GIMBAL_BIAS = -7912  # 0xE118
# uint32 spare
# uint32 spare
# uint32 spare
# uint32 spare
# uint32 spare
X_OFFSET = 128.125  # 0x43002000
Y_OFFSET = 256.75  # 0x43806000
Z_OFFSET = -257.75  # 0xC380E000
ECEF_1_1 = -258.8125  # 0xC3816800
ECEF_1_2 = 290.84375  # 0x43916C00
ECEF_1_3 = 1290.84375  # 0x44A15B00
ECEF_2_1 = 11  # 0x41300000
ECEF_2_2 = -450  # 0xC3E10000
ECEF_2_3 = 0.5  # 0x3F000000
ECEF_3_1 = 1.03125  # 0x3F840000
ECEF_3_2 = 0.75  # 0x3F400000
ECEF_3_3 = 1.0  # 0x3F800000


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x58, 0x03, 0x9B, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x24, 0x68, 0x13, 0x57, 0xFE, 0x38, 0xE1, 0x18, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x43, 0x00, 0x20, 0x00, 0x43, 0x80, 0x60, 0x00,
                   0xC3, 0x80, 0xE0, 0x00, 0xC3, 0x81, 0x68, 0x00, 0x43, 0x91, 0x6C, 0x00,
                   0x44, 0xA1, 0x5B, 0x00, 0x41, 0x30, 0x00, 0x00, 0xC3, 0xE1, 0x00, 0x00,
                   0x3F, 0x00, 0x00, 0x00, 0x3F, 0x84, 0x00, 0x00, 0x3F, 0x40, 0x00, 0x00,
                   0x3F, 0x80, 0x00, 0x00])


def run923Test():
    test923JSONSimple()
    test923FromBytes()
    test923ToBytes()
    print('923 Sensor Registration Bias Correction: PASS')


def test923JSONSimple():
    msg = r923SensorRegBiasCorrection(WEAPON_ID, FIRING_UNIT_ID, TIME_BIAS, ELEV_GIMBAL_BIAS, X_OFFSET, Y_OFFSET,
                                      Z_OFFSET, ECEF_1_1, ECEF_1_2, ECEF_1_3, ECEF_2_1, ECEF_2_2, ECEF_2_3, ECEF_3_1,
                                      ECEF_3_2, ECEF_3_3)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: r923'


def test923ToBytes():
    msg = r923SensorRegBiasCorrection(WEAPON_ID, FIRING_UNIT_ID, TIME_BIAS, ELEV_GIMBAL_BIAS, X_OFFSET, Y_OFFSET,
                                      Z_OFFSET, ECEF_1_1, ECEF_1_2, ECEF_1_3, ECEF_2_1, ECEF_2_2, ECEF_2_3, ECEF_3_1,
                                      ECEF_3_2, ECEF_3_3)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r923 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r923 toBytes'


def test923FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r923 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r923 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r923 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r923 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r923 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: r923 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID, 'Firing Unit ID wrong: r923 fromBytes'
    assert msg.timeBias.data == TIME_BIAS, 'Time Bias wrong: r923 fromBytes'
    assert msg.elevGimbalBias.data == ELEV_GIMBAL_BIAS, 'Elevation Gimbal Bias wrong: r923 fromBytes'
    assert msg.xOffset.data == X_OFFSET, 'X Offset wrong: r923 fromBytes'
    assert msg.yOffset.data == Y_OFFSET, 'Y Offset wrong: r923 fromBytes'
    assert msg.zOffset.data == Z_OFFSET, 'Z Offset wrong: r923 fromBytes'
    assert msg.ecef_1_1.data == ECEF_1_1, 'ECEF (1,1) wrong: r923 fromBytes'
    assert msg.ecef_1_2.data == ECEF_1_2, 'ECEF (1,2) wrong: r923 fromBytes'
    assert msg.ecef_1_3.data == ECEF_1_3, 'ECEF (1,3) wrong: r923 fromBytes'
    assert msg.ecef_2_1.data == ECEF_2_1, 'ECEF (2,1) wrong: r923 fromBytes'
    assert msg.ecef_2_2.data == ECEF_2_2, 'ECEF (2,2) wrong: r923 fromBytes'
    assert msg.ecef_2_3.data == ECEF_2_3, 'ECEF (2,3) wrong: r923 fromBytes'
    assert msg.ecef_3_1.data == ECEF_3_1, 'ECEF (3,1) wrong: r923 fromBytes'
    assert msg.ecef_3_2.data == ECEF_3_2, 'ECEF (3,2) wrong: r923 fromBytes'
    assert msg.ecef_3_3.data == ECEF_3_3, 'ECEF (3,3) wrong: r923 fromBytes'
