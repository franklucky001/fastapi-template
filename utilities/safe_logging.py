from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from logging import FileHandler
import time
import os


class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(self, *args, **kwargs):
        super(SafeTimedRotatingFileHandler, self).__init__(*args, **kwargs)
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.
        Always check time
        """
        try:
            if self.check_base_filename():
                self.build_base_filename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_base_filename(self):
        """
        Determine if builder should occur.
        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        time_check = self.suffix_time != time.strftime(self.suffix, timeTuple)
        file_check = os.path.exists(self.baseFilename + "." + self.suffix_time)
        return time_check or not file_check

    def build_base_filename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = "a"
        if not self.delay:
            self.stream = self._open()


class SafeRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super(SafeRotatingFileHandler, self).__init__(*args, **kwargs)
        self.suffix = "%Y-%m-%d_%H-%M-%S"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.
        Always check time
        """
        try:
            if self.check_base_filename(record):
                self.build_base_filename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_base_filename(self, record):
        """
        Determine if builder should occur.
        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        if self.suffix_time == "":
            return True
        timeTuple = time.localtime()
        time_check = self.suffix_time != time.strftime(self.suffix, timeTuple)
        file_check = not os.path.exists(self.baseFilename + "." + self.suffix_time)
        return (time_check or file_check) and self.shouldRollover(record)

    def build_base_filename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = "a"
        if not self.delay:
            self.stream = self._open()
