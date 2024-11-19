from unittest.mock import patch

import pytest

from src.main import apply_additional_filters, display_transactions, filter_by_status, get_user_file_choice, main


def test_get_user_file_choice_json():
    """Тестирует выбор JSON-файла."""
    with patch("builtins.input", return_value="1"):
        file_path, load_function, is_json = get_user_file_choice()
        assert file_path == "../data/operations.json"
        assert callable(load_function)
        assert is_json


def test_get_user_file_choice_csv():
    """Тестирует выбор CSV-файла."""
    with patch("builtins.input", return_value="2"):
        file_path, load_function, is_json = get_user_file_choice()
        assert file_path == "../data/transactions.csv"
        assert callable(load_function)
        assert not is_json


def test_get_user_file_choice_xlsx():
    """Тестирует выбор XLSX-файла."""
    with patch("builtins.input", return_value="3"):
        file_path, load_function, is_json = get_user_file_choice()
        assert file_path == "../data/transactions_excel.xlsx"
        assert callable(load_function)
        assert not is_json


def test_filter_by_status_valid():
    """Тестирует фильтрацию транзакций по статусу."""
    transactions = [
        {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
        {"state": "CANCELED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2"},
        {"state": "PENDING", "date": "2022-01-03T12:00:00.000Z", "description": "Transaction 3"},
    ]

    with patch("builtins.input", return_value="executed"):
        filtered_transactions = filter_by_status(transactions)
        assert len(filtered_transactions) == 1
        assert filtered_transactions[0]["state"] == "EXECUTED"


def test_filter_by_status_invalid():
    """Тестирует обработку некорректного статуса."""
    transactions = [
        {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
        {"state": "CANCELED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2"},
        {"state": "PENDING", "date": "2022-01-03T12:00:00.000Z", "description": "Transaction 3"},
    ]

    with patch("builtins.input", side_effect=["invalid", "canceled"]):
        filtered_transactions = filter_by_status(transactions)
        assert len(filtered_transactions) == 1
        assert filtered_transactions[0]["state"] == "CANCELED"


def test_apply_additional_filters_sort_by_date():
    """Тестирует применение дополнительных фильтров с сортировкой по дате."""
    transactions = [
        {"state": "EXECUTED", "date": "2022-01-03T12:00:00.000Z", "description": "Transaction 3"},
        {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
        {"state": "EXECUTED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2"},
    ]

    with patch("builtins.input", side_effect=["да", "по возрастанию", "нет", "нет"]):
        filtered_transactions = apply_additional_filters(transactions)
        assert len(filtered_transactions) == 3
        assert filtered_transactions[0]["date"] == "2022-01-01T12:00:00.000Z"
        assert filtered_transactions[1]["date"] == "2022-01-02T12:00:00.000Z"
        assert filtered_transactions[2]["date"] == "2022-01-03T12:00:00.000Z"


def test_apply_additional_filters_only_rubles():
    """Тестирует применение дополнительных фильтров с выводом только рублевых транзакций."""
    transactions = [
        {
            "state": "EXECUTED",
            "date": "2022-01-01T12:00:00.000Z",
            "description": "Transaction 1",
            "operationAmount": {"amount": 100, "currency": {"code": "RUB"}},
        },
        {
            "state": "EXECUTED",
            "date": "2022-01-02T12:00:00.000Z",
            "description": "Transaction 2",
            "operationAmount": {"amount": 200, "currency": {"code": "USD"}},
        },
        {
            "state": "EXECUTED",
            "date": "2022-01-03T12:00:00.000Z",
            "description": "Transaction 3",
            "operationAmount": {"amount": 300, "currency": {"code": "RUB"}},
        },
    ]

    with patch("builtins.input", side_effect=["да", "по убыванию", "да", "нет"]):
        filtered_transactions = apply_additional_filters(transactions)
        assert len(filtered_transactions) == 2
        assert filtered_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"
        assert filtered_transactions[1]["operationAmount"]["currency"]["code"] == "RUB"


def test_apply_additional_filters_filter_description():
    """Тестирует применение дополнительных фильтров с фильтрацией по описанию."""
    transactions = [
        {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
        {"state": "EXECUTED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2 with keyword"},
        {"state": "EXECUTED", "date": "2022-01-03T12:00:00.000Z", "description": "Transaction 3"},
    ]

    with patch("builtins.input", side_effect=["нет", "по убыванию", "да", "keyword"]):
        filtered_transactions = apply_additional_filters(transactions)
        assert len(filtered_transactions) == 1
        assert filtered_transactions[0]["description"] == "Transaction 2 with keyword"


def test_display_transactions_json_format():
    """Тестирует вывод транзакций в JSON формате."""
    transactions = [
        {
            "state": "EXECUTED",
            "date": "2022-01-01T12:00:00.000Z",
            "description": "Transaction 1",
            "operationAmount": {"amount": 100, "currency": {"code": "RUB"}},
            "from": "1234 5678 9012 3456",
            "to": "9876 5432 1098 7654",
        },
    ]

    with patch("builtins.print") as mock_print:
        display_transactions(transactions, is_json=True)
        mock_print.assert_any_call("\nРаспечатываю итоговый список транзакций...")
        mock_print.assert_any_call("Всего банковских операций в выборке: 1\n")
        mock_print.assert_any_call("01.01.2022 Transaction 1")
        mock_print.assert_any_call("1234 **1234 -> 9876 **9876")
        mock_print.assert_any_call("Сумма: 100 RUB\n")


def test_display_transactions_csv_format():
    """Тестирует вывод транзакций в CSV формате."""
    transactions = [
        {
            "state": "EXECUTED",
            "date": "2022-01-01T12:00:00.000Z",
            "description": "Transaction 1",
            "amount": 100,
            "currency_code": "RUB",
            "from": "1234 5678 9012 3456",
            "to": "9876 5432 1098 7654",
        },
    ]

    with patch("builtins.print") as mock_print:
        display_transactions(transactions, is_json=False)
        mock_print.assert_any_call("\nРаспечатываю итоговый список транзакций...")
        mock_print.assert_any_call("Всего банковских операций в выборке: 1\n")
        mock_print.assert_any_call("01.01.2022 Transaction 1")
        mock_print.assert_any_call("1234 **1234 -> 9876 **9876")
        mock_print.assert_any_call("Сумма: 100 RUB\n")


def test_main_json_file_choice():
    """Тестирует основную функцию с выбором JSON файла."""
    with patch("builtins.input", side_effect=["1", "executed", "нет", "нет", "нет"]):
        with patch(
            "src.utils.load_transactions",
            return_value=[
                {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
                {"state": "CANCELED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2"},
            ],
        ):
            main()


def test_main_csv_file_choice():
    """Тестирует основную функцию с выбором CSV файла."""
    with patch("builtins.input", side_effect=["2", "executed", "нет", "нет", "нет"]):
        with patch(
            "src.data_loader.load_transactions_from_csv",
            return_value=[
                {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
                {"state": "CANCELED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2"},
            ],
        ):
            main()


def test_main_xlsx_file_choice():
    """Тестирует основную функцию с выбором XLSX файла."""
    with patch("builtins.input", side_effect=["3", "executed", "нет", "нет", "нет"]):
        with patch(
            "src.data_loader.load_transactions_from_excel",
            return_value=[
                {"state": "EXECUTED", "date": "2022-01-01T12:00:00.000Z", "description": "Transaction 1"},
                {"state": "CANCELED", "date": "2022-01-02T12:00:00.000Z", "description": "Transaction 2"},
            ],
        ):
            main()


if __name__ == "__main__":
    pytest.main()
