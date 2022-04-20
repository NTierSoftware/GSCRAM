# author: Alex Erf, Airspace, alex.erf@airspace.co, created: 7/30/2018

import abc, json, threading
from datetime import datetime
# from Utilities import constants
from Log.CRAMLog import mainLog

class Element: #This class defines base functionality for any element of a CRAM Message.
    def __init__(self):#This is a base class, as such there is nothing to initialize.
        return
    
    @abc.abstractmethod
    def getNumBytes(self):
        """Subclasses must implement this method to return the total number of bytes in the element (message length)."""
        raise NotImplementedError('Element has not implemented getNumBytes()')
        return
    
    @classmethod
    @abc.abstractmethod
    def genFromBytes(cls, byteList):  # @NoSelf
        """Subclasses must implement this method to return an instance of the element constructed from the given byteList."""
        raise NotImplementedError('Element has not implemented genFromBytes()')
        return

    @abc.abstractmethod
    def getByteArray(self) -> bytearray:
        """Subclasses must implement this method to return a byte array representing the Element's data."""
        raise NotImplementedError('Element has not implemented getByteArray()')

    @abc.abstractmethod
    def getDataObject(self, enumGroup=None, useEnums=False):
        """Subclasses must implement this method to return an object representing the element's data (either list, value, or dictionary)."""
        raise NotImplementedError('Element has not implemented getDataObject()')
        return

    def toJSON(self, humanReadable = False) -> str:
        """Returns a string containing a JSON equivalent of the dictionary representing the element."""
        if humanReadable: return json.dumps(self.getDataObject(useEnums=True), separators=(',', ': '))
        return json.dumps(self.getDataObject())

    @classmethod
    @abc.abstractmethod
    def constructFromDictionary(cls, objDict: dict):
        raise NotImplementedError('Element has not implemented constructFromDictionary()')

    @classmethod
    def fromJSON(cls, jsonStr: str):
        json_dict = json.loads(jsonStr)
        return cls.constructFromDictionary(json_dict)

    def __log_thread(self):
        """Logs the CRAM element's information with decimal and hexadecimal versions of its byte array, as well as the JSON equivalent of the element."""
        mainLog.logDecMessage(self.getByteArray())
        mainLog.logHexMessage(self.getByteArray())
        mainLog.logJSONMessage(self)
        
    def log(self):
        """Calls the helper __log_thread function to log data asynchronously"""
        
        # for help on threading: https://pymotw.com/2/threading/
        thread = threading.Thread(target=self.__log_thread)
        thread.start()

    def clone(self):
        byteList = self.getByteArray()
        return self.genFromBytes(byteList)

    # def setRecvTime(self, recvTime:datetime = None):
    #     self.RecvTime = recvTime or datetime.utcnow()
    # def setSentTime(self, sentTime:datetime = None):
    #     self.SentTime = sentTime or datetime.utcnow()

    def __repr__(self): return self.toJSON(True)
