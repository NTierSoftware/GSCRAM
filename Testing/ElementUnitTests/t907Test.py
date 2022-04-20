# t907Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/14/2018

from CRAMmsg.unusedCRAMmsg.t907WESRAMTrack import t907WESRAMTrack
from CRAMmsg.Matrix import PMatrix
from CRAMmsg.Matrix import RMatrix
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

import struct

MSG_LENGTH_A = 92
MSG_LENGTH_B = 176
MSG_LENGTH_C = 176
MSG_LENGTH_D = 260
MSG_ID = 907
KIND = 0
PART_COUNT_A = 0
PART_COUNT_B = 1
PART_COUNT_C = 2
PART_COUNT_D = 3

WEAPON_ID = 0x1234
LOCAL_TRACK_ID = 0x22FF
SYS_TRACK_ID = 0x2701B1C9
TRACK_CLASS = 0x05
SIM_FLAG = 0x00
DROP_TRACK_FLAG = 0x01
CONFIRM_STATUS = 0x02
BALLISTIC_COEFF = 0x7281FF3E
UNCERT_BALLISTIC_COEFF = 0x82081117
TRACK_ECEF_X = -1  # 0xFFFFFFFF
TRACK_ECEF_Y = 4  # 0x00000004
TRACK_ECEF_Z = 17  # 0x00000011
TRACK_ECEF_VX = -3  # 0xFFFFFFFD
TRACK_ECEF_VY = 31  # 0x0000001F
TRACK_ECEF_VZ = 5  # 0x00000005
VALID_TIME = 0x36A981B8
IMPACT_POS_TQ = 0x0A
RADAR_CROSS_SECTION = -100  # 0x9C
POS_TQ = 0x08
VEL_TQ = 0x04
IPP_ECEF_X = -4  # 0xFFFFFFFC
IPP_ECEF_Y = 2  # 0x00000002
IPP_ECEF_Z = 0  # 0x00000000
IMPACT_TIME = 0x435476BA

