import requests


class HHParser:
    def get_employers(self):
        """ Получение всех работодателей """
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get("https://api.hh.ru/employers", params=params)
        response.raise_for_status()
        data =  response.json()["items"]
        employers = []
        for employer in data:
            employers.append({"id": employer["id"], "name": employer["name"]})
        return employers

    def get_vacancies_by_employer_id(self, employer_id):
        """ Получение списка вакансий для конкретного работодателя"""
        params = {"employer_id": employer_id, "per_page": 50}
        response = requests.get(" https://api.hh.ru/vacancies", params=params)
        data =  response.json()["items"]
        vacancies = []
        for vacancy in data:
            if vacancy["salary"]:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
            else:
                salary_from = 0
                salary_to = 0
            vacancies.append({"id": vacancy["id"], "name": vacancy["name"], "salary_from": salary_from, "salary_to": salary_to,
                "url": vacancy["alternate_url"]})
        return vacancies


