# -*- coding: utf-8 -*-
"""admin.py: messages extends"""

__author__ = 'ali'

class LevelOfMessageException(Exception):

    def __init__(self, *args, **kwargs):
        super(LevelOfMessageException, self).__init__(*args, **kwargs)

    def __str__(self):
        return "The level of the message, can't be proccess by this storage"
