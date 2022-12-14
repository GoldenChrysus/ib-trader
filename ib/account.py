from .api.client import IBClient
from typing import Dict


def get_account_by_alias(alias: str) -> Dict:
    accounts = list(filter(lambda x: x['accountAlias'] == alias, IBClient().api.get_accounts()))

    return None if not accounts else accounts[0]


def use_account(id: str) -> bool:
    res = IBClient().api.switch_account(id)
    success = res.get('set', False) or res.get('error', None) == 'Account already set'

    return success


def get_cash() -> float:
    return IBClient().api.get_cash()


def get_portfolio() -> dict:
    return IBClient().api.get_portfolio()
