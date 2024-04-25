import json
import os
from typing import Any

import requests

from src.abstract_classes import ApiGetter, Saving


class ApiConnector(ApiGetter):
    """Класс для работы с HeadHunter"""

    def __init__(self, area=113, page=0, in_page=50):
        self.area = area
        self.page = page
        self.in_page = in_page

    def get_vacancies(self, vacancy_name: str, api_url: Any) -> list[dict]:
        """
        Метод получает вакансии по API и сохраняет их в виде JSON - списка
        :param vacancy_name:название вакансии
        :param api_url:ссылки на API
        :return:
        """
        vacancy_param = {
            "text": vacancy_name,
            "area": self.area,
            "per_page": self.in_page,
            "page": self.page,
        }

        if api_url is None:
            raise Warning("Warning: API url is None")
        response = requests.get(api_url, params=vacancy_param, headers={"apikey": api_url})
        data = response.json()
        return self.fetch_data(data["items"])

    # проверить не получаем ли пустой список, получаем ли данные в определенном формате

    @staticmethod
    def fetch_data(data) -> list[dict]:
        """
        Метод оформляет информацию о вакансиях в удобном виде
        :param data:
        :return:
        """
        vacancies = []
        for key in data:
            name = key.get("name")
            area = key.get("area")
            url = f'https://hh.ru/vacancy/{key.get("id")}'
            salary = key.get("salary")
            if salary is None:
                salary = {}

            snippet = key.get("snippet")
            if snippet is None:
                snippet = {}

            description = snippet.get("requirement")
            if description is None:
                description = "Описание отсутствует"

            salary_from = salary.get("from")
            salary_to = salary.get("to")

            if salary_from is None:
                salary_from = 0

            if salary_to is None:
                salary_to = 0

            info = {
                f"Название вакансии": name,
                "Регион": area,
                "url": url,
                f"Зарплата от": salary_from,
                "Зарплата до": salary_to,
                f"Описание": description,
            }
            vacancies.append(info)
        return vacancies

    @staticmethod
    def filter_by_description(users_vacancies: list[dict], search_param: list):
        filtered_vacancies = []

        for item in users_vacancies:
            for param in search_param:
                try:
                    if param.lower() in item["Описание"].lower():
                        filtered_vacancies.append(item)
                except Exception as error:
                    print(f"{error} Невозможно провести фильтрацию," f" так как поисковый запрос не был найден")

        return filtered_vacancies

    @staticmethod
    def get_vacancies_by_salary(filtered_vacancies: list[dict], salary_from: int) -> list:
        sorted_by_salary = []

        for item in filtered_vacancies:
            if salary_from <= item["Зарплата от"]:
                sorted_by_salary.append(item)

        return sorted_by_salary


class Save(Saving):
    """запись файла в json"""

    def __init__(self, file):
        """
        Метод для инициализации пути для файла
        :param file:путь до файла
        """
        self.file = os.path.join("json_data", file)

    def save_vacancies_to_json(self, vacancies):
        """
        Метод класса, который сохраняет полученные вакансии в JSON файл
        :param vacancies: список вакансий
        :return: JSON файл
        """

        user_directory = os.path.dirname(self.file)

        if not os.path.exists(user_directory):
            try:
                os.makedirs(user_directory)
            except OSError as os_error:
                print(f"Невозможно создать директорию. Возникла ошибка {os_error}")
        else:
            try:
                with open(self.file, "w+", encoding="utf-8") as file:
                    json.dump(vacancies, file, ensure_ascii=False, indent=2)
                    return vacancies
            except Exception as error:
                print(f"Ошибка {error}: не удалось сохранить данные в файл")

    def find_data(self) -> list[dict]:
        """
        Метод считывает сохраненные данные в файле
        :return: list[dict]
        """
        try:
            with open(self.file, "r+") as f:
                data = json.load(f)
            return data
        except Exception as file_error:
            print(f"{file_error}: Файл не был найден в директории")

    def remove_vacancies(self):
        """
        Метод удаляет вакансию, если у нее не указана з/п или равна 0
        """

        try:
            loaded_data = self.find_data()
            for item in loaded_data:
                if item["salary_from"] != 0 or item["salary_to"] != 0:
                    sorted_vacancies = self.save_vacancies_to_json(item)
                    print(f"Отсортированные вакансии по зарплате: {sorted_vacancies}")
                    return sorted_vacancies
        except Exception as er:
            print(f"Обнаружена ошибка {er} при сортировке вакансий")
