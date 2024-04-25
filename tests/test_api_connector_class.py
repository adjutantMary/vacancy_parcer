import pytest

from src.classes import ApiConnector


@pytest.fixture
def vacancies_list():
    return [
        {
            "Название вакансии": "Junior Python разработчик",
            "Регион": {"id": "2", "name": "Санкт-Петербург", "url": "https://api.hh.ru/areas/2"},
            "url": "https://hh.ru/vacancy/96034351",
            "Зарплата от": 50000,
            "Зарплата до": None,
            "Описание": "<highlighttext>Python</highlighttext>. Асинхронное программирование. "
            "Знание минимум 1 веб фреймворка. Знание минимум 1 БД и 1 ORM. HTTP И REST. GIT. ",
        }
    ]


def test_api_error():
    """Метод провоцирует ошибку при некорректном API"""
    with pytest.raises(Warning, match="Warning: API url is None"):
        cls_obj = ApiConnector()
        cls_obj.get_vacancies("Python", None)


def test_fetch_data(vacancies_list):
    """Метод проверяет корректность сформированного списка fetch_data"""
    cls_obj = ApiConnector()
    input_data = [{"name": "Junior Python Developer", "salary": None, "snippet": {"requirement": ""}}]
    expected_output = [
        {
            "url": "https://hh.ru/vacancy/None",
            "Зарплата до": 0,
            "Зарплата от": 0,
            "Название вакансии": "Junior Python Developer",
            "Описание": "",
            "Регион": None,
        }
    ]
    assert cls_obj.fetch_data(input_data) == expected_output


def test_empty_list():
    """Метод тестирует обработку пустого списка"""
    input_data = []
    expected_data = []

    cls_obj = ApiConnector()

    assert cls_obj.fetch_data(input_data) == expected_data
