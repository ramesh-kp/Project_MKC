# """
# This file demonstrates the logging of data received from Azure,data send to Azure and the errors
# while executing the code.
# """
# import logging
# import os
# from logging.handlers import RotatingFileHandler
# import time

# from general_configurations import BASE_DIR, DEVICE_INFO, FILE_CREATED_AT, HEADER_1, HEADER_2
# from general_configurations import WRITE_MODE, FOLDER_NAME,LOG_WRITTEN, NEW_LINE
# from general_configurations import NO_OF_LOG_FILES,  FILE_SIZE

# class Datalogs(object):
#     """
#     This class consist of function which write the error logs to a file by specifying the filename
#     and message to be written.
#     """
#     __instance = None
#     @staticmethod
#     def get_instance():
#         """
#         Description:creates a single instance of a class
#         Input Parameters:None
#         Output Type:object
#         """
#         if Datalogs.__instance is None:
#             Datalogs()
#         return Datalogs.__instance
#     def __init__(self):
#         if Datalogs.__instance is not None:
#             raise Exception("This class is a singleton!")
#         else:
#             Datalogs.__instance = self

#     def create_string_builder(self,filename, deviceid):
#         """
#         Description: Returns the logger object
#         Input Parameters: filename,level of logging
#         Output Type: object
#         """
#         constant_1 = HEADER_1
#         get_created_time = str(time.asctime())
#         get_file_name = filename
#         constant_2 = HEADER_2
#         # print(constant_1 + '\n' + "File created at " + get_created_time + '\n' +
#         #         "Log is written to " + get_file_name + " for the deviceid " +
#         #         str(deviceid) + '\n' + constant_2)
#         return (NEW_LINE +constant_1 + NEW_LINE + FILE_CREATED_AT + get_created_time + NEW_LINE +
#                 LOG_WRITTEN + get_file_name + DEVICE_INFO +
#                 str(deviceid) + NEW_LINE + constant_2 + NEW_LINE)

#     def errorlog(self, filename, level=logging.DEBUG):
#         """
#         Description: Returns the logger object
#         Input Parameters: filename,level of logging
#         Output Type: object
#         """
#         logger = logging.getLogger(__name__)
#         logger.setLevel(level)
#         formatter = logging.Formatter(
#             "%(asctime)s - %(levelname)s - %(message)s"
#         )
#         # needroll = os.path.isfile(os.path.join(BASE_DIR, FOLDER_NAME , filename))
#         file_handler = Logerrors(
#             os.path.join(BASE_DIR, FOLDER_NAME , filename),
#             maxBytes=FILE_SIZE,
#             mode= WRITE_MODE,
#             backupCount=NO_OF_LOG_FILES,delay=True
#         )
#         file_handler.setFormatter(formatter)
#         if logger.hasHandlers():
#             logger.handlers.clear()
#         logger.addHandler(file_handler)
#         # if needroll:
#         #     logger.handlers[0].doRollover()
#         # logger.info(self.create_string_builder(filename, deviceid))
#         return logger

#     def logging_error(self, data, filename, loglevel, deviceid):
#         """
#         Description: Write the log to the spectific file
#         Input Parameters: Data to be written, filename, loglevel
#         Output Type: None
#         """
#         logging_error = self.errorlog(filename,deviceid)

#         if loglevel == logging.DEBUG:
#             logging_error.debug(data)
#         elif loglevel == logging.INFO:
#             logging_error.info(data)
#         elif loglevel == logging.WARNING:
#             logging_error.exception(data)
#         elif loglevel == logging.ERROR:
#             logging_error.exception(data)
#         else:
#             logging_error.critical(data)



# class Logerrors(RotatingFileHandler):
#     flag = False
#     def doRollover(self):
#         """
#         Do a rollover, as described in __init__().
#         """
#         if self.stream:
#             self.stream.close()
#             self.stream = None
#         if self.backupCount > 0:
#             for i in range(self.backupCount - 1, 0, -1):
#                 sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
#                 dfn = self.rotation_filename("%s.%d" % (self.baseFilename,
#                                                         i + 1))
#                 if os.path.exists(sfn):
#                     if os.path.exists(dfn):
#                         os.remove(dfn)
#                     os.rename(sfn, dfn)
#             dfn = self.rotation_filename(self.baseFilename + ".1")
#             if os.path.exists(dfn):
#                 os.remove(dfn)
#             self.rotate(self.baseFilename, dfn)
#         if  self.delay:
#             self.stream = self._open()
#             self.stream.write(Datalogs.get_instance().create_string_builder("examplefilelog.log",110))

