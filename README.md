# Автотесты для Кинопоиска
Автоматизированные UI и API тесты для сайта kinopoisk.ru.

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure
- config

### Струткура:
- ./test - тесты
- ./pages - описание страниц
- ./api - хелперы для работы с API
- ./db - хелперы для работы с БД

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)

## Шаблон для автоматизации тестирования на python

## Структура проекта

kinopoisk-autotests/
├── config/ # Настройки и тестовые данные
├── pages/ # Паттерн PageObject
├── tests/ # Тесты
├── utils/ # Вспомогательные утилиты
├── conftest.py # Фикстуры pytest
├── requirements.txt # Зависимости
└── README.md # Эта документация



### Шаги
1. Склонировать проект 'git clone https://github.com/NadinRostilova/Autotests_kinopoisk.git'
2. Установить зависимости
3. Запустить тесты 'pytest'

## Установка и запуск

### Предварительные требования
* Python 3.8+
* Браузер Chrome

### Установка зависимостей

```bash
pip install -r requirements.txt

### Только UI‑тесты:

bash
pytest tests/test_ui.py --alluredir=./allure-results

### Только API‑тесты:

bash
pytest tests/test_api.py --alluredir=./allure-results

### Все тесты:

bash
pytest --alluredir=./allure-results

Ссылка на финальный проект: https://nadinr.yonote.ru/share/dc60aa73-9678-4a55-98d7-1ae6fbc9e44a