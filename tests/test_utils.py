import json
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_transactions_file_not_exist() -> None:
    """Тест для случая, когда файл не существует."""
    file_path: str = "data/non_existent_file.json"
    result: List[Dict[str, Any]] = load_transactions(file_path)
    assert result == []


def test_load_transactions_empty_file() -> None:
    """Тест для случая пустого файла."""
    mock_empty_file = mock_open(read_data="")

    with patch("builtins.open", mock_empty_file):
        result: List[Dict[str, Any]] = load_transactions("data/empty_file.json")
        assert result == []


def test_load_transactions_invalid_json() -> None:
    """Тест для случая с некорректным JSON."""
    mock_invalid_json_file = mock_open(read_data="{invalid_json}")

    with patch("builtins.open", mock_invalid_json_file):
        result: List[Dict[str, Any]] = load_transactions("data/invalid_json.json")
        assert result == []


def test_load_transactions_valid_json() -> None:
    """Тест для случая с корректным JSON."""
    # Читаем данные из файла operations.json для теста
    with open("data/operations.json", "r", encoding="utf-8") as file:
        mock_valid_json_data = file.read()

    mock_valid_json_file = mock_open(read_data=mock_valid_json_data)

    with patch("builtins.open", mock_valid_json_file):
        result: List[Dict[str, Any]] = load_transactions("data/operations.json")
        assert result == json.loads(mock_valid_json_data)  # Проверяем соответствие
