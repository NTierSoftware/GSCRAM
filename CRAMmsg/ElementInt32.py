# ElementInt32.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/2/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import int32ToBytes
from Utilities.NumConversion import int32FromBytes


class ElementInt32(DataElement):
    """This class defines a basic CRAM message that contains a single 32-bit unsigned integer."""
    
    def getByteArray(self) -> bytearray:
        """Returns the object's 32-bit signed integer as a series of 4 bytes in a bytearray."""
        return int32ToBytes(self.data)
    
    def getNumBytes(self) -> int:
        """Returns 4 because a 32-bit signed integer is always 4 bytes."""
        return 4
    
    @classmethod
    def genFromBytes(cls, byteList):
        """Returns an ElementInt32 instance constructed from bytes."""
        return cls(int32FromBytes(byteList))
