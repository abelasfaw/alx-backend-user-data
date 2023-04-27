#!/usr/bin/env python3
'''obfuscated log message'''
import re
import os
import logging
import mysql.connector
from typing import List
from mysql.connector import MySQLConnection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''constructor to create new instance'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''returns obfuscated log records'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object'''
    logger = logging.getLogger("user_data")
    logging.progagate = False
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''returns a log message with obfuscated fields'''
    for field in fields:
        message = re.sub('{}=(.*?){}'.format(field, separator),
                         '{}={}{}'.format(field, redaction, separator),
                         message)
    return message


def get_db() -> MySQLConnection:
    '''returns connector to Database'''
    return mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", 'root'),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ''),
        host=os.getenv("PERSONAL_DATA_DB_HOST", 'localhost'),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
