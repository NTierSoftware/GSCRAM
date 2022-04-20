# author: JD, John.JD.Donaldson@airspace.co,
# date created: 8/9/18

from CRAMmsg.Element import Element
from CRAMmsg.Header import Header, HeaderConsts
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.ElementInt16 import ElementInt16
from CRAMmsg.ElementInt32 import ElementInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CoordTransform.CRAMtofromLLA import CRAMpoint, ECEFtofromLLA, LLApoint

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.Wrap import wrap
from Utilities.ValueNameConversion import objectToValue

from typing import List

from enum import Enum


class r909EngagementPlan(CRAMBaseMessage):
    MSG_LEN = 136
    MSG_ID = 909
    PART_COUNT = 0
    
    def __init__(self, planId, weaponId, firingUnitId, FCRId, trackClass, sysTrackId,
                 earliestInterceptTime, latestInterceptTime,
                 FCRChannel, ambientTemp,
                 launchTime, InterceptTime,
                 launchAzimuth, launchElev,
                 localTrackId, interceptorId,
                 trackECEF_X, trackECEF_Y, trackECEF_Z, trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
                 targetPriority, estPKill,
                 earliestLaunchTime, latestLaunchTime,
                 minElev, maxElev,
                 minAzimuth, maxAzimuth,
                 missileKind, trackManeuver, missileInFlight, trajectoryShape,
                 header: Header=None):
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.planId = wrap(planId, ElementUInt16)
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.firingUnitId = wrap(firingUnitId, ElementUInt16)
        self.FCRId = wrap(FCRId, ElementUInt8)
        self.trackClass = wrap(trackClass, ElementUInt8)
        self.sysTrackId = wrap(sysTrackId, ElementUInt32)
        self.earliestInterceptTime = wrap(earliestInterceptTime, ElementUInt32)
        self.latestInterceptTime = wrap(latestInterceptTime, ElementUInt32)
        self.FCRChannel = wrap(FCRChannel, ElementUInt16)
        self.ambientTemp = wrap(ambientTemp, ElementInt16)

        self.launchTime = wrap(launchTime, ElementUInt32)
        self.spare1 = ElementUInt32(0)
        self.InterceptTime = wrap(InterceptTime, ElementUInt32)
        self.launchAzimuth = wrap(launchAzimuth, ElementUInt32)
        self.launchElev = wrap(launchElev, ElementInt32)

        self.localTrackId = wrap(localTrackId, ElementUInt16)
        self.interceptorId = wrap(interceptorId, ElementUInt16)

        self.trackECEF_X = wrap(trackECEF_X, ElementInt32)
        self.trackECEF_Y = wrap(trackECEF_Y, ElementInt32)
        self.trackECEF_Z = wrap(trackECEF_Z, ElementInt32)
        self.trackECEF_Vx = wrap(trackECEF_Vx, ElementInt32)
        self.trackECEF_Vy = wrap(trackECEF_Vy, ElementInt32)
        self.trackECEF_Vz = wrap(trackECEF_Vz, ElementInt32)

        self.targetPriority = wrap(targetPriority, ElementUInt32)
        self.estPKill = wrap(estPKill, ElementUInt32)

        self.earliestLaunchTime = wrap(earliestLaunchTime, ElementUInt32)
        self.latestLaunchTime = wrap(latestLaunchTime, ElementUInt32)

        self.spare2 = ElementUInt32(0)
        self.spare3 = ElementUInt32(0)
        self.spare4 = ElementUInt32(0)

        self.minElev = wrap(minElev, ElementInt32)
        self.maxElev = wrap(maxElev, ElementInt32)

        self.minAzimuth = wrap(minAzimuth, ElementUInt32)
        self.maxAzimuth = wrap(maxAzimuth, ElementUInt32)

        self.missileKind = wrap(missileKind, ElementUInt8)
        self.trackManeuver = wrap(trackManeuver, ElementUInt8)
        self.missileInFlight = wrap(missileInFlight, ElementUInt8)
        self.trajectoryShape = wrap(trajectoryShape, ElementUInt8)
        self.spare5 = ElementUInt32(0)

    def getAllFields(self) -> List[Element]:
        return [self.header, self.planId, self.weaponId, self.firingUnitId, self.FCRId, self.trackClass, self.sysTrackId,
            self.earliestInterceptTime, self.latestInterceptTime,
            self.FCRChannel, self.ambientTemp,
            self.launchTime, self.spare1, self.InterceptTime,
            self.launchAzimuth, self.launchElev,
            self.localTrackId, self.interceptorId,
            self.trackECEF_X, self.trackECEF_Y, self.trackECEF_Z, self.trackECEF_Vx, self.trackECEF_Vy, self.trackECEF_Vz,
            self.targetPriority, self.estPKill,
            self.earliestLaunchTime, self.latestLaunchTime,
            self.spare2, self.spare3, self.spare4,
            self.minElev, self.maxElev,
            self.minAzimuth, self.maxAzimuth,
            self.missileKind, self.trackManeuver, self.missileInFlight, self.trajectoryShape,
            self.spare5]

    
    def getAllFieldNames(self) -> List[str]:
        return ['messageHeader', 'planId', 'weaponId', 'firingUnitId', 'FCRId', 'trackClass', 'sysTrackId',
                'earliestInterceptTime', 'latestInterceptTime',
                'FCRChannel', 'ambientTemp',
                'launchTime', 'spare1', 'InterceptTime',
                'launchAzimuth', 'launchElev',
                'localTrackId', 'interceptorId',
                'trackECEF_X', 'trackECEF_Y', 'trackECEF_Z', 'trackECEF_Vx', 'trackECEF_Vy', 'trackECEF_Vz',
                'targetPriority', 'estPKill',
                'earliestLaunchTime', 'latestLaunchTime',
                'spare2', 'spare3', 'spare4',
                'minElev', 'maxElev',
                'minAzimuth', 'maxAzimuth',
                'missileKind', 'trackManeuver', 'missileInFlight', 'trajectoryShape',
                'spare5']

    def getAllEnumGroups(self):
        return [None, None, None, None, r909Consts.FCRID, r909Consts.TrackClass, None, r909Consts.InterceptTime,
                r909Consts.InterceptTime, r909Consts.FCRChannel, None, r909Consts.LaunchTime, None,
                r909Consts.InterceptTime, r909Consts.LaunchAzimuth, r909Consts.LaunchElevation, r909Consts.LocalTrackID,
                r909Consts.InterceptorID,
                r909Consts.TrackECEF_X, r909Consts.TrackECEF_Y, r909Consts.TrackECEF_Z,
                r909Consts.TrackECEF_Vx, r909Consts.TrackECEF_Vy, r909Consts.TrackECEF_Vz, r909Consts.TargetPriority,
                r909Consts.EstPKill, r909Consts.LaunchTime, r909Consts.LaunchTime, None, None, None,
                r909Consts.Elevation, r909Consts.Elevation, r909Consts.Azimuth, r909Consts.Azimuth,
                r909Consts.MissileKind, r909Consts.TrackManeuver, r909Consts.MissileInFlight,
                r909Consts.TrajectoryShape, None]

    def getNumBytes(self) -> int: return self.MSG_LEN
    
    @classmethod
    def genFromBytes(cls, byteList):
        header = Header.genFromBytes(byteList[0:12])
        planId = ElementUInt16.genFromBytes(byteList[12:14])
        weaponId = ElementUInt16.genFromBytes(byteList[14:16])
        firingUnitId = ElementUInt16.genFromBytes(byteList[16:18])
        FCRId = ElementUInt8.genFromBytes(byteList[18:19])
        trackClass = ElementUInt8.genFromBytes(byteList[19:20])
        sysTrackId = ElementUInt32.genFromBytes(byteList[20:24])

        earliestInterceptTime = ElementUInt32.genFromBytes(byteList[24:28])
        latestInterceptTime = ElementUInt32.genFromBytes(byteList[28:32])

        FCRChannel = ElementUInt16.genFromBytes(byteList[32:34])
        ambientTemp = ElementInt16.genFromBytes(byteList[34:36])
        launchTime = ElementUInt32.genFromBytes(byteList[36:40])
        # bytes 40 - 43 are for spare
        interceptTime = ElementUInt32.genFromBytes(byteList[44:48])
        launchAzimuth = ElementUInt32.genFromBytes(byteList[48:52])
        launchElev = ElementInt32.genFromBytes(byteList[52:56])
        localTrackId = ElementUInt16.genFromBytes(byteList[56:58])
        interceptorId = ElementUInt16.genFromBytes(byteList[58:60])

        trackECEF_X = ElementInt32.genFromBytes(byteList[60:64])
        trackECEF_Y = ElementInt32.genFromBytes(byteList[64:68])
        trackECEF_Z = ElementInt32.genFromBytes(byteList[68:72])
        trackECEF_Vx = ElementInt32.genFromBytes(byteList[72:76])
        trackECEF_Vy = ElementInt32.genFromBytes(byteList[76:80])
        trackECEF_Vz = ElementInt32.genFromBytes(byteList[80:84])

        targetPriority = ElementUInt32.genFromBytes(byteList[84:88])
        estPKill = ElementUInt32.genFromBytes(byteList[88:92])
        earliestLaunchTime = ElementUInt32.genFromBytes(byteList[92:96])
        latestLaunchTime = ElementUInt32.genFromBytes(byteList[96:100])
        # bytes 100 - 111 are for spare
        minElev = ElementInt32.genFromBytes(byteList[112:116])
        maxElev = ElementInt32.genFromBytes(byteList[116:120])
        minAzimuth = ElementUInt32.genFromBytes(byteList[120:124])
        maxAzimuth = ElementUInt32.genFromBytes(byteList[124:128])

        missileKind = ElementUInt8.genFromBytes(byteList[128:129])
        trackManeuver = ElementUInt8.genFromBytes(byteList[129:130])
        missileInFlight = ElementUInt8.genFromBytes(byteList[130:131])
        trajectoryShape = ElementUInt8.genFromBytes(byteList[131:132])
        # bytes 132 - 135 are for spare

        return cls(planId, weaponId, firingUnitId, FCRId, trackClass, sysTrackId,
                   earliestInterceptTime, latestInterceptTime,
                   FCRChannel, ambientTemp, launchTime, interceptTime, launchAzimuth, launchElev, localTrackId, interceptorId,
                   trackECEF_X, trackECEF_Y, trackECEF_Z, trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
                   targetPriority, estPKill,
                   earliestLaunchTime, latestLaunchTime,
                   minElev, maxElev, minAzimuth, maxAzimuth,
                   missileKind, trackManeuver, missileInFlight, trajectoryShape,
                   header)



    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        fcrId = objectToValue(objDict['FCRId'], r909Consts.FCRID)
        trackClass = objectToValue(objDict['trackClass'], r909Consts.TrackClass)
        earliestInterceptTime = objectToValue(objDict['earliestInterceptTime'], r909Consts.InterceptTime)
        latestInterceptTime = objectToValue(objDict['latestInterceptTime'], r909Consts.InterceptTime)
        fcrChannel = objectToValue(objDict['FCRChannel'], r909Consts.FCRChannel)
        launchTime = objectToValue(objDict['launchTime'], r909Consts.LaunchTime)
        interceptTime = objectToValue(objDict['InterceptTime'], r909Consts.InterceptTime)
        launchAzimuth = objectToValue(objDict['launchAzimuth'], r909Consts.LaunchAzimuth)
        launchElev = objectToValue(objDict['launchElev'], r909Consts.LaunchElevation)
        localTrackId = objectToValue(objDict['localTrackId'], r909Consts.LocalTrackID)
        interceptorId = objectToValue(objDict['interceptorId'], r909Consts.InterceptorID)
        trackECEF_X = objectToValue(objDict['trackECEF_X'], r909Consts.TrackECEF_X)
        trackECEF_Y = objectToValue(objDict['trackECEF_Y'], r909Consts.TrackECEF_Y)
        trackECEF_Z = objectToValue(objDict['trackECEF_Z'], r909Consts.TrackECEF_Z)
        trackECEF_Vx = objectToValue(objDict['trackECEF_Vx'], r909Consts.TrackECEF_Vx)
        trackECEF_Vy = objectToValue(objDict['trackECEF_Vy'], r909Consts.TrackECEF_Vy)
        trackECEF_Vz = objectToValue(objDict['trackECEF_Vz'], r909Consts.TrackECEF_Vz)
        targetPriority = objectToValue(objDict['targetPriority'], r909Consts.TargetPriority)
        estPKill = objectToValue(objDict['estPKill'], r909Consts.EstPKill)
        earliestLaunchTime = objectToValue(objDict['earliestLaunchTime'], r909Consts.LaunchTime)
        latestLaunchTime = objectToValue(objDict['latestLaunchTime'], r909Consts.LaunchTime)
        minElev = objectToValue(objDict['minElev'], r909Consts.Elevation)
        maxElev = objectToValue(objDict['maxElev'], r909Consts.Elevation)
        minAzimuth = objectToValue(objDict['minAzimuth'], r909Consts.Azimuth)
        maxAzimuth = objectToValue(objDict['maxAzimuth'], r909Consts.Azimuth)
        missileKind = objectToValue(objDict['missileKind'], r909Consts.MissileKind)
        trackManeuver = objectToValue(objDict['trackManeuver'], r909Consts.TrackManeuver)
        missileInFlight = objectToValue(objDict['missileInFlight'], r909Consts.MissileInFlight)
        trajectoryShape = objectToValue(objDict['trajectoryShape'], r909Consts.TrajectoryShape)

        return cls(
            objDict['planId'], objDict['weaponId'], objDict['firingUnitId'], fcrId,
            trackClass, objDict['sysTrackId'],
            earliestInterceptTime, latestInterceptTime,
            fcrChannel, objDict['ambientTemp'],
            launchTime, interceptTime,
            launchAzimuth, launchElev,
            localTrackId, interceptorId,
            trackECEF_X, trackECEF_Y, trackECEF_Z, trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
            targetPriority, estPKill,
            earliestLaunchTime, latestLaunchTime,
            minElev, maxElev,
            minAzimuth, maxAzimuth,
            missileKind, trackManeuver, missileInFlight, trajectoryShape,
            header
        )

    def toLLA(self) -> LLApoint:
        return ECEFtofromLLA.CRAMtoLLA(CRAMpoint(self.trackECEF_X.data, self.trackECEF_Y.data, self.trackECEF_Z.data))


