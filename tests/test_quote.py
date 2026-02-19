import pytest

from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan="standard", months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan="standard", months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980

    def test_24ヶ月以上は14パーセント割引されること(self):
        quote = Quote(plan="standard", months=24)
        assert quote.discount_rate == 14
        assert quote.total_price == 40867

    def test_割引適用時の端数は切り捨てされること(self):
        # 1,980 × 12 × 92 ÷ 100 = 21,859.2 → 切り捨てで 21,859
        quote = Quote(plan="standard", months=12)
        assert quote.discount_rate == 8
        assert quote.total_price == 21859