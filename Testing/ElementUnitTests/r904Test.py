# r904Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/16/2018

from CRAMmsg.unusedCRAMmsg.r904AirPictureTrack import r904AirPictureTrack
from CRAMmsg.Matrix import PMatrix
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH_A = 60
MSG_LENGTH_B = 144
MSG_ID = 904
KIND = 0
PART_COUNT_A = 0
PART_COUNT_B = 1

SEQ_INDEX = 0x93F2
SEQ_COUNT = 0x7714
SYS_TRACK_ID = 0x6789F142
TRACK_ID = 0x03
TRACK_CLASS = 0x05
SIM_FLAG = 0x01
POS_TQ = 0x08
VEL_TQ = 0x0A
# uint24 spare
TRACK_ECEF_X = -1  # 0xFFFFFFFF
TRACK_ECEF_Y = 4  # 0x00000004
TRACK_ECEF_Z = 17  # 0x00000011
TRACK_ECEF_VX = -3  # 0xFFFFFFFD
TRACK_ECEF_VY = 31  # 0x0000001F
TRACK_ECEF_VZ = 5  # 0x00000005
VALID_TIME = 0x789ABC00
# uint32 spare

P_FIELDS = [-2.0, 1.0, -100.0, 10000.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# [0xC0000000, 0x3F800000, 0xC2C80000, 0x461C4000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
# 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
# 0x3F800000, 0x3F800000, 0x3F800000]

FAKE_TIME = 0xCCCCCCCC


BYTES_A = bytearray([0x00, 0x00, 0x00, 0x3C, 0x03, 0x88, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x93, 0xF2, 0x77, 0x14, 0x67, 0x89, 0xF1, 0x42, 0x03, 0x05, 0x01, 0x08,
                     0x0A, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x1F,
                     0x00, 0x00, 0x00, 0x05, 0x78, 0x9A, 0xBC, 0x00, 0x00, 0x00, 0x00, 0x00])

BYTES_B = bytearray([0x00, 0x00, 0x00, 0x90, 0x03, 0x88, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x93, 0xF2, 0x77, 0x14, 0x67, 0x89, 0xF1, 0x42, 0x03, 0x05, 0x01, 0x08,
                     0x0A, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x04,
                     0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x1F,
                     0x00, 0x00, 0x00, 0x05, 0x78, 0x9A, 0xBC, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0xC0, 0x00, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0xC2, 0xC8, 0x00, 0x00,
                     0x46, 0x1C, 0x40, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00])


def run904Test():
    test904JSONSimple()
    test904FromBytes()
    test904ToBytes()
    print("904 Air Picture Track: PASS")


def test904JSONSimple():
    msg = r904AirPictureTrack(SEQ_INDEX, SEQ_COUNT, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                              TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                              VALID_TIME)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy

    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                      P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                      P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                      P_FIELDS[20])

    msg2 = r904AirPictureTrack(SEQ_INDEX, SEQ_COUNT, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                              TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                              VALID_TIME, pFields)

    str2 = msg2.toJSON()
    msg2_copy = getMessageFromJSON(str2)
    assert msg2 == msg2_copy


def test904ToBytes():
    msg = r904AirPictureTrack(SEQ_INDEX, SEQ_COUNT, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                              TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                              VALID_TIME)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r904 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES_A, 'First byte array failed: r904 toBytes'

    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                      P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                      P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                      P_FIELDS[20])

    msg2 = r904AirPictureTrack(SEQ_INDEX, SEQ_COUNT, SYS_TRACK_ID, TRACK_ID, TRACK_CLASS, SIM_FLAG, POS_TQ, VEL_TQ,
                              TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                              VALID_TIME, pFields)
    msg2.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg2.getByteArray() == BYTES_B, 'Second byte array failed: r904 toBytes'


