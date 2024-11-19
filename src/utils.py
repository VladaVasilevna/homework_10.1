import json
import os
import re
from typing import Any, Dict, List

from src.logger import logger  # Импортируем логгер


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружены транзакции из {file_path}.")
                return data
            else:
                logger.warning(f"Данные из {file_path} не являются списком: {type(data)}.")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}.")
        return []


def filter_transactions_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    filtered = [transaction for transaction in transactions if transaction.get("state", "").lower() == status.lower()]
    logger.info(f'Найдено {len(filtered)} транзакций со статусом "{status}".')
    return filtered


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Ищет транзакции по строке в описании с использованием регулярных выражений."""
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)  # Регистронезависимый поиск
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит информацию о транзакциях в удобном формате."""
    if not transactions:
        print("Не найдено ни одной транзакции для отображения.")
        return

    for transaction in transactions:
        date = transaction["date"]
        description = transaction["description"]
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]

        print(f"{date}: {description} - {amount} {currency}")


# Пример использования функций
if __name__ == "__main__":
    file_path = "../data/operations.json"

    # Загружаем транзакции
    transactions = load_transactions(file_path)

    # Проверяем количество загруженных транзакций
    print(f"Загружено {len(transactions)} транзакций.")

    # Фильтруем по статусу EXECUTED
    executed_transactions = filter_transactions_by_status(transactions, "EXECUTED")

    # Выводим все выполненные транзакции
    print(f"Найдено {len(executed_transactions)} выполненных транзакций:")
    print_transactions(executed_transactions)
