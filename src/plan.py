from enum import Enum


class Plan(Enum):
    """契約プランを表す列挙型。"""

    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

    @property
    def monthly_price(self) -> int:
        """プランに対応する月額料金(円)を返す。"""
        prices = {
            "basic": 980,
            "standard": 1980,
            "premium": 4980,
        }
        return prices[self.value]
