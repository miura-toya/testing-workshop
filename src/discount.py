class DiscountRate:
    """契約月数に応じた割引率(%)を表す値オブジェクト。"""

    _LONG_TERM_MONTHS = 24
    _LONG_TERM_RATE = 14
    _MID_TERM_MONTHS = 12
    _MID_TERM_RATE = 8

    def __init__(self, months: int):
        if months >= self._LONG_TERM_MONTHS:
            self._value = self._LONG_TERM_RATE
        elif months >= self._MID_TERM_MONTHS:
            self._value = self._MID_TERM_RATE
        else:
            self._value = 0

    @property
    def value(self) -> int:
        """割引率(%)を返す。"""
        return self._value
