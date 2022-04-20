# author: Alex Erf, Airspace, alex.erf@airspace.co, 7/30/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import uint16ToBytes, uint16FromBytes

class ElementUInt16(DataElement):
    """This class defines a basic CRAM message that contains a single 16-bit unsigned integer."""
    
    def getByteArray(self) -> bytearray:
        if isinstance(self.data, str): self.data = int(self.data) #todo kluge
        """Returns the object's 16-bit unsigned integer as a series of 2 bytes in a bytearray."""
        return uint16ToBytes(self.data)
            
    def getNumBytes(self) -> int: return 2
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray): return cls(uint16FromBytes(byteList))


if __name__ == "__main__":
    temp = ElementUInt16(10000)
    print(temp.toJSON(True))
    temp.log()
    print(temp.getByteArray())

