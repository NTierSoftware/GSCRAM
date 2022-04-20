# t925Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/13/2018

from CRAMmsg.t925InterceptorStatus import t925InterceptorStatus
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 96
MSG_ID = 925
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0x8731
PLAN_ID = 0x0F33
SYS_TRACK_ID = 0x1235ADE1

# ECEF_X = -1  # 0xFFFFFFFF
# ECEF_Y = 1  # 0x00000001
# ECEF_Z = -3  # 0xFFFFFFFD

LOCAL_TRACK_ID = 0x3E41
INTERCEPTOR_ID = 0x8731 #Note: We make the interceptorId = to the weaponId, this may change if we deploy multiple drones to target.
# INTERCEPTOR_ID = 0x0919
INTERCEPTOR_STATUS = 0x06
MISSION_STATUS = 0x02
ESAD_STATE = 0x0003

ECEF_X = -1  # 0xFFFFFFFF
ECEF_Y = 1  # 0x00000001
ECEF_Z = -3  # 0xFFFFFFFD

TRACK_ECEF_VX = -4  # 0xFFFFFFFC
TRACK_ECEF_VY = -6  # 0xFFFFFFFA
TRACK_ECEF_VZ = -8  # 0xFFFFFFF8
YAW = 0x0019
PITCH = -100  # 0xFF9C
ROLL = -2  # 0xFFFE
SEEKER_RANGE = 0x98765432
VALID_TIME = 0x2A10B791
BATTERY_LIFE = -5  # 0xFFFFFFFB
TIME_TO_GO = -7  # 0xFFFFFFF9
RANGE_TO_GO = 0x02101717
SEEKER_AZIMUTH = -99  # 0xFF9D
SEEKER_ELEV = 12  # 0x000C
SEEKER_RANGE_RATE = -10  # 0xFFFFFFF6
INDICATED_AIR_SPEED = -12  # 0xFFFFFFF4
GPS_PDOP = 0x03


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x60, 0x03, 0x9D, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   # 0x87, 0x31, 0x0F, 0x33, 0x12, 0x35, 0xAD, 0xE1, 0x3E, 0x41, 0x09, 0x19,
                   0x87, 0x31, 0x0F, 0x33, 0x12, 0x35, 0xAD, 0xE1,

                   # 0xFF, 0xFF, 0xFF, 0xFF,
                   # 0x00, 0x00, 0x00, 0x01,
                   # 0xFF, 0xFF, 0xFF, 0xFD,
                   #
                   0x3E, 0x41, 0x87, 0x31,
                   0x06, 0x02, 0x00, 0x03,

                   0xFF, 0xFF, 0xFF, 0xFF,
                   0x00, 0x00, 0x00, 0x01,
                   0xFF, 0xFF, 0xFF, 0xFD,

                   0xFF, 0xFF, 0xFF, 0xFC,
                   0xFF, 0xFF, 0xFF, 0xFA,
                   0xFF, 0xFF, 0xFF, 0xF8,

                   0x00, 0x19, 0xFF, 0x9C, 0xFF, 0xFE, 0x00, 0x00,
                   0x98, 0x76, 0x54, 0x32, 0x2A, 0x10, 0xB7, 0x91, 0xFF, 0xFF, 0xFF, 0xFB,
                   0xFF, 0xFF, 0xFF, 0xF9, 0x02, 0x10, 0x17, 0x17, 0xFF, 0x9D, 0x00, 0x0C,
                   0xFF, 0xFF, 0xFF, 0xF6, 0xFF, 0xFF, 0xFF, 0xF4, 0x03, 0x00, 0x00, 0x00])


def run925Test():
    test925JSONSimple()
    test925FromBytes()
    test925ToBytes()
    print("925 drone Status: PASS")


def test925JSONSimple():
    msg = t925InterceptorStatus(WEAPON_ID, PLAN_ID, SYS_TRACK_ID,
                                LOCAL_TRACK_ID, INTERCEPTOR_ID, INTERCEPTOR_STATUS,
                                MISSION_STATUS, ESAD_STATE,
                                ECEF_X, ECEF_Y, ECEF_Z,
                                TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                                YAW, PITCH, ROLL, SEEKER_RANGE, VALID_TIME, BATTERY_LIFE, TIME_TO_GO,
                                RANGE_TO_GO, SEEKER_AZIMUTH, SEEKER_ELEV, SEEKER_RANGE_RATE, INDICATED_AIR_SPEED,
                                GPS_PDOP)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: t925'


