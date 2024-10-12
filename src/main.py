from data_loader import load_transactions_from_csv, load_transactions_from_excel
from operations import filter_operations
from utils import load_transactions


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")

    if choice == "1":
        file_path = "data/operations.json"
        transactions = load_transactions(file_path)
        file_type = "JSON"
    elif choice == "2":
        file_path = "data/transactions.csv"
        transactions = load_transactions_from_csv(file_path)
        file_type = "CSV"
    elif choice == "3":
        file_path = "data/transactions_excel.xlsx"
        transactions = load_transactions_from_excel(file_path)
        file_type = "XLSX"
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    print(f"Для обработки выбран {file_type}-файл.")

    # Фильтрация по статусу
    statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        status_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            f"Доступные для фильтровки статусы: {', '.join(statuses)}\nПользователь: "
        )

        status_input_upper = status_input.upper()

        if status_input_upper in statuses:
            print(f'Операции отфильтрованы по статусу "{status_input_upper}".')
            filtered_transactions = filter_operations(transactions, status_input_upper)
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    # Сортировка операций
    sort_by_date = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()

    if sort_by_date == "да":
        order = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        if order == "по возрастанию":
            filtered_transactions.sort(key=lambda x: x.get("date"))
        elif order == "по убыванию":
            filtered_transactions.sort(key=lambda x: x.get("date"), reverse=True)

    # Фильтрация по валюте
    only_rub = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()

    if only_rub == "да":
        filtered_transactions = [t for t in filtered_transactions if t.get("currency") == "RUB"]

    # Фильтрация по слову в описании
    filter_by_description = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )

    if filter_by_description == "да":
        search_term = input("Введите слово для фильтрации:\nПользователь: ")
        filtered_transactions = filter_operations(filtered_transactions, search_term)

    # Вывод итогового списка транзакций
    print("\nРаспечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

        for transaction in filtered_transactions:
            date = transaction.get("date", "Дата не указана")
            description = transaction.get("description", "Описание не указано")
            amount = transaction.get("amount", 0)
            currency = transaction.get("currency", "неизвестная валюта")

            print(f"{date} {description}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
