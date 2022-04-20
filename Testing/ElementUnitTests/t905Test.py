# t905Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/9/2018

from CRAMmsg.unusedCRAMmsg.t905WESAirTrack import t905WESAirTrack
from CRAMmsg.Matrix import PMatrix
from CRAMmsg.Matrix import RMatrix
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

import struct

MSG_LENGTH_A = 60
MSG_LENGTH_B = 144
MSG_LENGTH_C = 144
MSG_LENGTH_D = 228
MSG_ID = 905
KIND = 0
PART_COUNT_A = 0
PART_COUNT_B = 1
PART_COUNT_C = 2
PART_COUNT_D = 3

WEAPON_ID = 0x1234
LOCAL_TRACK_ID = 0x22FF
SYS_TRACK_ID = 0x2701B1C9
TRACK_ID = 0x03
TRACK_CLASS = 0x05
SIM_FLAG = 0x00
POS_TQ = 0x08
VEL_TQ = 0x04
TRACK_ECEF_X = -1  # 0xFFFFFFFF
TRACK_ECEF_Y = 4  # 0x00000004
TRACK_ECEF_Z = 17  # 0x00000011
TRACK_ECEF_VX = -3  # 0xFFFFFFFD
TRACK_ECEF_VY = 31  # 0x0000001F
TRACK_ECEF_VZ = 5  # 0x00000005
T_VALID = 160  # 0x000000A0
SENSOR_REG_TRACK = 0x00
DROP_TRACK_FLAG = 0x01

P_FIELDS = [-2.0, 1.0, -100.0, 10000.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        # [0xC0000000, 0x3F800000, 0xC2C80000, 0x461C4000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
        # 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
        # 0x3F800000, 0x3F800000, 0x3F800000]

R_FIELDS = [-3.6, 17.8, 0.912, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        # [0xC0666666, 0x418E6666, 0x3F6978D5, 0x00000000, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD,
        # 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD,
        # 0x3DCCCCCD, 0x3DCCCCCD, 0x3DCCCCCD]

FAKE_TIME = 0xCCCCCCCC


BYTES_A = bytearray([0x00, 0x00, 0x00, 0x3C, 0x03, 0x89, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x03, 0x05, 0x00, 0x08,
                     0x04, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x1F,
                     0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0xA0, 0x00, 0x01, 0x00, 0x00])

BYTES_B = bytearray([0x00, 0x00, 0x00, 0x90, 0x03, 0x89, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x03, 0x05, 0x00, 0x08,
                     0x04, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x1F,
                     0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0xA0, 0x00, 0x01, 0x00, 0x00,
                     0xC0, 0x00, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0xC2, 0xC8, 0x00, 0x00,
                     0x46, 0x1C, 0x40, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00])

BYTES_C = bytearray([0x00, 0x00, 0x00, 0x90, 0x03, 0x89, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x03, 0x05, 0x00, 0x08,
                     0x04, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x1F,
                     0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0xA0, 0x00, 0x01, 0x00, 0x00,
                     0xC0, 0x66, 0x66, 0x66, 0x41, 0x8E, 0x66, 0x66, 0x3F, 0x69, 0x78, 0xD5,
                     0x00, 0x00, 0x00, 0x00, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD])

BYTES_D = bytearray([0x00, 0x00, 0x00, 0xE4, 0x03, 0x89, 0x00, 0x03, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x03, 0x05, 0x00, 0x08,
                     0x04, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x1F,
                     0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0xA0, 0x00, 0x01, 0x00, 0x00,
                     0xC0, 0x00, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0xC2, 0xC8, 0x00, 0x00,
                     0x46, 0x1C, 0x40, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0xC0, 0x66, 0x66, 0x66, 0x41, 0x8E, 0x66, 0x66, 0x3F, 0x69, 0x78, 0xD5,
                     0x00, 0x00, 0x00, 0x00, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD,
                     0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD, 0x3D, 0xCC, 0xCC, 0xCD])


def run905Test():
    test905JSONSimple()
    test905FromBytes()
    test905ToBytes()
    print("905 WES Air Track: PASS")


def test905JSONSimple():
    msg = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                          TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                          T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG)
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

    msg2 = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                           TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                           T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG, pFields)
    str2 = msg2.toJSON()
    msg2_copy = getMessageFromJSON(str2)
    assert msg2 == msg2_copy

    msg3 = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                           TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                           T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG, rFields=rFields)

    str3 = msg3.toJSON()
    msg3_copy = getMessageFromJSON(str3)
    assert msg3 == msg3_copy

    msg4 = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                           TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                           T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG, pFields, rFields)

    str4 = msg4.toJSON()
    msg4_copy = getMessageFromJSON(str4)
    assert msg4 == msg4_copy


