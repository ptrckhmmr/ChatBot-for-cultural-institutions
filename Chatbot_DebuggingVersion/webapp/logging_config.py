"""
This module contains a class whose instance logs all the input und the chatbot's response
"""

import logging

class Logger:
    """A logger object, which directs its output into a specified file"""

    def __init__(self,filename):
        """
        This function creates a logger object with predefined formats and streams

        Input:
            filename: string var which describes the name of the file the logging should be done into

        Returns:
            Nothing.
        """

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
        """
        This function logs the in- and output

        Input:
            message: string var which represents the message to be logged

        Returns:
            Nothing.
        """
        self.logger.debug(message)