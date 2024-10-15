import logging

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel
from src.operations import count_transactions_by_type, filter_operations
from src.utils import load_transactions, search_transactions

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user_input(prompt: str, valid_options: list) -> str:
    """Получает ввод пользователя с проверкой на корректность."""
    attempts = 3  # Максимальное количество попыток
    while attempts > 0:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        attempts -= 1
        print(
            f"Некорректный ввод. Осталось попыток: {attempts}. "
            f"Пожалуйста, выберите один из: {', '.join(valid_options)}"
        )

    raise ValueError("Превышено максимальное количество попыток ввода.")


def get_status_input(prompt: str, valid_statuses: list) -> str:
    """Получает статус от пользователя с проверкой на корректность."""
    while True:
        status_input = input(prompt).strip().upper()  # Приводим к верхнему регистру для проверки
        if status_input in valid_statuses:
            return status_input
        print(f'Статус операции "{status_input}" недоступен.')


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_input("Пользователь: ", ["1", "2", "3"])

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

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    print(f"Для обработки выбран {file_type}-файл.")

    # Фильтрация по статусу
    statuses = ["EXECUTED", "CANCELED", "PENDING"]

    status_prompt = (
        f"Введите статус, по которому необходимо выполнить фильтрацию.\n"
        f"Доступные для фильтровки статусы: {', '.join(statuses)}\n"
        f"Пользователь: "
    )

    status_input = get_status_input(status_prompt, statuses)

    print(f'Операции отфильтрованы по статусу "{status_input}".')
    filtered_transactions = filter_operations(transactions, status_input)

    # Подсчет операций по категориям (если необходимо)
    categories = [
        "Оплата за интернет",
        "Перевод",
        "Покупка",
        "Оплата за телефон",
    ]

    transaction_counts = count_transactions_by_type(filtered_transactions, categories)

    # Сортировка операций
    sort_by_date = get_user_input("Отсортировать операции по дате? (да/нет)\nПользователь: ", ["да", "нет"])

    if sort_by_date == "да":
        order = get_user_input(
            "Отсортировать по возрастанию или по убыванию?\nПользователь: ", ["по возрастанию", "по убыванию"]
        )
        filtered_transactions.sort(key=lambda x: x.get("date"), reverse=(order == "по убыванию"))

    # Фильтрация по валюте
    only_rub = get_user_input("Выводить только рублевые транзакции? (да/нет)\nПользователь: ", ["да", "нет"])

    if only_rub == "да":
        filtered_transactions = [t for t in filtered_transactions if t.get("currency") == "RUB"]

    # Фильтрация по слову в описании
    filter_by_description = get_user_input(
        "Отфильтровать список транзакций по определенному слову в описании? (да/нет)\n" "Пользователь: ", ["да", "нет"]
    )

    if filter_by_description == "да":
        search_term = input("Введите слово для фильтрации:\nПользователь: ")
        filtered_transactions = search_transactions(filtered_transactions, search_term)

    # Вывод итогового списка транзакций
    print("\nРаспечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

        for transaction in filtered_transactions:
            if isinstance(transaction, dict):  # Проверка типа данных
                date = transaction.get("date", "Дата не указана")
                description = transaction.get("description", "Описание не указано")
                amount = transaction.get("amount", 0)
                currency = transaction.get("currency", "неизвестная валюта")

                print(f"{date} {description}\nСумма: {amount} {currency}\n")
            else:
                logger.error(f"Ошибка: ожидался словарь транзакции, но получен {type(transaction).__name__}.")

        # Вывод количества операций по категориям
        print("\nКоличество операций по категориям:")

        # Убедитесь, что transaction_counts — это словарь перед использованием .items()
        if isinstance(transaction_counts, dict):
            for category, count in transaction_counts.items():
                print(f"{category}: {count}")
        else:
            logger.error("Ошибка: ожидался словарь для подсчета операций по категориям.")


if __name__ == "__main__":
    main()
