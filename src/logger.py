import logging
import os

# Создаем директорию logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка логгера
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл с указанием кодировки
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат записи логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)

# Пример записи логов (можно удалить или изменить по необходимости)
logger.debug("Это сообщение для отладки")
logger.info("Информационное сообщение")
logger.warning("Предупреждение — нужно проверить, всё ли в порядке")
logger.error("Ошибка! Что-то пошло не так")
logger.critical("Критическая ошибка!")
