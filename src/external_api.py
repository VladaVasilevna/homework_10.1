import os
from typing import Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def convert_to_rub(transaction: Dict[str, float]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return float(amount)

    # Получаем курс валют из API
    api_key = os.getenv("API_KEY")
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"

    headers = {
        "apikey": api_key,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        rate = data["rates"].get("RUB")  # Получаем курс RUB

        # Если курс не найден или валюта некорректна, возвращаем 0.0
        if rate is None:
            return 0.0

        # Убедимся, что rate является числом
        if isinstance(rate, (int, float)):
            return round(amount * rate, 2)

    return 0.0  # Возвращаем 0.0 в случае ошибки API или отсутствия курса
