# ElementInt8.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/3/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import int8ToBytes
from Utilities.NumConversion import int8FromBytes


class ElementInt8(DataElement):
    """This class defines a basic CRAM message that contains a single 8-bit signed integer."""
    
    def getByteArray(self) -> bytearray:
        """Returns the object's 8-bit signed integer as a single byte in a bytearray."""
        return int8ToBytes(self.data)
    
    def getNumBytes(self) -> int:
        """Returns 1 because an 8-bit signed integer is always 1 byte."""
        return 1
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        """Returns an ElementInt8 instance constructed from bytes."""
        return cls(int8FromBytes(byteList))
    

def main():
    temp = ElementInt8(200)
    print(temp.toJSON())
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    temp.log()
    
if __name__ == "__main__":main()
