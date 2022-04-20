# rt902WeaponHeartbeat.py
#
# author: JD, John.JD.Donaldson@airspace.co using Alex' code
# date created: 8/6/2018

from CRAMmsg.CompoundElement import CompoundElement
from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight


class u999Unimplemented(CompoundElement):
    """This class defines an as yet unimplemented message."""
    MSG_LEN = 12
    MSG_ID = 999
    PART_COUNT = 0
    
    def __init__(self, header = None, msgID = None):
        """Generate only the Header since this is as yet unimplemented."""
        self.header = header or Header(ElementUInt32(self.MSG_LEN),
                                       ElementUInt16(msgID or self.MSG_ID),
                                       ElementUInt8(HeaderConsts.DEFAULT_INTERFACE),
                                       ElementUInt8(self.PART_COUNT),
                                       ElementUInt32(millisSinceMidnight()))

    def getAllFields(self): return [self.header]
    
    def getAllFieldNames(self): return ['messageHeader']
    
    def getNumBytes(self): return self.MSG_LEN
    
    @classmethod
    def genFromBytes(cls, byteList):
        header = Header.genFromBytes(byteList[0:12])
        return cls(header)
    
    
