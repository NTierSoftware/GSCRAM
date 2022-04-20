# t903Test.py
#
# author: Alex Erf, Airspace, alex.erf@airspace.co
# date created: 8/7/2018

from CRAMmsg.t903WeaponStatus import t903WeaponStatus
from CRAMmsg.t903WeaponStatus import t903_AI3
from CRAMmsg.t903WeaponStatus import t903_MML
from CRAMmsg.t903WeaponStatus import t903Consts

from CRAMmsg.ElementUInt32 import ElementUInt32

from Utilities.TimeUtils import millisSinceMidnight
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.JSONToMessage import getMessageFromJSON

MSG_LENGTH_A = 124
MSG_ID_A = 903
KIND_A = 0 # AI3
PART_COUNT_A = 2

WEAPON_ID_A = 0x1023
SYS_STATUS_A = 0x03
COMM_STATUS_A = 0x01
VEHICLE_DOOR_STATUS_A = t903Consts.VehicleDoorStatus.CLOSED.value  # 0x01
SEARCH_SENSOR_STATUS_A = 0x04
FC_TRACK_SENSOR_STATUS_A = 0x02
VIS_ID_SENSOR_STATUS_A = 0x01
SENSOR_NUM_FACES_A = 0x03
HOLD_FIRE_A = 0x00
SYS_MODE_A = 0x0008
WEAPON_KIND_A = 0x000A
SENSOR_ECEF_X_A = -100000 # 0xFFFE7960
SENSOR_ECEF_Y_A = 1234567 # 0x0012D687
SENSOR_ECEF_Z_A = -267378438 # 0xF01020FA
SENSOR_AZIMUTH_A = 0xA732BB01
MAX_DEF_RANGE_A = 0x000000E3
FIRE_CONTROL_MODES_A = [0x07, 0x03]
FIRING_UNIT_STATUSES_A = [0x06, 0x01]
FIRING_UNIT_IDS_A = [0x0001, 0x0002]
FIRING_UNIT_INVS_A = [0x0123, 0xA28F]
FIRING_UNIT_ROUND_STDBYS_A = [0xABBB, 0x6431]
FIRING_UNIT_ELEVS_A = [-10, 10] # [ 0xFFF6, 0x000A ]
FIRING_UNIT_AZIMUTHS_A = [0x00A0, 0x00B1]
FIRING_UNIT_ECEF_XS_A = [-78101, 98391] # [ 0xFFFECEEB, 0x00018057 ]
FIRING_UNIT_ECEF_YS_A = [394726076, -218893067] # [ 0x17870ABC, 0xF2F3F4F5 ]
FIRING_UNIT_ECEF_ZS_A = [1, 2004291857] # [0x00000001, 0x77771111]
FIRING_UNIT_START_BOUNDS_A = [-207, -32608] # [0xFF31, 0x80A0]
FIRING_UNIT_END_BOUNDS_A = [18, 28609] # [0x0012, 0x6FC1]
AMMO_KINDS_A = [0x03, 0x06]
PLATFORM_AZIMUTHS_A = [0x016A, 0x72BD]

BYTES_A = bytearray([0x00, 0x00, 0x00, 0x7C, 0x03, 0x87, 0x00, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                     0x10, 0x23, 0x03, 0x01, 0x01, 0x04, 0x02, 0x01, 0x03, 0x00, 0x00, 0x00,
                     0x00, 0x08, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFe, 0x79, 0x60,
                     0x00, 0x12, 0xD6, 0x87, 0xF0, 0x10, 0x20, 0xFA, 0xA7, 0x32, 0xBB, 0x01,
                     0x00, 0x00, 0x00, 0xE3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x07, 0x06, 0x00, 0x01, 0x01, 0x23, 0xAB, 0xBB, 0xFF, 0xF6, 0x00, 0xA0,
                     0xFF, 0xFE, 0xCE, 0xEB, 0x17, 0x87, 0x0A, 0xBC, 0x00, 0x00, 0x00, 0x01,
                     0xFF, 0x31, 0x00, 0x12, 0x00, 0x03, 0x01, 0x6A, 0x03, 0x01, 0x00, 0x02,
                     0xA2, 0x8F, 0x64, 0x31, 0x00, 0x0A, 0x00, 0xB1, 0x00, 0x01, 0x80, 0x57,
                     0xF2, 0xF3, 0xF4, 0xF5, 0x77, 0x77, 0x11, 0x11, 0x80, 0xA0, 0x6F, 0xC1,
                     0x00, 0x06, 0x72, 0xBD])

