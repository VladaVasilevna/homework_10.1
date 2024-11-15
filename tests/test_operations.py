from typing import Any, Dict, List

from src.operations import count_transactions_by_type, filter_operations


def test_filter_operations() -> None:
    transactions: List[Dict[str, Any]] = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Покупка в магазине", "amount": 300},
    ]

    filtered: List[Dict[str, Any]] = filter_operations(transactions, "интернет")
    assert len(filtered) == 1
    assert filtered[0]["description"] == "Оплата за интернет"


def test_count_transactions_by_type() -> None:
    transactions: List[Dict[str, Any]] = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Оплата за интернет", "amount": 150},
        {"description": "Покупка в магазине", "amount": 300},
        {"description": "Оплата за телефон", "amount": 50},
    ]

    categories: List[str] = [
        "Оплата за интернет",
        "Перевод другу",  # Изменено на более точное описание
        "Покупка",
        "Оплата за телефон",
    ]

    counts: Dict[str, int] = count_transactions_by_type(transactions, categories)

    assert counts["Оплата за интернет"] == 2
    assert counts["Перевод другу"] == 1  # Теперь ожидаем 1 для точного совпадения
    assert counts["Покупка"] == 1
    assert counts["Оплата за телефон"] == 1
