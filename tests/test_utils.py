import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions, search_transactions


@pytest.fixture
def sample_json_file(tmp_path) -> str:
    """Создает временный JSON файл для тестирования."""
    data = [
        {"description": "Покупка", "amount": 1500, "currency": "RUB"},
        {"description": "Перевод", "amount": 1000, "currency": "USD"},
        {"description": "Оплата счета", "amount": 500, "currency": "RUB"},
    ]
    json_file = tmp_path / "sample.json"
    with json_file.open("w") as f:
        json.dump(data, f)
    return str(json_file)


def test_load_transactions(sample_json_file: str) -> None:
    """Тестирует загрузку транзакций из JSON файла."""
    transactions = load_transactions(sample_json_file)
    assert len(transactions) == 3
    assert transactions[0]["description"] == "Покупка"


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"description": "Покупка", "amount": 1500, "currency": "RUB"}]',
)
def test_load_transactions_mocked(mock_open_func) -> None:
    """Тестирует загрузку транзакций с использованием мока."""
    transactions = load_transactions("dummy_path.json")
    assert len(transactions) == 1
    assert transactions[0]["description"] == "Покупка"


def test_search_transactions() -> None:
    """Тестирует поиск транзакций по описанию."""
    transactions = [
        {"description": "Покупка в магазине", "amount": 1500, "currency": "RUB"},
        {"description": "Перевод на счет", "amount": 1000, "currency": "USD"},
        {"description": "Оплата за интернет", "amount": 500, "currency": "RUB"},
    ]

    result = search_transactions(transactions, "магазин")
    assert len(result) == 1
    assert result[0]["description"] == "Покупка в магазине"

    result = search_transactions(transactions, "Оплата")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата за интернет"
