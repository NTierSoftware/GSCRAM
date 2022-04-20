# ElementInt16.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/3/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import int16ToBytes
from Utilities.NumConversion import int16FromBytes


class ElementInt16(DataElement):
    """This class defines a basic CRAM message that contains a single 16-bit signed integer."""
    
    def getByteArray(self) -> bytearray:
        """Returns the object's 16-bit signed integer as a series of 2 bytes in a bytearray."""
        return int16ToBytes(self.data)
            
    def getNumBytes(self) -> int:
        return 2
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        """Returns an ElementInt16 instance constructed from bytes."""
        return cls(int16FromBytes(byteList))

def main():
    temp = ElementInt16(10000)
    print(temp.toJSON(True))
    temp.log()
    
if __name__ == "__main__":main()
