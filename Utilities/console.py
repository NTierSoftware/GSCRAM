# https://stackoverflow.com/questions/19479504/how-can-i-open-two-consoles-from-a-single-script
import sys, time, logging, traceback, errno, threading
from datetime import datetime
from subprocess import CREATE_NEW_CONSOLE, PIPE, Popen

class console(Popen)  :
    RED = "C0"
    GREEN = "A0"
    BLUE = "B0"
    TELEMETRY = "89"
    DEBUG = "70"
    NETWORK = "0F"

    consoleNames = {
        DEBUG: '',
        NETWORK: 'Network thread',
        TELEMETRY: 'Target/Interceptor telemetry and Events'
    }

    Registry = {}

    LOGFILE = "console.log"
    LOGDIR = '\\GSCRAM\logs\\'
    SIMPLE_FORMAT = '%(message)s'

    def __init__(self, color=None, title=None):
        self.color = color
        self.title = title
        cmd = "import sys, os, locale"
        cmd += "\nos.system(\'color " + color + "\')" if color is not None else ""
        title = title if title is not None else "console #" + str(console.NumConsoles)
        cmd += "\nos.system(\"title " + title + "\")"
        # poor man's `cat`
        cmd += """
#print(sys.stdout.encoding, locale.getpreferredencoding() )
localEncoding = locale.getpreferredencoding()
for line in sys.stdin:
    sys.stdout.buffer.write(line.encode(localEncoding))
    sys.stdout.flush()
"""
        cmd = sys.executable, "-c", cmd
        # cmd = sys.executable, "\GSCRAM\src\Utilities\consoleScript.py"
        # print(cmd, end="", flush=True)
        super().__init__(cmd, stdin=PIPE, bufsize=1, universal_newlines=True, creationflags=CREATE_NEW_CONSOLE,
                         encoding='utf-8')

        self.LogFileName = title.replace(" ", ".").replace("#", ".").replace("/", ".").replace("(", ".").replace(")",
                                                                                                                 ".")

        self.logger = logging.getLogger(self.LogFileName)
        self.logger.setLevel(logging.DEBUG)

        self.OUT_FILE_LOG = console.LOGDIR + self.LogFileName + '.log'
        try:
            self.loggerFh = logging.FileHandler(self.OUT_FILE_LOG, encoding='utf-8')
        except FileNotFoundError:
            print("Console Log Error: could not find directory \GSCRAM\logs - please ensure this directory exists")
            sys.exit()
        self.loggerFh.setFormatter(logging.Formatter(console.SIMPLE_FORMAT))
        self.loggerFh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.loggerFh)

        # console.Registry.append(self) #register self, used in closeAll() class method
        console.Registry[color] = self

        self.shutdown: threading.Event = None

    @classmethod
    def closeAll(cls):
        logging.shutdown()
        for con in cls.Registry.values(): con.terminate()
        cls.Registry.clear()
        print("all consoles shutdown")

    def log(self, msg: str):
        try:
            self.stdin.write( '%s\n' % msg )
            self.stdin.flush()
            self.logger.debug( str(datetime.utcnow()) + ':\t' + msg)
        except OSError as err:
            if err.errno == errno.EINVAL:
                if self.shutdown is not None: self.shutdown.set()
                # print(self.color, self.title + ' console shutdown (or unicode issue)\t', msg)
                return #console has been shutdown, cannot write to stdin
            print("console.log() stdin err:\t", traceback.format_exc(), "msg: ", msg)


    @staticmethod
    def getConsole(name:str=DEBUG) -> 'console':
        try: retVal:console = console.Registry[name]
        except KeyError:
            try: title:str = console.consoleNames[name]
            except KeyError: title = console.consoleNames[name] = name
            retVal = console(color=console.BLUE, title="GSCRAM " + title)
            console.Registry[name] = retVal

        return retVal


    def setShutDownEvent(self, shutdown:threading.Event ):
        self.shutdown:threading.Event = shutdown

debugLog:          console = console(console.DEBUG, title="GSCRAM console (close to restart)")

if __name__ == "__main__":
    myConsole = console(color=console.RED, title="test error")
    myConsole.write("a test red console")
    myConsole.write("UNICODE COMING...")
    time.sleep(2)

    myConsole.write("♥♥♥♥♥♥♥♥")
    NoTitle= console()
    NoTitle.write("default color and title! This answer uses Windows 10")
    NoTitle.write(u"♥♥♥♥♥♥♥♥")
    NoTitle.write("♥")
    time.sleep(5)
    myConsole.terminate()
    NoTitle.write("some more text. Run this at the python console.")
    time.sleep(4)
    NoTitle.terminate()
    time.sleep(5)
