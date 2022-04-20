# r909Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/10/2018

from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.r909EngagementPlan import r909EngagementPlan
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 136
MSG_ID = 909
KIND = HeaderConsts.InterfaceKind.AI3.value.data
PART_COUNT = 0
FAKE_TIME = 0xCCCCCCCC

PLAN_ID = 0x2019
WEAPON_ID = 0x3847
FIRING_UNIT_ID = 0x0121
FCR_ID = 0x01
TRACK_CLASS = 0x36
SYS_TRACK_ID = 0x09091231
EARLY_INTERCEPT_TIME = 0x14F1B572
LATE_INTERCEPT_TIME = 0x78102FB3
FCR_CHANNEL = 0x0030
AMBIENT_TEMP = -20000  # 0xB1E0
LAUNCH_TIME = 0x22334455
INTERCEPT_TIME = 0x10890122
LAUNCH_AZIMUTH = 0x239081FE
LAUNCH_ELEV = -345  # 0xFFFFFEA7
LOCAL_TRACK_ID = 0x6734
INTERCEPTOR_ID = 0x12F8
TRACK_ECEF_X = 4  # 0x00000004
TRACK_ECEF_Y = -2  # 0xFFFFFFFE
TRACK_ECEF_Z = 13  # 0x0000000D
TRACK_ECEF_VX = 3  # 0x00000003
TRACK_ECEF_VY = 17  # 0x00000011
TRACK_ECEF_VZ = -16  # 0xFFFFFFF0
TARGET_PRIORITY = 99  # 0x00000063
ESTIMATED_PKILL = 12  # 0x0000000C
EARLY_LAUNCH_TIME = 0x232394A2
LATE_LAUNCH_TIME = 0x0912DDEA
MIN_ELEV = -3  # 0xFFFFFFFD
MAX_ELEV = 3  # 0x00000003
MIN_AZIMUTH = 0x08A431BC
MAX_AZIMUTH = 0xFF41FF45
MISSILE_KIND = 0x01
TRACK_MANEUVER = 0x02
MISSILE_IN_FLIGHT = 0x01
TRAJECTORY_SHAPE = 0x00


BYTES = bytearray([0x00, 0x00, 0x00, 0x88, 0x03, 0x8D, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x20, 0x19, 0x38, 0x47, 0x01, 0x21, 0x01, 0x36, 0x09, 0x09, 0x12, 0x31,
                   0x14, 0xF1, 0xB5, 0x72, 0x78, 0x10, 0x2F, 0xB3, 0x00, 0x30, 0xB1, 0xE0,
                   0x22, 0x33, 0x44, 0x55, 0x00, 0x00, 0x00, 0x00, 0x10, 0x89, 0x01, 0x22,
                   0x23, 0x90, 0x81, 0xFE, 0xFF, 0xFF, 0xFE, 0xA7, 0x67, 0x34, 0x12, 0xF8,
                   0x00, 0x00, 0x00, 0x04, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x0D,
                   0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x11, 0xFF, 0xFF, 0xFF, 0xF0,
                   0x00, 0x00, 0x00, 0x63, 0x00, 0x00, 0x00, 0x0C, 0x23, 0x23, 0x94, 0xA2,
                   0x09, 0x12, 0xDD, 0xEA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFD, 0x00, 0x00, 0x00, 0x03,
                   0x08, 0xA4, 0x31, 0xBC, 0xFF, 0x41, 0xFF, 0x45, 0x01, 0x02, 0x01, 0x00,
                   0x00, 0x00, 0x00, 0x00])


def run909Test():
    test909JSONSimple()
    test909FromBytes()
    test909ToBytes()
    print("909 Engagement Plan: PASS")


def test909JSONSimple():
    msg = r909EngagementPlan(PLAN_ID, WEAPON_ID, FIRING_UNIT_ID, FCR_ID, TRACK_CLASS, SYS_TRACK_ID,
                             EARLY_INTERCEPT_TIME, LATE_INTERCEPT_TIME, FCR_CHANNEL, AMBIENT_TEMP, LAUNCH_TIME,
                             INTERCEPT_TIME, LAUNCH_AZIMUTH, LAUNCH_ELEV, LOCAL_TRACK_ID, INTERCEPTOR_ID,
                             TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                             TARGET_PRIORITY, ESTIMATED_PKILL, EARLY_LAUNCH_TIME, LATE_LAUNCH_TIME, MIN_ELEV,
                             MAX_ELEV, MIN_AZIMUTH, MAX_AZIMUTH, MISSILE_KIND, TRACK_MANEUVER, MISSILE_IN_FLIGHT,
                             TRAJECTORY_SHAPE)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test909ToBytes():
    msg = r909EngagementPlan(PLAN_ID, WEAPON_ID, FIRING_UNIT_ID, FCR_ID, TRACK_CLASS, SYS_TRACK_ID,
                             EARLY_INTERCEPT_TIME, LATE_INTERCEPT_TIME, FCR_CHANNEL, AMBIENT_TEMP, LAUNCH_TIME,
                             INTERCEPT_TIME, LAUNCH_AZIMUTH, LAUNCH_ELEV, LOCAL_TRACK_ID, INTERCEPTOR_ID,
                             TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                             TARGET_PRIORITY, ESTIMATED_PKILL, EARLY_LAUNCH_TIME, LATE_LAUNCH_TIME, MIN_ELEV,
                             MAX_ELEV, MIN_AZIMUTH, MAX_AZIMUTH, MISSILE_KIND, TRACK_MANEUVER, MISSILE_IN_FLIGHT,
                             TRAJECTORY_SHAPE)

    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r909 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r909 toBytes'