MSG_LENGTH_B = 84
MSG_ID_B = 903
KIND_B = 1 # MML
PART_COUNT_B = 2

WEAPON_ID_B = 0xA011
SYS_STATUS_B = 0x04
COMM_STATUS_B = 0x01
CARRIER_PITCH_B = -179  # 0xFF4D
CARRIER_ROLL_B = 100  # 0x0064
PPL_AXIS_1_FW_B = -3206  # 0xF37A
PPL_AXIS_1_RIGHT_B = 1001  # 0x03E9
PPL_AXIS_1_DOWN_B = 0 # 0x0000
PPL_AXIS_2_FW_B = -32768 # 0x8000
PPL_AXIS_2_RIGHT_B = -1  # 0xFFFF
PPL_AXIS_2_DOWN_B = 2 # 0x0002
MAX_DEF_RANGE_B = 0x0A81BB00
WEAPON_KIND_B = 0x0004
FIRE_CONTROL_MODE_B = 0x05
FIRING_UNIT_STATUS_B = 0x06
FIRING_UNIT_ID_B = 0x0110
FIRING_UNIT_ELEV_B = 0x0020
FIRING_UNIT_AZIMUTH_B = 0x0200
FIRING_UNIT_ECEF_X_B = -286331154  # 0xEEEEEEEE
FIRING_UNIT_ECEF_Y_B = -2004318072  # 0x88888888
FIRING_UNIT_ECEF_Z_B = 406982947  # 0x18421123
FIRING_UNIT_INVS_B = [0x0001, 0x0002]
FIRING_UNIT_ROUND_STDBYS_B = [0x000F, 0x0010]
FIRING_UNIT_ROUND_READYS_B = [0xF000, 0xA111]
INTERCEPTOR_KINDS_B = [0x02, 0x09]

BYTES_B = bytearray([0x00, 0x00, 0x00, 0x54, 0x03, 0x87, 0x01, 0x02, 0xCC, 0xCC, 0xCC, 0xCC,
                     0xA0, 0x11, 0x04, 0x01, 0xFF, 0x4D, 0x00, 0x64, 0x00, 0x00, 0xF3, 0x7A,
                     0x03, 0xE9, 0x00, 0x00, 0x80, 0x00, 0xFF, 0xFF, 0x00, 0x02, 0x00, 0x00,
                     0x0A, 0x81, 0xBB, 0x00, 0x00, 0x04, 0x05, 0x06, 0x01, 0x10, 0x00, 0x20,
                     0x02, 0x00, 0x00, 0x00, 0xEE, 0xEE, 0xEE, 0xEE, 0x88, 0x88, 0x88, 0x88,
                     0x18, 0x42, 0x11, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x0F,
                     0xF0, 0x00, 0x02, 0x00, 0x00, 0x02, 0x00, 0x10, 0xA1, 0x11, 0x09, 0x00])

FAKE_TIME = 0xCCCCCCCC


def run903Test():
    test903_AI3_JSONSimple()
    test903_AI3ToBytes()
    test903_AI3FromBytes()
    test903_AI3_getNumBytes()
    print("903.0 AI3 Weapon Status: PASS")
    test903_MML_JSONSimple()
    test903_MMLToBytes()
    test903_MMLFromBytes()
    test903_MML_getNumBytes()
    print("903.1 MML Weapon Status: PASS")


