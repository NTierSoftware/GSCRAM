import abc, threading, json
from Utilities import constants

from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from Log.CRAMLog import mainLog
from datetime import datetime

# from typing import Any

class GSBaseMessage(CRAMBaseMessage):
    def __init__(self):
        self.SentTime:datetime = constants.AprilFoolsDay2k
        self.RecvTime = datetime.utcnow()


    @abc.abstractmethod
    def toJSON(self, humanReadable: bool=False) -> str:
        data = self.getDataObject()
        return '\n' + json.dumps(data, indent=4, separators=(',', ': ')) + ', sent:' + str(self.SentTime) + ', recd:' + str(self.RecvTime) + '\n' if humanReadable else json.dumps(data)


    @classmethod
    @abc.abstractmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        raise NotImplementedError('GSBaseMessage has not implemented fromJSON()')


    # def getDataObject(self, enumGroup=None, useEnums=False) -> dict:
    def getDataObject(self) -> dict:
        raise NotImplementedError('GSBaseMessage has not implemented getDataObject()')

    @abc.abstractmethod
    def clone(self) -> 'GSBaseMessage':
        raise NotImplementedError('GSBaseMessage has not implemented clone()')

    def __log_thread(self):
        mainLog.logString(self.toJSON())

    def log(self): # for help on threading: https://pymotw.com/2/threading/
        thread = threading.Thread(target=self.__log_thread)
        thread.start()

