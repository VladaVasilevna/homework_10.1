import json
import logging
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

from src.utils import load_transactions

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    filename='logs/test_load_transactions.log',  # Путь к файлу логов
    filemode='w',                                 # Перезапись файла при каждом запуске
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def test_load_transactions_file_not_exist() -> None:
    """Тест для случая, когда файл не существует."""
    file_path: str = "data/non_existent_file.json"
    result: List[Dict[str, Any]] = load_transactions(file_path)
    logging.warning(f"Тестирование отсутствующего файла: {file_path} -> {result}")
    assert result == []


def test_load_transactions_empty_file() -> None:
    """Тест для случая пустого файла."""
    mock_empty_file = mock_open(read_data="")

    with patch("builtins.open", mock_empty_file):
        result: List[Dict[str, Any]] = load_transactions("data/empty_file.json")
        logging.info("Тестирование пустого файла.")
        assert result == []


def test_load_transactions_invalid_json() -> None:
    """Тест для случая с некорректным JSON."""
    mock_invalid_json_file = mock_open(read_data="{invalid_json}")

    with patch("builtins.open", mock_invalid_json_file):
        result: List[Dict[str, Any]] = load_transactions("data/invalid_json.json")
        logging.error("Тестирование некорректного JSON.")
        assert result == []


def test_load_transactions_valid_json() -> None:
    """Тест для случая с корректным JSON."""
    # Читаем данные из файла operations.json для теста
    with open("data/operations.json", "r", encoding="utf-8") as file:
        mock_valid_json_data = file.read()

    mock_valid_json_file = mock_open(read_data=mock_valid_json_data)

    with patch("builtins.open", mock_valid_json_file):
        result: List[Dict[str, Any]] = load_transactions("data/operations.json")
        logging.info("Тестирование корректного JSON.")
        assert result == json.loads(mock_valid_json_data)  # Проверяем соответствие
