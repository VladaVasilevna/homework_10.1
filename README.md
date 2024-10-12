# Домашняя работа

## Описание:

Работа над виджетом банковских операций клиента.

## Работа функций:

1. Функция маскировки номера банковской карты get_mask_card_number принимает на вход номер карты и возвращает ее маску XXXX XX** **** XXXX.
2. Функция маскировки номера банковского счета get_mask_account принимает на вход номер счета и возвращает его маску **XXXX.
3. Функция mask_account_card, которая умеет обрабатывать информацию как о картах, так и о счетах.
4. Функция get_date, которая принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
5. Функция filter_by_state принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению.
6. Функция sort_by_date принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание).
Функция должна возвращать новый список, отсортированный по дате (date).
7. Функция filter_by_currency, которая принимает на вход список словарей, представляющих транзакции. Функция должна возвращать итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной (например, USD).
8. Генератор transaction_descriptions, который принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
9. Генератор card_number_generator, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX.
10. Декоратор log, который автоматически регистрирует детали выполнения функций, такие как время вызова, имя функции, передаваемые аргументы, результат выполнения и информация об ошибках.
11. Функция load_transactions, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
12. Функция convert_to_rub, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float. Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли.
13. Функция load_transactions_from_csv для считывания финансовых операций из CSV принимает путь к файлу CSV в качестве аргумента и выдает список словарей с транзакциями.
14. Функция load_transactions_from_excel для считывания финансовых операций из Excel принимает путь к файлу Excel в качестве аргумента и выдает список словарей с транзакциями.

## Требования к окружению:

   - Установите:

     ```Python 3.8+```

## Установка проекта:

- Склонировать репозиторий:

       ```bash git clone https://github.com/VladaVasilevna/homework_10.1```

- Перейти в директорию проекта:

       ```bash cd ваш-проект```

- (Если требуется) Создать и активировать виртуальное окружение:

  ```bash python -m venv venv source venv/bin/activate  # или venv\Scripts\activate для Windows```

- Склонировать репозиторий:

       ```bash git clone https://github.com/VladaVasilevna/homework_10.1```

- Перейти в директорию проекта:

       ```bash cd ваш-проект```

- (Если требуется) Создать и активировать виртуальное окружение:

       ```bash python -m venv venv source venv/bin/activate  # или venv\Scripts\activate для Windows```

## Установка зависимостей:

     ```bash pip install -r requirements.txt```



## Как запустить проект:

     ```bash python manage.py runserver```

## Тестирование
- Для всех фунцкций в проекте написаны тесты.
- Использованы фикстуры для создания необходимых входных данных для тестов.
- Использована параметризация в тестах для обеспечения тестирования функциональности с различными входными данными.
- Для декораторов применяется фикстура capsys, которая позволяет перехватывать вывод данных в консоль.
- Использованы Mock и patch.
- Создан отчет HTML.
