"""
This file demonstrates the logging of data received from Azure,data send to Azure and the errors
while executing the code.
"""
from datetime import datetime
import logging
import os
import Queue as queue

from logging.handlers import RotatingFileHandler
from sys import getsizeof

from general_configurations import BASE_DIR, NO_OF_LOG_FILES,  FILE_SIZE, WRITE_MODE, FOLDER_NAME

class Datalogs(object):
    """
    This class consist of function which write the error logs to a file by specifying the filename
    and message to be written.
    """
    __instance = None
    @staticmethod
    def get_instance():
        """
        Description:creates a single instance of a class
        Input Parameters:None
        Output Type:object
        """
        if Datalogs.__instance is None:
            Datalogs()
        return Datalogs.__instance
    def __init__(self):
        if Datalogs.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Datalogs.__instance = self

    @classmethod
    def errorlog(cls, filename, level=logging.DEBUG):
        """
        Description: Returns the logger object
        Input Parameters: filename,level of logging
        Output Type: object
        """
        logger = logging.getLogger()
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler = RotatingFileHandler(
            os.path.join(BASE_DIR, FOLDER_NAME , filename),
            maxBytes=FILE_SIZE,
            mode= "w",
            backupCount=NO_OF_LOG_FILES,
        )
        # path = os.path.join(BASE_DIR, Folder_name, filename)
        # ti_c = os.path.getctime(path)
        # file_handler.doRollover()
        file_handler.setFormatter(formatter)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(file_handler)
        return logger

    def log_message(self,deviceid):
        """
        Description:
        Input Parameters: deviceid
        Output Type: string
        """
        write_time = datetime.now()
        error_message = f"This file is created on {write_time} for the device with deviceid {deviceid}"
        return error_message

    def logging_error(self, data, filename, loglevel, deviceid):
        """
        Description: Write the log to the spectific file
        Input Parameters: Data to be written, filename, loglevel
        Output Type: None
        """
        logging_error = self.errorlog(filename)
        if os.stat(os.path.join(BASE_DIR, FOLDER_NAME , filename)).st_size == 0 or ((os.stat(
            os.path.join(BASE_DIR, FOLDER_NAME , filename)).st_size) + getsizeof(data)) > 500:
            message = self.log_message(deviceid)
            logging.info(message)
            # file1 = open(os.path.join(BASE_DIR, FOLDER_NAME , filename) , "w", encoding = "utf-8")
            # file1.write(message)
        if loglevel == logging.DEBUG:
            logging_error.debug(data)
        elif loglevel == logging.INFO:
            logging_error.info(data)
        elif loglevel == logging.WARNING:
            logging_error.exception(data)
        elif loglevel == logging.ERROR:
            logging_error.exception(data)
        else:
            logging_error.critical(data)

Datalogs().logging_error("hellooooooooo.","GFG.log",10,101)
