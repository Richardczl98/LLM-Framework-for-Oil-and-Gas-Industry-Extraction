"""
Author: Alex <alex.hu@57blocks.com>
Date Created: 2023-10-19
Description: Exception file.
"""

import json

RESULT_FORMAT_ERROR = -10001  # like mentioned->'1' but mentioned-> '1 1'
RESULT_ERROR = -10002  # Unhandled Error
RESPONSE_FORMAT_ERROR = -10003
RESPONSE_COLON_ERROR = -10004
RESPONSE_MISSING_VARIABLE_ERROR = -10005


ERR_MSG = {
    RESULT_FORMAT_ERROR: 'RESULT FORMAT ERROR',
    RESULT_ERROR:  'UNHANDLED ERROR',
    RESPONSE_FORMAT_ERROR: 'FORMAT ERROR',
    RESPONSE_COLON_ERROR: 'RESPONSE COLON ERROR',
    RESPONSE_MISSING_VARIABLE_ERROR: 'RESPONSE MISSING VARIABLE ERROR',
}


class ParserException(Exception):

    def __init__(self, code=RESULT_FORMAT_ERROR, payload=None, cls_name=''):
        Exception.__init__(self)
        self.code = code
        self.payload = payload
        self.call_cls = cls_name

    def to_dict(self):
        rv = dict(self.payload or ())

        rv['code'] = self.code

        rv['message'] = ERR_MSG[self.code]

        rv['class_name'] = self.call_cls

        return rv

    def __str__(self):
        return json.dumps(self.to_dict())
