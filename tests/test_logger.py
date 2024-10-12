import os
import sys

from src.utils import load_transactions

# Добавляем директорию src в путь поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Тестирование успешного случая
print("Тест успешного случая:")
transactions = load_transactions("transactions.json")
print(transactions)  # Ожидается вывод списка транзакций

# Тестирование случая с ошибкой формата
print("\nТест случая с ошибкой формата:")
transactions = load_transactions("invalid.json")
print(transactions)  # Ожидается вывод пустого списка и запись ошибки в лог

# Тестирование случая отсутствия файла
print("\nТест случая отсутствия файла:")
transactions = load_transactions("missing.json")
print(transactions)  # Ожидается вывод пустого списка и запись ошибки в лог
