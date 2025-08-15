import psycopg2
from src.db_manager import DBManager
from src.data_base import create_tables, insert_employers
from config import config


def main():
    # Параметры подключения и имя базы данных
    db_name = "hh_vacancies"
    params = config()

    try:
        # Создание базы данных (если ещё не создана)
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {db_name}")
        conn.close()

        # Создание таблиц
        create_tables(db_name)

        # Заполнение таблиц данными
        insert_employers(db_name)

        # Инициализация менеджера для работы с БД
        db_manager = DBManager(db_name, params)

        while True:
            print("\nВыберите действие:")
            print("1. Получить список компаний и количество вакансий")
            print("2. Получить список всех вакансий")
            print("3. Получить среднюю зарплату по вакансиям")
            print("4. Получить список вакансий с зарплатой выше средней")
            print("5. Поиск вакансий по ключевому слову")
            print("0. Выход")

            choice = input("> ")

            if choice == "1":
                # Компании и количество вакансий
                companies = db_manager.get_companies_and_vacancies_count()
                print("\nКомпании и количество вакансий:")
                for company, count in companies:
                    print(f"{company}: {count} вакансий")

            elif choice == "2":
                # Все вакансии
                vacancies = db_manager.get_all_vacancies()
                print("\nВсе вакансии:")
                for company, title, salary_from, salary_to, url in vacancies:
                    salary = format_salary(salary_from, salary_to)
                    print(f"{company}: {title} - {salary} | {url}")

            elif choice == "3":
                # Средняя зарплата
                avg_salary = db_manager.get_avg_salary()
                print(f"\nСредняя зарплата: {avg_salary} руб.")

            elif choice == "4":
                # Вакансии с зарплатой выше средней
                vacancies = db_manager.get_vacancies_with_higher_salary()
                print("\nВакансии с зарплатой выше средней:")
                for company, title, salary_from, salary_to, url in vacancies:
                    salary = format_salary(salary_from, salary_to)
                    print(f"{company}: {title} - {salary} | {url}")

            elif choice == "5":
                # Поиск по ключевому слову
                keyword = input("Введите ключевое слово для поиска: ")
                vacancies = db_manager.get_vacancies_with_keyword(keyword)
                print(f"\nРезультаты поиска по слову '{keyword}':")
                for company, title, salary_from, salary_to, url in vacancies:
                    salary = format_salary(salary_from, salary_to)
                    print(f"{company}: {title} - {salary} | {url}")

            elif choice == "0":
                break

            else:
                print("Неверный ввод. Попробуйте снова.")

    except psycopg2.Error as e:
        print(f"Ошибка при работе с PostgreSQL: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


def format_salary(salary_from, salary_to):
    """Форматирование зарплаты для вывода"""
    if salary_from and salary_to:
        return f"{salary_from} - {salary_to} руб."
    elif salary_from:
        return f"от {salary_from} руб."
    elif salary_to:
        return f"до {salary_to} руб."
    else:
        return "не указана"


if __name__ == "__main__":
    main()