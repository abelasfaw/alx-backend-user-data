#!/usr/bin/env python3
'''obfuscated log message'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''returns a log message with obfuscated fields'''
    for field in fields:
        message = re.sub('{}=(.*?){}'.format(field, separator),
                         '{}={}{}'.format(field, redaction, separator),
                         message)
    return message
