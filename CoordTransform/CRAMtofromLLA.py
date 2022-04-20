# http://danceswithcode.net/engineeringnotes/geodetic_to_ecef/geodetic_to_ecef.html
import math, json
from GSmsg.GSBaseMessage import GSBaseMessage
from typing import List
from GSmsg.rtDroneStatus import rtDroneStatus
class LLApoint(GSBaseMessage):
    def __init__(self, Lat: float, Lon: float, Elev: float ):
        self.Lat:float = float(Lat)
        self.Lon:float = float(Lon)
        self.Elev:float = float(Elev)

    def getDataObject(self) -> dict:
        wf = {}
        wf['Lat'] = self.Lat
        wf['Lon'] = self.Lon
        wf['Elev'] = self.Elev
        return wf

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'LLApoint':
        wf = json.loads(jsonStr)
        return cls( wf['Lat'], wf['Lon'], wf['Elev'])

    def fromCRAM(CRAM:'CRAMpoint'):
        return ECEFtofromLLA.CRAMtoLLA(CRAM)

    def toCRAM(self) -> 'CRAMpoint':
        return ECEFtofromLLA.LLAtoCRAM(self)

# https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes?noredirect=1&lq=1
    def __eq__(self, other):
        return (self.Lat == other.Lat) and (self.Lon == other.Lon) and (self.Elev == other.Elev)


class ECEFpoint(GSBaseMessage):
    def __init__(self, ECEF_X: float, ECEF_Y: float, ECEF_Z: float):
        self.ECEF_X = ECEF_X
        self.ECEF_Y = ECEF_Y
        self.ECEF_Z = ECEF_Z

    def getDataObject(self) -> dict:
        wf = {}
        wf['ECEF_X'] = self.ECEF_X
        wf['ECEF_Y'] = self.ECEF_Y
        wf['ECEF_Z'] = self.ECEF_Z
        return wf

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'ECEFpoint':
        wf = json.loads(jsonStr)
        return cls( wf['ECEF_X'], wf['ECEF_Y'], wf['ECEF_Z'])


class CRAMpoint(ECEFpoint):
    def __init__(self, ECEF_X: int, ECEF_Y: int, ECEF_Z: int):
        super().__init__(ECEF_X, ECEF_Y, ECEF_Z)

    @classmethod
    def fromECEF(cls, ECEF:ECEFpoint) -> 'CRAMpoint':
        return cls(int(ECEF.ECEF_X*100), int(ECEF.ECEF_Y*100), int(ECEF.ECEF_Z*100))

    def toECEF(self) -> ECEFpoint:
        return ECEFpoint(self.ECEF_X/100, self.ECEF_Y/100, self.ECEF_Z/100)

    @classmethod
    def fromDroneStatus(cls, Status:rtDroneStatus):
        LLA = LLApoint(Status.Lat, Status.Lon, Status.Elev)
        return ECEFtofromLLA.LLAtoCRAM(LLA)


class ECEFtofromLLA:
    a:float  = 6378137.0              #WGS-84 semi-major axis
    e2:float = 6.6943799901377997e-3  #WGS-84 first eccentricity squared
    a1:float = 4.2697672707157535e+4  #a1 = a*e2
    a2:float = 1.8230912546075455e+9  #a2 = a1*a1
    a3:float = 1.4291722289812413e+2  #a3 = a1*e2/2
    a4:float = 4.5577281365188637e+9  #a4 = 2.5*a2
    a5:float = 4.2840589930055659e+4  #a5 = a1+a3
    a6:float = 9.9330562000986220e-1  #a6 = 1-e2
    zp:float
    w2:float
    w:float
    r2:float
    r:float
    s2:float
    c2:float
    s:float
    c:float
    ss:float

    g:float
    rg:float
    rf:float
    u:float
    v:float
    m:float
    f:float
    p:float
    x:float
    y:float
    z:float

    n:float
    lat:float
    lon:float
    alt:float