#     def shouldRollover(self, record):
#         """
#         Determine if rollover should occur.

#         Basically, see if the supplied record would cause the file to exceed
#         the size limit we have.
#         """
#         # print("self.stream.tell() + len(msg)",self.stream.tell())
#         if self.stream is None:                 # delay was set...
#             self.stream = self._open()
#             if self.stream.tell() == 0:
#                 self.stream.write(Datalogs.get_instance().create_string_builder("examplefilelog.log",110))
#         if self.maxBytes > 0:                   # are we rolling over?
#             msg = "%s\n" % self.format(record)
#             self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
#             if self.stream.tell() + len(msg) >= self.maxBytes:
#                 self.flag = True
#                 return 1
#         return 0

# Datalogs().logging_error("Hello","examplefilelog.log", 101, 20)


"""
This file demonstrates the logging of data received from Azure,data send to Azure and the errors
while executing the code.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
import time

from general_configurations import BASE_DIR, DEVICE_INFO, FILE_CREATED_AT, HEADER_1, HEADER_2
from general_configurations import WRITE_MODE, FOLDER_NAME,LOG_WRITTEN, NEW_LINE
from general_configurations import NO_OF_LOG_FILES,  FILE_SIZE

class Datalogs(object):
    """
    This class consist of function which write the error logs to a file by specifying the filename
    and message to be written.
    """
    filename = None
    deviceid = None
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

    def create_string_builder(self,filename, deviceid):
        """
        Description: Returns the logger object
        Input Parameters: filename,level of logging
        Output Type: object
        """
        constant_1 = HEADER_1
        get_created_time = str(time.asctime())
        get_file_name = filename
        constant_2 = HEADER_2
        # print(constant_1 + '\n' + "File created at " + get_created_time + '\n' +
        #         "Log is written to " + get_file_name + " for the deviceid " +
        #         str(deviceid) + '\n' + constant_2)
        return (NEW_LINE +constant_1 + NEW_LINE + FILE_CREATED_AT + get_created_time + NEW_LINE +
                LOG_WRITTEN + get_file_name + DEVICE_INFO +
                str(deviceid) + NEW_LINE + constant_2 + NEW_LINE)

    def errorlog(self, filename, level=logging.DEBUG):
        """
        Description: Returns the logger object
        Input Parameters: filename,level of logging
        Output Type: object
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        # needroll = os.path.isfile(os.path.join(BASE_DIR, FOLDER_NAME , filename))
        file_handler = Logerrors(
            os.path.join(BASE_DIR, FOLDER_NAME , filename),
            maxBytes=FILE_SIZE,
            mode= WRITE_MODE,
            backupCount=NO_OF_LOG_FILES,delay=True
        )
        file_handler.setFormatter(formatter)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(file_handler)
        # if needroll:
        #     logger.handlers[0].doRollover()
        # logger.info(self.create_string_builder(filename, deviceid))
        return logger

    def logging_error(self, data, filename, loglevel, deviceid):
        """
        Description: Write the log to the spectific file
        Input Parameters: Data to be written, filename, loglevel
        Output Type: None
        """
        logging_error = self.errorlog(filename,deviceid)

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



class Logerrors(RotatingFileHandler):
    flag = False
    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d" % (self.baseFilename,
                                                        i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1")
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if  self.delay:
            self.stream = self._open()
            self.stream.write(Datalogs.get_instance().create_string_builder(Datalogs.get_instance().filename, Datalogs.get_instance().deviceid))

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        # print("self.stream.tell() + len(msg)",self.stream.tell())
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
            if self.stream.tell() == 0:
                self.stream.write(Datalogs.get_instance().create_string_builder(Datalogs.get_instance().filename, Datalogs.get_instance().deviceid))
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                self.flag = True
                return 1
        return 0

Datalogs().logging_error("Hello","exfilelog.log", 20, 110)

