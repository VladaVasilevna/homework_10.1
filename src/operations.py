import re
from typing import Any, Dict, List


def filter_operations(operations: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует список операций по строке поиска в описании."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    filtered_operations = [op for op in operations if pattern.search(op.get("description", ""))]

    return filtered_operations


def count_operations_by_category(operations: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Возвращает словарь с количеством операций по категориям."""
    category_count = {category: 0 for category in categories}

    for operation in operations:
        description = operation.get("description", "")
        for category in categories:
            if category in description:
                category_count[category] += 1

    return category_count
