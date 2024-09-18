# Домашняя работа 10.1

## Описание:

Работа над виджетом банковских операций клиента.

## Работа функций:

1. Функция filter_by_state принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению.

2. Функция sort_by_date принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание).
Функция должна возвращать новый список, отсортированный по дате (date).