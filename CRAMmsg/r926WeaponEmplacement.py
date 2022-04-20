# r926WeaponEmplacement.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/15/2018

from CRAMmsg.Element import Element
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Header import Header
from CRAMmsg.Header import HeaderConsts
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementInt16 import ElementInt16
from CRAMmsg.ElementInt32 import ElementInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.Wrap import wrap
from Utilities.ValueNameConversion import objectToValue

from typing import List

from enum import Enum


class r926WeaponEmplacement(CRAMBaseMessage):
    MSG_LEN = 72
    MSG_ID = 926
    PART_COUNT = 0

    def __init__(self, weaponId, weaponKind, validTime, ECEF_X, ECEF_Y, ECEF_Z, ECEF_Vx, ECEF_Vy, ECEF_Vz, elevation,
                 azimuth, platformAzimuth, header: Header=None):
        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.weaponKind = wrap(weaponKind, ElementUInt16)
        self.validTime = wrap(validTime, ElementUInt32)
        self.ECEF_X = wrap(ECEF_X, ElementInt32)
        self.ECEF_Y = wrap(ECEF_Y, ElementInt32)
        self.ECEF_Z = wrap(ECEF_Z, ElementInt32)
        self.ECEF_Vx = wrap(ECEF_Vx, ElementInt32)
        self.ECEF_Vy = wrap(ECEF_Vy, ElementInt32)
        self.ECEF_Vz = wrap(ECEF_Vz, ElementInt32)
        self.elevation = wrap(elevation, ElementInt16)
        self.azimuth = wrap(azimuth, ElementUInt16)
        self.platformAzimuth = wrap(platformAzimuth, ElementUInt16)
        self.spare1 = ElementUInt16(0)
        self.spare2 = ElementUInt32(0)
        self.spare3 = ElementUInt32(0)
        self.spare4 = ElementUInt32(0)
        self.spare5 = ElementUInt32(0)
        self.spare6 = ElementUInt32(0)

    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 926 Command's data fields in order."""
        return [self.header, self.weaponId, self.weaponKind, self.validTime, self.ECEF_X, self.ECEF_Y, self.ECEF_Z,
                self.ECEF_Vx, self.ECEF_Vy, self.ECEF_Vz, self.elevation, self.azimuth, self.platformAzimuth,
                self.spare1, self.spare2, self.spare3, self.spare4, self.spare5, self.spare6]

    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 926 Command's data fields' names in order."""
        return ['messageHeader', 'weaponId', 'weaponKind', 'validTime', 'ECEF_X', 'ECEF_Y', 'ECEF_Z', 'ECEF_Vx',
                'ECEF_Vy', 'ECEF_Vz', 'elevation', 'azimuth', 'platformAzimuth', 'spare1', 'spare2', 'spare3', 'spare4',
                'spare5', 'spare6']

    def getAllEnumGroups(self) -> List:
        return [None, None, t926Consts.WeaponKind, t926Consts.ValidTime,
                t926Consts.ECEF_X, t926Consts.ECEF_Y, t926Consts.ECEF_Z,
                t926Consts.ECEF_Vx, t926Consts.ECEF_Vy, t926Consts.ECEF_Vz,
                None, None, None, None,
                None, None, None, None, None]

    def getNumBytes(self) -> int:
        return self.MSG_LEN

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        weaponKind = ElementUInt16.genFromBytes(byteList[14:16])
        validTime = ElementUInt32.genFromBytes(byteList[16:20])
        ECEF_X = ElementInt32.genFromBytes(byteList[20:24])
        ECEF_Y = ElementInt32.genFromBytes(byteList[24:28])
        ECEF_Z = ElementInt32.genFromBytes(byteList[28:32])
        ECEF_Vx = ElementInt32.genFromBytes(byteList[32:36])
        ECEF_Vy = ElementInt32.genFromBytes(byteList[36:40])
        ECEF_Vz = ElementInt32.genFromBytes(byteList[40:44])
        elevation = ElementInt16.genFromBytes(byteList[44:46])
        azimuth = ElementUInt16.genFromBytes(byteList[46:48])
        platformAzimuth = ElementUInt16.genFromBytes(byteList[48:50])
        # bytes 50 - 71 are for spare

        return cls(weaponId, weaponKind, validTime, ECEF_X, ECEF_Y, ECEF_Z, ECEF_Vx, ECEF_Vy, ECEF_Vz, elevation,
                   azimuth, platformAzimuth, header)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        weaponKind = objectToValue(objDict['weaponKind'], t926Consts.WeaponKind)
        validTime = objectToValue(objDict['validTime'], t926Consts.ValidTime)
        ECEF_X = objectToValue(objDict['ECEF_X'], t926Consts.ECEF_X)
        ECEF_Y = objectToValue(objDict['ECEF_Y'], t926Consts.ECEF_Y)
        ECEF_Z = objectToValue(objDict['ECEF_Z'], t926Consts.ECEF_Z)
        ECEF_Vx = objectToValue(objDict['ECEF_Vx'], t926Consts.ECEF_Vx)
        ECEF_Vy = objectToValue(objDict['ECEF_Vy'], t926Consts.ECEF_Vy)
        ECEF_Vz = objectToValue(objDict['ECEF_Vz'], t926Consts.ECEF_Vz)

        return cls(objDict['weaponId'], weaponKind, validTime, ECEF_X, ECEF_Y, ECEF_Z, ECEF_Vx, ECEF_Vy, ECEF_Vz,
                   objDict['elevation'], objDict['azimuth'], objDict['platformAzimuth'], header)


class t926Consts:

    class WeaponKind(Enum):
        NO_STATEMENT = ElementUInt16(0)
        GUN = ElementUInt16(1)
        IMPROVED_GUN = ElementUInt16(2)
        AI3_MISSILE = ElementUInt16(3)
        COUNTER_UAS_MISSILE = ElementUInt16(4)
        EAPS_MISSILE = ElementUInt16(5)
        DIRECTED_ENERGY = ElementUInt16(6)
        MULTI_MISSION_LAUNCHER = ElementUInt16(7)
        BLADE = ElementUInt16(8)
        COYOTE = ElementUInt16(9)
        CLWS = ElementUInt16(10)
        CYCLOPS = ElementUInt16(11)
        RIwP = ElementUInt16(12)
        POSITIONER = ElementUInt16(13)
        CUJO = ElementUInt16(14)
        # >14 is reserved for growth

    class ValidTime(Enum): NO_STATEMENT = ElementUInt32(4294967295)

    # class ECEF(Enum): NO_STATEMENT = ElementInt32(0)
    # class ECEF_V(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class ECEF_X(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Y(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Z(Enum): NO_STATEMENT = ElementInt32(0)

    class ECEF_Vx(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class ECEF_Vy(Enum): NO_STATEMENT = ElementInt32(-2147483648)
    class ECEF_Vz(Enum): NO_STATEMENT = ElementInt32(-2147483648)
