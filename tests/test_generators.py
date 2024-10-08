from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> List[Dict]:
    """ Фикстура, возвращающая список транзакций для тестов. """
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200",
                "currency": {"code": "EUR"}
            }
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "300",
                "currency": {"code": "USD"}
            }
        }
    ]


@pytest.mark.parametrize("currency_code, expected_ids", [
    ('USD', [1, 3]),  # Ожидаем, что вернутся транзакции с id 1 и 3
    ('EUR', [2]),     # Ожидаем, что вернется транзакция с id 2
    ('GBP', []),      # Ожидаем, что не будет найдено ни одной транзакции
])
def test_filter_by_currency(transactions: List[Dict], currency_code: str, expected_ids: List[int]) -> None:
    """ Тестирование фильтрации транзакций по валюте. """
    result = list(filter_by_currency(transactions, currency_code))
    result_ids = [transaction['id'] for transaction in result]
    assert result_ids == expected_ids


def test_filter_by_currency_empty_list() -> None:
    """ Проверка обработки пустого списка транзакций. """
    result = list(filter_by_currency([], 'USD'))
    assert len(result) == 0


def test_filter_by_currency_no_currency_operations() -> None:
    """ Проверка обработки списка без соответствующих валютных операций. """
    transactions_no_currency = [
        {
            "id": 4,
            "operationAmount": {
                "amount": "400"
                # Отсутствует код валюты
            }
        },
        {
            "id": 5,
            "operationAmount": {
                "amount": "500",
                "currency": {"code": None}  # Код валюты None
            }
        }
    ]

    result = list(filter_by_currency(transactions_no_currency, 'USD'))
    assert len(result) == 0


# Тестирование генератора описаний транзакций
@pytest.mark.parametrize("input_transactions, expected_descriptions", [
    ([{"description": "Транзакция 1"}, {"description": "Транзакция 2"}, {}],
     ["Транзакция 1", "Транзакция 2", "Нет описания"]), ([], [])
])
def test_transaction_descriptions(input_transactions: List[Dict], expected_descriptions: List[str]) -> None:
    """ Тестирование генератора описаний транзакций с параметризацией. """
    result = list(transaction_descriptions(input_transactions))
    assert result == expected_descriptions


def test_transaction_descriptions_with_fixture(transactions: List[Dict]) -> None:
    """ Тестирование генератора описаний транзакций с использованием фикстуры. """
    result = list(transaction_descriptions(transactions))
    expected = [
        "Нет описания",   # Обновлено для соответствия структуре данных в фикстуре
        "Нет описания",
        "Нет описания"
    ]
    assert result == expected


@pytest.mark.parametrize("start, stop, expected_numbers", [
    (1, 5, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]),
    (10, 12, [
        "0000 0000 0000 0010",
        "0000 0000 0000 0011",
        "0000 0000 0000 0012"
    ]),
])
def test_card_number_generator(start: int, stop: int, expected_numbers: List[str]) -> None:
    """ Тестирование генератора номеров банковских карт. """
    result = list(card_number_generator(start, stop))
    assert result == expected_numbers


def test_card_number_generator_edge_cases() -> None:
    """ Проверка генератора на крайние значения диапазона. """
    # Проверка на минимальные значения
    result = list(card_number_generator(0, 0))
    assert result == ["0000 0000 0000 0000"]

    # Проверка на максимальные значения
    result = list(card_number_generator(9999, 10002))
    assert result == [
        "0000 0000 0000 9999",
        "0000 0000 0001 0000",
        "0000 0000 0001 0001",
        "0000 0000 0001 0002"
    ]
