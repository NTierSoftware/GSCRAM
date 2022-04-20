from GSmsg.GSBaseMessage import GSBaseMessage
import json

class rtDroneStatus(GSBaseMessage):

# {"msgType": "rtDroneStatus", "ASdroneId": "999", "wsInstallId": 1, "Lat": "37.696373", "Lon": "-122.020752","Elev": 125.075}
    def __init__(self, wsInstallId: int=None, ASdroneId: int=None, Lat: float=None, Lon: float=None, Elev: float=None):
        super().__init__()
        self.wsInstallId:int = wsInstallId
        self.ASdroneId:int = ASdroneId
        self.Lat: float = Lat
        self.Lon: float = Lon
        self.Elev: float = Elev

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__ ,
            'wsInstallId' : self.wsInstallId,
            'ASdroneId' : self.ASdroneId,
            'Lat' : self.Lat,
            'Lon' : self.Lon,
            'Elev' : self.Elev,
        }


    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        ds = json.loads(jsonStr)
        return cls(ds['wsInstallId'], ds['ASdroneId'], ds['Lat'], ds['Lon'], ds['Elev'])

    def clone(self) -> 'rtDroneStatus':
        return rtDroneStatus(self.wsInstallId, self.ASdroneId, self.Lat, self.Lon, self.Elev)


# https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes?noredirect=1&lq=1
    def __eq__(self, other):
        return (self.Lat == other.Lat) and (self.Lon == other.Lon) and (self.Elev == other.Elev)

