def get_mask_card_number(card_number: str) -> str:
    """Убедимся, что номер карты состоит только из цифр"""
    if not card_number.isdigit() or len(card_number) != 16:
        return "Номер карты должен содержать 16 цифр."

    """Форматируем номер карты"""
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"

    return masked_number


card_number = input("Введите номер карты:")
masked_card_number = get_mask_card_number(card_number)
print(masked_card_number)


def get_mask_account(account_number: str) -> str:
    """Убедимся, что номер счета состоит только из цифр"""
    if not account_number.isdigit() or len(account_number) < 4:
        return "Номер счета должен содержать как минимум 4 цифры."

    """Получаем последние 4 цифры номера счета"""
    masked_account = f"**{account_number[-4:]}"

    return masked_account


account_number = input("Введите номер счета:")
masked_account_number = get_mask_account(account_number)
print(masked_account_number)
