# r914Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/17/2018

from CRAMmsg.unusedCRAMmsg.r914ProtectedAssetPolygon import r914ProtectedAssetPolygon
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 76
MSG_ID = 914
KIND = 0
PART_COUNT = 4

ASSET_ID = 0x9281
NO_FIRE_ZONE = 0x01
ASSET_PRIORITY = 0x08
# uint8 spare
DELETE_FLAG = 0x01
# uint16 spare
# uint32 spare
# uint32 spare
# uint32 spare
# uint32 spare
ASSET_HEIGHT = 0xE2771283
ASSET_ALT = -10  # 0xFFFFFFF6
ASSET_LATS = [-200000, 100000, 50, -73981]  # [0xFFFCF2C0, 0x000186A0, 0x00000032, 0xFFFEDF03]
ASSET_LONGS = [80100000, -679000, -111111, -7321018]  # [0x04C63AA0, 0xFFF5A3A8, 0xFFFE4DF9, 0xFF904A46]


FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x4C, 0x03, 0x92, 0x00, 0x04, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x92, 0x81, 0x01, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0xE2, 0x77, 0x12, 0x83, 0xFF, 0xFF, 0xFF, 0xF6, 0xFF, 0xFC, 0xF2, 0xC0,
                   0x04, 0xC6, 0x3A, 0xA0, 0x00, 0x01, 0x86, 0xA0, 0xFF, 0xF5, 0xA3, 0xA8,
                   0x00, 0x00, 0x00, 0x32, 0xFF, 0xFE, 0x4D, 0xF9, 0xFF, 0xFE, 0xDF, 0x03,
                   0xFF, 0x90, 0x4A, 0x46])


def run914Test():
    test914JSONSimple()
    test914FromBytes()
    test914ToBytes()
    print('914 Protected Asset Polygon: PASS')


def test914JSONSimple():
    msg = r914ProtectedAssetPolygon(ASSET_ID, NO_FIRE_ZONE, ASSET_PRIORITY, DELETE_FLAG, ASSET_HEIGHT, ASSET_ALT,
                                    ASSET_LATS, ASSET_LONGS)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy, 'JSON failed: r914'


def test914ToBytes():
    msg = r914ProtectedAssetPolygon(ASSET_ID, NO_FIRE_ZONE, ASSET_PRIORITY, DELETE_FLAG, ASSET_HEIGHT, ASSET_ALT,
                                    ASSET_LATS, ASSET_LONGS)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): r914 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: r914 toBytes'


def test914FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: r914 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: r914 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: r914 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: r914 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: r914 fromBytes'

    assert msg.assetId.data == ASSET_ID, 'Asset ID wrong: r914 fromBytes'
    assert msg.noFireZone.data == NO_FIRE_ZONE, 'No Fire Zone wrong: r914 fromBytes'
    assert msg.assetPriority.data == ASSET_PRIORITY, 'Asset Priority wrong: r914 fromBytes'
    assert msg.deleteFlag.data == DELETE_FLAG, 'Delete Flag wrong: r914 fromBytes'
    assert msg.assetHeight.data == ASSET_HEIGHT, 'Asset Height wrong: r914 fromBytes'
    assert msg.assetAlt.data == ASSET_ALT, 'Asset Altitude wrong: r914 fromBytes'
    
    assert msg.assetLats[0].data == ASSET_LATS[0], 'Asset Latitude 0 wrong: r914 fromBytes'
    assert msg.assetLongs[0].data == ASSET_LONGS[0], 'Asset Longitude 0 wrong: r914 fromBytes'
    assert msg.assetLats[1].data == ASSET_LATS[1], 'Asset Latitude 1 wrong: r914 fromBytes'
    assert msg.assetLongs[1].data == ASSET_LONGS[1], 'Asset Longitude 1 wrong: r914 fromBytes'
    assert msg.assetLats[2].data == ASSET_LATS[2], 'Asset Latitude 2 wrong: r914 fromBytes'
    assert msg.assetLongs[2].data == ASSET_LONGS[2], 'Asset Longitude 2 wrong: r914 fromBytes'
    assert msg.assetLats[3].data == ASSET_LATS[3], 'Asset Latitude 3 wrong: r914 fromBytes'
    assert msg.assetLongs[3].data == ASSET_LONGS[3], 'Asset Longitude 3 wrong: r914 fromBytes'
