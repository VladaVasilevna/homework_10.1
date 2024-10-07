from typing import List, Tuple

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстура для корректных номеров карт
@pytest.fixture
def valid_card_numbers() -> List[Tuple[str, str]]:
    return [("1234567812345678", "1234 56** **** 5678")]  # Ожидается: "1234 56** **** 5678"


# Параметризованные тесты для проверки корректного маскирования номера карты
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),  # Корректный номер карты
    ],
)
def test_masking_correct_number_card(card_number: str, expected: str) -> None:
    """Тестирование правильности маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected


# Фикстура для некорректных номеров карт
@pytest.fixture
def invalid_card_numbers() -> List[Tuple[str, str]]:
    return [
        ("123456781234567", "Номер карты должен содержать 16 цифр."),
        ("12345678123456789", "Номер карты должен содержать 16 цифр."),
        ("1234abcd12345678", "Номер карты должен содержать 16 цифр."),
        ("123456781234567a", "Номер карты должен содержать 16 цифр."),
        ("1234 5678 1234 5678", "Номер карты должен содержать 16 цифр."),
        ("", "Номер карты должен содержать 16 цифр."),
        ("abcdefghabcdefgh", "Номер карты должен содержать 16 цифр."),
    ]


def test_masking_correct_number(valid_card_numbers: List[Tuple[str, str]]) -> None:
    """Тестирование правильности маскирования номера карты."""
    for card_number, expected in valid_card_numbers:
        assert get_mask_card_number(card_number) == expected


def test_masking_edge_cases(invalid_card_numbers: List[Tuple[str, str]]) -> None:
    """Тестирование работы функции на различных входных форматах номеров карт."""
    for card_number, expected in invalid_card_numbers:
        assert get_mask_card_number(card_number) == expected


def test_empty_input() -> None:
    """Тестирование, что функция корректно обрабатывает входные строки, где отсутствует номер карты."""
    assert get_mask_card_number("") == "Номер карты должен содержать 16 цифр."


def test_non_numeric_input() -> None:
    """Тестирование, что функция корректно обрабатывает нечисловые входные строки."""
    assert get_mask_card_number("abcdefghabcdefgh") == "Номер карты должен содержать 16 цифр."


@pytest.fixture
def account_numbers() -> List[str]:
    return [
        "123456",  # Ожидается: **3456
        "9876543210",  # Ожидается: **3210
        "00001234",  # Ожидается: **1234
        "1234",  # Ожидается: **1234
        "123",  # Ожидается: ошибка
        "12",  # Ожидается: ошибка
        "1",  # Ожидается: ошибка
        "1234abcd",  # Ожидается: ошибка
        "abcd",  # Ожидается: ошибка
        "",  # Ожидается: ошибка
    ]


def test_masking_correct_account(account_numbers: List[str]) -> None:
    """Тестирование правильности маскирования номера счета."""
    expected_results = [
        "**3456",
        "**3210",
        "**1234",
        "**1234",
        "Номер счета должен содержать как минимум 4 цифры.",
        "Номер счета должен содержать как минимум 4 цифры.",
        "Номер счета должен содержать как минимум 4 цифры.",
        "Номер счета должен содержать как минимум 4 цифры.",
        "Номер счета должен содержать как минимум 4 цифры.",
        "Номер счета должен содержать как минимум 4 цифры.",
    ]

    for account_number, expected in zip(account_numbers, expected_results):
        assert get_mask_account(account_number) == expected


# Параметризованные тесты для проверки некорректных номеров счетов
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("123", "Номер счета должен содержать как минимум 4 цифры."),
        ("12", "Номер счета должен содержать как минимум 4 цифры."),
        ("1", "Номер счета должен содержать как минимум 4 цифры."),
        ("abcd", "Номер счета должен содержать как минимум 4 цифры."),
        ("1234abcd", "Номер счета должен содержать как минимум 4 цифры."),
        ("", "Номер счета должен содержать как минимум 4 цифры."),
    ],
)
def test_masking_edge_cases_accounts(account_number: str, expected: str) -> None:
    """Тестирование работы функции на различных входных форматах номеров счетов."""
    assert get_mask_account(account_number) == expected
