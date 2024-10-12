from unittest.mock import MagicMock, patch

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel


def test_load_transactions_from_csv_success():
    with patch("pandas.read_csv") as mock_read_csv:
        # Настройка мока
        mock_read_csv.return_value = MagicMock(to_dict=MagicMock(return_value=[{"id": 1, "amount": 100}]))

        transactions = load_transactions_from_csv("fake_path.csv")

        # Проверка результата
        assert transactions == [{"id": 1, "amount": 100}]


def test_load_transactions_from_csv_file_not_found():
    with patch("pandas.read_csv") as mock_read_csv:
        # Настройка исключения
        mock_read_csv.side_effect = FileNotFoundError

        transactions = load_transactions_from_csv("fake_path.csv")

        # Проверка результата
        assert transactions == []


def test_load_transactions_from_excel_success():
    with patch("pandas.read_excel") as mock_read_excel:
        # Настройка мока
        mock_read_excel.return_value = MagicMock(to_dict=MagicMock(return_value=[{"id": 1, "amount": 200}]))

        transactions = load_transactions_from_excel("fake_path.xlsx")

        # Проверка результата
        assert transactions == [{"id": 1, "amount": 200}]


def test_load_transactions_from_excel_file_not_found():
    with patch("pandas.read_excel") as mock_read_excel:
        # Настройка исключения
        mock_read_excel.side_effect = FileNotFoundError

        transactions = load_transactions_from_excel("fake_path.xlsx")

        # Проверка результата
        assert transactions == []
