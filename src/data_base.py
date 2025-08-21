import psycopg2
from config import config
from src.api_hh import HHParser


def create_database(db_name: str) -> None:
    """Создание базы данных"""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()


def create_tables(db_name: str) -> None:
    """Созднание таблицы работодателей и вакансий"""
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )""")

            cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                url VARCHAR(255)
            )""")

    conn.close()


def insert_employers(db_name: str) -> None:
    """ Заполнение таблицы работодателей и вакансий"""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
                for employer in employers:
                    cur.execute("INSERT INTO employers (employer_id, name) VALUES (%s, %s)", (employer['id'], employer['name']))
                vacancies = hh_parser.get_vacancies_by_employer_id(employer['id'])

                for vacancy in vacancies:
                    cur.execute("INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url) VALUES (%s, %s, %s, %s, %s, %s)",
                                (vacancy['id'], employer['id'], vacancy['name'], vacancy['salary_from'] if vacancy else None,
                                 vacancy['salary_to'] if vacancy else None, vacancy['url']))

    conn.close()
