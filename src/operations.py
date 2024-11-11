import re
from collections import Counter
from typing import Any, Dict, List


def filter_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по строке в описании с использованием регулярных выражений."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)  # Регистронезависимый поиск
    filtered_transactions = [transaction for transaction in transactions if
                             pattern.search(transaction.get("description", ""))]

    return filtered_transactions


def count_operations_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям."""
    category_counter = Counter()  # Инициализируем счетчик категорий

    for transaction in transactions:
        description = transaction.get("description", "")
        for category in categories:
            if category in description:
                category_counter[category] += 1

    return dict(category_counter)
