# -*- coding: utf-8 -*-
# Author: Anjing Wang
# Date: Sep-27-2023

"""
Logger Configuration and Logging
"""

import os
import logging
# https://pypi.org/project/python-decouple/
# pip install python-decouple
from decouple import config

this_file_path = os.path.dirname(os.path.realpath(__file__))

class LoggerConfigurer:
    """
    Class to configure the logger.
    We would like to have a convenient way to configure
    especially the log file name.
    """

    def __init__(self):
        """
        Initialize the class.

        This function initializes the class by setting up the logger
        and configuring it with the project name.
        """
        self._logger = logging.getLogger('MyLogger')
        project_name = config('PROJECT', default='opgee')
        default_log = this_file_path + '/../log/' + project_name + '.log'
        self.configure_logger(default_log)

    def configure_logger(self,
                         log_file_full_name: str,
                         console_level = logging.DEBUG,
                         console_format = None):
        """
        Configures the logger's level, logfile name etc.

        Args:
            log_file_full_name (str): The full path of the log file.

        Returns:
            None
        """
        # prevent logging from propagating
        # other wise, logging might be duplicated
        # when it is imported in other files
        self._logger.propagate = False
        # Remove and close all existing handlers
        for handler in self._logger.handlers[:]:
            handler.close()
            self._logger.removeHandler(handler)

        # Set the level of logger
        self._logger.setLevel(logging.DEBUG)

        # make sure the log always ends with .log
        if not log_file_full_name.endswith(".log"):
            log_file_full_name = log_file_full_name + '.log'
        os.makedirs(os.path.dirname(log_file_full_name),
                    exist_ok=True)

        # Handlers setup
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file_full_name)
        console_handler.setLevel(console_level)
        file_handler.setLevel(logging.DEBUG)

        # Formatters setup
        # %(name)s
        # this is the logger name, we do not need to specify as it's the same
        format_str = '%(asctime)s-%(levelname)s-[%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
        formatter = logging.Formatter(format_str)
        if console_format is None:
            console_handler.setFormatter(formatter)
        else:
            console_formatter = logging.Formatter(console_format)
            console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

    @property
    def logger(self):
        """
        Return internal logger as a property.

        :return: The logger property.
        """
        return self._logger


# Create an instance
logger_config_instance = LoggerConfigurer()

# Direct reference to the logger
logger = logger_config_instance.logger


def main():
    """Test the configuration."""
    # DEBUG is the lowest
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    # CRITICAL is the highest
    logger.critical('This is a critical message')


if __name__ == "__main__":
    main()
