# DataElement.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/20/2018

from CRAMmsg.ComparableElement import ComparableElement
from Utilities.ValueNameConversion import valueToName


class DataElement(ComparableElement):

    def __init__(self, data_in):
        self.data = data_in

    def getDataObject(self, enumGroup=None, useEnums=False):
        if enumGroup is not None:
            return valueToName(self, enumGroup)
        else:
            return self.data

    def val(self):
        return self.data

    def __str__(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.data)
