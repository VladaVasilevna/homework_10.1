import pytest
from src.widget import mask_account_card, get_date

# Фикстура для некорректных входных данных
@pytest.fixture
def invalid_account_data():
    return [
        ("Visa 123456789012345", "Некорректный номер карты"),  # Длина меньше 16
        ("Visa 12345678123456789", "Некорректный номер карты"),  # Длина больше 16
        ("Maestro 1234abcd12345678", "Некорректный номер карты"),  # Не числовые символы
        ("Счет abcd", "Некорректный номер счета"),  # Не числовые символы
        ("Счет 1234abcd", "Некорректный номер счета"),  # Не числовые символы
        ("UnknownType 12345678", "Неизвестный тип карты или счета"),  # Неизвестный тип
    ]

# Параметризованные тесты для проверки корректного маскирования карт и счетов
@pytest.mark.parametrize("account_info, expected", [
    ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
    ("Maestro 9876543210123456", "Maestro 9876 54** **** 3456"),
    ("Счет 123456789012", "Счет **9012"),
])
def test_mask_account_card(account_info, expected):
    """Тестирование корректного маскирования карт и счетов."""
    assert mask_account_card(account_info) == expected

def test_invalid_account_data(invalid_account_data):
    """Тестирование обработки некорректных входных данных."""
    for account_info, expected in invalid_account_data:
        assert mask_account_card(account_info) == expected


# Фикстура для корректных дат
@pytest.fixture
def valid_dates():
    return [
        ("25 января 2023", "25.01.2023"),
        ("1 февраля 2020", "01.02.2020"),
        ("15 марта 2019", "15.03.2019"),
        ("31 декабря 2021", "31.12.2021"),
    ]

# Фикстура для некорректных дат
@pytest.fixture
def invalid_dates():
    return [
        ("25", "Некорректная дата"),  # Отсутствуют месяц и год
        ("января 2023", "Некорректная дата"),  # Отсутствует день
        ("25 2023", "Некорректная дата"),  # Отсутствует месяц
        ("25 мая 20", "Некорректная дата"),  # Год слишком короткий
        ("25 мая два тысячи двадцать три", "Некорректная дата"),  # Неверный формат года
    ]

# Параметризованные тесты для проверки обработки отсутствующей даты
@pytest.mark.parametrize("date_string, expected", [
    ("", "Некорректная дата"),  # Пустая строка
    (" ", "Некорректная дата"),  # Пробелы
])
def test_missing_dates(date_string, expected):
    """Тестирование обработки отсутствующей даты."""
    assert get_date(date_string) == expected

def test_valid_dates(valid_dates):
    """Тестирование правильности преобразования даты."""
    for date_string, expected in valid_dates:
        assert get_date(date_string) == expected

def test_invalid_dates(invalid_dates):
    """Тестирование работы функции на некорректных входных данных."""
    for date_string, expected in invalid_dates:
        assert get_date(date_string) == expected
