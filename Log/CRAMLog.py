# Alex Erf, Airspace, alex.erf@airspace.co, 7/30/2018

import logging, sys
# from Utilities.console import console
# debugScreen: console = console(console.DEBUG, title="GSCRAM Debug")


class CRAMLog:
    """This class contains functions to facilitate logging hexadecimal and decimal data streams from CRAM."""
    
    # Constants for log name references
    LOG_NAME_HEX = 'cram_log_hex'
    LOG_NAME_DEC = 'cram_log_dec'
    LOG_NAME_JSON = 'cram_log_json'
    LOG_NAME_STD = 'cram_log'

    OUT_FILE_HEX = '\GSCRAM\logs\cram_log.hex'
    OUT_FILE_DEC = '\GSCRAM\logs\cram_log.dec'
    OUT_FILE_JSON = '\GSCRAM\logs\cram_log.json'
    OUT_FILE_LOG = '\GSCRAM\logs\cram_log.log'

    # Constants for log message formats
    SIMPLE_FORMAT = '%(message)s'
    FULL_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s - %(message)s'

    def __init__(self):
        # return #kluge

        """Initializes the loggers, formatters, and log handlers."""
        # create loggers
        self.hexLogger = logging.getLogger(self.LOG_NAME_HEX)
        self.hexLogger.setLevel(logging.DEBUG)
        self.decLogger = logging.getLogger(self.LOG_NAME_DEC)
        self.decLogger.setLevel(logging.DEBUG)
        self.jsonLogger = logging.getLogger(self.LOG_NAME_JSON)
        self.jsonLogger.setLevel(logging.DEBUG)
        self.logger = logging.getLogger(self.LOG_NAME_STD)
        self.logger.setLevel(logging.DEBUG)
        # create console handler
        self.consoleLogger = logging.StreamHandler()
        self.consoleLogger.setLevel(logging.DEBUG)
        # create file handlers
        try:
            self.hexLoggerFh = logging.FileHandler(self.OUT_FILE_HEX)
            self.decLoggerFh = logging.FileHandler(self.OUT_FILE_DEC)
            self.jsonLoggerFh = logging.FileHandler(self.OUT_FILE_JSON)
            self.loggerFh = logging.FileHandler(self.OUT_FILE_LOG)
        except FileNotFoundError:
            print("Log Error: could not find directory \GSCRAM\logs - please ensure this directory exists")
            # print("Log Error: could not find directory C:\CRAM\logs - please ensure this directory exists")
            sys.exit()
        self.hexLoggerFh.setLevel(logging.DEBUG)
        self.decLoggerFh.setLevel(logging.DEBUG)
        self.jsonLoggerFh.setLevel(logging.DEBUG)
        self.loggerFh.setLevel(logging.DEBUG)
        # set the format
        self.simpleFormatter = logging.Formatter(self.SIMPLE_FORMAT)
        self.fullFormatter = logging.Formatter(self.FULL_FORMAT)
        self.consoleLogger.setFormatter(self.fullFormatter)
        self.hexLoggerFh.setFormatter(self.fullFormatter)
        self.decLoggerFh.setFormatter(self.fullFormatter)
        self.jsonLoggerFh.setFormatter(self.simpleFormatter)
        self.loggerFh.setFormatter(self.fullFormatter)
        # add handler to logging
        self.hexLogger.addHandler(self.hexLoggerFh)
        self.hexLogger.addHandler(self.consoleLogger)
        self.decLogger.addHandler(self.decLoggerFh)
        self.decLogger.addHandler(self.consoleLogger)
        self.jsonLogger.addHandler(self.jsonLoggerFh)
        self.logger.addHandler(self.loggerFh)
        self.logger.addHandler(self.consoleLogger)
        # Probably don't want a ton of json being output to console
        # self.jsonLogger.addHandler(self.consoleLogger)

    def logHexMessage(self, message, simple = False):
        # return #kluge

        """Logs a list of data in hexadecimal format."""
        if simple:
            self.consoleLogger.setFormatter(self.simpleFormatter)
            self.hexLoggerFh.setFormatter(self.simpleFormatter)
        byteList = bytearray(message)
        log = ''
        for b in byteList:
            out = format(b, '02x')
            log += out
            log += ' '
        self.hexLogger.debug(log)
        if simple:
            self.consoleLogger.setFormatter(self.fullFormatter)
            self.hexLoggerFh.setFormatter(self.fullFormatter)
            
    def logDecMessage(self, message, simple = False):
        # return #kluge

        """Logs a list of data in decimal format."""
        if simple:
            self.consoleLogger.setFormatter(self.simpleFormatter)
            self.decLoggerFh.setFormatter(self.simpleFormatter)
        byteList = bytearray(message)
        log = ''
        for b in byteList:
            log += str(b)
            log += ' '
        self.decLogger.debug(log)
        if simple:
            self.consoleLogger.setFormatter(self.fullFormatter)
            self.decLoggerFh.setFormatter(self.fullFormatter)
    
    def logJSONMessage(self, message):
        # return #kluge

        """Logs an Element in JSON form."""
        jsonLog = message.toJSON(True)
        self.jsonLogger.debug(jsonLog)

    def logString(self, string: str, simple=False):
        # return #kluge

        if simple:
            self.consoleLogger.setFormatter(self.simpleFormatter)
            self.loggerFh.setFormatter(self.simpleFormatter)
        self.logger.debug(string)
        if simple:
            self.consoleLogger.setFormatter(self.fullFormatter)
            self.loggerFh.setFormatter(self.fullFormatter)

        

# A central log to handle logging - can be accessed from other files/packages.
mainLog = CRAMLog()

def main():
    nums = [ 230, 47, 63, 2, 162 ]
    mainLog.logHexMessage(nums)
    mainLog.logDecMessage(nums)
    mainLog.logString('Hi!')
    mainLog.logString('yo!')


if __name__ == "__main__":main()
        