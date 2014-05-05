# -*- coding: utf-8 -*-
"""constants.py: messages extends"""

#if level for messages is 11 to don't show debug messages,
#then debug persistent and debug sticky don't show
from __future__ import unicode_literals


DEBUG = 10
INFO = 20
SUCCESS = 25
WARNING = 30
ERROR = 40

DEBUG_PERSISTENT = 8
INFO_PERSISTENT = 18
SUCCESS_PERSISTENT = 23
WARNING_PERSISTENT = 28
ERROR_PERSISTENT = 38

DEBUG_STICKY = 7
INFO_STICKY = 17
SUCCESS_STICKY = 22
WARNING_STICKY = 27
ERROR_STICKY = 37

DEFAULT_TAGS = {
    DEBUG_PERSISTENT: 'debug persistent',
    INFO_PERSISTENT: 'info persistent',
    SUCCESS_PERSISTENT: 'success persistent',
    WARNING_PERSISTENT: 'warning persistent',
    ERROR_PERSISTENT: 'error persistent',

    DEBUG_STICKY: 'debug sticky',
    INFO_STICKY: 'info sticky',
    SUCCESS_STICKY: 'success sticky',
    WARNING_STICKY: 'warning sticky',
    ERROR_STICKY: 'error sticky',

}

PERSISTENT_MESSAGE_LEVELS = (
    DEBUG_PERSISTENT, INFO_PERSISTENT, SUCCESS_PERSISTENT, WARNING_PERSISTENT, ERROR_PERSISTENT
)
STICKY_MESSAGE_LEVELS = (
    DEBUG_STICKY, INFO_STICKY, SUCCESS_STICKY, WARNING_STICKY, ERROR_STICKY
    )
