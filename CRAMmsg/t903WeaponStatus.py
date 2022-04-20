# t903WeaponHeartbeat.py
# author: Alex Erf, Airspace, alex.erf@airspace.co, JD, date created: 8/1/2018
from enum import Enum
from typing import List

from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.Element import Element
from CRAMmsg.ElementInt8 import ElementInt8
from CRAMmsg.ElementInt16 import ElementInt16
from CRAMmsg.ElementInt32 import ElementInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.Header import Header, HeaderConsts

# from CoordTransform.CRAMtofromLLA import CRAMpoint

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue
from Utilities.Wrap import wrap
# from GSmsg.rtDroneStatus import rtDroneStatus


class t903Consts:
    """Contains constants for the 903 Weapon Status (see doc 3.3.4 Tables VI and VII)."""
    class SysStatus(Enum):
        # 0 not used
        OPERATIONAL = ElementUInt8(1)
        DEGRADED = ElementUInt8(2)
        MAINTENANCE = ElementUInt8(3)
        NON_OPERATIONAL = ElementUInt8(4)
        RELOADING = ElementUInt8(5)
        # >5 not used

    class CommStatusC2S(Enum):
        # 0 not used
        OPERATIONAL = ElementUInt8(1)
        DEGRADED = ElementUInt8(2)
        MAINTENANCE = ElementUInt8(3)
        NON_OPERATIONAL = ElementUInt8(4)
        LOCAL_OVERRIDE = ElementUInt8(5)
        # >5 not used

    class VehicleDoorStatus(Enum):
        NO_STATEMENT = 0
        CLOSED = 1
        OPEN = 2
        # >2 not used

    class SearchSensorStatus(Enum):
        NO_STATEMENT = ElementUInt8(0)
        OPERATIONAL = ElementUInt8(1)
        DEGRADED = ElementUInt8(2)
        MAINTENANCE = ElementUInt8(3)
        NON_OPERATIONAL = ElementUInt8(4)
        # >4 not used

    class FC_TrackSensorStatus(Enum):
        NO_STATEMENT = ElementUInt8(0)
        OPERATIONAL = ElementUInt8(1)
        DEGRADED = ElementUInt8(2)
        MAINTENANCE = ElementUInt8(3)
        NON_OPERATIONAL = ElementUInt8(4)
        # >4 not used

    class VisualIDSensorStatus(Enum):
        NO_STATEMENT = ElementUInt8(0)
        OPERATIONAL = ElementUInt8(1)
        DEGRADED = ElementUInt8(2)
        MAINTENANCE = ElementUInt8(3)
        NON_OPERATIONAL = ElementUInt8(4)
        # >4 not used

    class SensorNumFaces(Enum): FACE_INDEPENDENT = ElementUInt8(0)
        # 1-4 is number of faces
        # >4 not used

    class HoldFire(Enum):
        NO_STATEMENT = ElementUInt8(0)
        HOLD_FIRE_ENABLED = ElementUInt8(1)  # applicable to gun system only

    class SysMode(Enum):
        NO_STATEMENT = ElementUInt16(0)
        AIR_READY = ElementUInt16(1)
        SEARCH = ElementUInt16(2)
        ACQUISITION = ElementUInt16(3)
        TRACK = ElementUInt16(4)
        FIRE = ElementUInt16(5)
        MAINTENANCE = ElementUInt16(6)
        SYS_OPERABILITY_TEST = ElementUInt16(7)
        TRANSMIT_TEST = ElementUInt16(8)
        PRE_AIM_CALIB = ElementUInt16(9)
        SEARCH_TEST = ElementUInt16(10)
        TOAST = ElementUInt16(11)
        OTHER_WEAPON_ENGAGEMENT = ElementUInt16(12)
        # all other values not defined

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
        COYOTE = ElementUInt16(9) #Use this for EXPW per Sara Meves 3/14/19 email
        CLWS = ElementUInt16(10)
        CYCLOPS = ElementUInt16(11)
        RIwP = ElementUInt16(12)
        POSITIONER = ElementUInt16(13)
        CUJO = ElementUInt16(14)
        # >14 is reserved for growth

    class ECEF_X(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Y(Enum): NO_STATEMENT = ElementInt32(0)
    class ECEF_Z(Enum): NO_STATEMENT = ElementInt32(0)

    class MaxDefendedRange(Enum):
        NO_STATEMENT = ElementUInt32(0)
        ONEMILE = ElementUInt32(1609)

    class FireControlMode(Enum):
        # <3 not used
        RF_SILENCE = ElementUInt8(3)
        WEAPONS_HOLD = ElementUInt8(4)
        WEAPONS_TIGHT = ElementUInt8(5)
        WEAPONS_FREE = ElementUInt8(6)
        # 7 is reserved
        MAINTENANCE = ElementUInt8(8)
        REGISTRATION = ElementUInt8(9)
        SIM_FLIGHT = ElementUInt8(10)
        LOCAL_CONTROL = ElementUInt8(11)
        REMOTE_INACTIVE = ElementUInt8(12)
        REMOVE_ACTIVE = ElementUInt8(13)
        CALIB_MODE = ElementUInt8(14)

    class FiringUnitStatus(Enum):
        NON_EXIST_LAUNCHER = ElementUInt8(0)
        OPERATIONAL = ElementUInt8(1)
        DEGRADED = ElementUInt8(2)
        MAINTENANCE_RELOAD = ElementUInt8(3)
        NON_OPERATIONAL = ElementUInt8(4)
        OUT_OF_INVENTORY = ElementUInt8(5)
        TRAINING = ElementUInt8(6)
        EMPLACED = ElementUInt8(7)
        REMOTE_STDBY = ElementUInt8(8)
        NON_OPERATIONAL_GPS = ElementUInt8(9)
        LOW_INVENTORY = ElementUInt8(10)
        # >10 not used

    class FiringUnitInventory(Enum): UNLIMITED = ElementUInt16(65535)

    class AmmoKind(Enum):
        NO_STATEMENT = ElementInt8(0)
        M246 = ElementInt8(1)
        M940 = ElementInt8(2)
        MK149 = ElementInt8(3)
        MK244 = ElementInt8(4)
        M33 = ElementInt8(5)
        M788 = ElementInt8(6)
        INTERCEPTOR_2BFB = ElementInt8(7)
        # >7 not used

    class PrincipalAxis(Enum): NO_STATEMENT = ElementInt16(-32768)

    class InterceptorKind(Enum):
        NO_STATEMENT = ElementUInt8(0)
        AIM_9X = ElementUInt8(1)
        UNKNOWN_1 = ElementUInt8(2)
        UNKNOWN_2 = ElementUInt8(3)
        UNKNOWN_3 = ElementUInt8(4)
        UNKNOWN_4 = ElementUInt8(5)
        UNKNOWN_5 = ElementUInt8(6)


class t903WeaponStatus(CRAMBaseMessage):
    MSG_ID = 903

    def __init__(self, header: Header): super().__init__(header)
    
    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        if byteList[6] == HeaderConsts.InterfaceKind.AI3.value.data:
            return t903_AI3.genFromBytes(byteList)
        elif byteList[6] == HeaderConsts.InterfaceKind.MML.value.data:
            return t903_MML.genFromBytes(byteList)

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        msgId = objectToValue(objDict['messageHeader']['interfaceKind'], HeaderConsts.InterfaceKind)
        if msgId == HeaderConsts.InterfaceKind.AI3.value:
            return t903_AI3.constructFromDictionary(objDict)
        elif msgId == HeaderConsts.InterfaceKind.MML.value:
            return t903_MML.constructFromDictionary(objDict)



class t903_AI3(t903WeaponStatus):
    """See ICD 3.3.4, Table VI for information about the AI3 version of the 903 Message."""
    BASE_LENGTH = 60
    ADDITIONAL_LENGTH = 32
    INTERFACE = HeaderConsts.InterfaceKind.AI3.value

    def __init__(self, weaponId, fireControlModes, firingUnitECEF_Xs, firingUnitECEF_Ys, firingUnitECEF_Zs,
                 sysStatus=t903Consts.SysStatus.OPERATIONAL.value,
                 commStatus=t903Consts.CommStatusC2S.OPERATIONAL.value,
                 vehicleDoorStatus=t903Consts.VehicleDoorStatus.CLOSED.value,
                 searchSensorStatus=t903Consts.SearchSensorStatus.NO_STATEMENT.value,
                 fcTrackSensorStatus=t903Consts.FC_TrackSensorStatus.NO_STATEMENT.value,
                 visIdSensorStatus=t903Consts.VisualIDSensorStatus.NO_STATEMENT.value,
                 sensorNumFaces=t903Consts.SensorNumFaces.FACE_INDEPENDENT.value,
                 holdFire=t903Consts.HoldFire.NO_STATEMENT.value,
                 sysMode=t903Consts.SysMode.AIR_READY.value, #TODO FIX
                 # sysMode=t903Consts.SysMode.TRACK.value,
                 weaponKind=t903Consts.WeaponKind.COYOTE.value,
                 sensorECEF_X=t903Consts.ECEF_X.NO_STATEMENT.value,
                 sensorECEF_Y=t903Consts.ECEF_Y.NO_STATEMENT.value,
                 sensorECEF_Z=t903Consts.ECEF_Z.NO_STATEMENT.value,
                 sensorAzimuth=0,
                 # maxDefRange=t903Consts.MaxDefendedRange.ONEMILE.value,
                 maxDefRange=20000, #todo TEST FIX change
                 firingUnitStatuses=[t903Consts.FiringUnitStatus.OPERATIONAL.value],
                 firingUnitIds= [1],
                 firingUnitInvs=[4],
                 # firingUnitInvs=[t903Consts.FiringUnitInventory.UNLIMITED.value],
                 firingUnitRoundStdbys=[1],
                 firingUnitElevs=[5461], #todo 30 degrees?? same as simulator
                 firingUnitAzimuths=[0],
                 # firingUnitElevs=[0], firingUnitAzimuths=[0],
                 firingUnitStartBounds=[0], firingUnitEndBounds=[360],
                 ammoKinds=[t903Consts.AmmoKind.NO_STATEMENT.value], platformAzimuths=[0],
                 header: Header=None):
        super().__init__(header or Header(self.BASE_LENGTH + self.ADDITIONAL_LENGTH * len(fireControlModes), self.MSG_ID,
                                          self.INTERFACE, len(fireControlModes), millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.sysStatus = wrap(sysStatus, ElementUInt8)
        self.commStatus = wrap(commStatus, ElementUInt8)
        self.vehicleDoorStatus = wrap(vehicleDoorStatus, ElementUInt8)
        self.spare1 = ElementUInt8(0)
        self.searchSensorStatus = wrap(searchSensorStatus, ElementUInt8)
        self.fcTrackSensorStatus = wrap(fcTrackSensorStatus, ElementUInt8)
        self.visIdSensorStatus = wrap(visIdSensorStatus, ElementUInt8)
        self.sensorNumFaces = wrap(sensorNumFaces, ElementUInt8)
        self.holdFire = wrap(holdFire, ElementUInt8)
        self.spare1 = ElementUInt16(0)
        self.sysMode = wrap(sysMode, ElementUInt16)
        self.weaponKind = wrap(weaponKind, ElementUInt16)
        self.spare2 = ElementUInt32(0)
        self.sensorECEF_X = wrap(sensorECEF_X, ElementInt32)
        self.sensorECEF_Y = wrap(sensorECEF_Y, ElementInt32)
        self.sensorECEF_Z = wrap(sensorECEF_Z, ElementInt32)
        self.sensorAzimuth = wrap(sensorAzimuth, ElementUInt32)
        self.maxDefRange = wrap(maxDefRange, ElementUInt32)
        self.spare3 = ElementUInt32(0)
        self.spare4 = ElementUInt32(0)

        self.fireControlModes = []
        for fcm in fireControlModes: self.fireControlModes.append(wrap(fcm, ElementUInt8))

        self.firingUnitStatuses = []
        for fus in firingUnitStatuses: self.firingUnitStatuses.append(wrap(fus, ElementUInt8))

        self.firingUnitIds = []
        for fuid in firingUnitIds: self.firingUnitIds.append(wrap(fuid, ElementUInt16))

        self.firingUnitInvs = []
        for fuinv in firingUnitInvs: self.firingUnitInvs.append(wrap(fuinv, ElementUInt16))

        self.firingUnitRoundStdbys = []
        for furs in firingUnitRoundStdbys: self.firingUnitRoundStdbys.append(wrap(furs, ElementUInt16))

        self.firingUnitElevs = []
        for fue in firingUnitElevs: self.firingUnitElevs.append(wrap(fue, ElementInt16))

        self.firingUnitAzimuths = []
        for fua in firingUnitAzimuths: self.firingUnitAzimuths.append(wrap(fua, ElementUInt16))

        self.firingUnitECEF_Xs = []
        for fux in firingUnitECEF_Xs: self.firingUnitECEF_Xs.append(wrap(fux, ElementInt32))

        self.firingUnitECEF_Ys = []
        for fuy in firingUnitECEF_Ys: self.firingUnitECEF_Ys.append(wrap(fuy, ElementInt32))

        self.firingUnitECEF_Zs = []
        for fuz in firingUnitECEF_Zs: self.firingUnitECEF_Zs.append(wrap(fuz, ElementInt32))

        self.firingUnitStartBounds = []
        for fusb in firingUnitStartBounds: self.firingUnitStartBounds.append(wrap(fusb, ElementInt16))

        self.firingUnitEndBounds = []
        for fueb in firingUnitEndBounds: self.firingUnitEndBounds.append(wrap(fueb, ElementInt16))

        self.spare5n = [ElementUInt8(0)] * self.header.partCount.data

        self.ammoKinds = []
        for ammoKind in ammoKinds: self.ammoKinds.append(wrap(ammoKind, ElementInt8))

        self.platformAzimuths = []
        for platformAzimuth in platformAzimuths: self.platformAzimuths.append(wrap(platformAzimuth, ElementUInt16))

    # @classmethod #todo ??
    # def fromDroneStatus(cls, status: rtDroneStatus):
    #     CRAM: CRAMpoint = CRAMpoint.fromDroneStatus(status)
    #     return cls(status.ASdroneId, status.ec)

    # todo HAVE NOT CONFIRMED WHETHER THIS IS THE CORRECT FORMAT FOR PART COUNT > 1
    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 903.0 Weapon Status' data fields in order."""
        arr = [self.header, self.weaponId, self.sysStatus, self.commStatus, self.vehicleDoorStatus, self.searchSensorStatus,
               self.fcTrackSensorStatus, self.visIdSensorStatus, self.sensorNumFaces, self.holdFire, self.spare1,
               self.sysMode, self.weaponKind, self.spare2, self.sensorECEF_X, self.sensorECEF_Y, self.sensorECEF_Z,
               self.sensorAzimuth, self.maxDefRange, self.spare3, self.spare4]
        for i in range(0, self.header.partCount.data):
            arr.append(self.fireControlModes[i])
            arr.append(self.firingUnitStatuses[i])
            arr.append(self.firingUnitIds[i])
            arr.append(self.firingUnitInvs[i])
            arr.append(self.firingUnitRoundStdbys[i])
            arr.append(self.firingUnitElevs[i])
            arr.append(self.firingUnitAzimuths[i])
            arr.append(self.firingUnitECEF_Xs[i])
            arr.append(self.firingUnitECEF_Ys[i])
            arr.append(self.firingUnitECEF_Zs[i])
            arr.append(self.firingUnitStartBounds[i])
            arr.append(self.firingUnitEndBounds[i])
            arr.append(self.spare5n[i])
            arr.append(self.ammoKinds[i])
            arr.append(self.platformAzimuths[i])
        return arr

    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 903.0 Weapon Status' data fields' names in order."""
        arr = ['messageHeader', 'weaponId', 'sysStatus', 'commStatusC2S', 'vehicleDoorStatus', 'searchSensorStatus',
               'fcTrackSensorStatus', 'visIdSensorStatus', 'sensorNumFaces', 'holdFire', 'spare1',
               'sysMode', 'weaponKind', 'spare2', 'sensorECEF_X', 'sensorECEF_Y', 'sensorECEF_Z',
               'sensorAzimuth', 'maxDefRange', 'spare3', 'spare4']
        for i in range(0, self.header.partCount.data):
            arr.append('fireControlMode-' + str(i))
            arr.append('firingUnitStatus-' + str(i))
            arr.append('firingUnitId-' + str(i))
            arr.append('firingUnitInv-' + str(i))
            arr.append('firingUnitRoundStdby-' + str(i))
            arr.append('firingUnitElev-' + str(i))
            arr.append('firingUnitAzimuth-' + str(i))
            arr.append('firingUnitECEF_X-' + str(i))
            arr.append('firingUnitECEF_Y-' + str(i))
            arr.append('firingUnitECEF_Z-' + str(i))
            arr.append('firingUnitStartBound-' + str(i))
            arr.append('firingUnitEndBound-' + str(i))
            arr.append('spare5-' + str(i))
            arr.append('ammoKind-' + str(i))
            arr.append('platformAzimuth-' + str(i))
        return arr


    def getAllEnumGroups(self):
        arr = [None, None, t903Consts.SysStatus, t903Consts.CommStatusC2S, t903Consts.VehicleDoorStatus,
               t903Consts.SearchSensorStatus, t903Consts.FC_TrackSensorStatus, t903Consts.VisualIDSensorStatus,
               t903Consts.SensorNumFaces, t903Consts.HoldFire, None, t903Consts.SysMode, t903Consts.WeaponKind,
               None,
               t903Consts.ECEF_X, t903Consts.ECEF_Y, t903Consts.ECEF_Z,
               None, t903Consts.MaxDefendedRange, None, None]
        for i in range(0, self.header.partCount.data):
            arr.extend([t903Consts.FireControlMode, t903Consts.FiringUnitStatus, None, t903Consts.FiringUnitInventory,
                        None, None, None,
                        t903Consts.ECEF_X, t903Consts.ECEF_Y, t903Consts.ECEF_Z,
                        None, None, None, t903Consts.AmmoKind, None])
        return arr

    # The __init__ function ensures that the header stores the proper number of bytes.
    def getNumBytes(self) -> int: return self.header.messageLength.data

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])
        fireControlModes = []
        firingUnitStatuses = []
        firingUnitIds = []
        firingUnitInvs = []
        firingUnitRoundStdbys = []
        firingUnitElevs = []
        firingUnitAzimuths = []
        firingUnitECEF_Xs = []
        firingUnitECEF_Ys = []
        firingUnitECEF_Zs = []
        firingUnitStartBounds = []
        firingUnitEndBounds = []
        ammoKinds = []
        platformAzimuths = []
        for i in range(0, header.partCount.data):
            fireControlModes.append(objectToValue(objDict['fireControlMode-' + str(i)], t903Consts.FireControlMode))
            firingUnitStatuses.append(objectToValue(objDict['firingUnitStatus-' + str(i)], t903Consts.FiringUnitStatus))
            firingUnitIds.append(objDict['firingUnitId-' + str(i)])
            firingUnitInvs.append(objectToValue(objDict['firingUnitInv-' + str(i)], t903Consts.FiringUnitInventory))
            firingUnitRoundStdbys.append(objDict['firingUnitRoundStdby-' + str(i)])
            firingUnitElevs.append(objDict['firingUnitElev-' + str(i)])
            firingUnitAzimuths.append(objDict['firingUnitAzimuth-' + str(i)])
            firingUnitECEF_Xs.append(objDict['firingUnitECEF_X-' + str(i)])
            firingUnitECEF_Ys.append(objDict['firingUnitECEF_Y-' + str(i)])
            firingUnitECEF_Zs.append(objDict['firingUnitECEF_Z-' + str(i)])
            firingUnitStartBounds.append(objDict['firingUnitStartBound-' + str(i)])
            firingUnitEndBounds.append(objDict['firingUnitEndBound-' + str(i)])
            ammoKinds.append(objectToValue(objDict['ammoKind-' + str(i)], t903Consts.AmmoKind))
            platformAzimuths.append(objDict['platformAzimuth-' + str(i)])

        sysStatus = objectToValue(objDict['sysStatus'], t903Consts.SysStatus)
        commStatus = objectToValue(objDict['commStatusC2S'], t903Consts.CommStatusC2S)
        vehicleDoorStatus = objectToValue(objDict['vehicleDoorStatus'], t903Consts.VehicleDoorStatus)
        searchSensorStatus = objectToValue(objDict['searchSensorStatus'], t903Consts.SearchSensorStatus)
        fcTrackSensorStatus = objectToValue(objDict['fcTrackSensorStatus'], t903Consts.FC_TrackSensorStatus)
        visIdSensorStatus = objectToValue(objDict['visIdSensorStatus'], t903Consts.VisualIDSensorStatus)
        sensorNumFaces = objectToValue(objDict['sensorNumFaces'], t903Consts.SensorNumFaces)
        holdFire = objectToValue(objDict['holdFire'], t903Consts.HoldFire)
        sysMode = objectToValue(objDict['sysMode'], t903Consts.SysMode)
        weaponKind = objectToValue(objDict['weaponKind'], t903Consts.WeaponKind)
        sensorECEF_X = objectToValue(objDict['sensorECEF_X'], t903Consts.ECEF_X)
        sensorECEF_Y = objectToValue(objDict['sensorECEF_Y'], t903Consts.ECEF_Y)
        sensorECEF_Z = objectToValue(objDict['sensorECEF_Z'], t903Consts.ECEF_Z)
        maxDefRange = objectToValue(objDict['maxDefRange'], t903Consts.MaxDefendedRange)


        return cls(objDict['weaponId'], fireControlModes, firingUnitECEF_Xs, firingUnitECEF_Ys, firingUnitECEF_Zs,
                   sysStatus, commStatus, vehicleDoorStatus, searchSensorStatus,
                   fcTrackSensorStatus, visIdSensorStatus, sensorNumFaces, holdFire, sysMode, weaponKind, sensorECEF_X,
                   sensorECEF_Y, sensorECEF_Z, objDict['sensorAzimuth'], maxDefRange,
                   firingUnitStatuses, firingUnitIds, firingUnitInvs, firingUnitRoundStdbys,
                   firingUnitElevs, firingUnitAzimuths,
                   firingUnitStartBounds, firingUnitEndBounds, ammoKinds, platformAzimuths, header)


    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        sysStatus = ElementUInt8.genFromBytes(byteList[14:15])
        commStatus = ElementUInt8.genFromBytes(byteList[15:16])
        vehicleDoorStatus = ElementUInt8.genFromBytes(byteList[16:17])
        searchSensorStatus = ElementUInt8.genFromBytes(byteList[17:18])
        fcTrackSensorStatus = ElementUInt8.genFromBytes(byteList[18:19])
        visIdSensorStatus = ElementUInt8.genFromBytes(byteList[19:20])
        sensorNumFaces = ElementUInt8.genFromBytes(byteList[20:21])
        holdFire = ElementUInt8.genFromBytes(byteList[21:22])
        # bytes 22 - 23 are for spare
        sysMode = ElementUInt16.genFromBytes(byteList[24:26])
        weaponKind = ElementUInt16.genFromBytes(byteList[26:28])
        # bytes 28 - 31 are for spare
        sensorECEF_X = ElementInt32.genFromBytes(byteList[32:36])
        sensorECEF_Y = ElementInt32.genFromBytes(byteList[36:40])
        sensorECEF_Z = ElementInt32.genFromBytes(byteList[40:44])
        sensorAzimuth = ElementUInt32.genFromBytes(byteList[44:48])
        maxDefRange = ElementUInt32.genFromBytes(byteList[48:52])
        # bytes 52 - 59 are for spare
        fireControlModes = []
        firingUnitStatuses = []
        firingUnitIDs = []
        firingUnitInvs = []
        firingUnitRoundStdbys = []
        firingUnitElevs = []
        firingUnitAzimuths = []
        firingUnitECEF_Xs = []
        firingUnitECEF_Ys = []
        firingUnitECEF_Zs = []
        firingUnitStartBounds = []
        firingUnitEndBounds = []
        ammoKinds = []
        platformAzimuths = []
        for i in range(0, header.partCount.data):
            fireControlModes.append(ElementUInt8.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 60 : cls.ADDITIONAL_LENGTH * i + 61]))
            firingUnitStatuses.append(ElementUInt8.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 61 : cls.ADDITIONAL_LENGTH * i + 62]))
            firingUnitIDs.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 62 : cls.ADDITIONAL_LENGTH * i + 64]))
            firingUnitInvs.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 64 : cls.ADDITIONAL_LENGTH * i + 66]))
            firingUnitRoundStdbys.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 66 : cls.ADDITIONAL_LENGTH * i + 68]))
            firingUnitElevs.append(ElementInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 68 : cls.ADDITIONAL_LENGTH * i + 70]))
            firingUnitAzimuths.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 70 : cls.ADDITIONAL_LENGTH * i + 72]))
            firingUnitECEF_Xs.append(ElementInt32.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 72 : cls.ADDITIONAL_LENGTH * i + 76]))
            firingUnitECEF_Ys.append(ElementInt32.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 76 : cls.ADDITIONAL_LENGTH * i + 80]))
            firingUnitECEF_Zs.append(ElementInt32.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 80 : cls.ADDITIONAL_LENGTH * i + 84]))
            firingUnitStartBounds.append(ElementInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 84 : cls.ADDITIONAL_LENGTH * i + 86]))
            firingUnitEndBounds.append(ElementInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 86 : cls.ADDITIONAL_LENGTH * i + 88]))
            # cls.ADDITIONAL_LENGTH * i + 88 is for spare
            ammoKinds.append(ElementInt8.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 89 : cls.ADDITIONAL_LENGTH * i + 90]))
            platformAzimuths.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 90 : cls.ADDITIONAL_LENGTH * i + 92]))


        return cls(weaponId, fireControlModes, firingUnitECEF_Xs, firingUnitECEF_Ys, firingUnitECEF_Zs,
                   sysStatus, commStatus, vehicleDoorStatus, searchSensorStatus,
                   fcTrackSensorStatus, visIdSensorStatus, sensorNumFaces, holdFire, sysMode, weaponKind, sensorECEF_X,
                   sensorECEF_Y, sensorECEF_Z, sensorAzimuth, maxDefRange,
                   firingUnitStatuses, firingUnitIDs, firingUnitInvs, firingUnitRoundStdbys,
                   firingUnitElevs, firingUnitAzimuths,
                   firingUnitStartBounds, firingUnitEndBounds, ammoKinds, platformAzimuths, header)


class t903_MML(t903WeaponStatus):
    """See ICD 3.3.4, Table VII for information about the MML version of the 903 Message."""
    BASE_LENGTH = 68
    ADDITIONAL_LENGTH = 8
    INTERFACE = HeaderConsts.InterfaceKind.MML.value

    def __init__(self, weaponId, sysStatus, commStatus, carrierPitch, carrierRoll, pplAxis1_Fw, pplAxis1_Right,
                 pplAxis1_Down, pplAxis2_Fw, pplAxis2_Right, pplAxis2_Down, maxDefRange, weaponKind, fireControlMode,
                 firingUnitStatus, firingUnitID, firingUnitElev, firingUnitAzimuth, firingUnitECEF_X, firingUnitECEF_Y,
                 firingUnitECEF_Z, firingUnitInvs, firingUnitRoundStdbys, firingUnitRoundReadys, interceptorKinds, header: Header=None):
        super().__init__(header or Header(self.BASE_LENGTH + self.ADDITIONAL_LENGTH * len(firingUnitInvs), self.MSG_ID,
                                          self.INTERFACE, len(firingUnitInvs), millisSinceMidnight()))
        self.weaponId = wrap(weaponId, ElementUInt16)
        self.sysStatus = wrap(sysStatus, ElementUInt8)
        self.commStatus = wrap(commStatus, ElementUInt8)
        self.carrierPitch = wrap(carrierPitch, ElementInt16)
        self.carrierRoll = wrap(carrierRoll, ElementInt16)
        self.spare1 = ElementUInt16(0)
        self.pplAxis1_Fw = wrap(pplAxis1_Fw, ElementInt16)
        self.pplAxis1_Right = wrap(pplAxis1_Right, ElementInt16)
        self.pplAxis1_Down = wrap(pplAxis1_Down, ElementInt16)
        self.pplAxis2_Fw = wrap(pplAxis2_Fw, ElementInt16)
        self.pplAxis2_Right = wrap(pplAxis2_Right, ElementInt16)
        self.pplAxis2_Down = wrap(pplAxis2_Down, ElementInt16)
        self.spare2 = ElementUInt16(0)
        self.maxDefRange = wrap(maxDefRange, ElementUInt32)
        self.weaponKind = wrap(weaponKind, ElementUInt16)
        self.fireControlMode = wrap(fireControlMode, ElementUInt8)
        self.firingUnitStatus = wrap(firingUnitStatus, ElementUInt8)
        self.firingUnitID = wrap(firingUnitID, ElementUInt16)
        self.firingUnitElev = wrap(firingUnitElev, ElementInt16)
        self.firingUnitAzimuth = wrap(firingUnitAzimuth, ElementUInt16)
        self.spare3 = ElementUInt16(0)
        self.firingUnitECEF_X = wrap(firingUnitECEF_X, ElementInt32)
        self.firingUnitECEF_Y = wrap(firingUnitECEF_Y, ElementInt32)
        self.firingUnitECEF_Z = wrap(firingUnitECEF_Z, ElementInt32)
        self.spare4 = ElementUInt32(0)

        self.firingUnitInvs = []
        for fuinv in firingUnitInvs: self.firingUnitInvs.append(wrap(fuinv, ElementUInt16))

        self.firingUnitRoundStdbys = []
        for furs in firingUnitRoundStdbys: self.firingUnitRoundStdbys.append(wrap(furs, ElementUInt16))

        self.firingUnitRoundReadys = []
        for furr in firingUnitRoundReadys: self.firingUnitRoundReadys.append(wrap(furr, ElementUInt16))

        self.interceptorKinds = []
        for ik in interceptorKinds: self.interceptorKinds.append(wrap(ik, ElementUInt8))

        self.spare5n = [ElementUInt8(0)] * self.header.partCount.data

    # HAVE NOT CONFIRMED WHETHER THIS IS THE CORRECT FORMAT FOR PART COUNT > 1
    def getAllFields(self) -> List[Element]:
        """Returns a list of all of the 903.1 Weapon Status' data fields in order."""
        arr = [self.header, self.weaponId, self.sysStatus, self.commStatus, self.carrierPitch, self.carrierRoll,
               self.spare1, self.pplAxis1_Fw, self.pplAxis1_Right, self.pplAxis1_Down, self.pplAxis2_Fw,
               self.pplAxis2_Right, self.pplAxis2_Down, self.spare2, self.maxDefRange, self.weaponKind,
               self.fireControlMode, self.firingUnitStatus, self.firingUnitID, self.firingUnitElev,
               self.firingUnitAzimuth, self.spare3, self.firingUnitECEF_X, self.firingUnitECEF_Y, self.firingUnitECEF_Z,
               self.spare4]
        for i in range(0, self.header.partCount.data):
            arr.append(self.firingUnitInvs[i])
            arr.append(self.firingUnitRoundStdbys[i])
            arr.append(self.firingUnitRoundReadys[i])
            arr.append(self.interceptorKinds[i])
            arr.append(self.spare5n[i])
        return arr

    def getAllFieldNames(self) -> List[str]:
        """Returns a list of all of the 903.0 Weapon Status' data fields' names in order."""
        arr = ['messageHeader', 'weaponId', 'sysStatus', 'commStatusC2S', 'carrierPitch', 'carrierRoll',
               'spare1', 'pplAxis1_Fw', 'pplAxis1_Right', 'pplAxis1_Down', 'pplAxis2_Fw',
               'pplAxis2_Right', 'pplAxis2_Down', 'spare2', 'maxDefRange', 'weaponKind',
               'fireControlMode', 'firingUnitStatus', 'firingUnitID', 'firingUnitElev',
               'firingUnitAzimuth', 'spare3', 'firingUnitECEF_X', 'firingUnitECEF_Y', 'firingUnitECEF_Z',
               'spare4']
        for i in range(0, self.header.partCount.data):
            arr.append('firingUnitInvs-' + str(i))
            arr.append('firingUnitRoundStdbys-' + str(i))
            arr.append('firingUnitRoundReadys-' + str(i))
            arr.append('interceptorKinds-' + str(i))
            arr.append('spare5-' + str(i))
        return arr

    def getAllEnumGroups(self):
        arr = [None, None, t903Consts.SysStatus, t903Consts.CommStatusC2S, None, None, None, t903Consts.PrincipalAxis,
               t903Consts.PrincipalAxis, t903Consts.PrincipalAxis, t903Consts.PrincipalAxis, t903Consts.PrincipalAxis,
               t903Consts.PrincipalAxis, None, t903Consts.MaxDefendedRange, t903Consts.WeaponKind,
               t903Consts.FireControlMode, t903Consts.FiringUnitStatus, None, None, None, None,
               t903Consts.ECEF_X, t903Consts.ECEF_Y, t903Consts.ECEF_Z,
               None]
        for i in range(0, self.header.partCount.data):
            arr.extend([t903Consts.FiringUnitInventory, None, None, t903Consts.InterceptorKind, None])
        return arr

    def getNumBytes(self) -> int:
        # The __init__ function ensures that the header stores the proper number of bytes.
        return self.header.messageLength.data

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])
        firingUnitInvs = []
        firingUnitRoundStdbys = []
        firingUnitRoundReadys = []
        interceptorKinds = []
        for i in range(0, header.partCount.data):
            firingUnitInvs.append(objectToValue(objDict['firingUnitInvs-' + str(i)], t903Consts.FiringUnitInventory))
            firingUnitRoundStdbys.append(objDict['firingUnitRoundStdbys-' + str(i)])
            firingUnitRoundReadys.append(objDict['firingUnitRoundReadys-' + str(i)])
            interceptorKinds.append(objectToValue(objDict['interceptorKinds-' + str(i)], t903Consts.InterceptorKind))

        sysStatus = objectToValue(objDict['sysStatus'], t903Consts.SysStatus)
        commStatus = objectToValue(objDict['commStatusC2S'], t903Consts.CommStatusC2S)
        pplAxis1_Fw = objectToValue(objDict['pplAxis1_Fw'], t903Consts.PrincipalAxis)
        pplAxis1_Right = objectToValue(objDict['pplAxis1_Right'], t903Consts.PrincipalAxis)
        pplAxis1_Down = objectToValue(objDict['pplAxis1_Down'], t903Consts.PrincipalAxis)
        pplAxis2_Fw = objectToValue(objDict['pplAxis2_Fw'], t903Consts.PrincipalAxis)
        pplAxis2_Right = objectToValue(objDict['pplAxis2_Right'], t903Consts.PrincipalAxis)
        pplAxis2_Down = objectToValue(objDict['pplAxis2_Down'], t903Consts.PrincipalAxis)
        maxDefRange = objectToValue(objDict['maxDefRange'], t903Consts.MaxDefendedRange)
        weaponKind = objectToValue(objDict['weaponKind'], t903Consts.WeaponKind)
        fireControlMode = objectToValue(objDict['fireControlMode'], t903Consts.FireControlMode)
        firingUnitStatus = objectToValue(objDict['firingUnitStatus'], t903Consts.FiringUnitStatus)
        firingUnitECEF_X = objectToValue(objDict['firingUnitECEF_X'], t903Consts.ECEF_X)
        firingUnitECEF_Y = objectToValue(objDict['firingUnitECEF_Y'], t903Consts.ECEF_Y)
        firingUnitECEF_Z = objectToValue(objDict['firingUnitECEF_Z'], t903Consts.ECEF_Z)

        return cls(objDict['weaponId'], sysStatus, commStatus, objDict['carrierPitch'], objDict['carrierRoll'],
                   pplAxis1_Fw, pplAxis1_Right, pplAxis1_Down, pplAxis2_Fw, pplAxis2_Right, pplAxis2_Down, maxDefRange,
                   weaponKind, fireControlMode, firingUnitStatus, objDict['firingUnitID'], objDict['firingUnitElev'],
                   objDict['firingUnitAzimuth'], firingUnitECEF_X, firingUnitECEF_Y, firingUnitECEF_Z, firingUnitInvs,
                   firingUnitRoundStdbys, firingUnitRoundReadys, interceptorKinds, header)

    @classmethod
    def genFromBytes(cls, byteList: bytearray):
        header = Header.genFromBytes(byteList[0:12])
        weaponId = ElementUInt16.genFromBytes(byteList[12:14])
        sysStatus = ElementUInt8.genFromBytes(byteList[14:15])
        commStatus = ElementUInt8.genFromBytes(byteList[15:16])
        carrierPitch = ElementInt16.genFromBytes(byteList[16:18])
        carrierRoll = ElementInt16.genFromBytes(byteList[18:20])
        # bytes 20 - 21 are for spare
        pplAxis1_Fw = ElementInt16.genFromBytes(byteList[22:24])
        pplAxis1_Right = ElementInt16.genFromBytes(byteList[24:26])
        pplAxis1_Down = ElementInt16.genFromBytes(byteList[26:28])
        pplAxis2_Fw = ElementInt16.genFromBytes(byteList[28:30])
        pplAxis2_Right = ElementInt16.genFromBytes(byteList[30:32])
        pplAxis2_Down = ElementInt16.genFromBytes(byteList[32:34])
        # bytes 34 - 35 are for spare
        maxDefRange = ElementUInt32.genFromBytes(byteList[36:40])
        weaponKind = ElementUInt16.genFromBytes(byteList[40:42])
        fireControlMode = ElementUInt8.genFromBytes(byteList[42:43])
        firingUnitStatus = ElementUInt8.genFromBytes(byteList[43:44])
        firingUnitID = ElementUInt16.genFromBytes(byteList[44:46])
        firingUnitElev = ElementInt16.genFromBytes(byteList[46:48])
        firingUnitAzimuth = ElementUInt16.genFromBytes(byteList[48:50])
        # bytes 50 - 51 are for spare
        firingUnitECEF_X = ElementInt32.genFromBytes(byteList[52:56])
        firingUnitECEF_Y = ElementInt32.genFromBytes(byteList[56:60])
        firingUnitECEF_Z = ElementInt32.genFromBytes(byteList[60:64])
        # bytes 64 - 67 are for spare

        firingUnitInvs = []
        firingUnitRoundStdbys = []
        firingUnitRoundReadys = []
        interceptorKinds = []
        for i in range(0, header.partCount.data):
            firingUnitInvs.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 68 : cls.ADDITIONAL_LENGTH * i + 70]))
            firingUnitRoundStdbys.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 70 : cls.ADDITIONAL_LENGTH * i + 72]))
            firingUnitRoundReadys.append(ElementUInt16.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 72 : cls.ADDITIONAL_LENGTH * i + 74]))
            interceptorKinds.append(ElementUInt8.genFromBytes(byteList[cls.ADDITIONAL_LENGTH * i + 74 : cls.ADDITIONAL_LENGTH * i + 75]))
            # bytes cls.ADDITIONAL_LENGTH * i + 75 is for spare

        return cls(weaponId, sysStatus, commStatus, carrierPitch, carrierRoll, pplAxis1_Fw, pplAxis1_Right,
                   pplAxis1_Down, pplAxis2_Fw, pplAxis2_Right, pplAxis2_Down, maxDefRange, weaponKind, fireControlMode,
                   firingUnitStatus, firingUnitID, firingUnitElev, firingUnitAzimuth, firingUnitECEF_X,
                   firingUnitECEF_Y, firingUnitECEF_Z, firingUnitInvs, firingUnitRoundStdbys,
                   firingUnitRoundReadys, interceptorKinds, header)


