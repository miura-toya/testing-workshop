class Quote:
    def __init__(self, plan: str, months: int):
        if plan == "basic":
            self._monthly_price = 980
        elif plan == "standard":
            self._monthly_price = 1980
        elif plan == "premium":
            self._monthly_price = 4980

        self._plan = plan
        self._months = months

        if months >= 24:
            self._discount_rate = 14
        elif months >= 12:
            self._discount_rate = 8
        else:
            self._discount_rate = 0

        self._total_price = self._monthly_price * months * (100 - self._discount_rate) // 100

    @property
    def plan(self) -> str:
        return self._plan

    @property
    def months(self) -> int:
        return self._months

    @property
    def monthly_price(self) -> int:
        return self._monthly_price

    @property
    def discount_rate(self) -> int:
        return self._discount_rate

    @property
    def total_price(self) -> int:
        return self._total_price