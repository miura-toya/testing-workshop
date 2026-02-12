import pymysql

from src.quote import Quote


def save_quote(conn: pymysql.Connection, customer_name: str, quote: Quote) -> int:
    """見積もりをDBに保存し、採番されたIDを返す。"""
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO quotes (customer_name, plan, months, monthly_price, discount_rate, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                customer_name,
                quote.plan,
                quote.months,
                quote.monthly_price,
                quote.discount_rate,
                quote.total_price,
            ),
        )
        conn.commit()
        return cursor.lastrowid
