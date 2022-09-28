"""
This file demonstrates the logging of data received from Azure,data send to Azure and the errors 
while executing the code.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from general_configurations import BASE_DIR, Folder_name, No_of_log_files, file_size, write_mode

# formatter = logging.Formatter('%(asctime)s %(levelname)s %(loglevel)s %(message)s')

class Datalogs(object):
    """
    This class consist of function which write the error logs to a file by specifying the filename
    and message to be written.
    """
    __instance = None
    @staticmethod
    def get_instance():
        if Datalogs.__instance == None:
             Datalogs()
        return Datalogs.__instance
    def __init__(self):
        if Datalogs.__instance != None:
             raise Exception("This class is a singleton!")
        else:
            Datalogs.__instance = self

    @classmethod
    def errorlog(cls, filename, level=logging.DEBUG):
        logger = logging.getLogger()
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler = RotatingFileHandler(
            os.path.join(BASE_DIR, Folder_name, filename),
            maxBytes=file_size,
            mode= write_mode,
            backupCount=No_of_log_files,
        )
        # file_handler_1 = HeaderFileHandler_1(os.path.join(BASE_DIR, Folder_name, filename),
        #     maxBytes=file_size,
        #     mode= write_mode,
        #     backupCount=No_of_log_files,
        # )
        # print(file_handler_1)
        # path = os.path.join(BASE_DIR, Folder_name, filename)
        # ti_c = os.path.getctime(path)
        file_handler.setFormatter(formatter)
        if (logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(file_handler)
        # print(f"The file located at the path {path} was created at {ti_c}")
        return logger

    def logging_error(self, data, filename, loglevel):
        logging_error = self.errorlog(filename)
        if loglevel == logging.DEBUG:
            logging_error.exception(data)
        elif loglevel == logging.INFO:
            logging_error.info(data)
        elif loglevel == logging.WARNING:
            logging_error.exception(data)
        elif loglevel == logging.ERROR:
            logging_error.exception(data)
        else:
            logging_error.critical(data)

# class HeaderFileHandler_1(RotatingFileHandler):
#     def _open(self):
#         print("lllll")
#         # RotatingFileHandler(
#         #     os.path.join(BASE_DIR, Folder_name, "CID.log"),
#         #     maxBytes=file_size,
#         #     mode= write_mode,
#         #     backupCount=No_of_log_files)
#         open_func = self._builtin_open
#         print(self.baseFilename)
#         # new_log = not os.path.exists(self.get_name)
#         print(self.rotation_filename)
#         # print("new_log",new_log)
#         f = open_func(self.baseFilename, self.mode,
#                          encoding=self.encoding, errors=self.errors)
#         if os.path.exists(self.baseFilename):
#             print("kk")
#             # f.write(f"Log created on {date.today()}\n")
#             f.write("Log created on ")
#         else:
#             print("pppp")
#         return f
    
Datalogs().logging_error("hello","svvvve.log",20)