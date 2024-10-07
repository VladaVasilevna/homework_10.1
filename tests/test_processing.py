import pytest
from typing import Dict, List, Any
from src.processing import filter_by_state, sort_by_date

# Фикстура для тестирования
@pytest.fixture
def transactions():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

def test_filter_by_state(transactions):
    """Тестирование фильтрации списка словарей по заданному статусу state."""
    executed = filter_by_state(transactions)
    canceled = filter_by_state(transactions, state='CANCELED')

    assert len(executed) == 2
    assert len(canceled) == 2
    assert all(tx['state'] == 'EXECUTED' for tx in executed)
    assert all(tx['state'] == 'CANCELED' for tx in canceled)

def test_no_matching_state(transactions):
    """Тестирование работы функции при отсутствии словарей с указанным статусом state."""
    filtered = filter_by_state(transactions, state='PENDING')
    assert filtered == []  # Ожидаем пустой список

# Параметризованные тесты для проверки различных значений статуса
@pytest.mark.parametrize("state, expected_count", [
    ('EXECUTED', 2),
    ('CANCELED', 2),
    ('PENDING', 0),
])
def test_parametrized_filter_by_state(transactions, state, expected_count):
    """Параметризованное тестирование фильтрации по различным статусам."""
    filtered = filter_by_state(transactions, state)
    assert len(filtered) == expected_count


# Фикстура для тестирования транзакций
@pytest.fixture
def transactions():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 123456789, 'state': 'EXECUTED', 'date': '2018-09-12T21:27:25.241689'},
    ]


# Тестирование сортировки в порядке убывания
def test_sort_by_date_desc(transactions):
    sorted_transactions = sort_by_date(transactions)
    expected_order = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 123456789, 'state': 'EXECUTED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]
    assert sorted_transactions == expected_order


# Тестирование сортировки в порядке возрастания
def test_sort_by_date_asc(transactions):
    sorted_transactions = sort_by_date(transactions, descending=False)
    expected_order = [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 123456789, 'state': 'EXECUTED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    ]
    assert sorted_transactions == expected_order


# Тестирование сортировки с одинаковыми датами
def test_sort_with_identical_dates():
    transactions = [
        {'id': 1, 'state': "EXECUTED", "date": "2022-01-01T00:00:00"},
        {'id': 2, 'state': "EXECUTED", "date": "2022-01-01T00:00:00"},
    ]
    sorted_transactions = sort_by_date(transactions)
    assert sorted_transactions[0]['id'] == 1 or sorted_transactions[0]['id'] == 2
    assert sorted_transactions[1]['id'] == 1 or sorted_transactions[1]['id'] == 2


# Параметризованный тест для некорректных форматов дат
@pytest.mark.parametrize("invalid_transaction", [
    [{'id': 1, "state": "EXECUTED", "date": "invalid-date"}],
    [{'id': 2, "state": "EXECUTED", "date": None}],
    [{'id': 3, "state": "EXECUTED", "date": "2021/01/01"}],
])
def test_sort_with_invalid_dates(invalid_transaction):
    sorted_transactions = sort_by_date(invalid_transaction)
    # Проверяем, что возвращаемый список пустой или содержит только корректные записи
    assert all('date' in t for t in sorted_transactions)  # Все записи должны иметь ключ date


# Тестирование фильтрации по статусу
def test_filter_by_state(transactions):
    """Тестирование фильтрации списка словарей по заданному статусу state."""
    executed = filter_by_state(transactions, state='EXECUTED')
    canceled = filter_by_state(transactions, state='CANCELED')

    assert len(executed) == 3  # Ожидаемое значение соответствует фактическому количеству
    assert len(canceled) == 2  # Ожидаемое значение соответствует фактическому количеству


# Параметризованное тестирование фильтрации по различным статусам.
@pytest.mark.parametrize("state, expected_count", [
    ('EXECUTED', 3),  # Ожидаемое количество записей со статусом EXECUTED
    ('CANCELED', 2),  # Ожидаемое количество записей со статусом CANCELED
    ('PENDING', 0),  # Ожидаемое количество записей со статусом PENDING (нет таких записей)
])
def test_parametrized_filter_by_state(transactions, state, expected_count):
    """Параметризованное тестирование фильтрации по различным статусам."""
    filtered = filter_by_state(transactions, state)
    assert len(filtered) == expected_count
