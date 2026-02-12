from pathlib import Path

import pytest

from src.database import get_connection

SCHEMA_SQL = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


@pytest.fixture(autouse=True)
def setup_db():
    """各テストの前にテーブルを作成・クリーンアップし、テスト後にテーブルを削除する。"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(SCHEMA_SQL.read_text())
            cursor.execute("DELETE FROM quotes")
        conn.commit()
    finally:
        conn.close()
    yield
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS quotes")
        conn.commit()
    finally:
        conn.close()
