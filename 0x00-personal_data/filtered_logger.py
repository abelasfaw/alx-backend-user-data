#!/usr/bin/env python3
'''obfuscated log message'''
import re
from typing import List


import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''returns obfuscated log records'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''returns a log message with obfuscated fields'''
    for field in fields:
        message = re.sub('{}=(.*?){}'.format(field, separator),
                         '{}={}{}'.format(field, redaction, separator),
                         message)
    return message
