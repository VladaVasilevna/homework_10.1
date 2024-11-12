from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel


@pytest.fixture
def sample_csv_file(tmp_path) -> str:
    """Создает временный CSV файл для тестирования."""
    data = """description,amount,currency\nПокупка,1500,RUB\nПеревод,1000,USD\nОплата счета,500,RUB"""
    csv_file = tmp_path / "sample.csv"
    with csv_file.open("w") as f:
        f.write(data)
    return str(csv_file)


@patch("pandas.read_csv")
def test_load_transactions_from_csv(mock_read_csv: MagicMock, sample_csv_file: str) -> None:
    """Тестирует загрузку транзакций из CSV файла."""
    mock_read_csv.return_value = pd.DataFrame(
        [
            {"description": "Покупка", "amount": 1500, "currency": "RUB"},
            {"description": "Перевод", "amount": 1000, "currency": "USD"},
            {"description": "Оплата счета", "amount": 500, "currency": "RUB"},
        ]
    )

    transactions = load_transactions_from_csv(sample_csv_file)

    assert len(transactions) == 3
    assert transactions[0]["description"] == "Покупка"


@patch("pandas.read_excel")
def test_load_transactions_from_excel(mock_read_excel: MagicMock) -> None:
    """Тестирует загрузку транзакций из Excel файла."""
    mock_read_excel.return_value = pd.DataFrame(
        [
            {"description": "Покупка", "amount": 1500, "currency": "RUB"},
            {"description": "Перевод", "amount": 1000, "currency": "USD"},
        ]
    )

    transactions = load_transactions_from_excel("dummy_path.xlsx")

    assert len(transactions) == 2
    assert transactions[1]["description"] == "Перевод"
