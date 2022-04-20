"""@file CfgParse.py
This program contains a the class kvpreader that takes a key input and returns the
value output if one exists for a given configuration file.
"""

import configparser

class CfgFileNotFound(Exception):
    def __init__(self, file_name):
        Exception.__init__(self, 'Cannot find GSCRAM log file: ' + file_name)


class KvpReader:
    def __init__(self, file_name='\\GSCRAM\\GSCRAM.cfg'):
        """Initializes the reader for the specified filename. :param file_name:
        A string of the filename including the file type (i.e. .ini, .cfg, .yaml, etc.) """

        # initialize the imported configparser class and read the file
        self.config = configparser.ConfigParser()
        self.file_read = self.config.read(file_name)
        if len(self.file_read) < 1: raise CfgFileNotFound(file_name)
        self.CONFIGFILE = file_name

    def getvalue(self, key_name, section_name = 'DEFAULT'):
        """Returns the value for the given key and section.

        :param key_name: A string of the desired key.
        :param section_name: A string for the section of the desired key. If no
        section is given, equals 'DEFAULT'.
        """

        # Find the value from the file
        self.value = self.config[section_name][key_name]

        return self.value
