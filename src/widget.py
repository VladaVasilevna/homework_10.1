def mask_account_card(account_info: str) -> str:
    """Функция маскировки карты или счета"""
    account_type, account_number = account_info.split(maxsplit=1)

    if account_type in ["Visa", "Maestro"]:  # Для карт
        if len(account_number) != 16 or not account_number.isdigit():
            return "Некорректный номер карты"

        masked_number = f"{account_number[:4]} {account_number[4:6]}** **** {account_number[12:]}"
        return f"{account_type} {masked_number}"

    elif account_type == "Счет":  # Для счета
        if not account_number.isdigit():
            return "Некорректный номер счета"

        masked_number = f"**{account_number[-4:]}"
        return f"{account_type} {masked_number}"

    else:
        return "Неизвестный тип карты или счета"


def get_date(date_string: str) -> str:
    """Функция преобразования строки в дату в формате DD.MM.YYYY"""
    parts = date_string.split()

    if len(parts) != 3:
        return "Некорректная дата"

    day, month_str, year = parts

    months = {
        "января": "01",
        "февраля": "02",
        "марта": "03",
        "апреля": "04",
        "мая": "05",
        "июня": "06",
        "июля": "07",
        "августа": "08",
        "сентября": "09",
        "октября": "10",
        "ноября": "11",
        "декабря": "12",
    }

    if month_str not in months:
        return "Некорректная дата"

    month = months[month_str]

    # Проверка на корректность дня
    if not day.isdigit() or int(day) < 1 or int(day) > 31:
        return "Некорректная дата"

    # Проверка на корректность года
    if len(year) != 4 or not year.isdigit():
        return "Некорректная дата"

    # Форматируем день с ведущим нулем
    day = day.zfill(2)

    return f"{day}.{month}.{year}"