class r909Consts:

    class FCRID(Enum):
        NO_STATEMENT = ElementUInt8(0)

    class TrackClass(Enum):
        NO_STATEMENT = ElementUInt8(0)
        MORTAR_UNKNOWN = ElementUInt8(1)
        MORTAR_60MM = ElementUInt8(2)
        MORTAR_81MM = ElementUInt8(3)
        MORTAR_120MM = ElementUInt8(4)
        MORTAR_LIGHT = ElementUInt8(5)
        MORTAR_MEDIUM = ElementUInt8(6)
        MORTAR_HEAVY = ElementUInt8(7)
        # 8 - 50 Mortar, Other, TBD
        ROCKET_UNKNOWN = ElementUInt8(51)
        ROCKET_57MM = ElementUInt8(52)
        ROCKET_107MM = ElementUInt8(53)
        ROCKET_122MM = ElementUInt8(54)
        ROCKET_127MM = ElementUInt8(55)
        ROCKET_2_75in = ElementUInt8(56)
        ROCKET_240MM = ElementUInt8(57)
        ROCKET_LIGHT = ElementUInt8(58)
        ROCKET_MEDIUM = ElementUInt8(59)
        ROCKET_HEAVY = ElementUInt8(60)
        # 61 - 100 TBD
        ARTILLERY_UNKNOWN = ElementUInt8(101)
        # 102 - 150 Artillery Other TBD
        SMALL_ARMS = ElementUInt8(151)
        # 152 - 179 For Other Threats TBD
        SURROGATE_UNKNOWN = ElementUInt8(180)
        SURROGATE_CLASS_1 = ElementUInt8(181)
        SURROGATE_CLASS_2 = ElementUInt8(182)
        SURROGATE_CLASS_3 = ElementUInt8(183)
        SURROGATE_CLASS_4 = ElementUInt8(184)
        SURROGATE_CLASS_5 = ElementUInt8(185)
        SURROGATE_CLASS_6 = ElementUInt8(186)
        SURROGATE_CLASS_7 = ElementUInt8(187)
        SURROGATE_CLASS_8 = ElementUInt8(188)
        SURROGATE_CLASS_9 = ElementUInt8(189)
        SURROGATE_OTHER = ElementUInt8(190)
        # 191 - 199 RAM TBD
        BALLISTIC_RAM_UNKNOWN = ElementUInt8(200)
        AIR_TRACK_UNKNOWN = ElementUInt8(201)
        FIXED_WING = ElementUInt8(202)
        ROTARY_WING = ElementUInt8(203)
        CRUISE_MISSILE = ElementUInt8(204)
        UAV = ElementUInt8(205)
        TACTICAL_BALLISTIC_MISSILE = ElementUInt8(206)
        SURFACE_TO_AIR_MISSILE = ElementUInt8(207)
        AIR_TO_SURFACE_MISSILE = ElementUInt8(208)
        GROUND = ElementUInt8(209)
        SURFACE = ElementUInt8(210)
        # 211 - 240 for Other Threats TBD
        AI3_INTERCEPTOR = ElementUInt8(241)
        COYOTE_INTERCEPTOR = ElementUInt8(242)
        CAL50 = ElementUInt8(243)
        MM30 = ElementUInt8(244)
        # 245 - 254 Future Interceptors TBD
        # 255 is Reserved

    class InterceptTime(Enum):
        NO_STATEMENT = ElementUInt32(4294967295)

    class FCRChannel(Enum):
        NO_STATEMENT = ElementUInt16(0)

    class LaunchTime(Enum):
        NO_STATEMENT = ElementUInt32(4294967295)

    class LaunchAzimuth(Enum):
        NO_STATEMENT = ElementUInt32(0)

    class LaunchElevation(Enum):
        NO_STATEMENT = ElementUInt32(0)

    class LocalTrackID(Enum):
        NO_STATEMENT = ElementUInt16(0)

    class InterceptorID(Enum):
        NO_STATEMENT = ElementUInt16(0)


    # class ECEF(Enum): NO_STATEMENT = ElementInt32(0)
    # class ECEF_V(Enum): NO_STATEMENT = ElementInt32(-2147483648)

    class TargetPriority(Enum): NO_STATEMENT = ElementUInt32(0)

    class EstPKill(Enum): NO_STATEMENT = ElementUInt32(0)

    class Elevation(Enum): NO_STATEMENT = ElementInt32(0)

    class Azimuth(Enum): NO_STATEMENT = ElementUInt32(0)

    class MissileKind(Enum):
        NO_STATEMENT = ElementUInt8(0)
        AIM9X = ElementUInt8(1)
        # >1 not used

    class TrackManeuver(Enum):
        NO_STATEMENT = ElementUInt8(0)
        NON_MANEUVERING = ElementUInt8(1)
        MANEUVERING = ElementUInt8(2)
        # >2 not used

    class MissileInFlight(Enum):
        NO_STATEMENT = ElementUInt8(0)
        OTHER_MISSILE_NOT_IN_FLIGHT = ElementUInt8(1)
        OTHER_MISSILE_IN_FLIGHT = ElementUInt8(2)
        # >2 not used

    class TrajectoryShape(Enum): NO_STATEMENT = ElementUInt8(0)
        # >0 not used

    class TrackECEF_X(Enum): NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Y(Enum): NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Z(Enum): NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Vx(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TrackECEF_Vy(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TrackECEF_Vz(Enum): NO_STATEMENT = ElementInt32(-2147483648)
