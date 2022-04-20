from GSmsg.GSBaseMessage import GSBaseMessage
# from datetime import datetime
import json

#Message from Groundspace to GSCRAM: Airspace has captured this target.
class rInterdiction(GSBaseMessage):
    # MSG_TYPE = 'rInterdiction'
    # MSG_TYPE = 8001

    def __init__(self, wsInstallId: int, Lat: float, Lon: float, Elev: float):
        super().__init__()
        self.wsInstallId = wsInstallId
        # self.targetId = targetId
        self.Lat = Lat
        self.Lon = Lon
        self.Elev = Elev
        # self.Interdiction = Interdiction

    # def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__ ,
            'wsInstallId' : self.wsInstallId,
            'Lat' : self.Lat,
            'Lon' : self.Lon,
            'Elev' : self.Elev,
        }


        # # super().getDataObject(self)
        # # wf = {}
        # # wf['msgType'] = self.MSG_TYPE
        # self.ds['ASdroneId'] = self.ASdroneId
        # # wf['targetId'] = self.targetId
        # self.ds['Lat'] = self.Lat
        # self.ds['Lon'] = self.Lon
        # self.ds['Elev'] = self.Elev
        # # wf['Interdiction'] = self.Interdiction.isoformat()
        # return self.ds

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        wf = json.loads(jsonStr)
        # dateString = wf['Interdiction']
        # ValueError: Invalid isoformat string: '2019-02-05T14:19:35.000Z'
        return cls(wf['wsInstallId'], wf['Lat'], wf['Lon'], wf['Elev'])
        # return cls(wf['ASdroneId'], wf['Lat'], wf['Lon'], wf['Elev'])


    # def clone(self) -> 'rInterdiction': return rInterdiction(self.ASdroneId, self.targetId, self.Lat, self.Lon, self.Elev, self.Interdiction)