def test905ToBytes():
    msg = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                          TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                          T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t905 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES_A, 'First byte array failed: t905 toBytes'
    
    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                          P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                          P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                          P_FIELDS[20])
    
    rFields = RMatrix(R_FIELDS[0], R_FIELDS[1], R_FIELDS[2], R_FIELDS[3], R_FIELDS[4], R_FIELDS[5], R_FIELDS[6],
                          R_FIELDS[7], R_FIELDS[8], R_FIELDS[9], R_FIELDS[10], R_FIELDS[11], R_FIELDS[12], R_FIELDS[13],
                          R_FIELDS[14], R_FIELDS[15], R_FIELDS[16], R_FIELDS[17], R_FIELDS[18], R_FIELDS[19],
                          R_FIELDS[20])

    msg2 = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                          TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                          T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG, pFields)
    msg2.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg2.getByteArray() == BYTES_B, 'Second byte array failed: t905 toBytes'

    msg3 = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                           TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                           T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG, rFields=rFields)
    msg3.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg3.getByteArray() == BYTES_C, 'Third byte array failed: t905 toBytes'

    msg4 = t905WESAirTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                           TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                           T_VALID, SENSOR_REG_TRACK, DROP_TRACK_FLAG, pFields, rFields)
    msg4.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg4.getByteArray() == BYTES_D, 'Fourth byte array failed: t905 toBytes'


