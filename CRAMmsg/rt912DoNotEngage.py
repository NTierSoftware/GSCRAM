# author: Alex Erf, Airspace, alex.erf@airspace.co, 8/14/2018
from enum import Enum
from typing import List
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Element import Element
from CRAMmsg.ElementInt32 import ElementInt32
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.Header import Header, HeaderConsts
from CoordTransform.CRAMtofromLLA import LLApoint, ECEFtofromLLA, CRAMpoint
from GSmsg.tDoNotEngage import tDoNotEngage
from GSmsg.tGoToWaypoint import tGoToWaypoint
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue
from Utilities.Wrap import wrap

class rt912DoNotEngage(CRAMBaseMessage):
    MSG_LEN = 44
    MSG_ID = 912
    PART_COUNT = 0

    def __init__(self, weaponId, planId, sysTrackId, localTrackId, DNE_reason, DNE_action, interceptorId,
                 commandResponse, ECEF_X, ECEF_Y, ECEF_Z, header: Header=None):
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.planId = wrap(planId, ElementUInt16)
        self.sysTrackId = wrap(sysTrackId, ElementUInt32)
        self.localTrackId = wrap(localTrackId, ElementUInt16)
        self.DNE_reason = wrap(DNE_reason, ElementUInt8)
        self.DNE_action = wrap(DNE_action, ElementUInt8)
        self.interceptorId = wrap(interceptorId, ElementUInt16)
        self.commandResponse = wrap(commandResponse, ElementUInt8)
        self.spare1 = ElementUInt8(0)
        self.ECEF_X = wrap(ECEF_X, ElementInt32)
        self.ECEF_Y = wrap(ECEF_Y, ElementInt32)
        self.ECEF_Z = wrap(ECEF_Z, ElementInt32)
        self.spare2 = ElementUInt32(0)

    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 912 Command's data fields in order."""
        return [self.header, self.weaponId, self.planId, self.sysTrackId, self.localTrackId, self.DNE_reason,
                self.DNE_action, self.interceptorId, self.commandResponse, self.spare1, self.ECEF_X, self.ECEF_Y,
                self.ECEF_Z, self.spare2]

    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 912 Command's data fields' names in order."""
        return ['messageHeader', 'weaponId', 'planId', 'sysTrackId', 'localTrackId', 'DNE_reason', 'DNE_action',
                'interceptorId', 'commandResponse', 'spare1', 'ECEF_X', 'ECEF_Y', 'ECEF_Z', 'spare2']

    def getAllEnumGroups(self) -> List:
        return [None, None, rt912Consts.PlanID, rt912Consts.SysTrackID, rt912Consts.LocalTrackID,
                rt912Consts.DNE_Reason, rt912Consts.DNE_Action, rt912Consts.InterceptorID, rt912Consts.CommandResponse,
                None, rt912Consts.ECEF_X, rt912Consts.ECEF_Y, rt912Consts.ECEF_Z, None]

    def getNumBytes(self) -> int: return self.MSG_LEN

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        planId = ElementUInt16.genFromBytes(byteList[14:16])
        sysTrackId = ElementUInt32.genFromBytes(byteList[16:20])
        localTrackId = ElementUInt16.genFromBytes(byteList[20:22])
        DNE_reason = ElementUInt8.genFromBytes(byteList[22:23])
        DNE_action = ElementUInt8.genFromBytes(byteList[23:24])
        interceptorId = ElementUInt16.genFromBytes(byteList[24:26])
        commandResponse = ElementUInt8.genFromBytes(byteList[26:27])
        # byte 27 is for spare
        ECEF_X = ElementInt32.genFromBytes(byteList[28:32])
        ECEF_Y = ElementInt32.genFromBytes(byteList[32:36])
        ECEF_Z = ElementInt32.genFromBytes(byteList[36:40])
        # bytes 40 - 43 are for spare
        return cls(weaponId, planId, sysTrackId, localTrackId, DNE_reason, DNE_action, interceptorId, commandResponse,
                   ECEF_X, ECEF_Y, ECEF_Z, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        planId = objectToValue(objDict['planId'], rt912Consts.PlanID)
        sysTrackId = objectToValue(objDict['sysTrackId'], rt912Consts.SysTrackID)
        localTrackId = objectToValue(objDict['localTrackId'], rt912Consts.LocalTrackID)
        DNE_reason = objectToValue(objDict['DNE_reason'], rt912Consts.DNE_Reason)
        DNE_action = objectToValue(objDict['DNE_action'], rt912Consts.DNE_Action)
        interceptorId = objectToValue(objDict['interceptorId'], rt912Consts.InterceptorID)
        commandResponse = objectToValue(objDict['commandResponse'], rt912Consts.CommandResponse)
        ECEF_X = objectToValue(objDict['ECEF_X'], rt912Consts.ECEF_X)
        ECEF_Y = objectToValue(objDict['ECEF_Y'], rt912Consts.ECEF_Y)
        ECEF_Z = objectToValue(objDict['ECEF_Z'], rt912Consts.ECEF_Z)

        return cls(objDict['weaponId'], planId, sysTrackId, localTrackId, DNE_reason, DNE_action, interceptorId,
                   commandResponse, ECEF_X, ECEF_Y, ECEF_Z, header)

    def WILLCOMPLY(self) -> ('rt912DoNotEngage', tDoNotEngage, tGoToWaypoint) :
        self.commandResponse = rt912Consts.CommandResponse.WILL_COMPLY.value
        DoNotEngage:tDoNotEngage = tDoNotEngage(self.weaponId.data, self.sysTrackId.data )
        Loiter: tGoToWaypoint = None

        if self.ECEF_X.data != 0:
            CRAM:CRAMpoint = CRAMpoint(self.ECEF_X.data, self.ECEF_Y.data, self.ECEF_Z.data )
            LLA: LLApoint = ECEFtofromLLA.CRAMtoLLA(CRAM)
            Loiter:tGoToWaypoint = tGoToWaypoint(self.weaponId.data, LLA.Lat, LLA.Lon, LLA.Elev)

        return self, DoNotEngage, Loiter

class rt912Consts:
    class PlanID(Enum): NO_STATEMENT = ElementUInt16(0)
    class SysTrackID(Enum): NO_STATEMENT = ElementUInt32(0)
    class LocalTrackID(Enum): NO_STATEMENT = ElementUInt16(0)

    class DNE_Reason(Enum):
        OTHER = ElementUInt8(0)
        PLAN_EXPIRED = ElementUInt8(1)
        THREAT_DELETED = ElementUInt8(2)
        DROP_TRACK = ElementUInt8(3)
        OPERATOR = ElementUInt8(4)
        INTERCEPTOR_DIVERGED = ElementUInt8(5)
        THREAT_DIVERGED = ElementUInt8(6)
        AIRCRAFT_IN_AREA = ElementUInt8(7)
        WES_NON_OP = ElementUInt8(8)
        FCR_NON_OP = ElementUInt8(9)
        INVALID_910_INTERCEPT = ElementUInt8(10)
        # 11 - 255 reserved for future use

    class DNE_Action(Enum):
        NO_STATEMENT = ElementUInt8(0)
        LOITER = ElementUInt8(1)
        LOITER_CW = ElementUInt8(2)
        LOITER_CCW = ElementUInt8(3)
        SELF_DESTRUCT = ElementUInt8(4)
        SAFE = ElementUInt8(5)
        LAND = ElementUInt8(6)
        WAYPOINT = ElementUInt8(7)
        ABORT_LAUNCH = ElementUInt8(8)
        # >8 not used

    class InterceptorID(Enum): NO_STATEMENT = ElementUInt16(0)

    class CommandResponse(Enum):
        NO_STATEMENT = ElementUInt8(0)
        CANNOT_COMPLY = ElementUInt8(1)
        WILL_COMPLY = ElementUInt8(2)

    class ECEF_X(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Y(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Z(Enum): NO_STATEMENT = ElementInt32(0)

