import logging
class LoggerDemo:
    def sample_logger(self):
        logger =logging.getLogger("demolog")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.addHandler(formatter)