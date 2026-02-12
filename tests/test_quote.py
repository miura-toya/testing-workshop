import pytest

from src.plan import Plan
from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize(
        "plan, expected_monthly",
        [
            (Plan.BASIC, 980),
            (Plan.STANDARD, 1980),
            (Plan.PREMIUM, 4980),
        ],
    )
    def test_プランに応じた月額料金が正しいこと(self, plan, expected_monthly):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected_monthly

    @pytest.mark.parametrize(
        "months, expected_discount, expected_total",
        [
            (1, 0, 1980),
            (11, 0, 21780),
            (12, 8, 21859),
            (23, 8, 41896),
            (24, 14, 40867),
        ],
    )
    def test_契約月数に応じた割引が適用されること(self, months, expected_discount, expected_total):
        quote = Quote(plan=Plan.STANDARD, months=months)
        assert quote.discount_rate == expected_discount
        assert quote.total_price == expected_total

    @pytest.mark.parametrize("invalid_plan", ["free", "enterprise"])
    def test_不正なプランの場合ValueErrorが発生すること(self, invalid_plan):
        with pytest.raises(ValueError):
            Plan(invalid_plan)
