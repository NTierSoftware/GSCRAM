# rt900WeaponCmd.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/31/2018

from CRAMmsg.Element import Element
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementUInt128 import ElementUInt128

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.Wrap import wrap
from Utilities.ValueNameConversion import objectToValue

from typing import List

from enum import Enum


class rt900WeaponCmd(CRAMBaseMessage):
    """This class defines a 900 Weapon Command Message (see doc 3.3.1)"""
    MSG_LEN = 60
    MSG_ID = 900
    PART_COUNT = 0
    
    def __init__(self, weaponId, commandCode, fireControlMode, planId, controlCode, sysTrackId, commandResponse, firingUnitId, header: Header=None):
        # Currently has interface kind default to 1: MML
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.commandCode = wrap(commandCode, ElementUInt8)
        self.fireControlMode = wrap(fireControlMode, ElementUInt8)
        self.planId = wrap(planId, ElementUInt16)
        self.controlCode = wrap(controlCode, ElementUInt16)
        self.sysTrackId = wrap(sysTrackId, ElementUInt32)
        self.commandResponse = wrap(commandResponse, ElementUInt8)
        self.spare1 = ElementUInt8(0)
        self.firingUnitId = wrap(firingUnitId, ElementUInt16)
        self.spare2 = ElementUInt128(0)
        self.spare3 = ElementUInt32(0)
        self.spare4 = ElementUInt32(0)
        self.spare5 = ElementUInt32(0)
        self.spare6 = ElementUInt32(0)
    
    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 900 Command's data fields in order."""
        return [self.header, self.weaponId, self.commandCode, self.fireControlMode, self.planId, self.controlCode,
                self.sysTrackId, self.commandResponse, self.spare1, self.firingUnitId, self.spare2, self.spare3,
                self.spare4, self.spare5, self.spare6]
    
    def getAllFieldNames(self) -> List[str]:
        return ['messageHeader', 'weaponId', 'commandCode', 'fireControlMode', 'planId', 'controlCode', 'systemTrackId',
                'commandResponse', 'spare1', 'firingUnitId', 'spare2', 'spare3', 'spare4', 'spare5', 'spare6']

    def getAllEnumGroups(self):
        return [None, None, rt900Consts.CommandCode, rt900Consts.FireControlMode, rt900Consts.PlanID,
                rt900Consts.ControlCode, rt900Consts.SysTrackID, rt900Consts.CommandResponse, None,
                rt900Consts.FiringUnitID, None, None, None, None, None]
    
    def getNumBytes(self) -> int:
        """Returns 60 because 900 Commands are always 60 bytes in length."""
        return self.MSG_LEN
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        """Returns an rt900WeaponCmd instance constructed from bytes."""
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        commandCode = ElementUInt8.genFromBytes(byteList[14:15])
        fireControlMode = ElementUInt8.genFromBytes(byteList[15:16])
        planId = ElementUInt16.genFromBytes(byteList[16:18])
        controlCode = ElementUInt16.genFromBytes(byteList[18:20])
        sysTrackId = ElementUInt32.genFromBytes(byteList[20:24])
        commandResponse = ElementUInt8.genFromBytes(byteList[24:25])
        # byte 25 is for spare
        firingUnitID = ElementUInt16.genFromBytes(byteList[26:28])
        # bytes 28 - 59 are all for spare
        return cls(weaponId, commandCode, fireControlMode, planId, controlCode, sysTrackId, commandResponse, firingUnitID, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])
        commandCode = objectToValue(objDict['commandCode'], rt900Consts.CommandCode)
        fireControlMode = objectToValue(objDict['fireControlMode'], rt900Consts.FireControlMode)
        planId = objectToValue(objDict['planId'], rt900Consts.PlanID)
        controlCode = objectToValue(objDict['controlCode'], rt900Consts.ControlCode)
        systemTrackId = objectToValue(objDict['systemTrackId'], rt900Consts.SysTrackID)
        commandResponse = objectToValue(objDict['commandResponse'], rt900Consts.CommandResponse)
        firingUnitId = objectToValue(objDict['firingUnitId'], rt900Consts.FiringUnitID)
        return cls(objDict['weaponId'], commandCode, fireControlMode, planId, controlCode, systemTrackId,
                   commandResponse, firingUnitId, header)


    def WILLCOMPLY(self) -> 'rt900WeaponCmd' :
        # 4.Upon receiving a 900 message, the WES shall send a 900 Command Message to the C2S
        # using the received message fields, but populating the Command Response field with a
        # 1 (Can’t Comply) or 2 (Will Comply).
        response = self.clone()
        response.commandResponse = rt900Consts.CommandResponse.WILL_COMPLY.value
        # Per Kevin Lee, NG 2/14/19
        # if (response.controlCode < rt900Consts.ControlCode.WEAPONS_HOLD.value) or (response.controlCode > rt900Consts.ControlCode.WEAPONS_FREE.value):
        #     response.controlCode = rt900Consts.ControlCode.WEAPONS_HOLD.value

        response.header.transmitTime.data = millisSinceMidnight()
        return response


class rt900Consts:
    """Contains constants for the 900 Weapon Command (see doc 3.3.1 Table III)."""
    
    class CommandCode(Enum):
        NO_STATEMENT = ElementUInt8(0)
        STATUS_REQU = ElementUInt8(1)
        AIR_TRACK_SURV_REQ = ElementUInt8(2)
        RAM_TRACK_SURV_REQ = ElementUInt8(3)
        # 4, 5, 6 are reserved
        CONTROL_CODE = ElementUInt8(7)
        CANCEL_SURV_AIR_TRACK_REQ = ElementUInt8(8)
        CANCEL_SURV_RAM_TRACK_REQ = ElementUInt8(9)
        ENABLE_TRANSMISSION_WEAPON_NO_FIRE = ElementUInt8(10)
        DISABLE_TRANSMISSION_WEAPON_NO_FIRE = ElementUInt8(11)
        # values > 11 not used
    
    class FireControlMode(Enum):
        NO_STATEMENT = ElementUInt8(0)
        COMMAND_MODE = ElementUInt8(1)
        ALLOCATE_MODE = ElementUInt8(2)
        # values > 2 not used
        
    class PlanID(Enum): NO_STATEMENT = ElementUInt16(0)
        # 1 - 65535 for Engagement Plan ID
        
    class ControlCode(Enum):
        NO_STATEMENT = ElementUInt16(0)
        RF_SILENCE = ElementUInt16(1)
        # 2 is reserved
        MAINTENANCE = ElementUInt16(3)
        REGISTRATION = ElementUInt16(4)
        WEAPONS_HOLD = ElementUInt16(5)
        WEAPON_TIGHT = ElementUInt16(6)
        WEAPONS_FREE = ElementUInt16(7)
        SIMULATED_FLIGHT = ElementUInt16(8)
        LOCAL_CONTROL = ElementUInt16(9)
        REMOTE_INACTIVE = ElementUInt16(10)
        REMOTE_ACTIVE = ElementUInt16(11)
        CALIBRATION_MODE = ElementUInt16(12)
        
    class SysTrackID(Enum): NO_STATEMENT = ElementUInt32(0)
        # 1 - (2^32 - 1) is track ID of RAM/Air Track, used with Command Codes 2, 3, 8, 9
        
    class CommandResponse(Enum):
        NO_STATEMENT = ElementUInt8(0)
        CANNOT_COMPLY = ElementUInt8(1)
        WILL_COMPLY = ElementUInt8(2)
        
    class FiringUnitID(Enum): ALL_APPLICABLE_FIRING_UNITS = ElementUInt16(0)
        
