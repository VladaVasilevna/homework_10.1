import logging
import os

# Создаем директорию logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл с указанием кодировки
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат записи логов
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Убедимся, что номер карты состоит только из цифр"""
    if not card_number.isdigit() or len(card_number) != 16:
        logger.error(f"Ошибка ввода номера карты: {card_number}")
        return "Номер карты должен содержать 16 цифр."

    logger.info(f"Успешно отформатирован номер карты: {card_number}")
    """Форматируем номер карты"""
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"

    return masked_number


def get_mask_account(account_number: str) -> str:
    """Убедимся, что номер счета состоит только из цифр"""
    if not account_number.isdigit() or len(account_number) < 4:
        logger.error(f"Ошибка ввода номера счета: {account_number}")
        return "Номер счета должен содержать как минимум 4 цифры."

    logger.info(f"Успешно отформатирован номер счета: {account_number}")
    """Получаем последние 4 цифры номера счета"""
    masked_account = f"**{account_number[-4:]}"

    return masked_account
