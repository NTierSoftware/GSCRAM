# t925InterceptorStatus.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/13/2018
#todo FIX .toJSON(true) ECEF_X = "NO_STATEMENT"
from enum import Enum
from typing import List

from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Element import Element
from CRAMmsg.ElementInt16 import ElementInt16
from CRAMmsg.ElementInt32 import ElementInt32
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt24 import ElementUInt24
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue
from Utilities.Wrap import wrap

class t925Consts:
    class PlanId(Enum): NO_STATEMENT = ElementUInt16(0)
    class SysTrackId(Enum): NO_STATEMENT = ElementUInt32(0)
    class LocalTrackId(Enum): NO_STATEMENT = ElementUInt16(0)

    class InterceptorStatus(Enum):
        NO_STATEMENT = ElementUInt8(0)
        MIDCOURSE = ElementUInt8(1)
        TERMINAL = ElementUInt8(2)
        FLYOUT = ElementUInt8(3)
        TURNAROUND = ElementUInt8(4)
        LANDING = ElementUInt8(5)
        DETONATE = ElementUInt8(6)
        MISSION_ABORTED = ElementUInt8(7)
        INTERRUPTED = ElementUInt8(8)
        # >8 not used

    class MissionStatus(Enum):
        NO_STATEMENT = ElementUInt8(0)
        MISSION_ACTIVE = ElementUInt8(1)
        WAYPOINT_ACTIVE = ElementUInt8(2)
        # >2 not used

    class ESAD_State(Enum):
        NO_STATEMENT = ElementUInt16(0)
        POST = ElementUInt16(1)
        FLYOUT = ElementUInt16(2)
        READY = ElementUInt16(3)
        ARM = ElementUInt16(4)
        SAFE = ElementUInt16(5)
        # >5 not used

    class ECEF_X(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Y(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Z(Enum): NO_STATEMENT = ElementInt32(0)

    class ECEF_Vx(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class ECEF_Vy(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class ECEF_Vz(Enum): NO_STATEMENT = ElementInt32(-2147483648)

    class SeekerRange(Enum): NO_STATEMENT = ElementUInt32(4294967295)
    class ValidTime(Enum): NO_STATEMENT = ElementUInt32(4294967295)
    class BatteryLife(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TimeToGo(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class RangeToGo(Enum): NO_STATEMENT = ElementUInt32(4294967295)
    class SeekerAzimuth(Enum): NO_STATEMENT = ElementInt16(-32768)
    class SeekerElevation(Enum): NO_STATEMENT = ElementInt16(-32768)
    class SeekerRangeRate(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class IndicatedAirSpeed(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class GPS_PDOP(Enum): NO_STATEMENT = ElementUInt8(0)


class t925InterceptorStatus(CRAMBaseMessage):
    MSG_LEN = 96
    MSG_ID = 925
    PART_COUNT = 0

    def __init__(self, weaponId, planId, sysTrackId, localTrackId, interceptorId,

                 interceptorStatus=t925Consts.InterceptorStatus.FLYOUT.value,
                 missionStatus=t925Consts.MissionStatus.WAYPOINT_ACTIVE.value,
                 ESADState=t925Consts.ESAD_State.READY.value,

                 ECEF_X=t925Consts.ECEF_X.NO_STATEMENT.value,
                 ECEF_Y=t925Consts.ECEF_Y.NO_STATEMENT.value,
                 ECEF_Z=t925Consts.ECEF_Z.NO_STATEMENT.value,
                 track_ECEF_Vx=1,
                 track_ECEF_Vy=1,
                 track_ECEF_Vz=1,
                 # track_ECEF_Vx=t925Consts.ECEF_Vx.NO_STATEMENT.value,
                 # track_ECEF_Vy=t925Consts.ECEF_Vy.NO_STATEMENT.value,
                 # track_ECEF_Vz=t925Consts.ECEF_Vz.NO_STATEMENT.value,

                 yaw=0, pitch=0, roll=0,
                 seekerRange=t925Consts.SeekerRange.NO_STATEMENT.value,
                 validTime=t925Consts.ValidTime.NO_STATEMENT.value,

                 batteryLife=600000,
                 timeToGo=t925Consts.TimeToGo.NO_STATEMENT.value,
                 rangeToGo=t925Consts.RangeToGo.NO_STATEMENT.value,
                 seekerAzimuth=t925Consts.SeekerAzimuth.NO_STATEMENT.value, seekerElevation=t925Consts.SeekerElevation.NO_STATEMENT.value,
                 seekerRangeRate=0, indicatedAirSpeed=0, GPS_PDOP=t925Consts.GPS_PDOP.NO_STATEMENT.value,
                 header: Header=None):
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.planId = wrap(planId, ElementUInt16)
        self.sysTrackId = wrap(sysTrackId, ElementUInt32)
        self.localTrackId = wrap(localTrackId, ElementUInt16)
        self.interceptorId = wrap(interceptorId, ElementUInt16)
        self.interceptorStatus = wrap(interceptorStatus, ElementUInt8)
        self.missionStatus = wrap(missionStatus, ElementUInt8)
        self.ESAD_State = wrap(ESADState, ElementUInt16)

        self.ECEF_X = wrap(ECEF_X, ElementInt32)
        self.ECEF_Y = wrap(ECEF_Y, ElementInt32)
        self.ECEF_Z = wrap(ECEF_Z, ElementInt32)
        self.trackECEF_Vx = wrap(track_ECEF_Vx, ElementInt32)
        self.trackECEF_Vy = wrap(track_ECEF_Vy, ElementInt32)
        self.trackECEF_Vz = wrap(track_ECEF_Vz, ElementInt32)

        self.yaw = wrap(yaw, ElementUInt16)
        self.pitch = wrap(pitch, ElementInt16)
        self.roll = wrap(roll, ElementInt16)
        self.spare1 = ElementUInt16(0)
        self.seekerRange = wrap(seekerRange, ElementUInt32)
        self.validTime = wrap(validTime, ElementUInt32)
        self.batteryLife = wrap(batteryLife, ElementInt32)
        self.timeToGo = wrap(timeToGo, ElementInt32)
        self.rangeToGo = wrap(rangeToGo, ElementUInt32)
        self.seekerAzimuth = wrap(seekerAzimuth, ElementInt16)
        self.seekerElevation = wrap(seekerElevation, ElementInt16)
        self.seekerRangeRate = wrap(seekerRangeRate, ElementInt32)
        self.indicatedAirSpeed = wrap(indicatedAirSpeed, ElementInt32)
        self.GPS_PDOP = wrap(GPS_PDOP, ElementUInt8)
        self.spare2 = ElementUInt24(0)


    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 925 Command's data fields in order."""
        return [self.header, self.weaponId, self.planId, self.sysTrackId,
                self.localTrackId, self.interceptorId,
                self.interceptorStatus, self.missionStatus, self.ESAD_State,
                self.ECEF_X, self.ECEF_Y, self.ECEF_Z,
                self.trackECEF_Vx, self.trackECEF_Vy, self.trackECEF_Vz, self.yaw, self.pitch, self.roll, self.spare1,
                self.seekerRange, self.validTime, self.batteryLife, self.timeToGo, self.rangeToGo, self.seekerAzimuth,
                self.seekerElevation, self.seekerRangeRate, self.indicatedAirSpeed, self.GPS_PDOP, self.spare2]

    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 925 Command's data fields' names in order."""
        return ['messageHeader', 'weaponId', 'planId', 'sysTrackId',
                'localTrackId', 'interceptorId',
                'interceptorStatus', 'missionStatus', 'ESAD_State',
                'ECEF_X', 'ECEF_Y', 'ECEF_Z',
                'trackECEF_Vx', 'trackECEF_Vy', 'trackECEF_Vz', 'yaw', 'pitch', 'roll', 'spare1',
                'seekerRange', 'validTime', 'batteryLife', 'timeToGo', 'rangeToGo', 'seekerAzimuth',
                'seekerElevation', 'seekerRangeRate', 'indicatedAirSpeed', 'GPS_PDOP', 'spare2']

    def getAllEnumGroups(self) -> List:
        return [None, None, t925Consts.PlanId, t925Consts.SysTrackId,
                t925Consts.LocalTrackId, None,
                t925Consts.InterceptorStatus, t925Consts.MissionStatus, t925Consts.ESAD_State,
                t925Consts.ECEF_X, t925Consts.ECEF_Y, t925Consts.ECEF_Z,
                t925Consts.ECEF_Vx, t925Consts.ECEF_Vy, t925Consts.ECEF_Vz,
                None, None, None, None, t925Consts.SeekerRange, t925Consts.ValidTime, t925Consts.BatteryLife,
                t925Consts.TimeToGo, t925Consts.RangeToGo, t925Consts.SeekerAzimuth, t925Consts.SeekerElevation, t925Consts.SeekerRangeRate,
                t925Consts.IndicatedAirSpeed, t925Consts.GPS_PDOP, None]

    def getNumBytes(self) -> int: return self.MSG_LEN

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        planId = ElementUInt16.genFromBytes(byteList[14:16])
        sysTrackId = ElementUInt32.genFromBytes(byteList[16:20])

        localTrackId = ElementUInt16.genFromBytes(byteList[20:22])
        interceptorId = ElementUInt16.genFromBytes(byteList[22:24])
        interceptorStatus = ElementUInt8.genFromBytes(byteList[24:25])
        missionStatus = ElementUInt8.genFromBytes(byteList[25:26])
        ESAD_State = ElementUInt16.genFromBytes(byteList[26:28])

        ECEF_X = ElementInt32.genFromBytes(byteList[28:32])
        ECEF_Y = ElementInt32.genFromBytes(byteList[32:36])
        ECEF_Z = ElementInt32.genFromBytes(byteList[36:40])

        trackECEF_Vx = ElementInt32.genFromBytes(byteList[40:44])
        trackECEF_Vy = ElementInt32.genFromBytes(byteList[44:48])
        trackECEF_Vz = ElementInt32.genFromBytes(byteList[48:52])
        yaw = ElementUInt16.genFromBytes(byteList[52:54])
        pitch = ElementInt16.genFromBytes(byteList[54:56])
        roll = ElementInt16.genFromBytes(byteList[56:58])
        # bytes 58 - 59 are for spare
        seekerRange = ElementUInt32.genFromBytes(byteList[60:64])
        validTime = ElementUInt32.genFromBytes(byteList[64:68])
        batteryLife = ElementInt32.genFromBytes(byteList[68:72])
        timeToGo = ElementInt32.genFromBytes(byteList[72:76])
        rangeToGo = ElementUInt32.genFromBytes(byteList[76:80])
        seekerAzimuth = ElementInt16.genFromBytes(byteList[80:82])
        seekerElevation = ElementInt16.genFromBytes(byteList[82:84])
        seekerRangeRate = ElementInt32.genFromBytes(byteList[84:88])
        indicatedAirSpeed = ElementInt32.genFromBytes(byteList[88:92])
        GPS_PDOP = ElementUInt8.genFromBytes(byteList[92:93])
        # bytes 93 - 95 are for spare

        return cls(weaponId, planId, sysTrackId,
                   localTrackId, interceptorId, interceptorStatus, missionStatus, ESAD_State,
                   ECEF_X, ECEF_Y, ECEF_Z,
                   trackECEF_Vx, trackECEF_Vy, trackECEF_Vz, yaw, pitch, roll,
                   seekerRange, validTime, batteryLife, timeToGo, rangeToGo, seekerAzimuth, seekerElevation, seekerRangeRate,
                   indicatedAirSpeed, GPS_PDOP, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        planId = objectToValue(objDict['planId'], t925Consts.PlanId)
        sysTrackId = objectToValue(objDict['sysTrackId'], t925Consts.SysTrackId)
        localTrackId = objectToValue(objDict['localTrackId'], t925Consts.LocalTrackId)
        interceptorStatus = objectToValue(objDict['interceptorStatus'], t925Consts.InterceptorStatus)
        missionStatus = objectToValue(objDict['missionStatus'], t925Consts.MissionStatus)
        ESAD_State = objectToValue(objDict['ESAD_State'], t925Consts.ESAD_State)

        ECEF_X = objectToValue(objDict['ECEF_X'], t925Consts.ECEF_X)
        ECEF_Y = objectToValue(objDict['ECEF_Y'], t925Consts.ECEF_Y)
        ECEF_Z = objectToValue(objDict['ECEF_Z'], t925Consts.ECEF_Z)
        trackECEF_Vx = objectToValue(objDict['trackECEF_Vx'], t925Consts.ECEF_Vx)
        trackECEF_Vy = objectToValue(objDict['trackECEF_Vy'], t925Consts.ECEF_Vy)
        trackECEF_Vz = objectToValue(objDict['trackECEF_Vz'], t925Consts.ECEF_Vz)

        seekerRange = objectToValue(objDict['seekerRange'], t925Consts.SeekerRange)
        validTime = objectToValue(objDict['validTime'], t925Consts.ValidTime)
        batteryLife = objectToValue(objDict['batteryLife'], t925Consts.BatteryLife)
        timeToGo = objectToValue(objDict['timeToGo'], t925Consts.TimeToGo)
        rangeToGo = objectToValue(objDict['rangeToGo'], t925Consts.RangeToGo)
        seekerAzimuth = objectToValue(objDict['seekerAzimuth'], t925Consts.SeekerAzimuth)
        seekerElevation = objectToValue(objDict['seekerElevation'], t925Consts.SeekerElevation)
        seekerRangeRate = objectToValue(objDict['seekerRangeRate'], t925Consts.SeekerRangeRate)
        indicatedAirSpeed = objectToValue(objDict['indicatedAirSpeed'], t925Consts.IndicatedAirSpeed)
        GPS_PDOP = objectToValue(objDict['GPS_PDOP'], t925Consts.GPS_PDOP)

        return cls(objDict['weaponId'], planId, sysTrackId,
                   localTrackId, objDict['interceptorId'], interceptorStatus, missionStatus, ESAD_State,
                   ECEF_X, ECEF_Y, ECEF_Z,
                   trackECEF_Vx, trackECEF_Vy, trackECEF_Vz,
                   objDict['yaw'], objDict['pitch'], objDict['roll'], seekerRange, validTime, batteryLife, timeToGo,
                   rangeToGo, seekerAzimuth, seekerElevation, seekerRangeRate, indicatedAirSpeed,
                   GPS_PDOP, header)



