from datetime import datetime, timedelta
from enum import Enum
from typing import List

from CoordTransform.CRAMtofromLLA import CRAMpoint, ECEFtofromLLA, LLApoint
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Element import Element
from CRAMmsg.ElementInt24 import ElementInt24
from CRAMmsg.ElementInt32 import ElementInt32
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.Header import Header, HeaderConsts
from CRAMmsg.Matrix import PMatrix
from GSmsg.tTargetStatus import tTargetStatus
from Utilities import constants
from Utilities.console import console, debugLog
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue
from Utilities.Wrap import wrap
# from Server.baseGSCRAMsocket import GSCRAMtofromGS

class r920Consts:
    class TrackId(Enum):
        PENDING = ElementUInt8(0)
        UNKNOWN = ElementUInt8(1)
        ASSUMED_FRIEND = ElementUInt8(2)
        FRIEND = ElementUInt8(3)
        NEUTRAL = ElementUInt8(4)
        SUSPECT = ElementUInt8(5)
        HOSTILE = ElementUInt8(6)
        # 7 - 255 Not Used

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
        BIOLOGICAL = ElementUInt8(211)
        GROUND_VEHICLE = ElementUInt8(212)
        GROUND_TERRAIN = ElementUInt8(213)
        # 214 - 240 for Other Threats TBD
        AI3_INTERCEPTOR = ElementUInt8(241)
        COYOTE_INTERCEPTOR = ElementUInt8(242)
        M33 = ElementUInt8(243)
        M788 = ElementUInt8(244)
        CYCLOPS_INTERCEPTOR = ElementUInt8(245)
        INTERCEPTOR_2BFB = ElementUInt8(246)
        CUJO_INTERCEPTOR = ElementUInt8(247)
        # 248 - 254 Future Interceptors TBD
        # 255 is Reserved

    class SimFlag(Enum):
        LIVE = ElementUInt8(0)
        SIMULATED = ElementUInt8(1)

    class DropTrackFlag(Enum):
        NOT_DROPPED = ElementUInt8(0)
        DROPPED = ElementUInt8(1)
        DISREGARD_TRACK = ElementUInt8(2)
        WAYPOINT_ACTIVE = ElementUInt8(3)
        # >3 not used

    class BallisticCoeff(Enum): UNKNOWN = ElementUInt32(0)

    class TrackECEF_X(Enum):  NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Y(Enum):  NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Z(Enum):  NO_STATEMENT = ElementInt32(0)
    class TrackECEF_Vx(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TrackECEF_Vy(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class TrackECEF_Vz(Enum): NO_STATEMENT = ElementInt32(-2147483648)


    class ValidTime(Enum): NO_STATEMENT = ElementUInt32(4294967295)

    class TrackCoordination(Enum):
        THREAT_STATE = ElementUInt8(0)
        SENSOR_REG_TRACK = ElementUInt8(1)
        CAMERA_CUE = ElementUInt8(2)
        # >3 not used

    class FCR_ID(Enum): NO_STATEMENT = ElementUInt8(0)

    class LocalTrackID(Enum): NO_STATEMENT = ElementUInt16(0)

    class AircraftInArea(Enum):
        CLEAR = ElementUInt8(0)
        AIRCRAFT_IN_AREA = ElementUInt8(189)  # 0b10111101
        AIRCRAFT_NOT_EVAL = ElementUInt8(195)  # 0b11000011

    class HeightAboveGround(Enum): NO_STATEMENT = ElementInt24(-8388608)

# "The C2S will send the 920 message at the same rate that C2S receives updates from local sources, not to exceed 20Hz."
class r920ThreatState(CRAMBaseMessage):
    BASE_LENGTH = 72
    MSG_ID = 920
    Numr920ThreatStates:int = 0
    nonDispatch920ThreatState = 0
    # LatencyLog:console = console(console.DRONE, title="GSCRAM Threat Relay Latency")
    Log = console.getConsole(console.TELEMETRY)

    # prevLLA = LLApoint(constants.GroundZero['Lat'], Lon = constants.GroundZero['Lon'], Elev = 9999)

    def __init__(self, weaponId, posTQ, velTQ, sysTrackId, trackId, trackClass, simFlag, dropTrackFlag, ballisticCoeff,
                 trackECEF_X, trackECEF_Y, trackECEF_Z, trackECEF_Vx, trackECEF_Vy, trackECEF_Vz, validTime,
                 trackCoordination, fcrId, localTrackId, aircraftInArea, heightAboveGround, pFields: PMatrix=None,
                 header: Header=None):
        length = self.BASE_LENGTH
        partCount = 0
        if pFields is not None:
            length += pFields.getByteLength()
            partCount = 1
        super().__init__(header or Header(length, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, partCount, millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.posTQ = wrap(posTQ, ElementUInt8)
        self.velTQ = wrap(velTQ, ElementUInt8)
        self.sysTrackId = wrap(sysTrackId, ElementUInt32)
        self.trackId = wrap(trackId, ElementUInt8)
        self.trackClass = wrap(trackClass, ElementUInt8)
        self.simFlag = wrap(simFlag, ElementUInt8)
        self.dropTrackFlag = wrap(dropTrackFlag, ElementUInt8)
        self.ballisticCoeff = wrap(ballisticCoeff, ElementUInt32)
        self.trackECEF_X = wrap(trackECEF_X, ElementInt32)
        self.trackECEF_Y = wrap(trackECEF_Y, ElementInt32)
        self.trackECEF_Z = wrap(trackECEF_Z, ElementInt32)
        self.trackECEF_Vx = wrap(trackECEF_Vx, ElementInt32)
        self.trackECEF_Vy = wrap(trackECEF_Vy, ElementInt32)
        self.trackECEF_Vz = wrap(trackECEF_Vz, ElementInt32)
        self.validTime = wrap(validTime, ElementUInt32)
        self.trackCoordination = wrap(trackCoordination, ElementUInt8)
        self.fcrId = wrap(fcrId, ElementUInt8)
        self.localTrackId = wrap(localTrackId, ElementUInt16)
        self.aircraftInArea = wrap(aircraftInArea, ElementUInt8)
        self.heightAboveGround = wrap(heightAboveGround, ElementInt24)
        self.spare1 = ElementUInt32(0)
        self.spare2 = ElementUInt32(0)

        self.pFields = pFields

    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 920 Command's data fields in order."""
        arr = [self.header, self.weaponId, self.posTQ, self.velTQ, self.sysTrackId, self.trackId, self.trackClass,
               self.simFlag, self.dropTrackFlag, self.ballisticCoeff, self.trackECEF_X, self.trackECEF_Y,
               self.trackECEF_Z, self.trackECEF_Vx, self.trackECEF_Vy, self.trackECEF_Vz, self.validTime,
               self.trackCoordination, self.fcrId, self.localTrackId, self.aircraftInArea, self.heightAboveGround,
               self.spare1, self.spare2]
        if self.header.partCount.data == 1:
            arr.extend(self.pFields.allFields())
        return arr

    def getAllFieldNames(self) -> List[str]: #Returns a list of all of the 920 Command's data fields' names in order.
        arr = ['messageHeader', 'weaponId', 'posTQ', 'velTQ', 'sysTrackId', 'trackId', 'trackClass', 'simFlag',
               'dropTrackFlag', 'ballisticCoeff', 'trackECEF_X', 'trackECEF_Y', 'trackECEF_Z', 'trackECEF_Vx',
               'trackECEF_Vy', 'trackECEF_Vz', 'validTime', 'trackCoordination', 'fcrId', 'localTrackId',
               'aircraftInArea', 'heightAboveGround', 'spare1', 'spare2']

        if self.header.partCount.data == 1:  arr.extend(self.pFields.allFieldNames())
        return arr

    def getAllEnumGroups(self):
        arr = [None, None, None, None, None, r920Consts.TrackId, r920Consts.TrackClass, r920Consts.SimFlag,
               r920Consts.DropTrackFlag, r920Consts.BallisticCoeff,
               r920Consts.TrackECEF_X, r920Consts.TrackECEF_Y, r920Consts.TrackECEF_Z,
               r920Consts.TrackECEF_Vx, r920Consts.TrackECEF_Vy, r920Consts.TrackECEF_Vz,
               r920Consts.ValidTime, r920Consts.TrackCoordination, r920Consts.FCR_ID, r920Consts.LocalTrackID,
               r920Consts.AircraftInArea, r920Consts.HeightAboveGround, None, None]
        if self.header.partCount.data == 1:
            arr.extend([None] * len(self.pFields.allFieldNames()))
        return arr

    def getNumBytes(self) -> int: return self.header.messageLength.data

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        posTQ = ElementUInt8.genFromBytes(byteList[14:15])
        velTQ = ElementUInt8.genFromBytes(byteList[15:16])
        sysTrackId = ElementUInt32.genFromBytes(byteList[16:20])
        trackId = ElementUInt8.genFromBytes(byteList[20:21])
        trackClass = ElementUInt8.genFromBytes(byteList[21:22])
        simFlag = ElementUInt8.genFromBytes(byteList[22:23])
        dropTrackFlag = ElementUInt8.genFromBytes(byteList[23:24])
        ballisticCoeff = ElementUInt32.genFromBytes(byteList[24:28])
        trackECEF_X = ElementInt32.genFromBytes(byteList[28:32])
        trackECEF_Y = ElementInt32.genFromBytes(byteList[32:36])
        trackECEF_Z = ElementInt32.genFromBytes(byteList[36:40])
        trackECEF_Vx = ElementInt32.genFromBytes(byteList[40:44])
        trackECEF_Vy = ElementInt32.genFromBytes(byteList[44:48])
        trackECEF_Vz = ElementInt32.genFromBytes(byteList[48:52])
        validTime = ElementUInt32.genFromBytes(byteList[52:56])
        trackCoordination = ElementUInt8.genFromBytes(byteList[56:57])
        fcrId = ElementUInt8.genFromBytes(byteList[57:58])
        localTrackId = ElementUInt16.genFromBytes(byteList[58:60])
        aircraftInArea = ElementUInt8.genFromBytes(byteList[60:61])
        heightAboveGround = ElementInt24.genFromBytes(byteList[61:64])
        # bytes 64 - 71 are for spare
        pFields = PMatrix.genFromBytes(byteList[72:156]) if header.partCount.data == 1 else None
        return cls(weaponId, posTQ, velTQ, sysTrackId, trackId, trackClass, simFlag, dropTrackFlag, ballisticCoeff,
                   trackECEF_X, trackECEF_Y, trackECEF_Z, trackECEF_Vx, trackECEF_Vy, trackECEF_Vz, validTime,
                   trackCoordination, fcrId, localTrackId, aircraftInArea, heightAboveGround, pFields, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])
        pFields = PMatrix.constructFromDictionary(objDict) if header.partCount.data == 1 else None

        trackId = objectToValue(objDict['trackId'], r920Consts.TrackId)
        trackClass = objectToValue(objDict['trackClass'], r920Consts.TrackClass)
        simFlag = objectToValue(objDict['simFlag'], r920Consts.SimFlag)
        dropTrackFlag = objectToValue(objDict['dropTrackFlag'], r920Consts.DropTrackFlag)
        ballisticCoeff = objectToValue(objDict['ballisticCoeff'], r920Consts.BallisticCoeff)
        trackECEF_X = objectToValue(objDict['trackECEF_X'], r920Consts.TrackECEF_X)
        trackECEF_Y = objectToValue(objDict['trackECEF_Y'], r920Consts.TrackECEF_Y)
        trackECEF_Z = objectToValue(objDict['trackECEF_Z'], r920Consts.TrackECEF_Z)
        trackECEF_Vx = objectToValue(objDict['trackECEF_Vx'], r920Consts.TrackECEF_Vx)
        trackECEF_Vy = objectToValue(objDict['trackECEF_Vy'], r920Consts.TrackECEF_Vy)
        trackECEF_Vz = objectToValue(objDict['trackECEF_Vz'], r920Consts.TrackECEF_Vz)
        validTime = objectToValue(objDict['validTime'], r920Consts.ValidTime)
        trackCoordination = objectToValue(objDict['trackCoordination'], r920Consts.TrackCoordination)
        fcrId = objectToValue(objDict['fcrId'], r920Consts.FCR_ID)
        localTrackId = objectToValue(objDict['localTrackId'], r920Consts.LocalTrackID)
        aircraftInArea = objectToValue(objDict['aircraftInArea'], r920Consts.AircraftInArea)
        heightAboveGround = objectToValue(objDict['heightAboveGround'], r920Consts.HeightAboveGround)

        return cls(objDict['weaponId'], objDict['posTQ'], objDict['velTQ'], objDict['sysTrackId'], trackId,
                   trackClass, simFlag, dropTrackFlag, ballisticCoeff, trackECEF_X, trackECEF_Y, trackECEF_Z,
                   trackECEF_Vx, trackECEF_Vy, trackECEF_Vz, validTime, trackCoordination, fcrId, localTrackId,
                   aircraftInArea, heightAboveGround, pFields, header)


    def toLLA(self) -> LLApoint:
        return ECEFtofromLLA.CRAMtoLLA(CRAMpoint(self.trackECEF_X.data, self.trackECEF_Y.data, self.trackECEF_Z.data))

    ThreatTypes = (r920Consts.TrackId.UNKNOWN.value, r920Consts.TrackId.HOSTILE.value, r920Consts.TrackId.SUSPECT.value)
    InterdictedTargets = []

    def isaThreat(self) -> bool:
        # sometimes the 920 reports on a friendly drone which is NOT a target!
        # and sometimes a drone has already been interdicted so it is not now a threat.
        # isaThreat:bool = (self.trackId in r920ThreatState.ThreatTypes) and not (self.sysTrackId.data in r920ThreatState.InterdictedTargets)
        return (self.trackId in r920ThreatState.ThreatTypes) and not (self.sysTrackId.data in r920ThreatState.InterdictedTargets)



    """
        r920ThreatState.forwardToGroundspace:
        If the target is a threat:
        Convert the target from CRAM hundredths of meters to LLA and forward to GS.

        If the target is a threat AND we're in Simulation:
        Convert the target from CRAM hundredths of meters, interpolate, convert to LLA and forward to GS.
        Send no faster than 5Hz = .2 seconds
    """
    Last920SentTime:datetime = constants.AprilFoolsDay2k #initialize to April Fool's Day
    TooMany920:int = 0

    # def forwardToGroundspace(self, Groundspace: '') -> constants.currentState:
    #     if self.CEASEFIRE():
    #     # if self.dropTrackFlag.data != r920Consts.DropTrackFlag.NOT_DROPPED.value: # Stop Interdiction and GOHOME
    #         print("\nself.dropTrackFlag is NOT r920Consts.DropTrackFlag.NOT_DROPPED: " + str(self.dropTrackFlag.data ))
    #         return constants.currentState.GOHOME
    #
    #     if (datetime.utcnow() - r920ThreatState.Last920SentTime) >= constants.Groundspacetimedelta:
    #         LLA = self.toLLA()
    #         myTargetStatus = tTargetStatus(self.weaponId.data, self.sysTrackId.data,
    #                                        LLA.Lat, LLA.Lon, LLA.Elev,
    #                                        self.trackECEF_Vx.data, self.trackECEF_Vy.data, self.trackECEF_Vz.data)
    #
    #         Groundspace.sendGSmsg(myTargetStatus)
    #         r920ThreatState.Last920SentTime = datetime.utcnow()
    #         r920ThreatState.Numr920ThreatStates += 1
    #         newLine = "\n" if (r920ThreatState.Numr920ThreatStates % 25 == 0) else ""
    #
    #         # debugLog:console = console.getConsole(console.DEBUG)
    #         debugLog.log(newLine + " Threat" + str(r920ThreatState.Numr920ThreatStates))
    #
    #         # telemetryLog:console = console.getConsole(console.TELEMETRY)
    #         r920ThreatState.Log.log( str(self) )
    #         r920ThreatState.Log.log(str(myTargetStatus))
    #         # r920ThreatState.prevLLA = LLA
    #         # telemetryLog.log("target sent to GS:\t" + myTargetStatus.SentTime.isoformat() + "\t" + myTargetStatus.toJSON()  )
    #
    #         # r920ThreatState.LatencyLog.log(str(r920ThreatState.Numr920ThreatStates) + ": " + "Recv: " + str(self.RecvTime) + ", Sent: " + str(myTargetStatus.SentTime) + ", Latency(ms): " + str(r920ThreatState.millis_interval(self.RecvTime, myTargetStatus.SentTime)))
    #     else:
    #         r920ThreatState.TooMany920 += 1
    #         if (r920ThreatState.TooMany920 % 10 == 0) : print(' Threat overflow' + str(r920ThreatState.TooMany920) + ' ', end='', flush=True)
    #     return constants.currentState.NOCHANGE

    # def forwardToGroundspace(self, Groundspace: '') -> constants.currentState:
    #     if self.CEASEFIRE():
    #         print(">>>>\t\tCEASEFIRE\t\t<<<<")
    #         debugLog.log(">>>>\t\tCEASEFIRE\t\t<<<<")
    #         return constants.currentState.GOHOME
    #
    #     if (datetime.utcnow() - r920ThreatState.Last920SentTime) >= constants.Groundspacetimedelta:
    #         LLA = self.toLLA()
    #         myTargetStatus = tTargetStatus(self.weaponId.data, self.sysTrackId.data,
    #                                        LLA.Lat, LLA.Lon, LLA.Elev,
    #                                        self.trackECEF_Vx.data, self.trackECEF_Vy.data, self.trackECEF_Vz.data)
    #
    #         Groundspace.sendGSmsg(myTargetStatus)
    #         # r920ThreatState.Last920SentTime = datetime.utcnow()
    #         r920ThreatState.Last920SentTime = myTargetStatus.SentTime
    #         # print('Last920SentTime', r920ThreatState.Last920SentTime)
    #         r920ThreatState.Numr920ThreatStates += 1
    #         newLine = "\n" if (r920ThreatState.Numr920ThreatStates % 25 == 0) else ""
    #
    #         debugLog.log(newLine + " Threat" + str(r920ThreatState.Numr920ThreatStates))
    #
    #         r920ThreatState.Log.log( str(self) )
    #         r920ThreatState.Log.log(str(myTargetStatus))
    #     else:
    #         r920ThreatState.TooMany920 += 1
    #         if (r920ThreatState.TooMany920 % 10 == 0) : print(' Threat overflow' + str(r920ThreatState.TooMany920) + ' ', end='', flush=True)
    #     return constants.currentState.NOCHANGE


    def forwardToGroundspace(self, Groundspace: '') -> constants.currentState:
        if self.CEASEFIRE():
            print(">>>>\t\tCEASEFIRE\t\t<<<<")
            debugLog.log(">>>>\t\tCEASEFIRE\t\t<<<<")
            return constants.currentState.GOHOME

        LLA = self.toLLA()
        myTargetStatus = tTargetStatus(self.weaponId.data, self.sysTrackId.data,
                                       LLA.Lat, LLA.Lon, LLA.Elev,
                                       self.trackECEF_Vx.data, self.trackECEF_Vy.data, self.trackECEF_Vz.data)

        if (datetime.utcnow() - r920ThreatState.Last920SentTime) >= constants.Groundspacetimedelta: #do not send to GS faster than 5Hz
            Groundspace.sendGSmsg(myTargetStatus)
        # r920ThreatState.Last920SentTime = datetime.utcnow()
            r920ThreatState.Last920SentTime = myTargetStatus.SentTime
            # print('Last920SentTime', r920ThreatState.Last920SentTime)
            r920ThreatState.Numr920ThreatStates += 1
            newLine = "\n" if (r920ThreatState.Numr920ThreatStates % 25 == 0) else ""

            debugLog.log(newLine + " Threat" + str(r920ThreatState.Numr920ThreatStates))

            r920ThreatState.Log.log( str(self) )
            r920ThreatState.Log.log(str(myTargetStatus))
        else:
            r920ThreatState.TooMany920 += 1
            if (r920ThreatState.TooMany920 % 10 == 0) : print(' Threat overflow' + str(r920ThreatState.TooMany920) + ' ', end='', flush=True)
        return constants.currentState.NOCHANGE




#https://stackoverflow.com/questions/18426882/python-time-difference-in-milliseconds-not-working-for-me
    def millis_interval(start:datetime, end:datetime):
        diff = end - start
        millis = diff.days * 24 * 60 * 60 * 1000
        millis += diff.seconds * 1000
        millis += diff.microseconds / 1000
        return millis


    def INTERDICTION(self):
        r920ThreatState.InterdictedTargets.append( self.sysTrackId.data )
        r920ThreatState.Numr920ThreatStates = r920ThreatState.nonDispatch920ThreatState = r920ThreatState.TooMany920 = 0

        # r920ThreatState.Numr920ThreatStates = r920ThreatState.nonDispatch920ThreatState = r920ThreatState.SameLocation = r920ThreatState.TooMany920 = 0
        # r920ThreatState.prevLLA = LLApoint(constants.GroundZero['Lat'], Lon=constants.GroundZero['Lon'], Elev=9999)
        # print("r920ThreatState.INTERDICTION().InterdictedTargets", r920ThreatState.InterdictedTargets )

    def CEASEFIRE(self) ->bool: return self.dropTrackFlag.data != r920Consts.DropTrackFlag.NOT_DROPPED.value


# https: // stackoverflow.com / questions / 4932438 / how - to - create - a - custom - string - representation -for -a -class -object
    def __repr__(self):
        selfPt = self.toLLA()
        return "target recd from CRAM:\t" + self.RecvTime.isoformat() + "\thae:" + str(selfPt.Elev) + "\tLat:" + str(selfPt.Lat) + "\tLon:" + str(selfPt.Lon) \
               + "\tid:" + str(self.sysTrackId.data) + '\tceasefire:' + str(self.CEASEFIRE())

