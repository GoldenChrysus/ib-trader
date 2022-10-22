import decimal


def round_down(value: float, decimals: int) -> decimal.Decimal:
    with decimal.localcontext() as context:
        value = decimal.Decimal(value)

        context.rounding = decimal.ROUND_DOWN

        return round(value, decimals)