P_FIELDS = [-2.0, 1.0, -100.0, 10000.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# [0xC0000000, 0x3F800000, 0xC2C80000, 0x461C4000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
# 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
# 0x3F800000, 0x3F800000, 0x3F800000]

R_FIELDS = [-3.6, 17.8, 0.912, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
# [0xC0666666, 0x418E6666, 0x3F6978D5, 0x00000000, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD,
# 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD,
# 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD]

FAKE_TIME = 0xCCCCCCCC


BYTES_A = bytearray([0x00, 0x00, 0x00, 0x5C, 0x03, 0x8B, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x05, 0x00, 0x01, 0x02,
                     0x72, 0x81, 0xFF, 0x3E, 0x82, 0x08, 0x11, 0x17, 0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD,
                     0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0x36, 0xA9, 0x81, 0xB8,
                     0x0A, 0x9C, 0x08, 0x04, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00, 0x43, 0x54, 0x76, 0xBA, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


BYTES_B = bytearray([0x00, 0x00, 0x00, 0xB0, 0x03, 0x8B, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x05, 0x00, 0x01, 0x02,
                     0x72, 0x81, 0xFF, 0x3E, 0x82, 0x08, 0x11, 0x17, 0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD,
                     0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0x36, 0xA9, 0x81, 0xB8,
                     0x0A, 0x9C, 0x08, 0x04, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00, 0x43, 0x54, 0x76, 0xBA, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0xC2, 0xC8, 0x00, 0x00, 0x46, 0x1C, 0x40, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00])

BYTES_C = bytearray([0x00, 0x00, 0x00, 0xB0, 0x03, 0x8B, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x05, 0x00, 0x01, 0x02,
                     0x72, 0x81, 0xFF, 0x3E, 0x82, 0x08, 0x11, 0x17, 0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD,
                     0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0x36, 0xA9, 0x81, 0xB8,
                     0x0A, 0x9C, 0x08, 0x04, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00, 0x43, 0x54, 0x76, 0xBA, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x66, 0x66, 0x66,
                     0x41, 0x8E, 0x66, 0x66, 0x3F, 0x69, 0x78, 0xD5, 0x00, 0x00, 0x00, 0x00,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD])


BYTES_D = bytearray([0x00, 0x00, 0x01, 0x04, 0x03, 0x8B, 0x00, 0x03, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x05, 0x00, 0x01, 0x02,
                     0x72, 0x81, 0xFF, 0x3E, 0x82, 0x08, 0x11, 0x17, 0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD,
                     0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0x36, 0xA9, 0x81, 0xB8,
                     0x0A, 0x9C, 0x08, 0x04, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x02,
                     0x00, 0x00, 0x00, 0x00, 0x43, 0x54, 0x76, 0xBA, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0xC2, 0xC8, 0x00, 0x00, 0x46, 0x1C, 0x40, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0xC0, 0x66, 0x66, 0x66,
                     0x41, 0x8E, 0x66, 0x66, 0x3F, 0x69, 0x78, 0xD5, 0x00, 0x00, 0x00, 0x00,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD])


def run907Test():
    test907JSONSimple()
    test907FromBytes()
    test907ToBytes()
    print("907 WES RAM Track: PASS")


def test907JSONSimple():
    msg = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                          CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                          TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                          RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy

    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                      P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                      P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                      P_FIELDS[20])

    rFields = RMatrix(R_FIELDS[0], R_FIELDS[1], R_FIELDS[2], R_FIELDS[3], R_FIELDS[4], R_FIELDS[5], R_FIELDS[6],
                      R_FIELDS[7], R_FIELDS[8], R_FIELDS[9], R_FIELDS[10], R_FIELDS[11], R_FIELDS[12], R_FIELDS[13],
                      R_FIELDS[14], R_FIELDS[15], R_FIELDS[16], R_FIELDS[17], R_FIELDS[18], R_FIELDS[19],
                      R_FIELDS[20])

    msg2 = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                           CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                           TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                           RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME,
                           pFields)
    str2 = msg2.toJSON()
    msg2_copy = getMessageFromJSON(str2)
    assert msg2 == msg2_copy

    msg3 = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                           CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                           TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                           RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME,
                           rFields=rFields)
    str3 = msg3.toJSON()
    msg3_copy = getMessageFromJSON(str3)
    assert msg3 == msg3_copy

    msg4 = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                           CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                           TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                           RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME,
                           pFields, rFields)
    str4 = msg4.toJSON()
    msg4_copy = getMessageFromJSON(str4)
    assert msg4 == msg4_copy


def test907ToBytes():
    msg = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                          CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                          TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                          RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t907 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES_A, 'First byte array failed: t907 toBytes'

    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                      P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                      P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                      P_FIELDS[20])

    rFields = RMatrix(R_FIELDS[0], R_FIELDS[1], R_FIELDS[2], R_FIELDS[3], R_FIELDS[4], R_FIELDS[5], R_FIELDS[6],
                      R_FIELDS[7], R_FIELDS[8], R_FIELDS[9], R_FIELDS[10], R_FIELDS[11], R_FIELDS[12], R_FIELDS[13],
                      R_FIELDS[14], R_FIELDS[15], R_FIELDS[16], R_FIELDS[17], R_FIELDS[18], R_FIELDS[19],
                      R_FIELDS[20])

    msg2 = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                          CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                          TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                          RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME,
                          pFields)
    msg2.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg2.getByteArray() == BYTES_B, 'Second byte array failed: t907 toBytes'

    msg3 = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                           CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                           TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                           RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME,
                           rFields=rFields)
    msg3.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg3.getByteArray() == BYTES_C, 'Third byte array failed: t907 toBytes'

    msg4 = t907WESRAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_CLASS, SIM_FLAG, DROP_TRACK_FLAG,
                           CONFIRM_STATUS, BALLISTIC_COEFF, UNCERT_BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y,
                           TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, VALID_TIME, IMPACT_POS_TQ,
                           RADAR_CROSS_SECTION, POS_TQ, VEL_TQ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, IMPACT_TIME,
                           pFields, rFields)
    msg4.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg4.getByteArray() == BYTES_D, 'Fourth byte array failed: t907 toBytes'


