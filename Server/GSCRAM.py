import time
from datetime import datetime
from Utilities import constants
from Utilities.CfgParse import KvpReader
from Utilities.console import debugLog
from Utilities.Exceptions import GroundspaceConnectionErr, noCRAMConn, noGroundspaceServerConn
from Utilities.Utility import Utility


class GSCRAM:
    Util:Utility = Utility.getInstance()
    configr = KvpReader()
    deployment  = configr.getvalue(key_name="Deployment")
    APPVERSION = configr.getvalue(key_name="APPVERSION", section_name=deployment)

    @staticmethod
    def start():
        debugLog.log("GSCRAM Counter Rocket, Artillary, and Mortar v" + GSCRAM.APPVERSION + "\t(copyright Airspace Systems, Inc.)")

        debugLog.log("Glossary:")
        debugLog.log("\t\t " + constants.ConnectFail + " = connect fail")
        debugLog.log("\t\t " + constants.WaitingForGroundspaceInterceptor + " = Waiting for Groundspace Interceptor")
        debugLog.log("\t\t " + constants.Heartbeat + " = Application level linkage Heartbeat pulse")
        debugLog.log("\t\t " + constants.NettimeResponseSentToCRAM + " = Nettime response sent to CRAM")
        debugLog.log("\t\t " + constants.ThreatStatusReceivedFromCRAMandForwardedtoGS + " = Threat status received from CRAM and forwarded to GS")
        debugLog.log("\t\t " + constants.nonThreatStatusReceivedfromCRAMNotFWDtoGS + " = nonThreat status received from CRAM (not forwarded to GS)")
        debugLog.log("\t\t " + constants.GroundspaceInterceptorStatusSenttoCRAM + " = Groundspace Interceptor status sent to CRAM\n\n")

        retries: int = 0
        try:
            while not Utility.startUp():
                Utility.shutDown(str(datetime.utcnow()) + " startup failed/retry")
                retries += 1
                retrystr:str = str(datetime.utcnow()) + ":\tstart() retry: " + str(retries)
                print(retrystr)
                debugLog.log(retrystr)
                time.sleep(1.11)
        except (GroundspaceConnectionErr, noGroundspaceServerConn, noCRAMConn) as err:
            debugLog.log("\n\nGSCRAM start() error!: " + str(err) + "\n\n")
            Utility.shutDown("start fail: " + str(err))

