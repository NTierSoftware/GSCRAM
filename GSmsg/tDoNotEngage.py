import json
from GSmsg.GSBaseMessage import GSBaseMessage


class tDoNotEngage(GSBaseMessage):
    MSG_TYPE = 'tDoNotEngage'
    # MSG_TYPE = 912

    def __init__(self, wsInstallId: int, targetId: int):
        self.wsInstallId = wsInstallId
        self.targetId = targetId

    def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__,
            'wsInstallId': self.wsInstallId,
            'targetId' : self.targetId,
        }

    # def getDataObject(self) -> dict:
    #     dne = {}
    #     dne['msgType'] = self.MSG_TYPE
    #     dne['ASdroneId'] = self.ASdroneId
    #     dne['targetId'] = self.targetId
    #     return dne

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        dne = json.loads(jsonStr)
        return cls(dne['wsInstallId'], dne['targetId'])
        # return cls(dne['ASdroneId'], dne['targetId'])


    # def clone(self) -> 'tDoNotEngage': return tDoNotEngage(self.ASdroneId, self.targetId)
