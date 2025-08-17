# Проект: Анализ вакансий с HeadHunter (hh.ru)

Проект для сбора и анализа данных о вакансиях и компаниях с сайта hh.ru с последующим хранением в PostgreSQL и удобным управлением через Python-интерфейс.

## Основные функции
- Парсинг данных о компаниях и вакансиях через API hh.ru
- Хранение данных в PostgreSQL
- Анализ вакансий через класс `DBManager`
- Гибкие запросы к данным (фильтрация, статистика)


### 2. Настройка БД
Создайте файл `database.ini` в корне проекта:
```python
[postgresql]
host = localhost
port = 5432
user = your_username
password = your_password
```

## Методы DBManager
| Метод | Описание | Пример вывода |
|-------|----------|---------------|
| `get_companies_and_vacancies_count()` | Количество вакансий по компаниям | Яндекс: 42 |
| `get_all_vacancies()` | Все вакансии с зарплатами | Python-разработчик: 120000 руб. |
| `get_avg_salary()` | Средняя зарплата | 98500 руб. |
| `get_vacancies_with_higher_salary()` | Вакансии с зарплатой выше средней | Team Lead: 200000 руб. |
| `get_vacancies_with_keyword()` | Поиск по ключевым словам | "Data Scientist" |


