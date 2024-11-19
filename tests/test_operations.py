from typing import Any, Dict, List

from src.operations import count_operations_by_category, filter_transactions


def test_filter_transactions() -> None:
    # Тест фильтрации транзакций по строке
    transactions: List[Dict[str, Any]] = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Покупка в магазине", "amount": 300},
    ]

    filtered: List[Dict[str, Any]] = filter_transactions(transactions, "интернет")
    assert len(filtered) == 1
    assert filtered[0]["description"] == "Оплата за интернет"

    # Тест фильтрации без совпадений
    filtered = filter_transactions(transactions, "автомобиль")
    assert len(filtered) == 0

    # Тест регистронезависимого поиска
    filtered = filter_transactions(transactions, "ИНТЕРНЕТ")
    assert len(filtered) == 1
    assert filtered[0]["description"] == "Оплата за интернет"


def test_filter_transactions_empty_transactions() -> None:
    # Тест фильтрации с пустым списком транзакций
    transactions: List[Dict[str, Any]] = []
    filtered: List[Dict[str, Any]] = filter_transactions(transactions, "интернет")
    assert len(filtered) == 0


def test_count_operations_by_category() -> None:
    # Тест подсчета операций по категориям
    transactions: List[Dict[str, Any]] = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Оплата за интернет", "amount": 150},
        {"description": "Покупка в магазине", "amount": 300},
        {"description": "Оплата за телефон", "amount": 50},
    ]

    categories: List[str] = [
        "Оплата за интернет",
        "Перевод другу",
        "Покупка",
        "Оплата за телефон",
    ]

    counts: Dict[str, int] = count_operations_by_category(transactions, categories)

    assert counts["Оплата за интернет"] == 2
    assert counts["Перевод другу"] == 1
    assert counts["Покупка"] == 1
    assert counts["Оплата за телефон"] == 1


def test_count_operations_by_category_no_matches() -> None:
    # Тест подсчета операций без совпадений
    transactions: List[Dict[str, Any]] = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Оплата за интернет", "amount": 150},
        {"description": "Покупка в магазине", "amount": 300},
        {"description": "Оплата за телефон", "amount": 50},
    ]

    categories: List[str] = [
        "Автомобиль",
        "Жилье",
        "Путешествие",
    ]

    counts: Dict[str, int] = count_operations_by_category(transactions, categories)

    assert counts["Автомобиль"] == 0
    assert counts["Жилье"] == 0
    assert counts["Путешествие"] == 0


def test_count_operations_by_category_empty_categories() -> None:
    # Тест подсчета операций с пустым списком категорий
    transactions: List[Dict[str, Any]] = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Оплата за интернет", "amount": 150},
        {"description": "Покупка в магазине", "amount": 300},
        {"description": "Оплата за телефон", "amount": 50},
    ]

    categories: List[str] = []

    counts: Dict[str, int] = count_operations_by_category(transactions, categories)

    assert counts == {}


def test_count_operations_by_category_empty_transactions() -> None:
    # Тест подсчета операций с пустым списком транзакций
    transactions: List[Dict[str, Any]] = []
    categories: List[str] = [
        "Оплата за интернет",
        "Перевод другу",
        "Покупка",
        "Оплата за телефон",
    ]

    counts: Dict[str, int] = count_operations_by_category(transactions, categories)

    assert counts == {
        "Оплата за интернет": 0,
        "Перевод другу": 0,
        "Покупка": 0,
        "Оплата за телефон": 0,
    }
