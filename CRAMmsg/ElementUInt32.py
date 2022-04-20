# ElementUInt32.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/30/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import uint32ToBytes
from Utilities.NumConversion import uint32FromBytes


class ElementUInt32(DataElement):
    """This class defines a basic CRAM message that contains a single 32-bit unsigned integer."""
    
    def getByteArray(self) -> bytearray:
        """Returns the object's 32-bit unsigned integer as a series of 4 bytes in a bytearray."""
        return uint32ToBytes(self.data)
    
    def getNumBytes(self) -> int:
        return 4
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        # print("ElementUInt32(DataElement).genFromBytes() HEADER LENGTH!:", cls(uint32FromBytes(byteList)))
        return cls(uint32FromBytes(byteList))

def main():
    temp = ElementUInt32(100000)
    print(temp)
    temp.log()
    
if __name__ == "__main__":main()
