# Header.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/30/2018


from CRAMmsg.Element import Element
from CRAMmsg.CompoundElement import CompoundElement
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.CRAMmsgType import CRAMmsgType

from typing import List

from Utilities.Wrap import wrap
from Utilities.ValueNameConversion import objectToValue

from enum import Enum


class Header(CompoundElement):
    MSG_LEN = 12
    
    def __init__(self, length, msgId, kind, count, time):
        self.messageLength = wrap(length, ElementUInt32)
        self.messageId = wrap(msgId, ElementUInt16)
        self.interfaceKind = wrap(kind, ElementUInt8)
        self.partCount = wrap(count, ElementUInt8)
        self.transmitTime = wrap(time, ElementUInt32)

    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the header's data fields in order."""
        return [self.messageLength, self.messageId, self.interfaceKind, self.partCount, self.transmitTime]
    
    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the header's field names in order."""
        return ['messageLength', 'messageId', 'interfaceKind', 'partCount', 'transmitTime']

    def getAllEnumGroups(self):
        return [None, CRAMmsgType, HeaderConsts.InterfaceKind, None, None]
    
    def getNumBytes(self) -> int:
        return self.MSG_LEN
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        length = ElementUInt32.genFromBytes(byteList[0:4])
        msgId = ElementUInt16.genFromBytes(byteList[4:6])
        interfaceKind = ElementUInt8.genFromBytes(byteList[6:7])
        partCount = ElementUInt8.genFromBytes(byteList[7:8])
        transmitTime = ElementUInt32.genFromBytes(byteList[8:12])
        return cls(length, msgId, interfaceKind, partCount, transmitTime)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        messageId = objectToValue(objDict['messageId'], CRAMmsgType)
        interfaceKind = objectToValue(objDict['interfaceKind'], HeaderConsts.InterfaceKind)
        return cls(objDict['messageLength'], messageId, interfaceKind,
                   objDict['partCount'], objDict['transmitTime'])

class HeaderConsts:
    """Contains constants for the Header element (see doc 3.2.4.3.1 Table II)."""

    class InterfaceKind(Enum):
        AI3 = ElementUInt8(0)
        MML = ElementUInt8(1)

    DEFAULT_INTERFACE = InterfaceKind.AI3