#Convert Earth-Centered-Earth-Fixed (ECEF) to lat, Lon, Altitude
#Input is a three element array containing x, y, z in meters
#Returned array contains lat and lon in degrees, and altitude in meters
    @staticmethod
    def ECEFtoLLA( ecef: ECEFpoint ) -> LLApoint :
        geo:List[float] = [0,0,0]   #Results go here (Lat, Lon, Altitude)
        ECEFtofromLLA.x = ecef.ECEF_X
        ECEFtofromLLA.y = ecef.ECEF_Y
        ECEFtofromLLA.z = ecef.ECEF_Z
        ECEFtofromLLA.zp = abs(ECEFtofromLLA.z)
        ECEFtofromLLA.w2 = ECEFtofromLLA.x * ECEFtofromLLA.x + ECEFtofromLLA.y * ECEFtofromLLA.y
        ECEFtofromLLA.w = math.sqrt(ECEFtofromLLA.w2)
        ECEFtofromLLA.r2 = ECEFtofromLLA.w2 + ECEFtofromLLA.z * ECEFtofromLLA.z
        ECEFtofromLLA.r = math.sqrt(ECEFtofromLLA.r2)
        geo[1] = math.atan2(ECEFtofromLLA.y, ECEFtofromLLA.x)       #Lon (final)
        ECEFtofromLLA.s2 = ECEFtofromLLA.z * ECEFtofromLLA.z / ECEFtofromLLA.r2
        ECEFtofromLLA.c2 = ECEFtofromLLA.w2 / ECEFtofromLLA.r2
        ECEFtofromLLA.u = ECEFtofromLLA.a2 / ECEFtofromLLA.r
        ECEFtofromLLA.v = ECEFtofromLLA.a3 - ECEFtofromLLA.a4 / ECEFtofromLLA.r
        if( ECEFtofromLLA.c2 > 0.3):
            ECEFtofromLLA.s = (ECEFtofromLLA.zp / ECEFtofromLLA.r) * (1.0 + ECEFtofromLLA.c2 * (ECEFtofromLLA.a1 + ECEFtofromLLA.u + ECEFtofromLLA.s2 * ECEFtofromLLA.v) / ECEFtofromLLA.r)
            geo[0] = math.asin(ECEFtofromLLA.s)      #Lat
            ECEFtofromLLA.ss = ECEFtofromLLA.s * ECEFtofromLLA.s
            ECEFtofromLLA.c = math.sqrt(1.0 - ECEFtofromLLA.ss)
        else:
            ECEFtofromLLA.c = (ECEFtofromLLA.w / ECEFtofromLLA.r) * (1.0 - ECEFtofromLLA.s2 * (ECEFtofromLLA.a5 - ECEFtofromLLA.u - ECEFtofromLLA.c2 * ECEFtofromLLA.v) / ECEFtofromLLA.r)
            geo[0] = math.acos(ECEFtofromLLA.c)      #Lat
            ECEFtofromLLA.ss = 1.0 - ECEFtofromLLA.c * ECEFtofromLLA.c
            ECEFtofromLLA.s = math.sqrt(ECEFtofromLLA.ss)

        ECEFtofromLLA.g = 1.0 - ECEFtofromLLA.e2 * ECEFtofromLLA.ss
        ECEFtofromLLA.rg = ECEFtofromLLA.a / math.sqrt(ECEFtofromLLA.g)
        ECEFtofromLLA.rf = ECEFtofromLLA.a6 * ECEFtofromLLA.rg
        ECEFtofromLLA.u = ECEFtofromLLA.w - ECEFtofromLLA.rg * ECEFtofromLLA.c
        ECEFtofromLLA.v = ECEFtofromLLA.zp - ECEFtofromLLA.rf * ECEFtofromLLA.s
        ECEFtofromLLA.f = ECEFtofromLLA.c * ECEFtofromLLA.u + ECEFtofromLLA.s * ECEFtofromLLA.v
        ECEFtofromLLA.m = ECEFtofromLLA.c * ECEFtofromLLA.v - ECEFtofromLLA.s * ECEFtofromLLA.u
        ECEFtofromLLA.p = ECEFtofromLLA.m / (ECEFtofromLLA.rf / ECEFtofromLLA.g + ECEFtofromLLA.f)
        geo[0] = geo[0] + ECEFtofromLLA.p      #Lat
        geo[2] = ECEFtofromLLA.f + ECEFtofromLLA.m * ECEFtofromLLA.p / 2.0     #Altitude
        if( ECEFtofromLLA.z < 0.0): geo[0] *= -1.0     #Lat

        return LLApoint( math.degrees( geo[0] ), math.degrees(geo[1]) , geo[2])

#Convert Lat, Lon, Altitude to Earth-Centered-Earth-Fixed (ECEF)
#Input is a three element array containing lat, lon (degrees) and alt (m)
#Returned array contains x, y, z in meters
    @staticmethod
    def LLAtoECEF( geo:LLApoint) -> ECEFpoint :
        ECEFtofromLLA.lat = math.radians(float(geo.Lat))
        ECEFtofromLLA.lon = math.radians(float(geo.Lon))
        ECEFtofromLLA.alt = float(geo.Elev)
        ECEFtofromLLA.n = ECEFtofromLLA.a / math.sqrt(1 - ECEFtofromLLA.e2 * math.sin(ECEFtofromLLA.lat) * math.sin(ECEFtofromLLA.lat))

        return ECEFpoint((ECEFtofromLLA.n + ECEFtofromLLA.alt) * math.cos(ECEFtofromLLA.lat) * math.cos(ECEFtofromLLA.lon),
                         (ECEFtofromLLA.n + ECEFtofromLLA.alt) * math.cos(ECEFtofromLLA.lat) * math.sin(ECEFtofromLLA.lon),
                         (ECEFtofromLLA.n * (1 - ECEFtofromLLA.e2) + ECEFtofromLLA.alt) * math.sin(ECEFtofromLLA.lat)
                         )

    @staticmethod
    def CRAMtoLLA(CRAM: CRAMpoint) -> LLApoint: return ECEFtofromLLA.ECEFtoLLA(CRAM.toECEF())

    @staticmethod
    def LLAtoCRAM(LLA: LLApoint) -> CRAMpoint: return CRAMpoint.fromECEF(ECEFtofromLLA.LLAtoECEF(LLA))

if __name__ == "__main__":
    myLLA = LLApoint(37.696373, -122.020752, 1) #PK FIELD
    print(myLLA.toJSON())
    myECEF = ECEFtofromLLA.LLAtoECEF(myLLA)
    print(myECEF.toJSON())
    myLLA = ECEFtofromLLA.ECEFtoLLA(myECEF)
    print(myLLA.toJSON())

