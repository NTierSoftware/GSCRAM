from enum import Enum

class CRAMmsgType(Enum):
    rt900WeaponCmd = 900
    r901LinkInit = 901
    rt902WeaponHeartbeat = 902
    t903WeaponStatus = 903
    r904AirPictureTrack = 904
    t905WESAirTrack = 905
    r906RAMTrack = 906
    t907WESRAMTrack = 907
    t908LaunchPoint = 908
    r909EngagementPlan = 909
    t910EngagementStatus = 910
    r911LauncherPrePosition = 911
    rt912DoNotEngage = 912
    r913ProtectedAssetCircle = 913
    r914ProtectedAssetPolygon = 914
    rt915NetTime = 915
    t916WeaponNoFireSectors = 916
    rt917Operator = 917
    t918FCRStatus = 918
    r919InventoryManagement = 919
    r920ThreatState = 920
    t921LauncherCutout = 921
    rt922MeteorologicalData = 922
    r923SensorRegBiasCorrection = 923
    rt924InterceptorWaypoint = 924
    t925InterceptorStatus = 925
    t926WeaponEmplacement = 926

    # @classmethod
    # def msgIsOfKind(cls, msg: 'CRAMBaseMssage', kind: 'CRAMmsgType') -> bool:
    #     return msg.getMsgID() == kind.value

