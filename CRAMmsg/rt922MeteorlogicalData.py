# rt922MeteorlogicalDatapy
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/6/2018

from CRAMmsg.Element import Element
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementInt16 import ElementInt16

from Utilities.Wrap import wrap
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue

from typing import List

from enum import Enum


class rt922Consts:
    PULSE_RATE = 30.00 #3.3.23.1 The 922 message is transmitted periodically every 30 seconds, or upon threshold changes.

    """See ICD 3.3.23 - Table XXXV for information about the data fields and constants."""
    class WindSpeed(Enum): NO_STATEMENT = ElementUInt16(65535)

    class AbsAtmPressure(Enum): NO_STATEMENT = ElementUInt16(65535)


class rt922MeteorlogicalData(CRAMBaseMessage):
    """See ICD 3.3.23 for information about the 922 Meteorological Data Message."""
    MSG_LEN = 36
    MSG_ID = 922
    PART_COUNT = 0
    
    def __init__(self, ambientTemp=0, windSpd=rt922Consts.WindSpeed.NO_STATEMENT, windDir=0, absAtmPressure=rt922Consts.AbsAtmPressure.NO_STATEMENT, header: Header = None):

        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.ambientTemp = wrap(ambientTemp, ElementInt16)
        self.windSpd = wrap(windSpd, ElementUInt16)
        self.windDir = wrap(windDir, ElementUInt16)
        self.absAtmPressure = wrap(absAtmPressure, ElementUInt16)
        self.spare1 = ElementUInt32(0)
        self.spare2 = ElementUInt32(0)
        self.spare3 = ElementUInt32(0)
        self.spare4 = ElementUInt32(0)
    
    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 922 Command's data fields in order."""
        return [self.header, self.ambientTemp, self.windSpd, self.windDir, self.absAtmPressure, self.spare1,
                self.spare2, self.spare3, self.spare4]
    
    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 922 Command's data fields' names in order."""
        return ['messageHeader', 'ambientTemp', 'windSpd', 'windDir', 'absAtmPressure', 'spare1',
                'spare2', 'spare3', 'spare4']

    def getAllEnumGroups(self) -> List:
        return [None, None, rt922Consts.WindSpeed, None, rt922Consts.AbsAtmPressure, None, None, None, None]
    
    def getNumBytes(self) -> int: return self.MSG_LEN
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        ambientTemp = ElementInt16.genFromBytes(byteList[12:14])
        windSpd = ElementUInt16.genFromBytes(byteList[14:16])
        windDir = ElementUInt16.genFromBytes(byteList[16:18])
        absAtmPressure = ElementUInt16.genFromBytes(byteList[18:20])
        # bytes 20 - 35 are all for spare
        return cls(ambientTemp, windSpd, windDir, absAtmPressure, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        windSpd = objectToValue(objDict['windSpd'], rt922Consts.WindSpeed)
        absAtmPressure = objectToValue(objDict['absAtmPressure'], rt922Consts.AbsAtmPressure)

        return cls(objDict['ambientTemp'], windSpd, objDict['windDir'], absAtmPressure, header)
    
