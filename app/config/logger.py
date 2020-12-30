"""Custom logger module."""

import logging
import os
import datetime
import sys
from logging.handlers import RotatingFileHandler

class LogConfig:
    LOGGER_NAME = "app_logger"
    LOG_FOLDER = 'logs'
    LOG_BASE_PATH = f".{os.sep}{LOG_FOLDER}"
    FILE_MAX_BYTES = 50 * 1024 * 1024

    @staticmethod
    def get_logger():
        return logging.getLogger(LogConfig.LOGGER_NAME)

    @staticmethod
    def logger_init(log_base_dir=None):
        if log_base_dir is not None:
            LogConfig.LOG_BASE_PATH = f"{log_base_dir}{os.sep}{LogConfig.LOG_FOLDER}"

        if not os.path.exists(LogConfig.LOG_BASE_PATH):
            os.makedirs(LogConfig.LOG_BASE_PATH)

        logger = logging.getLogger(LogConfig.LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        fh = DayRotatingFileHandler('pmsp', LogConfig.LOG_BASE_PATH, maxBytes=LogConfig.FILE_MAX_BYTES,
                                    backupCount=100, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        chErr = logging.StreamHandler(sys.stderr)
        chErr.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s - [%(funcName)s()]")

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        chErr.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        #logger.addHandler(chErr)


class DayRotatingFileHandler(RotatingFileHandler):
    _logName = ""
    _FILE_INDEX = 0

    def __init__(self, name, logFolderPath, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False):
        self._logName = name
        self._logFolderPath = logFolderPath
        # 因為log是用當日日期, 檢查是否當天已經有log,有的話則將檔名的index往上加
        self.set_file_index(self._logName)
        filename = self._logFolderPath + os.sep + self.day_prefix_filename(self._logName)
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)

    def doRollover(self):
        basefilename_list = self.baseFilename.split(os.sep)
        basefilename_list[-1] = self.day_prefix_filename(self._logName)
        self.baseFilename = f'{os.sep}'.join(basefilename_list)
        super().doRollover()

    def set_file_index(self, name):
        for i in range(1000):
            self._FILE_INDEX = i
            if os.path.exists(self._logFolderPath + os.sep + self.day_prefix_filename(name)):
                continue
            else:
                return

        print('Failed to start logging, STOP SERVER!!!')
        exit(0)

    def day_prefix_filename(self, name):
        return '{0}-{1}-{2}.log'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d'), name, self._FILE_INDEX)


