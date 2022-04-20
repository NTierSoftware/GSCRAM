# NumConversion.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 7/31/2018

# https://stackoverflow.com/a/12946226

import struct

# NOTE: the ToBytes functions can probably be changed to use struct.pack - look into that
# https://pymotw.com/2/struct/
# https://grokbase.com/t/python/python-ideas/0987evxa3t/bitwise-operations-on-bytes
# https://www.delftstack.com/howto/python/how-to-convert-bytes-to-integers/

def uint8ToBytes(num: int) -> bytearray:
    """Returns a bytearray consisting of a single unsigned 8-bit integer."""
    return bytearray([num])


def uint16ToBytes(num: int) -> bytearray:
    """Converts an unsigned 16-bit integer into a two-byte bytearray."""
    arr = bytearray(2)
    try:
        arr[0] = (num & 0xFF00) >> 8
        arr[1] = num & 0xFF
    except Exception as err:
        print("type(num):", type(num), "num:", num)
        raise err
    return arr

# def uint16ToBytes(num: int) -> bytearray:
#     """Converts an unsigned 16-bit integer into a two-byte bytearray."""
#     arr = bytearray(2)
#     arr[0] = (num & 0xFF00) >> 8
#     arr[1] = num & 0xFF
#     return arr

def uint24ToBytes(num: int) -> bytearray:
    arr = bytearray(3)
    arr[0] = (num & 0xFF0000) >> 16
    arr[1] = (num & 0xFF00) >> 8
    arr[2] = num & 0xFF
    return arr


def uint32ToBytes(num: int) -> bytearray:
    """Converts an unsigned 32-bit integer into a four-byte bytearray."""
    arr = bytearray(4)
    arr[0] = (num & 0xFF000000) >> 24
    arr[1] = (num & 0xFF0000) >> 16
    arr[2] = (num & 0xFF00) >> 8
    arr[3] = num & 0xFF
    return arr


def uint128ToBytes(num: int) -> bytearray:
    """Converts an unsigned 128-bit integer into a sixteen-byte bytearray."""
    arr = bytearray(16)
    mask = 0xFF000000000000000000000000000000
    shifts = 120
    for i in range(0, 16):
        arr[i] = (num & mask) >> shifts
        shifts -= 8
        mask >>= 8
    return arr


def uint8FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with one byte into a single unsigned 8-bit integer."""
    return intBytes[0]


def uint16FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with two bytes into a single unsigned 16-bit integer."""
    num = 0
    num |= (intBytes[0] << 8)
    num |= intBytes[1]
    return num


def uint24FromBytes(intBytes: bytearray) -> int:
    num = 0
    num |= (intBytes[0] << 16)
    num |= (intBytes[1] << 8)
    num |= intBytes[2]
    return num


def uint32FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with four bytes into a single unsigned 32-bit integer."""
    num = 0
    num |= (intBytes[0] << 24)
    num |= (intBytes[1] << 16)
    num |= (intBytes[2] << 8)
    num |= intBytes[3]
    return num


def uint128FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with sixteen bytes into a single unsigned 128-bit integer."""
    num = 0
    shifts = 120
    for i in range(0, 16):
        num |= (intBytes[i] << shifts)
        shifts -= 8
    return num


def int8ToBytes(num: int) -> bytearray:
    """Returns a bytearray consisting of a single signed 8-bit integer."""
    num = num & 0xFF  # forces num to be one byte
    return bytearray([num])


def int16ToBytes(num: int) -> bytearray:
    """Converts an unsigned 16-bit integer into a two-byte bytearray."""
    num = num & 0xFFFF # forces num to be two bytes
    arr = bytearray(2)
    arr[0] = (num & 0xFF00) >> 8
    arr[1] = num & 0xFF
    return arr


def int24ToBytes(num: int) -> bytearray:
    num = num & 0xFFFFFF  # forces num to be three bytes
    arr = bytearray(3)
    arr[0] = (num & 0xFF0000) >> 16
    arr[1] = (num & 0xFF00) >> 8
    arr[2] = num & 0xFF
    return arr


def int32ToBytes(num: int) -> bytearray:
    """Converts an unsigned 32-bit integer into a four-byte bytearray."""
    num = num & 0xFFFFFFFF # forces num to be four bytes
    arr = bytearray(4)
    arr[0] = (num & 0xFF000000) >> 24
    arr[1] = (num & 0xFF0000) >> 16
    arr[2] = (num & 0xFF00) >> 8
    arr[3] = num & 0xFF
    return arr


def int8FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with one byte into a single signed 8-bit integer."""
    return struct.unpack(">b", intBytes)[0]


def int16FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with two bytes into a single unsigned 16-bit integer."""
    return struct.unpack(">h", intBytes)[0]


def int24FromBytes(intBytes: bytearray) -> int:
    intBytes.insert(0, 0x00)
    unsigned = struct.unpack(">I", intBytes)[0]
    return unsigned if not (unsigned & 0x800000) else unsigned - 0x1000000  # https://stackoverflow.com/a/3783732


def int32FromBytes(intBytes: bytearray) -> int:
    """Converts a bytearray with four bytes into a single unsigned 32-bit integer"""
    return struct.unpack(">i", intBytes)[0]


def float32ToBytes(num: float) -> bytearray:
    return bytearray(struct.pack(">f", num))


def float32FromBytes(floatBytes: bytearray) -> float:
    return struct.unpack(">f", floatBytes)[0]

