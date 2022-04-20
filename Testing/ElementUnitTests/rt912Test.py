# rt912Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/14/2018

from CRAMmsg.rt912DoNotEngage import rt912DoNotEngage
from CRAMmsg.rt912DoNotEngage import rt912Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 44
MSG_ID = 912
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0x8712
PLAN_ID = 0x1231
SYS_TRACK_ID = 0x9A8B7C66
LOCAL_TRACK_ID = 0x4433
DNE_REASON = 0x06
DNE_ACTION = rt912Consts.DNE_Action.SELF_DESTRUCT.value.data
INTERCEPTOR_ID = 0x9E1A
COMMAND_RESPONSE = 0x02
ECEF_X = -1  # 0xFFFFFFFF
ECEF_Y = 17  # 0x00000011
ECEF_Z = -2  # 0xFFFFFFFE

FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x2C, 0x03, 0x90, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                   0x87, 0x12, 0x12, 0x31, 0x9A, 0x8B, 0x7C, 0x66, 0x44, 0x33, 0x06, 0x04,
                   0x9E, 0x1A, 0x02, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x11,
                   0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00])

def run912Test():
    test912JSONSimple()
    test912FromBytes()
    test912ToBytes()
    print("912 Do Not Engage: PASS")


def test912JSONSimple():
    msg = rt912DoNotEngage(WEAPON_ID, PLAN_ID, SYS_TRACK_ID, LOCAL_TRACK_ID, DNE_REASON, DNE_ACTION, INTERCEPTOR_ID,
                           COMMAND_RESPONSE, ECEF_X, ECEF_Y, ECEF_Z)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test912ToBytes():
    msg = rt912DoNotEngage(WEAPON_ID, PLAN_ID, SYS_TRACK_ID, LOCAL_TRACK_ID, DNE_REASON, DNE_ACTION, INTERCEPTOR_ID,
                           COMMAND_RESPONSE, ECEF_X, ECEF_Y, ECEF_Z)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): rt912 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: rt912 toBytes'

def test912FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: rt912 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: rt912 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: rt912 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: rt912 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: rt912 fromBytes'

    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: rt912 fromBytes'
    assert msg.planId.data == PLAN_ID, 'Plan ID wrong: rt912 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'System Track ID wrong: rt912 fromBytes'
    assert msg.localTrackId.data == LOCAL_TRACK_ID, 'Local Track ID wrong: rt912 fromBytes'
    assert msg.DNE_reason.data == DNE_REASON, 'DNE Reason wrong: rt912 fromBytes'
    assert msg.DNE_action.data == DNE_ACTION, 'DNE Action wrong: rt912 fromBytes'
    assert msg.interceptorId.data == INTERCEPTOR_ID, 'drone ID wrong: rt912 fromBytes'
    assert msg.commandResponse.data == COMMAND_RESPONSE, 'Command Response wrong: rt912 fromBytes'
    assert msg.ECEF_X.data == ECEF_X, 'ECEF X wrong: rt912 fromBytes'
    assert msg.ECEF_Y.data == ECEF_Y, 'ECEF Y wrong: rt912 fromBytes'
    assert msg.ECEF_Z.data == ECEF_Z, 'ECEF Z wrong: rt912 fromBytes'

