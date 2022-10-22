from ..api.client import INSTANCE
from .base import get_price as get_price_base


def get_id(symbol: str) -> int:
    return INSTANCE.get_conid(symbol, instrument_filters={'assetClass': 'STK'}, contract_filters={'isUS': True})


def get_price(symbol: str) -> float:
    return get_price_base(symbol=symbol, id=get_id(symbol))
