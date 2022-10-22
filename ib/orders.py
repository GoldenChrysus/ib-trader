from .api.client import IBClient
from typing import Dict


def submit_orders(orders: list) -> Dict:
    return IBClient().api.submit_orders(orders)
