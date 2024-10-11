import os
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


@pytest.fixture(autouse=True)
def set_api_key() -> None:
    """Фикстура для установки API_KEY в окружении."""
    os.environ["API_KEY"] = "test_api_key"


def test_convert_to_rub_with_rub_currency() -> None:
    """Тест для случая, когда валюта уже в рублях."""
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 100.0


def test_convert_to_rub_with_usd_currency() -> None:
    """Тест для случая с конвертацией из USD в RUB."""
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "USD"}

    mock_response_data: Dict[str, Any] = {"rates": {"RUB": 75.0}}

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response_data)

        result = convert_to_rub(transaction)
        assert result == 7500.0


def test_convert_to_rub_with_invalid_currency() -> None:
    """Тест для случая с некорректной валютой."""
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "INVALID"}

    mock_response_data: Dict[str, Any] = {"rates": {}}  # Пустой словарь для rates

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response_data)

        result = convert_to_rub(transaction)  # Используем переменную
        assert result == 0.0  # Если курс не найден, возвращаем 0.0


def test_convert_to_rub_api_error() -> None:
    """Тест для случая с ошибкой API."""
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "EUR"}

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=500)  # Симулируем ошибку сервера

        result = convert_to_rub(transaction)
        assert result == 0.0  # Возвращаем 0.0 в случае ошибки API