def test904FromBytes():
    msg = getMessageFromBytes(BYTES_A)
    assert msg.header.messageLength.data == MSG_LENGTH_A, 'First Message Length wrong: r904 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'First Message ID wrong: r904 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'First Interface Kind wrong: r904 fromBytes'
    assert msg.header.partCount.data == PART_COUNT_A, 'First Part Count wrong: r904 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'First Transmit Time wrong: r904 fromBytes'

    assert msg.seqIndex.data == SEQ_INDEX, 'First Sequence Index wrong: r904 fromBytes'
    assert msg.seqCount.data == SEQ_COUNT, 'First Sequence Count wrong: r904 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'First System Track ID wrong: r904 fromBytes'
    assert msg.trackId.data == TRACK_ID, 'First Track Identity wrong: r904 fromBytes'
    assert msg.trackClass.data == TRACK_CLASS, 'First Track Classification wrong: r904 fromBytes'
    assert msg.simFlag.data == SIM_FLAG, 'First Simulated Flag wrong: r904 fromBytes'
    assert msg.posTQ.data == POS_TQ, 'First Position TQ wrong: r904 fromBytes'
    assert msg.velTQ.data == VEL_TQ, 'First Velocity TQ wrong: r904 fromBytes'
    assert msg.trackECEF_X.data == TRACK_ECEF_X, 'First Track ECEF X wrong: r904 fromBytes'
    assert msg.trackECEF_Y.data == TRACK_ECEF_Y, 'First Track ECEF Y wrong: r904 fromBytes'
    assert msg.trackECEF_Z.data == TRACK_ECEF_Z, 'First Track ECEF Z wrong: r904 fromBytes'
    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'First Track ECEF Vx wrong: r904 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'First Track ECEF Vy wrong: r904 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'First Track ECEF Vz wrong: r904 fromBytes'
    assert msg.validTime.data == VALID_TIME, 'First Valid Time wrong: r904 fromBytes'

    msg2 = getMessageFromBytes(BYTES_B)
    assert msg2.header.messageLength.data == MSG_LENGTH_B, 'Second Message Length wrong: r904 fromBytes'
    assert msg2.header.messageId.data == MSG_ID, 'Second Message ID wrong: r904 fromBytes'
    assert msg2.header.interfaceKind.data == KIND, 'Second Interface Kind wrong: r904 fromBytes'
    assert msg2.header.partCount.data == PART_COUNT_B, 'Second Part Count wrong: r904 fromBytes'
    assert msg2.header.transmitTime.data == FAKE_TIME, 'Second Transmit Time wrong: r904 fromBytes'

    assert msg2.seqIndex.data == SEQ_INDEX, 'Second Sequence Index wrong: r904 fromBytes'
    assert msg2.seqCount.data == SEQ_COUNT, 'Second Sequence Count wrong: r904 fromBytes'
    assert msg2.sysTrackId.data == SYS_TRACK_ID, 'Second System Track ID wrong: r904 fromBytes'
    assert msg2.trackId.data == TRACK_ID, 'Second Track Identity wrong: r904 fromBytes'
    assert msg2.trackClass.data == TRACK_CLASS, 'Second Track Classification wrong: r904 fromBytes'
    assert msg2.simFlag.data == SIM_FLAG, 'Second Simulated Flag wrong: r904 fromBytes'
    assert msg2.posTQ.data == POS_TQ, 'Second Position TQ wrong: r904 fromBytes'
    assert msg2.velTQ.data == VEL_TQ, 'Second Velocity TQ wrong: r904 fromBytes'
    assert msg2.trackECEF_X.data == TRACK_ECEF_X, 'Second Track ECEF X wrong: r904 fromBytes'
    assert msg2.trackECEF_Y.data == TRACK_ECEF_Y, 'Second Track ECEF Y wrong: r904 fromBytes'
    assert msg2.trackECEF_Z.data == TRACK_ECEF_Z, 'Second Track ECEF Z wrong: r904 fromBytes'
    assert msg2.trackECEF_Vx.data == TRACK_ECEF_VX, 'Second Track ECEF Vx wrong: r904 fromBytes'
    assert msg2.trackECEF_Vy.data == TRACK_ECEF_VY, 'Second Track ECEF Vy wrong: r904 fromBytes'
    assert msg2.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Second Track ECEF Vz wrong: r904 fromBytes'
    assert msg2.validTime.data == VALID_TIME, 'Second Valid Time wrong: r904 fromBytes'
   
    msg2p = msg2.pFields.allFields()
    for i in range(0, len(P_FIELDS)):
        assert P_FIELDS[i] == msg2p[i].data
