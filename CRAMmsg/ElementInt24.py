# ElementInt24.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/10/2018

from CRAMmsg.DataElement import DataElement
from Utilities.NumConversion import int24ToBytes
from Utilities.NumConversion import int24FromBytes
from Utilities.Wrap import wrap


class ElementInt24(DataElement):

    def getByteArray(self) -> bytearray:
        return int24ToBytes(self.data)

    def getNumBytes(self) -> int:
        return 3

    @classmethod
    def genFromBytes(cls, byteList):
        byteList = wrap(byteList, bytearray)
        return cls(int24FromBytes(byteList))
