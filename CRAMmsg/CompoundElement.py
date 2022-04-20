import abc
from CRAMmsg.Element import Element
from typing import List

class CompoundElement(Element):
    @abc.abstractmethod
    def getAllFields(self) -> List[Element]:
        """"Subclasses must implement this method to return all of their fields in the proper order (according to documentation)"""
        raise NotImplementedError('SendableMessage has not implemented getAllFields()')

    @abc.abstractmethod
    def getAllFieldNames(self) -> List[str]:
        """"Subclasses must implement this method to return all of their fields' names in the proper order (according to documentation)"""
        raise NotImplementedError('SendableMessage has not implemented getAllFieldNames()')

    @abc.abstractmethod
    def getAllEnumGroups(self) -> List:
        raise NotImplementedError('CompoundElement has not implemented getAllEnumGroups()')

    def getByteArray(self) -> bytearray: #Returns a byte array containing all of the data elements in byte form.
        fields = self.getAllFields()
        arr = bytearray()
        for f in fields: arr.extend(f.getByteArray())
        return arr

    def getDataObject(self, enumGroup=None, useEnums=False) -> dict:
        """Returns a dictionary mapping strings for the names of the various data fields to the respective values.
        :param useEnums:
        """
        fieldNames = self.getAllFieldNames()  # keys
        fields = self.getAllFields()  # values
        types = self.getAllEnumGroups()
        data = {}
        for x in range(0, len(fields)):
            # print("debug getDataObject: ", x)
            data[fieldNames[x]] = fields[x].getDataObject(types[x] if useEnums else None, useEnums = useEnums )
        return data


    def __eq__(self, other) -> bool:
        myFields = self.getAllFields()
        otherFields = other.getAllFields()
        for i in range(0, len(myFields)):
            if not myFields[i] == otherFields[i]: return False
        return True
