# t910Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/13/2018

from CRAMmsg.t910EngagementStatus import t910EngagementStatus
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 92
MSG_ID = 910
KIND = 0
PART_COUNT = 0

PLAN_ID = 0x71A1
WEAPON_ID = 0xD3F2
ENGAGEMENT_STATUS = 0x03
INTERCEPTOR_ID = 0x1A79
SYSTEM_TRACK_ID = 0x9781DD10
LOCAL_TRACK_ID = 0xFFFE
EST_PKILL = 0x00C21107
LAUNCH_TIME = 0x62A10910
INTERCEPT_TIME = 0x92817381
WPN_FREE_TIME = 0xABCDEF33
LAUNCH_AZIMUTH = 0x90103A41
LAUNCH_ELEV = -50000  # 0xFFFF3CB0
TRACK_ECEF_X = -92  # 0xFFFFFFA4
TRACK_ECEF_Y = -268435455  # 0xF0000001
TRACK_ECEF_Z = 50  # 0x00000032
TRACK_ECEF_VX = -1  # 0xFFFFFFFF
TRACK_ECEF_VY = 2  # 0x00000002
TRACK_ECEF_VZ = 7  # 0x00000007
EARLY_LAUNCH_TIME = 0x88008800
LATE_LAUNCH_TIME = 0x71AE8326

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x5C, 0x03, 0x8E, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x71, 0xA1, 0xD3, 0xF2, 0x00, 0x03, 0x1A, 0x79, 0x97, 0x81, 0xDD, 0x10,
                   0xFF, 0xFE, 0x00, 0x00, 0x00, 0xC2, 0x11, 0x07, 0x62, 0xA1, 0x09, 0x10,
                   0x92, 0x81, 0x73, 0x81, 0xAB, 0xCD, 0xEF, 0x33, 0x90, 0x10, 0x3A, 0x41,
                   0xFF, 0xFF, 0x3C, 0xB0, 0xFF, 0xFF, 0xFF, 0xA4, 0xF0, 0x00, 0x00, 0x01,
                   0x00, 0x00, 0x00, 0x32, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x02,
                   0x00, 0x00, 0x00, 0x07, 0x88, 0x00, 0x88, 0x00, 0x71, 0xAE, 0x83, 0x26,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def run910Test():
    test910JSONSimple()
    test910FromBytes()
    test910ToBytes()
    print("910 Engagement Status: PASS")


def test910JSONSimple():
    msg = t910EngagementStatus(PLAN_ID, WEAPON_ID, ENGAGEMENT_STATUS, INTERCEPTOR_ID, SYSTEM_TRACK_ID, LOCAL_TRACK_ID,
                               EST_PKILL, LAUNCH_TIME, INTERCEPT_TIME, WPN_FREE_TIME, LAUNCH_AZIMUTH, LAUNCH_ELEV,
                               TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                               EARLY_LAUNCH_TIME, LATE_LAUNCH_TIME)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test910ToBytes():
    msg = t910EngagementStatus(PLAN_ID, WEAPON_ID, ENGAGEMENT_STATUS, INTERCEPTOR_ID, SYSTEM_TRACK_ID, LOCAL_TRACK_ID,
                               EST_PKILL, LAUNCH_TIME, INTERCEPT_TIME, WPN_FREE_TIME, LAUNCH_AZIMUTH, LAUNCH_ELEV,
                               TRACK_ECEF_X, TRACK_ECEF_Y, TRACK_ECEF_Z, TRACK_ECEF_VX, TRACK_ECEF_VY, TRACK_ECEF_VZ,
                               EARLY_LAUNCH_TIME, LATE_LAUNCH_TIME)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t910 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: t910 toBytes'


def test910FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: t910 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: t910 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: t910 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: t910 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t910 fromBytes'

    assert msg.planId.data == PLAN_ID, 'Plan ID wrong: t910 fromBytes'
    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: t910 fromBytes'
    assert msg.engagementStatus.data == ENGAGEMENT_STATUS, 'Engagement Status wrong: t910 fromBytes'
    assert msg.interceptorId.data == INTERCEPTOR_ID, 'drone ID wrong: t910 fromBytes'
    assert msg.sysTrackId.data == SYSTEM_TRACK_ID, 'System Track ID wrong: t910 fromBytes'
    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'Local Track ID wrong: t910 fromBytes'
    assert msg.estPKill.data == EST_PKILL, 'Estimated PKill wrong: t910 fromBytes'
    assert msg.launchTime.data == LAUNCH_TIME, 'Launch Time wrong: t910 fromBytes'
    assert msg.interceptTime.data == INTERCEPT_TIME, 'Intercept Time wrong: t910 fromBytes'
    assert msg.wpnFreeTime.data == WPN_FREE_TIME, 'Wpn Free Time wrong: t910 fromBytes'
    assert msg.launchAzimuth.data == LAUNCH_AZIMUTH, 'Launch Azimuth wrong: t910 fromBytes'
    assert msg.launchElev.data == LAUNCH_ELEV, 'Launch Elevation wrong: t910 fromBytes'
    assert msg.trackECEF_X.data == TRACK_ECEF_X, 'Track ECEF X wrong: t910 fromBytes'
    assert msg.trackECEF_Y.data == TRACK_ECEF_Y, 'Track ECEF Y wrong: t910 fromBytes'
    assert msg.trackECEF_Z.data == TRACK_ECEF_Z, 'Track ECEF Z wrong: t910 fromBytes'
    assert msg.trackECEF_Vx.data == TRACK_ECEF_VX, 'Track ECEF Vx wrong: t910 fromBytes'
    assert msg.trackECEF_Vy.data == TRACK_ECEF_VY, 'Track ECEF Vy wrong: t910 fromBytes'
    assert msg.trackECEF_Vz.data == TRACK_ECEF_VZ, 'Track ECEF Vz wrong: t910 fromBytes'
    assert msg.earliestLaunchTime.data == EARLY_LAUNCH_TIME, 'Earliest Launch Time wrong: t910 fromBytes'
    assert msg.latestLaunchTime.data == LATE_LAUNCH_TIME, 'Latest Launch Time wrong: t910 fromBytes'

