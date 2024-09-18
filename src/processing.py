from typing import Dict, List


def filter_by_state(transactions, state='EXECUTED'):
    """ Фильтрует список словарей по значению ключа state """
    return [transaction for transaction in transactions if transaction.get('state') == state]


transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]


executed_transactions = filter_by_state(transactions)
canceled_transactions = filter_by_state(transactions, state='CANCELED')


def sort_by_date(transactions: List[Dict], descending: bool = True) -> List[Dict]:
    """ Сортирует список словарей по дате """
    return sorted(transactions, key=lambda x: x['date'], reverse=descending)


transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]


sorted_transactions_desc = sort_by_date(transactions)
sorted_transactions_asc = sort_by_date(transactions, descending=False)
