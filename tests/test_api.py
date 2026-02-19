from fastapi.testclient import TestClient

from src.database import get_connection
from src.main import app


class TestCreateQuote:
    def test_POST_quotesで見積もりが作成されDBに保存されること(self):
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