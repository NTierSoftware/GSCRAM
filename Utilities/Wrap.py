
from enum import Enum


def wrap(value, cls):
    if isinstance(value, Enum): return value.value
    elif isinstance(value, cls): return value

    return cls(value)
