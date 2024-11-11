import logging

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel
from src.operations import filter_transactions, count_operations_by_category
from src.utils import load_transactions, search_transactions

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Меню выбора файла
    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        user_input = input("Ваш выбор: ")

        if user_input == '1':
            file_path = '../data/operations.json'
            transactions = load_transactions(file_path)
            break
        elif user_input == '2':
            file_path = '../data/transactions.csv'
            transactions = load_transactions_from_csv(file_path)
            break
        elif user_input == '3':
            file_path = '../data/transactions_excel.xlsx'
            transactions = load_transactions_from_excel(file_path)
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите пункт меню от 1 до 3.")

    # Проверка загруженных данных
    print(f"Загружено {len(transactions)} транзакций.")

    # Фильтрация по статусу
    statuses = ['executed', 'canceled', 'pending']

    while True:
        status_input = input("\nВведите статус, по которому необходимо выполнить фильтрацию. "
                             "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n").lower()

        if status_input in statuses:
            filtered_transactions = [t for t in transactions if t.get("state", "").lower() == status_input]
            logger.info(f"Операции отфильтрованы по статусу \"{status_input.upper()}\".")
            logger.info(f"Найдено {len(filtered_transactions)} транзакций со статусом \"{status_input.upper()}\".")
            break
        else:
            print(f"Статус операции \"{status_input}\" недоступен.")

    # Запрос дополнительных параметров фильтрации
    sort_by_date = input("\nОтсортировать операции по дате? Да/Нет\n").strip().lower() == 'да'
    sort_order = None

    if sort_by_date:
        sort_order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()

    only_rubles = input("\nВыводить только рублевые транзакции? Да/Нет\n").strip().lower() == 'да'

    filter_description = input(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower() == 'да'
    search_string = ""

    if filter_description:
        search_string = input("Введите слово для фильтрации по описанию:\n")

    # Применение фильтров
    if only_rubles:
        filtered_transactions = [t for t in filtered_transactions if t.get("code") == "RUB"]

    if filter_description and search_string:
        filtered_transactions = search_transactions(filtered_transactions, search_string)

    # Сортировка транзакций
    if sort_by_date and filtered_transactions:
        filtered_transactions.sort(key=lambda x: x.get("date"), reverse=(sort_order == "по убыванию"))

    # Вывод результата
    if filtered_transactions:
        print("\nРаспечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

        for transaction in filtered_transactions:
            date = transaction.get("date", "Неизвестная дата")
            description = transaction.get("description", "Нет описания")
            amount = transaction.get("amount", "Неизвестная сумма")
            currency = transaction.get("code", "Неизвестная валюта")

            print(f"{date} {description}\nСумма: {amount} {currency}\n")
    else:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()