def test903_AI3_JSONSimple():
    msg = t903_AI3(weaponId=WEAPON_ID_A, sysStatus=SYS_STATUS_A, commStatus=COMM_STATUS_A, vehicleDoorStatus=VEHICLE_DOOR_STATUS_A, searchSensorStatus=SEARCH_SENSOR_STATUS_A,
                   fcTrackSensorStatus=FC_TRACK_SENSOR_STATUS_A,
                   visIdSensorStatus=VIS_ID_SENSOR_STATUS_A, sensorNumFaces=SENSOR_NUM_FACES_A, holdFire=HOLD_FIRE_A,
                   sysMode=SYS_MODE_A, weaponKind=WEAPON_KIND_A,
                   sensorECEF_X=SENSOR_ECEF_X_A, sensorECEF_Y=SENSOR_ECEF_Y_A, sensorECEF_Z=SENSOR_ECEF_Z_A,
                   sensorAzimuth=SENSOR_AZIMUTH_A, maxDefRange=MAX_DEF_RANGE_A,
                   fireControlModes=FIRE_CONTROL_MODES_A,
                   firingUnitStatuses=FIRING_UNIT_STATUSES_A, firingUnitIds=FIRING_UNIT_IDS_A, firingUnitInvs=FIRING_UNIT_INVS_A,
                   firingUnitRoundStdbys=FIRING_UNIT_ROUND_STDBYS_A,
                   firingUnitElevs=FIRING_UNIT_ELEVS_A, firingUnitAzimuths=FIRING_UNIT_AZIMUTHS_A,
                   firingUnitECEF_Xs=FIRING_UNIT_ECEF_XS_A, firingUnitECEF_Ys=FIRING_UNIT_ECEF_YS_A, firingUnitECEF_Zs=FIRING_UNIT_ECEF_ZS_A,
                   firingUnitStartBounds=FIRING_UNIT_START_BOUNDS_A, firingUnitEndBounds=FIRING_UNIT_END_BOUNDS_A,
                   ammoKinds=AMMO_KINDS_A, platformAzimuths=PLATFORM_AZIMUTHS_A)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test903_AI3_getNumBytes():
    msg1 = getMessageFromBytes(BYTES_A)
    assert msg1.getNumBytes() == MSG_LENGTH_A, 'First getNumBytes failed: t903.0'
    # msg2 = t903_AI3(WEAPON_ID_A, SYS_STATUS_A, COMM_STATUS_A, VEHICLE_DOOR_STATUS_A, SEARCH_SENSOR_STATUS_A, FC_TRACK_SENSOR_STATUS_A,
    #                VIS_ID_SENSOR_STATUS_A, SENSOR_NUM_FACES_A, HOLD_FIRE_A, SYS_MODE_A, WEAPON_KIND_A, SENSOR_ECEF_X_A,
    #                SENSOR_ECEF_Y_A, SENSOR_ECEF_Z_A, SENSOR_AZIMUTH_A, MAX_DEF_RANGE_A, FIRE_CONTROL_MODES_A,
    #                FIRING_UNIT_STATUSES_A, FIRING_UNIT_IDS_A, FIRING_UNIT_INVS_A, FIRING_UNIT_ROUND_STDBYS_A,
    #                FIRING_UNIT_ELEVS_A, FIRING_UNIT_AZIMUTHS_A, FIRING_UNIT_ECEF_XS_A, FIRING_UNIT_ECEF_YS_A,
    #                FIRING_UNIT_ECEF_ZS_A, FIRING_UNIT_START_BOUNDS_A, FIRING_UNIT_END_BOUNDS_A, AMMO_KINDS_A, PLATFORM_AZIMUTHS_A)

    msg2 = t903_AI3(weaponId=WEAPON_ID_A, sysStatus=SYS_STATUS_A, commStatus=COMM_STATUS_A, vehicleDoorStatus=VEHICLE_DOOR_STATUS_A, searchSensorStatus=SEARCH_SENSOR_STATUS_A,
                   fcTrackSensorStatus=FC_TRACK_SENSOR_STATUS_A,
                   visIdSensorStatus=VIS_ID_SENSOR_STATUS_A, sensorNumFaces=SENSOR_NUM_FACES_A, holdFire=HOLD_FIRE_A,
                   sysMode=SYS_MODE_A, weaponKind=WEAPON_KIND_A,
                   sensorECEF_X=SENSOR_ECEF_X_A, sensorECEF_Y=SENSOR_ECEF_Y_A, sensorECEF_Z=SENSOR_ECEF_Z_A,
                   sensorAzimuth=SENSOR_AZIMUTH_A, maxDefRange=MAX_DEF_RANGE_A,
                   fireControlModes=FIRE_CONTROL_MODES_A,
                   firingUnitStatuses=FIRING_UNIT_STATUSES_A, firingUnitIds=FIRING_UNIT_IDS_A, firingUnitInvs=FIRING_UNIT_INVS_A,
                   firingUnitRoundStdbys=FIRING_UNIT_ROUND_STDBYS_A,
                   firingUnitElevs=FIRING_UNIT_ELEVS_A, firingUnitAzimuths=FIRING_UNIT_AZIMUTHS_A,
                   firingUnitECEF_Xs=FIRING_UNIT_ECEF_XS_A, firingUnitECEF_Ys=FIRING_UNIT_ECEF_YS_A, firingUnitECEF_Zs=FIRING_UNIT_ECEF_ZS_A,
                   firingUnitStartBounds=FIRING_UNIT_START_BOUNDS_A, firingUnitEndBounds=FIRING_UNIT_END_BOUNDS_A,
                   ammoKinds=AMMO_KINDS_A, platformAzimuths=PLATFORM_AZIMUTHS_A)



    assert msg2.getNumBytes() == MSG_LENGTH_A, 'Second getNumBytes failed: t903.0'


