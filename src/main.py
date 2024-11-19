import re
from datetime import datetime

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel
from src.masks import get_mask_account, get_mask_card_number
from src.operations import filter_transactions
from src.utils import load_transactions


def extract_number(text):
    """Извлекает числовую часть из заданной строки."""
    match = re.search(r"\d+", text)  # Находим первую последовательность цифр
    return match.group(0) if match else ""


def get_user_file_choice():
    """Запрашивает у пользователя выбор файла для загрузки транзакций."""
    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        user_input = input("Ваш выбор: ")

        if user_input == "1":
            print("Для обработки выбран JSON-файл.")
            return "../data/operations.json", load_transactions, True
        elif user_input == "2":
            print("Для обработки выбран CSV-файл.")
            return "../data/transactions.csv", load_transactions_from_csv, False
        elif user_input == "3":
            print("Для обработки выбран XLSX-файл.")
            return "../data/transactions_excel.xlsx", load_transactions_from_excel, False
        else:
            print("Неверный выбор. Пожалуйста, выберите пункт меню от 1 до 3.")


def filter_by_status(transactions):
    """Фильтрует транзакции по статусу."""
    statuses = ["executed", "canceled", "pending"]

    while True:
        status_input = input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).lower()

        if status_input in statuses:
            filtered_transactions = [
                t for t in transactions if isinstance(t.get("state"), str) and t.get("state").lower() == status_input
            ]
            print(f'Операции отфильтрованы по статусу "{status_input.upper()}".')
            if not filtered_transactions:
                print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
                return []
            else:
                print(f'Найдено {len(filtered_transactions)} транзакций со статусом "{status_input.upper()}".')
                return filtered_transactions
        else:
            print(f'Статус операции "{status_input}" недоступен.')


def apply_additional_filters(filtered_transactions):
    """Применяет дополнительные фильтры к отфильтрованным транзакциям."""
    sort_by_date = input("\nОтсортировать операции по дате? Да/Нет\n").strip().lower() == "да"
    sort_order = None

    if sort_by_date:
        sort_order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()

    only_rubles = input("\nВыводить только рублевые транзакции? Да/Нет\n").strip().lower() == "да"

    filter_description = (
        input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower() == "да"
    )
    search_string = ""

    if filter_description:
        search_string = input("Введите слово для фильтрации по описанию:\n")

    # Применение фильтров
    if only_rubles:
        filtered_transactions = [
            t
            for t in filtered_transactions
            if (
                t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
                or t.get("currency_code") == "RUB"
            )
        ]

    if filter_description and search_string:
        filtered_transactions = filter_transactions(filtered_transactions, search_string)

    # Сортировка транзакций по дате в зависимости от выбора пользователя
    if sort_by_date and filtered_transactions:
        filtered_transactions.sort(key=lambda x: x.get("date"), reverse=(sort_order == "по убыванию"))

    return filtered_transactions


def display_transactions(filtered_transactions, is_json=True):
    """Выводит отфильтрованные транзакции в нужном формате."""
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for transaction in filtered_transactions:
        date_str = transaction.get("date", "Неизвестная дата")

        try:
            date_obj = datetime.fromisoformat(date_str[:-1])
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except ValueError:
            formatted_date = "Неизвестная дата"

        description = transaction.get("description", "Нет описания")

        # Извлечение суммы и валюты в зависимости от формата файла
        if is_json:
            amount = transaction.get("operationAmount", {}).get("amount", "Неизвестная сумма")
            currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "Неизвестная валюта")
        else:  # Для CSV и XLSX
            amount = transaction.get("amount", "Неизвестная сумма")
            currency = transaction.get("currency_code", "Неизвестная валюта")

        from_account_raw = transaction.get("from", "")
        to_account_raw = transaction.get("to", "")

        # Обработка пустого поля 'from'
        if not from_account_raw or not isinstance(from_account_raw, str):
            to_account_number = extract_number(to_account_raw)
            masked_to_account = get_mask_account(to_account_number) if to_account_number else ""
            print(f"{formatted_date} {description}")
            print(f"Счет {masked_to_account}")
            print(f"Сумма: {amount} {currency}\n")
        else:
            from_account_number = extract_number(from_account_raw)
            to_account_number = extract_number(to_account_raw)

            masked_from_account = (
                get_mask_card_number(from_account_number)
                if len(from_account_number) == 16
                else get_mask_account(from_account_number)
            )
            masked_to_account = (
                get_mask_card_number(to_account_number)
                if len(to_account_number) == 16
                else get_mask_account(to_account_number)
            )

            from_display_name = f"{from_account_raw.split()[0]} {masked_from_account} -> " if from_account_raw else ""
            to_display_name = f"{to_account_raw.split()[0]} {masked_to_account}" if to_account_raw else ""

            print(f"{formatted_date} {description}")
            print(f"{from_display_name}{to_display_name}")
            print(f"Сумма: {amount} {currency}\n")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Меню выбора файла и загрузка данных
    file_path, load_function, is_json = get_user_file_choice()

    try:
        transactions = load_function(file_path)

        # Проверка загруженных данных
        print(f"Загружено {len(transactions)} транзакций.")

        # Фильтрация по статусу
        filtered_transactions = filter_by_status(transactions)

        # Применение дополнительных фильтров только если есть отфильтрованные транзакции
        if filtered_transactions:
            filtered_transactions = apply_additional_filters(filtered_transactions)

            # Вывод результата
            if filtered_transactions:
                display_transactions(filtered_transactions, is_json)
            else:
                print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")

    except Exception as e:
        print(f"Произошла ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    main()
