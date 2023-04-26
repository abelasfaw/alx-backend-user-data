#!/usr/bin/env python3
'''obfuscated log message'''
import re


def filter_datum(fields, redaction, message, separator):
    '''returns a log message with obfuscated fields'''
    for field in fields:
        message = re.sub('{}=(.*?){}'.format(field, separator),
                         '{}={}{}'.format(field, redaction, separator),
                         message)
    return message
