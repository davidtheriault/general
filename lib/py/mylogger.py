#!/usr/bin/env python

# 2010-04
# written by David Theriault
# Logging Class
# Prints to Console and to logfile, also catches
# uncaught exceptions and logs them before exiting.

# Python Modules.
import logging
import os
import sys
from pathlib import Path

class MyLogger(logging.Logger):
    """Generic Logging class"""
    DEFAULT_LOGFILE = str(Path.home()) + '/log/logger.log'

    def __init__(self, log_file=None, level="INFO", print_console=True, label="Uncaught Exception"):
        """Establishing writing to a logfile and to the console"""
        # Below is new style for extending class, won't work with old python.
        #super(MyLogger, self).__init__(label, level)
        level=level.upper()
        logging.Logger.__init__(self, label, level)
        log_file = log_file or self.DEFAULT_LOGFILE
        path, logfile = os.path.split(log_file)
        if(path and not os.path.exists(path)):
            print("warning: logfile path:%s not found\ncreating directory..." % path,)
            os.makedirs(path)
            print("  directory created.")
        LEVELS = {
          'DEBUG': logging.DEBUG,
          'INFO': logging.INFO,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR,
          'CRITICAL': logging.CRITICAL}
        # Carry through command line debugging.
        if(level not in LEVELS.keys()):
            print("Error level %s is not defined, must be one of:%s, setting to level info." % (level, str(LEVELS.keys())))
            level="INFO"
        self.name = label
        self.setLevel(LEVELS[level])
        # create file handler for loggings
        fh = logging.FileHandler(log_file)
        fh.setLevel(LEVELS[level])
        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(LEVELS[level])
        # create formatter and add it to the handlers
        # If we ever upgrade to python 2.5 can use the below logging to display the function name.
        formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(funcName)s|%(lineno)d|%(message)s", "%Y-%m-%d %H:%M:%S" )
        #log_formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(filename)s|%(lineno)d|%(message)s", "%Y-%m-%d %H:%M:%S" )
        #cons_formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(filename)s|%(message)s", "%Y-%m-%d %H:%M:%S" )
        log_formatter = formatter
        cons_formatter = logging.Formatter("%(lineno)d:%(message)s")
    
        ch.setFormatter(cons_formatter)
        fh.setFormatter(log_formatter)
        # add the handlers to logger
        # Option to skip console output.
        if(print_console):
            self.addHandler(ch)
        self.addHandler(fh)
        self.debug("logging init complete, logging to file %s" % log_file)
        sys.excepthook = self.excepthook

    def closeLogs(self):
        """Close any and all logging handles"""
        self.debug("closing logfile handlers")
        for handle in self.handlers:
            handle.close()

    def excepthook(self, *args):
        """Remap uncaught exceptions and print to the main logger if defined, otherwise
        make a new logger and print it out there.
        """

        if(self.handlers):
            self.error("Uncaught Exception:", exc_info=args)
            self.closeLogs()
        else:
            print("Uncaught Exception:%s" % str(args))



