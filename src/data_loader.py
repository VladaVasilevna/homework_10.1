from typing import Any, Dict, List

import pandas as pd

from .logger import logger  # Импортируем логгер


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из CSV-файла."""
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно загружены транзакции из {file_path}.")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}.")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"Файл пуст: {file_path}.")
        return []
    except pd.errors.ParserError:
        logger.error(f"Ошибка парсинга CSV в файле: {file_path}.")
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из Excel-файла."""
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно загружены транзакции из {file_path}.")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}.")
        return []
    except ValueError:
        logger.error(f"Ошибка чтения Excel файла: {file_path}.")
        return []
