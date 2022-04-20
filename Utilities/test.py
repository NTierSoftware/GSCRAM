import sys, time, os, locale
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE

class console(Popen)  :
    NumConsoles = 0
    def __init__(self, color=None, title=None):
        console.NumConsoles += 1

        cmd = "import sys, os, locale"
        cmd += "\nos.system(\'chcp 65001" +  "\')"
        # cmd += "\nos.system(\'set PYTHONIOENCODING=UTF-8" +  "\')"

        cmd += "\nos.system(\'color " + color + "\')" if color is not None else ""
        title = title if title is not None else "console #" + str(console.NumConsoles)
        cmd += "\nos.system(\"title " + title + "\")"
        # poor man's `cat`
        cmd += """
print(sys.stdout.encoding, locale.getpreferredencoding() )
endcoding = locale.getpreferredencoding()
for line in sys.stdin:
    sys.stdout.buffer.write(line.encode(endcoding))
    sys.stdout.flush()
"""

        cmd = sys.executable, "-c", cmd
        # print(cmd, end="", flush=True)
        super().__init__(cmd, stdin=PIPE, bufsize=1, universal_newlines=True, creationflags=CREATE_NEW_CONSOLE, encoding='utf-8')


    def write(self, msg):
        # try:
        #     logMsg:str = (str(datetime.datetime.now()) + ":\t" + msg + "\n")
        #     self.stdin.write(logMsg )
        #     # self.logger.debug(logMsg)
        # # except OSError: pass #Console has been shutdown.
        # except Exception as err:
        #     print("console.write() err:\t", traceback.format_exc(), err)
        #     time.sleep(1)
        self.stdin.write(msg.encode(encoding='utf-8').decode(encoding='utf-8')  )
    # def write(self, msg): self.stdin.write(msg.encode("utf_8") if isinstance(msg, unicode) else msg )


if __name__ == "__main__":
    myConsole = console(color="c0", title="test error console")
    myConsole.write("Thank you jfs. Cool explanation")
    myConsole.write("\ndefault color and title! This answer uses Windows 10\n")
    time.sleep(2)

    myConsole.write(u"\n♥♥♥♥♥♥♥♥\n")
    time.sleep(5)
    NoTitle= console()
    NoTitle.write(u"\n♥\n")
    time.sleep(5)
    myConsole.terminate()
    # NoTitle.write("some more text. Run this at the python console.")
    time.sleep(4)
    NoTitle.terminate()
    time.sleep(5)