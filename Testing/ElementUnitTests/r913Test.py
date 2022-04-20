# r913Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/15/2018

from CRAMmsg.unusedCRAMmsg.r913ProtectedAssetCircle import r913ProtectedAssetCircle
from CRAMmsg.unusedCRAMmsg.r913ProtectedAssetCircle import r913Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 52
MSG_ID = 913
KIND = 0
PART_COUNT = 0

ASSET_ID = 0x9281
NO_FIRE_ZONE = 0x01
ASSET_PRIORITY = 0x08
# uint8 spare
DELETE_FLAG = r913Consts.DeleteFlag.DELETE_ASSET.value.data
# uint16 spare
# uint32 spare
# uint32 spare
# uint32 spare
ASSET_RADIUS = 0x0002F178
ASSET_HEIGHT = 0xE2771283
ASSET_ALT = -10  # 0xFFFFFFF6
ASSET_LAT = -400000  # 0xFFF9E580
ASSET_LONG = 50  # 0x00000032


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x34, 0x03, 0x91, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x92, 0x81, 0x01, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xF1, 0x78,
                   0xE2, 0x77, 0x12, 0x83, 0xFF, 0xFF, 0xFF, 0xF6, 0xFF, 0xF9, 0xE5, 0x80,
                   0x00, 0x00, 0x00, 0x32])


def run913Test():
    test913JSONSimple()
    test913FromBytes()
    test913ToBytes()
    print('913 Protected Asset Circle: PASS')


def test913JSONSimple():
    msg = r913ProtectedAssetCircle(ASSET_ID, NO_FIRE_ZONE, ASSET_PRIORITY, DELETE_FLAG, ASSET_RADIUS, ASSET_HEIGHT,
                                   ASSET_ALT, ASSET_LAT, ASSET_LONG)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: r913'


def test913ToBytes():
    msg = r913ProtectedAssetCircle(ASSET_ID, NO_FIRE_ZONE, ASSET_PRIORITY, DELETE_FLAG, ASSET_RADIUS, ASSET_HEIGHT,
                                   ASSET_ALT, ASSET_LAT, ASSET_LONG)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r913 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r913 toBytes'


def test913FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r913 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r913 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r913 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r913 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r913 fromBytes'

    assert msg.assetId.data == ASSET_ID, 'Asset ID wrong: t913 fromBytes'
    assert msg.noFireZone.data == NO_FIRE_ZONE, 'No Fire Zone wrong: t913 fromBytes'
    assert msg.assetPriority.data == ASSET_PRIORITY, 'Asset Priority wrong: t913 fromBytes'
    assert msg.deleteFlag.data == DELETE_FLAG, 'Delete Flag wrong: t913 fromBytes'
    assert msg.assetRadius.data == ASSET_RADIUS, 'Asset Radius wrong: t913 fromBytes'
    assert msg.assetHeight.data == ASSET_HEIGHT, 'Asset Height wrong: t913 fromBytes'
    assert msg.assetAlt.data == ASSET_ALT, 'Asset Altitude wrong: t913 fromBytes'
    assert msg.assetLat.data == ASSET_LAT, 'Asset Latitude wrong: t913 fromBytes'
    assert msg.assetLong.data == ASSET_LONG, 'Asset Longitude wrong: t913 fromBytes'

