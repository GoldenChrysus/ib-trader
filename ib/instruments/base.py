from ..api.client import IBClient


def get_price(symbol: str, id: int) -> float:
    bars = IBClient().api.get_bars(symbol=symbol, conid=id)

    return list(reversed(bars['data']))[0]['c']
