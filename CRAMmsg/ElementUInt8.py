# ElementUInt8.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/30/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import uint8ToBytes
from Utilities.NumConversion import uint8FromBytes



class ElementUInt8(DataElement):
    """This class defines a basic CRAM message that contains a single 8-bit unsigned integer."""
    
    def getByteArray(self) -> bytearray:
        """Returns the object's 8-bit unsigned integer as a single byte in a bytearray."""
        return uint8ToBytes(self.data)
    
    def getNumBytes(self) -> int:
        return 1
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        return cls(uint8FromBytes(byteList))
    

def main():
    temp = ElementUInt8(200)
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
