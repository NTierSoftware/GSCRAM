
from CRAMmsg.Element import Element


class TextElement(Element):

    def __init__(self, text: str):
        self.text = text

    def getNumBytes(self):
        return len(self.text)

    def getByteArray(self) -> bytearray:
        b = bytearray()
        b.extend(self.text.encode('ascii'))
        return b

    def getDataObject(self, enumGroup=None, useEnums=False):
        return self.text

    @classmethod
    def genFromBytes(cls, byteList):
        s = byteList.decode('ascii')
        return cls(s)

    def __eq__(self, other) -> bool:
        return self.text == other.text
