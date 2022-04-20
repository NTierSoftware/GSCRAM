# John.JD.Donaldson@airspace.co, 8/20/2018
# https://softwareengineering.stackexchange.com/questions/351389/dynamic-dispatch-from-a-string-python
import json
# import traceback

from datetime import datetime

from GSmsg.GSBaseMessage import GSBaseMessage
from GSmsg.rInterdiction import rInterdiction
from GSmsg.rtDroneStatus import rtDroneStatus
# from GSmsg.tDoNotEngage import tDoNotEngage
# from GSmsg.tGoToWaypoint import tGoToWaypoint
# from GSmsg.tTargetStatus import tTargetStatus
# from GSmsg.tWeaponsFree import tWeaponsFree
from GSmsg.rErrNoDroneAvailable import rErrNoDroneAvailable
# from GSmsg.tGoHome import tGoHome
# from GSmsg.ErrDisconnect import ErrDisconnect
# from Utilities.Exceptions import GroundspaceReject, BadJSON
# from Utilities import constants

GSmsgtypes = {
    'rtDroneStatus': rtDroneStatus,
    'rInterdiction': rInterdiction,
    'rErrNoDroneAvailable': rErrNoDroneAvailable,
}
# 'ErrDisconnect': ErrDisconnect,
# 'tTargetStatus': tTargetStatus,
# 'tWeaponsFree': tWeaponsFree,
# 'tGoToWaypoint': tGoToWaypoint,
# 'tDoNotEngage': tDoNotEngage,
# 'tGoHome': tGoHome


def JSONToGSmsg(jsonStr: str) -> GSBaseMessage:
    try:
        return GSmsgtypes[json.loads(jsonStr)['msgType']].fromJSON(jsonStr)
        # debug...
        # json_dict = json.loads(jsonStr)
        # msgType = json_dict['msgType']
        # return GSmsgtypes[msgType].fromJSON(jsonStr)
    except (json.decoder.JSONDecodeError, KeyError, TypeError) as err:
        # if constants.GSOk in jsonStr: return JSONToGSmsg(jsonStr.replace(constants.GSOk, ''))
        if jsonStr.startswith('Command '): print(datetime.utcnow(), "\nERR: Groundspace does not understand this message:", jsonStr, '\n', end='', flush=True)
        else:
            if jsonStr: print(datetime.utcnow(), "\nJSONToGSmsg() ERR: Bad JSON:", jsonStr, '\n', err, '\n', end='', flush=True)

    return None
        # traceback.print_stack()
