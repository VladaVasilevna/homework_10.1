import re
from collections import Counter
from typing import Any, Dict, List


def filter_operations(operations: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует список операций по строке поиска в описании."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    filtered_operations = [op for op in operations if pattern.search(op.get("description", ""))]

    return filtered_operations


def count_transactions_by_type(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество банковских операций по типам."""
    counter: Counter = Counter()  # Аннотация типа

    for transaction in transactions:
        description = transaction.get("description", "")

        for category in categories:
            if category in description:
                counter[category] += 1

    return dict(counter)


if __name__ == "__main__":
    # Пример использования функций (можно удалить в финальной версии)
    transactions = [
        {"description": "Оплата за интернет", "amount": 100},
        {"description": "Перевод другу", "amount": 200},
        {"description": "Оплата за интернет", "amount": 150},
        {"description": "Покупка в магазине", "amount": 300},
        {"description": "Оплата за телефон", "amount": 50},
    ]

    categories = [
        "Оплата за интернет",
        "Перевод",
        "Покупка",
        "Оплата за телефон",
    ]

    result = count_transactions_by_type(transactions, categories)

    print("Количество операций по категориям:")
    for category, count in result.items():
        print(f"{category}: {count}")
