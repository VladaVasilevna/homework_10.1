import json
from typing import Any, Dict, List

from .logger import logger  # Импортируем логгер


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружены транзакции из {file_path}.")
                return data
            else:
                logger.warning(f"Данные из {file_path} не являются списком.")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}.")
        return []