def test905FromBytes():
    msg = getMessageFromBytes(BYTES_A)
    assert msg.header.messageLength.data == MSG_LENGTH_A, 'First Message Length wrong: t905 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'First Message ID wrong: t905 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'First Interface Kind wrong: t905 fromBytes'
    assert msg.header.partCount.data == PART_COUNT_A, 'First Part Count wrong: t905 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'First Transmit Time wrong: t905 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'First Weapon ID wrong: t905 fromBytes'
    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'First Local Track ID wrong: t905 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'First System Track ID wrong: t905 fromBytes'
    assert msg.trackIdentity.data == TRACK_ID, 'First Track Identity wrong: t905 fromBytes'
    assert msg.trackClass.data == TRACK_CLASS, 'First Track Classificatoin wrong: t905 fromBytes'
    assert msg.simFlag.data == SIM_FLAG, 'First Simulated Flag wrong: t905 fromBytes'
    assert msg.posTQ.data == POS_TQ, 'First Pos TQ wrong: t905 fromBytes'
    assert msg.velTQ.data == VEL_TQ, 'First Vel TQ wrong: t905 fromBytes'
    assert msg.trackECEF_X.data == TRACK_ECEF_X, 'First Track ECEF X wrong: t905 fromBytes'
    assert msg.trackECEF_Y.data == TRACK_ECEF_Y, 'First Track ECEF Y wrong: t905 fromBytes'
    assert msg.trackECEF_Z.data == TRACK_ECEF_Z, 'First Track ECEF Z wrong: t905 fromBytes'
    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'First Track ECEF Vx wrong: t905 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'First Track ECEF Vy wrong: t905 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'First ECEF Vz wrong: t905 fromBytes'
    assert msg.tValid.data == T_VALID, 'First T Valid wrong: t905 fromBytes'
    assert msg.sensorRegTrack.data == SENSOR_REG_TRACK, 'First Sensor Registration Track wrong: t905 fromBytes'
    assert msg.dropTrackFlag.data == DROP_TRACK_FLAG, 'First Drop Track Flag wrong: t905 fromBytes'
    
    msg2 = getMessageFromBytes(BYTES_B)
    assert msg2.header.messageLength.data == MSG_LENGTH_B, 'Second Message Length wrong: t905 fromBytes'
    assert msg2.header.messageId.data == MSG_ID, 'Second Message ID wrong: t905 fromBytes'
    assert msg2.header.interfaceKind.data == KIND, 'Second Interface Kind wrong: t905 fromBytes'
    assert msg2.header.partCount.data == PART_COUNT_B, 'Second Part Count wrong: t905 fromBytes'
    assert msg2.header.transmitTime.data == FAKE_TIME, 'Second Transmit Time wrong: t905 fromBytes'

    assert msg2.weaponId.data == WEAPON_ID, 'Second Weapon ID wrong: t905 fromBytes'
    assert msg2.localTrackId.data == LOCAL_TRACK_ID, 'Second Local Track ID wrong: t905 fromBytes'
    assert msg2.sysTrackId.data == SYS_TRACK_ID, 'Second System Track ID wrong: t905 fromBytes'
    assert msg2.trackIdentity.data == TRACK_ID, 'Second Track Identity wrong: t905 fromBytes'
    assert msg2.trackClass.data == TRACK_CLASS, 'Second Track Classificatoin wrong: t905 fromBytes'
    assert msg2.simFlag.data == SIM_FLAG, 'Second Simulated Flag wrong: t905 fromBytes'
    assert msg2.posTQ.data == POS_TQ, 'Second Pos TQ wrong: t905 fromBytes'
    assert msg2.velTQ.data == VEL_TQ, 'Second Vel TQ wrong: t905 fromBytes'
    assert msg2.trackECEF_X.data == TRACK_ECEF_X, 'Second Track ECEF X wrong: t905 fromBytes'
    assert msg2.trackECEF_Y.data == TRACK_ECEF_Y, 'Second Track ECEF Y wrong: t905 fromBytes'
    assert msg2.trackECEF_Z.data == TRACK_ECEF_Z, 'Second Track ECEF Z wrong: t905 fromBytes'
    assert msg2.trackECEF_Vx.data == TRACK_ECEF_VX, 'Second Track ECEF Vx wrong: t905 fromBytes'
    assert msg2.trackECEF_Vy.data == TRACK_ECEF_VY, 'Second Track ECEF Vy wrong: t905 fromBytes'
    assert msg2.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Second ECEF Vz wrong: t905 fromBytes'
    assert msg2.tValid.data == T_VALID, 'Second T Valid wrong: t905 fromBytes'
    assert msg2.sensorRegTrack.data == SENSOR_REG_TRACK, 'Second Sensor Registration Track wrong: t905 fromBytes'
    assert msg2.dropTrackFlag.data == DROP_TRACK_FLAG, 'Second Drop Track Flag wrong: t905 fromBytes'

    msg2p = msg2.pFields.allFields()
    for i in range(0, len(P_FIELDS)):
        assert P_FIELDS[i] == msg2p[i].data
        
    msg3 = getMessageFromBytes(BYTES_C)
    assert msg3.header.messageLength.data == MSG_LENGTH_C, 'Third Message Length wrong: t905 fromBytes'
    assert msg3.header.messageId.data == MSG_ID, 'Third Message ID wrong: t905 fromBytes'
    assert msg3.header.interfaceKind.data == KIND, 'Third Interface Kind wrong: t905 fromBytes'
    assert msg3.header.partCount.data == PART_COUNT_C, 'Third Part Count wrong: t905 fromBytes'
    assert msg3.header.transmitTime.data == FAKE_TIME, 'Third Transmit Time wrong: t905 fromBytes'

    assert msg3.weaponId.data == WEAPON_ID, 'Third Weapon ID wrong: t905 fromBytes'
    assert msg3.localTrackId.data == LOCAL_TRACK_ID, 'Third Local Track ID wrong: t905 fromBytes'
    assert msg3.sysTrackId.data == SYS_TRACK_ID, 'Third System Track ID wrong: t905 fromBytes'
    assert msg3.trackIdentity.data == TRACK_ID, 'Third Track Identity wrong: t905 fromBytes'
    assert msg3.trackClass.data == TRACK_CLASS, 'Third Track Classificatoin wrong: t905 fromBytes'
    assert msg3.simFlag.data == SIM_FLAG, 'Third Simulated Flag wrong: t905 fromBytes'
    assert msg3.posTQ.data == POS_TQ, 'Third Pos TQ wrong: t905 fromBytes'
    assert msg3.velTQ.data == VEL_TQ, 'Third Vel TQ wrong: t905 fromBytes'
    assert msg3.trackECEF_X.data == TRACK_ECEF_X, 'Third Track ECEF X wrong: t905 fromBytes'
    assert msg3.trackECEF_Y.data == TRACK_ECEF_Y, 'Third Track ECEF Y wrong: t905 fromBytes'
    assert msg3.trackECEF_Z.data == TRACK_ECEF_Z, 'Third Track ECEF Z wrong: t905 fromBytes'
    assert msg3.trackECEF_Vx.data == TRACK_ECEF_VX, 'Third Track ECEF Vx wrong: t905 fromBytes'
    assert msg3.trackECEF_Vy.data == TRACK_ECEF_VY, 'Third Track ECEF Vy wrong: t905 fromBytes'
    assert msg3.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Third ECEF Vz wrong: t905 fromBytes'
    assert msg3.tValid.data == T_VALID, 'Third T Valid wrong: t905 fromBytes'
    assert msg3.sensorRegTrack.data == SENSOR_REG_TRACK, 'Third Sensor Registration Track wrong: t905 fromBytes'
    assert msg3.dropTrackFlag.data == DROP_TRACK_FLAG, 'Third Drop Track Flag wrong: t905 fromBytes'

    msg3r = msg3.rFields.allFields()
    for i in range(0, len(R_FIELDS)):
        fixedNum = struct.unpack(">f", struct.pack(">f", R_FIELDS[i]))[0]
        assert fixedNum == msg3r[i].data
        
    msg4 = getMessageFromBytes(BYTES_D)
    assert msg4.header.messageLength.data == MSG_LENGTH_D, 'Fourth Message Length wrong: t905 fromBytes'
    assert msg4.header.messageId.data == MSG_ID, 'Fourth Message ID wrong: t905 fromBytes'
    assert msg4.header.interfaceKind.data == KIND, 'Fourth Interface Kind wrong: t905 fromBytes'
    assert msg4.header.partCount.data == PART_COUNT_D, 'Fourth Part Count wrong: t905 fromBytes'
    assert msg4.header.transmitTime.data == FAKE_TIME, 'Fourth Transmit Time wrong: t905 fromBytes'

    assert msg4.weaponId.data == WEAPON_ID, 'Fourth Weapon ID wrong: t905 fromBytes'
    assert msg4.localTrackId.data == LOCAL_TRACK_ID, 'Fourth Local Track ID wrong: t905 fromBytes'
    assert msg4.sysTrackId.data == SYS_TRACK_ID, 'Fourth System Track ID wrong: t905 fromBytes'
    assert msg4.trackIdentity.data == TRACK_ID, 'Fourth Track Identity wrong: t905 fromBytes'
    assert msg4.trackClass.data == TRACK_CLASS, 'Fourth Track Classificatoin wrong: t905 fromBytes'
    assert msg4.simFlag.data == SIM_FLAG, 'Fourth Simulated Flag wrong: t905 fromBytes'
    assert msg4.posTQ.data == POS_TQ, 'Fourth Pos TQ wrong: t905 fromBytes'
    assert msg4.velTQ.data == VEL_TQ, 'Fourth Vel TQ wrong: t905 fromBytes'
    assert msg4.trackECEF_X.data == TRACK_ECEF_X, 'Fourth Track ECEF X wrong: t905 fromBytes'
    assert msg4.trackECEF_Y.data == TRACK_ECEF_Y, 'Fourth Track ECEF Y wrong: t905 fromBytes'
    assert msg4.trackECEF_Z.data == TRACK_ECEF_Z, 'Fourth Track ECEF Z wrong: t905 fromBytes'
    assert msg4.trackECEF_Vx.data == TRACK_ECEF_VX, 'Fourth Track ECEF Vx wrong: t905 fromBytes'
    assert msg4.trackECEF_Vy.data == TRACK_ECEF_VY, 'Fourth Track ECEF Vy wrong: t905 fromBytes'
    assert msg4.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Fourth ECEF Vz wrong: t905 fromBytes'
    assert msg4.tValid.data == T_VALID, 'Fourth T Valid wrong: t905 fromBytes'
    assert msg4.sensorRegTrack.data == SENSOR_REG_TRACK, 'Fourth Sensor Registration Track wrong: t905 fromBytes'
    assert msg4.dropTrackFlag.data == DROP_TRACK_FLAG, 'Fourth Drop Track Flag wrong: t905 fromBytes'
    
    msg4p = msg4.pFields.allFields()
    for i in range(0, len(P_FIELDS)):
        assert P_FIELDS[i] == msg4p[i].data

    msg4r = msg4.rFields.allFields()
    for i in range(0, len(R_FIELDS)):
        fixedNum = struct.unpack(">f", struct.pack(">f", R_FIELDS[i]))[0]
        assert fixedNum == msg4r[i].data
