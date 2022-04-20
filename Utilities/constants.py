# https://stackoverflow.com/questions/6345840/whats-the-best-way-to-initialise-and-use-constants-across-python-classes
# todo Perhaps in the future these can be replaced with actual UNICODE chars!
# https://github.com/Microsoft/console/issues/190
from datetime import datetime, timedelta
from enum import Enum


ConnectFail = ":-( "
WaitingForGroundspaceInterceptor = "w"
Heartbeat = " ^"
NettimeResponseSentToCRAM = "Nettime"
ThreatStatusReceivedFromCRAMandForwardedtoGS = "Threat"
nonThreatStatusReceivedfromCRAMNotFWDtoGS  =  "Threat :-)"
GroundspaceInterceptorStatusSenttoCRAM = "->"

# ConnectFail = "☹"
# WaitingForGroundspaceInterceptor = "🛪"
# Heartbeat = " ♥"
# NettimeResponseSentToCRAM = "⏱"
# ThreatStatusReceivedFromCRAMandForwardedtoGS = "🔪"
# nonThreatStatusReceivedfromCRAMNotFWDtoGS  =  "🔪😊︎"
# GroundspaceInterceptorStatusSenttoCRAM = "✈"

GroundspaceSendRate: float = 0.2  # Send no faster than 5Hz = .2 seconds
Groundspacetimedelta = timedelta(seconds=GroundspaceSendRate)
# GSOkbytes:bytes = b'Ok\r\n'
GSOk:str = 'Ok\r\n'


AprilFoolsDay2k :datetime = datetime(2000,4,1) #Use as an initializer
NullWeaponId = -1

GroundZero = {
    'Lat':37.870575,
    'Lon':-122.379556,
    'Elev':0,
    } #middle of SF Bay just East of Angel Island.


# https://www.geeksforgeeks.org/enum-in-python/
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html
# https://dev.to/karn/building-a-simple-state-machine-in-python
class currentState(Enum):
    NOCHANGE = 0
    LOOP = 1
    DISPATCH = 2
    INTERDICTION = 3
    GOHOME = 4