def test907FromBytes():
    msg = getMessageFromBytes(BYTES_A)
    assert msg.header.messageLength.data == MSG_LENGTH_A, 'First Message Length wrong: t907 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'First Message ID wrong: t907 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'First Interface Kind wrong: t907 fromBytes'
    assert msg.header.partCount.data == PART_COUNT_A, 'First Part Count wrong: t907 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'First Transmit Time wrong: t907 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'First Weapon ID wrong: t907 fromBytes'
    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'First Local Track ID wrong: t907 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'First System Track ID wrong: t907 fromBytes'
    assert msg.trackClass.data == TRACK_CLASS, 'First Track Classificatoin wrong: t907 fromBytes'
    assert msg.simFlag.data == SIM_FLAG, 'First Simulated Flag wrong: t907 fromBytes'
    assert msg.dropTrackFlag.data == DROP_TRACK_FLAG, 'First Drop Track Flag wrong: t907 fromBytes'
    assert msg.confirmStatus.data == CONFIRM_STATUS, 'First Confirm Status wrong: t907 fromBytes'
    assert msg.ballisticCoeff.data == BALLISTIC_COEFF, 'First Ballistic Coefficient wrong: t907 fromBytes'
    assert msg.uncertBallisticCoeff.data == UNCERT_BALLISTIC_COEFF, 'First Uncert Ballistic Coefficient wrong: t907 fromBytes'
    assert msg.trackECEF_X.data == TRACK_ECEF_X, 'First Track ECEF X wrong: t907 fromBytes'
    assert msg.trackECEF_Y.data == TRACK_ECEF_Y, 'First Track ECEF Y wrong: t907 fromBytes'
    assert msg.trackECEF_Z.data == TRACK_ECEF_Z, 'First Track ECEF Z wrong: t907 fromBytes'
    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'First Track ECEF Vx wrong: t907 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'First Track ECEF Vy wrong: t907 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'First ECEF Vz wrong: t907 fromBytes'
    assert msg.validTime.data == VALID_TIME, 'First Valid Time wrong: t907 fromBytes'
    assert msg.impactPosTQ.data == IMPACT_POS_TQ, 'First Impact Position TQ wrong: t907 fromBytes'
    assert msg.radarCrossSection.data == RADAR_CROSS_SECTION, 'First Radar Cross Section wrong: t907 fromBytes'
    assert msg.posTQ.data == POS_TQ, 'First Pos TQ wrong: t907 fromBytes'
    assert msg.velTQ.data == VEL_TQ, 'First Vel TQ wrong: t907 fromBytes'
    assert msg.IppECEF_X.data == IPP_ECEF_X, 'First Ipp ECEF X wrong: t907 fromBytes'
    assert msg.IppECEF_Y.data == IPP_ECEF_Y, 'First Ipp ECEF Y wrong: t907 fromBytes'
    assert msg.IppECEF_Z.data == IPP_ECEF_Z, 'First Ipp ECEF Z wrong: t907 fromBytes'
    assert msg.impactTime.data == IMPACT_TIME, 'First Impact Time wrong: t907 fromBytes'

    msg2 = getMessageFromBytes(BYTES_B)
    assert msg2.header.messageLength.data == MSG_LENGTH_B, 'Second Message Length wrong: t907 fromBytes'
    assert msg2.header.messageId.data == MSG_ID, 'Second Message ID wrong: t907 fromBytes'
    assert msg2.header.interfaceKind.data == KIND, 'Second Interface Kind wrong: t907 fromBytes'
    assert msg2.header.partCount.data == PART_COUNT_B, 'Second Part Count wrong: t907 fromBytes'
    assert msg2.header.transmitTime.data == FAKE_TIME, 'Second Transmit Time wrong: t907 fromBytes'

    assert msg2.weaponId.data == WEAPON_ID, 'Second Weapon ID wrong: t907 fromBytes'
    assert msg2.localTrackId.data == LOCAL_TRACK_ID, 'Second Local Track ID wrong: t907 fromBytes'
    assert msg2.sysTrackId.data == SYS_TRACK_ID, 'Second System Track ID wrong: t907 fromBytes'
    assert msg2.trackClass.data == TRACK_CLASS, 'Second Track Classificatoin wrong: t907 fromBytes'
    assert msg2.simFlag.data == SIM_FLAG, 'Second Simulated Flag wrong: t907 fromBytes'
    assert msg2.dropTrackFlag.data == DROP_TRACK_FLAG, 'Second Drop Track Flag wrong: t907 fromBytes'
    assert msg2.confirmStatus.data == CONFIRM_STATUS, 'Second Confirm Status wrong: t907 fromBytes'
    assert msg2.ballisticCoeff.data == BALLISTIC_COEFF, 'Second Ballistic Coefficient wrong: t907 fromBytes'
    assert msg2.uncertBallisticCoeff.data == UNCERT_BALLISTIC_COEFF, 'Second Uncert Ballistic Coefficient wrong: t907 fromBytes'
    assert msg2.trackECEF_X.data == TRACK_ECEF_X, 'Second Track ECEF X wrong: t907 fromBytes'
    assert msg2.trackECEF_Y.data == TRACK_ECEF_Y, 'Second Track ECEF Y wrong: t907 fromBytes'
    assert msg2.trackECEF_Z.data == TRACK_ECEF_Z, 'Second Track ECEF Z wrong: t907 fromBytes'
    assert msg2.trackECEF_Vx.data == TRACK_ECEF_VX, 'Second Track ECEF Vx wrong: t907 fromBytes'
    assert msg2.trackECEF_Vy.data == TRACK_ECEF_VY, 'Second Track ECEF Vy wrong: t907 fromBytes'
    assert msg2.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Second ECEF Vz wrong: t907 fromBytes'
    assert msg2.validTime.data == VALID_TIME, 'Second Valid Time wrong: t907 fromBytes'
    assert msg2.impactPosTQ.data == IMPACT_POS_TQ, 'Second Impact Position TQ wrong: t907 fromBytes'
    assert msg2.radarCrossSection.data == RADAR_CROSS_SECTION, 'Second Radar Cross Section wrong: t907 fromBytes'
    assert msg2.posTQ.data == POS_TQ, 'Second Pos TQ wrong: t907 fromBytes'
    assert msg2.velTQ.data == VEL_TQ, 'Second Vel TQ wrong: t907 fromBytes'
    assert msg2.IppECEF_X.data == IPP_ECEF_X, 'Second Ipp ECEF X wrong: t907 fromBytes'
    assert msg2.IppECEF_Y.data == IPP_ECEF_Y, 'Second Ipp ECEF Y wrong: t907 fromBytes'
    assert msg2.IppECEF_Z.data == IPP_ECEF_Z, 'Second Ipp ECEF Z wrong: t907 fromBytes'
    assert msg2.impactTime.data == IMPACT_TIME, 'Second Impact Time wrong: t907 fromBytes'

    msg2p = msg2.pFields.allFields()
    for i in range(0, len(P_FIELDS)):
        assert P_FIELDS[i] == msg2p[i].data, 'P Fields wrong: t907 fromBytes'

    msg3 = getMessageFromBytes(BYTES_C)
    assert msg3.header.messageLength.data == MSG_LENGTH_C, 'Third Message Length wrong: t907 fromBytes'
    assert msg3.header.messageId.data == MSG_ID, 'Third Message ID wrong: t907 fromBytes'
    assert msg3.header.interfaceKind.data == KIND, 'Third Interface Kind wrong: t907 fromBytes'
    assert msg3.header.partCount.data == PART_COUNT_C, 'Third Part Count wrong: t907 fromBytes'
    assert msg3.header.transmitTime.data == FAKE_TIME, 'Third Transmit Time wrong: t907 fromBytes'

    assert msg3.weaponId.data == WEAPON_ID, 'Third Weapon ID wrong: t907 fromBytes'
    assert msg3.localTrackId.data == LOCAL_TRACK_ID, 'Third Local Track ID wrong: t907 fromBytes'
    assert msg3.sysTrackId.data == SYS_TRACK_ID, 'Third System Track ID wrong: t907 fromBytes'
    assert msg3.trackClass.data == TRACK_CLASS, 'Third Track Classificatoin wrong: t907 fromBytes'
    assert msg3.simFlag.data == SIM_FLAG, 'Third Simulated Flag wrong: t907 fromBytes'
    assert msg3.dropTrackFlag.data == DROP_TRACK_FLAG, 'Third Drop Track Flag wrong: t907 fromBytes'
    assert msg3.confirmStatus.data == CONFIRM_STATUS, 'Third Confirm Status wrong: t907 fromBytes'
    assert msg3.ballisticCoeff.data == BALLISTIC_COEFF, 'Third Ballistic Coefficient wrong: t907 fromBytes'
    assert msg3.uncertBallisticCoeff.data == UNCERT_BALLISTIC_COEFF, 'Third Uncert Ballistic Coefficient wrong: t907 fromBytes'
    assert msg3.trackECEF_X.data == TRACK_ECEF_X, 'Third Track ECEF X wrong: t907 fromBytes'
    assert msg3.trackECEF_Y.data == TRACK_ECEF_Y, 'Third Track ECEF Y wrong: t907 fromBytes'
    assert msg3.trackECEF_Z.data == TRACK_ECEF_Z, 'Third Track ECEF Z wrong: t907 fromBytes'
    assert msg3.trackECEF_Vx.data == TRACK_ECEF_VX, 'Third Track ECEF Vx wrong: t907 fromBytes'
    assert msg3.trackECEF_Vy.data == TRACK_ECEF_VY, 'Third Track ECEF Vy wrong: t907 fromBytes'
    assert msg3.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Third ECEF Vz wrong: t907 fromBytes'
    assert msg3.validTime.data == VALID_TIME, 'Third Valid Time wrong: t907 fromBytes'
    assert msg3.impactPosTQ.data == IMPACT_POS_TQ, 'Third Impact Position TQ wrong: t907 fromBytes'
    assert msg3.radarCrossSection.data == RADAR_CROSS_SECTION, 'Third Radar Cross Section wrong: t907 fromBytes'
    assert msg3.posTQ.data == POS_TQ, 'Third Pos TQ wrong: t907 fromBytes'
    assert msg3.velTQ.data == VEL_TQ, 'Third Vel TQ wrong: t907 fromBytes'
    assert msg3.IppECEF_X.data == IPP_ECEF_X, 'Third Ipp ECEF X wrong: t907 fromBytes'
    assert msg3.IppECEF_Y.data == IPP_ECEF_Y, 'Third Ipp ECEF Y wrong: t907 fromBytes'
    assert msg3.IppECEF_Z.data == IPP_ECEF_Z, 'Third Ipp ECEF Z wrong: t907 fromBytes'
    assert msg3.impactTime.data == IMPACT_TIME, 'Third Impact Time wrong: t907 fromBytes'
    
    msg3r = msg3.rFields.allFields()
    for i in range(0, len(R_FIELDS)):
        fixedNum = struct.unpack(">f", struct.pack(">f", R_FIELDS[i]))[0]
        assert fixedNum == msg3r[i].data

    msg4 = getMessageFromBytes(BYTES_D)
    assert msg4.header.messageLength.data == MSG_LENGTH_D, 'Fourth Message Length wrong: t907 fromBytes'
    assert msg4.header.messageId.data == MSG_ID, 'Fourth Message ID wrong: t907 fromBytes'
    assert msg4.header.interfaceKind.data == KIND, 'Fourth Interface Kind wrong: t907 fromBytes'
    assert msg4.header.partCount.data == PART_COUNT_D, 'Fourth Part Count wrong: t907 fromBytes'
    assert msg4.header.transmitTime.data == FAKE_TIME, 'Fourth Transmit Time wrong: t907 fromBytes'

    assert msg4.weaponId.data == WEAPON_ID, 'Fourth Weapon ID wrong: t907 fromBytes'
    assert msg4.localTrackId.data == LOCAL_TRACK_ID, 'Fourth Local Track ID wrong: t907 fromBytes'
    assert msg4.sysTrackId.data == SYS_TRACK_ID, 'Fourth System Track ID wrong: t907 fromBytes'
    assert msg4.trackClass.data == TRACK_CLASS, 'Fourth Track Classificatoin wrong: t907 fromBytes'
    assert msg4.simFlag.data == SIM_FLAG, 'Fourth Simulated Flag wrong: t907 fromBytes'
    assert msg4.dropTrackFlag.data == DROP_TRACK_FLAG, 'Fourth Drop Track Flag wrong: t907 fromBytes'
    assert msg4.confirmStatus.data == CONFIRM_STATUS, 'Fourth Confirm Status wrong: t907 fromBytes'
    assert msg4.ballisticCoeff.data == BALLISTIC_COEFF, 'Fourth Ballistic Coefficient wrong: t907 fromBytes'
    assert msg4.uncertBallisticCoeff.data == UNCERT_BALLISTIC_COEFF, 'Fourth Uncert Ballistic Coefficient wrong: t907 fromBytes'
    assert msg4.trackECEF_X.data == TRACK_ECEF_X, 'Fourth Track ECEF X wrong: t907 fromBytes'
    assert msg4.trackECEF_Y.data == TRACK_ECEF_Y, 'Fourth Track ECEF Y wrong: t907 fromBytes'
    assert msg4.trackECEF_Z.data == TRACK_ECEF_Z, 'Fourth Track ECEF Z wrong: t907 fromBytes'
    assert msg4.trackECEF_Vx.data == TRACK_ECEF_VX, 'Fourth Track ECEF Vx wrong: t907 fromBytes'
    assert msg4.trackECEF_Vy.data == TRACK_ECEF_VY, 'Fourth Track ECEF Vy wrong: t907 fromBytes'
    assert msg4.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Fourth ECEF Vz wrong: t907 fromBytes'
    assert msg4.validTime.data == VALID_TIME, 'Fourth Valid Time wrong: t907 fromBytes'
    assert msg4.impactPosTQ.data == IMPACT_POS_TQ, 'Fourth Impact Position TQ wrong: t907 fromBytes'
    assert msg4.radarCrossSection.data == RADAR_CROSS_SECTION, 'Fourth Radar Cross Section wrong: t907 fromBytes'
    assert msg4.posTQ.data == POS_TQ, 'Fourth Pos TQ wrong: t907 fromBytes'
    assert msg4.velTQ.data == VEL_TQ, 'Fourth Vel TQ wrong: t907 fromBytes'
    assert msg4.IppECEF_X.data == IPP_ECEF_X, 'Fourth Ipp ECEF X wrong: t907 fromBytes'
    assert msg4.IppECEF_Y.data == IPP_ECEF_Y, 'Fourth Ipp ECEF Y wrong: t907 fromBytes'
    assert msg4.IppECEF_Z.data == IPP_ECEF_Z, 'Fourth Ipp ECEF Z wrong: t907 fromBytes'
    assert msg4.impactTime.data == IMPACT_TIME, 'Fourth Impact Time wrong: t907 fromBytes'

    msg4p = msg4.pFields.allFields()
    for i in range(0, len(P_FIELDS)):
        assert P_FIELDS[i] == msg4p[i].data

    msg4r = msg4.rFields.allFields()
    for i in range(0, len(R_FIELDS)):
        fixedNum = struct.unpack(">f", struct.pack(">f", R_FIELDS[i]))[0]
        assert fixedNum == msg4r[i].data
