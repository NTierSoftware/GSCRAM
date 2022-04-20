# rt900Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/3/2018

from CRAMmsg.rt900WeaponCmd import rt900WeaponCmd
from CRAMmsg.rt900WeaponCmd import rt900Consts
from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH = 60
MSG_ID = 900
KIND = 0
PART_COUNT = 0

WEAPON_ID = 0x1A2B
COMMAND_CODE = rt900Consts.CommandCode.ENABLE_TRANSMISSION_WEAPON_NO_FIRE.value
FIRE_CONTROL_MODE = rt900Consts.FireControlMode.ALLOCATE_MODE.value
PLAN_ID = 0x1234
CONTROL_CODE = rt900Consts.ControlCode.REGISTRATION.value
SYS_TRACK_ID = 0x12345678
COMMAND_RESPONSE = rt900Consts.CommandResponse.CANNOT_COMPLY.value
FIRING_UNIT_ID = rt900Consts.FiringUnitID.ALL_APPLICABLE_FIRING_UNITS.value
FAKE_TIME = 0xCCCCCCCC

BYTES = bytearray([0x00, 0x00, 0x00, 0x3C, 0x03, 0x84, 0x00, 0x00, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x1A, 0x2B, 0x0A, 0x02, 0x12, 0x34, 0x00, 0x04, 0x12, 0x34, 0x56, 0x78,
                     0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


def run900Test():
    test900JSONSimple()
    test900FromBytes()
    test900ToBytes()
    test900Reverse()
    print("900 Weapon Command: PASS")

def test900JSONSimple():
    msg = rt900WeaponCmd(WEAPON_ID, COMMAND_CODE, FIRE_CONTROL_MODE, PLAN_ID, CONTROL_CODE, SYS_TRACK_ID, COMMAND_RESPONSE, FIRING_UNIT_ID)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test900ToBytes():
    msg = rt900WeaponCmd(WEAPON_ID, COMMAND_CODE, FIRE_CONTROL_MODE, PLAN_ID, CONTROL_CODE, SYS_TRACK_ID, COMMAND_RESPONSE, FIRING_UNIT_ID)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): rt900 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES, 'Byte array failed: rt900 toBytes'
    
def test900FromBytes():
    msg = getMessageFromBytes(BYTES)
    assert msg.header.messageLength.data == MSG_LENGTH, 'Message Length wrong: rt900 fromBytes'
    assert msg.header.messageId.data == MSG_ID, 'Message ID wrong: rt900 fromBytes'
    assert msg.header.interfaceKind.data == KIND, 'Interface Kind wrong: rt900 fromBytes'
    assert msg.header.partCount.data == PART_COUNT, 'Part Count wrong: rt900 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: rt900 fromBytes'
    
    assert msg.weaponId.data == WEAPON_ID, 'Weapon ID wrong: rt900 fromBytes'
    assert msg.commandCode.data == COMMAND_CODE.data, 'Command Code wrong: rt900 fromBytes'
    assert msg.fireControlMode.data == FIRE_CONTROL_MODE.data, 'Fire Control Mode wrong: rt900 fromBytes'
    assert msg.planId.data == PLAN_ID, 'Plan ID wrong: rt900 fromBytes'
    assert msg.controlCode.data == CONTROL_CODE.data, 'Control Code wrong: rt900 fromBytes'
    assert msg.sysTrackId.data == SYS_TRACK_ID, 'System Track ID wrong: rt900 fromBytes'
    assert msg.commandResponse.data == COMMAND_RESPONSE.data, 'Command Response wrong: rt900 fromBytes'
    assert msg.firingUnitId.data == FIRING_UNIT_ID.data, 'Firing Unit ID wrong: rt900 fromBytes'
    return

def test900Reverse():
    msg = rt900WeaponCmd(WEAPON_ID, COMMAND_CODE, FIRE_CONTROL_MODE, PLAN_ID, CONTROL_CODE, SYS_TRACK_ID, COMMAND_RESPONSE, FIRING_UNIT_ID)
    byteList = msg.getByteArray()
    msg2 = getMessageFromBytes(byteList)
    assert msg.header.messageLength.data == msg2.header.messageLength.data, 'Invalid inverse: rt900'
    assert msg.header.messageId.data == msg2.header.messageId.data, 'Invalid inverse: rt900'
    assert msg.header.interfaceKind.data == msg2.header.interfaceKind.data, 'Invalid inverse: rt900'
    assert msg.header.partCount.data == msg2.header.partCount.data, 'Invalid inverse: rt900'
    assert msg.header.transmitTime.data == msg2.header.transmitTime.data, 'Invalid inverse: rt900'
    assert msg.weaponId.data == msg2.weaponId.data, 'Invalid inverse: rt900'
    assert msg.commandCode.data == msg2.commandCode.data, 'Invalid inverse:rt900'
    assert msg.fireControlMode.data == msg2.fireControlMode.data, 'Invalid inverse:rt900'
    assert msg.planId.data == msg2.planId.data, 'Invalid inverse:rt900'
    assert msg.controlCode.data == msg2.controlCode.data, 'Invalid inverse:rt900'
    assert msg.sysTrackId.data == msg2.sysTrackId.data, 'Invalid inverse:rt900'
    assert msg.commandResponse.data == msg2.commandResponse.data, 'Invalid inverse:rt900'
    assert msg.firingUnitId.data == msg2.firingUnitId.data, 'Invalid inverse:rt900'

