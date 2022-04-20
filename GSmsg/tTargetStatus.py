import json
from GSmsg.GSBaseMessage import GSBaseMessage

class tTargetStatus(GSBaseMessage):
    MSG_TYPE = 'tTargetStatus'
    # MSG_TYPE = 920

    def __init__(self, wsInstallId: int, targetId: int,
                 Lat: float, Lon: float, Elev: float,
                 ECEF_Vx: int, ECEF_Vy: int ,ECEF_Vz: int):
        self.wsInstallId:int = wsInstallId
        self.targetId:int = targetId
        self.Lat: float = Lat
        self.Lon: float = Lon
        self.Elev: float = Elev
        self.ECEF_Vx:int = round(ECEF_Vx/100)
        self.ECEF_Vy:int = round(ECEF_Vy/100)
        self.ECEF_Vz:int = round(ECEF_Vz/100)


    # def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__,
            'wsInstallId' : self.wsInstallId,
            'targetId' : self.targetId,
            'Lat' : self.Lat,
            'Lon' : self.Lon,
            'Elev' : self.Elev,
            'ECEF_Vx' : self.ECEF_Vx,
            'ECEF_Vy' : self.ECEF_Vy,
            'ECEF_Vz' : self.ECEF_Vz,
        }


    # def getDataObject(self) -> dict:
    #     ts = {}
    #     ts['msgType'] = self.MSG_TYPE
    #     ts['ASdroneId'] = self.ASdroneId
    #     ts['targetId'] = self.targetId
    #     ts['Lat'] = self.Lat
    #     ts['Lon'] = self.Lon
    #     ts['Elev'] = self.Elev
    #     ts['ECEF_Vx'] = self.ECEF_Vx
    #     ts['ECEF_Vy'] = self.ECEF_Vy
    #     ts['ECEF_Vz'] = self.ECEF_Vz
    #     return ts

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        ts = json.loads(jsonStr)
        return cls(ts['wsInstallId'], ts['targetId'], ts['Lat'], ts['Lon'], ts['Elev'], ts['ECEF_Vx'], ts['ECEF_Vy'], ts['ECEF_Vz'])
        # return cls(ts['ASdroneId'], ts['targetId'], ts['Lat'], ts['Lon'], ts['Elev'], ts['ECEF_Vx'], ts['ECEF_Vy'], ts['ECEF_Vz'])

    def clone(self) -> 'tTargetStatus':
        return tTargetStatus(self.wsInstallId, self.targetId, self.Lat, self.Lon, self.Elev,
                             self.ECEF_Vx, self.ECEF_Vy, self.ECEF_Vz)

    def __repr__(self):
        return "target sent to GS:\t" + self.SentTime.isoformat() + "\thae:" + str(self.Elev) + "\tLat:" + str(self.Lat) + "\tLon:" + str(self.Lon) \
               + "\tid:" + str(self.targetId) \
               + "\tECEF_Vx:" + str(self.ECEF_Vx) + "\tECEF_Vy:" + str(self.ECEF_Vy) + "\tECEF_Vz:" + str(self.ECEF_Vz)

