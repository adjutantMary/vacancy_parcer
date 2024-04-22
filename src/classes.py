from abstract_classes import ApiGetter, Saving
import requests, json, os

from path import JSON_DATA


class ApiConnector(ApiGetter):
    """Класс для работы с HeadHunter"""

    def __init__(self, area=113, page=0, in_page=10):
        self.area = area
        self.page = page
        self.in_page = in_page

    def get_vacancies(self, vacancy_name: str, api_url="https://api.hh.ru/vacancies") -> list[dict]:
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
        return data["items"]

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

            if salary == 0 or salary == "Зарплата не указана" or salary is None:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = salary.get("from")
                salary_to = salary.get("to")

            info = {"Название вакансии": name, "Регион": area, "url": url, "Зарплата от": salary_from, "Зарплата до": salary_to}
            vacancies.append(info)
        return vacancies

    @staticmethod
    def filter_by_description(users_vacancies: list[dict], search_param: list):
        filtered_vacancies = []

        for item in users_vacancies:
            for param in search_param:
                if param in item['snippet']['requirement']:
                    filtered_vacancies.append(item)
                    break
        return filtered_vacancies

    @staticmethod
    def get_vacancies_by_salary(filtered_vacancies: list[dict], salary_from: int) -> list:
        sorted_by_salary = []

        for item in filtered_vacancies:
            if item['salary'] is not None:
                if salary_from <= item['salary']['from']:
                    sorted_by_salary.append(item)

        return sorted_by_salary


class Save(Saving):
    """запись файла в json"""

    def __init__(self, file):
        """
        Метод для инициализации пути для файла
        :param file:путь до файла
        """
        self.file = os.path.join(JSON_DATA, file)

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
                with open("vacancies.json", "w+") as file:
                    json.dump(vacancies, file, ensure_ascii=False, indent=2)
            except Exception as error:
                print(f"Ошибка {error}: не удалось сохранить данные в файл")

    def find_data(self) -> list[dict]:
        """
        Метод считывает сохранненные данные в файле
        :return: list[dict]
        """
        try:
            with open(self.file, "r+") as f:
                data = json.load(f)
            return data
        except FileNotFoundError as file_error:
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
                    print(f'Отсортированные вакансии по зарплате: {sorted_vacancies}')
                    return sorted_vacancies
        except Exception as er:
            print(f"Обнаружена ошибка {er} при сортировке вакансий")
