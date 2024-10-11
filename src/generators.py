from typing import Dict, Generator, List


def filter_by_currency(transactions: List[Dict], currency_code: str) -> Generator[Dict, None, None]:
    """Фильтрует список транзакций по заданной валюте"""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Генератор, который возвращает описание каждой транзакции"""
    for transaction in transactions:
        yield transaction.get("description", "Нет описания")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start, stop + 1):
        # Форматирование номера карты
        formatted_number = f"{number:016d}"  # Преобразуем в строку длиной 16 символов с ведущими нулями
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
