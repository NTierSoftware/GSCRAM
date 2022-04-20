from CRAMmsg.Element import Element
from CRAMmsg.ElementFloat32 import ElementFloat32

from Utilities.Wrap import wrap

from typing import List

class PMatrix:
    LENGTH = 84

    FIELD_NAMES = ['PxPx-Covariance', 'PxPy-Covariance', 'PxPz-Covariance', 'PxVx-Covariance', 'PxVy-Covariance',
                   'PxVz-Covariance', 'PyPy-Covariance', 'PyPz-Covariance', 'PyVx-Covariance', 'PyVy-Covariance',
                   'PyVz-Covariance', 'PzPz-Covariance', 'PzVx-Covariance', 'PzVy-Covariance', 'PzVz-Covariance',
                   'VxVx-Covariance', 'VxVy-Covariance', 'VxVz-Covariance', 'VyVy-Covariance', 'VyVz-Covariance',
                   'VzVz-Covariance']

    def __init__(self, PxPx, PxPy, PxPz,PxVx, PxVy, PxVz, PyPy, PyPz, PyVx, PyVy, PyVz, PzPz, PzVx, PzVy, PzVz,
                 VxVx, VxVy, VxVz, VyVy, VyVz, VzVz):
        self.PxPx = wrap(PxPx, ElementFloat32)
        self.PxPy = wrap(PxPy, ElementFloat32)
        self.PxPz = wrap(PxPz, ElementFloat32)
        self.PxVx = wrap(PxVx, ElementFloat32)
        self.PxVy = wrap(PxVy, ElementFloat32)
        self.PxVz = wrap(PxVz, ElementFloat32)
        self.PyPy = wrap(PyPy, ElementFloat32)
        self.PyPz = wrap(PyPz, ElementFloat32)
        self.PyVx = wrap(PyVx, ElementFloat32)
        self.PyVy = wrap(PyVy, ElementFloat32)
        self.PyVz = wrap(PyVz, ElementFloat32)
        self.PzPz = wrap(PzPz, ElementFloat32)
        self.PzVx = wrap(PzVx, ElementFloat32)
        self.PzVy = wrap(PzVy, ElementFloat32)
        self.PzVz = wrap(PzVz, ElementFloat32)
        self.VxVx = wrap(VxVx, ElementFloat32)
        self.VxVy = wrap(VxVy, ElementFloat32)
        self.VxVz = wrap(VxVz, ElementFloat32)
        self.VyVy = wrap(VyVy, ElementFloat32)
        self.VyVz = wrap(VyVz, ElementFloat32)
        self.VzVz = wrap(VzVz, ElementFloat32)

    def getByteLength(self) -> int:
        return self.LENGTH

    def allFields(self) -> List[Element]:
        return [self.PxPx, self.PxPy, self.PxPz, self.PxVx, self.PxVy, self.PxVz, self.PyPy, self.PyPz, self.PyVx,
                self.PyVy, self.PyVz, self.PzPz, self.PzVx, self.PzVy, self.PzVz, self.VxVx, self.VxVy, self.VxVz,
                self.VyVy, self.VyVz, self.VzVz]

    def allFieldNames(self) -> List[str]:
        return self.FIELD_NAMES


    @classmethod
    def genFromBytes(cls, byteList):
        pArr = []
        for i in range(0, 21):
            pArr.append(ElementFloat32.genFromBytes(byteList[4 * i : 4 + 4 * i]))
        return cls(pArr[0], pArr[1], pArr[2], pArr[3], pArr[4], pArr[5], pArr[6], pArr[7], pArr[8],
                   pArr[9], pArr[10], pArr[11], pArr[12], pArr[13], pArr[14], pArr[15], pArr[16],
                   pArr[17], pArr[18], pArr[19], pArr[20])

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        fields = []
        for fn in cls.FIELD_NAMES:
            fields.append(objDict[fn])
        return cls(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8],
                   fields[9], fields[10], fields[11], fields[12], fields[13], fields[14], fields[15], fields[16],
                   fields[17], fields[18], fields[19], fields[20])


