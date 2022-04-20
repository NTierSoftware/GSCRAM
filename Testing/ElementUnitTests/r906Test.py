# t906Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/16/2018

from CRAMmsg.unusedCRAMmsg.r906RAMTrack import r906RAMTrack
from CRAMmsg.Matrix import PMatrix
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH_A = 92
MSG_LENGTH_B = 176
MSG_ID = 906
KIND = 0
PART_COUNT_A = 0
PART_COUNT_B = 1

WEAPON_ID = 0x1234
LOCAL_TRACK_ID = 0x22FF
SYS_TRACK_ID = 0x2701B1C9
POS_TQ = 0x08
VEL_TQ = 0x04
IMPACT_POS_TQ = 0x0A
# uint8 spare
TRACK_CLASS = 0x05
SIM_FLAG = 0x00
DROP_TRACK_FLAG = 0x01
CONFIRM_STATUS = 0x02
BALLISTIC_COEFF = 0x7281FF3E
TRACK_ECEF_X = -1  # 0xFFFFFFFF
TRACK_ECEF_Y = 4  # 0x00000004
TRACK_ECEF_Z = 17  # 0x00000011
TRACK_ECEF_VX = -3  # 0xFFFFFFFD
TRACK_ECEF_VY = 31  # 0x0000001F
TRACK_ECEF_VZ = 5  # 0x00000005
IPP_ECEF_X = -4  # 0xFFFFFFFC
IPP_ECEF_Y = 2  # 0x00000002
IPP_ECEF_Z = 0  # 0x00000000
VALID_TIME = 0x36A981B8
IMPACT_TIME = 0x435476BA
# uint32 spare
# uint32 spare
# uint32 spare
# uint32 spare

P_FIELDS = [-2.0, 1.0, -100.0, 10000.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# [0xC0000000, 0x3F800000, 0xC2C80000, 0x461C4000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
# 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000, 0x3F800000,
# 0x3F800000, 0x3F800000, 0x3F800000]

FAKE_TIME = 0xCCCCCCCC


BYTES_A = bytearray([0x00, 0x00, 0x00, 0x5C, 0x03, 0x8A, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x08, 0x04, 0x0A, 0x00,
                     0x05, 0x00, 0x01, 0x02, 0x72, 0x81, 0xFF, 0x3E, 0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD,
                     0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0xFF, 0xFF, 0xFF, 0xFC,
                     0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x36, 0xA9, 0x81, 0xB8,
                     0x43, 0x54, 0x76, 0xBA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


BYTES_B = bytearray([0x00, 0x00, 0x00, 0xB0, 0x03, 0x8A, 0x00, 0x01, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x12, 0x34, 0x22, 0xFF, 0x27, 0x01, 0xB1, 0xC9, 0x08, 0x04, 0x0A, 0x00,
                     0x05, 0x00, 0x01, 0x02, 0x72, 0x81, 0xFF, 0x3E, 0xFF, 0xFF, 0xFF, 0xFF,
                     0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xFD,
                     0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0xFF, 0xFF, 0xFF, 0xFC,
                     0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x36, 0xA9, 0x81, 0xB8,
                     0x43, 0x54, 0x76, 0xBA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0xC2, 0xC8, 0x00, 0x00, 0x46, 0x1C, 0x40, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00,
                     0x3F, 0x80, 0x00, 0x00, 0x3F, 0x80, 0x00, 0x00])


def run906Test():
    test906JSONSimple()
    test906FromBytes()
    test906ToBytes()
    print("906 RAM Track: PASS")


def test906JSONSimple():
    msg = r906RAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, POS_TQ, VEL_TQ, IMPACT_POS_TQ, TRACK_CLASS, SIM_FLAG,
                       DROP_TRACK_FLAG, CONFIRM_STATUS, BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z,
                       TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, VALID_TIME,
                       IMPACT_TIME)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy

    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                      P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                      P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                      P_FIELDS[20])

    msg2 = r906RAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, POS_TQ, VEL_TQ, IMPACT_POS_TQ, TRACK_CLASS, SIM_FLAG,
                       DROP_TRACK_FLAG, CONFIRM_STATUS, BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z,
                       TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, VALID_TIME,
                       IMPACT_TIME, pFields)
    str2 = msg2.toJSON()
    msg2_copy = getMessageFromJSON(str2)
    assert msg2 == msg2_copy


