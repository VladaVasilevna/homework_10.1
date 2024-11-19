from collections import Counter
from typing import Any, Dict, List

import pandas as pd

from src.logger import logger  # Импортируем логгер


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из CSV-файла."""
    try:
        df = pd.read_csv(file_path, delimiter=";")
        transactions = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}.")
        return []
    except pd.errors.EmptyDataError:
        logger.warning(f"Файл пустой: {file_path}.")
        return []
    except pd.errors.ParserError:
        logger.error(f"Ошибка парсинга CSV в файле: {file_path}.")
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из Excel-файла."""
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}.")
        return []
    except ValueError as e:
        logger.error(f"Ошибка при загрузке Excel файла {file_path}: {e}.")
        return []


def count_transactions_by_type(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество банковских операций определенного типа."""
    category_counter: Counter = Counter()  # Добавлено аннотирование типа

    for transaction in transactions:
        description = transaction.get("description", "")
        for category in categories:
            if category in description:
                category_counter[category] += 1

    return dict(category_counter)