def test903_AI3ToBytes():
    # msg = t903_AI3(WEAPON_ID_A, SYS_STATUS_A, COMM_STATUS_A, VEHICLE_DOOR_STATUS_A, SEARCH_SENSOR_STATUS_A, FC_TRACK_SENSOR_STATUS_A,
    #                VIS_ID_SENSOR_STATUS_A, SENSOR_NUM_FACES_A, HOLD_FIRE_A, SYS_MODE_A, WEAPON_KIND_A, SENSOR_ECEF_X_A,
    #                SENSOR_ECEF_Y_A, SENSOR_ECEF_Z_A, SENSOR_AZIMUTH_A, MAX_DEF_RANGE_A, FIRE_CONTROL_MODES_A,
    #                FIRING_UNIT_STATUSES_A, FIRING_UNIT_IDS_A, FIRING_UNIT_INVS_A, FIRING_UNIT_ROUND_STDBYS_A,
    #                FIRING_UNIT_ELEVS_A, FIRING_UNIT_AZIMUTHS_A, FIRING_UNIT_ECEF_XS_A, FIRING_UNIT_ECEF_YS_A,
    #                FIRING_UNIT_ECEF_ZS_A, FIRING_UNIT_START_BOUNDS_A, FIRING_UNIT_END_BOUNDS_A, AMMO_KINDS_A, PLATFORM_AZIMUTHS_A)

    msg = t903_AI3(weaponId=WEAPON_ID_A, sysStatus=SYS_STATUS_A, commStatus=COMM_STATUS_A, vehicleDoorStatus=VEHICLE_DOOR_STATUS_A, searchSensorStatus=SEARCH_SENSOR_STATUS_A,
                   fcTrackSensorStatus=FC_TRACK_SENSOR_STATUS_A,
                   visIdSensorStatus=VIS_ID_SENSOR_STATUS_A, sensorNumFaces=SENSOR_NUM_FACES_A, holdFire=HOLD_FIRE_A,
                   sysMode=SYS_MODE_A, weaponKind=WEAPON_KIND_A,
                   sensorECEF_X=SENSOR_ECEF_X_A, sensorECEF_Y=SENSOR_ECEF_Y_A, sensorECEF_Z=SENSOR_ECEF_Z_A,
                   sensorAzimuth=SENSOR_AZIMUTH_A, maxDefRange=MAX_DEF_RANGE_A,
                   fireControlModes=FIRE_CONTROL_MODES_A,
                   firingUnitStatuses=FIRING_UNIT_STATUSES_A, firingUnitIds=FIRING_UNIT_IDS_A, firingUnitInvs=FIRING_UNIT_INVS_A,
                   firingUnitRoundStdbys=FIRING_UNIT_ROUND_STDBYS_A,
                   firingUnitElevs=FIRING_UNIT_ELEVS_A, firingUnitAzimuths=FIRING_UNIT_AZIMUTHS_A,
                   firingUnitECEF_Xs=FIRING_UNIT_ECEF_XS_A, firingUnitECEF_Ys=FIRING_UNIT_ECEF_YS_A, firingUnitECEF_Zs=FIRING_UNIT_ECEF_ZS_A,
                   firingUnitStartBounds=FIRING_UNIT_START_BOUNDS_A, firingUnitEndBounds=FIRING_UNIT_END_BOUNDS_A,
                   ammoKinds=AMMO_KINDS_A, platformAzimuths=PLATFORM_AZIMUTHS_A)



    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t903.0 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES_A, 'Byte array failed: t903.0 toBytes'

