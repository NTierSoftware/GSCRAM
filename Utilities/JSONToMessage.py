# JD, Alex Erf, Airspace, alex.erf@airspace.co, 8/8/2018
# https://softwareengineering.stackexchange.com/questions/351389/dynamic-dispatch-from-a-string-python
import json
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.rt900WeaponCmd import rt900WeaponCmd
from CRAMmsg.rt902WeaponHeartbeat import rt902WeaponHeartbeat
from CRAMmsg.t903WeaponStatus import t903WeaponStatus
# from CRAMmsg.r909EngagementPlan import r909EngagementPlan
from CRAMmsg.t910EngagementStatus import t910EngagementStatus
# from CRAMmsg.rt912DoNotEngage import rt912DoNotEngage
from CRAMmsg.rt915NetTime import rt915NetTime
from CRAMmsg.r920ThreatState import r920ThreatState
# from CRAMmsg.rt922MeteorlogicalData import rt922MeteorlogicalData
# from GSmsg.ErrDisconnect import ErrDisconnect
from CRAMmsg.rt702Spoof import rt702Spoof
CRAMmsgtypes = {
    915: rt915NetTime,
    900: rt900WeaponCmd,
    902: rt902WeaponHeartbeat,
    # 909: r909EngagementPlan,
    # 912: rt912DoNotEngage,
    920: r920ThreatState,
    # 922: rt922MeteorlogicalData,
    903: t903WeaponStatus,
    # 910: t910EngagementStatus
    702: rt702Spoof,
}
# 924: rt924InterceptorWaypoint,
# 925: t925InterceptorStatus,
# 926: r926WeaponEmplacement


def getMessageFromJSON(jsonStr: str) -> CRAMBaseMessage:
    json_dict = json.loads(jsonStr)
    msgId = json_dict['messageHeader']['messageId']


    return CRAMmsgtypes[msgId].fromJSON(jsonStr)
#TODO error handling
