# ElementFloat32.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/8/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import float32ToBytes
from Utilities.NumConversion import float32FromBytes


class ElementFloat32(DataElement):

    def getByteArray(self) -> bytearray:
        return float32ToBytes(self.data)

    def getNumBytes(self) -> int:
        return 4

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        return cls(float32FromBytes(byteList))