def test903_AI3FromBytes():
    msg = getMessageFromBytes(BYTES_A)
    assert msg.header.messageLength.data == MSG_LENGTH_A, 'Message Length wrong: t903.0 fromBytes'
    assert msg.header.messageId.data == MSG_ID_A, 'Message ID wrong: t903.0 fromBytes'
    assert msg.header.interfaceKind.data == KIND_A, 'Interface Kind wrong: t903.0 fromBytes'
    assert msg.header.partCount.data == PART_COUNT_A, 'Part Count wrong: t903.0 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t903.0 fromBytes'

    assert msg.weaponId.data == WEAPON_ID_A, 'Weapon ID wrong: t903.0 fromBytes'
    assert msg.sysStatus.data == SYS_STATUS_A, 'System Status wrong: t903.0 fromBytes'
    assert msg.commStatus.data == COMM_STATUS_A, 'Comm Status C2S wrong: t903.0 fromBytes'
    assert msg.vehicleDoorStatus.data == VEHICLE_DOOR_STATUS_A, 'Vehicle Door Status wrong: t903.0 fromBytes'
    assert msg.searchSensorStatus.data == SEARCH_SENSOR_STATUS_A, 'Search Sensor Status wrong: t903.0 fromBytes'
    assert msg.fcTrackSensorStatus.data == FC_TRACK_SENSOR_STATUS_A, 'FC/Track Sensor Status wrong: t903.0 fromBytes'
    assert msg.visIdSensorStatus.data == VIS_ID_SENSOR_STATUS_A, 'Visual ID Sensor Status wrong: t903.0 fromBytes'
    assert msg.sensorNumFaces.data == SENSOR_NUM_FACES_A, 'Sensor Num Faces wrong: t903.0 fromBytes'
    assert msg.holdFire.data == HOLD_FIRE_A, 'Hold Fire wrong: t903.0 fromBytes'
    assert msg.sysMode.data == SYS_MODE_A, 'System Mode wrong: t903.0 fromBytes'
    assert msg.weaponKind.data == WEAPON_KIND_A, 'Weapon Kind wrong: t903.0 fromBytes'
    assert msg.sensorECEF_X.data == SENSOR_ECEF_X_A, 'Sensor ECEF X wrong: t903.0 fromBytes'
    assert msg.sensorECEF_Y.data == SENSOR_ECEF_Y_A, 'Sensor ECEF Y wrong: t903.0 fromBytes'
    assert msg.sensorECEF_Z.data == SENSOR_ECEF_Z_A, 'Sensor ECEF Z wrong: t903.0 fromBytes'
    assert msg.sensorAzimuth.data == SENSOR_AZIMUTH_A, 'Sensor Azimuth wrong: t903.0 fromBytes'
    assert msg.maxDefRange.data == MAX_DEF_RANGE_A, 'Max Defended Range wrong: t903.0 fromBytes'
    assert msg.fireControlModes[0].data == FIRE_CONTROL_MODES_A[0], 'First Fire Control Mode wrong: t903.0 fromBytes'
    assert msg.fireControlModes[1].data == FIRE_CONTROL_MODES_A[1], 'Second Fire Control Mode wrong: t903.0 fromBytes'
    assert msg.firingUnitStatuses[0].data == FIRING_UNIT_STATUSES_A[0], 'First Firing Unit Status wrong: t903.0 fromBytes'
    assert msg.firingUnitStatuses[1].data == FIRING_UNIT_STATUSES_A[1], 'Second Firing Unit Status wrong: t903.0 fromBytes'
    assert msg.firingUnitIds[0].data == FIRING_UNIT_IDS_A[0], 'First Firing Unit ID wrong: t903.0 fromBytes'
    assert msg.firingUnitIds[1].data == FIRING_UNIT_IDS_A[1], 'Second Firing Unit ID wrong: t903.0 fromBytes'
    assert msg.firingUnitInvs[0].data == FIRING_UNIT_INVS_A[0], 'First Firing Unit Inventory wrong: t903.0 fromBytes'
    assert msg.firingUnitInvs[1].data == FIRING_UNIT_INVS_A[1], 'Second Firing Unit Inventory wrong: t903.0 fromBytes'
    assert msg.firingUnitRoundStdbys[0].data == FIRING_UNIT_ROUND_STDBYS_A[0], 'First Firing Unit Rounds Standby wrong: t903.0 fromBytes'
    assert msg.firingUnitRoundStdbys[1].data == FIRING_UNIT_ROUND_STDBYS_A[1], 'Second Firing Unit Rounds Standby wrong: t903.0 fromBytes'
    assert msg.firingUnitElevs[0].data == FIRING_UNIT_ELEVS_A[0], 'First Firing Unit Elevation wrong: t903.0 fromBytes'
    assert msg.firingUnitElevs[1].data == FIRING_UNIT_ELEVS_A[1], 'Second Firing Unit Elevation wrong: t903.0 fromBytes'
    assert msg.firingUnitAzimuths[0].data == FIRING_UNIT_AZIMUTHS_A[0], 'First Firing Unit Azimuth wrong: t903.0 fromBytes'
    assert msg.firingUnitAzimuths[1].data == FIRING_UNIT_AZIMUTHS_A[1], 'Second Firing Unit Azimuth wrong: t903.0 fromBytes'
    assert msg.firingUnitECEF_Xs[0].data == FIRING_UNIT_ECEF_XS_A[0], 'First Firing Unit ECEF X wrong: t903.0 fromBytes'
    assert msg.firingUnitECEF_Xs[1].data == FIRING_UNIT_ECEF_XS_A[1], 'Second Firing Unit ECEF X wrong: t903.0 fromBytes'
    assert msg.firingUnitECEF_Ys[0].data == FIRING_UNIT_ECEF_YS_A[0], 'First Firing Unit ECEF Y wrong: t903.0 fromBytes'
    assert msg.firingUnitECEF_Ys[1].data == FIRING_UNIT_ECEF_YS_A[1], 'Second Firing Unit ECEF Y wrong: t903.0 fromBytes'
    assert msg.firingUnitECEF_Zs[0].data == FIRING_UNIT_ECEF_ZS_A[0], 'First Firing Unit ECEF Z wrong: t903.0 fromBytes'
    assert msg.firingUnitECEF_Zs[1].data == FIRING_UNIT_ECEF_ZS_A[1], 'Second Firing Unit ECEF Z wrong: t903.0 fromBytes'
    assert msg.firingUnitStartBounds[0].data == FIRING_UNIT_START_BOUNDS_A[0], 'First Firing Unit Starting Boundary wrong: t903.0 fromBytes'
    assert msg.firingUnitStartBounds[1].data == FIRING_UNIT_START_BOUNDS_A[1], 'Second Firing Unit Starting Boundary wrong: t903.0 fromBytes'
    assert msg.firingUnitEndBounds[0].data == FIRING_UNIT_END_BOUNDS_A[0], 'First Firing Unit Ending Boundary wrong: t903.0 fromBytes'
    assert msg.firingUnitEndBounds[1].data == FIRING_UNIT_END_BOUNDS_A[1], 'Second Firing Unit Ending Boundary wrong: t903.0 fromBytes'
    assert msg.ammoKinds[0].data == AMMO_KINDS_A[0], 'First Ammo Kind wrong: t903.0 fromBytes'
    assert msg.ammoKinds[1].data == AMMO_KINDS_A[1], 'Second Ammo Kind wrong: t903.0 fromBytes'
    assert msg.platformAzimuths[0].data == PLATFORM_AZIMUTHS_A[0], 'First Platform Azimuth wrong: t903.0 fromBytes'
    assert msg.platformAzimuths[1].data == PLATFORM_AZIMUTHS_A[1], 'Second Platform Azimuth wrong: t903.0 fromBytes'


