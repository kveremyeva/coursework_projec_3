import psycopg2
from psycopg2 import sql


class DBManager:
    def __init__(self, db_name, params):
        """
        Инициализация подключения к базе данных
        :param db_name: имя базы данных
        :param params: параметры подключения (host, user, password и т.д.)
        """
        self.conn = psycopg2.connect(dbname=db_name, **params)

    def __del__(self):
        """Закрытие соединения при удалении объекта"""
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return: список кортежей (название компании, количество вакансий)
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.vacancy_id) 
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
                ORDER BY COUNT(v.vacancy_id) DESC
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием компании, названия, зарплаты и ссылки
        :return: список кортежей (компания, вакансия, зарплата от, зарплата до, ссылка)
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                ORDER BY e.name, v.title
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        :return: средняя зарплата (float)
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to)/2)
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            """)
            return round(cur.fetchone()[0], 2)

    def get_vacancies_with_higher_salary(self):
        """
        Получает список вакансий с зарплатой выше средней
        :return: список кортежей с информацией о вакансиях
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE (v.salary_from > %s OR v.salary_to > %s)
                ORDER BY (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0))/2 DESC
            """, (avg_salary, avg_salary))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список вакансий, содержащих ключевое слово в названии
        :param keyword: ключевое слово для поиска
        :return: список кортежей с информацией о вакансиях
        """
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.title ILIKE %s
                ORDER BY e.name, v.title
            """), [f'%{keyword}%'])
            return cur.fetchall()