class RMatrix:
    LENGTH = 84

    FIELD_NAMES = ['PxPx-RMatrix', 'PxPy-RMatrix', 'PxPz-RMatrix', 'PxVx-RMatrix', 'PxVy-RMatrix',
                   'PxVz-RMatrix', 'PyPy-RMatrix', 'PyPz-RMatrix', 'PyVx-RMatrix', 'PyVy-RMatrix',
                   'PyVz-RMatrix', 'PzPz-RMatrix', 'PzVx-RMatrix', 'PzVy-RMatrix', 'PzVz-RMatrix',
                   'VxVx-RMatrix', 'VxVy-RMatrix', 'VxVz-RMatrix', 'VyVy-RMatrix', 'VyVz-RMatrix',
                   'VzVz-RMatrix']

    def __init__(self, PxPx, PxPy, PxPz,PxVx, PxVy, PxVz, PyPy, PyPz, PyVx, PyVy, PyVz, PzPz, PzVx, PzVy, PzVz,
                 VxVx, VxVy, VxVz, VyVy, VyVz, VzVz):
        self.PxPx = wrap(PxPx, ElementFloat32)
        self.PxPy = wrap(PxPy, ElementFloat32)
        self.PxPz = wrap(PxPz, ElementFloat32)
        self.PxVx = wrap(PxVx, ElementFloat32)
        self.PxVy = wrap(PxVy, ElementFloat32)
        self.PxVz = wrap(PxVz, ElementFloat32)
        self.PyPy = wrap(PyPy, ElementFloat32)
        self.PyPz = wrap(PyPz, ElementFloat32)
        self.PyVx = wrap(PyVx, ElementFloat32)
        self.PyVy = wrap(PyVy, ElementFloat32)
        self.PyVz = wrap(PyVz, ElementFloat32)
        self.PzPz = wrap(PzPz, ElementFloat32)
        self.PzVx = wrap(PzVx, ElementFloat32)
        self.PzVy = wrap(PzVy, ElementFloat32)
        self.PzVz = wrap(PzVz, ElementFloat32)
        self.VxVx = wrap(VxVx, ElementFloat32)
        self.VxVy = wrap(VxVy, ElementFloat32)
        self.VxVz = wrap(VxVz, ElementFloat32)
        self.VyVy = wrap(VyVy, ElementFloat32)
        self.VyVz = wrap(VyVz, ElementFloat32)
        self.VzVz = wrap(VzVz, ElementFloat32)

    def getByteLength(self) -> int:
        return self.LENGTH

    def allFields(self) -> List[Element]:
        return [self.PxPx, self.PxPy, self.PxPz, self.PxVx, self.PxVy, self.PxVz, self.PyPy, self.PyPz, self.PyVx,
                self.PyVy, self.PyVz, self.PzPz, self.PzVx, self.PzVy, self.PzVz, self.VxVx, self.VxVy, self.VxVz,
                self.VyVy, self.VyVz, self.VzVz]

    def allFieldNames(self) -> List[str]:
        return self.FIELD_NAMES

    @classmethod
    def genFromBytes(cls, byteList):
        rArr = []
        for i in range(0, 21):
            rArr.append(ElementFloat32.genFromBytes(byteList[4 * i : 4 + 4 * i]))
        return cls(rArr[0], rArr[1], rArr[2], rArr[3], rArr[4], rArr[5], rArr[6], rArr[7], rArr[8],
                   rArr[9], rArr[10], rArr[11], rArr[12], rArr[13], rArr[14], rArr[15], rArr[16],
                   rArr[17], rArr[18], rArr[19], rArr[20])

    @classmethod
    def constructFromDictionary(cls, objDict: dict):
        fields = []
        for fn in cls.FIELD_NAMES:
            fields.append(objDict[fn])
        return cls(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8],
                   fields[9], fields[10], fields[11], fields[12], fields[13], fields[14], fields[15], fields[16],
                   fields[17], fields[18], fields[19], fields[20])

