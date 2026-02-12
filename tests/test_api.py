from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.database import get_connection
from src.main import app

SCHEMA_SQL = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


@pytest.fixture(autouse=True)
def setup_db():
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


def test_POST_quotesで見積もりが作成できる():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.post(
        "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
    )

    # Assert
    data = response.json()
    assert response.status_code == 201
    assert "id" in data
    assert data["monthly_price"] == 1980
    assert data["discount_rate"] == 8
    assert data["total_price"] == 21859

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM quotes WHERE id = %s", (data["id"],))
            row = cursor.fetchone()
    finally:
        conn.close()
    assert row is not None
    assert row["total_price"] == 21859


def test_DBエラー時に500エラーが返ること():
    # Arrange: テーブルを削除してDBエラーを発生させる
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE quotes")
        conn.commit()
    finally:
        conn.close()

    # Act
    client = TestClient(app)
    response = client.post(
        "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
    )

    # Assert
    assert response.status_code == 500


@pytest.mark.parametrize(
    "body",
    [
        {"customer_name": "田中太郎", "plan": "free", "months": 12},
        {"customer_name": "田中太郎", "plan": "standard", "months": 0},
        {"customer_name": "田中太郎"},
    ],
)
def test_不正なリクエストで422エラーが返ること(body):
    client = TestClient(app)
    response = client.post("/quotes", json=body)
    assert response.status_code == 422
