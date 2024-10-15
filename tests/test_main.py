from unittest.mock import patch

import pytest

from src.main import get_status_input, get_user_input, main


def test_get_user_input_valid():
    """Тестирует получение корректного ввода от пользователя."""
    with patch("builtins.input", side_effect=["1"]):
        result = get_user_input("Выберите пункт: ", ["1", "2", "3"])
        assert result == "1"


def test_get_user_input_invalid():
    """Тестирует обработку некорректного ввода пользователя."""
    with patch("builtins.input", side_effect=["некорректный ввод", "некорректный ввод", "2"]):
        result = get_user_input("Выберите пункт: ", ["1", "2", "3"])
        assert result == "2"


def test_get_user_input_exceed_attempts():
    """Тестирует превышение максимального количества попыток ввода."""
    with patch("builtins.input", side_effect=["некорректный ввод"] * 3):
        with pytest.raises(ValueError, match="Превышено максимальное количество попыток ввода."):
            get_user_input("Выберите пункт: ", ["1", "2", "3"])


def test_get_status_input_valid():
    """Тестирует получение корректного статуса от пользователя."""
    with patch("builtins.input", side_effect=["EXECUTED"]):
        result = get_status_input("Введите статус: ", ["EXECUTED", "CANCELED", "PENDING"])
        assert result == "EXECUTED"


def test_get_status_input_invalid():
    """Тестирует обработку некорректного статуса."""
    with patch("builtins.input", side_effect=["недоступный статус", "CANCELED"]):
        result = get_status_input("Введите статус: ", ["EXECUTED", "CANCELED", "PENDING"])
        assert result == "CANCELED"


def test_get_status_input_exceed_attempts():
    """Тестирует, что ввод некорректного статуса повторяется до получения правильного."""
    with patch("builtins.input", side_effect=["недоступный статус", "недоступный статус", "PENDING"]):
        result = get_status_input("Введите статус: ", ["EXECUTED", "CANCELED", "PENDING"])
        assert result == "PENDING"


@patch("builtins.input", side_effect=["1", "EXECUTED"])  # Выбор JSON и статус
@patch("src.main.load_transactions", return_value=[{"description": "Покупка", "amount": 1500}])
@patch("src.main.filter_operations", return_value=[{"description": "Покупка", "amount": 1500}])
@patch("src.main.count_transactions_by_type", return_value={"Покупка": 1})
@patch("builtins.print")
def test_main_load_transactions_json(mock_print, mock_count_transactions, mock_filter, mock_load, mock_input):
    main()

    # Проверка вызова функций
    mock_load.assert_called_once_with("data/operations.json")
    mock_filter.assert_called_once()
    mock_count_transactions.assert_called_once()

    # Проверяем вывод
    assert mock_print.call_count > 0


@patch("builtins.input", side_effect=["2", "CANCELED"])  # Выбор CSV и статус
@patch("src.main.load_transactions_from_csv", return_value=[{"description": "Оплата", "amount": 500}])
@patch("src.main.filter_operations", return_value=[{"description": "Оплата", "amount": 500}])
@patch("src.main.count_transactions_by_type", return_value={"Оплата": 1})
@patch("builtins.print")
def test_main_load_transactions_csv(mock_print, mock_count_transactions, mock_filter, mock_load_csv, mock_input):
    main()

    # Проверка вызова функций
    mock_load_csv.assert_called_once_with("data/transactions.csv")
    mock_filter.assert_called_once()
    mock_count_transactions.assert_called_once()

    # Проверяем вывод
    assert mock_print.call_count > 0


if __name__ == "__main__":
    pytest.main()
