import logging

class Logger:
    """A logger, which directs its output into a specified file"""

    def __init__(self,filename):

        self.logger = logging.getLogger(__name__)
        self.formatter = logging.Formatter('%(message)s')
        self.file_handler = logging.FileHandler(filename)
        self.stream_handler = logging.StreamHandler()

        # getting level
        self.logger.setLevel(logging.DEBUG)

         # handling log file
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)

        # handling output to console
        self.stream_handler.setFormatter(self.formatter)

        # combining logger and handlers
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def log(self,message):
        self.logger.debug(message)