def test906ToBytes():
    msg = r906RAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, POS_TQ, VEL_TQ, IMPACT_POS_TQ, TRACK_CLASS, SIM_FLAG,
                       DROP_TRACK_FLAG, CONFIRM_STATUS, BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z,
                       TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, VALID_TIME,
                       IMPACT_TIME)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r906 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES_A, 'First byte array failed: r906 toBytes'

    pFields = PMatrix(P_FIELDS[0], P_FIELDS[1], P_FIELDS[2], P_FIELDS[3], P_FIELDS[4], P_FIELDS[5], P_FIELDS[6],
                      P_FIELDS[7], P_FIELDS[8], P_FIELDS[9], P_FIELDS[10], P_FIELDS[11], P_FIELDS[12], P_FIELDS[13],
                      P_FIELDS[14], P_FIELDS[15], P_FIELDS[16], P_FIELDS[17], P_FIELDS[18], P_FIELDS[19],
                      P_FIELDS[20])

    msg2 = r906RAMTrack(WEAPON_ID, LOCAL_TRACK_ID, SYS_TRACK_ID, POS_TQ, VEL_TQ, IMPACT_POS_TQ, TRACK_CLASS, SIM_FLAG,
                       DROP_TRACK_FLAG, CONFIRM_STATUS, BALLISTIC_COEFF, TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z,
                       TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ, IPP_ECEF_X, IPP_ECEF_Y, IPP_ECEF_Z, VALID_TIME,
                       IMPACT_TIME, pFields)
    msg2.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg2.getByteArray() == BYTES_B, 'Second byte array failed: r906 toBytes'


