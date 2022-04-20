# ElementUInt128.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/31/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import uint128ToBytes
from Utilities.NumConversion import uint128FromBytes


class ElementUInt128(DataElement):
    """This class defines a basic CRAM message that contains a single 128-bit unsigned integer."""
    
    def getByteArray(self) -> bytearray:
        """Returns the object's 128-bit unsigned integer as a series of 16 bytes in a bytearray."""
        return uint128ToBytes(self.data)
    
    def getNumBytes(self) -> int:
        return 16
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        return cls(uint128FromBytes(byteList))
