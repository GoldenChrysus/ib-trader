from ib.api.client import INSTANCE


def get_price(symbol: str, id: int) -> float:
    bars = INSTANCE.get_bars(symbol=symbol, conid=id)

    return list(reversed(bars['data']))[0]['c']
