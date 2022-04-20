# rt902WeaponHeartbeat.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/31/2018
# Note that this is the first message sent from IFPC MML to C2 upon socket initialization.

from CRAMmsg.Element import Element
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.Wrap import wrap
from Utilities.ValueNameConversion import objectToValue

from typing import List

from enum import Enum

class rt902Consts:
    """Contains constants for the 902 Weapon Heartbeat (see doc 3.3.3 Table V)."""

    PULSE_RATE = 2.00  # "3.3.3.1 The 902 message shall be transmitted at a rate of 0.5 Hz."

    class IFVersion(Enum):
        NO_STATEMENT = ElementUInt8(0)
        # 1, 2 are spare
        SUPPORTS_1H389_ICD_REV_C = ElementUInt8(3)
        SUPPORTS_1H389_ICD_REV_D = ElementUInt8(4)
        SUPPORTS_1H389_ICD_REV_E = ElementUInt8(5)
        SUPPORTS_1H389_ICD_REV_F_AND_NC = ElementUInt8(6)
        SUPPORTS_137_ICD_REV_A = ElementUInt8(7)
        SUPPORTS_137_ICD_REV_B = ElementUInt8(8)
        SUPPORTS_137_ICD_REV_C = ElementUInt8(9)
        SUPPORTS_137_ICD_REV_D = ElementUInt8(10)
        # 11 - 255 are spare

    class ActionRequest(Enum):
        NO_STATEMENT = ElementUInt8(0)
        WES_DATA_COLLECTION = ElementUInt8(1)


class rt902WeaponHeartbeat(CRAMBaseMessage):
    MSG_LEN = 20
    MSG_ID = 902
    PART_COUNT = 0

    def __init__(self, weaponId, IFVersion=rt902Consts.IFVersion.NO_STATEMENT.value,
                 actionRequest=rt902Consts.ActionRequest.NO_STATEMENT.value, header: Header=None):
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value,
                                          self.PART_COUNT, millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.IFVersion = wrap(IFVersion, ElementUInt8)
        self.actionRequest = wrap(actionRequest, ElementUInt8)
        self.spare1 = ElementUInt32(0)
    
    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 902 Command's data fields in order."""
        return [self.header, self.weaponId, self.IFVersion, self.actionRequest, self.spare1]
    
    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 902 Command's data fields' names in order."""
        return ['messageHeader', 'weaponId', 'IFVersion', 'actionRequest', 'spare1']

    def getAllEnumGroups(self) -> List:
        return [None, None, rt902Consts.IFVersion, rt902Consts.ActionRequest, None]

    def getNumBytes(self) -> int: return self.MSG_LEN
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        IFVersion = ElementUInt8.genFromBytes(byteList[14:15])
        actionRequest = ElementUInt8.genFromBytes(byteList[15:16])
        # bytes 16 - 19 are all for spare
        return cls(weaponId, IFVersion, actionRequest, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])
        IFVersion = objectToValue(objDict['IFVersion'], rt902Consts.IFVersion)
        actionReq = objectToValue(objDict['actionRequest'], rt902Consts.ActionRequest)
        return cls(objDict['weaponId'], IFVersion, actionReq, header)
