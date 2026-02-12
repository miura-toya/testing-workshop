from src.discount import DiscountRate
from src.plan import Plan


class Quote:
    """プランと契約月数から見積もりを算出する値オブジェクト。"""

    def __init__(self, plan: Plan, months: int):
        self._plan = plan
        self._months = months
        self._monthly_price = plan.monthly_price
        self._discount_rate = DiscountRate(months)
        self._total_price = self._calc_total()

    def _calc_total(self) -> int:
        """月額 × 月数 に割引率を適用した合計金額を整数で返す。"""
        return self._monthly_price * self._months * (100 - self._discount_rate.value) // 100

    @property
    def plan(self) -> str:
        return self._plan.value

    @property
    def months(self) -> int:
        return self._months

    @property
    def monthly_price(self) -> int:
        return self._monthly_price

    @property
    def discount_rate(self) -> int:
        return self._discount_rate.value

    @property
    def total_price(self) -> int:
        return self._total_price
