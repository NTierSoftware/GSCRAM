from GSmsg.GSBaseMessage import GSBaseMessage
import json

#Message from GSCRAM to Groundspace : Send this Drone home.
class tGoHome(GSBaseMessage):
    # MSG_TYPE = 'tGoHome'
    # MSG_TYPE = 8002

    def __init__(self, wsInstallId: int):
        self.wsInstallId = wsInstallId

    # def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__ ,
            'wsInstallId' : self.wsInstallId,
        }

    # def getDataObject(self) -> dict:
    #     wf = {}
    #     wf['msgType'] = self.MSG_TYPE
    #     wf['ASdroneId'] = self.ASdroneId
    #     return wf

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        wf = json.loads(jsonStr)
        return cls(wf['wsInstallId'])
        # return cls(wf['ASdroneId'])


# class rtDroneStatus(GSBaseMessage):
#     MSG_TYPE = 903
#
#     def __init__(self, ASdroneId: int=None, Lat: float=None, Lon: float=None, Elev: float=None):
#         self.ASdroneId:int = ASdroneId
#         self.Lat: float = Lat
#         self.Lon: float = Lon
#         self.Elev: float = Elev
#
#     def getMsgType(self): return self.MSG_TYPE
#
#     def getDataObject(self) -> dict:
#         ds = {}
#         ds['msgType'] = self.MSG_TYPE
#         ds['ASdroneId'] = self.ASdroneId
#         ds['Lat'] = self.Lat
#         ds['Lon'] = self.Lon
#         ds['Elev'] = self.Elev
#         return ds
#
#     @classmethod
#     def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
#         ds = json.loads(jsonStr)
#         return cls(ds['ASdroneId'], ds['Lat'], ds['Lon'], ds['Elev'])
#
#     def clone(self) -> 'rtDroneStatus':
#         return rtDroneStatus(self.ASdroneId, self.Lat, self.Lon, self.Elev)
