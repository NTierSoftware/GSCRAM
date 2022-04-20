import socket, time, errno
from Utilities.CfgParse import KvpReader
from Utilities.Exceptions import noCRAMConn, noGroundspaceServerConn, noCoTConn
# from Utilities.console import debugLog
from Utilities.console import console, debugLog
from Utilities import constants


class connections:
#There are 3 types of Simulations
# LIVE means no Simulation.
# TABLETOP means TABLETOP testing in which case
#    both the CoT CDS3 Simulator (to display and transmit Radar RES target and Interceptor telemetry)
#    and the Interpolator (fake flight status to interpolate/move the Interceptor towards the target) are required.
# SELFREPORTINGTARGET means testing at Patrick Kennedy Field in which case the Interpolator is not used
# but the CDS3 Simulator is still needed as before.

    LIVE = 'LIVE'
    SELFREPORTINGTARGET = 'SELFREPORTINGTARGET'
    TABLETOP = 'TABLETOP'

    configr = KvpReader()
    deployment  = configr.getvalue(key_name="Deployment")
    # APPVERSION = configr.getvalue(key_name="APPVERSION", section_name=deployment)
    SIMULATE =  configr.getvalue(key_name="SIMULATE", section_name=deployment)
    # MAXConnretries  = int( configr.getvalue(key_name="MAXConnretries", section_name=deployment))
    # Timeout  = .411 #seconds
    Timeout  = .2 #seconds
    GroundspaceTCP = 2301
    GroundspaceUDP = 2302
    TCPbufsize  = 1024
    # MaxNumConns = 1
    GSaddress = CRAMaddress = CRAMaccept = ()


    def shut(s:socket.socket):
        if s:# is None: return
            try: s.shutdown(socket.SHUT_RDWR)
            except (OSError, AttributeError): pass
            try: s.close()
            except (OSError, AttributeError): pass

    @staticmethod
    def clientToGroundspaceSvr() -> socket : #GSCRAM CLIENT conn to Groundspace Server
        GroundspaceClient = None
        try:
            deploy = connections.deployment
            GroundspaceServer = connections.configr.getvalue(key_name="LocalGroundspaceServer", section_name=deploy)
            connections.GSaddress = (GroundspaceServer, connections.GroundspaceTCP)
            GroundspaceClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

            GroundspaceClient.connect(connections.GSaddress)
            # GroundspaceClient.settimeout(0)
            return GroundspaceClient
        # except (socket.error, socket.timeout) as err:
        except Exception as err:
            print('clientToGroundspaceSvr() err: ', err, end='', flush=True)
            connections.shut(GroundspaceClient)
        return None


    @staticmethod
    def serverToCRAMclient() -> socket:  # GSCRAM Server conn to CRAM client
        CRAMclientConn = CRAMsocket= None

        try:
            deploy = connections.deployment
            LocalCRAMclient = connections.configr.getvalue(key_name="LocalCRAMclient", section_name=deploy)
            CRAMTCP = int(connections.configr.getvalue(key_name="CRAMTCP", section_name=deploy))
            connections.CRAMaddress = (LocalCRAMclient, CRAMTCP)

            CRAMsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CRAMsocket.bind(connections.CRAMaddress)
            CRAMsocket.settimeout(connections.Timeout)
            CRAMsocket.listen(1)
            (CRAMclientConn, addr) = connections.CRAMaccept = CRAMsocket.accept()

            return CRAMclientConn
        except socket.error:
            # print('serverToCRAMclient() err:', err, end='', flush=True)
            connections.shut(CRAMclientConn)
            connections.shut(CRAMsocket)
        return None




    GSCoTSvr = configr.getvalue(key_name="GSCoTSvr", section_name=deployment )
    CoTport = int( configr.getvalue(key_name="CoTport", section_name=deployment ) )

    GSCRAMtoCDS3addr = (GSCoTSvr, CoTport)


    @staticmethod
    def DJISimulatorToGSCRAMudp(FIRSTCONNECT:bool=False) -> socket : # server conn to receive CoT sim target location updates
        CoTsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        CoTsock.bind(connections.GSCRAMtoCDS3addr)
        # CoTsock.settimeout(0)

        numRetries = 0
        while True:
        # while numRetries < connections.MAXConnretries or (connections.MAXConnretries == 0): #MAXConnretries ==0 means retry indefinitely
            try:
                CoTsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                CoTsock.bind(connections.GSCRAMtoCDS3addr)
                CoTsock.settimeout(connections.Timeout)
                if FIRSTCONNECT: debugLog.log("connected to CoT client: " + ' ' + str(CoTsock))
                return CoTsock
            except (socket.error, socket.timeout) as err:
                numRetries += 1
                debugLog.log(constants.ConnectFail + "retry CoT client " + str(numRetries) + ' ' + str(connections.GSCRAMtoCDS3addr) + ' ' + str(err))
                # debugScreen.log( ":-( retry CoT client " + str(numRetries) + ' ' + str(connections.GSCRAMtoCDS3addr) + ' ' + str(err))
                continue

        raise noCoTConn("Cannot connect to CoT")


    @staticmethod
    def DJISimulatorToGSCRAMtcp(FIRSTCONNECT:bool=False) -> socket : # server conn to receive CoT sim target location updates
        CoTsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        CoTsock.bind(connections.GSCRAMtoCDS3addr)
        CoTsock.settimeout(0)

        numRetries = 0
        while True:
        # while numRetries < connections.MAXConnretries or (connections.MAXConnretries == 0): #MAXConnretries ==0 means retry indefinitely
            try:
                CoTsock.settimeout(connections.Timeout)
                # CoTsock.listen(connections.MaxNumConns)
                CoTsock.listen(1)
                CoTclientConn, addr = CoTsock.accept()
                CoTclientConn.settimeout(None)
                if FIRSTCONNECT: debugLog.log("connected to CoT client: " + ' ' + str(addr))
                return CoTclientConn
            except (socket.error, socket.timeout) as err:
                numRetries += 1
                debugLog.log(constants.ConnectFail + "retry CoT client " + str(numRetries) + ' ' + str(connections.GSCRAMtoCDS3addr) + ' ' + str(err))
                # debugScreen.log( ":-( retry CoT client " + str(numRetries) + ' ' + str(connections.GSCRAMtoCDS3addr) + ' ' + str(err))
                continue

        raise noCoTConn("Cannot connect to CoT")

    @staticmethod
    def DJISimulatorToGSCRAM(FIRSTCONNECT:bool=False) -> socket : # server conn to receive CoT sim target location updates
        CoTsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        try: CoTsock.bind(connections.GSCRAMtoCDS3addr)
        except OSError as err:
            if err.errno == errno.EADDRNOTAVAIL: raise Exception("Have you turned on WIFI?: " + str(err))
            raise err

        CoTsock.settimeout(0)

        numRetries = 0
        while True:
        # while numRetries < connections.MAXConnretries or (connections.MAXConnretries == 0): #MAXConnretries ==0 means retry indefinitely
            try:
                CoTsock.settimeout(connections.Timeout)
                # CoTsock.listen(connections.MaxNumConns)
                CoTsock.listen(1)
                CoTclientConn, addr = CoTsock.accept()
                CoTclientConn.settimeout(None)
                if FIRSTCONNECT: debugLog.log("DJISimulatorToGSCRAM: connected to CoT client: " + ' ' + str(addr))
                return CoTclientConn
            except (socket.error, socket.timeout) as err:
                numRetries += 1
                debugLog.log(constants.ConnectFail + "retry CoT client " + str(numRetries) + ' ' + str(connections.GSCRAMtoCDS3addr) + ' ' + str(err))
                continue

        raise noCoTConn("Cannot connect to CoT")
