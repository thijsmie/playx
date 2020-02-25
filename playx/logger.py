
from pathlib import Path
import datetime
import os
import inspect


class Logger:
    """
        Custom logger that meets the requirements of using multiple logging setup.
    """
    _instances = []

    def __init__(
            self,
            name,
            level='INFO',
            disable_file=False
    ):
        self.name = name
        self._file_format = ''
        self._console_format = ''
        self._log_file = Path('~/.playx/logs/log.cat').expanduser()
        self._check_logfile()
        self._level_number = {
                                'DEBUG': 0,
                                'INFO': 1,
                                'WARNING': 2,
                                'ERROR': 3,
                                'CRITICAL': 4
                             }
        self.level = self._level_number[level]
        self._disable_file = disable_file
        self._instances.append(self)

    def _check_logfile(self):
        """
        Check if the passed logfile path is present.
        If not present then create it.
        """
        if not self._log_file.exists():
            if not self._log_file.parent.exists():
                os.makedirs(self._log_file.parent)
            f = open(self._log_file, 'w')
            f.close()

    def _write_file(self):
        """Write to the file regardless of the LEVEL_NUMBER."""
        if self._disable_file:
            return

        with open(self._log_file, 'a') as f:
            # The file log is to be written to the _log_file file
            f = open(self._log_file, 'a')
            f.write(self._file_format)

    def _write(self, message, LEVEL_NUMBER):
        """
            Write the logs.

            LEVEL_NUMBER is the levelnumber of the level that is calling the
            _write function.
        """
        self._make_format(message)
        self._write_file()
        if LEVEL_NUMBER >= self.level:
            print(self._console_format)

    def _make_format(self, message):
        """
        Make the format of the string that is to be written.
        """
        t = datetime.datetime.now()
        DATETIME_FORMAT = '{}-{}-{} {}:{}:{}'.format(
                                t.year,
                                t.month,
                                t.day,
                                t.hour,
                                t.minute,
                                t.second
                              )
        self._console_format = '[{}]: {}'.format(self.name, message)
        self._file_format = '[{}]-[{}]: {}\n'.format(self.name, DATETIME_FORMAT, message)

    def update_level(self, level):
        """
        Update all the instances of the class with the passed
        level.
        """
        for instance in Logger._instances:
            instance.level = self._level_number[level]

    def hold(self):
        """
        Hold the screen by using input()
        """
        LEVEL_NUMBER = 0

        if LEVEL_NUMBER >= self.level:
            input("Screen hold! Press any key to continue")

    def debug(self, message):
        """
        Add the message if the level is debug.
        """
        LEVEL_NUMBER = 0
        self._write(message, LEVEL_NUMBER)

    def info(self, message):
        """
        Add the message if the level is info or less.
        """
        LEVEL_NUMBER = 1
        self._write(message, LEVEL_NUMBER)

    def warning(self, message):
        """
        Add the message if the level is warning or less.
        """
        LEVEL_NUMBER = 2
        self._write(message, LEVEL_NUMBER)

    def error(self, message):
        """
        Add the message if the level is error or less.
        """
        LEVEL_NUMBER = 3
        self._write(message, LEVEL_NUMBER)

    def critical(self, message):
        """
        Add the message if the level is critical or less.
        """
        LEVEL_NUMBER = 4
        self._write(message, LEVEL_NUMBER)
        exit()


class LoggerB:
    instance = None
    is_init = False
    args = {
        "level": None,
        "disable_file": None,
        "name": None
    }

    def __init__(
            self,
            name='',
            level='INFO',
            disable_file=False
    ):
        if not Logger.is_init:
            Logger.is_init = True
            Logger.args["level"] = level
            Logger.args["disable_file"] = disable_file
            Logger.args["name"] = name

        Logger.instance = LoggerBase(name, Logger.args["level"], Logger.args["disable_file"])
        # if not Logger.instance:
        #    Logger.instance = LoggerBase(inspect.stack()[1], level, disable_file)

    def __getattr__(self, name):
        return getattr(self.instance, name)
