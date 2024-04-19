from abc import ABC, abstractmethod


class ApiGetter(ABC):

    @abstractmethod
    def _get_vacancies(self, vacancy_name: str, api_url: str) -> list:
        """
        Класс принимает api адрес вакансий
        :param api_url:
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def fetch_data(data):
        pass


class Saving(ABC):
    """Абстрактный класс для работы с JSON файлом"""

    @abstractmethod
    def save_vacancies_to_json(self, vacancies: list):
        """
        Метод загружает вакансии и сохраняет в формате JSON
        :param vacancies: список вакансий
        :return: JSON файл
        """
        pass

    @abstractmethod
    def find_data(self):
        """
        Метод по поиску данных из файла по указанным критериям
        :return: list
        """
        pass

    @abstractmethod
    def remove_vacancies(self):
        """
        Метод удаляет вакансию из списка
        """
        pass
