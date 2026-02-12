from typing import Literal

import pymysql
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from src.database import get_db

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
    pass  # TODO: ハンズオンで実装