def test903_MML_JSONSimple():
    msg = t903_MML(WEAPON_ID_B, SYS_STATUS_B, COMM_STATUS_B, CARRIER_PITCH_B, CARRIER_ROLL_B, PPL_AXIS_1_FW_B,
                    PPL_AXIS_1_RIGHT_B, PPL_AXIS_1_DOWN_B, PPL_AXIS_2_FW_B, PPL_AXIS_2_RIGHT_B, PPL_AXIS_2_DOWN_B,
                    MAX_DEF_RANGE_B, WEAPON_KIND_B, FIRE_CONTROL_MODE_B, FIRING_UNIT_STATUS_B, FIRING_UNIT_ID_B,
                    FIRING_UNIT_ELEV_B, FIRING_UNIT_AZIMUTH_B, FIRING_UNIT_ECEF_X_B, FIRING_UNIT_ECEF_Y_B,
                    FIRING_UNIT_ECEF_Z_B, FIRING_UNIT_INVS_B, FIRING_UNIT_ROUND_STDBYS_B, FIRING_UNIT_ROUND_READYS_B,
                    INTERCEPTOR_KINDS_B)
    str1 = msg.toJSON()
    msg_copy = getMessageFromJSON(str1)
    assert msg == msg_copy


def test903_MML_getNumBytes():
    msg1 = getMessageFromBytes(BYTES_B)
    assert msg1.getNumBytes() == MSG_LENGTH_B, 'First getNumBytes failed: t903.1'
    msg2 = t903_MML(WEAPON_ID_B, SYS_STATUS_B, COMM_STATUS_B, CARRIER_PITCH_B, CARRIER_ROLL_B, PPL_AXIS_1_FW_B,
                    PPL_AXIS_1_RIGHT_B, PPL_AXIS_1_DOWN_B, PPL_AXIS_2_FW_B, PPL_AXIS_2_RIGHT_B, PPL_AXIS_2_DOWN_B,
                    MAX_DEF_RANGE_B, WEAPON_KIND_B, FIRE_CONTROL_MODE_B, FIRING_UNIT_STATUS_B, FIRING_UNIT_ID_B,
                    FIRING_UNIT_ELEV_B, FIRING_UNIT_AZIMUTH_B, FIRING_UNIT_ECEF_X_B, FIRING_UNIT_ECEF_Y_B,
                    FIRING_UNIT_ECEF_Z_B, FIRING_UNIT_INVS_B, FIRING_UNIT_ROUND_STDBYS_B, FIRING_UNIT_ROUND_READYS_B,
                    INTERCEPTOR_KINDS_B)
    assert msg2.getNumBytes() == MSG_LENGTH_B, 'Second getNumBytes failed: t903.1'


