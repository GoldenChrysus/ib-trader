from .api.client import INSTANCE
from typing import Dict


def submit_orders(orders: list) -> Dict:
    return INSTANCE.submit_orders(orders)
