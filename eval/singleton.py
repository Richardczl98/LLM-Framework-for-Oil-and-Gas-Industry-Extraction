"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: singleton class.
"""

import abc

class Singleton(abc.ABCMeta, type):
    ''' Singleton metaclass ensure only one instance of a class '''

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


