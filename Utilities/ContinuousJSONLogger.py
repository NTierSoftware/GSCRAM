# Alex Erf, Airspace, alex.erf@airspace.co
# Date Created: 8/21/18

import json, os
from typing import Any, TextIO
#TODO PURGE/CLEAR/ROTATE logs dir
class ContinuousJSONLogger:
    """This class is used to log an array of json objects on the fly."""

    def __init__(self, file: TextIO):
        self.file = file
        self.file.write('[\n]')
        self.firstWritten = False
        self.rewind()

    def log(self, obj: Any):
        if self.firstWritten: self.file.write(',')
        self.file.write('\n')
        self.file.write(json.dumps(obj, indent=4, separators=(',', ': ')))
        self.file.write('\n]')
        self.rewind()
        self.firstWritten = True

    def rewind(self): self.file.seek(self.file.tell() - 3, os.SEEK_SET)

