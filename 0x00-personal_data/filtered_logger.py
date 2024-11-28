#!/usr/bin/env python3
""""0. Regex-ing"""
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """a function called filter_datum that returns the
    log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=" + ".*?" + separator,
                         field + "=" + redaction + separator,
                         message)
    return message


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
        """a function called format that returns the
        log message obfuscated"""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg,
                            self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """a function called get_logger that takes no arguments"""
    # logger = logging.getLogger('user_data', propagate=False,
    #                            setLevel=logging.INFO)
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """a function called get_db that takes no arguments"""
    db = mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    )
    return db


# task 4
def main() -> None:
    """a function called main that takes no arguments"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        msg = "name=" + row[0] + ";email=" + row[1] +\
                ";phone=" + row[2] + ";ssn=" + row[3] +\
                ";password=" + row[4] + ";ip=" + row[5] +\
                ";last_login=" + str(row[6]) +\
                ";user_agent=" + row[7] + ";"

        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
