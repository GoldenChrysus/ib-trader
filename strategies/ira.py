from .consts import ACCOUNT_ALIAS, CURRENCIES, TARGETS
from ib.account import get_account_by_alias, get_cash, get_portfolio, use_account
from ib.helpers import round_down
from ib.instruments.equity import get_id, get_price
# from ib.orders import submit_orders
from ib.waiters.time import wait_until_time
from typing import Dict


def _get_data() -> Dict:
    cash = get_cash()
    portfolio = get_portfolio()
    prices = {}
    values = {}
    allocations = {}
    total_value = 0.0

    for symbol, shares in portfolio.items():
        if symbol in CURRENCIES:
            continue

        prices[symbol] = get_price(symbol)
        values[symbol] = shares * prices[symbol]

    total_value = sum(values.values())

    for symbol, value in values.items():
        allocations[symbol] = value / total_value

    allocations = dict(sorted(allocations.items(), key=lambda x: x[1] - TARGETS[x[0]]))

    return {
        'allocations': allocations,
        'cash': cash,
        'portfolio': portfolio,
        'prices': prices,
        'total': total_value,
    }


def rebalance_holdings():
    wait_until_time('09:45', 'America/New_York')

    if not (account := get_account_by_alias(ACCOUNT_ALIAS)):
        raise RuntimeError('Account not found.')

    if not use_account(account['id']):
        raise RuntimeError('Could not switch accounts.')

    data = _get_data()

    if data['cash'] <= 5:
        print('Cash too low: $%s' % data['cash'])
        return

    total_value = data['cash'] + data['total']
    orders = []
    spent = 0.0

    for symbol in data['allocations'].keys():
        ideal_shares = max(0, round_down((total_value * TARGETS[symbol] / data['prices'][symbol]) - data['portfolio'][symbol], 4))
        viable_shares = min(ideal_shares, round_down((data['cash'] - spent) / data['prices'][symbol], 4))

        orders.append({
            'acctId': account['id'],
            'conid': get_id(symbol),
            'orderType': 'LMT',
            'side': 'BUY',
            'price': data['prices'][symbol] + 0.05,
            'quantity': float(viable_shares),
            'ticker': symbol,
            'tif': 'GTC',
            # 'outsideRTH': True,
        })

        spent += (float(viable_shares) * data['prices'][symbol])

    print(orders)
    # print(submit_orders(orders))
