# author: John.JD.Donaldson@airspace.co, created: 8/6/2018
from enum import Enum

from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.ElementUInt16 import ElementUInt16
from CRAMmsg.ElementUInt32 import ElementUInt32
from CRAMmsg.ElementUInt8 import ElementUInt8
from CRAMmsg.Header import Header, HeaderConsts
from Utilities import constants
from Utilities.console import debugLog
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.ValueNameConversion import objectToValue
from Utilities.Wrap import wrap

class rt702Spoof(CRAMBaseMessage):
    MSG_LEN = 40
    MSG_ID = 702
    PART_COUNT = 0

    def __init__(self, msgType, weaponId, requestTime, receiptTime, responseTime, header=None):
        self.transmitTime = ElementUInt32(millisSinceMidnight())

        super().__init__(header or Header(self.MSG_LEN, self.MSG_ID, HeaderConsts.DEFAULT_INTERFACE.value, self.PART_COUNT, self.transmitTime))

        self.msgType = wrap(msgType, ElementUInt8)
        self.spare1 = ElementUInt8(0)
        self.weaponId = wrap(weaponId, ElementUInt16)

        self.requestTime = wrap(requestTime, ElementUInt32)
        self.receiptTime = wrap(receiptTime, ElementUInt32)
        self.responseTime = wrap(responseTime, ElementUInt32)

        self.spare2 = self.spare3 = self.spare4 = ElementUInt32(0)

    """Returns a list of all of the Command'GSsocket data fields in order."""

    def getAllFields(self): return [self.header, self.msgType, self.spare1, self.weaponId,
                                    self.requestTime, self.receiptTime, self.responseTime,
                                    self.spare2, self.spare3, self.spare4]


    def getAllFieldNames(self): return ['messageHeader', 'msgType', 'spare1', 'weaponId',
                                        'requestTime', 'receiptTime', 'responseTime',
                                        'spare2', 'spare3', 'spare4']

    def getAllEnumGroups(self):
        return [None, rt915Consts.msgType, None, None, None, None, None, None, None, None]

    def getNumBytes(self): return self.MSG_LEN

    @classmethod
    def genFromBytes(cls, byteList):
        header = Header.genFromBytes(byteList[0:12])
        msgType = ElementUInt8.genFromBytes(byteList[12:13])  # should equal rt915Consts.msgType.REQUEST !?!?!
        # spare1
        weaponId = ElementUInt16.genFromBytes(byteList[14:16])

        requestTime = ElementUInt32.genFromBytes(byteList[16:20])
        receiptTime = ElementUInt32.genFromBytes(byteList[20:24])
        responseTime = ElementUInt32.genFromBytes(byteList[24:28])

        # spare2, spare3, spare4
        return cls(msgType, weaponId, requestTime, receiptTime, responseTime, header)


    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        header = Header.constructFromDictionary(objDict['messageHeader'])

        msgType = objectToValue(objDict['msgType'], rt915Consts.msgType)

        return cls(msgType, objDict['weaponId'], objDict['requestTime'], objDict['receiptTime'],
                   objDict['responseTime'], header)


    numNetTimes = 0
    def sendResponse(self, CRAM, receiptTime) -> 'rt702Spoof':

        responseMsg = rt702Spoof(rt915Consts.msgType.RESPONSE.value, self.weaponId, self.requestTime, receiptTime,
                                 responseTime=millisSinceMidnight())

        CRAM.sendCRAMmsg(responseMsg)
        rt702Spoof.numNetTimes += 1

        debugLog.log(constants.NettimeResponseSentToCRAM + str(rt702Spoof.numNetTimes))
        return responseMsg


class Sendrt915Error(Exception):
    def __init__(self, operation: str, message: str):
        self.operation = operation
        self.message = message
        return


class rt915Consts:
    class msgType(Enum):
        REQUEST = ElementUInt8(0)  # The 915 message is sent in request form (Message Type = 0) from the C2S to the WES
        RESPONSE = ElementUInt8(1)  # ...or in response form (Message Type = 1) from the WES to the C2S
