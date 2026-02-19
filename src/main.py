from typing import Literal

import pymysql
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from src.database import get_db
from src.plan import Plan
from src.quote import Quote

app = FastAPI()


class QuoteRequest(BaseModel):
    """見積もり作成リクエストのスキーマ。"""

    customer_name: str
    plan: Literal["basic", "standard", "premium"]
    months: int = Field(gt=0)


class QuoteResponse(BaseModel):
    """見積もり作成レスポンスのスキーマ。"""

    id: int
    customer_name: str
    plan: str
    months: int
    monthly_price: int
    discount_rate: int
    total_price: int


@app.post("/quotes", status_code=201, response_model=QuoteResponse)
def create_quote(
    req: QuoteRequest, conn: pymysql.Connection = Depends(get_db)
) -> QuoteResponse:
    """見積もりを作成してDBに保存し、結果を返す。"""
    quote = Quote(plan=Plan(req.plan), months=req.months)

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO quotes (customer_name, plan, months, monthly_price, discount_rate, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                req.customer_name,
                quote.plan,
                quote.months,
                quote.monthly_price,
                quote.discount_rate,
                quote.total_price,
            ),
        )
        conn.commit()
        quote_id = cursor.lastrowid

    return QuoteResponse(
        id=quote_id,
        customer_name=req.customer_name,
        plan=quote.plan,
        months=quote.months,
        monthly_price=quote.monthly_price,
        discount_rate=quote.discount_rate,
        total_price=quote.total_price,
    )