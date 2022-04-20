from datetime import datetime

class baseMethodErr(Exception):
    def __init__(self, method:str ): print('\n', datetime.utcnow(), method, "must be overridden.")

class noCRAMConn(Exception):
    def __init__(self, operation: str):
        self.operation = operation
        return

class noGroundspaceServerConn(Exception):
    def __init__(self, operation: str):
        self.operation = operation
        return

class noCoTConn(Exception):
    def __init__(self, operation: str):
        self.operation = operation
        return


class UnexpectedResponseFromGroundspace(Exception):
    def __init__(self, message: str):
        self.message = message
        print('\n', datetime.utcnow(), "Unexpected Response from Groundspace: ", self.message)

class UnexpectedResponseFromCRAM(Exception):
    def __init__(self, badMsgId:int, message: bytearray):
        self.msgId = badMsgId
        self.message = message
        print("\nbadMsgId\tlength\tmsg.hex()\n", str(self.msgId) + "\t" + str(self.message.__len__()) + "\t" + str(self.message.hex()))


class GroundspaceConnectionErr(Exception):
    def __init__(self, err: Exception):
        print("Groundspace Connection error: " + str(err))


#begin JSONtoGSmsg exceptions
class UnimplementedMsgFromGroundspace(Exception):
    def __init__(self, message: str):
        self.message = message
        print("This is an unimplemented Groundspace message:", self.message)

class GSInterceptorDisconnected(Exception):
    def __init__(self, msg:str=''):
        print("\n\n\t\tThe Groundspace Interceptor is not connected! Connect it and/or restart.\n\n", self)

class GroundspaceReject(Exception):
    def __init__(self, message: str):
        self.message = message
        print("Groundspace does not understand this message:", self.message)

class BadJSON(Exception):
    def __init__(self, message: str):
        self.message = message
        print("Bad JSON from Groundspace:", self.message)

#end JSONtoGSmsg exceptions

#begin Conversation exceptions
class MkFilePathError(Exception):
    def __init__(self, path): Exception.__init__(self, 'Cannot create log files/paths: ' + path)

class SendToGSErr(Exception):
    def __init__(self): Exception.__init__(self, 'Cannot send message to Groundspace! Check TCP connection.')

class MessageReceiveError(Exception):
    def __init__(self):
        self.message = 'Cannot receive message. Check TCP connection.'
        print(self.message, self)
        Exception.__init__(self, self.message)

class MessageMissingError(Exception):
    def __init__(self, frameNum):
        Exception.__init__(self, 'No Message in Conversation with frame number: {0}'.format(frameNum))

class MessageWrongTypeError(Exception):
    def __init__(self, frameNum, cls):
        Exception.__init__(self, 'Message with frame number {0} is not of type: {1}'.format(frameNum, cls))

class BadOkfromGroundspace(Exception):
    def __init__(self, badOk):
        Exception.__init__(self, 'The response \"Ok\\r\\n" was expected from Groundspace but this was received: ' + badOk )

#end Conversation exceptions

#begin Looper exceptions
class applicationLevelLinkageErr(Exception):
    def __init__(self): Exception.__init__(self, 'applicationLevelLinkageErr: Groundspace or CRAM connection error.')

#end Looper exceptions


#begin CoTpulse exceptions
class CoTpulseDeadError(Exception):
    def __init__(self, operation: str, message: str):
        self.operation = operation
        self.message = message
#end CoTpulse exceptions



#begin NetworkThread exceptions
class selectErrs(Exception):
    def __init__(self, message: str):
        self.message = message
        print('\n', datetime.utcnow(), "NetworkThread: errors found in select(): ", self.message)

class NetworkThreadTimeout(Exception):
    def __init__(self ): print('\n', datetime.utcnow(), "err NetworkThreadTimeout")

# class NetworkThreadNoRegistry(Exception):
#     def __init__(self ): print('\n', datetime.utcnow(), "err NetworkThreadNoRegistry: You must call NetworkThread.register() before NetworkThread.start()" )

class threadedSocketNoTelemetryYet(Exception):
    def __init__(self ): print('\n', datetime.utcnow(), "err threadedSocketNoTelemetryYet")


class NetworkThreadRegistryNotConnected(Exception):
    def __init__(self ): print('\n', datetime.utcnow(), "err in NetworkThread: the socket must be connected before it can be registered.")


#end NetworkThread exceptions
