from CRAMmsg.CompoundElement import CompoundElement
from CRAMmsg.Header import Header
from datetime import datetime
from Utilities import constants


class CRAMBaseMessage(CompoundElement):
    def __init__(self, header: Header):
        self.header = header
        self.SentTime:datetime = constants.AprilFoolsDay2k
        self.RecvTime:datetime  = datetime.utcnow()

    def getMsgID(self) -> int: return self.header.messageId.data
