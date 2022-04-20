import json
from GSmsg.GSBaseMessage import GSBaseMessage

class tGoToWaypoint(GSBaseMessage):
    # MSG_TYPE = 'tGoToWaypoint'
    # MSG_TYPE = 924

    def __init__(self, wsInstallId: int, Lat: float, Lon: float, Elev: float):
        self.wsInstallId = wsInstallId
        self.Lat = Lat
        self.Lon = Lon
        self.Elev = Elev

    # def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__ ,
            'wsInstallId' : self.wsInstallId,
            'Lat' : self.Lat,
            'Lon' : self.Lon,
            'Elev' : self.Elev,
        }

    # def getDataObject(self) -> dict:
    #     gtw = {}
    #     gtw['msgType'] = self.MSG_TYPE
    #     gtw['ASdroneId'] = self.ASdroneId
    #     gtw['Lat'] = self.Lat
    #     gtw['Lon'] = self.Lon
    #     gtw['Elev'] = self.Elev
    #     return gtw

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        gtw = json.loads(jsonStr)
        return cls(gtw['wsInstallId'], gtw['Lat'], gtw['Lon'], gtw['Elev'])
        # return cls(gtw['ASdroneId'], gtw['Lat'], gtw['Lon'], gtw['Elev'])


    # def clone(self) -> 'tGoToWaypoint': return tGoToWaypoint(self.ASdroneId, self.Lat, self.Lon, self.Elev)