def test903_MMLToBytes():
    msg = t903_MML(WEAPON_ID_B, SYS_STATUS_B, COMM_STATUS_B, CARRIER_PITCH_B, CARRIER_ROLL_B, PPL_AXIS_1_FW_B,
                   PPL_AXIS_1_RIGHT_B, PPL_AXIS_1_DOWN_B, PPL_AXIS_2_FW_B, PPL_AXIS_2_RIGHT_B, PPL_AXIS_2_DOWN_B,
                   MAX_DEF_RANGE_B, WEAPON_KIND_B, FIRE_CONTROL_MODE_B, FIRING_UNIT_STATUS_B, FIRING_UNIT_ID_B,
                   FIRING_UNIT_ELEV_B, FIRING_UNIT_AZIMUTH_B, FIRING_UNIT_ECEF_X_B, FIRING_UNIT_ECEF_Y_B,
                   FIRING_UNIT_ECEF_Z_B, FIRING_UNIT_INVS_B, FIRING_UNIT_ROUND_STDBYS_B, FIRING_UNIT_ROUND_READYS_B,
                   INTERCEPTOR_KINDS_B)
    assert msg.header.transmitTime.data + 5000 > millisSinceMidnight(), 'Transmit time way off (>5 seconds): t903.1 toBytes'
    msg.header.transmitTime = ElementUInt32(FAKE_TIME)
    assert msg.getByteArray() == BYTES_B, 'Byte array failed: t903.1 toBytes'

