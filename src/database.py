import os
from collections.abc import Generator

import pymysql

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "3307")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "root"),
    "database": os.environ.get("DB_NAME", "test_quotes"),
}


def get_connection() -> pymysql.Connection:
    """DB_CONFIGに基づいてMySQLコネクションを生成して返す。"""
    return pymysql.connect(
        **DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )


def get_db() -> Generator[pymysql.Connection]:
    """コネクションを生成し、使用後に自動でcloseする。"""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
