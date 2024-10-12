from typing import Dict, Generator
from unittest.mock import MagicMock, patch

import pytest

from src.main import main


@pytest.fixture(autouse=True)
def mock_dependencies() -> Generator[Dict[str, MagicMock], None, None]:
    mock_load_json = MagicMock()
    mock_load_csv = MagicMock()
    mock_load_excel = MagicMock()
    mock_filter = MagicMock()
    mock_count = MagicMock()

    with patch("src.utils.load_transactions", mock_load_json), patch(
        "src.data_loader.load_transactions_from_csv", mock_load_csv
    ), patch("src.data_loader.load_transactions_from_excel", mock_load_excel), patch(
        "src.operations.filter_operations", mock_filter
    ), patch(
        "src.operations.count_transactions_by_type", mock_count
    ):
        # Настройка возвратов для моков
        mock_load_json.return_value = [
            {"date": "2024-01-01", "description": "Оплата за интернет", "amount": 100, "currency": "RUB"},
            {"date": "2024-01-02", "description": "Перевод другу", "amount": 200, "currency": "RUB"},
        ]
        mock_load_csv.return_value = [
            {"date": "2024-01-03", "description": "Покупка в магазине", "amount": 300, "currency": "USD"},
        ]
        mock_load_excel.return_value = [
            {"date": "2024-01-04", "description": "Оплата за телефон", "amount": 50, "currency": "RUB"},
        ]

        yield {
            "mock_count": mock_count,
            "mock_filter": mock_filter,
        }


def test_main_json_choice(mock_dependencies: Dict[str, MagicMock]) -> None:
    with patch("builtins.input", side_effect=["1", "EXECUTED", "да", "по возрастанию", "нет"]):
        main()

    assert mock_dependencies["mock_filter"].call_count == 1


def test_main_csv_choice(mock_dependencies: Dict[str, MagicMock]) -> None:
    with patch("builtins.input", side_effect=["2", "EXECUTED", "да", "по убыванию", "нет"]):
        main()

    assert mock_dependencies["mock_filter"].call_count == 1


def test_main_excel_choice(mock_dependencies: Dict[str, MagicMock]) -> None:
    with patch("builtins.input", side_effect=["3", "EXECUTED", "да", "по возрастанию", "нет"]):
        main()

    assert mock_dependencies["mock_filter"].call_count == 1


def test_invalid_choice(mock_dependencies: Dict[str, MagicMock]) -> None:
    with patch("builtins.input", side_effect=["4"]):
        main()

    # Проверка вызова assert_not_called корректно
    mock_dependencies["mock_count"].assert_not_called()