def test903_MMLFromBytes():
    msg = getMessageFromBytes(BYTES_B)
    assert msg.header.messageLength.data == MSG_LENGTH_B, 'Message Length wrong: t903.1 fromBytes'
    assert msg.header.messageId.data == MSG_ID_B, 'Message ID wrong: t903.1 fromBytes'
    assert msg.header.interfaceKind.data == KIND_B, 'Interface Kind wrong: t903.1 fromBytes'
    assert msg.header.partCount.data == PART_COUNT_B, 'Part Count wrong: t903.1 fromBytes'
    assert msg.header.transmitTime.data == FAKE_TIME, 'Transmit Time wrong: t903.1 fromBytes'

    assert msg.weaponId.data == WEAPON_ID_B, 'Weapon ID wrong: t903.1 fromBytes'
    assert msg.sysStatus.data == SYS_STATUS_B, 'System Status wrong: t903.1 fromBytes'
    assert msg.commStatus.data == COMM_STATUS_B, 'Comm Status C2S wrong: t903.1 fromBytes'
    assert msg.carrierPitch.data == CARRIER_PITCH_B, 'Carrier Pitch wrong: t903.1 fromBytes'
    assert msg.carrierRoll.data == CARRIER_ROLL_B, 'Carrier Roll wrong: t903.1 fromBytes'
    assert msg.pplAxis1_Fw.data == PPL_AXIS_1_FW_B, 'Principal Axis 1 Fw wrong: t903.1 fromBytes'
    assert msg.pplAxis1_Right.data == PPL_AXIS_1_RIGHT_B, 'Principal Axis 1 Right wrong: t903.1 fromBytes'
    assert msg.pplAxis1_Down.data == PPL_AXIS_1_DOWN_B, 'Principal Axis 1 Down wrong: t903.1 fromBytes'
    assert msg.pplAxis2_Fw.data == PPL_AXIS_2_FW_B, 'Principal Axis 2 Fw wrong: t903.1 fromBytes'
    assert msg.pplAxis2_Right.data == PPL_AXIS_2_RIGHT_B, 'Principal Axis 2 Right wrong: t903.1 fromBytes'
    assert msg.pplAxis2_Down.data == PPL_AXIS_2_DOWN_B, 'Principal Axis 2 Down wrong: t903.1 fromBytes'
    assert msg.maxDefRange.data == MAX_DEF_RANGE_B, 'Max Defended Range wrong: t903.1 fromBytes'
    assert msg.weaponKind.data == WEAPON_KIND_B, 'Weapon Kind wrong: t903.1 fromBytes'
    assert msg.fireControlMode.data == FIRE_CONTROL_MODE_B, 'Fire Control Mode wrong: t903.1 fromBytes'
    assert msg.firingUnitStatus.data == FIRING_UNIT_STATUS_B, 'Firing Unit Status wrong: t903.1 fromBytes'
    assert msg.firingUnitID.data == FIRING_UNIT_ID_B, 'Firing Unit ID wrong: t903.1 fromBytes'
    assert msg.firingUnitElev.data == FIRING_UNIT_ELEV_B, 'Firing Unit Elevation wrong: t903.1 fromBytes'
    assert msg.firingUnitAzimuth.data == FIRING_UNIT_AZIMUTH_B, 'Firing Unit Azimuth wrong: t903.1 fromBytes'
    assert msg.firingUnitECEF_X.data == FIRING_UNIT_ECEF_X_B, 'Firing Unit ECEF X wrong: t903.1 fromBytes'
    assert msg.firingUnitECEF_Y.data == FIRING_UNIT_ECEF_Y_B, 'Firing Unit ECEF Y wrong: t903.1 fromBytes'
    assert msg.firingUnitECEF_Z.data == FIRING_UNIT_ECEF_Z_B, 'Firing Unit ECEF Z wrong: t903.1 fromBytes'
    assert msg.firingUnitInvs[0].data == FIRING_UNIT_INVS_B[0], 'First Firing Unit Inventory wrong: t903.1 fromBytes'
    assert msg.firingUnitInvs[1].data == FIRING_UNIT_INVS_B[1], 'Second Firing Unit Inventory wrong: t903.1 fromBytes'
    assert msg.firingUnitRoundStdbys[0].data == FIRING_UNIT_ROUND_STDBYS_B[0], 'First Firing Unit Rounds Standby wrong: t903.1 fromBytes'
    assert msg.firingUnitRoundStdbys[1].data == FIRING_UNIT_ROUND_STDBYS_B[1], 'Second Firing Unit Rounds Standby wrong: t903.1 fromBytes'
    assert msg.firingUnitRoundReadys[0].data == FIRING_UNIT_ROUND_READYS_B[0], 'First Firing Unit Rounds Ready wrong: t903.1 fromBytes'
    assert msg.firingUnitRoundReadys[1].data == FIRING_UNIT_ROUND_READYS_B[1], 'Second Firing Unit Rounds Ready wrong: t903.1 fromBytes'
    assert msg.interceptorKinds[0].data == INTERCEPTOR_KINDS_B[0], 'First drone Kind wrong: t903.1 fromBytes'
    assert msg.interceptorKinds[1].data == INTERCEPTOR_KINDS_B[1], 'Second drone Kind wrong: t903.1 fromBytes'

