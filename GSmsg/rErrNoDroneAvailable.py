from GSmsg.GSBaseMessage import GSBaseMessage
import json

class rErrNoDroneAvailable(GSBaseMessage):
    # MSG_TYPE = 'rErrNoDroneAvailable'
    # MSG_TYPE = 9999

    def __init__(self, errNo: int = None, addlInfo: str = None):
        super().__init__()
        self.errNo = errNo
        self.addlInfo = addlInfo

    # def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__ ,
            'errNo' : self.errNo,
            'addlInfo' : self.addlInfo,
        }


    # def getDataObject(self) -> dict:
    #     # super().getDataObject()
    #     # ds = {}
    #     # ds['msgType'] = self.MSG_TYPE
    #     self.ds['errNo'] = self.errNo
    #     self.ds['addlInfo'] = self.addlInfo
    #     return self.ds

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'rErrNoDroneAvailable':
        ds = json.loads(jsonStr)
        return cls(ds['errNo'], ds['addlInfo'])

    def clone(self) -> 'rErrNoDroneAvailable':
        return rErrNoDroneAvailable(self.errNo, self.addlInfo)
