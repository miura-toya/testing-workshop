import pytest

from src.plan import Plan
from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [(Plan.BASIC, 980), (Plan.STANDARD, 1980), (Plan.PREMIUM, 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan=Plan.STANDARD, months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan=Plan.STANDARD, months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980

    def test_24ヶ月以上は14パーセント割引されること(self):
        quote = Quote(plan=Plan.STANDARD, months=24)
        assert quote.discount_rate == 14
        assert quote.total_price == 40867

    def test_割引適用時の端数は切り捨てされること(self):
        # 1,980 × 12 × 92 ÷ 100 = 21,859.2 → 切り捨てで 21,859
        quote = Quote(plan=Plan.STANDARD, months=12)
        assert quote.discount_rate == 8
        assert quote.total_price == 21859

    @pytest.mark.parametrize("invalid_plan", ["free", "enterprise"])
    def test_不正なプランの場合ValueErrorが発生すること(self, invalid_plan):
        with pytest.raises(ValueError):
            Plan(invalid_plan)