def test906FromBytes():
    msg = getMessageFromBytes(BYTES_A)
    assert msg.header.messageLength.data == MSG_LENGTH_A, 'First Message Length wrong: r906 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'First Message ID wrong: r906 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'First Interface Kind wrong: r906 fromBytes'
    assert msg.header.partCount.data == PART_COUNT_A, 'First Part Count wrong: r906 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'First Transmit Time wrong: r906 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'First Weapon ID wrong: r906 fromBytes'
    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'First Local Track ID wrong: r906 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'First System Track ID wrong: r906 fromBytes'
    assert msg.posTQ.data == POS_TQ, 'First Pos TQ wrong: r906 fromBytes'
    assert msg.velTQ.data == VEL_TQ, 'First Vel TQ wrong: r906 fromBytes'
    assert msg.impactPosTQ.data == IMPACT_POS_TQ, 'First Impact Position TQ wrong: r906 fromBytes'
    assert msg.trackClass.data == TRACK_CLASS, 'First Track Classificatoin wrong: r906 fromBytes'
    assert msg.simFlag.data == SIM_FLAG, 'First Simulated Flag wrong: r906 fromBytes'
    assert msg.dropTrackFlag.data == DROP_TRACK_FLAG, 'First Drop Track Flag wrong: r906 fromBytes'
    assert msg.confirmStatus.data == CONFIRM_STATUS, 'First Confirm Status wrong: r906 fromBytes'
    assert msg.ballisticCoeff.data == BALLISTIC_COEFF, 'First Ballistic Coefficient wrong: r906 fromBytes'
    assert msg.trackECEF_X.data == TRACK_ECEF_X, 'First Track ECEF X wrong: r906 fromBytes'
    assert msg.trackECEF_Y.data == TRACK_ECEF_Y, 'First Track ECEF Y wrong: r906 fromBytes'
    assert msg.trackECEF_Z.data == TRACK_ECEF_Z, 'First Track ECEF Z wrong: r906 fromBytes'
    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'First Track ECEF Vx wrong: r906 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'First Track ECEF Vy wrong: r906 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'First ECEF Vz wrong: r906 fromBytes'
    assert msg.IppECEF_X.data == IPP_ECEF_X, 'First Ipp ECEF X wrong: r906 fromBytes'
    assert msg.IppECEF_Y.data == IPP_ECEF_Y, 'First Ipp ECEF Y wrong: r906 fromBytes'
    assert msg.IppECEF_Z.data == IPP_ECEF_Z, 'First Ipp ECEF Z wrong: r906 fromBytes'
    assert msg.validTime.data == VALID_TIME, 'First Valid Time wrong: r906 fromBytes'
    assert msg.impactTime.data == IMPACT_TIME, 'First Impact Time wrong: r906 fromBytes'

    msg2 = getMessageFromBytes(BYTES_B)
    assert msg2.header.messageLength.data == MSG_LENGTH_B, 'Second Message Length wrong: r906 fromBytes'
    assert msg2.header.messageId.data == MSG_ID, 'Second Message ID wrong: r906 fromBytes'
    assert msg2.header.interfaceKind.data == KIND, 'Second Interface Kind wrong: r906 fromBytes'
    assert msg2.header.partCount.data == PART_COUNT_B, 'Second Part Count wrong: r906 fromBytes'
    assert msg2.header.transmitTime.data == FAKE_TIME, 'Second Transmit Time wrong: r906 fromBytes'

    assert msg2.weaponId.data == WEAPON_ID, 'Second Weapon ID wrong: r906 fromBytes'
    assert msg2.localTrackId.data == LOCAL_TRACK_ID, 'Second Local Track ID wrong: r906 fromBytes'
    assert msg2.sysTrackId.data == SYS_TRACK_ID, 'Second System Track ID wrong: r906 fromBytes'
    assert msg2.posTQ.data == POS_TQ, 'Second Pos TQ wrong: r906 fromBytes'
    assert msg2.velTQ.data == VEL_TQ, 'Second Vel TQ wrong: r906 fromBytes'
    assert msg2.impactPosTQ.data == IMPACT_POS_TQ, 'Second Impact Position TQ wrong: r906 fromBytes'
    assert msg2.trackClass.data == TRACK_CLASS, 'Second Track Classificatoin wrong: r906 fromBytes'
    assert msg2.simFlag.data == SIM_FLAG, 'Second Simulated Flag wrong: r906 fromBytes'
    assert msg2.dropTrackFlag.data == DROP_TRACK_FLAG, 'Second Drop Track Flag wrong: r906 fromBytes'
    assert msg2.confirmStatus.data == CONFIRM_STATUS, 'Second Confirm Status wrong: r906 fromBytes'
    assert msg2.ballisticCoeff.data == BALLISTIC_COEFF, 'Second Ballistic Coefficient wrong: r906 fromBytes'
    assert msg2.trackECEF_X.data == TRACK_ECEF_X, 'Second Track ECEF X wrong: r906 fromBytes'
    assert msg2.trackECEF_Y.data == TRACK_ECEF_Y, 'Second Track ECEF Y wrong: r906 fromBytes'
    assert msg2.trackECEF_Z.data == TRACK_ECEF_Z, 'Second Track ECEF Z wrong: r906 fromBytes'
    assert msg2.trackECEF_Vx.data == TRACK_ECEF_VX, 'Second Track ECEF Vx wrong: r906 fromBytes'
    assert msg2.trackECEF_Vy.data == TRACK_ECEF_VY, 'Second Track ECEF Vy wrong: r906 fromBytes'
    assert msg2.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Second ECEF Vz wrong: r906 fromBytes'
    assert msg2.IppECEF_X.data == IPP_ECEF_X, 'Second Ipp ECEF X wrong: r906 fromBytes'
    assert msg2.IppECEF_Y.data == IPP_ECEF_Y, 'Second Ipp ECEF Y wrong: r906 fromBytes'
    assert msg2.IppECEF_Z.data == IPP_ECEF_Z, 'Second Ipp ECEF Z wrong: r906 fromBytes'
    assert msg2.validTime.data == VALID_TIME, 'Second Valid Time wrong: r906 fromBytes'
    assert msg2.impactTime.data == IMPACT_TIME, 'Second Impact Time wrong: r906 fromBytes'

    msg2p = msg2.pFields.allFields()
    for i in range(0, len(P_FIELDS)):
        assert P_FIELDS[i] == msg2p[i].data, 'P Fields wrong: r906 fromBytes'
