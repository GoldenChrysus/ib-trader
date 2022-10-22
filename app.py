from consts import CURRENCIES, TARGETS
from lib.account import get_account_by_alias, get_cash, get_portfolio, use_account
from lib.helpers import round_down
from lib.inst.equity import get_id, get_price
from lib.orders import submit_orders


def testing():
    from lib.api.client import INSTANCE
    import json

    # print(INSTANCE.get_conid('MUB', instrument_filters={'assetClass': 'STK'}, contract_filters={'isUS': True}))
    print(json.dumps(INSTANCE.get_live_orders()))


def main():
    if not (account := get_account_by_alias('Traditional IRA')):
        raise RuntimeError('Account not found.')

    if not use_account(account['id']):
        raise RuntimeError('Could not switch accounts.')

    cash = get_cash()

    if cash <= 5:
        print('Cash too low: $%s' % (cash))
        return

    portfolio = get_portfolio()
    prices = {}
    values = {}
    allocations = {}
    total_value = 0.0
    spent = 0.0

    for symbol, shares in portfolio.items():
        if symbol in CURRENCIES:
            continue

        prices[symbol] = get_price(symbol)
        values[symbol] = shares * prices[symbol]

    total_value = sum(values.values())

    for symbol, value in values.items():
        allocations[symbol] = value / total_value

    allocations = dict(sorted(allocations.items(), key=lambda x: x[1] - TARGETS[x[0]]))
    total_value += cash
    orders = []

    for symbol in allocations.keys():
        ideal_shares = max(0, round_down((total_value * TARGETS[symbol] / prices[symbol]) - portfolio[symbol], 4))
        viable_shares = min(ideal_shares, round_down((cash - spent) / prices[symbol], 4))

        orders.append({
            'acctId': account['id'],
            'conid': get_id(symbol),
            'orderType': 'LMT',
            'side': 'BUY',
            'price': prices[symbol] + 0.05,
            'quantity': float(viable_shares),
            'ticker': symbol,
            'tif': 'GTC',
            # 'outsideRTH': True,
        })

        spent += (float(viable_shares) * prices[symbol])

    print(orders)
    # print(submit_orders(orders))


if __name__ == '__main__':
    main()
    # testing()
