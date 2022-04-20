
import abc
from CRAMmsg.Element import Element

class ComparableElement(Element):

    @abc.abstractmethod
    def val(self):
        raise NotImplementedError('ComparableElement has not implemented val()')

    def __lt__(self, other):
        if not isinstance(other, ComparableElement):
            return self.val() < other
        return self.val() < other.val()

    def __le__(self, other):
        if not isinstance(other, ComparableElement):
            return self.val() <= other
        return self.val() <= other.val()

    def __gt__(self, other):
        if not isinstance(other, ComparableElement):
            return self.val() > other
        return self.val() > other.val()

    def __ge__(self, other):
        if not isinstance(other, ComparableElement):
            return self.val() >= other
        return self.val() >= other.val()

    def __eq__(self, other):
        if not isinstance(other, ComparableElement):
            return self.val() == other
        return self.val() == other.val()