def test925ToBytes():
    # msg = t925InterceptorStatus(WEAPON_ID, PLAN_ID, SYS_TRACK_ID, LOCAL_TRACK_ID, INTERCEPTOR_ID, INTERCEPTOR_STATUS,
    #                             MISSION_STATUS, ESAD_STATE, ECEF_X, ECEF_Y, ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY,
    #                             TRACK_ECEF_VZ, YAW, PITCH, ROLL, SEEKER_RANGE, VALID_TIME, BATTERY_LIFE, TIME_TO_GO,
    #                             RANGE_TO_GO, SEEKER_AZIMUTH, SEEKER_ELEV, SEEKER_RANGE_RATE, INDICATED_AIR_SPEED,
    #                             GPS_PDOP)
    msg = t925InterceptorStatus(WEAPON_ID, PLAN_ID, SYS_TRACK_ID,
                                LOCAL_TRACK_ID, INTERCEPTOR_ID, INTERCEPTOR_STATUS,
                                MISSION_STATUS, ESAD_STATE,
                                ECEF_X, ECEF_Y, ECEF_Z,
                                TRACK_ECEF_VX, TRACK_ECEF_VY,
                                TRACK_ECEF_VZ, YAW, PITCH, ROLL, SEEKER_RANGE, VALID_TIME, BATTERY_LIFE, TIME_TO_GO,
                                RANGE_TO_GO, SEEKER_AZIMUTH, SEEKER_ELEV, SEEKER_RANGE_RATE, INDICATED_AIR_SPEED,
                                GPS_PDOP)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t925 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t925 toBytes'


def test925FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t925 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t925 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t925 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t925 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t925 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t925 fromBytes'
    assert msg.planId.data == PLAN_ID, 'Plan ID wrong: t925 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'System Track ID wrong: t925 fromBytes'

    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'Local Track ID wrong: t925 fromBytes'
    # assert msg.interceptorId.data == INTERCEPTOR_ID, 'drone ID wrong: t925 fromBytes'
    assert msg.interceptorStatus.data == INTERCEPTOR_STATUS, 'drone Status wrong: t925 fromBytes'
    assert msg.missionStatus.data == MISSION_STATUS, 'Mission Status wrong: t925 fromBytes'
    assert msg.ESAD_State.data == ESAD_STATE, 'ESAD State wrong: t925 fromBytes'

    assert msg.ECEF_X.data == ECEF_X, 'ECEF X wrong: t925 fromBytes'
    assert msg.ECEF_Y.data == ECEF_Y, 'ECEF Y wrong: t925 fromBytes'
    assert msg.ECEF_Z.data == ECEF_Z, 'ECEF Z wrong: t925 fromBytes'

    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'Track ECEF Vx wrong: t925 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'Track ECEF Vy wrong: t925 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Track ECEF Vz wrong: t925 fromBytes'
    assert msg.yaw.data == YAW, 'Yaw wrong: t925 fromBytes'
    assert msg.pitch.data == PITCH, 'Pitch wrong: t925 fromBytes'
    assert msg.roll.data == ROLL, 'Roll wrong: t925 fromBytes'
    assert msg.seekerRange.data == SEEKER_RANGE, 'Seeker Range wrong: t925 fromBytes'
    assert msg.validTime.data == VALID_TIME, 'Valid Time wrong: t925 fromBytes'
    assert msg.batteryLife.data == BATTERY_LIFE, 'Battery Life wrong: t925 fromBytes'
    assert msg.timeToGo.data == TIME_TO_GO, 'Time to Go wrong: t925 fromBytes'
    assert msg.rangeToGo.data == RANGE_TO_GO, 'Range to Go wrong: t925 fromBytes'
    assert msg.seekerAzimuth.data == SEEKER_AZIMUTH, 'Seeker Azimuth wrong: t925 fromBytes'
    assert msg.seekerElev.data == SEEKER_ELEV, 'Seeker Elevation wrong: t925 fromBytes'
    assert msg.seekerRangeRate.data == SEEKER_RANGE_RATE, 'Seeker Range Rate wrong: t925 fromBytes'
    assert msg.indicatedAirSpeed.data == INDICATED_AIR_SPEED, 'Indicated Air Speed wrong: t925 fromBytes'
    assert msg.GPS_PDOP.data == GPS_PDOP, 'GPS PDOP wrong: t925 fromBytes'

