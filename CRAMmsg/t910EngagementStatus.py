#  author: Alex Erf, Airspace, alex.erf@airspace.co, created: 8/10/2018
from enum import Enum
from typing import List
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Element import Element
from CRAMmsg.ElementInt32 import ElementInt32
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.Header import Header, HeaderConsts
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue
from Utilities.Wrap import wrap

class t910Consts:
    class EngagementStatus(Enum):
        PENDING_RELEASE = ElementUInt8(1)
        INTENT_TO_FIRE = ElementUInt8(2)
        MISSILE_COMMITTED = ElementUInt8(3)
        MISSILE_READY = ElementUInt8(4)
        MISSILE_FIRING = ElementUInt8(5)
        MISSILE_AWAY = ElementUInt8(6)
        FIRING = ElementUInt8(7)
        FIRING_ENDED = ElementUInt8(8)

        # CantCo Responses
        NON_OPERATIONAL = ElementUInt8(11)
        OUT_OF_INVENTORY = ElementUInt8(12)
        CONSTRAINT_VIOLATION_OTHER = ElementUInt8(13)
        SENSOR_RESOURCE_VIOLATION = ElementUInt8(14)
        AIR_TRACK_AVOIDANCE_VIOLATION = ElementUInt8(15)
        SENSOR_FAILED_ACQUISITION = ElementUInt8(16)
        PKILL_REQ_NOT_MET = ElementUInt8(17)
        # 18 is reserved for future CantCo use
        CANT_CO_OTHER = ElementUInt8(19)

        # EB = Engagement Broken
        EB_OUTSIDE_DEFENDED_AREA = ElementUInt8(21)
        EB_KILLED                = ElementUInt8(22)
        EB_NOT_KILLED            = ElementUInt8(23)
        EB_C2DIR_912DNE          = ElementUInt8(24)
        EB_C2DIR_ABORT           = ElementUInt8(25)
        EB_HANG_FIRE             = ElementUInt8(26)
        EB_OPERATOR              = ElementUInt8(27)
        # 28 - 30 Reserved for future EB use
        EB_OTHER = ElementUInt8(31)

        # Constraint Violation Responses
        CONSTRAINT_VIOLATION_ALT = ElementUInt8(32)
        CONSTRAINT_VIOLATION_LAUNCH_ANGLE = ElementUInt8(33)
        CONSTRAINT_VIOLATION_PREP_SLEW_TIME = ElementUInt8(34)
        CONSTRAINT_VIOLATION_ENGAGEMENT_ANGLE = ElementUInt8(35)
        CONSTRAINT_VIOLATION_BI_STATIC_ANGLE = ElementUInt8(36)
        CONSTRAINT_VIOLATION_DOPPLER_CROSSOVER = ElementUInt8(37)
        CONSTRAINT_VIOLATION_MANEUVER_ENDGAME = ElementUInt8(38)
        CONSTRAINT_VIOLATION_MAX_RANGE = ElementUInt8(39)
        # >39 reserved for future use

    class InterceptorId(Enum): NO_STATEMENT = ElementUInt16(0)
    class SysTrackId(Enum)   : NO_STATEMENT = ElementUInt32(0)
    class LocalTrackId(Enum) : NO_STATEMENT = ElementUInt16(0)
    class WpnFreeTime(Enum)  : NO_STATEMENT = ElementUInt32(4294967295)

    class TrackECEF_X(Enum): NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Y(Enum): NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Z(Enum): NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Vx(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TrackECEF_Vy(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TrackECEF_Vz(Enum): NO_STATEMENT = ElementInt32(-2147483648)

    class LaunchTime(Enum): NO_STATEMENT = ElementUInt32(4294967295)

class t910EngagementStatus(CRAMBaseMessage):
    MSG_LEN = 92
    MSG_ID = 910
    PART_COUNT = 0

    def __init__(self, planId, weaponId, engagementStatus, interceptorId, sysTrackId, localTrackId, estPKill,
                 launchTime, interceptTime, wpnFreeTime, launchAzimuth, launchElev,
                 trackECEF_X, trackECEF_Y, trackECEF_Z,
                 trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
                 earliestLaunchTime, latestLaunchTime,
                 header: Header=None):
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.planId = wrap(planId, ElementUInt16)
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.spare1 = ElementUInt8(0)
        self.engagementStatus = wrap(engagementStatus, ElementUInt8)
        self.interceptorId = wrap(interceptorId, ElementUInt16)
        self.sysTrackId = wrap(sysTrackId, ElementUInt32)
        self.localTrackId = wrap(localTrackId, ElementUInt16)
        self.spare2 = ElementUInt16(0)
        self.estPKill = wrap(estPKill, ElementUInt32)
        self.launchTime = wrap(launchTime, ElementUInt32)
        self.interceptTime = wrap(interceptTime, ElementUInt32)
        self.wpnFreeTime = wrap(wpnFreeTime, ElementUInt32)
        self.launchAzimuth = wrap(launchAzimuth, ElementUInt32)
        self.launchElev = wrap(launchElev, ElementInt32)
        self.trackECEF_X = wrap(trackECEF_X, ElementInt32)
        self.trackECEF_Y = wrap(trackECEF_Y, ElementInt32)
        self.trackECEF_Z = wrap(trackECEF_Z, ElementInt32)

        self.trackECEF_Vx = t910Consts.TrackECEF_Vx.NO_STATEMENT.value
        self.trackECEF_Vy = t910Consts.TrackECEF_Vy.NO_STATEMENT.value
        self.trackECEF_Vz = t910Consts.TrackECEF_Vz.NO_STATEMENT.value

        self.earliestLaunchTime = wrap(earliestLaunchTime, ElementUInt32)
        self.latestLaunchTime = wrap(latestLaunchTime, ElementUInt32)
        self.spare3 = ElementUInt32(0)
        self.spare4 = ElementUInt32(0)

    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 910 Command's data fields in order."""
        return [self.header, self.planId, self.weaponId, self.spare1, self.engagementStatus, self.interceptorId,
                self.sysTrackId, self.localTrackId, self.spare2, self.estPKill, self.launchTime, self.interceptTime,
                 self.wpnFreeTime, self.launchAzimuth, self.launchElev, self.trackECEF_X, self.trackECEF_Y,
                self.trackECEF_Z, self.trackECEF_Vx, self.trackECEF_Vy, self.trackECEF_Vz, self.earliestLaunchTime,
                self.latestLaunchTime, self.spare3, self.spare4]

    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 910 Command's data fields' names in order."""
        return ['messageHeader', 'planId', 'weaponId', 'spare1', 'engagementStatus', 'interceptorId', 'sysTrackId',
                'localTrackId', 'spare2', 'estPKill', 'launchTime', 'interceptTime', 'wpnFreeTime', 'launchAzimuth',
                'launchElev', 'trackECEF_X', 'trackECEF_Y', 'trackECEF_Z', 'trackECEF_Vx', 'trackECEF_Vy',
                'trackECEF_Vz', 'earliestLaunchTime', 'latestLaunchTime', 'spare3', 'spare4']

    def getAllEnumGroups(self) -> List:
        return [None, None, None, None, t910Consts.EngagementStatus, t910Consts.InterceptorId, t910Consts.SysTrackId,
                t910Consts.LocalTrackId, None, None, None, None, None, t910Consts.WpnFreeTime, None, None,
                t910Consts.TrackECEF_X, t910Consts.TrackECEF_Y, t910Consts.TrackECEF_Z,
                t910Consts.TrackECEF_Vx, t910Consts.TrackECEF_Vy, t910Consts.TrackECEF_Vz,
                t910Consts.LaunchTime, t910Consts.LaunchTime, None, None]

    def getNumBytes(self) -> int: return self.MSG_LEN

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        planId = ElementUInt16.genFromBytes(byteList[12:14])
        weaponId = ElementUInt16.genFromBytes(byteList[14:16])
        # byte 16 is for spare
        engagementStatus = ElementUInt8.genFromBytes(byteList[17:18])
        interceptorId = ElementUInt16.genFromBytes(byteList[18:20])
        sysTrackId = ElementUInt32.genFromBytes(byteList[20:24])
        localTrackId = ElementUInt16.genFromBytes(byteList[24:26])
        # bytes 26 - 27 are for spare
        estPKill = ElementUInt32.genFromBytes(byteList[28:32])
        launchTime = ElementUInt32.genFromBytes(byteList[32:36])
        interceptTime = ElementUInt32.genFromBytes(byteList[36:40])
        wpnFreeTime = ElementUInt32.genFromBytes(byteList[40:44])
        launchAzimuth = ElementUInt32.genFromBytes(byteList[44:48])
        launchElev = ElementInt32.genFromBytes(byteList[48:52])
        trackECEF_X = ElementInt32.genFromBytes(byteList[52:56])
        trackECEF_Y = ElementInt32.genFromBytes(byteList[56:60])
        trackECEF_Z = ElementInt32.genFromBytes(byteList[60:64])
        trackECEF_Vx = ElementInt32.genFromBytes(byteList[64:68])
        trackECEF_Vy = ElementInt32.genFromBytes(byteList[68:72])
        trackECEF_Vz = ElementInt32.genFromBytes(byteList[72:76])
        earliestLaunchTime = ElementUInt32.genFromBytes(byteList[76:80])
        latestLaunchTime = ElementUInt32.genFromBytes(byteList[80:84])
        # bytes 84 - 91 are for spare
        return cls(planId, weaponId, engagementStatus, interceptorId, sysTrackId, localTrackId, estPKill, launchTime,
                   interceptTime, wpnFreeTime, launchAzimuth, launchElev,
                   trackECEF_X, trackECEF_Y, trackECEF_Z,
                   trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
                   earliestLaunchTime, latestLaunchTime, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        engagementStatus = objectToValue(objDict['engagementStatus'], t910Consts.EngagementStatus)
        interceptorId = objectToValue(objDict['interceptorId'], t910Consts.InterceptorId)
        sysTrackId = objectToValue(objDict['sysTrackId'], t910Consts.SysTrackId)
        localTrackId = objectToValue(objDict['localTrackId'], t910Consts.LocalTrackId)
        wpnFreeTime = objectToValue(objDict['wpnFreeTime'], t910Consts.WpnFreeTime)
        trackECEF_X = objectToValue(objDict['trackECEF_X'], t910Consts.TrackECEF_X)
        trackECEF_Y = objectToValue(objDict['trackECEF_Y'], t910Consts.TrackECEF_Y)
        trackECEF_Z = objectToValue(objDict['trackECEF_Z'], t910Consts.TrackECEF_Z)
        trackECEF_Vx = objectToValue(objDict['trackECEF_Vx'], t910Consts.TrackECEF_Vx)
        trackECEF_Vy = objectToValue(objDict['trackECEF_Vy'], t910Consts.TrackECEF_Vy)
        trackECEF_Vz = objectToValue(objDict['trackECEF_Vz'], t910Consts.TrackECEF_Vz)
        earliestLaunchTime = objectToValue(objDict['earliestLaunchTime'], t910Consts.LaunchTime)
        latestLaunchTime = objectToValue(objDict['latestLaunchTime'], t910Consts.LaunchTime)

        return cls(objDict['planId'], objDict['weaponId'], engagementStatus, interceptorId, sysTrackId, localTrackId,
                   objDict['estPKill'], objDict['launchTime'], objDict['interceptTime'], wpnFreeTime,
                   objDict['launchAzimuth'], objDict['launchElev'],
                   trackECEF_X, trackECEF_Y, trackECEF_Z,
                   trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
                   earliestLaunchTime, latestLaunchTime, header)


