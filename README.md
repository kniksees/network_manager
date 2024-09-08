### Что было сделано:
- Написана функция `get_the_tallest_hero` для получения самого высого героя по параметрам. Функция разбита на несколько, для более простого и глубокого тестирования:
  - `get_request` отправляет запрос на сервер и получает ответ.
  - `filter_heroes` фильтрует героев по заданным параметрам.
  - `find_max` ищет самого высокого героя.
- Т.к. API может менятся и подключение к серверу не всегда стабильно:
  - Для большинства тестов использованы моки.
  - В интеграционном тесте проверяем не на конкретный результат, а формат возвращаемых данных.
### Для запуска тестов:
1. Убедитесь, что у вас установлено: python, pytest, allure, pytest-cov(опционально).
2. Клонируйте репозиторий: `git clone https://github.com/kniksees/network_manager`.
3. Перейдите в папку проекта: `cd network_manager`.
4. Используйте:
   - `pytest test_network_manager.py` для запуска простого тестов.
   - `pytest --cov=network_manager test_network_manager.py` если у вас установлен pytest-cov и вам нужен отчет о покрытии.
   - `pytest --alluredir=./reports` and `allure serve ./reports` чтобы посмотреть отчет в allure.
### Покрытие:
<img width="502" alt="Screenshot 2024-09-08 at 23 26 01" src="https://github.com/user-attachments/assets/9f9c9c3b-3207-470c-8e7a-d7c7446d330b">

