import os

import pytest

from src.classes import Save


@pytest.fixture
def path():
    return "test_file.json"


@pytest.fixture
def data():
    return [
        {
            "Название вакансии": "Junior Python разработчик",
            "Регион": {"id": "2", "name": "Санкт-Петербург", "url": "https://api.hh.ru/areas/2"},
            "url": "https://hh.ru/vacancy/96034351",
            "Зарплата от": 50000,
            "Зарплата до": None,
            "Описание": "<highlighttext>Python</highlighttext>. Асинхронное программирование. Знание минимум 1 веб фреймворка. Знание минимум 1 БД и 1 ORM. HTTP И REST. GIT. ",
        }
    ]


def test_saving_vacancies(data, path):
    """Метод тестирует сохранение вакансий в файл"""
    cls_obj = Save("test.json")

    data_json = cls_obj.save_vacancies_to_json(data)
    assert os.path.exists(os.path.join("json_data", "test.json"))
    assert data_json == data