def test909FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r909 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r909 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r909 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r909 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r909 fromBytes'

    assert msg.planId.data == PLAN_ID, 'Plan ID wrong: r909 fromBytes'
    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: r909 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID, 'Firing Unit ID wrong: r909 fromBytes'
    assert msg.FCRId.data == FCR_ID, 'FCR ID wrong: r909 fromBytes'
    assert msg.trackClass.data == TRACK_CLASS, 'Track Classification wrong: r909 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'System Track ID wrong: r909 fromBytes'
    assert msg.earliestInterceptTime.data == EARLY_INTERCEPT_TIME, 'Earliest Intercept Time wrong: r909 fromBytes'
    assert msg.latestInterceptTime.data == LATE_INTERCEPT_TIME, 'Latest Intercept Time wrong: r909 fromBytes'
    assert msg.FCRChannel.data == FCR_CHANNEL, 'FCR Channel wrong: r909 fromBytes'
    assert msg.ambientTemp.data == AMBIENT_TEMP, 'Ambient Temperature wrong: r909 fromBytes'
    assert msg.launchTime.data == LAUNCH_TIME, 'Launch Time wrong: r909 fromBytes'
    assert msg.InterceptTime.data == INTERCEPT_TIME, 'Intercept Time wrong: r909 fromBytes'
    assert msg.launchAzimuth.data == LAUNCH_AZIMUTH, 'Launch Azimuth wrong: r909 fromBytes'
    assert msg.launchElev.data == LAUNCH_ELEV, 'Launch Elevation wrong: r909 fromBytes'
    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'Local Track ID wrong: r909 fromBytes'
    assert msg.interceptorId.data == INTERCEPTOR_ID, 'drone ID wrong: r909 fromBytes'
    assert msg.trackECEF_X.data == TRACK_ECEF_X, 'Track ECEF X wrong: r909 fromBytes'
    assert msg.trackECEF_Y.data == TRACK_ECEF_Y, 'Track ECEF Y wrong: r909 fromBytes'
    assert msg.trackECEF_Z.data == TRACK_ECEF_Z, 'Track ECEF Z wrong: r909 fromBytes'
    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'Track ECEF Vx wrong: r909 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'Track ECEF Vy wrong: r909 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Track ECEF Vz wrong: r909 fromBytes'
    assert msg.targetPriority.data == TARGET_PRIORITY, 'Target Priority wrong: r909 fromBytes'
    assert msg.estPKill.data == ESTIMATED_PKILL, 'Estimated PKill wrong: r909 fromBytes'
    assert msg.earliestLaunchTime.data == EARLY_LAUNCH_TIME, 'Earliest Launch Time wrong: r909 fromBytes'
    assert msg.latestLaunchTime.data == LATE_LAUNCH_TIME, 'Latest Launch Time wrong: r909 fromBytes'
    assert msg.minElev.data == MIN_ELEV, 'Min Elevation wrong: r909 fromBytes'
    assert msg.maxElev.data == MAX_ELEV, 'Max Elevation wrong: r909 fromBytes'
    assert msg.minAzimuth.data == MIN_AZIMUTH, 'Min Azimuth wrong: r909 fromBytes'
    assert msg.maxAzimuth.data == MAX_AZIMUTH, 'Max Azimuth wrong: r909 fromBytes'
    assert msg.missileKind.data == MISSILE_KIND, 'Missile Kind wrong: r909 fromBytes'
    assert msg.trackManeuver.data == TRACK_MANEUVER, 'Track Maneuver wrong: r909 fromBytes'
    assert msg.missileInFlight.data == MISSILE_IN_FLIGHT, 'Missile In Flight wrong: r909 fromBytes'
    assert msg.trajectoryShape.data == TRAJECTORY_SHAPE, 'Trajectory Shape wrong: r909 fromBytes'

