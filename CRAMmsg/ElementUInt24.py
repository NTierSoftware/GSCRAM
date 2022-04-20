# ElementUInt24.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/9/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import uint24ToBytes
from Utilities.NumConversion import uint24FromBytes


class ElementUInt24(DataElement):

    def getByteArray(self) -> bytearray:
        """Returns the object's 32-bit unsigned integer as a series of 4 bytes in a bytearray."""
        return uint24ToBytes(self.data)

    def getNumBytes(self) -> int:
        return 3

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        return cls(uint24FromBytes(byteList))

